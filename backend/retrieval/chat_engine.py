from backend.conversation.memory import ConversationMemory
from backend.retrieval.multimodal_query_engine import MultimodalQueryEngine


class ChatEngine:
    def __init__(self):
        self.memory = ConversationMemory()
        self.engine = MultimodalQueryEngine()
        self.last_intent = None

    def chat(self, user_message: str):
        # Maintain conversational text
        self.memory.start(user_message)
        final_query = self.memory.get_combined_query()

        response = self.engine.retrieve(
            query_text=final_query,
            previous_intent=self.last_intent
        )

        # Update intent memory only if supported
        if response.get("supported") and response.get("intent"):
            self.last_intent = response["intent"]

        return {
            "query": final_query,
            **response
        }
