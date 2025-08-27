# 🛠️ Estrutura Técnica - Sub (Subsíndico IA)

## 📁 Estrutura de Diretórios Proposta

```
sindicopro-sub/
├── docs/                          # Documentação do projeto
│   ├── SUB_PLANO_IMPLEMENTACAO.md
│   ├── PERGUNTAS_ESCLARECEDORAS.md
│   ├── EXEMPLO_PRATICO.md
│   └── ESTRUTURA_TECNICA.md
├── src/
│   └── sub_crew/
│       ├── __init__.py
│       ├── main.py                # Ponto de entrada principal
│       ├── crew.py                # Configuração da crew principal
│       ├── config/
│       │   ├── agents.yaml        # Configuração dos agentes
│       │   ├── tasks.yaml         # Configuração das tarefas
│       │   └── knowledge/         # Base de conhecimento
│       │       ├── legal/         # Documentação legal
│       │       ├── maintenance/   # Guias de manutenção
│       │       ├── finance/       # Documentação financeira
│       │       └── communication/ # Guias de comunicação
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── base_agent.py      # Classe base para agentes
│       │   ├── sub_agent.py       # Agente principal (Sub)
│       │   ├── legal_agent.py     # Especialista legal
│       │   ├── maintenance_agent.py # Especialista manutenção
│       │   ├── finance_agent.py   # Especialista financeiro
│       │   └── communication_agent.py # Especialista comunicação
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── base_tool.py       # Classe base para ferramentas
│       │   ├── legal_tools.py     # Ferramentas legais
│       │   ├── maintenance_tools.py # Ferramentas manutenção
│       │   ├── finance_tools.py   # Ferramentas financeiras
│       │   ├── communication_tools.py # Ferramentas comunicação
│       │   └── utility_tools.py   # Ferramentas utilitárias
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── logger.py          # Sistema de logs
│       │   ├── config.py          # Gerenciamento de configuração
│       │   ├── validators.py      # Validações
│       │   └── formatters.py      # Formatação de respostas
│       └── api/
│           ├── __init__.py
│           ├── routes.py          # Rotas da API
│           ├── middleware.py      # Middleware de autenticação
│           └── schemas.py         # Schemas de dados
├── tests/
│   ├── __init__.py
│   ├── test_agents/              # Testes dos agentes
│   ├── test_tools/               # Testes das ferramentas
│   ├── test_integration/         # Testes de integração
│   └── fixtures/                 # Dados de teste
├── knowledge/                    # Base de conhecimento externa
│   ├── legal_docs/              # Documentação legal
│   ├── maintenance_guides/      # Guias de manutenção
│   ├── finance_templates/       # Templates financeiros
│   └── communication_examples/  # Exemplos de comunicação
├── pyproject.toml               # Configuração do projeto
├── .env.example                 # Exemplo de variáveis de ambiente
├── .gitignore                   # Arquivos ignorados pelo git
└── README.md                    # Documentação principal
```

## 🔧 Configuração dos Agentes

### `src/sub_crew/config/agents.yaml`

```yaml
# Agente Principal - Sub (Subsíndico)
sub_agent:
  role: >
    Subsíndico IA - Assistente especializado em gestão condominial
  goal: >
    Fornecer orientações completas e práticas para síndicos e administradores
    de condomínios, coordenando especialistas para resolver problemas complexos
  backstory: >
    Você é o Sub, um assistente IA especializado em gestão condominial.
    Você tem anos de experiência ajudando síndicos a resolver problemas
    complexos. Você é amigável, profissional e sempre busca a melhor
    solução para cada situação.

# Agente Especialista Legal
legal_agent:
  role: >
    Especialista em Direito Condominial e Legislação
  goal: >
    Fornecer orientações jurídicas precisas sobre questões condominiais,
    baseadas na legislação vigente e jurisprudência
  backstory: >
    Você é um advogado especializado em direito condominial com mais de
    15 anos de experiência. Você conhece profundamente a Lei do Condomínio,
    o Código Civil e toda a jurisprudência relevante.

# Agente Especialista em Manutenção
maintenance_agent:
  role: >
    Especialista em Manutenção Predial e Infraestrutura
  goal: >
    Orientar sobre manutenção preventiva, identificação de problemas
    estruturais e gestão de fornecedores
  backstory: >
    Você é um engenheiro civil especializado em manutenção predial com
    vasta experiência em condomínios. Você conhece todos os sistemas
    prediais e as melhores práticas de manutenção.

# Agente Especialista Financeiro
finance_agent:
  role: >
    Especialista em Gestão Financeira Condominial
  goal: >
    Analisar situações financeiras, criar estratégias de cobrança e
    orientar sobre planejamento financeiro
  backstory: >
    Você é um contador especializado em gestão condominial com expertise
    em análise financeira, cobrança e planejamento orçamentário.

# Agente Especialista em Comunicação
communication_agent:
  role: >
    Especialista em Comunicação e Relacionamento Condominial
  goal: >
    Desenvolver estratégias de comunicação eficazes e orientar sobre
    gestão de conflitos e relacionamento com moradores
  backstory: >
    Você é um especialista em comunicação organizacional com foco em
    condomínios. Você tem experiência em mediação de conflitos e
    desenvolvimento de estratégias de comunicação.
```

## 📋 Configuração das Tarefas

### `src/sub_crew/config/tasks.yaml`

```yaml
# Tarefa de Análise Inicial
analyze_query_task:
  description: >
    Analisar a consulta do usuário e identificar as áreas de conhecimento
    necessárias para fornecer uma resposta completa e acionável.
  expected_output: >
    Análise estruturada da consulta com identificação dos especialistas
    necessários e pontos principais a serem abordados.
  agent: sub_agent

# Tarefa de Consulta Legal
legal_consultation_task:
  description: >
    Fornecer orientações jurídicas específicas sobre a questão apresentada,
    baseadas na legislação condominial vigente.
  expected_output: >
    Orientação jurídica detalhada com base legal, procedimentos recomendados
    e considerações importantes.
  agent: legal_agent

# Tarefa de Análise de Manutenção
maintenance_analysis_task:
  description: >
    Analisar questões relacionadas à manutenção predial e fornecer
    orientações técnicas e práticas.
  expected_output: >
    Análise técnica detalhada com recomendações de manutenção, identificação
    de problemas e orientações sobre fornecedores.
  agent: maintenance_agent

# Tarefa de Análise Financeira
financial_analysis_task:
  description: >
    Analisar aspectos financeiros da situação e fornecer estratégias
    de gestão financeira e cobrança.
  expected_output: >
    Análise financeira detalhada com estratégias de cobrança, impactos
    econômicos e recomendações de planejamento.
  agent: finance_agent

# Tarefa de Estratégia de Comunicação
communication_strategy_task:
  description: >
    Desenvolver estratégias de comunicação eficazes para a situação
    apresentada, considerando relacionamento com moradores.
  expected_output: >
    Estratégia de comunicação detalhada com abordagens recomendadas,
    modelos de comunicação e cronograma de ações.
  agent: communication_agent

# Tarefa de Consolidação Final
consolidate_response_task:
  description: >
    Consolidar as análises de todos os especialistas em uma resposta
    final estruturada e acionável para o usuário.
  expected_output: >
    Resposta final consolidada com plano de ação estruturado, cronograma
    e próximos passos claros.
  agent: sub_agent
```

## 🛠️ Ferramentas Especializadas

### Estrutura Base das Ferramentas

```python
# src/sub_crew/tools/base_tool.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List

class BaseTool(ABC):
    """Classe base para todas as ferramentas do Sub"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Executa a ferramenta e retorna o resultado"""
        pass
    
    def validate_input(self, **kwargs) -> bool:
        """Valida os parâmetros de entrada"""
        return True
```

### Exemplos de Ferramentas Especializadas

```python
# src/sub_crew/tools/legal_tools.py
class LegalResearchTool(BaseTool):
    """Ferramenta para pesquisa de legislação condominial"""
    
    def execute(self, query: str) -> Dict[str, Any]:
        # Implementação da pesquisa legal
        pass

class DocumentGeneratorTool(BaseTool):
    """Ferramenta para geração de documentos legais"""
    
    def execute(self, document_type: str, data: Dict) -> Dict[str, Any]:
        # Implementação da geração de documentos
        pass

# src/sub_crew/tools/maintenance_tools.py
class MaintenanceDiagnosticTool(BaseTool):
    """Ferramenta para diagnóstico de problemas de manutenção"""
    
    def execute(self, problem_description: str) -> Dict[str, Any]:
        # Implementação do diagnóstico
        pass

class SupplierRecommendationTool(BaseTool):
    """Ferramenta para recomendação de fornecedores"""
    
    def execute(self, service_type: str, location: str) -> Dict[str, Any]:
        # Implementação das recomendações
        pass
```

## 🔄 Fluxo de Processamento

### 1. **Recebimento da Consulta**
```python
# src/sub_crew/main.py
def process_query(user_query: str, user_context: Dict) -> str:
    """
    Processa uma consulta do usuário e retorna uma resposta estruturada
    """
    # 1. Análise inicial da consulta
    # 2. Identificação dos especialistas necessários
    # 3. Coordenação dos agentes
    # 4. Consolidação da resposta
    # 5. Retorno da resposta final
```

### 2. **Coordenação Multi-Agente**
```python
# src/sub_crew/crew.py
class SubCrew:
    """Crew principal do Sub"""
    
    def __init__(self):
        self.agents = self._initialize_agents()
        self.tools = self._initialize_tools()
    
    def process_complex_query(self, query: str) -> str:
        """
        Processa consultas complexas coordenando múltiplos agentes
        """
        # Implementação do fluxo de coordenação
```

## 📊 Sistema de Logs e Monitoramento

### Estrutura de Logs
```python
# src/sub_crew/utils/logger.py
import logging
from typing import Dict, Any

class SubLogger:
    """Sistema de logs especializado para o Sub"""
    
    def __init__(self):
        self.logger = logging.getLogger('sub_crew')
        self._setup_logging()
    
    def log_query(self, user_query: str, user_id: str):
        """Registra consultas dos usuários"""
        pass
    
    def log_agent_response(self, agent_name: str, response: str):
        """Registra respostas dos agentes"""
        pass
    
    def log_performance_metrics(self, metrics: Dict[str, Any]):
        """Registra métricas de performance"""
        pass
```

## 🔒 Segurança e Privacidade

### Validação de Entrada
```python
# src/sub_crew/utils/validators.py
class InputValidator:
    """Validador de entrada para segurança"""
    
    @staticmethod
    def validate_user_query(query: str) -> bool:
        """Valida consultas dos usuários"""
        # Implementação da validação
        pass
    
    @staticmethod
    def sanitize_input(input_data: str) -> str:
        """Sanitiza dados de entrada"""
        # Implementação da sanitização
        pass
```

## 🧪 Estrutura de Testes

### Organização dos Testes
```
tests/
├── test_agents/
│   ├── test_sub_agent.py
│   ├── test_legal_agent.py
│   └── test_maintenance_agent.py
├── test_tools/
│   ├── test_legal_tools.py
│   └── test_maintenance_tools.py
├── test_integration/
│   ├── test_crew_workflow.py
│   └── test_api_endpoints.py
└── fixtures/
    ├── sample_queries.json
    └── expected_responses.json
```

## 🚀 Configuração de Deploy

### Variáveis de Ambiente
```bash
# .env.example
OPENAI_API_KEY=your_openai_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
LOG_LEVEL=INFO
ENVIRONMENT=development
```

### Docker Configuration
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY knowledge/ ./knowledge/

CMD ["python", "-m", "src.sub_crew.main"]
```

Esta estrutura técnica fornece uma base sólida e escalável para o desenvolvimento do Sub, permitindo fácil manutenção, testes e evolução do sistema.
