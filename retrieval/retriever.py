from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_docs(query, index, docs, k=3):
    q_vec = model.encode([query])
    _, idx = index.search(np.array(q_vec), k)
    return [docs[i] for i in idx[0]]
