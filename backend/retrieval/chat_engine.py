from backend.retrieval.multimodal_query_engine import MultimodalQueryEngine
from backend.rag.explain import RealLLM

CATEGORY_SYNONYMS = {
    "ring": ["ring", "band"],
    "necklace": ["necklace", "chain", "pendant"]
}

def normalize_query(text: str) -> str:
    t = text.lower()
    for canonical, synonyms in CATEGORY_SYNONYMS.items():
        for s in synonyms:
            if s in t:
                return canonical + " " + text
    return text


def detect_category(text: str):
    t = text.lower()
    for cat, synonyms in CATEGORY_SYNONYMS.items():
        for s in synonyms:
            if s in t:
                return cat
    return None


class ChatEngine:
    def __init__(self):
        self.engine = MultimodalQueryEngine()
        self.llm = RealLLM()

        # conversational memory
        self.last_image = None
        self.last_category = None

    # ---------- CHAT INTENT ----------
    def detect_intent(self, text: str) -> str:
        prompt = f"""
Classify the intent of the message.

Message:
"{text}"

Return ONLY one word:
chat or search
"""
        try:
            r = self.llm.generate(prompt).lower()
            return "search" if "search" in r else "chat"
        except Exception:
            return "search"

    # ---------- CHAT RESPONSE ----------
    def chat_reply(self, text: str) -> str:
        prompt = f"""
You are a friendly jewellery assistant.

User said:
"{text}"

Reply naturally like a normal chatbot.
Ask what jewellery they want if appropriate.
"""
        try:
            return self.llm.generate(prompt)
        except Exception:
            return "🙂 I’m here to help! Tell me what jewellery you’re looking for."

    # ---------- MAIN ENTRY ----------
    def handle(self, *, text="", image=None, force_search=False):

        # 🔹 IMAGE UPLOAD → STORE & WAIT
        if image is not None:
            self.last_image = image
            return {
                "type": "chat",
                "message": (
                    "📷 Image received.\n"
                    "Now tell me what you want from this image "
                    "(for example: elegant, gold, necklace)."
                ),
                "results": [],
                "explanation": ""
            }

        # 🔹 VOICE / HANDWRITING → FORCE SEARCH
        if force_search:
            text = normalize_query(text)
            category = detect_category(text)

            if category != self.last_category:
                self.last_image = None
                self.last_category = category

            result = self.engine.retrieve(text=text, image=self.last_image)
            return {"type": "search", **result}

        # 🔹 PURE TEXT → INTENT CHECK
        intent = self.detect_intent(text)

        if intent == "chat":
            return {
                "type": "chat",
                "message": self.chat_reply(text),
                "results": [],
                "explanation": ""
            }

        # 🔹 SEARCH
        text = normalize_query(text)
        category = detect_category(text)

        # reset context if category changes
        if category and category != self.last_category:
            self.last_image = None

        self.last_category = category

        result = self.engine.retrieve(text=text, image=self.last_image)
        return {"type": "search", **result}
