from openai import OpenAI
from app.config import settings
from typing import Optional
import io

class AudioService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
    
    def transcribe_audio(self, audio_file: bytes, filename: str) -> str:
        """Transcreve áudio usando Whisper API"""
        audio_io = io.BytesIO(audio_file)
        audio_io.name = filename
        
        transcript = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_io,
            language="pt"  # Português
        )
        
        return transcript.text

