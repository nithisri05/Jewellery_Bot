import re

# Known jewellery keywords
KEYWORDS = [
    "gold", "silver", "diamond", "ruby", "necklace",
    "ring", "traditional", "modern", "thin", "heavy"
]

def extract_keywords(ocr_text: str):
    ocr_text = ocr_text.lower()

    found = []

    for kw in KEYWORDS:
        # fuzzy-ish match
        if kw in ocr_text or any(
            abs(len(kw) - len(word)) <= 2 and kw[0] == word[:1]
            for word in re.findall(r"[a-z]+", ocr_text)
        ):
            found.append(kw)

    return list(set(found))
