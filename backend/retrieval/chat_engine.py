from backend.conversation.memory import ConversationMemory
from backend.retrieval.multimodal_query_engine import MultimodalQueryEngine

class ChatEngine:
    def __init__(self):
        self.memory = ConversationMemory()
        self.engine = MultimodalQueryEngine()

    def chat(self, message: str):
        self.memory.update(message)
        final_query = self.memory.get_combined_query()

        results = self.engine.retrieve_from_text(final_query)

        return {
            "query": final_query,
            "results": results,
            "explanation": "Results retrieved using multimodal similarity search."
        }
