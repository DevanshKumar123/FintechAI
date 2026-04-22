import streamlit as st
import os, sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vectordb.build_index import build_faiss_index
from retrieval.retriever import retrieve_docs
from api.stock_api import (
    get_live_stock_price,
    get_top_gainers,
    get_top_losers,
    get_gold_price_india
)
from api.market_news import get_market_news
from llm.hf_llm import generate_answer
from utils.guardrails import is_finance_query
from utils.config import DISCLAIMER
from utils.keywords import STOCK_KEYWORDS, NEWS_KEYWORDS

# -------------------------------------------------
st.set_page_config(page_title="FintechAI", layout="centered")
st.title("💰 AI Finance Assistant")

# -------------------------------------------------
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "active_chat" not in st.session_state:
    cid = f"Chat {datetime.now().strftime('%H:%M:%S')}"
    st.session_state.chats[cid] = []
    st.session_state.active_chat = cid

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

if "quick_query" not in st.session_state:
    st.session_state.quick_query = None

# -------------------------------------------------
def apply_theme(theme):
    bg_bot = "#1e1e1e" if theme == "Dark" else "#f1f3f8"
    text_bot = "white" if theme == "Dark" else "#1a1a1a"

    st.markdown(
        f"""
        <style>
        .chat-row {{ display:flex; margin:4px 0; }}
        .chat-row.user {{ justify-content:flex-end; }}
        .chat-row.bot {{ justify-content:flex-start; }}

        .user-bubble {{
            background:#2b3fa3; color:white;
            padding:10px 14px; border-radius:14px; max-width:70%;
        }}
        .bot-bubble {{
            background:{bg_bot}; color:{text_bot};
            padding:10px 14px; border-radius:14px; max-width:70%;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

apply_theme(st.session_state.theme)

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.title("💬 Chats")

st.session_state.theme = st.sidebar.radio(
    "Theme", ["Light", "Dark"],
    index=0 if st.session_state.theme == "Light" else 1
)
st.sidebar.divider()

st.sidebar.subheader("⚡ Quick Ask")
if st.sidebar.button("💰 Today’s Top Gainers"):
    st.session_state.quick_query = "TOP_GAINERS"
if st.sidebar.button("📉 Today’s Top Losers"):
    st.session_state.quick_query = "TOP_LOSERS"
if st.sidebar.button("🏦 Best SIP options"):
    st.session_state.quick_query = "Best SIP options for long term investment"
if st.sidebar.button("📊 NIFTY outlook"):
    st.session_state.quick_query = "NIFTY outlook for this week"
if st.sidebar.button("🪙 Gold price today"):
    st.session_state.quick_query = "GOLD_PRICE"

st.sidebar.divider()

search_query = st.sidebar.text_input("🔍 Search chats")

if st.sidebar.button("➕ New Chat"):
    cid = f"Chat {datetime.now().strftime('%H:%M:%S')}"
    st.session_state.chats[cid] = []
    st.session_state.active_chat = cid

st.sidebar.divider()

for cid in list(st.session_state.chats.keys()):
    if search_query.lower() not in cid.lower():
        continue
    col1, col2 = st.sidebar.columns([4, 1])
    if col1.button(cid, key=f"open_{cid}"):
        st.session_state.active_chat = cid
    if col2.button("🗑️   ", key=f"del_{cid}"):
        del st.session_state.chats[cid]
        st.rerun()

# -------------------------------------------------
@st.cache_resource
def load_index():
    return build_faiss_index()

index, docs = load_index()
chat = st.session_state.chats[st.session_state.active_chat]

# -------------------------------------------------
user_input = st.chat_input("Ask finance, stock, tax, or investment questions...")

query = None
if st.session_state.quick_query:
    query = st.session_state.quick_query
    st.session_state.quick_query = None
elif user_input:
    query = user_input

# -------------------------------------------------
if query:
    chat.append(("user", query))

    # QUICK ACTIONS
    if query == "TOP_GAINERS":
        chat.append(("assistant", get_top_gainers()))
    elif query == "TOP_LOSERS":
        chat.append(("assistant", get_top_losers()))
    elif query == "GOLD_PRICE":
        chat.append(("assistant", get_gold_price_india()))

    else:
        if not is_finance_query(query):
            chat.append(("assistant", "⚠️ I can answer only finance-related questions."))
        else:
            q = query.lower()
            is_stock = any(k in q for k in STOCK_KEYWORDS)
            is_news = any(k in q for k in NEWS_KEYWORDS)
            is_price_query = any(w in q for w in ["price", "today", "current", "share"])

            # STOCK PRICE
            if is_stock and is_price_query:
                chat.append(("assistant", get_live_stock_price(query)
                             or "⚠️ Stock price not available right now."))

            # SIMPLE DEFINITIONS
            elif q.startswith("what is") or q.startswith("define"):
                chat.append(("assistant", generate_answer("", query)))

            # NEWS
            elif is_news:
                chat.append(("assistant", generate_answer(get_market_news(), query)))

            # GENERAL FINANCE
            else:
                context = "\n".join(retrieve_docs(query, index, docs))
                chat.append(("assistant", generate_answer(context, query)))

# -------------------------------------------------
for role, msg in chat:
    bubble = "user-bubble" if role == "user" else "bot-bubble"
    align = "user" if role == "user" else "bot"
    st.markdown(
        f"""
        <div class="chat-row {align}">
            <div class="{bubble}">{msg}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.warning(DISCLAIMER)
