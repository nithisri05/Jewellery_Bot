import os
import json
import uuid

BASE_IMAGE_DIR = "data/images"
OUTPUT_PATH = "data/metadata.json"

metadata = []

for category in os.listdir(BASE_IMAGE_DIR):
    category_path = os.path.join(BASE_IMAGE_DIR, category)

    if not os.path.isdir(category_path):
        continue

    for filename in os.listdir(category_path):
        if not filename.lower().endswith((".jpg", ".png", ".jpeg")):
            continue

        metadata.append({
            "id": str(uuid.uuid4()),
            "category": category,
            "image_path": f"data/images/{category}/{filename}"
        })

with open(OUTPUT_PATH, "w") as f:
    json.dump(metadata, f, indent=2)

print(f"Metadata generated for {len(metadata)} images across categories")
