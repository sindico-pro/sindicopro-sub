# 🏢 Sub (Subsíndico IA) - Chat Básico

Bem-vindo ao **Sub** (Subsíndico IA), um assistente de inteligência artificial especializado em gestão condominial. Esta é a versão inicial com chat básico, que será consumida pelo projeto Next.js do Sindico Pro.

## 🎯 Sobre o Projeto

O **Sub** é um assistente IA que ajuda síndicos e administradores de condomínios com:

- 📋 Orientações sobre legislação condominial
- 🔧 Dicas de manutenção predial
- 💰 Gestão financeira
- 📢 Estratégias de comunicação
- 🛠️ Resolução de problemas comuns

## 🚀 Início Rápido

### 1. **Instalação das Dependências**

```bash
# Instalar dependências Python
pip install -r requirements.txt
```

### 2. **Configuração do Ambiente**

```bash
# Copiar arquivo de exemplo
cp env.example .env

# Editar o arquivo .env com suas configurações
# OBRIGATÓRIO: Adicionar sua OPENAI_API_KEY
```

### 3. **Executar a API**

```bash
# Opção 1: Usando o script
python run_api.py

# Opção 2: Usando uvicorn diretamente
uvicorn src.sub_crew.api.app:app --reload --host 0.0.0.0 --port 8000
```

### 4. **Testar a API**

A API estará disponível em:

- 🌐 **API**: http://localhost:8000
- 📚 **Documentação**: http://localhost:8000/docs
- ❤️ **Health Check**: http://localhost:8000/api/chat/health

## 📡 Endpoints da API

### **POST /api/chat/message**

Envia uma mensagem para o Sub.

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
    "response": "Olá! Sou o Sub, seu assistente especializado em gestão condominial...",
    "message_id": "msg789",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### **GET /api/chat/health**

Verifica se a API está funcionando.

### **GET /api/chat/providers**

Lista os provedores de IA disponíveis.

### **GET /docs**

Documentação interativa da API (Swagger UI).

## 🔧 Configuração

### Variáveis de Ambiente (.env)

```bash
# AI Configuration
# Provedor de IA padrão (gemini ou openai)
DEFAULT_AI_PROVIDER=gemini

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Google AI Configuration
GOOGLE_AI_API_KEY=your_google_ai_api_key_here

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,https://sindicopro.com

# Logging
LOG_LEVEL=INFO
```

## 🧪 Testando a API

### Usando curl

```bash
# Teste básico
curl -X POST "http://localhost:8000/api/chat/message" \
     -H "Content-Type: application/json" \
     -d '{"message": "Olá Sub!", "user_id": "test123"}'

# Health check
curl "http://localhost:8000/api/chat/health"
```

### Usando Python

```python
import requests

# Enviar mensagem
response = requests.post(
    "http://localhost:8000/api/chat/message",
    json={
        "message": "Olá Sub!",
        "user_id": "test123"
    }
)

print(response.json())
```

## 🔗 Integração com Next.js

### Exemplo de uso no frontend

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

export const sendMessageToSub = async (message: ChatMessage) => {
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

## 📁 Estrutura do Projeto

```
sindicopro-sub/
├── docs/                          # Documentação
│   ├── SUB_PLANO_IMPLEMENTACAO.md
│   ├── CHAT_BASICO_API.md
│   └── ...
├── src/
│   └── sub_crew/
│       ├── api/                   # API FastAPI
│       │   ├── app.py            # Aplicação principal
│       │   ├── routes/           # Rotas da API
│       │   ├── models/           # Schemas Pydantic
│       │   └── services/         # Lógica de negócio
│       └── ...
├── requirements.txt               # Dependências Python
├── env.example                   # Exemplo de configuração
├── run_api.py                   # Script para executar
└── README.md
```

## 🎯 Próximos Passos

### Fase 1 - Chat Básico ✅

- [x] API FastAPI básica
- [x] Integração com OpenAI
- [x] Endpoints de chat
- [x] Documentação da API

### Fase 2 - Melhorias

- [ ] Histórico de conversas
- [ ] Contexto de usuário
- [ ] Validações avançadas
- [ ] Logs e monitoramento

### Fase 3 - Sistema Multi-Agente

- [ ] Agentes especializados
- [ ] Coordenação entre agentes
- [ ] Ferramentas especializadas
- [ ] Base de conhecimento

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

- **Documentação**: `/docs` na API
- **Issues**: GitHub Issues
- **Email**: [seu-email@exemplo.com]

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

**Sub (Subsíndico IA)** - Seu assistente especializado em gestão condominial! 🏢🤖
