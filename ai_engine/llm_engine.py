import requests
import json

def ask_ai(prompt):
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload)

    data = response.json()

    return data["response"]
def generate_mcqs(text):
    prompt = f"""
    Generate 5 MCQs from this topic:

    {text}

    Format:
    1. Question?
       a) option
       b) option
       c) option
       d) option
       Answer: a)
    """

    return ask_ai(prompt)