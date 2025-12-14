from fastapi import APIRouter, HTTPException, Depends
from app.models.psychologist import PsychologistCreate, PsychologistResponse
from app.services.supabase_service import SupabaseService
from app.middleware.auth import verify_api_key
from uuid import UUID
import logging

router = APIRouter(prefix="/psychologists", tags=["psychologists"])
logger = logging.getLogger(__name__)

supabase_service = SupabaseService()

@router.post("/", response_model=PsychologistResponse)
async def create_psychologist(
    psychologist: PsychologistCreate,
    api_key: str = Depends(verify_api_key)
):
    """Cria um novo psicólogo"""
    try:
        psychologist_data = {
            "name": psychologist.name,
            "email": psychologist.email
        }
        result = supabase_service.create_psychologist(psychologist_data)
        if not result:
            raise HTTPException(status_code=500, detail="Erro ao criar psicólogo")
        return PsychologistResponse(**result)
    except Exception as e:
        logger.error(f"Erro ao criar psicólogo: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{psychologist_id}", response_model=PsychologistResponse)
async def get_psychologist(
    psychologist_id: UUID,
    api_key: str = Depends(verify_api_key)
):
    """Busca um psicólogo por ID"""
    result = supabase_service.get_psychologist(str(psychologist_id))
    if not result:
        raise HTTPException(status_code=404, detail="Psicólogo não encontrado")
    return PsychologistResponse(**result)

@router.get("/", response_model=list[PsychologistResponse])
async def list_psychologists(api_key: str = Depends(verify_api_key)):
    """Lista todos os psicólogos"""
    psychologists = supabase_service.list_psychologists()
    return [PsychologistResponse(**p) for p in psychologists]

