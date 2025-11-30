import os
import requests

DEEPINFRA_KEY = os.getenv("DEEPINFRA_KEY")  # ya jo bhi env var use kar rahe ho
BASE_URL = "https://api.deepinfra.com/v1/openai/chat/completions"

def ask_ai(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {DEEPINFRA_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",  # yahan apna model
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 800,
        "temperature": 0.4,
    }

    try:
        res = requests.post(BASE_URL, json=payload, headers=headers, timeout=60)
    except Exception as e:
        return f"❌ Network error while calling AI: {e}"

    # JSON parse
    try:
        data = res.json()
    except Exception:
        return f"❌ API response not JSON:\n{res.text}"

    # YAHAN PAR SAFE HANDLING
    if "choices" in data and data["choices"]:
        # kuch providers message ko dict rakhte hain, kuch object – dono handle:
        msg = data["choices"][0].get("message") or data["choices"][0].get("delta", {})
        content = msg.get("content")
        if content:
            return content
        else:
            return f"❌ AI gave empty content: {data}"

    # agar error field hai
    if "error" in data:
        # kuch APIs: {"error": {"message": "..."}}
        err = data["error"]
        if isinstance(err, dict):
            return "❌ AI Error: " + err.get("message", str(err))
        return "❌ AI Error: " + str(err)

    # koi aur strange format
    return f"❌ Unexpected AI response: {data}"

