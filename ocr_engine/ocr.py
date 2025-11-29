import easyocr
import numpy as np
from PIL import Image

reader = easyocr.Reader(['en'], gpu=False)

def extract_text_from_image(image_file):
    # Streamlit uploaded file -> PIL Image
    img = Image.open(image_file)

    # PIL -> numpy array
    img_np = np.array(img)

    # OCR
    result = reader.readtext(img_np)

    extracted_text = ""
    for res in result:
        extracted_text += res[1] + " "

    return extracted_text.strip()
