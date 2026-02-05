import faiss
import json
import torch
import numpy as np
from backend.models.clip_singleton import CLIPSingleton

INDEX_PATH = "data/faiss.index"
ID_MAP_PATH = "data/id_mapping.json"
METADATA_PATH = "data/metadata.json"

class MultimodalQueryEngine:
    def __init__(self):
        self.index = faiss.read_index(INDEX_PATH)

        with open(ID_MAP_PATH) as f:
            self.id_map = json.load(f)

        with open(METADATA_PATH) as f:
            self.metadata = json.load(f)

        self.metadata_dict = {
            item["id"]: item for item in self.metadata
        }

        self.model, self.processor = CLIPSingleton.load()

    def _search(self, query_vector, top_k=5):
        scores, indices = self.index.search(query_vector, top_k)

        results = []
        for idx in indices[0]:
            item_id = self.id_map[str(idx)]
            results.append(self.metadata_dict[item_id])

        return results

    def retrieve_from_text(self, text: str):
        inputs = self.processor(
            text=[text],
            return_tensors="pt",
            padding=True
        )

        with torch.no_grad():
            outputs = self.model.text_model(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"]
            )
            features = self.model.text_projection(
                outputs.pooler_output
            )

        features = features / features.norm(dim=-1, keepdim=True)
        query_vector = features.cpu().numpy().astype("float32")

        return self._search(query_vector)

    def retrieve_from_image(self, image):
        inputs = self.processor(images=image, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model.vision_model(
                pixel_values=inputs["pixel_values"]
            )
            features = self.model.visual_projection(
                outputs.pooler_output
            )

        features = features / features.norm(dim=-1, keepdim=True)
        query_vector = features.cpu().numpy().astype("float32")

        return self._search(query_vector)
