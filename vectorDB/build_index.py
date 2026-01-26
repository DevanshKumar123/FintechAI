import faiss
import numpy as np

from embeddings.embedding_generator import generate_embeddings
from transformation.text_splitter import split_text

def build_faiss_index():
    """
    Builds a FAISS vector index from finance documents.
    """

    # Step 1: Split raw data into chunks
    documents = split_text()

    # Step 2: Generate embeddings
    embeddings = generate_embeddings(documents)

    # Step 3: Convert embeddings to numpy array
    embeddings_np = np.array(embeddings).astype("float32")

    # Step 4: Build FAISS index
    dimension = embeddings_np.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_np)

    return index, documents
