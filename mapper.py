def map_transaction_to_doc_data(record: dict) -> dict: 
    return {
        "id": record.get("id"),
        "driver": record.get("personName"),
        "vehicle": record.get("transportName"),
        "fuel": record.get("fuelName"),
        "amount": record.get("value"),
        "date": record.get("date"),
        "azs": record.get("azsName"),
        "company": record.get("departmentName"),
        "department": record.get("departmentName"),
        "legal_entity_code": "31328990"

    }
