import os
from groq import Groq

# Groq API key from environment variable (Streamlit Cloud safe)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client (NO extra arguments)
client = Groq(api_key=GROQ_API_KEY)

def ask_ai(prompt):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1024
    )
    return response.choices[0].message["content"]


def generate_mcqs(text):
    import json

    prompt = f"""
    From this text, generate EXACTLY 5 multiple choice questions in JSON format:

    {{
      "mcqs": [
        {{
          "question": "text",
          "options": ["A", "B", "C", "D"],
          "correct_index": 1
        }}
      ]
    }}

    TEXT:
    {text}
    """

    raw = ask_ai(prompt)

    start = raw.find("{")
    end = raw.rfind("}")

    if start == -1 or end == -1:
        return []

    json_data = raw[start:end+1]

    try:
        data = json.loads(json_data)
        return data.get("mcqs", [])
    except:
        return []


def generate_notes(text):
    prompt = f"""
    Write simple study notes with 5–8 bullet points.
    Use **bold** for important terms.

    Text:
    {text}
    """

    return ask_ai(prompt)
