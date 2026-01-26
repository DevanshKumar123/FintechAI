from sentence_transformers import SentenceTransformer

# Load embedding model once
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def generate_embeddings(documents):
    """
    Generates vector embeddings for a list of text documents.
    """

    if not documents:
        return []

    embeddings = model.encode(
        documents,
        show_progress_bar=True
    )

    return embeddings
