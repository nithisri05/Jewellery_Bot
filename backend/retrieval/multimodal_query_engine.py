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

        # 🔹 Supported categories (dynamic)
        self.supported_categories = sorted(
            list(set(item["category"].lower() for item in self.metadata))
        )

        # 🔹 Precompute category embeddings
        self.category_embeddings = self._embed_categories()

        self.INTENT_THRESHOLD = 0.20

    # ---------------- PATH NORMALIZATION ----------------
    def _normalize_image_path(self, path: str):
        path = path.replace("\\", "/")
        if path.startswith("data/images/"):
            return path.replace("data/images/", "")
        return path

    # ---------------- CATEGORY EMBEDDINGS ----------------
    def _embed_categories(self):
        inputs = self.processor(
            text=self.supported_categories,
            return_tensors="pt",
            padding=True
        )

        with torch.no_grad():
            outputs = self.model.text_model(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"]
            )
            features = self.model.text_projection(outputs.pooler_output)

        features = features / features.norm(dim=-1, keepdim=True)
        return features.cpu().numpy()

    # ---------------- INTENT DETECTION ----------------
    def _detect_intent(self, text: str):
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
            query_emb = self.model.text_projection(outputs.pooler_output)

        query_emb = query_emb / query_emb.norm(dim=-1, keepdim=True)
        query_vec = query_emb.cpu().numpy()

        sims = np.dot(query_vec, self.category_embeddings.T)[0]
        best_idx = int(np.argmax(sims))
        best_score = float(sims[best_idx])

        if best_score >= self.INTENT_THRESHOLD:
            return self.supported_categories[best_idx]

        return None

    # ---------------- INTENT WITH FOLLOW-UP ----------------
    def resolve_intent(self, text: str, previous_intent: str | None):
        intent = self._detect_intent(text)
        if intent:
            return intent, "new"

        if previous_intent:
            return previous_intent, "followup"

        return None, "unsupported"

    # ---------------- FAISS SEARCH ----------------
    def _search(self, query_vector, top_k=5):
        scores, indices = self.index.search(query_vector, top_k)

        results = []
        for idx in indices[0]:
            item_id = self.id_map[str(idx)]
            item = self.metadata_dict[item_id].copy()
            item["image_path"] = self._normalize_image_path(item["image_path"])
            results.append(item)

        return results

    # ---------------- MAIN ENTRY (ALL MODALITIES) ----------------
    def retrieve(self, query_text: str, previous_intent: str | None = None):
        intent, intent_type = self.resolve_intent(query_text, previous_intent)

        if intent is None:
            return {
                "supported": False,
                "suggested_categories": self.supported_categories,
                "results": [],
                "explanation": None
            }

        # Encode query for retrieval
        inputs = self.processor(
            text=[query_text],
            return_tensors="pt",
            padding=True
        )

        with torch.no_grad():
            outputs = self.model.text_model(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"]
            )
            features = self.model.text_projection(outputs.pooler_output)

        features = features / features.norm(dim=-1, keepdim=True)
        query_vector = features.cpu().numpy().astype("float32")

        results = self._search(query_vector)
        explanation = generate_explanation(query_text, results)

        return {
            "supported": True,
            "intent": intent,
            "intent_type": intent_type,
            "results": results,
            "explanation": explanation
        }
