import sys
import os

# Add project root to Python path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
)

from backend.input.handwriting_input import HandwritingInput

hw = HandwritingInput()

text = hw.extract_text("data/handwritten/notes1.jpeg")

print("Recognized handwriting:")
print(text)
