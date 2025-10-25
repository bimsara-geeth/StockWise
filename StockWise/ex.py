import requests

base_url = "https://www.cse.lk/api/"
endpoint = "tradeSummary"

data = {"symbol": "LOLC.N0000"}

response = requests.post(base_url + endpoint)

print(f"Status code: {response.status_code}")
print(response.json())  # Prints the response as a Python dictionary