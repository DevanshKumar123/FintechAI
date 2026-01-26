import streamlit as st
import os, sys

sys.path.append(os.getcwd())

from vectordb.build_index import build_faiss_index
from retrieval.retriever import retrieve_docs
from realtime.stocks import get_stock_data
from llm.hf_llm import generate_answer
from utils.guardrails import is_finance_query
from utils.config import DISCLAIMER

st.set_page_config(page_title="AI Finance Chatbot", layout="centered")
st.title("💰 AI Finance Assistant")

# ---------------- SESSION MEMORY ----------------
if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------- OPTIONAL ASSUMPTIONS ----------------
st.sidebar.header("Investment Assumptions (Optional)")

amount = st.sidebar.selectbox(
    "Investment Amount",
    ["Not specified", "₹50,000", "₹1 lakh", "₹5 lakh"]
)

risk = st.sidebar.selectbox(
    "Risk Profile",
    ["Not specified", "Low", "Moderate", "High"]
)

horizon = st.sidebar.selectbox(
    "Time Horizon",
    ["Not specified", "Short-term (1–2 yrs)", "Medium-term (3–5 yrs)", "Long-term (5+ yrs)"]
)

assumptions = {
    "amount": amount,
    "risk": risk,
    "horizon": horizon
}

# ---------------- LOAD VECTOR DB ----------------
@st.cache_resource
def load_index():
    return build_faiss_index()

index, docs = load_index()

# ---------------- USER INPUT ----------------
query = st.chat_input("Ask finance, stock, tax, or investment questions...")

if query:
    if not is_finance_query(query):
        st.error("❌ This assistant supports only finance-related queries.")
    else:
        st.session_state.chat.append(("user", query))

        # ---------------- STOCK-RELATED QUERY ----------------
        if "stock" in query.lower():
            stocks = get_stock_data()

            stock_context = ""
            for s in stocks:
                stock_context += (
                    f"{s['name']} | "
                    f"Price: {s['price']} {s['currency']} | "
                    f"{s['link']}\n"
                )

            response = generate_answer(
                context=stock_context,
                question=query,
                assumptions=assumptions,
                chat_history=st.session_state.chat
            )

        # ---------------- RAG + LLM ----------------
        else:
            retrieved = retrieve_docs(query, index, docs)
            context = "\n".join(retrieved)

            response = generate_answer(
                context=context,
                question=query,
                assumptions=assumptions,
                chat_history=st.session_state.chat
            )

        st.session_state.chat.append(("assistant", response))

# ---------------- RENDER CHAT ----------------
for role, msg in st.session_state.chat:
    with st.chat_message(role):
        st.markdown(msg)

st.warning(DISCLAIMER)
