from storage import read_json_list
from validator import get_missing_required_fields
import json
import requests


url = "https://apiv2.petroline.in.ua/api/TrkTransactions/list"

token = "ТУТ_ТВІЙ_ТОКЕН"

headers = {
    "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJUaWNrZXQiOiI0QzQyQ0Q5Ni1BQ0VBLTQ1NTctQjg4My0yMTM4ODhDNjVFMTUiLCJuYmYiOjE3NzY4NjM5NzYsImV4cCI6MTc3NzAzNjc3NiwiaXNzIjoiaXNzdWVyQ2xvbmUiLCJhdWQiOiJhdWRpZW5jZUNsb25lIn0.Zr6ms6SthANrC-zdUfNODetvDpzrrPnsCQVPQRbyN2s",
    "Content-Type": "application/json",
    "accept": "application/json",
}

payload = {
    "filter": {
        "date": {
            "start": "2026-04-01T00:00:00Z",
            "end": "2026-04-22T23:59:59Z"
        }
    },
    "loadOption": {
        "skip": 0,
        "take": 1
    }
}

response = requests.post(url, json=payload, headers=headers)

print("STATUS:", response.status_code)
print("TEXT:", response.text)
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJUaWNrZXQiOiI0QzQyQ0Q5Ni1BQ0VBLTQ1NTctQjg4My0yMTM4ODhDNjVFMTUiLCJuYmYiOjE3NzY4NjM5NzYsImV4cCI6MTc3NzAzNjc3NiwiaXNzIjoiaXNzdWVyQ2xvbmUiLCJhdWQiOiJhdWRpZW5jZUNsb25lIn0.Zr6ms6SthANrC-zdUfNODetvDpzrrPnsCQVPQRbyN2s

# def main():
#     data = read_json_list("data/test_data.json")
#     id = data[1].get("id")
#     print(id)
#     missing_fields = get_missing_required_fields(data)



# main()