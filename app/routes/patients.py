from fastapi import APIRouter, HTTPException, Depends
from app.models.patient import PatientCreate, PatientResponse
from app.services.supabase_service import SupabaseService
from app.middleware.auth import verify_api_key
from uuid import UUID
import logging

router = APIRouter(prefix="/patients", tags=["patients"])
logger = logging.getLogger(__name__)

supabase_service = SupabaseService()

@router.post("/", response_model=PatientResponse)
async def create_patient(
    patient: PatientCreate,
    api_key: str = Depends(verify_api_key)
):
    """Cria um novo paciente"""
    try:
        patient_data = {
            "name": patient.name
        }
        result = supabase_service.create_patient(patient_data)
        if not result:
            raise HTTPException(status_code=500, detail="Erro ao criar paciente")
        return PatientResponse(**result)
    except Exception as e:
        logger.error(f"Erro ao criar paciente: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(
    patient_id: UUID,
    api_key: str = Depends(verify_api_key)
):
    """Busca um paciente por ID"""
    result = supabase_service.get_patient(str(patient_id))
    if not result:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return PatientResponse(**result)

@router.get("/", response_model=list[PatientResponse])
async def list_patients(api_key: str = Depends(verify_api_key)):
    """Lista todos os pacientes"""
    patients = supabase_service.list_patients()
    return [PatientResponse(**p) for p in patients]

