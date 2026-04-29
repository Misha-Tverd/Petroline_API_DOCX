def filter_all_required_fields(data: list) -> list:
    required_fields = {
        "date_start": "20.04.2026",
        "date_end": "28.04.2026",
        "amount": int|float,
        "driver": "personName",
        "vehicle": "transportName",
        "fuel": "fuelName",
        "azs": "azsName",
        "company": "departmentName",
        "department": "departmentName",
    }
