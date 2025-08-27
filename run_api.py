#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para executar a API do Sub (Subsíndico IA)
"""

import uvicorn
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

if __name__ == "__main__":
    # Configurações da API
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    print(f"🚀 Iniciando Sub API...")
    print(f"📍 Host: {host}")
    print(f"🔌 Porta: {port}")
    print(f"🐛 Debug: {debug}")
    print(f"📚 Documentação: http://{host}:{port}/docs")
    print(f"❤️  Health Check: http://{host}:{port}/api/chat/health")
    print("-" * 50)
    
    # Executa a API
    uvicorn.run(
        "src.sub_crew.api.app:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )
