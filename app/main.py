from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import sessions, psychologists, patients
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PSI AI API",
    description="API para processamento de sessões de psicoterapia com IA",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure adequadamente para produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions.router)
app.include_router(psychologists.router)
app.include_router(patients.router)

@app.get("/")
async def root():
    return {
        "message": "PSI AI API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

