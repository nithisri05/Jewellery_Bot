import sys
import os
import tempfile
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from PIL import Image

# -----------------------------
# Fix Python path
# -----------------------------
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# -----------------------------
# Internal imports
# -----------------------------
from backend.retrieval.chat_engine import ChatEngine
from backend.retrieval.image_upload_engine import ImageUploadEngine
from backend.input.voice_input import VoiceInputEngine
from backend.input.handwriting_input import HandwritingInputEngine

# -----------------------------
# FastAPI app
# -----------------------------
app = FastAPI(
    title="Multimodal Jewellery Chatbot",
    description="Text, Image, Voice, and Handwriting based jewellery retrieval",
    version="1.0"
)

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Static files (images)
# -----------------------------
app.mount(
    "/images",
    StaticFiles(directory="data/images"),
    name="images"
)

# -----------------------------
# Engines (loaded once)
# -----------------------------
chat_engine = ChatEngine()
image_engine = ImageUploadEngine()
voice_engine = VoiceInputEngine()
handwriting_engine = HandwritingInputEngine()

# -----------------------------
# Pydantic models
# -----------------------------
class JewelleryItem(BaseModel):
    id: str
    category: str
    image_path: str

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    query: str
    results: List[JewelleryItem]
    explanation: str

# -----------------------------
# TEXT → IMAGE
# -----------------------------
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return chat_engine.chat(request.message)

# -----------------------------
# IMAGE → IMAGE
# -----------------------------
@app.post("/search-by-image")
async def search_by_image(file: UploadFile = File(...)):
    image = Image.open(file.file).convert("RGB")
    results, explanation = image_engine.search(image)

    return {
        "results": results,
        "explanation": explanation
    }

# -----------------------------
# VOICE → IMAGE
# -----------------------------
@app.post("/search-by-voice")
async def search_by_voice(file: UploadFile = File(...)):
    # Save audio temporarily
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
        temp_audio.write(await file.read())
        temp_audio_path = temp_audio.name

    # Speech → text
    text_query = voice_engine.speech_to_text(temp_audio_path)

    # Text → image retrieval
    results = chat_engine.engine.retrieve_from_text(text_query)

    # Cleanup
    os.remove(temp_audio_path)

    return {
        "query": text_query,
        "results": results,
        "explanation": "Results retrieved using voice input."
    }

# -----------------------------
# HANDWRITING → IMAGE
# -----------------------------
@app.post("/search-by-handwriting")
async def search_by_handwriting(file: UploadFile = File(...)):
    image = Image.open(file.file).convert("RGB")

    # OCR → text
    text_query = handwriting_engine.extract_text(image)

    # Text → image retrieval
    results = chat_engine.engine.retrieve_from_text(text_query)

    return {
        "query": text_query,
        "results": results,
        "explanation": "Results retrieved using handwritten input."
    }
