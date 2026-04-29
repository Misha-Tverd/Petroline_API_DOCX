REQUIRED_FIELDS = [
    "id",
    "driver",
    "vehicle",
    "fuel",
    "amount",
    "date",
    "azs",
    "company",
    "department"
]

def get_missing_required_fields(record: dict) -> list[str]:
    missing_fields = []
    for field in REQUIRED_FIELDS:
        if field not in record or record[field] is None:
            missing_fields.append(field)
    return missing_fields
    missing_fields = []
    for field in REQUIRED_FIELDS:
        value = record.get(field)
        if value is None or str(value).strip() == "":
            missing_fields.append(field)
    return missing_fields