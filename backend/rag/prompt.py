def build_explanation_prompt(query_text, retrieved_items):
    context = ""

    for i, item in enumerate(retrieved_items, start=1):
        context += (
            f"{i}. Category: {item.get('category', 'unknown')}\n"
            f"   Image Path: {item.get('image_path', 'unknown')}\n\n"
        )

    prompt = f"""
You are a jewellery recommendation assistant.

User request:
"{query_text}"

Retrieved jewellery designs:
{context}

Explain clearly WHY these jewellery designs match the user's request.
Base your explanation ONLY on the retrieved designs above.
Do not add extra assumptions.
"""

    return prompt
