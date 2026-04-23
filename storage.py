from pathlib import Path 
import json


def read_json_list(path: Path) -> list:
    path = Path(path)

    if not path.is_file():
          return []
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
         print(f"Error: The file {path.name} is corrupted or empty.")


def write_json_list(data: list) -> None:
    path = Path("data/missing_records.json") 
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)