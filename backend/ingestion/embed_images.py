import json
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# -----------------------------
# Paths
# -----------------------------
METADATA_PATH = "data/metadata.json"

# -----------------------------
# Load CLIP model & processor
# -----------------------------
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

model.eval()

# -----------------------------
# Load metadata
# -----------------------------
with open(METADATA_PATH, "r") as f:
    metadata = json.load(f)

print("Generating CLIP PROJECTED image embeddings...")

# -----------------------------
# Generate embeddings
# -----------------------------
for item in metadata:
    image_path = item["image_path"]

    try:
        image = Image.open(image_path).convert("RGB")
    except Exception as e:
        print(f"Skipping {image_path}: {e}")
        continue

    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        # Vision encoder
        vision_outputs = model.vision_model(
            pixel_values=inputs["pixel_values"]
        )

        # 🔑 CLIP shared embedding space (512-dim)
        image_features = model.visual_projection(
            vision_outputs.pooler_output
        )

    # Normalize
    image_features = image_features / image_features.norm(dim=-1, keepdim=True)

    # Save embedding
    item["embedding"] = image_features.squeeze().tolist()

# -----------------------------
# Save updated metadata
# -----------------------------
with open(METADATA_PATH, "w") as f:
    json.dump(metadata, f, indent=2)

print(f"Saved projected embeddings for {len(metadata)} images")
