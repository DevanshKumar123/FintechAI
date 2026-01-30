# def is_finance_query(query: str) -> bool:
#     q = query.lower()

#     finance_keywords = [
#         # investment intent
#         "invest", "investment", "sip", "lumpsum", "portfolio",
#         "wealth", "saving", "savings",

#         # money terms
#         "money", "rupee", "rupees", "rs", "lakh", "crore",

#         # assets
#         "stock", "stocks", "share", "shares", "equity",
#         "mutual fund", "mutual funds", "mf",
#         "fd", "fixed deposit", "rd",
#         "bond", "debt", "gold",

#         # tax & compliance
#         "tax", "itr", "80c", "80d", "capital gain",
#         "ppf", "epf", "nps",

#         # markets
#         "market", "nse", "bse", "sensex", "nifty"
#     ]

#     return any(word in q for word in finance_keywords)

def is_finance_query(query: str) -> bool:
    q = query.lower()

    finance_keywords = [
        # core finance
        "finance", "financial",

        # investment intent
        "invest", "investment", "investing",
        "sip", "lumpsum", "portfolio",
        "wealth", "saving", "savings",

        # money terms
        "money", "rupee", "rupees", "rs", "lakh", "crore",

        # assets
        "stock", "stocks", "share", "shares", "equity",
        "mutual fund", "mutual funds", "mf",
        "fd", "fixed deposit", "rd",
        "bond", "debt", "gold",

        # tax & compliance
        "tax", "taxation", "itr", "80c", "80d", "capital gain",
        "ppf", "epf", "nps",

        # markets
        "market", "nse", "bse", "sensex", "nifty"
    ]

    return any(keyword in q for keyword in finance_keywords)
