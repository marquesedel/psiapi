from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class SessionCreate(BaseModel):
    psychologist_id: UUID
    patient_id: UUID
    audio_url: Optional[str] = None

class SessionResponse(BaseModel):
    id: UUID
    psychologist_id: UUID
    patient_id: UUID
    audio_url: Optional[str]
    transcription: Optional[str]
    full_summary: Optional[str]
    anonymous_summary: Optional[str]
    patient_demand: Optional[str]
    context: Optional[str]
    analise_da_ia: Optional[str] = None
    questions: Optional[List[str]] = None
    answers: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class SessionUpdate(BaseModel):
    transcription: Optional[str] = None
    full_summary: Optional[str] = None
    anonymous_summary: Optional[str] = None
    patient_demand: Optional[str] = None
    context: Optional[str] = None
    analise_da_ia: Optional[str] = None
    questions: Optional[List[str]] = None
    answers: Optional[List[str]] = None

