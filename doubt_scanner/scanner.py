from paddleocr import PaddleOCR
from PIL import Image
import numpy as np

# Load OCR only once
ocr = PaddleOCR(lang='en', use_angle_cls=True)

def scan_doubt(image_path):
    img = Image.open(image_path).convert("RGB")
    img_np = np.array(img)

    result = ocr.ocr(img_np, cls=True)

    text_output = []
    for line in result:
        for part in line:
            text_output.append(part[1][0])

    return "\n".join(text_output)