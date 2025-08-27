# -*- coding: utf-8 -*-
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv
from .ai_providers import AIServiceFactory
from ...agents.filter_agent import FilterAgent

# Carrega variáveis de ambiente
load_dotenv()

class ChatService:
    """Serviço para processamento de mensagens do chat"""
    
    def __init__(self, ai_provider: str = "gemini"):
        """
        Inicializa o serviço com o provedor de IA especificado
        
        Args:
            ai_provider: Nome do provedor de IA ("openai" ou "gemini")
        """
        self.ai_provider = ai_provider
        self.provider = AIServiceFactory.create_provider(ai_provider)
        self.filter_agent = FilterAgent()
    
    async def get_response(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Processa uma mensagem e retorna a resposta do Sub
        
        Args:
            message: Mensagem do usuário
            context: Contexto adicional (opcional)
            
        Returns:
            Resposta do Sub
        """
        print(f"🔧 Chat Service: Processando mensagem com {self.ai_provider}")
        print(f"📝 Mensagem: {message}")
        print(f"🏢 Contexto: {context}")
        
        # Primeiro, verificar se a mensagem está dentro do escopo
        print("🔍 Filter Agent: Analisando escopo da mensagem...")
        is_in_scope, filter_response, filter_metadata = self.filter_agent.analyze_message(message, context)
        
        print(f"🔍 Filter Agent: Resultado - {'DENTRO' if is_in_scope else 'FORA'} do escopo")
        print(f"🔍 Filter Agent: Metadados - {filter_metadata}")
        
        if not is_in_scope:
            print("🚫 Filter Agent: Mensagem fora do escopo, retornando resposta filtrada")
            return filter_response
        
        print("✅ Filter Agent: Mensagem dentro do escopo, processando com IA...")
        
        try:
            response = await self.provider.generate_response(message, context)
            print(f"✅ Chat Service: Resposta gerada com sucesso")
            return response
            
        except Exception as e:
            print(f"❌ Erro ao processar mensagem com {self.ai_provider}: {e}")
            return "Desculpe, estou enfrentando dificuldades técnicas no momento. Pode tentar novamente em alguns instantes?"
    
    def get_provider_info(self) -> Dict[str, Any]:
        """
        Retorna informações sobre o provedor de IA atual
        
        Returns:
            Informações do provedor
        """
        return {
            "provider": self.ai_provider,
            "available_providers": AIServiceFactory.get_available_providers()
        }
