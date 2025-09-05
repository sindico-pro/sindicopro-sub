#!/usr/bin/env python
"""
Exemplos de uso do modo chat do Síndico PRO Chatbot.
"""
import sys
import os
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sub_crew.main import run, chat

def example_direct_usage():
    """Exemplo de uso direto da função run."""
    print("=" * 60)
    print("📝 EXEMPLO 1: Uso direto da função run()")
    print("=" * 60)
    
    # Pergunta personalizada
    question = "Preciso saber sobre a contratação de funcionários para o condomínio. Quais são os procedimentos?"
    
    print(f"🤖 Pergunta: {question}")
    print()
    
    try:
        result = run(question)
        print("📝 Resposta:")
        print(str(result))
    except Exception as e:
        print(f"❌ Erro: {e}")

def example_chat_mode():
    """Exemplo de uso do modo chat."""
    print("\n" + "=" * 60)
    print("💬 EXEMPLO 2: Modo chat interativo")
    print("=" * 60)
    
    # Simular argumentos da linha de comando
    original_argv = sys.argv.copy()
    
    try:
        # Simular: python -m sub_crew.main chat "Pergunta aqui"
        sys.argv = ["main.py", "chat", "Como calcular a taxa de condomínio?"]
        chat()
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        # Restaurar argumentos originais
        sys.argv = original_argv

def example_multiple_questions():
    """Exemplo com múltiplas perguntas."""
    print("\n" + "=" * 60)
    print("🔄 EXEMPLO 3: Múltiplas perguntas")
    print("=" * 60)
    
    questions = [
        "Olá! Sou síndico de um condomínio residencial.",
        "Preciso contratar um porteiro. Quais são os requisitos?",
        "E sobre o salário mínimo para porteiro?",
        "Quais documentos preciso para a contratação?",
        "Obrigado pela ajuda!"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n{i}. Pergunta: {question}")
        print("-" * 40)
        
        try:
            result = run(question)
            print(f"Resposta: {str(result)[:200]}...")
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        print()

def example_error_handling():
    """Exemplo de tratamento de erros."""
    print("\n" + "=" * 60)
    print("⚠️  EXEMPLO 4: Tratamento de erros")
    print("=" * 60)
    
    # Pergunta que pode causar erro
    question = "Esta é uma pergunta que não é sobre condomínios. O que você vai fazer?"
    
    print(f"🤖 Pergunta: {question}")
    print()
    
    try:
        result = run(question)
        print("📝 Resposta:")
        print(str(result))
    except Exception as e:
        print(f"❌ Erro capturado: {e}")
        print("   (Isso é esperado para perguntas fora do contexto)")

def show_usage_instructions():
    """Mostrar instruções de uso."""
    print("\n" + "=" * 60)
    print("📚 INSTRUÇÕES DE USO")
    print("=" * 60)
    print()
    print("1. 🚀 Modo API (Recomendado para produção):")
    print("   python start_api.py")
    print("   # Acesse http://localhost:8000/docs")
    print()
    print("2. 💬 Modo Chat (Para testes rápidos):")
    print("   sub_crew chat 'Sua pergunta aqui'")
    print("   # ou")
    print("   python -m src.sub_crew.main chat 'Sua pergunta aqui'")
    print()
    print("3. 🔧 Uso programático:")
    print("   from sub_crew.main import run")
    print("   result = run('Sua pergunta aqui')")
    print()
    print("4. 🧪 Teste da API:")
    print("   python examples/api_usage.py")
    print()

if __name__ == "__main__":
    print("🏢 SÍNDICO PRO CHATBOT - EXEMPLOS DE USO")
    print("=" * 60)
    print()
    
    # Verificar se a API key está configurada
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  AVISO: GEMINI_API_KEY não encontrada!")
        print("   Configure a variável de ambiente:")
        print("   export GEMINI_API_KEY='sua_chave_aqui'")
        print()
        print("   Ou execute: python setup.py")
        print()
    
    # Executar exemplos
    try:
        example_direct_usage()
        example_chat_mode()
        example_multiple_questions()
        example_error_handling()
        show_usage_instructions()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Execução interrompida pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro geral: {e}")
        print("   Verifique se todas as dependências estão instaladas")
        print("   Execute: pip install -e .")
    
    print("\n🎉 Exemplos concluídos!")
    print("   Para mais informações, consulte o README.md")
