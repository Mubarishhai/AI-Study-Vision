import os
import requests

DEEPINFRA_KEY = os.getenv("DEEPINFRA_KEY")

def ask_ai(prompt):
    url = "https://api.deepinfra.com/v1/openai/chat/completions"

    payload = {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    headers = {
        "Authorization": f"Bearer {DEEPINFRA_KEY}",
        "Content-Type": "application/json"
    }

    res = requests.post(url, json=payload, headers=headers)
    data = res.json()

    return data["choices"][0]["message"]["content"]
