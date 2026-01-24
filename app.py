import streamlit as st
from vectordb.build_index import build_faiss_index
from retrieval.retriever import retrieve_docs
from llm.hf_llm import generate_answer
from utils.config import DISCLAIMER

st.set_page_config(page_title="AI Finance Assistant")

st.title("💰 AI Finance Assistant")

# Build vector DB once
documents = build_faiss_index()

query = st.text_input("Ask a finance-related question:")

if query:
    relevant_docs = retrieve_docs(query, documents)
    context = "\n".join(relevant_docs)

    answer = generate_answer(context, query)

    st.subheader("📊 AI Response")
    st.write(answer)

    st.warning(DISCLAIMER)
