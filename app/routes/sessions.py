from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends, Body
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
        
        # Não salva o áudio no bucket - apenas processa diretamente
        # Cria sessão no banco sem audio_url
        session_data = {
            "psychologist_id": str(psychologist_id),
            "patient_id": str(patient_id),
            "audio_url": None
        }
        session = supabase_service.create_session(session_data)
        
        if not session:
            raise HTTPException(status_code=500, detail="Erro ao criar sessão no banco de dados")
        
        session_id = session["id"]
        logger.info(f"Iniciando processamento completo da sessão {session_id}")
        
        # Processa tudo síncronamente antes de retornar
        try:
            # Busca nomes do paciente e psicólogo para anonimização
            patient = supabase_service.get_patient(str(patient_id))
            psychologist = supabase_service.get_psychologist(str(psychologist_id))
            
            if not patient:
                raise HTTPException(status_code=404, detail="Paciente não encontrado")
            if not psychologist:
                raise HTTPException(status_code=404, detail="Psicólogo não encontrado")
            
            patient_name = patient.get("name", "")
            psychologist_name = psychologist.get("name", "")
            
            # 1. Transcreve áudio
            logger.info(f"Transcrevendo áudio da sessão {session_id}")
            raw_transcription = audio_service.transcribe_audio(audio_content, audio.filename)
            
            # 2. Anonimiza transcrição substituindo nomes por letras
            logger.info(f"Anonimizando transcrição da sessão {session_id}")
            transcription = openai_service.anonymize_names_in_transcription(
                raw_transcription, 
                patient_name, 
                psychologist_name
            )
            
            # 3. Atualiza sessão com transcrição anonimizada
            logger.info(f"Salvando transcrição da sessão {session_id}")
            supabase_service.update_session(session_id, {"transcription": transcription})
            
            # 4. Gera perguntas sobre a sessão
            logger.info(f"Gerando perguntas sobre a sessão {session_id}")
            questions = openai_service.generate_session_questions(
                transcription,
                patient_name,
                psychologist_name
            )
            
            # 5. Processa com OpenAI (resumos, demandas, contexto)
            logger.info(f"Processando com OpenAI a sessão {session_id}")
            results = openai_service.process_session(transcription)
            
            # 6. Atualiza sessão com todos os resultados (incluindo análise da IA e perguntas)
            logger.info(f"Salvando resultados do processamento da sessão {session_id}")
            updated_session = supabase_service.update_session(session_id, {
                "full_summary": results["full_summary"],
                "anonymous_summary": results["anonymous_summary"],
                "patient_demand": results["patient_demand"],
                "context": results["context"],
                "analise_da_ia": results["analise_da_ia"],
                "questions": questions,
                "answers": None  # Inicializa como None, será preenchido depois
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

@router.patch("/{session_id}/answers", response_model=SessionResponse)
async def update_session_answers(
    session_id: UUID,
    answers: list[str] = Body(...),
    api_key: str = Depends(verify_api_key)
):
    """Atualiza as respostas às perguntas da sessão"""
    # Verifica se a sessão existe
    session = supabase_service.get_session(str(session_id))
    if not session:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    
    # Verifica se há perguntas
    questions = session.get("questions")
    if not questions:
        raise HTTPException(status_code=400, detail="Esta sessão não possui perguntas")
    
    # Valida que o número de respostas corresponde ao número de perguntas
    if len(answers) != len(questions):
        raise HTTPException(
            status_code=400, 
            detail=f"O número de respostas ({len(answers)}) deve corresponder ao número de perguntas ({len(questions)})"
        )
    
    # Atualiza as respostas
    updated_session = supabase_service.update_session(str(session_id), {"answers": answers})
    
    if not updated_session:
        raise HTTPException(status_code=500, detail="Erro ao atualizar respostas")
    
    return SessionResponse(**updated_session)

