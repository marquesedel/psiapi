from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends
from app.models.session import SessionCreate, SessionResponse, SessionUpdate
from app.services.audio_service import AudioService
from app.services.openai_service import OpenAIService
from app.services.supabase_service import SupabaseService
from app.middleware.auth import verify_api_key
from uuid import UUID
import logging

router = APIRouter(prefix="/sessions", tags=["sessions"])
logger = logging.getLogger(__name__)

audio_service = AudioService()
openai_service = OpenAIService()
supabase_service = SupabaseService()

@router.post("/", response_model=SessionResponse)
async def create_session(
    psychologist_id: UUID = Form(...),
    patient_id: UUID = Form(...),
    audio: UploadFile = File(...),
    api_key: str = Depends(verify_api_key)
):
    """Cria uma nova sessão e processa o áudio completamente antes de retornar"""
    try:
        # Lê arquivo de áudio
        audio_content = await audio.read()
        
        # Upload para Supabase Storage
        try:
            audio_url = supabase_service.upload_audio(audio_content, audio.filename)
        except Exception as upload_error:
            error_msg = str(upload_error)
            if "Bucket" in error_msg and "not found" in error_msg.lower():
                logger.error(f"Bucket não encontrado: {error_msg}")
                raise HTTPException(
                    status_code=400,
                    detail=error_msg
                )
            raise
        
        # Cria sessão no banco
        session_data = {
            "psychologist_id": str(psychologist_id),
            "patient_id": str(patient_id),
            "audio_url": audio_url
        }
        session = supabase_service.create_session(session_data)
        
        if not session:
            raise HTTPException(status_code=500, detail="Erro ao criar sessão no banco de dados")
        
        session_id = session["id"]
        logger.info(f"Iniciando processamento completo da sessão {session_id}")
        
        # Processa tudo síncronamente antes de retornar
        try:
            # 1. Transcreve áudio
            logger.info(f"Transcrevendo áudio da sessão {session_id}")
            transcription = audio_service.transcribe_audio(audio_content, audio.filename)
            
            # 2. Atualiza sessão com transcrição
            logger.info(f"Salvando transcrição da sessão {session_id}")
            supabase_service.update_session(session_id, {"transcription": transcription})
            
            # 3. Processa com OpenAI (resumos, demandas, contexto)
            logger.info(f"Processando com OpenAI a sessão {session_id}")
            results = openai_service.process_session(transcription)
            
            # 4. Atualiza sessão com todos os resultados (incluindo análise da IA)
            logger.info(f"Salvando resultados do processamento da sessão {session_id}")
            updated_session = supabase_service.update_session(session_id, {
                "full_summary": results["full_summary"],
                "anonymous_summary": results["anonymous_summary"],
                "patient_demand": results["patient_demand"],
                "context": results["context"],
                "analise_da_ia": results["analise_da_ia"]
            })
            
            logger.info(f"Sessão {session_id} processada com sucesso - todos os dados salvos")
            
            # Retorna a sessão atualizada com todos os dados processados
            return SessionResponse(**updated_session)
            
        except Exception as process_error:
            logger.error(f"Erro ao processar sessão {session_id}: {str(process_error)}")
            # Atualiza a sessão com status de erro (se houver campo para isso)
            # ou mantém a sessão criada mesmo com erro no processamento
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao processar sessão: {str(process_error)}"
            )
            
    except HTTPException:
        # Re-lança HTTPException sem modificação
        raise
    except Exception as e:
        logger.error(f"Erro ao criar sessão: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: UUID,
    api_key: str = Depends(verify_api_key)
):
    """Busca uma sessão por ID"""
    session = supabase_service.get_session(str(session_id))
    if not session:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    return SessionResponse(**session)

@router.get("/", response_model=list[SessionResponse])
async def list_sessions(
    psychologist_id: UUID = None,
    patient_id: UUID = None,
    api_key: str = Depends(verify_api_key)
):
    """Lista sessões com filtros opcionais"""
    sessions = supabase_service.list_sessions(
        psychologist_id=str(psychologist_id) if psychologist_id else None,
        patient_id=str(patient_id) if patient_id else None
    )
    return [SessionResponse(**session) for session in sessions]

