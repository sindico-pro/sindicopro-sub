from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ChatMessage(BaseModel):
    """Schema para mensagem de entrada do chat"""
    message: str
    user_id: str
    condo_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    """Schema para resposta do chat"""
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None

class ChatHistory(BaseModel):
    """Schema para histórico de conversas"""
    message_id: str
    user_message: str
    sub_response: str
    timestamp: datetime

class HealthResponse(BaseModel):
    """Schema para resposta de health check"""
    status: str
    timestamp: str
    version: str
