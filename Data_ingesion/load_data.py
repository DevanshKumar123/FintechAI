"""
This file loads all raw finance-related text data.
This is the first step in the RAG pipeline.
"""

import os

DATA_DIR = "data/raw"

def load_all_text():
    """
    Reads all .txt files from data/raw directory
    and combines them into a single string.
    """
    all_text = ""

    for file in os.listdir(DATA_DIR):
        if file.endswith(".txt"):
            with open(os.path.join(DATA_DIR, file), "r", encoding="utf-8") as f:
                all_text += f.read() + "\n"

    return all_text


if __name__ == "__main__":
    data = load_all_text()
    print("Data successfully ingested.")