# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import chat
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Cria a aplicação FastAPI
app = FastAPI(
    title="Sub API",
    description="API do Subsíndico IA - Assistente de Gestão Condominial",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuração CORS para permitir requisições do Next.js
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(chat.router)

@app.get("/")
async def root():
    """
    Endpoint raiz da API
    
    Returns:
        Informações básicas sobre a API
    """
    return {
        "message": "Sub API - Subsíndico IA",
        "description": "Assistente de Gestão Condominial",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/chat/health"
    }

@app.get("/api")
async def api_info():
    """
    Informações sobre a API
    
    Returns:
        Detalhes sobre os endpoints disponíveis
    """
    return {
        "api_name": "Sub API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "health": "/api/chat/health",
            "docs": "/docs",
            "redoc": "/redoc"
        },
        "description": "API do Subsíndico IA para assistência em gestão condominial"
    }
