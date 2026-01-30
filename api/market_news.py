import yfinance as yf

def get_market_news():
    try:
        news = yf.get_news("market")
        headlines = [n["title"] for n in news[:5]]
        return "Latest Market News:\n" + "\n".join(headlines)
    except:
        return "Market news not available."