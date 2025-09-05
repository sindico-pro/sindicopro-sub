#!/usr/bin/env python
"""
Script para iniciar a API do chatbot Síndico PRO.
"""
import os
import sys
import uvicorn
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Adicionar o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def check_redis_connection():
    """Verificar se o Redis está disponível."""
    try:
        import redis
        redis_url = os.getenv("REDIS_URL")
        client = redis.from_url(redis_url, decode_responses=True)
        client.ping()
        print("✅ Redis conectado com sucesso")
        return True
    except Exception as e:
        print(f"❌ ERRO: Redis não está disponível!")
        print(f"   Erro: {e}")
        print()
        print("🔧 SOLUÇÕES:")
        print("   1. Instalar Redis:")
        print("      - Ubuntu/Debian: sudo apt install redis-server")
        print("      - macOS: brew install redis")
        print("      - Docker: docker run -d -p 6379:6379 redis:7-alpine")
        print()
        print("   2. Iniciar Redis:")
        print("      redis-server")
        print()
        print("   3. Verificar configuração:")
        print("      export REDIS_URL=redis://localhost:6379")
        print()
        return False

def main():
    """Iniciar a API do chatbot."""
    
    # Verificar se a chave da API está configurada
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  AVISO: GEMINI_API_KEY não encontrada!")
        print("   Configure a variável de ambiente GEMINI_API_KEY")
        print("   Exemplo: export GEMINI_API_KEY='sua_chave_aqui'")
        print()
    
    # Verificar Redis
    if not check_redis_connection():
        print("❌ Não é possível iniciar sem Redis!")
        sys.exit(1)
    
    # Configurações do servidor
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    print("🚀 Iniciando API do Síndico PRO Chatbot...")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   URL: http://{host}:{port}")
    print()
    print("📚 Documentação da API: http://{host}:{port}/docs")
    print("🔍 Health Check: http://{host}:{port}/health")
    print("🔴 Redis Status: http://{host}:{port}/memory/status")
    print()
    
    # Iniciar servidor
    uvicorn.run(
        "sub_crew.api:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
