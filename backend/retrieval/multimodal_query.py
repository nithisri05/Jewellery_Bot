# =============================
# FIX PYTHON PATH (MUST BE FIRST)
# =============================
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
)

# =============================
# IMPORTS
# =============================
import json
import faiss
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

from backend.conversation.memory import ConversationMemory
from backend.rag.explain import generate_explanation
from backend.input.voice_input import VoiceInput

# =============================
# PATHS & SETTINGS
# =============================
INDEX_PATH = "data/faiss.index"
ID_MAP_PATH = "data/id_mapping.json"
METADATA_PATH = "data/metadata.json"

QUERY_IMAGE_PATH = "data/images/necklace/necklace_4.jpg"
INITIAL_QUERY_TEXT = "thin modern necklace"
VOICE_AUDIO_PATH = "data/audio/jewellery_audio.wav"

TOP_K = 5
IMAGE_WEIGHT = 0.6
TEXT_WEIGHT = 0.4

# =============================
# LOAD FAISS & METADATA
# =============================
index = faiss.read_index(INDEX_PATH)

with open(ID_MAP_PATH, "r") as f:
    id_mapping = json.load(f)

with open(METADATA_PATH, "r") as f:
    metadata = json.load(f)

metadata_dict = {item["id"]: item for item in metadata}

# =============================
# LOAD CLIP
# =============================
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
model.eval()

# =============================
# IMAGE EMBEDDING (ONCE)
# =============================
image = Image.open(QUERY_IMAGE_PATH).convert("RGB")
image_inputs = processor(images=image, return_tensors="pt")

with torch.no_grad():
    vision_outputs = model.vision_model(
        pixel_values=image_inputs["pixel_values"]
    )
    image_emb = model.visual_projection(
        vision_outputs.pooler_output
    )

image_emb = image_emb / image_emb.norm(dim=-1, keepdim=True)

# =============================
# RETRIEVAL FUNCTION (CORE)
# =============================
def run_retrieval(query_text):
    # Text embedding
    text_inputs = processor(
        text=[query_text],
        return_tensors="pt",
        padding=True
    )

    with torch.no_grad():
        text_outputs = model.text_model(
            input_ids=text_inputs["input_ids"],
            attention_mask=text_inputs["attention_mask"]
        )
        text_emb = model.text_projection(
            text_outputs.pooler_output
        )

    text_emb = text_emb / text_emb.norm(dim=-1, keepdim=True)

    # Multimodal fusion
    final_emb = IMAGE_WEIGHT * image_emb + TEXT_WEIGHT * text_emb
    final_emb = final_emb / final_emb.norm(dim=-1, keepdim=True)

    query_vector = final_emb.cpu().numpy().astype("float32")

    scores, indices = index.search(query_vector, TOP_K)

    results = []
    for idx in indices[0]:
        jewellery_id = id_mapping[idx]
        results.append(metadata_dict[jewellery_id])

    return results

# =============================
# CONVERSATION MEMORY
# =============================
memory = ConversationMemory()
memory.start(INITIAL_QUERY_TEXT)

# =============================
# INITIAL RETRIEVAL
# =============================
initial_query = memory.get_combined_query()
initial_results = run_retrieval(initial_query)

print("\n🔍 INITIAL RESULTS")
print("Query:", initial_query, "\n")

for i, item in enumerate(initial_results, 1):
    print(f"{i}. {item['category']} | {item['image_path']}")

print("\n🧠 INITIAL EXPLANATION:")
print(generate_explanation(initial_query, initial_results))

# =============================
# VOICE REFINEMENT (STEP-10)
# =============================
voice = VoiceInput()
voice_text = voice.transcribe(VOICE_AUDIO_PATH)

print("\n🎤 Voice input:", voice_text)

memory.update(voice_text)
updated_query = memory.get_combined_query()

print("🔁 Updated query:", updated_query)

# =============================
# REFINED RETRIEVAL (STEP-11)
# =============================
refined_results = run_retrieval(updated_query)

print("\n🔁 REFINED RESULTS (After Voice)")
for i, item in enumerate(refined_results, 1):
    print(f"{i}. {item['category']} | {item['image_path']}")

print("\n🧠 UPDATED EXPLANATION:")
print(generate_explanation(updated_query, refined_results))
