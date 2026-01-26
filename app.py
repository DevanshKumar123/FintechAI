import streamlit as st
import os, sys

sys.path.append(os.getcwd())

from vectordb.build_index import build_faiss_index
from retrieval.retriever import retrieve_docs
<<<<<<< HEAD
from LLM.hf_llm import generate_answer
=======
from realtime.stocks import get_stock_data
from llm.hf_llm import generate_answer
>>>>>>> 7c8d023 (Updated info)
from utils.guardrails import is_finance_query
from utils.config import DISCLAIMER

st.set_page_config(page_title="AI Finance Chatbot")

st.title("💰 AI Finance Assistant")

# Chat memory
if "chat" not in st.session_state:
    st.session_state.chat = []

index, docs = build_faiss_index()

query = st.chat_input("Ask finance, stock, tax, or investment questions...")

if query:
    if not is_finance_query(query):
        st.error("This chatbot supports only finance-related queries.")
    else:
        st.session_state.chat.append(("user", query))

<<<<<<< HEAD
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
=======
        # Stock related
        if "stock" in query.lower():
            stocks = get_stock_data()
            stock_text = ""
            for s in stocks:
                stock_text += f"{s['name']} | Price: {s['price']} {s['currency']} | {s['link']}\n"
            response = generate_answer(stock_text, query)
        else:
            context = "\n".join(retrieve_docs(query, index, docs))
            response = generate_answer(context, query)
>>>>>>> 7c8d023 (Updated info)

        st.session_state.chat.append(("assistant", response))

for role, msg in st.session_state.chat:
    with st.chat_message(role):
        st.markdown(msg)

st.warning(DISCLAIMER)
<<<<<<< HEAD
st.info(TERMS)

=======
>>>>>>> 7c8d023 (Updated info)
