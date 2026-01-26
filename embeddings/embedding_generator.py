from sentence_transformers import SentenceTransformer
from transformation.text_splitter import split_text

def generate_embeddings():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    docs = split_text()
    vectors = model.encode(docs)
    return docs, vectors
