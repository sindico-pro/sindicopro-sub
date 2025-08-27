# -*- coding: utf-8 -*-
"""
Sistema modular para suportar múltiplos provedores de IA
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class AIProvider(ABC):
    """Classe base para provedores de IA"""
    
    @abstractmethod
    async def generate_response(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Gera uma resposta usando o provedor de IA"""
        pass

class OpenAIProvider(AIProvider):
    """Provedor OpenAI GPT"""
    
    def __init__(self):
        import openai
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY não configurada")
        
        self.client = openai.OpenAI(api_key=api_key)
    
    async def generate_response(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Gera resposta usando OpenAI GPT"""
        try:
            system_prompt = self._get_system_prompt(context)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Erro OpenAI: {e}")
            return "Desculpe, estou enfrentando dificuldades técnicas no momento. Pode tentar novamente em alguns instantes?"
    
    def _get_system_prompt(self, context: Optional[Dict[str, Any]] = None) -> str:
        """Gera o prompt do sistema"""
        base_prompt = """
        Você é o Sub (Subsíndico IA), um assistente especializado em gestão condominial.
        
        Suas características:
        - Você é amigável, profissional e sempre busca a melhor solução
        - Você tem conhecimento sobre legislação condominial, manutenção, finanças e comunicação
        - Você sempre responde em português brasileiro
        - Você é conciso mas completo em suas respostas
        - Você oferece orientações práticas e acionáveis
        - Você sempre se apresenta como o Sub
        
        Contexto do usuário: {context}
        
        Responda de forma clara e útil, sempre se apresentando como o Sub.
        """
        
        if context:
            context_str = str(context)
        else:
            context_str = "Síndico ou administrador de condomínio"
            
        return base_prompt.format(context=context_str)

class GoogleGeminiProvider(AIProvider):
    """Provedor Google Gemini"""
    
    def __init__(self):
        import google.generativeai as genai
        
        api_key = os.getenv("GOOGLE_AI_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_AI_API_KEY não configurada")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def generate_response(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Gera resposta usando Google Gemini"""
        print(f"🤖 Gemini Provider: Gerando resposta...")
        print(f"📝 Mensagem: {message}")
        print(f"🏢 Contexto: {context}")
        
        try:
            system_prompt = self._get_system_prompt(context)
            print(f"🎯 System Prompt: {system_prompt[:100]}...")
            
            # Combina o prompt do sistema com a mensagem do usuário
            full_prompt = f"{system_prompt}\n\nUsuário: {message}\n\nSub:"
            
            response = self.model.generate_content(full_prompt)
            
            print(f"✅ Gemini Provider: Resposta gerada com sucesso")
            return response.text
            
        except Exception as e:
            print(f"❌ Erro Gemini: {e}")
            return "Desculpe, estou enfrentando dificuldades técnicas no momento. Pode tentar novamente em alguns instantes?"
    
    def _get_system_prompt(self, context: Optional[Dict[str, Any]] = None) -> str:
        """Gera o prompt do sistema para Gemini"""
        base_prompt = """
        Você é o Sub (Subsíndico IA), um assistente especializado em gestão condominial.
        
        Suas características:
        - Você é amigável, profissional e sempre busca a melhor solução
        - Você tem conhecimento sobre legislação condominial, manutenção, finanças e comunicação
        - Você sempre responde em português brasileiro
        - Você é conciso mas completo em suas respostas
        - Você oferece orientações práticas e acionáveis
        - Você sempre se apresenta como o Sub
        
        Contexto do usuário: {context}
        
        Responda de forma clara e útil, sempre se apresentando como o Sub.
        """
        
        if context:
            context_str = str(context)
        else:
            context_str = "Síndico ou administrador de condomínio"
            
        return base_prompt.format(context=context_str)

class AIServiceFactory:
    """Factory para criar provedores de IA"""
    
    @staticmethod
    def create_provider(provider_name: str = "gemini") -> AIProvider:
        """
        Cria um provedor de IA baseado no nome
        
        Args:
            provider_name: Nome do provedor ("openai" ou "gemini")
            
        Returns:
            Instância do provedor de IA
        """
        provider_name = provider_name.lower()
        
        if provider_name == "openai":
            return OpenAIProvider()
        elif provider_name == "gemini":
            return GoogleGeminiProvider()
        else:
            raise ValueError(f"Provedor de IA não suportado: {provider_name}")
    
    @staticmethod
    def get_available_providers() -> list:
        """Retorna lista de provedores disponíveis"""
        return ["openai", "gemini"]
