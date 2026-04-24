FIELD_MAPPING = {
    "id": "id",
    "driver": "personName",
    "vehicle": "transportName",
    "fuel": "fuelName",
    "amount": "value",
    "date": "date",
    "azs": "azsName",
}


def map_transaction_to_doc_data(record: dict) -> dict:
    return {
        doc_field: record.get(api_field)
        for doc_field, api_field in FIELD_MAPPING.items()
    }
