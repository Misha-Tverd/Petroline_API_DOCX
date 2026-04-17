from __future__ import annotations

import json
import time
from pathlib import Path

from api_client import PetrolineClient, PetrolineApiError
from config import get_settings
from mapper import map_transaction_to_word_tags
from storage import append_missing_record, load_processed_ids, save_processed_id
from utils import build_output_paths
from validators import validate_required_fields
from word_generator import generate_docx



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
    )

    payload = client.build_trk_transactions_payload(
        date_from=settings.date_from,
        date_to=settings.date_to,
        subdivision_id=settings.subdivision_id,
        take=settings.take,
    )
    return client.get_trk_transactions(payload)



def process_one_transaction(transaction: dict, settings, processed_ids: set[int]) -> None:
    record_id = int(transaction.get("id", 0))
    if record_id in processed_ids:
        print(f"[SKIP] already processed: {record_id}")
        return

    mapped = map_transaction_to_word_tags(transaction)
    is_valid, missing_fields = validate_required_fields(mapped)

    if not is_valid and settings.retry_seconds > 0:
        print(f"[WAIT] record {record_id}, retry after {settings.retry_seconds}s")
        time.sleep(settings.retry_seconds)
        mapped = map_transaction_to_word_tags(transaction)
        is_valid, missing_fields = validate_required_fields(mapped)

    if not is_valid:
        append_missing_record(
            log_path=settings.missing_log_path,
            record_id=record_id,
            missing_fields=missing_fields,
            raw_data=transaction,
        )
        print(f"[LOG] missing fields for record {record_id}: {missing_fields}")
        return

    vehicle_output_path, driver_output_path = build_output_paths(settings.output_dir, transaction)
    generate_docx(settings.template_path, mapped, vehicle_output_path)
    generate_docx(settings.template_path, mapped, driver_output_path)
    save_processed_id(settings.processed_ids_path, record_id)
    processed_ids.add(record_id)
    print(f"[OK] created docs for record {record_id}")



def main() -> None:
    settings = get_settings()
    processed_ids = load_processed_ids(settings.processed_ids_path)

    try:
        if settings.use_sample_data:
            transactions = load_transactions_from_sample(settings.sample_data_path)
        else:
            transactions = fetch_transactions_from_api(settings)
    except (OSError, ValueError, json.JSONDecodeError, PetrolineApiError) as exc:
        print(f"[ERROR] {exc}")
        return

    if not transactions:
        print("[INFO] no transactions found")
        return

    for transaction in transactions:
        process_one_transaction(transaction, settings, processed_ids)


if __name__ == "__main__":
    main()
