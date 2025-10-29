from django.shortcuts import render
import requests

def get_symbols():
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

    return symbols

def get_price(symbol):
    base_url = "https://www.cse.lk/api/"
    endpoint = "tradeSummary"

    response = requests.post(base_url + endpoint)
    file = response.json()

    trade_summary = (
        file.get("reqTradeSummery")
    )

    for item in trade_summary:
        if item["symbol"] == symbol:
            return item["price"]

    return None

def get_name(symbol):
    base_url = "https://www.cse.lk/api/"
    endpoint = "tradeSummary"

    response = requests.post(base_url + endpoint)
    file = response.json()

    trade_summary = (
        file.get("reqTradeSummery")
    )

    for item in trade_summary:
        if item["symbol"] == symbol:
            return item["name"]

    return None

def get_change(symbol):
    base_url = "https://www.cse.lk/api/"
    endpoint = "tradeSummary"

    response = requests.post(base_url + endpoint)
    file = response.json()

    trade_summary = (
        file.get("reqTradeSummery")
    )

    for item in trade_summary:
        if item["symbol"] == symbol:
            return item["change"]

    return None

def get_percentage_change(symbol):
    base_url = "https://www.cse.lk/api/"
    endpoint = "tradeSummary"

    response = requests.post(base_url + endpoint)
    file = response.json()

    trade_summary = (
        file.get("reqTradeSummery")
    )

    for item in trade_summary:
        if item["symbol"] == symbol:
            return item["percentageChange"]

    return None