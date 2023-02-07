# Provides ways to work with large multidimensional arrays
import numpy as np 
# Allows for further data manipulation and analysis
import pandas as pd 
import matplotlib.pyplot as plt # Plotting
import matplotlib.dates as mdates # Styling dates

# pip install numpy
# conda install -c anaconda pandas
# conda install -c conda-forge matplotlib

import datetime as dt # For defining dates

import time

# In Powershell Prompt : conda install -c conda-forge multitasking
# pip install -i https://pypi.anaconda.org/ranaroussi/simple yfinance

import yfinance as yf

# To show all your output File -> Preferences -> Settings Search for Notebook
# Notebook Output Text Line Limit and set to 100

# Used for file handling like deleting files
import os

# conda install -c conda-forge cufflinks-py
# conda install -c plotly plotly
import cufflinks as cf
import plotly.express as px
import plotly.graph_objects as go

import random
import itertools

# Make Plotly work in your Jupyter Notebook
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
# Use Plotly locally
cf.go_offline()

from plotly.subplots import make_subplots

# New Imports
# Used to get data from a directory
import os
from os import listdir
from os.path import isfile, join

import warnings
warnings.simplefilter("ignore")


PATH = "Tickers/"

S_DATE = "2019-01-01"
E_DATE = "2022-12-09"

S_DATE_DT = pd.to_datetime(S_DATE)
E_DATE_DT = pd.to_datetime(E_DATE)

risk_free_rate = 0.0125 # Approximate 10 year bond rate

files = [x for x in listdir(PATH) if isfile(join(PATH, x))]
tickers = [os.path.splitext(x)[0] for x in files]

# 3263 total stocks
tickers.sort()



def get_stock_df_from_csv(ticker):
    
    # Try to get the file and if it doesn't exist issue a warning
    try:
        df = pd.read_csv(PATH + ticker + '.csv', index_col=0)
    except FileNotFoundError as ex:
        print(ex)
    else:
        return df

def merge_df_by_column_name(col_name, sdate, edate, *tickers):
    # Will hold data for all dataframes with the same column name
    mult_df = pd.DataFrame()
    
    for x in tickers:
        df = get_stock_df_from_csv(x)
        
        # NEW Check if your dataframe has duplicate indexes
        if not df.index.is_unique:
        #     #Delete duplicates 
            df = df.loc[~df.index.duplicated(), :]
        
        mask = (df.index >= sdate) & (df.index <= edate)
        mult_df[x] = df.loc[mask][col_name]
        
    return mult_df


def build_portfolio(S_DATE, E_DATE, tickers) -> list:
    mult_df = merge_df_by_column_name('Close', S_DATE, E_DATE, *tickers)

    mult_cum_df = merge_df_by_column_name('cum_return',  S_DATE,
                                    E_DATE, *tickers)

    mult_df = mult_df.astype(float)

    returns = np.log(mult_df / mult_df.shift(1))

    mean_ret = returns.mean() * 252 # 252 average trading days per year

    # only want stocks with a mean return of 30%
    mean_ret = mean_ret[mean_ret > 0.30]

    mean_ret = mean_ret.sort_values(ascending=False)



    random_sets = [mean_ret.sample(7) for _ in range(1500)]
    portfolios = []

    for port in random_sets:
        num_stocks = port.shape[0]
        r = returns[port.axes[0].tolist()]
        
        p_ret = [] # Returns list
        p_vol = [] # Volatility list
        p_SR = [] # Sharpe Ratio list
        p_wt = [] # Stock weights list


        for x in range(5000):
            # Generate random weights
            p_weights = np.random.random(num_stocks)
            p_weights /= np.sum(p_weights)
            
            # Add return using those weights to list
            ret_1 = np.sum(p_weights * r.mean()) * 252
            p_ret.append(ret_1)
            
            # Add volatility or standard deviation to list
            vol_1 = np.sqrt(np.dot(p_weights.T, np.dot(r.cov() * 252, p_weights)))
            p_vol.append(vol_1)
            
            # Get Sharpe ratio
            SR_1 = (ret_1 - risk_free_rate) / vol_1
            p_SR.append(SR_1)
            
            # Store the weights for each portfolio
            p_wt.append(p_weights)
            
        # Convert to Numpy arrays
        p_ret = np.array(p_ret)
        p_vol = np.array(p_vol)
        p_SR = np.array(p_SR)
        p_wt = np.array(p_wt)


        # Return the index of the largest Sharpe Ratio
        SR_idx = np.argmax(p_SR)

        """# Find the ideal portfolio weighting at that index
        i = 0
        while i < num_stocks:
            print("Stock : %s : %2.2f" % (mean_ret.axes[0][i], (p_wt[SR_idx][i] * 100)))
            i += 1
            """
        """# Find volatility of that portfolio
        print("\nVolatility :", p_vol[SR_idx])
            
        # Find return of that portfolio
        print("Return :", p_ret[SR_idx])"""

        if p_vol[SR_idx] < 0.35:
            print(port)
            portfolios.append((port, p_vol[SR_idx], p_ret[SR_idx]))


    return portfolios