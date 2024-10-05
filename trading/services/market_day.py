# trading/services/market_data.py

import yfinance as yf
import pandas as pd

def fetch_market_data(symbol, start_date, end_date):
    """
    Fetch historical market data from Yahoo Finance using yfinance.

    Args:
        symbol (str): The stock or crypto symbol (e.g., 'AAPL', 'BTC-USD')
        start_date (str or pd.Timestamp): The start date for historical data
        end_date (str or pd.Timestamp): The end date for historical data

    Returns:
        pd.DataFrame: A DataFrame with historical market data (e.g., 'Open', 'Close', 'High', 'Low', 'Volume')
    """
    try:
        market_data = yf.download(symbol, start=start_date, end=end_date)
        if market_data.empty:
            raise ValueError(f"No market data found for {symbol}.")
        return market_data[['Open', 'High', 'Low', 'Close', 'Volume']]
    except Exception as e:
        print(f"Error fetching market data: {e}")
        return pd.DataFrame()  # Return empty DataFrame in case of error
