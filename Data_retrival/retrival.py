"""
Retrieves relevant finance documents
based on user query.
"""

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_PATH = "vectordb/faiss_index/index.faiss"

def retrieve_docs(query, documents, top_k=3):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_vector = model.encode([query])

    index = faiss.read_index(INDEX_PATH)
    distances, indices = index.search(np.array(query_vector), top_k)

    return [documents[i] for i in indices[0]]
