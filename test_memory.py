#!/usr/bin/env python
"""
Teste do sistema de memória (arquivos vs Redis).
"""
import os
import sys
import time
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_file_memory():
    """Testar memória em arquivos."""
    print("📁 Testando memória em arquivos...")
    print("=" * 50)
    
    # Configurar para usar arquivos
    os.environ["MEMORY_TYPE"] = "file"
    
    from sub_crew.memory_factory import create_memory
    from sub_crew.memory import ChatMessage
    from datetime import datetime
    
    memory = create_memory()
    
    # Teste básico
    session_id = "test_file_session"
    message = ChatMessage(
        content="Teste de mensagem em arquivo",
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
    
    # Limpar
    memory.clear_conversation(session_id)
    print("✅ Conversa limpa")
    
    return True

def test_redis_memory():
    """Testar memória Redis."""
    print("\n🔴 Testando memória Redis...")
    print("=" * 50)
    
    # Configurar para usar Redis
    os.environ["MEMORY_TYPE"] = "redis"
    os.environ["REDIS_URL"] = "redis://localhost:6379"
    os.environ["MEMORY_FALLBACK"] = "true"
    
    try:
        from sub_crew.memory_factory import create_memory
        from sub_crew.memory import ChatMessage
        from datetime import datetime
        
        memory = create_memory()
        
        # Verificar se Redis está disponível
        if hasattr(memory, 'health_check'):
            health = memory.health_check()
            if not health.get("redis_available", False):
                print("⚠️  Redis não disponível, usando fallback")
                return test_file_memory()
        
        # Teste básico
        session_id = "test_redis_session"
        message = ChatMessage(
            content="Teste de mensagem no Redis",
            sender="user",
            timestamp=datetime.now()
        )
        
        # Adicionar mensagem
        memory.add_message(session_id, message)
        print("✅ Mensagem adicionada no Redis")
        
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
        print(f"❌ Erro no Redis: {e}")
        print("🔄 Tentando fallback para arquivos...")
        return test_file_memory()

def test_performance():
    """Teste de performance comparativo."""
    print("\n⚡ Teste de performance...")
    print("=" * 50)
    
    from sub_crew.memory import ChatMessage
    from datetime import datetime
    import time
    
    # Teste com arquivos
    print("📁 Testando performance com arquivos...")
    os.environ["MEMORY_TYPE"] = "file"
    
    from sub_crew.memory_factory import create_memory
    file_memory = create_memory()
    
    start_time = time.time()
    for i in range(100):
        message = ChatMessage(
            content=f"Mensagem de teste {i}",
            sender="user",
            timestamp=datetime.now()
        )
        file_memory.add_message(f"perf_test_{i}", message)
    
    file_time = time.time() - start_time
    print(f"✅ Arquivos: {file_time:.2f}s para 100 mensagens")
    
    # Teste com Redis (se disponível)
    print("\n🔴 Testando performance com Redis...")
    os.environ["MEMORY_TYPE"] = "redis"
    
    try:
        redis_memory = create_memory()
        
        if hasattr(redis_memory, 'health_check'):
            health = redis_memory.health_check()
            if not health.get("redis_available", False):
                print("⚠️  Redis não disponível para teste de performance")
                return
        
        start_time = time.time()
        for i in range(100):
            message = ChatMessage(
                content=f"Mensagem de teste Redis {i}",
                sender="user",
                timestamp=datetime.now()
            )
            redis_memory.add_message(f"redis_perf_test_{i}", message)
        
        redis_time = time.time() - start_time
        print(f"✅ Redis: {redis_time:.2f}s para 100 mensagens")
        
        # Comparação
        if redis_time < file_time:
            speedup = file_time / redis_time
            print(f"🚀 Redis é {speedup:.1f}x mais rápido que arquivos")
        else:
            slowdown = redis_time / file_time
            print(f"🐌 Redis é {slowdown:.1f}x mais lento que arquivos")
            
    except Exception as e:
        print(f"❌ Erro no teste de performance do Redis: {e}")

def show_recommendations():
    """Mostrar recomendações de uso."""
    print("\n" + "=" * 60)
    print("📋 RECOMENDAÇÕES DE USO")
    print("=" * 60)
    print()
    print("📁 USAR ARQUIVOS quando:")
    print("   - Desenvolvimento e testes")
    print("   - Aplicações pequenas/médias (< 1000 usuários)")
    print("   - Deploy simples (sem dependências externas)")
    print("   - Custo zero de infraestrutura")
    print()
    print("🔴 USAR REDIS quando:")
    print("   - Produção com alta concorrência")
    print("   - Múltiplas instâncias da API")
    print("   - Performance crítica (< 100ms)")
    print("   - Escalabilidade horizontal")
    print()
    print("⚙️  CONFIGURAÇÃO:")
    print("   # Para arquivos (padrão)")
    print("   export MEMORY_TYPE=file")
    print()
    print("   # Para Redis")
    print("   export MEMORY_TYPE=redis")
    print("   export REDIS_URL=redis://localhost:6379")
    print("   export MEMORY_FALLBACK=true  # Fallback para arquivos")
    print()
    print("🐳 DOCKER:")
    print("   # Com Redis")
    print("   docker-compose -f docker-compose.redis.yml up")
    print()
    print("   # Sem Redis (apenas arquivos)")
    print("   docker-compose up")

def main():
    """Função principal do teste."""
    print("🧪 TESTE DO SISTEMA DE MEMÓRIA")
    print("=" * 60)
    print()
    
    try:
        # Teste com arquivos
        test_file_memory()
        
        # Teste com Redis
        test_redis_memory()
        
        # Teste de performance
        test_performance()
        
        # Recomendações
        show_recommendations()
        
        print("\n🎉 Testes concluídos!")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro geral: {e}")

if __name__ == "__main__":
    main()
