import requests
import json
import time
import pandas as pd

# Define the API endpoint and parameters
api_endpoint = "https://www.alphavantage.co/query"
api_params = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": "AAPL",
    "interval": "1min",
    "apikey": "0F7GUPDYDEGTFHEM"
}

tickers = ["AAPL", "MSFT", "GOOG", "TSLA", "NVDA"]
# Define the buy signal criteria
def generate_signal(data):
    if data["ema_13"] > data["ema_48"] and data["prev_ema_13"] < data["prev_ema_48"]:
        print("Buy signal detected for " + api_params["symbol"])
    else:
        print("No buy signal detected for " + api_params["symbol"])

# Continuously fetch and analyze real-time data
while True:
    for tick in tickers:
        api_params["symbol"] = tick
        # Make the API call and parse the JSON response
        response = requests.get(api_endpoint, params=api_params)
        response_json = json.loads(response.text)
        # Extract the latest stock data and calculate the moving averages
        latest_data = response_json["Time Series (1min)"]
        latest_data = {k: float(v["4. close"]) for k, v in latest_data.items()}
        latest_data = sorted(latest_data.items(), reverse=True)
        latest_data = latest_data[0:50]
        latest_data = dict(latest_data)
        latest_data = {"Close": list(latest_data.values())}
        latest_data = pd.DataFrame(latest_data)
        latest_data["ema_13"] = latest_data["Close"].ewm(span=13, adjust=False).mean()
        latest_data["ema_48"] = latest_data["Close"].ewm(span=48, adjust=False).mean()
        latest_data = latest_data.iloc[-1]

        # Extract the previous day's data and calculate the moving averages
        prev_data = list(latest_data)
        prev_data[0] = latest_data.name - 60
        prev_data = tuple(prev_data)
        prev_data = pd.DataFrame(list(prev_data)).transpose()
        prev_data.columns = latest_data.index
        prev_data["ema_13"] = prev_data["Close"].ewm(span=13, adjust=False).mean()
        prev_data["ema_48"] = prev_data["Close"].ewm(span=48, adjust=False).mean()
        prev_data = prev_data.iloc[-1]

        # Generate the buy signal based on the current and previous data
        signal_data = {
            "ema_13": latest_data["ema_13"],
            "ema_48": latest_data["ema_48"],
            "prev_ema_13": prev_data["ema_13"],
            "prev_ema_48": prev_data["ema_48"]
        }
        generate_signal(signal_data)

    # Wait for the next minute to fetch new data
    time.sleep(60)