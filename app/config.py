# app/config.py

import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class Settings:
    # Configurações do Banco de Dados
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://seu_usuario:sua_senha@localhost/seu_banco")
    
    # Configurações de Segurança
    SECRET_KEY: str = os.getenv("SECRET_KEY", "CheckInSuperApp")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Configurações do Servidor
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

settings = Settings() 