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

    # Debug: status + raw body (logs me dikhega)
    try:
        print("AI STATUS_CODE:", res.status_code)
        print("AI RAW RESPONSE:", res.text[:1000])  # 1000 chars tak hi
    except Exception:
        pass

    # JSON parse
    try:
        data = res.json()
    except Exception:
        return f"❌ API response not JSON:\n{res.text}"

    # ------- SAFE CHOICES HANDLING -------

    choices = data.get("choices")
    if isinstance(choices, list) and len(choices) > 0 and isinstance(choices[0], dict):
        choice = choices[0]

        content = None

        # OpenAI / DeepInfra chat-style:
        msg = choice.get("message")
        if isinstance(msg, dict):
            content = msg.get("content")

        # Streaming-style delta:
        if not content:
            delta = choice.get("delta")
            if isinstance(delta, dict):
                content = delta.get("content")

        # Text-style completion:
        if not content:
            content = choice.get("text")

        if content:
            return content

        # Yaha aa gaya matlab structure ajeeb hai
        return f"❌ AI gave empty/unknown content structure: {data}"

    # ------- ERROR FIELD HANDLING -------

    if "error" in data:
        err = data["error"]
        if isinstance(err, dict):
            msg = err.get("message") or err.get("detail") or str(err)
            return "❌ AI Error: " + msg
        return "❌ AI Error: " + str(err)

    # ------- FALLBACK -------

    return f"❌ Unexpected AI response: {data}"