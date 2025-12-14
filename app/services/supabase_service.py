from supabase import create_client, Client
from app.config import settings
from typing import Optional, Dict, Any
import uuid
import re
import os
import unicodedata

class SupabaseService:
    def __init__(self):
        self.client: Client = create_client(settings.supabase_url, settings.supabase_key)
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitiza o nome do arquivo para seguir as regras do AWS S3/Supabase Storage
        
        Remove caracteres inválidos, normaliza Unicode e substitui espaços por underscores.
        Mantém apenas caracteres alfanuméricos, hífens, underscores e pontos.
        """
        # Separa nome e extensão
        name, ext = os.path.splitext(filename)
        
        # Normaliza caracteres Unicode (NFD = decomposed form)
        # Isso separa acentos dos caracteres base
        name = unicodedata.normalize('NFD', name)
        
        # Remove caracteres de combinação (acentos)
        name = ''.join(char for char in name if unicodedata.category(char) != 'Mn')
        
        # Remove caracteres inválidos (mantém apenas alfanuméricos, hífen, underscore)
        # Substitui espaços e outros caracteres por underscore
        name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
        
        # Remove múltiplos underscores consecutivos
        name = re.sub(r'_+', '_', name)
        
        # Remove underscores no início e fim
        name = name.strip('_')
        
        # Se o nome ficou vazio, usa um nome padrão
        if not name:
            name = 'audio_file'
        
        # Limita o tamanho do nome (máximo 200 caracteres antes da extensão)
        if len(name) > 200:
            name = name[:200]
        
        # Retorna nome sanitizado com extensão
        return f"{name}{ext}" if ext else name
    
    def _ensure_bucket_exists(self):
        """Verifica se o bucket existe e tenta criá-lo se não existir"""
        try:
            # Tenta criar o bucket (se já existir, o Supabase retornará erro que podemos ignorar)
            try:
                self.client.storage.create_bucket(
                    settings.supabase_storage_bucket,
                    options={"public": True}
                )
            except Exception as create_error:
                # Se o erro não for sobre bucket já existir, relança
                error_str = str(create_error).lower()
                if "already exists" not in error_str and "duplicate" not in error_str:
                    # Se for outro tipo de erro (como permissão), tenta continuar mesmo assim
                    # O upload vai falhar depois se realmente não existir
                    pass
        except Exception as e:
            # Se houver erro inesperado, apenas loga mas continua
            # O upload vai falhar depois se o bucket realmente não existir
            pass
    
    def upload_audio(self, file_content: bytes, filename: str) -> str:
        """Upload áudio para Supabase Storage e retorna URL"""
        # Tenta garantir que o bucket existe
        self._ensure_bucket_exists()
        
        # Sanitiza o nome do arquivo para evitar caracteres inválidos
        sanitized_filename = self._sanitize_filename(filename)
        
        # Cria um caminho único usando UUID + nome sanitizado
        file_path = f"{uuid.uuid4()}_{sanitized_filename}"
        
        try:
            self.client.storage.from_(settings.supabase_storage_bucket).upload(
                file_path,
                file_content,
                file_options={"content-type": "audio/mpeg"}
            )
            
            # Retorna URL pública
            response = self.client.storage.from_(settings.supabase_storage_bucket).get_public_url(file_path)
            return response
        except Exception as e:
            error_msg = str(e)
            if "InvalidKey" in error_msg or "Invalid key" in error_msg:
                raise Exception(
                    f"Nome de arquivo inválido após sanitização. "
                    f"Nome original: '{filename}', Nome sanitizado: '{sanitized_filename}'. "
                    f"Erro: {error_msg}"
                )
            if "Bucket not found" in error_msg or "not found" in error_msg.lower() or "bucket" in error_msg.lower():
                raise Exception(
                    f"Bucket '{settings.supabase_storage_bucket}' não encontrado no Supabase Storage. "
                    f"Por favor, crie o bucket manualmente:\n"
                    f"1. Acesse o dashboard do Supabase\n"
                    f"2. Vá em Storage > Buckets\n"
                    f"3. Clique em 'New bucket'\n"
                    f"4. Nome: '{settings.supabase_storage_bucket}'\n"
                    f"5. Marque como público (public) se necessário\n"
                    f"Erro original: {error_msg}"
                )
            raise
    
    def create_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria uma nova sessão no banco"""
        response = self.client.table("sessions").insert(session_data).execute()
        return response.data[0] if response.data else None
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Busca uma sessão por ID"""
        response = self.client.table("sessions").select("*").eq("id", session_id).execute()
        return response.data[0] if response.data else None
    
    def update_session(self, session_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza uma sessão"""
        response = self.client.table("sessions").update(updates).eq("id", session_id).execute()
        return response.data[0] if response.data else None
    
    def list_sessions(self, psychologist_id: Optional[str] = None, patient_id: Optional[str] = None) -> list[Dict[str, Any]]:
        """Lista sessões com filtros opcionais"""
        query = self.client.table("sessions").select("*")
        
        if psychologist_id:
            query = query.eq("psychologist_id", psychologist_id)
        if patient_id:
            query = query.eq("patient_id", patient_id)
        
        response = query.order("created_at", desc=True).execute()
        return response.data if response.data else []
    
    # Métodos para Psicólogos
    def create_psychologist(self, psychologist_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo psicólogo"""
        response = self.client.table("psychologists").insert(psychologist_data).execute()
        return response.data[0] if response.data else None
    
    def get_psychologist(self, psychologist_id: str) -> Optional[Dict[str, Any]]:
        """Busca um psicólogo por ID"""
        response = self.client.table("psychologists").select("*").eq("id", psychologist_id).execute()
        return response.data[0] if response.data else None
    
    def list_psychologists(self) -> list[Dict[str, Any]]:
        """Lista todos os psicólogos"""
        response = self.client.table("psychologists").select("*").order("created_at", desc=True).execute()
        return response.data if response.data else []
    
    # Métodos para Pacientes
    def create_patient(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo paciente"""
        response = self.client.table("patients").insert(patient_data).execute()
        return response.data[0] if response.data else None
    
    def get_patient(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """Busca um paciente por ID"""
        response = self.client.table("patients").select("*").eq("id", patient_id).execute()
        return response.data[0] if response.data else None
    
    def list_patients(self) -> list[Dict[str, Any]]:
        """Lista todos os pacientes"""
        response = self.client.table("patients").select("*").order("created_at", desc=True).execute()
        return response.data if response.data else []

