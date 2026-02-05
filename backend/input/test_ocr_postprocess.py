import sys
import os

# Add project root to Python path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
)

from backend.input.ocr_postprocess import extract_keywords

text = """
STRRDITVON RL
GOLD
NEON
"""

print("Extracted keywords:")
print(extract_keywords(text))
