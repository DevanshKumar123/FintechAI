FINANCE_KEYWORDS = [
    "stock","investment","mutual fund","finance",
    "tax","itr","market","share","sip","money"
]

def is_finance_query(q):
    return any(k in q.lower() for k in FINANCE_KEYWORDS)
