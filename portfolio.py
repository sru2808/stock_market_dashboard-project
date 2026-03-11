import pandas as pd

portfolio = []

def add_stock(symbol, shares, price):

    portfolio.append({
        "Symbol":symbol,
        "Shares":shares,
        "Buy Price":price,
        "Investment":shares*price
    })

def get_portfolio():

    return pd.DataFrame(portfolio)
