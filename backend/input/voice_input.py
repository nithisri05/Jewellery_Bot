import whisper

class VoiceInputEngine:
    def __init__(self):
        # base is accurate enough + fast
        self.model = whisper.load_model("base")

    def speech_to_text(self, audio_path: str) -> str:
        result = self.model.transcribe(audio_path)
        return result["text"].strip()
