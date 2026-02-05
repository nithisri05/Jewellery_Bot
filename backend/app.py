import sys
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from PIL import Image

from backend.retrieval.chat_engine import ChatEngine
from backend.retrieval.image_upload_engine import ImageUploadEngine

# -----------------------------
# FIX PYTHON PATH
# -----------------------------
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# -----------------------------
# FASTAPI APP
# -----------------------------
app = FastAPI(
    title="Multimodal Jewellery Chatbot",
    description="Text + Image based jewellery retrieval",
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
# STATIC FILES (IMAGES)
# -----------------------------
app.mount(
    "/images",
    StaticFiles(directory="data/images"),
    name="images"
)

# -----------------------------
# ENGINES
# -----------------------------
chatbot = ChatEngine()
image_engine = ImageUploadEngine()

# -----------------------------
# DATA MODELS
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
# TEXT CHAT
# -----------------------------
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return chatbot.chat(request.message)

# -----------------------------
# IMAGE SEARCH
# -----------------------------
@app.post("/search-by-image")
async def search_by_image(file: UploadFile = File(...)):
    image = Image.open(file.file).convert("RGB")
    results, explanation = image_engine.search(image)
    return {
        "results": results,
        "explanation": explanation
    }
