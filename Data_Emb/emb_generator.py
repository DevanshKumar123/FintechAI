"""
Converts finance text chunks into numerical vectors
using Hugging Face sentence-transformers.
"""

from sentence_transformers import SentenceTransformer
from transformation.text_splitter import split_text

def generate_embeddings():
    model = SentenceTransformer("all-MiniLM-L6-v2")

    chunks = split_text()
    embeddings = model.encode(chunks)

    return chunks, embeddings


if __name__ == "__main__":
    docs, vectors = generate_embeddings()
    print("Embeddings generated successfully.")