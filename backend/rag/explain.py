import os
import requests
from backend.rag.prompt import build_explanation_prompt

BASE_URL = os.getenv("LLM_BASE_URL")
API_KEY  = os.getenv("LLM_API_KEY")
MODEL    = os.getenv("LLM_MODEL")

class RealLLM:
    def generate(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "You are a helpful jewellery assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.4
        }

        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

def generate_explanation(query_text, retrieved_items):
    prompt = build_explanation_prompt(query_text, retrieved_items)
    llm = RealLLM()
    return llm.generate(prompt)
