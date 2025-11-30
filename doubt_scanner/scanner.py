import requests

OCR_API_KEY = "helloworld"   # Safe free API key

def scan_doubt(image_file):
    url = "https://api.ocr.space/parse/image"

    payload = {
        'apikey': OCR_API_KEY,
        'language': 'eng',
        'scale': True,
        'OCREngine': 2
    }

    files = {
        'file': (image_file.name, image_file, image_file.type)
    }

    response = requests.post(url, data=payload, files=files)
    result = response.json()

    # 🔥 Correct OCR output extraction
    try:
        return result["ParsedResults"][0]["ParsedText"]
    except Exception as e:
        return f"❌ OCR Error: Could not extract text.\n{e}"
