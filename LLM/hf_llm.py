from huggingface_hub import InferenceClient
import os

HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token=HF_TOKEN
)

def generate_answer(context, question, assumptions=None, chat_history=None):

    assumption_text = ""
    if assumptions:
        assumption_text = f"""
Assumptions (for educational analysis only):
- Investment amount: {assumptions.get("amount")}
- Risk profile: {assumptions.get("risk")}
- Time horizon: {assumptions.get("horizon")}
"""

    messages = [
        {
            "role": "system",
            "content": (
                "You are a finance-only AI assistant.\n"
                "You MAY provide educational, assumption-based financial analysis.\n"
                "You MUST NOT give personalized investment advice or buy/sell instructions.\n"
                "Use phrases like 'commonly considered', 'often used', 'one possible approach'.\n"
                "Explain reasoning, risks, and trade-offs.\n"
                "ALWAYS include a short disclaimer at the end."
            )
        },
        {
            "role": "system",
            "content": f"Context:\n{context}\n{assumption_text}"
        }
    ]

    if chat_history:
        for role, msg in chat_history[-6:]:
            messages.append({"role": role, "content": msg})

    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        messages=messages,
        max_tokens=350,
        temperature=0.4
    )

    return response.choices[0].message.content
