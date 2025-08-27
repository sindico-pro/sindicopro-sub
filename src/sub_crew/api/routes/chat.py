# -*- coding: utf-8 -*-
from fastapi import APIRouter, HTTPException, Query
from ..models.chat import ChatMessage, ChatResponse, HealthResponse
from ..services.chat_service import ChatService
import uuid
from datetime import datetime
import os

# Obtém o provedor de IA das variáveis de ambiente ou usa Gemini como padrão
DEFAULT_AI_PROVIDER = os.getenv("DEFAULT_AI_PROVIDER", "gemini")

router = APIRouter(prefix="/api/chat", tags=["chat"])
chat_service = ChatService(DEFAULT_AI_PROVIDER)

@router.post("/message", response_model=ChatResponse)
async def send_message(message: ChatMessage):
    """
    Envia uma mensagem para o Sub e recebe uma resposta
    
    Args:
        message: Mensagem do usuário com contexto
        
    Returns:
        Resposta do Sub com ID da mensagem e timestamp
    """
    print(f"🤖 API Python: Mensagem recebida de {message.user_id}")
    print(f"📝 Conteúdo: {message.message}")
    print(f"🏢 Contexto: {message.context}")
    
    try:
        print("🚀 Processando com IA...")
        # Processa a mensagem
        response = await chat_service.get_response(
            message.message, 
            message.context
        )
        print(f"✅ Resposta gerada: {response[:100]}...")
        
        # Gera ID único para a mensagem
        message_id = str(uuid.uuid4())
        
        return ChatResponse(
            success=True,
            data={
                "response": response,
                "message_id": message_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    except Exception as e:
        print(f"❌ Erro na API Python: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Verifica se a API está funcionando
    
    Returns:
        Status da API com timestamp e versão
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0"
    )

@router.get("/")
async def chat_info():
    """
    Informações sobre o endpoint de chat
    
    Returns:
        Informações básicas sobre o chat
    """
    provider_info = chat_service.get_provider_info()
    
    return {
        "service": "Sub Chat API",
        "description": "API do Subsíndico IA - Assistente de Gestão Condominial",
        "ai_provider": provider_info["provider"],
        "available_providers": provider_info["available_providers"],
        "endpoints": {
            "POST /api/chat/message": "Enviar mensagem para o Sub",
            "GET /api/chat/health": "Verificar saúde da API",
            "GET /api/chat/providers": "Listar provedores de IA disponíveis"
        }
    }

@router.get("/providers")
async def list_providers():
    """
    Lista os provedores de IA disponíveis
    
    Returns:
        Lista de provedores disponíveis
    """
    provider_info = chat_service.get_provider_info()
    
    return {
        "current_provider": provider_info["provider"],
        "available_providers": provider_info["available_providers"],
        "description": "Provedores de IA suportados pelo Sub"
    }
