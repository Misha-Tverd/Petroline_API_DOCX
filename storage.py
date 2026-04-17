from __future__ import annotations

import json
from pathlib import Path



def _load_json_list(path: Path) -> list:
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        return []

    try:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                return []
            data = json.loads(content)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []



def append_missing_record(log_path: Path, record_id: int, missing_fields: list[str], raw_data: dict) -> None:
    data = _load_json_list(log_path)
    data.append(
        {
            "id": record_id,
            "missing_fields": missing_fields,
            "raw": raw_data,
        }
    )
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)



def load_processed_ids(path: Path) -> set[int]:
    data = _load_json_list(path)
    result: set[int] = set()
    for item in data:
        try:
            result.add(int(item))
        except (TypeError, ValueError):
            continue
    return result



def save_processed_id(path: Path, record_id: int) -> None:
    data = _load_json_list(path)
    if record_id not in data:
        data.append(record_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
