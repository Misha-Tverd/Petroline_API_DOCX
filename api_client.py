from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from datetime import UTC, datetime

import requests


class PetrolineApiError(Exception):
    pass


def _normalize_bearer_token(token: str | None) -> str | None:
    if not token:
        return None
    token = token.strip()
    if token.lower().startswith("bearer "):
        token = token[7:].strip()
    return token or None


def _jwt_expiration(token: str | None) -> datetime | None:
    token = _normalize_bearer_token(token)
    if not token or token.count(".") != 2:
        return None

    try:
        payload = token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        data = json.loads(base64.urlsafe_b64decode(payload))
        exp = data.get("exp")
        return datetime.fromtimestamp(exp, UTC) if exp else None
    except (ValueError, TypeError, json.JSONDecodeError):
        return None


@dataclass
class PetrolineClient:
    base_url: str
    login: str
    password: str
    timeout: int = 30
    token: str | None = None

    def __post_init__(self) -> None:
        self.token = _normalize_bearer_token(self.token)

    def _headers(self) -> dict[str, str]:
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _token_expired(self) -> bool:
        expires_at = _jwt_expiration(self.token)
        return bool(expires_at and expires_at <= datetime.now(UTC))

    def _ensure_token_is_current(self) -> None:
        if self._token_expired():
            expires_at = _jwt_expiration(self.token)
            expired_at = expires_at.strftime("%Y-%m-%d %H:%M:%S") if expires_at else "unknown time"
            raise PetrolineApiError(f"PETROLINE_TOKEN is expired. Token expired at {expired_at} UTC.")

    def authenticate(self) -> str:
        url = f"{self.base_url}/api/Auth/token"
        payload = {
            "login": self.login,
            "password": self.password,
        }
        response = requests.post(url, json=payload, headers=self._headers(), timeout=self.timeout)
        if response.status_code >= 400:
            raise PetrolineApiError(f"Auth failed: {response.status_code} {response.text}")

        data = response.json()
        token = data.get("token") or data.get("accessToken") or data.get("access_token")
        if not token:
            raise PetrolineApiError(f"Token not found in auth response: {data}")

        self.token = _normalize_bearer_token(token)
        self._ensure_token_is_current()
        return token

    def build_trk_transactions_payload(
        self,
        *,
        date_from: str,
        date_to: str,
        subdivision_id: int | None = None,
        skip: int = 0,
        take: int = 100,
    ) -> dict:
        date_filters = [
            {
                "operatorType": 0,
                "operands": None,
                "field": "date",
                "filterType": 6,
                "value": date_from,
            },
            {
                "operatorType": 0,
                "operands": None,
                "field": "date",
                "filterType": 3,
                "value": date_to,
            },
        ]

        operands = [
            {
                "operatorType": 1,
                "operands": date_filters,
                "field": None,
                "filterType": 0,
                "value": None,
            }
        ]

        if subdivision_id is not None:
            operands.append(
                {
                    "operatorType": 2,
                    "operands": [
                        {
                            "operatorType": 0,
                            "operands": None,
                            "field": "subdivisionId",
                            "filterType": 1,
                            "value": subdivision_id,
                        }
                    ],
                    "field": None,
                    "filterType": 0,
                    "value": None,
                }
            )

        return {
            "where": {
                "operatorType": 1,
                "operands": operands,
                "field": None,
                "filterType": 0,
                "value": None,
            },
            "orderBy": [
                {
                    "field": "date",
                    "order": 0,
                }
            ],
            "skip": skip,
            "take": take,
        }

    def get_trk_transactions(self, payload: dict) -> list[dict]:
        if not self.token:
            self.authenticate()
        elif self._token_expired() and self.login and self.password:
            self.token = None
            self.authenticate()
        self._ensure_token_is_current()

        url = f"{self.base_url}/api/TrkTransactions/list"
        response = requests.post(url, json=payload, headers=self._headers(), timeout=self.timeout)
        if response.status_code >= 400:
            raise PetrolineApiError(f"Transactions request failed: {response.status_code} {response.text}")

        data = response.json()
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            for key in ("items", "data", "rows", "result"):
                items = data.get(key)
                if isinstance(items, list):
                    return items
        raise PetrolineApiError(f"Unexpected transactions response: {data}")
