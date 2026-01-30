import os
import requests
import wikipediaapi
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

# ---------------- CONFIG ----------------

DATA_PATH = "data/raw"

WIKI_PAGES = [
    "Finance",
    "Investment",
    "Stock_market",
    "Mutual_fund",
    "Systematic_investment_plan",
    "Gold_as_an_investment",
    "Taxation_in_India"
]

GROWW_PAGES = [
    "https://groww.in/p/investment",
    "https://groww.in/p/mutual-funds",
    "https://groww.in/p/stocks"
]

# -------- API KEY (ONLY ALPHA VANTAGE) --------

ALPHA_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

HEADERS = {
    "User-Agent": "AI-Finance-Assistant/1.0 (Educational Use)"
}

# ---------------- HELPERS ----------------

def normalize_text(text: str) -> str:
    """Remove duplicates and extra whitespace."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return "\n".join(sorted(set(lines)))

# ---------------- WIKIPEDIA ----------------

def fetch_wikipedia():
    wiki = wikipediaapi.Wikipedia(
        language="en",
        user_agent="AI-Finance-Assistant/1.0 (educational)"
    )

    text = ""
    for title in WIKI_PAGES:
        page = wiki.page(title)
        if page.exists():
            text += f"\n\n[SOURCE: Wikipedia | {title}]\n"
            text += page.text + "\n"

    return text

# ---------------- GROWW (CONTROLLED SCRAPING) ----------------

def fetch_groww(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        content = f"\n\n[SOURCE: Groww | {url}]\n"
        for tag in soup.find_all(["h2", "h3", "p"]):
            t = tag.get_text(strip=True)
            if 80 < len(t) < 350:
                content += t + "\n"

        return content
    except Exception:
        return ""

# ---------------- STOCK PRICE (ALPHA VANTAGE) ----------------

def fetch_stock_snapshot(symbol="IBM"):
    """
    Delayed stock price snapshot using Alpha Vantage.
    Suitable for educational use.
    """
    if not ALPHA_KEY:
        return ""

    url = (
        "https://www.alphavantage.co/query"
        f"?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_KEY}"
    )

    try:
        r = requests.get(url, timeout=10)
        data = r.json().get("Global Quote", {})

        if not data:
            return ""

        return f"""
[SOURCE: Alpha Vantage | Stock Snapshot]

Symbol: {data.get('01. symbol')}
Price: {data.get('05. price')}
Change: {data.get('09. change')}
Change Percent: {data.get('10. change percent')}
Last Trading Day: {data.get('07. latest trading day')}

Note: Price is delayed and for educational purposes only.
"""
    except Exception:
        return ""

# ---------------- GOLD PRICE (ALPHA VANTAGE) ----------------

def fetch_gold_price():
    """
    Gold price using Alpha Vantage (daily reference).
    """
    if not ALPHA_KEY:
        return ""

    url = (
        "https://www.alphavantage.co/query"
        f"?function=GOLD&apikey={ALPHA_KEY}"
    )

    try:
        r = requests.get(url, timeout=10)
        data = r.json().get("data", [])

        if not data:
            return ""

        latest = data[0]

        return f"""
[SOURCE: Alpha Vantage | Gold]

Date: {latest.get('date')}
Gold Price (USD per oz): {latest.get('value')}

Note: Daily reference price.
"""
    except Exception:
        return ""

# ---------------- MAIN INGESTION ----------------

def load_all_data():
    """
    Loads finance-related educational data for vector embedding.
    """

    text = ""

    # -------- LOCAL FILES --------
    if os.path.exists(DATA_PATH):
        for f in os.listdir(DATA_PATH):
            if f.endswith(".txt"):
                with open(
                    os.path.join(DATA_PATH, f),
                    "r",
                    encoding="utf-8"
                ) as file:
                    text += file.read() + "\n"

    # -------- STATIC KNOWLEDGE --------
    text += fetch_wikipedia()

    for url in GROWW_PAGES:
        text += fetch_groww(url)

    # -------- SUMMARIZED MARKET SNAPSHOTS --------
    text += fetch_stock_snapshot()
    text += fetch_gold_price()

    return normalize_text(text)
