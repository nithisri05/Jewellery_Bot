import whisper
import numpy as np

class VoiceInputEngine:
    def __init__(self):
        self.model = whisper.load_model("base")

    def speech_to_text(self, audio_path: str) -> str:
        """
        audio_path: path to audio file (wav/mp3/m4a)
        """
        result = self.model.transcribe(audio_path)
        text = result.get("text", "").strip()
        return text
