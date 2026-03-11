import yfinance as yf
import pandas as pd

def get_stock_data(symbol, period="6mo"):
    
    stock = yf.Ticker(symbol)
    df = stock.history(period=period)

    df.reset_index(inplace=True)

    return df