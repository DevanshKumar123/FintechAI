FINANCE_KEYWORDS = [
    "stock", "investment", "mutual fund", "finance",
    "tax", "itr", "market", "share", "sip", "money", "returns"
]

def is_finance_query(query: str) -> bool:
    return any(word in query.lower() for word in FINANCE_KEYWORDS)
