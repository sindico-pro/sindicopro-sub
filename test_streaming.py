#!/usr/bin/env python3
"""
Script de teste para verificar o streaming da API.
"""
import asyncio
import aiohttp
import json

async def test_streaming():
    """Testar o endpoint de streaming."""
    
    url = "http://localhost:8000/chat/stream"
    payload = {
        "message": "Olá, como você pode me ajudar com gestão condominial?",
        "session_id": "test_session_123",
        "user_id": "test_user_456"
    }
    
    print("🚀 Testando streaming da API...")
    print(f"📡 URL: {url}")
    print(f"📝 Payload: {json.dumps(payload, indent=2)}")
    print("-" * 50)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                print(f"📊 Status: {response.status}")
                print(f"📋 Headers: {dict(response.headers)}")
                print("-" * 50)
                
                if response.status == 200:
                    print("✅ Streaming iniciado!")
                    print("📝 Conteúdo recebido:")
                    
                    async for line in response.content:
                        line_str = line.decode('utf-8').strip()
                        if line_str.startswith('data: '):
                            data_str = line_str[6:]  # Remove 'data: '
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
                                print(f"❌ Erro ao decodificar JSON: {data_str}")
                else:
                    error_text = await response.text()
                    print(f"❌ Erro: {response.status}")
                    print(f"📄 Resposta: {error_text}")
                    
    except aiohttp.ClientConnectorError:
        print("❌ Erro: Não foi possível conectar à API")
        print("💡 Certifique-se de que a API está rodando em http://localhost:8000")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

async def test_regular_endpoint():
    """Testar o endpoint regular para comparação."""
    
    url = "http://localhost:8000/chat"
    payload = {
        "message": "Teste do endpoint regular",
        "session_id": "test_session_regular",
        "user_id": "test_user_regular"
    }
    
    print("\n🔄 Testando endpoint regular...")
    print(f"📡 URL: {url}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                print(f"📊 Status: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    print("✅ Resposta recebida:")
                    print(f"📝 Mensagem: {data.get('message', 'N/A')}")
                    print(f"🆔 Session ID: {data.get('session_id', 'N/A')}")
                    print(f"👤 User ID: {data.get('user_id', 'N/A')}")
                else:
                    error_text = await response.text()
                    print(f"❌ Erro: {response.status}")
                    print(f"📄 Resposta: {error_text}")
                    
    except Exception as e:
        print(f"❌ Erro: {e}")

async def main():
    """Executar todos os testes."""
    print("🧪 Testes da API de Streaming - Síndico PRO")
    print("=" * 60)
    
    # Testar endpoint regular primeiro
    await test_regular_endpoint()
    
    print("\n" + "=" * 60)
    
    # Testar endpoint de streaming
    await test_streaming()
    
    print("\n" + "=" * 60)
    print("🏁 Testes concluídos!")

if __name__ == "__main__":
    asyncio.run(main())
