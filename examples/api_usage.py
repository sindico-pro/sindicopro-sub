#!/usr/bin/env python
"""
Exemplo de uso da API do Síndico PRO Chatbot.
"""
import requests
import json
import time

# Configuração da API
API_BASE_URL = "http://localhost:8000"

def test_chat_api():
    """Testar a API de chat."""
    print("🧪 Testando API do Síndico PRO Chatbot")
    print("=" * 50)
    
    # Testar health check
    print("1. Testando health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API está funcionando!")
            print(f"   Resposta: {response.json()}")
        else:
            print(f"❌ Erro no health check: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API")
        print("   Certifique-se de que a API está rodando em http://localhost:8000")
        return
    
    print()
    
    # Testar chat
    print("2. Testando chat...")
    session_id = None
    
    # Primeira mensagem
    print("   Enviando primeira mensagem...")
    message1 = {
        "message": "Olá! Eu sou síndico de um condomínio e preciso de ajuda."
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/chat", json=message1)
        if response.status_code == 200:
            data = response.json()
            session_id = data["session_id"]
            print("✅ Primeira mensagem enviada com sucesso!")
            print(f"   Session ID: {session_id}")
            print(f"   Resposta: {data['response'][:100]}...")
        else:
            print(f"❌ Erro ao enviar primeira mensagem: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return
    except Exception as e:
        print(f"❌ Erro: {e}")
        return
    
    print()
    
    # Segunda mensagem (com contexto)
    print("3. Testando contexto da conversa...")
    print("   Enviando segunda mensagem...")
    message2 = {
        "message": "Preciso contratar um contador para o condomínio. O que devo fazer?",
        "session_id": session_id
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/chat", json=message2)
        if response.status_code == 200:
            data = response.json()
            print("✅ Segunda mensagem enviada com sucesso!")
            print(f"   Resposta: {data['response'][:100]}...")
        else:
            print(f"❌ Erro ao enviar segunda mensagem: {response.status_code}")
            print(f"   Resposta: {response.text}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print()
    
    # Testar histórico
    print("4. Testando histórico da conversa...")
    try:
        response = requests.get(f"{API_BASE_URL}/sessions/{session_id}/history")
        if response.status_code == 200:
            data = response.json()
            print("✅ Histórico obtido com sucesso!")
            print(f"   Total de mensagens: {len(data['messages'])}")
            for i, msg in enumerate(data['messages'], 1):
                print(f"   Mensagem {i}: {msg['sender']} - {msg['content'][:50]}...")
        else:
            print(f"❌ Erro ao obter histórico: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print()
    
    # Testar listagem de sessões
    print("5. Testando listagem de sessões...")
    try:
        response = requests.get(f"{API_BASE_URL}/sessions")
        if response.status_code == 200:
            data = response.json()
            print("✅ Sessões listadas com sucesso!")
            print(f"   Total de sessões: {len(data)}")
            for session in data:
                print(f"   Sessão: {session['session_id'][:8]}... - {session['message_count']} mensagens")
        else:
            print(f"❌ Erro ao listar sessões: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print()
    print("🎉 Teste concluído!")

def test_chat_flow():
    """Testar um fluxo completo de conversa."""
    print("\n" + "=" * 50)
    print("🔄 Testando fluxo completo de conversa")
    print("=" * 50)
    
    session_id = None
    
    # Lista de perguntas para testar
    questions = [
        "Olá! Sou síndico de um condomínio residencial.",
        "Preciso saber sobre a contratação de funcionários.",
        "Quais são os documentos necessários?",
        "E sobre o salário mínimo?",
        "Obrigado pela ajuda!"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n{i}. Pergunta: {question}")
        
        message = {
            "message": question
        }
        
        if session_id:
            message["session_id"] = session_id
        
        try:
            response = requests.post(f"{API_BASE_URL}/chat", json=message)
            if response.status_code == 200:
                data = response.json()
                session_id = data["session_id"]
                print(f"   Resposta: {data['response'][:150]}...")
            else:
                print(f"   ❌ Erro: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
        
        time.sleep(1)  # Pausa entre mensagens
    
    print(f"\n✅ Fluxo concluído! Session ID: {session_id}")

if __name__ == "__main__":
    print("🚀 Iniciando testes da API Síndico PRO Chatbot")
    print("   Certifique-se de que a API está rodando em http://localhost:8000")
    print()
    
    # Instalar requests se não estiver instalado
    try:
        import requests
    except ImportError:
        print("❌ Erro: Biblioteca 'requests' não encontrada")
        print("   Instale com: pip install requests")
        exit(1)
    
    # Executar testes
    test_chat_api()
    test_chat_flow()
    
    print("\n" + "=" * 50)
    print("📚 Para mais informações, consulte:")
    print("   - Documentação da API: http://localhost:8000/docs")
    print("   - README.md do projeto")
    print("   - examples/nextjs-integration.md")
