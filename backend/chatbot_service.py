import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")
GROQ_PROMPT = os.getenv("GROQ_PROMPT", "Tu es un assistant éducatif.")
GROQ_API_URL = os.getenv("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")


def ask_groq_chatbot(user_message: str, history=None):
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY non défini dans l'environnement.")
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    messages = []
    if GROQ_PROMPT:
        messages.append({"role": "system", "content": GROQ_PROMPT})
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message})
    data = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.7
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    try:
        response.raise_for_status()
    except Exception:
        print("Réponse Groq:", response.text)
        raise
    result = response.json()
    return result["choices"][0]["message"]["content"]
