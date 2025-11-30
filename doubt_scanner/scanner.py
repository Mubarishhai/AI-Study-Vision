import base64
import requests

GROQ_API_KEY = "YOUR_API_KEY"

def scan_doubt(image_file):
    url = "https://api.groq.com/openai/v1/chat/completions"

    # Convert image to base64
    img_bytes = image_file.read()
    img_b64 = base64.b64encode(img_bytes).decode()

    payload = {
        "model": "llama-3.2-vision",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract the text exactly from this image"},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{img_b64}"
                    }
                ]
            }
        ]
    }

    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}

    response = requests.post(url, json=payload, headers=headers)
    result = response.json()

    return result["choices"][0]["message"]["content"]
