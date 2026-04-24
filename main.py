from pathlib import Path

from mapper import map_transaction_to_doc_data
from storage import read_json_list, write_json_list
from validator import get_missing_required_fields

DATA_PATH = Path("data/test_data.json")
MISSING_RECORDS_PATH = Path("data/missing_records.json")


def collect_missing_records(records: list[dict]) -> list[dict]:
    missing_records = []

    for record in records:
        doc_data = map_transaction_to_doc_data(record)
        missing_fields = get_missing_required_fields(doc_data)

        if missing_fields:
            missing_records.append(
                {
                    "id": record.get("id"),
                    "missing_fields": missing_fields,
                    "record": record,
                }
            )

    return missing_records


def main() -> None:
    records = read_json_list(DATA_PATH)

    if not records:
        print("No records to process.")
        write_json_list([], MISSING_RECORDS_PATH)
        return

    missing_records = collect_missing_records(records)
    write_json_list(missing_records, MISSING_RECORDS_PATH)

    if not missing_records:
        print("All required fields are present.")
        return

    print(f"Records with missing fields: {len(missing_records)}")
    for item in missing_records:
        print(f"Record {item['id']}: {', '.join(item['missing_fields'])}")


if __name__ == "__main__":
    main()
