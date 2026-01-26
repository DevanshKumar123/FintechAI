from ingestion.load_data import load_all_data

def split_text(chunk_size=500, overlap=50):
    """
    Simple text splitter without LangChain.
    Stable and dependency-free.
    """
    text = load_all_data()
    chunks = []

    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks
