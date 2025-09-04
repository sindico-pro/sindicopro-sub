# 🏢 Sub (Subsíndico IA) - Sistema Multi-Agente com CrewAI

Bem-vindo ao **Sub** (Subsíndico IA), um assistente de inteligência artificial especializado em gestão condominial. Esta é a versão inicial com sistema multi-agente usando CrewAI, que será consumida pelo projeto Next.js do Sindico Pro.

## 🎯 Sobre o Projeto

O **Sub** é um assistente IA multi-agente que ajuda síndicos e administradores de condomínios com:

- 🤖 **Agentes Especializados**: Sistema de múltiplos agentes coordenados
- 📋 **Orientações Legais**: Consultas sobre legislação condominial
- 🔧 **Manutenção Predial**: Dicas e orientações técnicas
- 💰 **Gestão Financeira**: Aconselhamento sobre finanças condominiais
- 📢 **Comunicação**: Estratégias para melhorar a comunicação
- 🛠️ **Resolução de Problemas**: Análise e soluções para questões comuns
- 🌐 **Pesquisa Web**: Busca de informações atualizadas na internet

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
# OBRIGATÓRIO: Adicionar sua GEMINI_API_KEY
# Obtenha sua chave em: https://aistudio.google.com/app/apikey
```

### 3. **Executar o Sub Crew**

```bash
# Com o ambiente virtual ativado
source .venv/bin/activate.fish  # Para fish shell
# ou
source .venv/bin/activate       # Para bash/zsh

# Executar o comando
poetry run sub_crew
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

# Google AI Configuration (Google AI Studio)
GEMINI_API_KEY=your_gemini_api_key_here

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
├── knowledge/                     # Base de conhecimento
├── src/
│   └── sub_crew/
│       ├── config/               # Configurações dos agentes e tarefas
│       │   ├── agents.yaml       # Configuração dos agentes
│       │   └── tasks.yaml        # Configuração das tarefas
│       ├── tools/                # Ferramentas customizadas
│       ├── crew.py               # Definição da crew principal
│       └── main.py               # Ponto de entrada da aplicação
├── pyproject.toml                # Configuração do Poetry
├── poetry.lock                   # Lock das dependências
├── env.example                   # Exemplo de configuração
└── README.md
```

## 🎯 Próximos Passos

### Fase 1 - Sistema Multi-Agente com CrewAI ✅

- [x] Configuração básica do CrewAI
- [x] Agentes especializados em gestão condominial
- [x] Integração com Google Gemini
- [x] Ferramentas de busca web

### Fase 2 - Melhorias

- [ ] Base de conhecimento condominial
- [ ] Histórico de conversas
- [ ] Contexto de usuário
- [ ] Validações avançadas

### Fase 3 - API e Integração

- [ ] API REST para integração com frontend
- [ ] Sistema de autenticação
- [ ] Logs e monitoramento
- [ ] Deploy em produção

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
