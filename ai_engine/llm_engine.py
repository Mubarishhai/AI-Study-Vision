import os
import requests
from groq import Groq

# If USE_LOCAL=true → Ollama
# If not → Groq Cloud
USE_LOCAL = os.getenv("USE_LOCAL", "false").lower() == "true"

def ask_ai(prompt):

    if USE_LOCAL:
        # ---------- LOCAL OLLAMA ----------
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }

        try:
            r = requests.post(url, json=payload)
            data = r.json()
            return data.get("response", "❌ No response from Ollama")
        except Exception as e:
            return f"❌ Local Ollama error: {e}"

    else:
        # ---------- CLOUD GROQ ----------
        try:
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            chat = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}]
            )
            return chat.choices[0].message.content

        except Exception as e:
            return f"❌ Cloud AI Error: {e}"
