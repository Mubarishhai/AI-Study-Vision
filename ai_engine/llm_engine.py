import os
import json
import requests

# Groq API key ko env variable se lo (Streamlit Secrets se aayegi)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-8b-8192"   # Fast + smart


def _call_groq_chat(prompt: str) -> dict:
    """
    Groq API ko safe tarike se call karta hai
    JSON response return karta hai (ya error dict).
    """

    if not GROQ_API_KEY:
        return {"error": "GROQ_API_KEY missing. Set it in Streamlit Secrets."}

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 800,
        "temperature": 0.4,
    }

    try:
        res = requests.post(GROQ_URL, json=payload, headers=headers, timeout=60)
    except Exception as e:
        return {"error": f"Network error while calling Groq: {e}"}

    try:
        data = res.json()
    except Exception:
        return {"error": f"Groq non-JSON response: {res.text}"}

    return data


def ask_ai(prompt: str) -> str:
    """
    Simple text answer (Explanation, Chat, Doubt solution, etc.)
    """

    data = _call_groq_chat(prompt)

    # error field aa gaya
    if "error" in data:
        err = data["error"]
        return f"❌ AI Error: {err}"

    # normal OpenAI-style response
    if "choices" in data and data["choices"]:
        msg = data["choices"][0].get("message", {})
        content = msg.get("content")
        if content:
            return content

    # kuch unexpected mila
    return f"❌ Unexpected AI response: {data}"


def generate_mcqs(text: str):
    """
    Text se EXACT 5 MCQs JSON format me banata hai.
    """

    prompt = f"""
    From the following text, generate EXACTLY 5 multiple choice questions.

    Reply in PURE JSON only, with this exact structure:

    {{
      "mcqs": [
        {{
          "question": "Question text here",
          "options": ["Option A", "Option B", "Option C", "Option D"],
          "correct_index": 0
        }}
      ]
    }}

    Don't add any explanation text outside JSON.
    Text:
    {text}
    """

    raw = ask_ai(prompt)

    # JSON extract
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1:
        return []

    json_str = raw[start:end+1]

    try:
        data = json.loads(json_str)
        return data.get("mcqs", [])
    except Exception:
        return []


def generate_notes(text: str) -> str:
    """
    Chhote, clean study notes banata hai.
    """

    prompt = f"""
    Create short study notes for the following content.

    Rules:
    - Use 5 to 8 bullet points.
    - Use very simple language.
    - Highlight important terms with **bold**.
    - Output should be in Markdown.

    Text:
    {text}
    """

    return ask_ai(prompt)
