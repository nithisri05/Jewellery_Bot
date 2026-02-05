import json
import faiss
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import os
import uuid

DATA_DIR = "data/images"
INDEX_PATH = "data/faiss.index"
MAP_PATH = "data/id_mapping.json"
META_PATH = "data/metadata.json"

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
model.eval()

embeddings = []
id_mapping = {}
metadata = []

idx = 0

for category in os.listdir(DATA_DIR):
    category_path = os.path.join(DATA_DIR, category)

    if not os.path.isdir(category_path):
        continue

    for img_name in os.listdir(category_path):
        img_path = os.path.join(category_path, img_name)

        image = Image.open(img_path).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")

        with torch.no_grad():
            out = model.vision_model(pixel_values=inputs["pixel_values"])
            emb = model.visual_projection(out.pooler_output)
            emb = emb / emb.norm(dim=-1, keepdim=True)

        emb = emb.squeeze(0).numpy().astype("float32")

        item_id = str(uuid.uuid4())

        embeddings.append(emb)
        id_mapping[str(idx)] = item_id
        metadata.append({
            "id": item_id,
            "category": category,
            "image_path": img_path
        })

        idx += 1

# Build FAISS
dim = len(embeddings[0])
index = faiss.IndexFlatIP(dim)
index.add(torch.tensor(embeddings))

faiss.write_index(index, INDEX_PATH)

with open(MAP_PATH, "w") as f:
    json.dump(id_mapping, f)

with open(META_PATH, "w") as f:
    json.dump(metadata, f, indent=2)

print("✅ FAISS rebuilt successfully")
