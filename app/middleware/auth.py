from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Define o header onde a API_KEY deve ser enviada
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Verifica se a API_KEY fornecida é válida.
    A API_KEY deve ser enviada no header 'X-API-Key'
    """
    if not api_key:
        logger.warning("Tentativa de acesso sem API_KEY")
        raise HTTPException(
            status_code=401,
            detail="API_KEY é obrigatória. Envie no header 'X-API-Key'"
        )
    
    if api_key != settings.api_key:
        logger.warning(f"Tentativa de acesso com API_KEY inválida")
        raise HTTPException(
            status_code=403,
            detail="API_KEY inválida"
        )
    
    return api_key
