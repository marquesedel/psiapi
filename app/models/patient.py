from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class PatientCreate(BaseModel):
    name: str

class PatientResponse(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

