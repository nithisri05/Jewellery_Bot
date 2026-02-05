from PIL import Image
from backend.retrieval.multimodal_query_engine import MultimodalQueryEngine

engine = MultimodalQueryEngine()

image = Image.open("data/images/necklace/necklace_4.jpg").convert("RGB")
results = engine.retrieve_from_image(image)

for r in results:
    print(r["id"], r["category"], r["image_path"])
