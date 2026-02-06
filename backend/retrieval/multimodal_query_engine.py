import faiss
import json
import torch
import numpy as np
from backend.models.clip_singleton import CLIPSingleton
from backend.rag.explain import generate_explanation

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

        self.metadata_dict = {item["id"]: item for item in self.metadata}

        self.model, self.processor = CLIPSingleton.load()

    # ---------- TEXT EMBEDDING ----------
    def _embed_text(self, text: str):
        inputs = self.processor(
            text=[text],
            return_tensors="pt",
            padding=True
        )
        with torch.no_grad():
            out = self.model.text_model(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"]
            )
            emb = self.model.text_projection(out.pooler_output)

        emb = emb / emb.norm(dim=-1, keepdim=True)
        return emb.cpu().numpy().astype("float32")

    # ---------- IMAGE EMBEDDING ----------
    def _embed_image(self, image):
        inputs = self.processor(images=image, return_tensors="pt")
        with torch.no_grad():
            out = self.model.vision_model(
                pixel_values=inputs["pixel_values"]
            )
            emb = self.model.visual_projection(out.pooler_output)

        emb = emb / emb.norm(dim=-1, keepdim=True)
        return emb.cpu().numpy().astype("float32")

    # ---------- SEARCH ----------
    def _search(self, vector, top_k=5):
        _, indices = self.index.search(vector, top_k)
        results = []

        for idx in indices[0]:
            item = self.metadata_dict[self.id_map[str(idx)]].copy()
            item["image_path"] = (
                item["image_path"]
                .replace("\\", "/")
                .replace("data/images/", "")
            )
            results.append(item)

        return results

    # ---------- PUBLIC API ----------
    def retrieve(self, text="", image=None):
        if image is not None:
            img_vec = self._embed_image(image)
            if text.strip():
                txt_vec = self._embed_text(text)
                vec = 0.6 * img_vec + 0.4 * txt_vec
            else:
                vec = img_vec
        else:
            vec = self._embed_text(text)

        vec = vec / np.linalg.norm(vec)
        results = self._search(vec)

        try:
            explanation = generate_explanation(text or "image query", results)
        except Exception:
            explanation = ""

        return {
            "results": results,
            "explanation": explanation
        }
