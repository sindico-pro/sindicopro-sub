"""
Sistema de memória Redis para o chatbot.
"""
import os
from .memory import RedisConversationMemory

def create_memory() -> RedisConversationMemory:
    """
    Criar instância de memória Redis.
    
    Variáveis de ambiente:
    - REDIS_URL: URL do Redis (padrão: "redis://localhost:6379")
    - REDIS_DB: Número do banco Redis (padrão: 0)
    - REDIS_KEY_PREFIX: Prefixo das chaves (padrão: "sindico_pro:")
    """
    
    print("🔴 Configurando memória Redis...")
    
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    redis_db = int(os.getenv("REDIS_DB", "0"))
    key_prefix = os.getenv("REDIS_KEY_PREFIX", "sindico_pro:")
    
    return RedisConversationMemory(
        redis_url=redis_url,
        db=redis_db,
        key_prefix=key_prefix
    )

# Instância global configurada automaticamente
memory = create_memory()
