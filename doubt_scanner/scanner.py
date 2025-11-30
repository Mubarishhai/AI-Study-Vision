import pytesseract
from PIL import Image
import io

def scan_doubt(image_file):
    img = Image.open(io.BytesIO(image_file.read()))
    text = pytesseract.image_to_string(img)
    return text

