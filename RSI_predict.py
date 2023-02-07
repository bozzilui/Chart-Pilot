import requests
import json

# Replace with your API key
API_KEY = "0F7GUPDYDEGTFHEM"

# Replace with the stock symbol you want to analyze
STOCK_SYMBOL = "SPY"

# Set the number of days to analyze
ANALYSIS_PERIOD = 30

# Set the moving average period
MA_PERIOD = 14

# Set the relative strength index period
RSI_PERIOD = 14

# Set the threshold for the relative strength index
RSI_THRESHOLD = 70

# Set the moving average weight
MA_WEIGHT = 0.25

# Set the relative strength index weight
RSI_WEIGHT = 0.5

# Set the risk tolerance
RISK_TOLERANCE = 0.5

# Get the stock data from the API
response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={STOCK_SYMBOL}&apikey={API_KEY}")

# Parse the JSON data
stock_data = json.loads(response.text)

# Get the list of daily prices
daily_prices = stock_data["Time Series (Daily)"]

# Calculate the moving average
moving_average = 0
for i in range(ANALYSIS_PERIOD):
  for date in daily_prices.keys():
    moving_average += float(daily_prices[date]["4. close"])
moving_average /= ANALYSIS_PERIOD

# Calculate the relative strength index
rsi = 0
for i in range(RSI_PERIOD):
  for date in daily_prices.keys():
    rsi += float(daily_prices[date]["4. close"])
rsi /= RSI_PERIOD

# Calculate the overall score
score = moving_average * MA_WEIGHT + rsi * RSI_WEIGHT

# Generate the buy/sell signal
if score >= RISK_TOLERANCE:
    print("Buy")
else:
    print("Sell")