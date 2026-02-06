import os
import requests
from backend.rag.prompt import build_explanation_prompt

BASE_URL = os.getenv("LLM_BASE_URL")
API_KEY  = os.getenv("LLM_API_KEY")
MODEL    = os.getenv("LLM_MODEL")


class RealLLM:
    def generate(self, prompt: str) -> str:
        if not BASE_URL or not API_KEY or not MODEL:
            raise RuntimeError("LLM not configured")

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "You are a jewellery assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }

        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )

        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]


def generate_explanation(query_text, retrieved_items):
    if not retrieved_items:
        return ""

    try:
        prompt = build_explanation_prompt(query_text, retrieved_items)
        llm = RealLLM()
        return llm.generate(prompt)
    except Exception:
        categories = list(
            {item.get("category", "") for item in retrieved_items}
        )
        return (
            f"These designs match your request for {', '.join(categories)} "
            f"based on visual style and similarity."
        )
