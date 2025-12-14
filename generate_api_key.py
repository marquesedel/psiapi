#!/usr/bin/env python3
"""
Script para gerar uma API_KEY segura para a PSI AI API
"""
import secrets
import string

def generate_api_key(length: int = 32) -> str:
    """
    Gera uma API_KEY segura usando caracteres alfanuméricos
    
    Args:
        length: Tamanho da chave (padrão: 32 caracteres)
    
    Returns:
        API_KEY gerada
    """
    # Caracteres permitidos: letras maiúsculas, minúsculas e números
    alphabet = string.ascii_letters + string.digits
    api_key = ''.join(secrets.choice(alphabet) for _ in range(length))
    return api_key

if __name__ == "__main__":
    # Gera uma API_KEY de 32 caracteres (pode ajustar o tamanho)
    api_key = generate_api_key(32)
    
    print("=" * 60)
    print("API_KEY gerada com sucesso!")
    print("=" * 60)
    print(f"\nAPI_KEY: {api_key}\n")
    print("=" * 60)
    print("\nAdicione esta chave ao seu arquivo .env:")
    print(f"API_KEY={api_key}\n")
    print("=" * 60)
