import faiss, numpy as np, os
from embeddings.embedding_generator import generate_embeddings

<<<<<<< HEAD
INDEX_PATH = "vectorDB/faiss_index/index.faiss"
DOC_PATH = "vectorDB/faiss_index/docs.npy"

=======
>>>>>>> 7c8d023 (Updated info)
def build_faiss_index():
    docs, vectors = generate_embeddings()
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(np.array(vectors))
    return index, docs
