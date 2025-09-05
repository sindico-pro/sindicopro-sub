#!/usr/bin/env python
"""
Teste rápido da API do Síndico PRO Chatbot.
"""
import requests
import json

def test_api():
    """Testar a API local."""
    base_url = "http://localhost:8000"
    
    print("🧪 Testando API do Síndico PRO Chatbot")
    print("=" * 50)
    
    # Teste 1: Health check
    print("1. Testando health check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check OK")
            print(f"   Resposta: {response.json()}")
        else:
            print(f"❌ Health check falhou: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API")
        print("   Certifique-se de que a API está rodando:")
        print("   python start_api.py")
        return
    
    print()
    
    # Teste 2: Chat
    print("2. Testando chat...")
    try:
        payload = {
            "message": "Testando"
        }
        
        response = requests.post(f"{base_url}/chat", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat funcionando!")
            print(f"   Session ID: {data['session_id']}")
            print(f"   Resposta: {data['response'][:100]}...")
        else:
            print(f"❌ Chat falhou: {response.status_code}")
            print(f"   Erro: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro no chat: {e}")
    
    print()
    print("🎉 Teste concluído!")

if __name__ == "__main__":
    test_api()
