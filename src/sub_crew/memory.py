"""
Sistema de memória com Redis para gerenciar contexto de conversas do chatbot.
Versão alternativa ao memory.py para ambientes de produção com alta concorrência.
"""
import json
import redis
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

# Definir as classes de dados
@dataclass
class ChatMessage:
    content: str
    sender: str  # "user" ou "assistant"
    timestamp: datetime
    
    def to_dict(self):
        return {
            "content": self.content,
            "sender": self.sender,
            "timestamp": self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            content=data["content"],
            sender=data["sender"],
            timestamp=datetime.fromisoformat(data["timestamp"])
        )

@dataclass
class SessionInfo:
    session_id: str
    created_at: datetime
    last_activity: datetime
    message_count: int
    
    def to_dict(self):
        return {
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "message_count": self.message_count
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            session_id=data["session_id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            last_activity=datetime.fromisoformat(data["last_activity"]),
            message_count=data["message_count"]
        )

class RedisConversationMemory:
    """
    Sistema de memória usando Redis para gerenciar conversas e contexto do chatbot.
    Ideal para ambientes de produção com alta concorrência.
    """
    
    def __init__(self, 
                 redis_url: str = "redis://localhost:6379",
                 db: int = 0,
                 key_prefix: str = "sindico_pro:"):
        """
        Inicializar sistema de memória Redis.
        
        Args:
            redis_url: URL de conexão do Redis
            db: Número do banco de dados Redis
            key_prefix: Prefixo para as chaves Redis
        """
        self.redis_url = redis_url
        self.db = db
        self.key_prefix = key_prefix
        
        # Conectar ao Redis (obrigatório)
        try:
            self.redis_client = redis.from_url(redis_url, db=db, decode_responses=True)
            # Testar conexão
            self.redis_client.ping()
            print("✅ Conectado ao Redis com sucesso")
        except Exception as e:
            print(f"❌ ERRO: Não foi possível conectar ao Redis: {e}")
            print("   Certifique-se de que o Redis está rodando!")
            raise RuntimeError(f"Redis não disponível: {e}")
    
    def _get_key(self, key_type: str, identifier: str, user_id: Optional[str] = None) -> str:
        """Gerar chave Redis com prefixo e user_id."""
        if user_id:
            return f"{self.key_prefix}{key_type}:{user_id}:{identifier}"
        return f"{self.key_prefix}{key_type}:{identifier}"
    
    def add_message(self, session_id: str, message: ChatMessage, user_id: Optional[str] = None):
        """
        Adicionar mensagem a uma conversa.
        """
        
        try:
            # Adicionar mensagem à lista
            message_key = self._get_key("messages", session_id, user_id)
            self.redis_client.lpush(message_key, json.dumps(message.to_dict()))
            
            # Atualizar contador de mensagens
            count_key = self._get_key("count", session_id, user_id)
            self.redis_client.incr(count_key)
            
            # Atualizar última atividade
            activity_key = self._get_key("activity", session_id, user_id)
            self.redis_client.set(activity_key, datetime.now().isoformat())
            
            # Definir TTL (expira em 30 dias)
            ttl = 30 * 24 * 60 * 60  # 30 dias em segundos
            self.redis_client.expire(message_key, ttl)
            self.redis_client.expire(count_key, ttl)
            self.redis_client.expire(activity_key, ttl)
            
        except Exception as e:
            print(f"Erro ao adicionar mensagem no Redis: {e}")
            raise
    
    def get_conversation(self, session_id: str, user_id: Optional[str] = None) -> Optional[List[ChatMessage]]:
        """
        Obter histórico de uma conversa.
        """
        try:
            message_key = self._get_key("messages", session_id, user_id)
            messages_data = self.redis_client.lrange(message_key, 0, -1)
            
            if not messages_data:
                return []
            
            # Converter de JSON para ChatMessage (ordem reversa para cronológica)
            messages = []
            for msg_data in reversed(messages_data):
                try:
                    msg_dict = json.loads(msg_data)
                    messages.append(ChatMessage.from_dict(msg_dict))
                except Exception as e:
                    print(f"Erro ao converter mensagem: {e}")
                    continue
            
            return messages
            
        except Exception as e:
            print(f"Erro ao obter conversa do Redis: {e}")
            return []
    
    def get_conversation_context(self, session_id: str, max_messages: int = 10, user_id: Optional[str] = None) -> str:
        """
        Obter contexto da conversa formatado para o crew.
        """
        conversation = self.get_conversation(session_id, user_id)
        if not conversation:
            return ""
        
        # Pegar últimas mensagens
        recent_messages = conversation[-max_messages:]
        
        context_parts = []
        for msg in recent_messages:
            role = "Usuário" if msg.sender == "user" else "Assistente"
            context_parts.append(f"{role}: {msg.content}")
        
        return "\n".join(context_parts)
    
    def clear_conversation(self, session_id: str, user_id: Optional[str] = None):
        """
        Limpar histórico de uma conversa.
        """
        try:
            # Remover todas as chaves relacionadas à sessão
            message_key = self._get_key("messages", session_id, user_id)
            count_key = self._get_key("count", session_id, user_id)
            activity_key = self._get_key("activity", session_id, user_id)
            
            self.redis_client.delete(message_key, count_key, activity_key)
            
        except Exception as e:
            print(f"Erro ao limpar conversa no Redis: {e}")
            raise
    
    def list_sessions(self, user_id: Optional[str] = None) -> List[SessionInfo]:
        """
        Listar todas as sessões ativas.
        """
        try:
            # Buscar todas as chaves de atividade
            if user_id:
                activity_pattern = self._get_key("activity", f"{user_id}:*")
            else:
                activity_pattern = self._get_key("activity", "*")
            activity_keys = self.redis_client.keys(activity_pattern)
            
            sessions = []
            for activity_key in activity_keys:
                # Extrair session_id da chave
                key_parts = activity_key.split(":")
                if user_id:
                    session_id = key_parts[-1]  # Última parte é o session_id
                else:
                    session_id = key_parts[-1]  # Última parte é o session_id
                
                # Obter informações da sessão
                count_key = self._get_key("count", session_id, user_id)
                message_count = int(self.redis_client.get(count_key) or 0)
                last_activity = datetime.fromisoformat(
                    self.redis_client.get(activity_key) or datetime.now().isoformat()
                )
                
                # Criar SessionInfo (usar last_activity como created_at para simplicidade)
                session_info = SessionInfo(
                    session_id=session_id,
                    created_at=last_activity,  # Aproximação
                    message_count=message_count,
                    last_activity=last_activity
                )
                sessions.append(session_info)
            
            return sessions
            
        except Exception as e:
            print(f"Erro ao listar sessões do Redis: {e}")
            return []
    
    def get_session_info(self, session_id: str, user_id: Optional[str] = None) -> Optional[SessionInfo]:
        """
        Obter informações de uma sessão específica.
        """
        try:
            count_key = self._get_key("count", session_id, user_id)
            activity_key = self._get_key("activity", session_id, user_id)
            
            message_count = int(self.redis_client.get(count_key) or 0)
            last_activity_str = self.redis_client.get(activity_key)
            
            if not last_activity_str:
                return None
            
            last_activity = datetime.fromisoformat(last_activity_str)
            
            return SessionInfo(
                session_id=session_id,
                created_at=last_activity,  # Aproximação
                message_count=message_count,
                last_activity=last_activity
            )
            
        except Exception as e:
            print(f"Erro ao obter info da sessão do Redis: {e}")
            return None
    
    def cleanup_old_sessions(self, days: int = 30, user_id: Optional[str] = None):
        """
        Limpar sessões antigas (mais de X dias sem atividade).
        """
        try:
            cutoff_timestamp = datetime.now().timestamp() - (days * 24 * 60 * 60)
            
            # Buscar todas as chaves de atividade
            if user_id:
                activity_pattern = self._get_key("activity", f"{user_id}:*")
            else:
                activity_pattern = self._get_key("activity", "*")
            activity_keys = self.redis_client.keys(activity_pattern)
            
            sessions_to_remove = []
            for activity_key in activity_keys:
                last_activity_str = self.redis_client.get(activity_key)
                if last_activity_str:
                    last_activity = datetime.fromisoformat(last_activity_str)
                    if last_activity.timestamp() < cutoff_timestamp:
                        session_id = activity_key.split(":")[-1]
                        sessions_to_remove.append(session_id)
            
            # Remover sessões antigas
            for session_id in sessions_to_remove:
                self.clear_conversation(session_id, user_id)
                
        except Exception as e:
            print(f"Erro ao limpar sessões antigas do Redis: {e}")
            raise
    
    def get_stats(self, user_id: Optional[str] = None) -> Dict:
        """
        Obter estatísticas do sistema de memória.
        """
        try:
            # Contar sessões ativas
            if user_id:
                activity_pattern = self._get_key("activity", f"{user_id}:*")
            else:
                activity_pattern = self._get_key("activity", "*")
            activity_keys = self.redis_client.keys(activity_pattern)
            total_sessions = len(activity_keys)
            
            # Contar total de mensagens
            total_messages = 0
            for activity_key in activity_keys:
                session_id = activity_key.split(":")[-1]
                count_key = self._get_key("count", session_id, user_id)
                message_count = int(self.redis_client.get(count_key) or 0)
                total_messages += message_count
            
            return {
                "total_sessions": total_sessions,
                "total_messages": total_messages,
                "storage_type": "redis",
                "redis_url": self.redis_url,
                "user_id": user_id,
                "last_cleanup": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Erro ao obter estatísticas do Redis: {e}")
            return {"error": str(e)}
    
    def health_check(self) -> Dict:
        """
        Verificar saúde do sistema Redis.
        """
        try:
            # Testar conexão
            self.redis_client.ping()
            
            # Obter info do Redis
            info = self.redis_client.info()
            
            return {
                "status": "healthy",
                "redis_available": True,
                "redis_version": info.get("redis_version"),
                "used_memory": info.get("used_memory_human"),
                "connected_clients": info.get("connected_clients")
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "redis_available": False
            }
