import pytesseract
from PIL import Image

class HandwritingInputEngine:
    def extract_text(self, image: Image.Image) -> str:
        """
        Extract text from handwritten image using OCR
        """
        text = pytesseract.image_to_string(image)
        return text.strip()
