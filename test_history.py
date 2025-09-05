#!/usr/bin/env python3
"""
Script para testar o carregamento de histórico de conversas
"""

import requests
import json
import time

def test_conversation_history():
    """Testa o endpoint de histórico de conversas"""
    
    print("🧪 Testando carregamento de histórico de conversas...")
    print("=" * 60)
    
    # Dados de teste
    session_id = "test_session_123"
    user_id = "test_user_456"
    
    # 1. Primeiro, criar algumas mensagens de teste
    print("📝 Criando mensagens de teste...")
    
    test_messages = [
        "Olá, como você pode me ajudar?",
        "Qual é o seu nome?",
        "Obrigado pela ajuda!"
    ]
    
    for i, message in enumerate(test_messages):
        print(f"  Enviando mensagem {i+1}: {message}")
        
        payload = {
            "message": message,
            "session_id": session_id,
            "user_id": user_id
        }
        
        try:
            response = requests.post("http://localhost:8000/chat", json=payload)
            if response.status_code == 200:
                print(f"  ✅ Mensagem {i+1} enviada com sucesso")
            else:
                print(f"  ❌ Erro ao enviar mensagem {i+1}: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Erro de conexão: {e}")
        
        # Pequena pausa entre mensagens
        time.sleep(1)
    
    print("\n" + "=" * 60)
    
    # 2. Agora testar o carregamento do histórico
    print("📚 Testando carregamento do histórico...")
    
    try:
        response = requests.get(
            f"http://localhost:8000/sessions/{session_id}/history?user_id={user_id}",
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Histórico carregado com sucesso!")
            print(f"📊 Total de mensagens: {len(data.get('messages', []))}")
            
            print("\n📋 Mensagens no histórico:")
            for i, msg in enumerate(data.get('messages', []), 1):
                sender = "👤 Usuário" if msg.get('sender') == 'user' else "🤖 Sub"
                content = msg.get('content', '')
                timestamp = msg.get('timestamp', 'N/A')
                print(f"  {i}. {sender}: {content[:50]}{'...' if len(content) > 50 else ''}")
                print(f"     Timestamp: {timestamp}")
                print()
                
        else:
            print(f"❌ Erro ao carregar histórico: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
    
    print("\n" + "=" * 60)
    
    # 3. Testar limpeza do histórico
    print("🧹 Testando limpeza do histórico...")
    
    try:
        response = requests.delete(
            f"http://localhost:8000/sessions/{session_id}?user_id={user_id}",
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Histórico limpo com sucesso!")
        else:
            print(f"❌ Erro ao limpar histórico: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
    
    print("\n🎉 Teste de histórico concluído!")

if __name__ == "__main__":
    test_conversation_history()
