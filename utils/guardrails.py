FINANCE_KEYWORDS = [
    "stock", "investment", "tax", "itr", "mutual fund",
    "sip", "finance", "money", "income", "share", "market",
    "budget", "saving", "loan", "interest"
]

def is_finance_query(query: str) -> bool:
    query = query.lower()
    return any(word in query for word in FINANCE_KEYWORDS)
