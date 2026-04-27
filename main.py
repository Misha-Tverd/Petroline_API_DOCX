from __future__ import annotations

import json
from pathlib import Path

from api_client import PetrolineApiError, PetrolineClient
from config import get_settings
from mapper import map_transactions_to_limit_card, transaction_matches_driver
from utils import sanitize_filename_part
from word_generator import generate_limit_card_docx


def load_transactions_from_sample(path: Path) -> list[dict]:
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if isinstance(data, dict) and isinstance(data.get("items"), list):
        return data["items"]
    if isinstance(data, list):
        return data
    raise ValueError("Sample data must be a list or a dict with key 'items'.")


def fetch_transactions_from_api(settings) -> list[dict]:
    client = PetrolineClient(
        base_url=settings.petroline_base_url,
        login=settings.petroline_login,
        password=settings.petroline_password,
        timeout=settings.petroline_timeout,
        token=settings.petroline_token or None,
    )

    payload = client.build_trk_transactions_payload(
        date_from=settings.date_from,
        date_to=settings.date_to,
        subdivision_id=settings.subdivision_id,
        take=settings.take,
    )
    return client.get_trk_transactions(payload)


def build_limit_card_output_path(settings, context: dict) -> Path:
    date_part = context["date"].replace(".", "-")
    vehicle_part = sanitize_filename_part(context["vehicle"], fallback="vehicle")
    driver_part = sanitize_filename_part(context["recipient_name"], fallback="driver")
    file_name = f"{date_part}_{vehicle_part}_{driver_part}.docx"
    return settings.output_dir / "limit_cards" / file_name


def main() -> None:
    settings = get_settings()

    try:
        if settings.use_sample_data:
            transactions = load_transactions_from_sample(settings.sample_data_path)
        else:
            transactions = fetch_transactions_from_api(settings)
    except (OSError, ValueError, json.JSONDecodeError, PetrolineApiError) as exc:
        print(f"[ERROR] {exc}")
        return

    matched = [
        transaction
        for transaction in transactions
        if transaction_matches_driver(transaction, settings.target_driver)
    ]

    if not matched:
        print(f"[INFO] no transactions found for {settings.target_driver}")
        return

    context = map_transactions_to_limit_card(matched, settings)
    output_path = build_limit_card_output_path(settings, context)
    generate_limit_card_docx(context, output_path)
    print(f"[OK] created limit card: {output_path}")


if __name__ == "__main__":
    main()
