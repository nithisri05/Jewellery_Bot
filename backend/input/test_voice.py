import sys
import os

# -----------------------------
# Fix import path
# -----------------------------
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
)

# -----------------------------
# Imports
# -----------------------------
from backend.input.voice_input import VoiceInputEngine
from backend.retrieval.multimodal_query_engine import MultimodalQueryEngine

# -----------------------------
# Initialize engines
# -----------------------------
voice_engine = VoiceInputEngine()
retrieval_engine = MultimodalQueryEngine()

# -----------------------------
# Path to audio file
# -----------------------------
AUDIO_PATH = r"D:\Jewellery-multimodal-rag\data\audio\jewellery_audio.wav"


# -----------------------------
# Voice → Text
# -----------------------------
print("\n--- VOICE TO TEXT ---")
text_query = voice_engine.speech_to_text(AUDIO_PATH)
print("Recognized text:", text_query)

# -----------------------------
# Text → Image Retrieval
# -----------------------------
print("\n--- RETRIEVED RESULTS ---")
results = retrieval_engine.retrieve_from_text(text_query)

for rank, item in enumerate(results, start=1):
    print(f"Rank {rank}")
    print("ID       :", item["id"])
    print("Category :", item["category"])
    print("Image    :", item["image_path"])
    print("-" * 40)
