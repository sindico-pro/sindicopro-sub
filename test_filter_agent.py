#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para o FilterAgent
"""

import sys
import os

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sub_crew.agents.filter_agent import FilterAgent

def test_filter_agent():
    """Testa o FilterAgent com diferentes tipos de mensagens"""
    
    filter_agent = FilterAgent()
    
    # Testes de mensagens DENTRO do escopo
    in_scope_tests = [
        "Como funciona o sistema Síndico Pro?",
        "Preciso de ajuda com inadimplência no condomínio",
        "Como criar uma assembleia no sistema?",
        "Quais são as despesas condominiais?",
        "Como funciona o rateio de despesas?",
        "Preciso de orientação sobre convenção condominial",
        "Como configurar notificações no dashboard?",
        "Quais são as funcionalidades do kanban?",
        "Como gerar relatórios de ocorrências?",
        "Preciso de ajuda com manutenção predial",
        
        # Arquitetura e Engenharia Condominial
        "Sub, eu preciso fazer uma reforma na fachada e estava conversando com o conselho, e ficamos na duvida, se para esse tipo de obra, precisamos de um coro qualificado.",
        "Preciso de orientação sobre projeto de impermeabilização do condomínio",
        "Como contratar um engenheiro para obra no condomínio?",
        "Preciso de projeto arquitetônico para reforma da área de lazer",
        "Quais documentos preciso para obra de hidráulica no condomínio?",
        "Como funciona a licitação para obra condominial?",
        "Preciso de projeto elétrico para instalação de câmeras",
        "Qual a melhor forma de impermeabilizar a laje do condomínio?",
        "Como contratar arquiteto para projeto de paisagismo?",
        "Preciso de orientação sobre reforma estrutural no prédio",
        
        # Advocacia Condominial
        "Preciso de orientação sobre processo de cobrança judicial no condomínio",
        "Como contratar um advogado para o condomínio?",
        "Quais são os procedimentos para execução condominial?",
        "Preciso de orientação sobre acordo judicial com inadimplente",
        "Como funciona a mediação em conflitos condominiais?",
        "Quais são as responsabilidades civis do síndico?",
        "Preciso de orientação sobre arbitragem condominial",
        "Como proceder com notificação extrajudicial?",
        "Quais são os prazos para ação de cobrança?",
        "Preciso de orientação sobre responsabilidade por acidentes no condomínio",
        
        # Contabilidade Condominial
        "Como contratar um contador para o condomínio?",
        "Preciso de orientação sobre prestação de contas",
        "Como elaborar o balanço patrimonial do condomínio?",
        "Quais são os critérios para rateio de despesas?",
        "Como funciona o fundo de reserva condominial?",
        "Preciso de orientação sobre auditoria contábil",
        "Como elaborar o orçamento anual do condomínio?",
        "Quais são as despesas extraordinárias?",
        "Como funciona a conciliação bancária?",
        "Preciso de orientação sobre lançamentos contábeis"
    ]
    
    # Testes de mensagens FORA do escopo
    out_of_scope_tests = [
        "O que faz um urologista?",
        "Como fazer uma consulta médica pessoal?",
        "Preciso de um advogado para divórcio pessoal",
        "Quero contratar um contador para minha empresa pessoal",
        "Como funciona o Instagram?",
        "Qual o melhor restaurante da cidade?",
        "Preciso de ajuda com meu carro pessoal",
        "Como viajar para a Europa?",
        "Quero comprar roupas online",
        "Como funciona o Netflix?",
        "Preciso de um psicólogo para depressão",
        "Qual o melhor time de futebol?",
        "Como funciona a política brasileira?",
        "Preciso de ajuda com religião pessoal"
    ]
    
    print("🧪 TESTANDO FILTER AGENT")
    print("=" * 50)
    
    print("\n✅ TESTES - MENSAGENS DENTRO DO ESCOPO:")
    print("-" * 40)
    
    for i, message in enumerate(in_scope_tests, 1):
        is_in_scope, response, metadata = filter_agent.analyze_message(message)
        status = "✅ DENTRO" if is_in_scope else "❌ FORA"
        print(f"{i:2d}. {status} | {message}")
        if not is_in_scope:
            print(f"    Score: {metadata.get('total_score', 0)} | Confidence: {metadata.get('confidence', 'unknown')}")
    
    print("\n❌ TESTES - MENSAGENS FORA DO ESCOPO:")
    print("-" * 40)
    
    for i, message in enumerate(out_of_scope_tests, 1):
        is_in_scope, response, metadata = filter_agent.analyze_message(message)
        status = "❌ FORA" if not is_in_scope else "✅ DENTRO"
        print(f"{i:2d}. {status} | {message}")
        if is_in_scope:
            print(f"    Score: {metadata.get('total_score', 0)} | Confidence: {metadata.get('confidence', 'unknown')}")
    
    print("\n📊 RESUMO DOS TESTES:")
    print("-" * 40)
    
    # Contar resultados
    in_scope_correct = sum(1 for msg in in_scope_tests 
                          if filter_agent.analyze_message(msg)[0])
    out_scope_correct = sum(1 for msg in out_of_scope_tests 
                           if not filter_agent.analyze_message(msg)[0])
    
    total_tests = len(in_scope_tests) + len(out_of_scope_tests)
    accuracy = (in_scope_correct + out_scope_correct) / total_tests * 100
    
    print(f"✅ Dentro do escopo: {in_scope_correct}/{len(in_scope_tests)} ({in_scope_correct/len(in_scope_tests)*100:.1f}%)")
    print(f"❌ Fora do escopo: {out_scope_correct}/{len(out_scope_tests)} ({out_scope_correct/len(out_scope_tests)*100:.1f}%)")
    print(f"🎯 Precisão geral: {accuracy:.1f}%")
    
    # Testar resposta de fora do escopo
    print("\n💬 EXEMPLO DE RESPOSTA PARA PERGUNTA FORA DO ESCOPO:")
    print("-" * 60)
    test_message = "O que faz um urologista?"
    is_in_scope, response, metadata = filter_agent.analyze_message(test_message)
    print(f"Pergunta: {test_message}")
    print(f"Resposta: {response}")

if __name__ == "__main__":
    test_filter_agent()
