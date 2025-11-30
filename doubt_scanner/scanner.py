import easyocr
from PIL import Image
import numpy as np
import io

reader = easyocr.Reader(['en'], gpu=False)

def scan_doubt(image_file):
    # Converting uploaded image to array
    image_bytes = image_file.read()
    image = Image.open(io.BytesIO(image_bytes))
    image = np.array(image)

    # OCR extract text
    result = reader.readtext(image, detail=0)
    extracted_text = "\n".join(result)

    return extracted_text
