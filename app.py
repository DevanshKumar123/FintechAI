import streamlit as st
import sys
import os

# Ensure project root is on path
sys.path.append(os.getcwd())

from vectorDB.build_index import build_faiss_index
from retrieval.retriever import retrieve_docs
from LLM.hf_llm import generate_answer
from utils.guardrails import is_finance_query
from utils.config import DISCLAIMER, TERMS
from realtime.stocks import get_stock_info

# ---------------- STREAMLIT CONFIG ----------------
st.set_page_config(page_title="AI Finance Assistant", layout="centered")
st.title("💰 AI Finance Assistant")

# ---------------- SESSION MEMORY ----------------
if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------- LOAD VECTOR DB (ONCE) ----------------
@st.cache_resource
def load_vector_db():
    return build_faiss_index()

index, docs = load_vector_db()

# ---------------- SHORT-TERM DETECTION ----------------
SHORT_TERM_KEYWORDS = [
    "today", "5 days", "short term", "this week",
    "next few days", "swing", "for few days"
]

# ---------------- USER INPUT ----------------
query = st.chat_input("Ask a finance-related question...")

if query:
    # Finance-only guard
    if not is_finance_query(query):
        st.error("❌ This assistant only supports finance-related queries.")
    else:
        st.session_state.chat.append(("user", query))

        is_short_term = any(k in query.lower() for k in SHORT_TERM_KEYWORDS)

        # ---------------- REAL-TIME STOCK QUERY ----------------
        if ".ns" in query.lower() or ".bo" in query.lower():
            ticker = query.strip().split()[-1].upper()
            stock = get_stock_info(ticker)

            response = f"""
### 📊 {stock['name']}

- **Current Price:** {stock['price']} {stock['currency']}
- **Recent Price History:** {stock['history']}
- **More details:** {stock['link']}

⚠️ *This is educational market information only, not a buy/sell recommendation.*
"""

        # ---------------- RAG + LLM FLOW ----------------
        else:
            retrieved_docs = retrieve_docs(query, index, docs)
            context = "\n".join(retrieved_docs)

            if is_short_term:
                context = (
                    "The user is asking for educational short-term market analysis. "
                    "Do NOT give buy/sell calls or guaranteed returns. "
                    "Explain risks, trends, and general observations.\n\n"
                    + context
                )

            history_text = "\n".join(
                [f"{role}: {msg}" for role, msg in st.session_state.chat[-5:]]
            )

            response = generate_answer(context, history_text, query)

        st.session_state.chat.append(("assistant", response))

# ---------------- RENDER CHAT ----------------
for role, msg in st.session_state.chat:
    with st.chat_message(role):
        st.markdown(msg)

# ---------------- FOOTER ----------------
st.markdown("---")
st.warning(DISCLAIMER)
st.info(TERMS)

