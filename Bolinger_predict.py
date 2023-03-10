import requests
import json
import numpy as np
from datetime import datetime
from datetime import timedelta

# Replace with your API key
API_KEY = "0F7GUPDYDEGTFHEM"

# Replace with the stock symbol you want to analyze
STOCK_SYMBOL = "COSM"

def predict(ticker, start_date, end_date):

    # Set the number of days to analyze
    ANALYSIS_PERIOD = 30
    start_date = start_date
    end_date = start_date


    ticker = ticker.upper()
    # Convert the start and end dates to datetime objects
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Set the number of standard deviations for the Bollinger bands
    BOLLINGER_SD = 1

    # Set the risk tolerance
    RISK_TOLERANCE = 0.01

    # Get the stock data from the API
    response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&apikey={API_KEY}")

    # Parse the JSON data
    stock_data = json.loads(response.text)

    # Get the list of daily prices
    daily_prices = stock_data["Time Series (Daily)"]

    # Get the closing prices over the analysis period
    closing_prices = []
    for i in range(ANALYSIS_PERIOD):
        for date in daily_prices.keys():
            closing_prices.append(float(daily_prices[date]["4. close"]))  

    # Calculate the moving average
    moving_average = np.mean(closing_prices)

    # Calculate the standard deviation
    standard_deviation = np.std(closing_prices)

    # Calculate the upper and lower Bollinger bands
    upper_band = moving_average + BOLLINGER_SD * standard_deviation
    lower_band = moving_average - BOLLINGER_SD * standard_deviation

    # Get the current price
    current_price = float(daily_prices[start_date.strftime('%Y-%m-%d')]["4. close"])
    print(current_price)
    print(upper_band)
    print(lower_band)
    # Generate the buy/sell signal
    if current_price >= upper_band - RISK_TOLERANCE:
        return "Sell"
    elif current_price <= lower_band + RISK_TOLERANCE:
        return "Buy"
    else:
        return "Hold"