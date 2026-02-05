import json
import faiss
import torch
import numpy as np
from transformers import CLIPProcessor, CLIPModel

# -----------------------------
# Paths
# -----------------------------
INDEX_PATH = "data/faiss.index"
ID_MAP_PATH = "data/id_mapping.json"
METADATA_PATH = "data/metadata.json"

QUERY_TEXT = "thin gold necklace with stones"
TOP_K = 5

# -----------------------------
# Load FAISS & metadata
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
# Encode TEXT → CLIP SHARED SPACE
# -----------------------------
inputs = processor(
    text=[QUERY_TEXT],
    return_tensors="pt",
    padding=True
)

with torch.no_grad():
    text_outputs = model.text_model(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"]
    )

    # 🔑 CLIP shared embedding space
    text_features = model.text_projection(
        text_outputs.pooler_output
    )

# Normalize
text_features = text_features / text_features.norm(dim=-1, keepdim=True)

query_vector = text_features.cpu().numpy().astype("float32")
print("FAISS index dimension:", index.d)
print("Query vector shape:", query_vector.shape)

# -----------------------------
# FAISS search
# -----------------------------
scores, indices = index.search(query_vector, TOP_K)

print("\nTop jewellery results for TEXT query\n")
print(f"Query: {QUERY_TEXT}\n")

for rank, idx in enumerate(indices[0]):
    jewellery_id = id_mapping[idx]
    item = metadata_dict[jewellery_id]

    print(f"Rank {rank+1}")
    print(f"ID       : {jewellery_id}")
    print(f"Category : {item['category']}")
    print(f"Image    : {item['image_path']}")
    print("-" * 40)
    