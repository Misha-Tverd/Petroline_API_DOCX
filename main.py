from storage import read_json_list
import requests

# auth_url = "https://apiv2.petroline.in.ua/api/Auth/token"

# headers = {
#     "login": "12345abcdef",
#     "password": "bearer"
# }

# response = requests.post(auth_url, headers=headers)
# print(response.status_code)
# print(response.text)


url = "https://apiv2.petroline.in.ua/api/TrkTransactions/list"

headers = {
    "Authorization": "Bearer 12345abcdef",
    "Content-Type": "application/json"
}

payload = {
    "page": 1,
    "pageSize": 10
}
response = requests.post(url, json=payload, headers=headers)

print(response.status_code)
print(response.text)

def main():
    data = read_json_list("data/test_data.json")
    

main()