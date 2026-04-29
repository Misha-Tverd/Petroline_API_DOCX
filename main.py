from storage import read_json_list, write_missing_records, test_data
from validator import get_missing_required_fields
import json
import requests
from mapper import map_transaction_to_doc_data 
from validator import get_missing_required_fields

url = "https://apiv2.petroline.in.ua/api/TrkTransactions/list"

token = "ТУТ_ТВІЙ_ТОКЕН"

headers = {
    "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJUaWNrZXQiOiJBNDFBRTBGQS1EMjM0LTQ5NjEtQjQ4Qi1CNDQ1MzIzMUQzQ0EiLCJuYmYiOjE3NzczNzU3NDYsImV4cCI6MTc3NzU0ODU0NiwiaXNzIjoiaXNzdWVyQ2xvbmUiLCJhdWQiOiJhdWRpZW5jZUNsb25lIn0.U6VW2SV0j0w55PnXPAglb6ixyKC21fuD7MIrAJ4Dxig",
    "PETROLINE_TIMEOUT": "30",
    "Content-Type": "application/json",
    "accept": "application/json",
}

payload = {
    "filter": {
        "date": {
            "start": "2026-04-26T00:00:00Z",
            "end": "2026-04-28T23:59:59Z"
        }
    },
    "loadOption": {
        "skip": 0,
        "take": 30
    }
}

response = requests.post(url, json=payload, headers=headers)
test_data(response.json())
mapped_data = map_transaction_to_doc_data(response.json()[0])
print("MAPPED DATA:", mapped_data)


# def main():
#     data = read_json_list("data/test_data.json")
#     requiremt_fields = map_transaction_to_doc_data(data[0])
#     missed_fields = get_missing_required_fields(requiremt_fields)
#     if missed_fields == []:
#         print("All required fields are present.")
#     else:
#         write_json_list(missed_fields)
#         print("Missed fields:", missed_fields)
        



# if __name__ == "__main__":
#     main()