"""
Generates final AI response using Hugging Face model.
"""

from transformers import pipeline

def generate_answer(context, question):
    generator = pipeline(
        "text-generation",
        model="google/flan-t5-large"
    )

    prompt = f"""
    Context:
    {context}

    Question:
    {question}

    Answer with disclaimer:
    """

    response = generator(prompt, max_length=300)
    return response[0]["generated_text"]
