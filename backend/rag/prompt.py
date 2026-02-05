def build_explanation_prompt(query_text, retrieved_items):
    context_lines = []

    for item in retrieved_items[:5]:
        context_lines.append(
            f"- Category: {item.get('category', 'unknown')}"
        )

    context = "\n".join(context_lines)

    prompt = f"""
You are a jewellery recommendation assistant.

User query:
"{query_text}"

Retrieved jewellery categories:
{context}

Explain in ONE short sentence why these items match the user's request.
Be concise. Do not list items. Do not repeat the query.
"""

    return prompt.strip()
