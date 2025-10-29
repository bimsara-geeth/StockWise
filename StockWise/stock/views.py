from django.shortcuts import render
import requests

base_url = "https://www.cse.lk/api/"
endpoint = "tradeSummary"

response = requests.post(base_url + endpoint)
file = response.json()

trade_summary = (
    file.get("reqTradeSummery")
)

symbols = []

for item in trade_summary:
    symbols.append(item["symbol"])

print(symbols)