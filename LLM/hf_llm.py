from huggingface_hub import InferenceClient
from huggingface_hub.utils import HfHubHTTPError
import os
import time

# ---------------- HF CLIENT (MUST BE GLOBAL) ----------------
HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token=HF_TOKEN
)

# ---------------- GENERATE ANSWER ----------------
def generate_answer(context, question, assumptions=None, chat_history=None):
    """
    Generates finance-only, compliant responses with retry handling
    for Hugging Face model warm-up.
    """

    # -------- ASSUMPTIONS TEXT --------
    assumption_text = ""
    if assumptions:
        assumption_text = "Assumptions for educational analysis:\n"
        for k, v in assumptions.items():
            assumption_text += f"- {k.capitalize()}: {v}\n"

    # -------- SYSTEM PROMPT --------
    system_prompt = """
You are an AI Finance Assistant.

Scope:
- Answer ONLY finance-related questions.
- Politely refuse non-finance questions.

Rules:
- No buy/sell instructions
- No guaranteed returns
- Educational, analysis-based insights only
- Use phrases like "commonly considered", "often analyzed"
- Always explain reasoning
- Always mention risks
- If assumptions are provided, tailor the explanation to those assumptions
- Always end with a disclaimer
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": f"Context:\n{context}\n\n{assumption_text}"}
    ]

    if chat_history:
        for role, msg in chat_history[-6:]:
            messages.append({"role": role, "content": msg})

    messages.append({"role": "user", "content": question})

    # -------- RETRY LOGIC FOR MODEL WARM-UP --------
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                messages=messages,
                max_tokens=350,
                temperature=0.4
            )
            return response.choices[0].message.content

        except HfHubHTTPError as e:
            if "model_pending_deploy" in str(e):
                time.sleep(20)  # wait for model warm-up
            else:
                raise e

    return "⚠️ The model is currently warming up. Please try again in a moment."
