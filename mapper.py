def map_transaction_to_doc_data(record: dict) -> dict: 
    return {
        "driver": record.get("personName"),
        "vehicle": record.get("transportName"),
        "fuel": record.get("fuelName"),
        "amount": record.get("value"),
        "data": record.get("data"),
        "azs": record.get("azsName")
    }
