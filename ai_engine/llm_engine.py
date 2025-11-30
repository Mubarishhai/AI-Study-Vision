import os
import requests

DEEPINFRA_KEY = os.getenv("DEEPINFRA_API_KEY")  # ya jo bhi env var use kar rahe ho
BASE_URL = "https://api.deepinfra.com/v1/openai/chat/completions"

def ask_ai(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {DEEPINFRA_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 800,
        "temperature": 0.4,
    }

    try:
        res = requests.post(BASE_URL, json=payload, headers=headers, timeout=60)
    except Exception as e:
        return f"❌ Network error while calling AI: {e}"

    try:
        data = res.json()
    except:
        return f"❌ API response not JSON:\n{res.text}"

    if "choices" in data and data["choices"]:
        choice = data["choices"][0]

        # 🔥 DeepInfra LLaMA output
        if "text" in choice:
            return choice["text"]

        # 🔥 OpenAI-style output
        if "message" in choice:
            return choice["message"].get("content", "")

        return f"❌ Unknown AI output: {data}"

    if "error" in data:
        err = data["error"]
        return "❌ AI Error: " + (err.get("message") if isinstance(err, dict) else str(err))

    return f"❌ Unexpected AI response: {data}"