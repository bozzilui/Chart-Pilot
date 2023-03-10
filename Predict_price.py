import numpy as np
import yfinance as yf
from sklearn.tree import DecisionTreeRegressor
import datetime

def predict_stock_prices(ticker: str, start_date, end_date):
  print(type(ticker))



  # Collect the stock data
  stock = yf.Ticker(ticker.upper())
  df = stock.history(start=start_date, end=end_date)

  df = df.sample(frac=1)
  # Extract the relevant columns from the dataframe
  X = df[['High', 'Low', 'Close', 'Volume']]
  y = df['Close'].shift(-1)

  # Split the data into training and test sets
  X_train = X[:int(0.8 * len(X))]
  y_train = y[:int(0.8 * len(y))]
  X_test = X[int(0.8 * len(X)):]
  y_test = y[int(0.8 * len(y)):]

  # Train the decision tree regressor
  reg = DecisionTreeRegressor()
  reg.fit(X_train, y_train)

  # Use the trained model to make predictions on new data
  prediction = np.mean(reg.predict(X_test))
  prediction = round(prediction,2)
  return prediction

if __name__ == "__main__":
  stock = input("Please enter a stock ticker symbol: ")
  predict_stock_prices(stock)



