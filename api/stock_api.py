import yfinance as yf

STOCK_SYMBOLS = {
    "bajaj finance": "BAJFINANCE.NS",
    "reliance": "RELIANCE.NS",
    "tcs": "TCS.NS",
    "infosys": "INFY.NS",
    "hdfc bank": "HDFCBANK.NS",
    "icici bank": "ICICIBANK.NS"
}

# ---------------- SINGLE STOCK PRICE ----------------
def get_live_stock_price(query: str):
    q = query.lower()
    for name, symbol in STOCK_SYMBOLS.items():
        if name in q:
            data = yf.Ticker(symbol).history(period="1d")
            if data.empty:
                return None

            price = round(data["Close"].iloc[-1], 2)
            return (
                f"📊 **{name.title()}**\n\n"
                f"💰 **Price:** ₹{price}\n\n"
                f"🔗 https://finance.yahoo.com/quote/{symbol}\n\n"
                f"⚠️ *Price may be delayed. Educational use only.*"
            )
    return None


# ---------------- TOP GAINERS ----------------
def get_top_gainers():
    tickers = list(STOCK_SYMBOLS.values())
    rows = []

    for t in tickers:
        d = yf.Ticker(t).history(period="2d")
        if len(d) >= 2:
            pct = ((d["Close"].iloc[-1] - d["Close"].iloc[-2]) / d["Close"].iloc[-2]) * 100
            if pct > 0:
                rows.append((t.replace(".NS", ""), round(pct, 2)))

    rows.sort(key=lambda x: x[1], reverse=True)

    return "📈 **TOP GAINERS**\n\n" + "\n".join(
        [f"📈 **{r[0]}**: +{r[1]}%" for r in rows[:5]]
    )


# ---------------- TOP LOSERS ----------------
def get_top_losers():
    tickers = list(STOCK_SYMBOLS.values())
    rows = []

    for t in tickers:
        d = yf.Ticker(t).history(period="2d")
        if len(d) >= 2:
            pct = ((d["Close"].iloc[-1] - d["Close"].iloc[-2]) / d["Close"].iloc[-2]) * 100
            if pct < 0:
                rows.append((t.replace(".NS", ""), round(pct, 2)))

    rows.sort(key=lambda x: x[1])

    return "📉 **TOP LOSERS**\n\n" + "\n".join(
        [f"📉 **{r[0]}**: {r[1]}%" for r in rows[:5]]
    )


# ---------------- GOLD PRICE ----------------
def get_gold_price_india():
    data = yf.Ticker("GC=F").history(period="1d")
    if data.empty:
        return None

    usd = data["Close"].iloc[-1]
    inr = round(usd * 83, 2)

    return (
        "🪙 **Gold Price Today (India)**\n\n"
        f"💰 ₹{inr} per ounce\n\n"
        "⚠️ Approx INR conversion. Educational use only."
    )
