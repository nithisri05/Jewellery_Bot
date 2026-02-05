import json
import faiss
import numpy as np

# -----------------------------
# Paths
# -----------------------------
METADATA_PATH = "data/metadata.json"
INDEX_PATH = "data/faiss.index"
ID_MAP_PATH = "data/id_mapping.json"

# -----------------------------
# Load metadata
# -----------------------------
with open(METADATA_PATH, "r") as f:
    metadata = json.load(f)

# -----------------------------
# Load embeddings generated in Step 3
# (recompute-safe approach)
# -----------------------------
embeddings = []
ids = []

for item in metadata:
    if "embedding" in item:
        embeddings.append(item["embedding"])
        ids.append(item["id"])

# Convert to numpy
vectors = np.array(embeddings).astype("float32")

# -----------------------------
# Build FAISS index
# -----------------------------
dim = vectors.shape[1]
index = faiss.IndexFlatIP(dim)   # Inner Product (for normalized vectors)

index.add(vectors)

# -----------------------------
# Save index and ID mapping
# -----------------------------
faiss.write_index(index, INDEX_PATH)

with open(ID_MAP_PATH, "w") as f:
    json.dump(ids, f)

print(f"FAISS index built with {index.ntotal} vectors")
