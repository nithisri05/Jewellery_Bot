from backend.retrieval.multimodal_query_engine import MultimodalQueryEngine

engine = MultimodalQueryEngine()

query = "thin gold necklace with stones"
results = engine.retrieve_from_text(query)

print("Query:", query)
for r in results:
    print(r["id"], r["category"], r["image_path"])
