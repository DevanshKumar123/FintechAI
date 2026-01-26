from transformers import pipeline

# ✅ Correct pipeline for FLAN-T5
llm = pipeline(
    "text2text-generation",
    model="google/flan-t5-large",
    temperature=0.7,
    top_p=0.9
)

def generate_answer(context, history, question):

    # 🔹 Expand keyword-only queries
    if len(question.split()) <= 3:
        question = f"Explain {question} in detail for educational purposes."

    # 🔹 Fallback context
    if not context or len(context.strip()) < 50:
        context = (
            "This is a finance-related topic. "
            "Explain it in a clear and educational way without "
            "giving buy or sell recommendations."
        )

    final_prompt = f"""
You are a professional Finance Assistant like ChatGPT.

Rules:
- Answer ONLY finance-related questions
- Be detailed and human-like
- Do NOT guarantee returns
- Educational explanation only

Conversation History:
{history}

Context:
{context}

User Question:
{question}

Answer:
"""

    response = llm(final_prompt, max_length=512)
    return response[0]["generated_text"]


