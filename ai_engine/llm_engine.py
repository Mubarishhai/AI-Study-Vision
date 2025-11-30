import os
import json
import requests

# Groq API Key from Streamlit Secrets
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Correct Groq endpoint (DO NOT CHANGE)
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# Correct free model
GROQ_MODEL = "llama3-8b-8192"


def ask_ai(prompt):
    if not GROQ_API_KEY:
        return "❌ Error: GROQ_API_KEY missing. Set it in Streamlit Secrets."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 800,
        "temperature": 0.4,
    }

    try:
        res = requests.post(GROQ_URL, json=payload, headers=headers, timeout=60)
        data = res.json()
    except Exception as e:
        return f"❌ Network Error: {e}"

    # Handle Groq style response
    if "choices" in data:
        try:
            return data["choices"][0]["message"]["content"]
        except:
            return f"❌ Unexpected AI response: {data}"

    # If Groq returns error
    if "error" in data:
        return f"❌ Groq Error: {data['error']}"

    return f"❌ Unexpected AI response: {data}"
