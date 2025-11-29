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
    import json

    prompt = f"""
    From the following text, generate EXACTLY 5 multiple choice questions.

    Format JSON only:
    {{
      "mcqs": [
        {{
          "question": "text",
          "options": ["A", "B", "C", "D"],
          "correct_index": 1
        }}
      ]
    }}

    Text:
    {text}
    """

    raw = ask_ai(prompt)

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

def generate_notes(text):
    prompt = f"""
    Create short study notes for this topic.

    Text:
    {text}

    Format:
    - 5 to 8 bullet points
    - Very simple language
    - Highlight important terms with **bold**
    """

    return ask_ai(prompt)
