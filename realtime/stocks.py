import yfinance as yf

def get_stock_data():
    tickers = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]
    stocks = []

    for t in tickers:
        stock = yf.Ticker(t)
        hist = stock.history(period="2d")

        if len(hist) >= 2:
            prev = hist["Close"][-2]
            latest = hist["Close"][-1]
            change_pct = ((latest - prev) / prev) * 100
        else:
            latest = hist["Close"][-1]
            change_pct = 0.0

        stocks.append({
            "name": stock.info.get("shortName", t),
            "price": round(latest, 2),
            "currency": "INR",
            "change_pct": round(change_pct, 2),
            "link": f"https://finance.yahoo.com/quote/{t}"
        })

    return stocks
