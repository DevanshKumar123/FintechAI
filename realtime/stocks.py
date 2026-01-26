import yfinance as yf

DEFAULT_STOCKS = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]

def get_stock_data():
    data = []
    for t in DEFAULT_STOCKS:
        s = yf.Ticker(t)
        info = s.info
        data.append({
            "name": info.get("longName"),
            "price": info.get("currentPrice"),
            "currency": info.get("currency"),
            "link": f"https://finance.yahoo.com/quote/{t}"
        })
    return data
