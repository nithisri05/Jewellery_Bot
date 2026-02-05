import sys
import os
import tempfile
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from PIL import Image

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from backend.retrieval.chat_engine import ChatEngine
from backend.input.voice_input import VoiceInputEngine
from backend.input.handwriting_input import HandwritingInputEngine

app = FastAPI(title="Multimodal Jewellery Chatbot", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/images", StaticFiles(directory="data/images"), name="images")

chat_engine = ChatEngine()
voice_engine = VoiceInputEngine()
handwriting_engine = HandwritingInputEngine()

# ---------------- TEXT ONLY ----------------
@app.post("/chat")
def chat(payload: dict):
    return chat_engine.chat(payload.get("message", ""))

# ---------------- IMAGE + TEXT ----------------
@app.post("/search-by-image")
async def search_by_image(
    file: UploadFile = File(...),
    query: str = Form(...)
):
    image = Image.open(file.file).convert("RGB")

    # Combine image context + text query
    combined_query = query

    response = chat_engine.engine.retrieve(
        query_text=combined_query,
        previous_intent=chat_engine.last_intent
    )

    if response.get("supported") and response.get("intent"):
        chat_engine.last_intent = response["intent"]

    return {
        "query": combined_query,
        **response
    }

# ---------------- VOICE ----------------
@app.post("/search-by-voice")
async def search_by_voice(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        temp_path = tmp.name

    text_query = voice_engine.speech_to_text(temp_path)
    os.remove(temp_path)

    response = chat_engine.engine.retrieve(
        query_text=text_query,
        previous_intent=chat_engine.last_intent
    )

    if response.get("supported") and response.get("intent"):
        chat_engine.last_intent = response["intent"]

    return {"query": text_query, **response}

# ---------------- HANDWRITING ----------------
@app.post("/search-by-handwriting")
async def search_by_handwriting(file: UploadFile = File(...)):
    image = Image.open(file.file).convert("RGB")
    text_query = handwriting_engine.extract_text(image)

    response = chat_engine.engine.retrieve(
        query_text=text_query,
        previous_intent=chat_engine.last_intent
    )

    if response.get("supported") and response.get("intent"):
        chat_engine.last_intent = response["intent"]

    return {"query": text_query, **response}
