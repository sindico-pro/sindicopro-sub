#!/usr/bin/env python3
"""
Teste simples da API para verificar se está funcionando.
"""
import requests
import json

def test_api():
    """Testar a API básica."""
    
    # Testar endpoint de saúde
    print("🔍 Testando endpoint de saúde...")
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ API está funcionando!")
            print(f"Resposta: {response.json()}")
        else:
            print(f"❌ Erro: {response.text}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return
    
    print("\n" + "="*50)
    
    # Testar endpoint de chat
    print("🔍 Testando endpoint de chat...")
    payload = {
        "message": "Olá, como você pode me ajudar?",
        "session_id": "test_123",
        "user_id": "user_456"
    }
    
    try:
        response = requests.post("http://localhost:8000/chat", json=payload)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Chat funcionando!")
            data = response.json()
            print(f"Mensagem: {data.get('message', 'N/A')}")
        else:
            print(f"❌ Erro: {response.text}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print("\n" + "="*50)
    
    # Testar endpoint de streaming
    print("🔍 Testando endpoint de streaming...")
    try:
        response = requests.post("http://localhost:8000/chat/stream", json=payload, stream=True)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Streaming funcionando!")
            print("📝 Conteúdo recebido:")
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        data_str = line_str[6:]
                        if data_str == '[DONE]':
                            print("\n🏁 Streaming concluído!")
                            break
                        try:
                            data = json.loads(data_str)
                            if 'choices' in data and len(data['choices']) > 0:
                                delta = data['choices'][0].get('delta', {})
                                content = delta.get('content', '')
                                if content:
                                    print(content, end='', flush=True)
                        except json.JSONDecodeError:
                            pass
        else:
            print(f"❌ Erro: {response.text}")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_api()
