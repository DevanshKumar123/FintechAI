"""
Stores embeddings in FAISS vector database
for fast semantic search.
"""

import faiss
import numpy as np
import os
from embeddings.embedding_generator import generate_embeddings

def build_faiss_index():
    documents, embeddings = generate_embeddings()

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    os.makedirs("vectordb/faiss_index", exist_ok=True)
    faiss.write_index(index, "vectordb/faiss_index/index.faiss")

    return documents


if __name__ == "__main__":
    build_faiss_index()
    print("FAISS index built successfully.")
