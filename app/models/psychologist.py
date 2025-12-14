from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

class PsychologistCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None

class PsychologistResponse(BaseModel):
    id: UUID
    name: str
    email: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

