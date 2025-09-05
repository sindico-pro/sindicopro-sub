#!/usr/bin/env python
"""
Teste específico para AWS MemoryDB.
"""
import os
import sys
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_aws_memorydb():
    """Testar conexão com AWS MemoryDB."""
    print("☁️  Testando AWS MemoryDB...")
    print("=" * 50)
    
    # Configurar URL do AWS MemoryDB
    aws_redis_url = "redis://clustercfg.sub-redis.lueflv.memorydb.us-east-1.amazonaws.com:6379"
    os.environ["REDIS_URL"] = aws_redis_url
    
    try:
        import redis
        client = redis.from_url(aws_redis_url, decode_responses=True)
        client.ping()
        print("✅ Conectado ao AWS MemoryDB com sucesso!")
        
        # Teste básico
        client.set("test_key", "test_value", ex=60)
        value = client.get("test_key")
        print(f"✅ Teste de escrita/leitura: {value}")
        
        # Limpar teste
        client.delete("test_key")
        print("✅ Teste concluído e limpo")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao conectar com AWS MemoryDB: {e}")
        print()
        print("🔧 POSSÍVEIS SOLUÇÕES:")
        print("   1. Verificar se o cluster está ativo na AWS")
        print("   2. Verificar permissões de rede (Security Groups)")
        print("   3. Verificar se está na mesma VPC")
        print("   4. Verificar se o endpoint está correto")
        print()
        return False

def test_memory_system_aws():
    """Testar sistema de memória com AWS MemoryDB."""
    print("\n🧠 Testando sistema de memória com AWS MemoryDB...")
    print("=" * 50)
    
    try:
        from sub_crew.memory_factory import memory
        from sub_crew.memory import ChatMessage
        from datetime import datetime
        
        # Teste básico
        session_id = "aws_test_session"
        message = ChatMessage(
            content="Teste de mensagem no AWS MemoryDB",
            sender="user",
            timestamp=datetime.now()
        )
        
        # Adicionar mensagem
        memory.add_message(session_id, message)
        print("✅ Mensagem adicionada ao AWS MemoryDB")
        
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

def show_aws_setup_instructions():
    """Mostrar instruções de configuração para AWS."""
    print("\n" + "=" * 60)
    print("☁️  CONFIGURAÇÃO PARA AWS MEMORYDB")
    print("=" * 60)
    print()
    print("1. 🔧 Configurar variáveis de ambiente:")
    print("   export GEMINI_API_KEY='sua_chave_aqui'")
    print("   export REDIS_URL='redis://clustercfg.sub-redis.lueflv.memorydb.us-east-1.amazonaws.com:6379'")
    print()
    print("2. 🐳 Usar Docker Compose para AWS:")
    print("   cp config.aws.env .env")
    print("   docker-compose -f docker-compose.aws.yml up")
    print()
    print("3. 🚀 Executar diretamente:")
    print("   python start_api.py")
    print()
    print("4. 🧪 Testar:")
    print("   python test_aws_redis.py")
    print()
    print("📋 VERIFICAÇÕES IMPORTANTES:")
    print("   ✅ Cluster MemoryDB ativo na AWS")
    print("   ✅ Security Groups permitem conexão na porta 6379")
    print("   ✅ Instância na mesma VPC do cluster")
    print("   ✅ Endpoint correto do cluster")

def main():
    """Função principal."""
    print("☁️  TESTE DO AWS MEMORYDB")
    print("=" * 60)
    
    # Teste de conexão
    if not test_aws_memorydb():
        print("\n❌ AWS MemoryDB não está acessível!")
        show_aws_setup_instructions()
        return
    
    # Teste do sistema
    if test_memory_system_aws():
        print("\n🎉 Todos os testes passaram!")
        print("   Seu sistema está pronto para usar AWS MemoryDB!")
    else:
        print("\n❌ Alguns testes falharam!")
        show_aws_setup_instructions()

if __name__ == "__main__":
    main()
