import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from transformation.text_splitter import split_text

INDEX_PATH = "faiss.index"
DOCS_PATH = "docs.pkl"

def build_faiss_index():
    # ✅ LOAD IF ALREADY BUILT
    if os.path.exists(INDEX_PATH) and os.path.exists(DOCS_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(DOCS_PATH, "rb") as f:
            docs = pickle.load(f)
        return index, docs

    # ❌ BUILD ONLY ONCE
    texts = split_text()

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(
        texts,
        batch_size=1,            # ✅ REQUIRED
        show_progress_bar=True
    )

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)
    with open(DOCS_PATH, "wb") as f:
        pickle.dump(texts, f)

    return index, texts
