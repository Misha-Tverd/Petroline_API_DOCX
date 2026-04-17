from __future__ import annotations

from dataclasses import dataclass

import requests


class PetrolineApiError(Exception):
    pass


@dataclass
class PetrolineClient:
    base_url: str
    login: str
    password: str
    timeout: int = 30
    token: str | None = None

    def _headers(self) -> dict[str, str]:
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

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

        self.token = token
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

        url = f"{self.base_url}/api/TrkTransactions/list"
        response = requests.post(url, json=payload, headers=self._headers(), timeout=self.timeout)
        if response.status_code >= 400:
            raise PetrolineApiError(f"Transactions request failed: {response.status_code} {response.text}")

        data = response.json()
        if not isinstance(data, list):
            raise PetrolineApiError(f"Unexpected transactions response: {data}")
        return data
