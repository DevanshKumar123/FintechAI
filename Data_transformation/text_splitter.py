"""
Splits large finance text into small chunks
to improve embedding quality and retrieval accuracy.
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from ingestion.load_data import load_all_text

def split_text():
    raw_text = load_all_text()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(raw_text)
    return chunks


if __name__ == "__main__":
    chunks = split_text()
    print(f"Total chunks created: {len(chunks)}")