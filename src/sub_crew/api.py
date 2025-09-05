#!/usr/bin/env python
"""
API FastAPI para o chatbot especializado em questões condominiais brasileiras.
"""
import uuid
from datetime import datetime
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import uvicorn
import asyncio
import json

from sub_crew.crew import SubCrew
from sub_crew.memory import ChatMessage
from sub_crew.memory_factory import memory

# Configuração da API
app = FastAPI(
    title="Síndico PRO Chatbot API",
    description="API para assistente virtual especializado em questões condominiais brasileiras",
    version="1.0.0"
)

# Configuração CORS para integração com Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://localhost:3000"],  # URLs do Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instância global do sistema de memória (configurada automaticamente)

# Modelos Pydantic
class ChatMessageRequest(BaseModel):
    content: str
    sender: str  # "user" ou "assistant"
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    message: str  # Mudando de 'response' para 'message' para compatibilidade com frontend
    session_id: str
    timestamp: datetime
    message_id: str
    user_id: Optional[str] = None

class SessionInfo(BaseModel):
    session_id: str
    created_at: datetime
    message_count: int
    last_activity: datetime

class ConversationHistory(BaseModel):
    session_id: str
    messages: List[ChatMessageRequest]

# Dependência para obter o crew
def get_crew():
    return SubCrew()

# Endpoints da API

@app.get("/")
async def root():
    """Endpoint de saúde da API"""
    return {
        "message": "Síndico PRO Chatbot API está funcionando!",
        "version": "1.0.0",
        "timestamp": datetime.now()
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    crew: SubCrew = Depends(get_crew)
):
    """
    Endpoint principal para conversar com o chatbot.
    Mantém contexto da conversa através do session_id e user_id.
    """
    try:
        # Gerar session_id se não fornecido
        session_id = request.session_id or str(uuid.uuid4())
        user_id = request.user_id
        
        # Adicionar mensagem do usuário ao histórico
        user_message = ChatMessage(
            content=request.message,
            sender="user",
            timestamp=datetime.now()
        )
        memory.add_message(session_id, user_message, user_id)
        
        # Obter histórico da conversa
        conversation_history = memory.get_conversation(session_id, user_id)
        
        # Preparar contexto para o crew
        context = _prepare_context_for_crew(conversation_history, request.message)
        
        # Executar crew com contexto
        crew_instance = crew.crew()
        result = crew_instance.kickoff(inputs=context)
        
        # Extrair resposta do resultado
        response_text = _extract_response_from_result(result)
        
        # Adicionar resposta do assistente ao histórico
        assistant_message = ChatMessage(
            content=response_text,
            sender="assistant",
            timestamp=datetime.now()
        )
        memory.add_message(session_id, assistant_message, user_id)
        
        # Gerar ID único para a mensagem
        message_id = str(uuid.uuid4())
        
        return ChatResponse(
            message=response_text,  # Mudando de 'response' para 'message'
            session_id=session_id,
            timestamp=datetime.now(),
            message_id=message_id,
            user_id=user_id
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar mensagem: {str(e)}"
        ) from e

@app.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    crew: SubCrew = Depends(get_crew)
):
    """
    Endpoint para streaming de respostas do chatbot.
    Retorna resposta em tempo real conforme é gerada.
    """
    try:
        # Gerar session_id se não fornecido
        session_id = request.session_id or str(uuid.uuid4())
        user_id = request.user_id
        
        # Adicionar mensagem do usuário ao histórico
        user_message = ChatMessage(
            content=request.message,
            sender="user",
            timestamp=datetime.now()
        )
        memory.add_message(session_id, user_message, user_id)
        
        # Obter histórico da conversa
        conversation_history = memory.get_conversation(session_id, user_id)
        
        # Preparar contexto para o crew
        context = _prepare_context_for_crew(conversation_history, request.message)
        
        # Função para gerar resposta em streaming
        async def generate_stream():
            try:
                # Executar crew com contexto
                crew_instance = crew.crew()
                result = crew_instance.kickoff(inputs=context)
                
                # Extrair resposta do resultado
                response_text = _extract_response_from_result(result)
                
                # Simular streaming palavra por palavra
                words = response_text.split()
                full_response = ""
                
                for i, word in enumerate(words):
                    full_response += word
                    if i < len(words) - 1:
                        full_response += " "
                    
                    # Enviar chunk no formato do AI SDK
                    chunk = {
                        "id": str(uuid.uuid4()),
                        "object": "text_completion.chunk",
                        "created": int(datetime.now().timestamp()),
                        "model": "sindico-pro-crew",
                        "choices": [
                            {
                                "index": 0,
                                "delta": {"content": word + (" " if i < len(words) - 1 else "")},
                                "finish_reason": None
                            }
                        ]
                    }
                    
                    yield f"data: {json.dumps(chunk)}\n\n"
                    await asyncio.sleep(0.05)  # Pequeno delay para simular streaming
                
                # Enviar chunk final
                final_chunk = {
                    "id": str(uuid.uuid4()),
                    "object": "text_completion.chunk",
                    "created": int(datetime.now().timestamp()),
                    "model": "sindico-pro-crew",
                    "choices": [
                        {
                            "index": 0,
                            "delta": {},
                            "finish_reason": "stop"
                        }
                    ]
                }
                yield f"data: {json.dumps(final_chunk)}\n\n"
                yield "data: [DONE]\n\n"
                
                # Adicionar resposta completa ao histórico
                assistant_message = ChatMessage(
                    content=response_text,
                    sender="assistant",
                    timestamp=datetime.now()
                )
                memory.add_message(session_id, assistant_message, user_id)
                
            except Exception as e:
                error_chunk = {
                    "error": {
                        "message": f"Erro ao processar mensagem: {str(e)}",
                        "type": "server_error"
                    }
                }
                yield f"data: {json.dumps(error_chunk)}\n\n"
        
        return StreamingResponse(
            generate_stream(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/plain; charset=utf-8"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar mensagem: {str(e)}"
        ) from e

@app.get("/sessions/{session_id}/history", response_model=ConversationHistory)
async def get_conversation_history(session_id: str, user_id: Optional[str] = None):
    """Obter histórico de uma conversa específica"""
    try:
        conversation = memory.get_conversation(session_id, user_id)
        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Sessão não encontrada"
            )
        
        # Converter ChatMessage para ChatMessageRequest
        messages_request = []
        for msg in conversation:
            messages_request.append(ChatMessageRequest(
                content=msg.content,
                sender=msg.sender,
                timestamp=msg.timestamp
            ))
        
        return ConversationHistory(
            session_id=session_id,
            messages=messages_request
        )
    except HTTPException:
        # Re-raise HTTPException (404) sem modificar
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter histórico: {str(e)}"
        ) from e

@app.delete("/sessions/{session_id}")
async def clear_conversation(session_id: str, user_id: Optional[str] = None):
    """Limpar histórico de uma conversa específica"""
    try:
        memory.clear_conversation(session_id, user_id)
        return {"message": "Histórico da conversa limpo com sucesso"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao limpar histórico: {str(e)}"
        ) from e

@app.get("/sessions", response_model=List[SessionInfo])
async def list_sessions(user_id: Optional[str] = None):
    """Listar todas as sessões ativas"""
    try:
        sessions = memory.list_sessions(user_id)
        return sessions
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar sessões: {str(e)}"
        ) from e

@app.get("/health")
async def health_check(user_id: Optional[str] = None):
    """Verificação de saúde da API"""
    stats = memory.get_stats(user_id)
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "memory_sessions": stats.get("total_sessions", 0),
        "memory_type": stats.get("storage_type", "redis"),
        "user_id": user_id
    }

@app.get("/memory/status")
async def memory_status(user_id: Optional[str] = None):
    """Status detalhado do sistema de memória"""
    stats = memory.get_stats(user_id)
    
    # Se for Redis, obter informações adicionais
    if hasattr(memory, 'health_check'):
        health = memory.health_check()
        stats.update(health)
    
    return stats

# Funções auxiliares

def _prepare_context_for_crew(conversation_history: List[ChatMessage], current_message: str) -> Dict:
    """
    Preparar contexto da conversa para o crew.
    Inclui histórico e mensagem atual.
    """
    # Construir contexto da conversa
    context_messages = []
    for msg in conversation_history[-10:]:  # Últimas 10 mensagens para contexto
        role = "Usuário" if msg.sender == "user" else "Assistente"
        context_messages.append(f"{role}: {msg.content}")
    
    # Adicionar mensagem atual
    context_messages.append(f"Usuário: {current_message}")
    
    # Construir contexto completo
    conversation_context = "\n".join(context_messages)
    
    return {
        "question": current_message,
        "conversation_history": conversation_context,
        "current_year": str(datetime.now().year),
        "context": f"Histórico da conversa:\n{conversation_context}\n\nPergunta atual: {current_message}"
    }

def _extract_response_from_result(result) -> str:
    """
    Extrair resposta do resultado do crew.
    """
    if hasattr(result, 'raw'):
        return str(result.raw)
    elif hasattr(result, 'output'):
        return str(result.output)
    else:
        return str(result)

# Executar servidor se chamado diretamente
if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
