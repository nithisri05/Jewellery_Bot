from backend.retrieval.multimodal_query_engine import MultimodalQueryEngine

class ImageUploadEngine:
    def __init__(self):
        self.engine = MultimodalQueryEngine()

    def search(self, image):
        results = self.engine.retrieve_from_image(image)
        return results, "Results retrieved using image similarity."
