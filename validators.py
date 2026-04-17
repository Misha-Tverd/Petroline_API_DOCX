from __future__ import annotations

CRITICAL_FIELDS = [
    "driver",
    "vehicle",
    "liters",
]



def validate_required_fields(mapped_data: dict) -> tuple[bool, list[str]]:
    missing_fields: list[str] = []

    for field in CRITICAL_FIELDS:
        value = mapped_data.get(field)
        if value is None or value == "":
            missing_fields.append(field)

    return len(missing_fields) == 0, missing_fields
