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

# ---------------- SHORT-TERM KEYWORDS ----------------
SHORT_TERM_KEYWORDS = [
    "today", "trending", "short term", "5 days",
    "this week", "momentum", "swing"
]

# ---------------- SIDEBAR ----------------
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

assumptions = {}
if amount != "Not specified":
    assumptions["amount"] = amount
if risk != "Not specified":
    assumptions["risk"] = risk
if horizon != "Not specified":
    assumptions["horizon"] = horizon

if assumptions:
    st.sidebar.success("Assumptions applied")
else:
    st.sidebar.info("Using generic analysis")

# ---------------- VECTOR DB ----------------
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
        is_short_term = any(k in query.lower() for k in SHORT_TERM_KEYWORDS)

        # ---------------- STOCK QUERIES ----------------
        if "stock" in query.lower():
            stocks = get_stock_data()

            stock_context = "Commonly tracked stocks with recent market movement:\n\n"
            for s in stocks:
                stock_context += (
                    f"- {s['name']}\n"
                    f"  Current Price: {s['price']} {s['currency']}\n"
                    f"  1-Day Change: {s['change_pct']}%\n"
                    f"  Reference Link: {s['link']}\n\n"
                )

            if is_short_term:
                stock_context = (
                    "The user is asking for educational short-term or trending stock analysis. "
                    "Do NOT give buy/sell advice. Explain momentum, volatility, and risks.\n\n"
                    + stock_context
                )

            # ---- LLM CALL WITH FALLBACK ----
            with st.spinner("Analyzing market data..."):
                try:
                    response = generate_answer(
                        context=stock_context,
                        question=query,
                        assumptions=assumptions,
                        chat_history=st.session_state.chat
                    )
                except Exception:
                    response = (
                        stock_context
                        + "\n⚠️ Market analysis is loading. Please ask again shortly.\n\n"
                        + DISCLAIMER
                    )

        # ---------------- NON-STOCK QUERIES ----------------
        else:
            retrieved = retrieve_docs(query, index, docs)
            context = "\n".join(retrieved)

            with st.spinner("Analyzing financial information..."):
                try:
                    response = generate_answer(
                        context=context,
                        question=query,
                        assumptions=assumptions,
                        chat_history=st.session_state.chat
                    )
                except Exception:
                    response = (
                        "⚠️ The AI model is currently warming up. "
                        "Please try again in a moment.\n\n"
                        + DISCLAIMER
                    )

        st.session_state.chat.append(("assistant", response))

# ---------------- CHAT RENDER ----------------
for role, msg in st.session_state.chat:
    with st.chat_message(role):
        st.markdown(msg)

st.warning(DISCLAIMER)
