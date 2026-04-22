REQUIRED_FIELDS = [
    "id",
    "personName",
    "transportName",
    "fuelName",
    "value"
]

def get_missing_required_fields(record: dict) -> list[str]:
    if record():
        id = record.get(REQUIRED_FIELDS)
    return []