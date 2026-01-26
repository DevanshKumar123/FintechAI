import yfinance as yf

def get_stock_info(ticker: str):
    stock = yf.Ticker(ticker)

    info = stock.info
    hist = stock.history(period="6mo")

    return {
        "name": info.get("longName", ticker),
        "price": info.get("currentPrice"),
        "currency": info.get("currency"),
        "history": hist.tail(5)[["Close"]].to_dict(),
        "link": f"https://finance.yahoo.com/quote/{ticker}"
    }
