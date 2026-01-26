import os

DATA_PATH = "data/raw"

def load_all_data():
    text = ""
    for file in os.listdir(DATA_PATH):
        if file.endswith(".txt"):
            with open(os.path.join(DATA_PATH, file), "r", encoding="utf-8") as f:
                text += f.read() + "\n"
    return text
