import faiss, os, numpy as np
from embeddings.embedding_generator import generate_embeddings

INDEX_PATH = "vectorDB/faiss_index/index.faiss"
DOC_PATH = "vectorDB/faiss_index/docs.npy"

def build_faiss_index():
    if os.path.exists(INDEX_PATH):
        index = faiss.read_index(INDEX_PATH)
        docs = np.load(DOC_PATH, allow_pickle=True).tolist()
        return index, docs

    docs, embeddings = generate_embeddings()
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

    os.makedirs("vectordb/faiss_index", exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
    np.save(DOC_PATH, np.array(docs, dtype=object))

    return index, docs
