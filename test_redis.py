#!/usr/bin/env python
"""
Teste simples do sistema Redis.
"""
import os
import sys
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_redis_connection():
    """Testar conexão com Redis."""
    print("🔴 Testando conexão com Redis...")
    
    try:
        import redis
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        client = redis.from_url(redis_url, decode_responses=True)
        client.ping()
        print("✅ Redis conectado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao conectar com Redis: {e}")
        return False

def test_memory_system():
    """Testar sistema de memória."""
    print("\n🧠 Testando sistema de memória...")
    
    try:
        from sub_crew.memory_factory import memory
        from sub_crew.memory import ChatMessage
        from datetime import datetime
        
        # Teste básico
        session_id = "test_session"
        message = ChatMessage(
            content="Teste de mensagem",
            sender="user",
            timestamp=datetime.now()
        )
        
        # Adicionar mensagem
        memory.add_message(session_id, message)
        print("✅ Mensagem adicionada")
        
        # Recuperar conversa
        conversation = memory.get_conversation(session_id)
        print(f"✅ Conversa recuperada: {len(conversation)} mensagens")
        
        # Estatísticas
        stats = memory.get_stats()
        print(f"✅ Estatísticas: {stats}")
        
        # Health check
        if hasattr(memory, 'health_check'):
            health = memory.health_check()
            print(f"✅ Health check: {health}")
        
        # Limpar
        memory.clear_conversation(session_id)
        print("✅ Conversa limpa")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no sistema de memória: {e}")
        return False

def main():
    """Função principal."""
    print("🧪 TESTE DO SISTEMA REDIS")
    print("=" * 40)
    
    # Teste de conexão
    if not test_redis_connection():
        print("\n❌ Redis não está disponível!")
        print("   Instale e inicie o Redis primeiro:")
        print("   - Ubuntu/Debian: sudo apt install redis-server && redis-server")
        print("   - macOS: brew install redis && redis-server")
        print("   - Docker: docker run -d -p 6379:6379 redis:7-alpine")
        return
    
    # Teste do sistema
    if test_memory_system():
        print("\n🎉 Todos os testes passaram!")
    else:
        print("\n❌ Alguns testes falharam!")

if __name__ == "__main__":
    main()
