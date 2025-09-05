#!/usr/bin/env python
"""
Script de configuração e instalação do Síndico PRO Chatbot.
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header():
    """Imprimir cabeçalho do script."""
    print("=" * 60)
    print("🏢 SÍNDICO PRO CHATBOT - CONFIGURAÇÃO")
    print("=" * 60)
    print()

def check_python_version():
    """Verificar versão do Python."""
    print("🐍 Verificando versão do Python...")
    
    if sys.version_info < (3, 10):
        print("❌ Erro: Python 3.10 ou superior é necessário")
        print(f"   Versão atual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def check_gemini_api_key():
    """Verificar se a chave da API do Gemini está configurada."""
    print("\n🔑 Verificando chave da API do Gemini...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️  AVISO: GEMINI_API_KEY não encontrada!")
        print("   Configure a variável de ambiente:")
        print("   export GEMINI_API_KEY='sua_chave_aqui'")
        print()
        print("   Ou crie um arquivo .env com:")
        print("   GEMINI_API_KEY=sua_chave_aqui")
        return False
    
    print("✅ GEMINI_API_KEY configurada")
    return True

def install_dependencies():
    """Instalar dependências do projeto."""
    print("\n📦 Instalando dependências...")
    
    try:
        # Instalar o projeto em modo de desenvolvimento
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-e", "."
        ], check=True, capture_output=True, text=True)
        
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        print(f"   Saída: {e.stdout}")
        print(f"   Erro: {e.stderr}")
        return False

def create_directories():
    """Criar diretórios necessários."""
    print("\n📁 Criando diretórios...")
    
    directories = [
        "memory_data",
        "examples",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ {directory}/")
    
    return True

def create_env_file():
    """Criar arquivo .env se não existir."""
    print("\n⚙️  Configurando arquivo de ambiente...")
    
    env_file = Path(".env")
    if env_file.exists():
        print("   ✅ Arquivo .env já existe")
        return True
    
    # Copiar do exemplo
    example_file = Path("config.env.example")
    if example_file.exists():
        shutil.copy(example_file, env_file)
        print("   ✅ Arquivo .env criado a partir do exemplo")
        print("   ⚠️  Lembre-se de configurar sua GEMINI_API_KEY no arquivo .env")
    else:
        print("   ⚠️  Arquivo de exemplo não encontrado")
    
    return True

def test_installation():
    """Testar se a instalação está funcionando."""
    print("\n🧪 Testando instalação...")
    
    try:
        # Testar importação dos módulos principais
        sys.path.insert(0, str(Path("src")))
        
        from sub_crew.crew import SubCrew
        from sub_crew.memory import ConversationMemory
        from sub_crew.api import app
        
        print("   ✅ Módulos importados com sucesso")
        
        # Testar criação de instâncias
        memory = ConversationMemory()
        print("   ✅ Sistema de memória funcionando")
        
        return True
    except Exception as e:
        print(f"   ❌ Erro no teste: {e}")
        return False

def show_next_steps():
    """Mostrar próximos passos."""
    print("\n" + "=" * 60)
    print("🎉 INSTALAÇÃO CONCLUÍDA!")
    print("=" * 60)
    print()
    print("📋 PRÓXIMOS PASSOS:")
    print()
    print("1. 🔑 Configure sua chave da API do Gemini:")
    print("   export GEMINI_API_KEY='sua_chave_aqui'")
    print()
    print("2. 🚀 Inicie a API:")
    print("   python start_api.py")
    print("   # ou")
    print("   uvicorn src.sub_crew.api:app --host 0.0.0.0 --port 8000 --reload")
    print()
    print("3. 🌐 Acesse a documentação:")
    print("   http://localhost:8000/docs")
    print()
    print("4. 🧪 Teste a API:")
    print("   python examples/api_usage.py")
    print()
    print("5. 🔗 Integre com Next.js:")
    print("   Consulte examples/nextjs-integration.md")
    print()
    print("📚 DOCUMENTAÇÃO:")
    print("   - README.md: Guia completo")
    print("   - examples/: Exemplos de uso")
    print("   - http://localhost:8000/docs: API docs")
    print()

def main():
    """Função principal do script de configuração."""
    print_header()
    
    # Verificações
    if not check_python_version():
        sys.exit(1)
    
    check_gemini_api_key()  # Apenas aviso, não bloqueia
    
    # Instalação
    if not install_dependencies():
        print("\n❌ Falha na instalação das dependências")
        sys.exit(1)
    
    if not create_directories():
        print("\n❌ Falha na criação dos diretórios")
        sys.exit(1)
    
    if not create_env_file():
        print("\n❌ Falha na configuração do ambiente")
        sys.exit(1)
    
    # Teste
    if not test_installation():
        print("\n❌ Falha no teste da instalação")
        sys.exit(1)
    
    # Próximos passos
    show_next_steps()

if __name__ == "__main__":
    main()
