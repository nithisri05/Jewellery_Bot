from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from PIL import Image
import tempfile, os

from backend.retrieval.chat_engine import ChatEngine
from backend.input.voice_input import VoiceInputEngine
from backend.input.handwriting_input import HandwritingInputEngine

app = FastAPI(title="Multimodal Jewellery Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/images", StaticFiles(directory="data/images"), name="images")

chatbot = ChatEngine()
voice_engine = VoiceInputEngine()
handwriting_engine = HandwritingInputEngine()

# -------- TEXT --------
@app.post("/chat")
def chat(payload: dict):
    return chatbot.handle(text=payload.get("message", ""))

# -------- IMAGE --------
@app.post("/search-by-image")
async def search_by_image(file: UploadFile = File(...)):
    image = Image.open(file.file).convert("RGB")
    return chatbot.handle(image=image)

# -------- VOICE --------
@app.post("/search-by-voice")
async def search_by_voice(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        path = tmp.name

    text = voice_engine.speech_to_text(path)
    os.remove(path)

    return chatbot.handle(text=text, force_search=True)

# -------- HANDWRITING --------
@app.post("/search-by-handwriting")
async def search_by_handwriting(file: UploadFile = File(...)):
    image = Image.open(file.file).convert("RGB")
    text = handwriting_engine.extract_text(image)
    return chatbot.handle(text=text, force_search=True)
