import json
import faiss
import torch
import numpy as np
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# -----------------------------
# Paths

# -----------------------------
INDEX_PATH = "data/faiss.index"
ID_MAP_PATH = "data/id_mapping.json"
METADATA_PATH = "data/metadata.json"

# 🔁 Change this to test different images
QUERY_IMAGE_PATH = "D:/Jewellery-multimodal-rag/data/images/necklace/necklace_4.jpg"
TOP_K = 5

# -----------------------------
# Load FAISS index & mappings
# -----------------------------
index = faiss.read_index(INDEX_PATH)

with open(ID_MAP_PATH, "r") as f:
    id_mapping = json.load(f)

with open(METADATA_PATH, "r") as f:
    metadata = json.load(f)

metadata_dict = {item["id"]: item for item in metadata}

# -----------------------------
# Load CLIP
# -----------------------------
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

model.eval()

# -----------------------------
# Embed query image
# -----------------------------
image = Image.open(QUERY_IMAGE_PATH).convert("RGB")
inputs = processor(images=image, return_tensors="pt")

with torch.no_grad():
    vision_outputs = model.vision_model(
        pixel_values=inputs["pixel_values"]
    )
    query_embedding = vision_outputs.pooler_output

query_embedding = query_embedding / query_embedding.norm(dim=-1, keepdim=True)

query_vector = query_embedding.cpu().numpy().astype("float32")

# -----------------------------
# Search FAISS
# -----------------------------
scores, indices = index.search(query_vector, TOP_K)

print("\nTop similar jewellery results:\n")

for rank, idx in enumerate(indices[0]):
    jewellery_id = id_mapping[idx]
    item = metadata_dict[jewellery_id]

    print(f"Rank {rank+1}")
    print(f"ID        : {jewellery_id}")
    print(f"Category  : {item['category']}")
    print(f"Image     : {item['image_path']}")
    print("-" * 40)
