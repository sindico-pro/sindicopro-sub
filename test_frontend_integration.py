#!/usr/bin/env python3
"""
Script para testar a integração frontend-backend
"""

import requests
import json
import time

def test_frontend_integration():
    """Testa se a API está pronta para receber requisições do frontend"""
    
    print("🧪 Testando integração frontend-backend...")
    print("=" * 60)
    
    # Dados de teste
    session_id = "test_frontend_session"
    user_id = "test_frontend_user"
    
    # 1. Testar se a API está rodando
    print("🔍 Verificando se a API está rodando...")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ API está rodando")
        else:
            print(f"❌ API retornou status {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Erro ao conectar com a API: {e}")
        return
    
    # 2. Testar endpoint de chat streaming
    print("\n📡 Testando endpoint de chat streaming...")
    payload = {
        "message": "Teste de integração frontend",
        "session_id": session_id,
        "user_id": user_id
    }
    
    try:
        response = requests.post("http://localhost:8000/chat/stream", json=payload)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Endpoint de streaming funcionando")
            
            # Verificar se retorna dados de streaming
            content = response.text
            if "data:" in content:
                print("✅ Formato de streaming correto")
            else:
                print("⚠️ Formato de streaming pode estar incorreto")
        else:
            print(f"❌ Erro no endpoint de streaming: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao testar streaming: {e}")
    
    # 3. Testar endpoint de histórico
    print("\n📚 Testando endpoint de histórico...")
    try:
        response = requests.get(
            f"http://localhost:8000/sessions/{session_id}/history?user_id={user_id}",
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Histórico carregado: {len(data.get('messages', []))} mensagens")
        elif response.status_code == 404:
            print("✅ Histórico vazio (normal para nova sessão)")
        else:
            print(f"❌ Erro no histórico: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao testar histórico: {e}")
    
    print("\n🎉 Teste de integração concluído!")
    print("\n💡 Agora você pode testar no frontend:")
    print("   1. Abrir http://localhost:3000")
    print("   2. Fazer login")
    print("   3. Abrir o chat")
    print("   4. Digitar uma mensagem e clicar em enviar")

if __name__ == "__main__":
    test_frontend_integration()
