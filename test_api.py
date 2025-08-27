#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar se a API do Sub está funcionando
"""

import requests
import json
import time
from datetime import datetime

def test_health_check():
    """Testa o endpoint de health check"""
    print("🏥 Testando Health Check...")
    
    try:
        response = requests.get("http://localhost:8000/api/chat/health")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check OK: {data}")
            return True
        else:
            print(f"❌ Health Check falhou: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar à API. Certifique-se de que ela está rodando.")
        return False
    except Exception as e:
        print(f"❌ Erro no Health Check: {e}")
        return False

def test_chat_message():
    """Testa o endpoint de chat"""
    print("\n💬 Testando Chat...")
    
    test_message = {
        "message": "Olá Sub! Como você pode me ajudar com gestão condominial?",
        "user_id": "test_user_123",
        "condo_id": "test_condo_456",
        "context": {
            "user_role": "sindico",
            "condo_type": "residencial"
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/chat/message",
            json=test_message,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat funcionando!")
            print(f"📝 Resposta do Sub: {data['data']['response'][:100]}...")
            print(f"🆔 Message ID: {data['data']['message_id']}")
            print(f"⏰ Timestamp: {data['data']['timestamp']}")
            return True
        else:
            print(f"❌ Chat falhou: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no Chat: {e}")
        return False

def test_api_info():
    """Testa os endpoints de informação da API"""
    print("\nℹ️  Testando Informações da API...")
    
    try:
        # Testa endpoint raiz
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ Endpoint raiz OK")
        
        # Testa informações da API
        response = requests.get("http://localhost:8000/api")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Informações da API: {data['api_name']} v{data['version']}")
        
        # Testa informações do chat
        response = requests.get("http://localhost:8000/api/chat")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat API: {data['service']}")
            print(f"🤖 Provedor de IA: {data['ai_provider']}")
            print(f"📋 Provedores disponíveis: {', '.join(data['available_providers'])}")
        
        # Testa lista de provedores
        response = requests.get("http://localhost:8000/api/chat/providers")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Provedores: {data['current_provider']} (atual)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar informações: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🧪 Iniciando testes da API do Sub...")
    print("=" * 50)
    
    # Aguarda um pouco para garantir que a API está pronta
    print("⏳ Aguardando API inicializar...")
    time.sleep(2)
    
    # Executa os testes
    tests = [
        test_health_check,
        test_chat_message,
        test_api_info
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erro no teste: {e}")
            results.append(False)
    
    # Resumo dos resultados
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Testes passaram: {passed}/{total}")
    print(f"❌ Testes falharam: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 Todos os testes passaram! A API está funcionando corretamente.")
    else:
        print("⚠️  Alguns testes falharam. Verifique a configuração da API.")
    
    print(f"\n📅 Teste executado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
