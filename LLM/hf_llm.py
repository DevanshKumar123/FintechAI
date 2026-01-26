from huggingface_hub import InferenceClient
import os

<<<<<<< HEAD
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
=======
HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token=HF_TOKEN
)

def generate_answer(context, question, chat_history=None):
    """
    Uses Hugging Face conversational API (Chat Completion)
    """

    messages = [
        {
            "role": "system",
            "content": (
                "You are a finance-only AI assistant. "
                "Answer only questions related to finance, stocks, mutual funds, "
                "investments, and taxation. "
                "Do not give buy/sell signals or guaranteed returns. "
                "Mention risks and add a disclaimer."
            )
        },
        {
            "role": "system",
            "content": f"Context information:\n{context}"
        }
    ]

    # Optional chat memory
    if chat_history:
        for role, msg in chat_history:
            messages.append({"role": role, "content": msg})

    messages.append({"role": "user", "content": question})
>>>>>>> 7c8d023 (Updated info)

    response = client.chat.completions.create(
        messages=messages,
        max_tokens=300,
        temperature=0.4
    )

<<<<<<< HEAD
User Question:
{question}

Answer:
"""

    response = llm(final_prompt, max_length=512)
    return response[0]["generated_text"]


=======
    return response.choices[0].message.content
>>>>>>> 7c8d023 (Updated info)
