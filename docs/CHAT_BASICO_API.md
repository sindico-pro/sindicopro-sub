# 💬 Chat Básico - Sub (Subsíndico IA)

## 🎯 Objetivo Inicial

Criar uma **API Python** simples e funcional que será consumida pelo projeto Next.js do Sindico Pro, fornecendo um chat básico do Sub.

## 🏗️ Arquitetura Inicial

### Estrutura Simplificada

```
sindicopro-sub/
├── src/
│   └── sub_crew/
│       ├── __init__.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── app.py              # FastAPI application
│       │   ├── routes/
│       │   │   ├── __init__.py
│       │   │   └── chat.py         # Rotas do chat
│       │   ├── models/
│       │   │   ├── __init__.py
│       │   │   └── chat.py         # Schemas do chat
│       │   └── services/
│       │       ├── __init__.py
│       │       └── chat_service.py # Lógica do chat
│       ├── agents/
│       │   ├── __init__.py
│       │   └── sub_agent.py        # Agente principal (Sub)
│       └── config/
│           ├── __init__.py
│           └── settings.py         # Configurações
├── requirements.txt                # Dependências Python
├── .env.example                   # Variáveis de ambiente
└── README.md
```

## 🔧 Tecnologias para o MVP

### Backend (Python)

- **FastAPI**: Framework web para criar a API
- **Pydantic**: Validação de dados e schemas
- **OpenAI**: LLM para respostas do chat
- **Uvicorn**: Servidor ASGI
- **Python-dotenv**: Gerenciamento de variáveis de ambiente

### Integração

- **CORS**: Para permitir requisições do Next.js
- **JSON**: Formato de comunicação
- **HTTP/REST**: Protocolo de comunicação

## 📡 Endpoints da API

### 1. **POST /api/chat/message**

Envia uma mensagem para o Sub e recebe uma resposta.

**Request:**

```json
{
  "message": "Olá Sub, como você pode me ajudar?",
  "user_id": "user123",
  "condo_id": "condo456",
  "context": {
    "user_role": "sindico",
    "condo_type": "residencial"
  }
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "response": "Olá! Sou o Sub, seu assistente especializado em gestão condominial. Posso te ajudar com questões sobre legislação, manutenção, finanças e comunicação. Como posso ser útil hoje?",
    "message_id": "msg789",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### 2. **GET /api/chat/history/{user_id}**

Recupera o histórico de conversas do usuário.

**Response:**

```json
{
  "success": true,
  "data": {
    "conversations": [
      {
        "message_id": "msg789",
        "user_message": "Olá Sub, como você pode me ajudar?",
        "sub_response": "Olá! Sou o Sub...",
        "timestamp": "2024-01-15T10:30:00Z"
      }
    ]
  }
}
```

### 3. **GET /api/health**

Verifica se a API está funcionando.

**Response:**

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0"
}
```

## 🛠️ Implementação Inicial

### 1. **Configuração do Projeto**

```python
# requirements.txt
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
openai==1.3.0
python-dotenv==1.0.0
python-multipart==0.0.6
```

### 2. **Schemas de Dados**

```python
# src/sub_crew/api/models/chat.py
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ChatMessage(BaseModel):
    message: str
    user_id: str
    condo_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None

class ChatHistory(BaseModel):
    message_id: str
    user_message: str
    sub_response: str
    timestamp: datetime
```

### 3. **Serviço do Chat**

```python
# src/sub_crew/api/services/chat_service.py
import openai
from typing import Dict, Any
import os

class ChatService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def get_response(self, message: str, context: Dict[str, Any] = None) -> str:
        """
        Processa uma mensagem e retorna a resposta do Sub
        """
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

    def _get_system_prompt(self, context: Dict[str, Any] = None) -> str:
        """
        Gera o prompt do sistema baseado no contexto
        """
        base_prompt = """
        Você é o Sub (Subsíndico IA), um assistente especializado em gestão condominial.

        Suas características:
        - Você é amigável, profissional e sempre busca a melhor solução
        - Você tem conhecimento sobre legislação condominial, manutenção, finanças e comunicação
        - Você sempre responde em português brasileiro
        - Você é conciso mas completo em suas respostas
        - Você oferece orientações práticas e acionáveis

        Contexto do usuário: {context}

        Responda de forma clara e útil, sempre se apresentando como o Sub.
        """

        if context:
            return base_prompt.format(context=str(context))
        return base_prompt.format(context="Síndico ou administrador de condomínio")
```

### 4. **Rotas da API**

```python
# src/sub_crew/api/routes/chat.py
from fastapi import APIRouter, HTTPException
from ..models.chat import ChatMessage, ChatResponse
from ..services.chat_service import ChatService
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/chat", tags=["chat"])
chat_service = ChatService()

@router.post("/message", response_model=ChatResponse)
async def send_message(message: ChatMessage):
    """
    Envia uma mensagem para o Sub e recebe uma resposta
    """
    try:
        # Processa a mensagem
        response = await chat_service.get_response(
            message.message,
            message.context
        )

        # Gera ID único para a mensagem
        message_id = str(uuid.uuid4())

        return ChatResponse(
            success=True,
            data={
                "response": response,
                "message_id": message_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """
    Verifica se a API está funcionando
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }
```

### 5. **Aplicação FastAPI**

```python
# src/sub_crew/api/app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import chat

app = FastAPI(
    title="Sub API",
    description="API do Subsíndico IA - Assistente de Gestão Condominial",
    version="1.0.0"
)

# Configuração CORS para permitir requisições do Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://sindicopro.com"],  # Ajustar conforme necessário
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(chat.router)

@app.get("/")
async def root():
    return {"message": "Sub API - Subsíndico IA"}
```

## 🚀 Como Executar

### 1. **Configuração do Ambiente**

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas chaves
```

### 2. **Executar a API**

```bash
# Desenvolvimento
uvicorn src.sub_crew.api.app:app --reload --host 0.0.0.0 --port 8000

# Produção
uvicorn src.sub_crew.api.app:app --host 0.0.0.0 --port 8000
```

### 3. **Testar a API**

```bash
# Teste básico
curl -X POST "http://localhost:8000/api/chat/message" \
     -H "Content-Type: application/json" \
     -d '{"message": "Olá Sub!", "user_id": "test123"}'

# Verificar saúde da API
curl "http://localhost:8000/api/health"
```

## 🔗 Integração com Next.js

### Exemplo de Uso no Frontend

```typescript
// services/subApi.ts
const SUB_API_URL =
  process.env.NEXT_PUBLIC_SUB_API_URL || "http://localhost:8000";

export interface ChatMessage {
  message: string;
  user_id: string;
  condo_id?: string;
  context?: Record<string, any>;
}

export interface ChatResponse {
  success: boolean;
  data: {
    response: string;
    message_id: string;
    timestamp: string;
  };
  error?: string;
}

export const sendMessageToSub = async (
  message: ChatMessage
): Promise<ChatResponse> => {
  const response = await fetch(`${SUB_API_URL}/api/chat/message`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(message),
  });

  if (!response.ok) {
    throw new Error("Erro ao enviar mensagem para o Sub");
  }

  return response.json();
};
```

## 📋 Próximos Passos

### Fase 1 - Chat Básico (MVP)

- [x] Estrutura da API FastAPI
- [x] Endpoint básico de chat
- [x] Integração com OpenAI
- [ ] Testes básicos
- [ ] Documentação da API

### Fase 2 - Melhorias

- [ ] Histórico de conversas
- [ ] Contexto de usuário
- [ ] Validações avançadas
- [ ] Logs e monitoramento

### Fase 3 - Sistema Multi-Agente

- [ ] Implementação dos agentes especializados
- [ ] Coordenação entre agentes
- [ ] Ferramentas especializadas
- [ ] Base de conhecimento

## 🎯 Benefícios desta Abordagem

1. **Simplicidade**: Começamos com o básico e evoluímos
2. **Testabilidade**: Fácil de testar e debugar
3. **Escalabilidade**: Estrutura preparada para crescimento
4. **Integração**: API REST padrão para o Next.js
5. **Flexibilidade**: Fácil de modificar e expandir

Esta estrutura inicial nos permite ter um chat funcional rapidamente, enquanto mantemos a base para evoluir para o sistema multi-agente completo!
