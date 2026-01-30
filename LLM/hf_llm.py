# import os
# import re
# import time
# from dotenv import load_dotenv

# from langchain_community.llms import HuggingFaceHub
# from langchain.schema import SystemMessage, HumanMessage

# # -------------------------------------------------
# # LOAD ENV
# # -------------------------------------------------
# load_dotenv()

# HF_TOKEN = os.getenv("HF_TOKEN")
# if not HF_TOKEN:
#     raise ValueError("HF_TOKEN not found in .env")

# # -------------------------------------------------
# # LANGSMITH (AUTO-TRACING)
# # -------------------------------------------------
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_PROJECT"] = os.getenv(
#     "LANGCHAIN_PROJECT", "ai-finance-assistant"
# )

# # -------------------------------------------------
# # LLM
# # -------------------------------------------------
# llm = HuggingFaceHub(
#     repo_id="mistralai/Mistral-7B-Instruct-v0.2",
#     huggingfacehub_api_token=HF_TOKEN,
#     model_kwargs={
#         "temperature": 0.3,
#         "max_new_tokens": 500
#     }
# )

# # -------------------------------------------------
# # HELPERS
# # -------------------------------------------------
# def clean_text(text: str) -> str:
#     return re.sub(r"<.*?>", "", text)

# # -------------------------------------------------
# # MAIN FUNCTION (UNCHANGED SIGNATURE)
# # -------------------------------------------------
# def generate_answer(context, question, assumptions=None, chat_history=None):

#     system_prompt = """
# You are an AI Finance Assistant.

# Rules:
# - Answer ONLY finance-related questions
# - Educational explanation only
# - No buy/sell advice
# - Always mention risks
# - End with a disclaimer
# """

#     context = context[:1500]

#     messages = [SystemMessage(content=system_prompt)]

#     if context:
#         messages.append(
#             SystemMessage(content=f"Context:\n{context}")
#         )

#     if chat_history:
#         for role, msg in chat_history[-3:]:
#             if role == "user":
#                 messages.append(HumanMessage(content=msg))

#     messages.append(HumanMessage(content=question))

#     # ---------- TRY TWICE (HF COLD START FIX) ----------
#     for attempt in range(2):
#         try:
#             response = llm(messages)
#             return clean_text(response)

#         except Exception:
#             if attempt == 0:
#                 time.sleep(6)  # allow HF model to wake up
#                 continue

#             return (
#                 "⚠️ The AI model is temporarily unavailable due to high load.\n\n"
#                 "Please try again in a few seconds."
#             )


import os
import re
from dotenv import load_dotenv
import google.generativeai as genai

# -------------------------------------------------
# LOAD ENV
# -------------------------------------------------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# -------------------------------------------------
# GEMINI CONFIG
# -------------------------------------------------
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config={
        "temperature": 0.3,
        "max_output_tokens": 1200
    }
)

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def clean_text(text: str) -> str:
    return re.sub(r"<.*?>", "", text)

# -------------------------------------------------
# MAIN FUNCTION (SIGNATURE UNCHANGED)
# -------------------------------------------------
def generate_answer(context, question, assumptions=None, chat_history=None):

    system_prompt = """
You are an AI Finance Assistant.

Rules:
- Answer ONLY finance-related questions
- Educational explanation only
- No buy/sell advice
- Always mention risks
- End with a disclaimer
"""

    context = context.strip()[:1500]

    if not context:
        context = f"The user is asking a finance-related conceptual question about: {question}"

    prompt = f"""
{system_prompt}

Context:
{context}

Question:
{question}
"""

    try:
        response = model.generate_content(prompt)
        return clean_text(response.text)

    except Exception:
        return (
            "⚠️ The AI service is temporarily unavailable.\n\n"
            "Please try again in a moment."
        )
