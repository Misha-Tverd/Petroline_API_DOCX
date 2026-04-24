import json
from pathlib import Path


DEFAULT_MISSING_RECORDS_PATH = Path("data/missing_records.json")


def read_json_list(path: str | Path) -> list:
    path = Path(path)

    if not path.is_file():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print(f"Error: The file {path.name} is corrupted or empty.")
        return []

    if not isinstance(data, list):
        print(f"Error: The file {path.name} must contain a JSON list.")
        return []

    return data


def write_json_list(
    data: list,
    path: str | Path = DEFAULT_MISSING_RECORDS_PATH,
) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
