from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    openai_api_key: str
    supabase_url: str
    supabase_key: str
    supabase_storage_bucket: str = "audio-sessions"
    api_key: str  # API_KEY para autenticação da API
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

