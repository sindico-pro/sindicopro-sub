# Síndico PRO Chatbot

Assistente virtual especializado em questões condominiais brasileiras, desenvolvido com CrewAI e FastAPI.

## 🏢 Sobre o Projeto

O Síndico PRO Chatbot é um assistente virtual inteligente que utiliza agentes de IA colaborativos para responder questões relacionadas ao mercado condominial brasileiro. O sistema mantém contexto de conversa, permitindo interações naturais e contínuas.

## 🚀 Características

- **Agentes Especializados**: Sistema de agentes colaborativos usando CrewAI
- **Contexto de Conversa**: Mantém histórico das mensagens para respostas contextuais
- **API REST**: Interface FastAPI para integração com frontend
- **Google Gemini**: Modelo de linguagem avançado para respostas precisas
- **Memória Redis**: Sistema de armazenamento de conversas em Redis
- **CORS Configurado**: Pronto para integração com Next.js
- **Alta Performance**: Redis para máxima escalabilidade e velocidade

## 🛠️ Tecnologias

- **Python 3.10+**
- **CrewAI**: Framework para agentes colaborativos
- **FastAPI**: Framework web moderno e rápido
- **Google Gemini**: Modelo de linguagem
- **Pydantic**: Validação de dados
- **Uvicorn**: Servidor ASGI
- **Redis**: Cache e armazenamento de conversas

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone <repository-url>
cd sindicopro-sub
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -e .
```

### 4. Configure o Redis

#### **Opção A: Redis Local (Desenvolvimento)**

```bash
# Instalar Redis
# Ubuntu/Debian: sudo apt install redis-server
# macOS: brew install redis
# Docker: docker run -d -p 6379:6379 redis:7-alpine

# Iniciar Redis
redis-server
```

#### **Opção B: AWS MemoryDB (Produção)**

```bash
# Usar seu cluster AWS MemoryDB
# Endpoint: clustercfg.sub-redis.lueflv.memorydb.us-east-1.amazonaws.com:6379
```

### 5. Configure as variáveis de ambiente

#### **Para Redis Local:**

```bash
# Copie o arquivo de exemplo
cp config.env.example .env

# Edite o arquivo .env e configure sua chave da API
export GEMINI_API_KEY="sua_chave_do_google_gemini"

# Configuração Redis local
export REDIS_URL="redis://localhost:6379"
export REDIS_DB="0"
export REDIS_KEY_PREFIX="sindico_pro:"
```

#### **Para AWS MemoryDB:**

```bash
# Copie o arquivo de configuração AWS
cp config.aws.env .env

# Edite o arquivo .env e configure sua chave da API
export GEMINI_API_KEY="sua_chave_do_google_gemini"

# Configuração AWS MemoryDB
export REDIS_URL="redis://clustercfg.sub-redis.lueflv.memorydb.us-east-1.amazonaws.com:6379"
export REDIS_DB="0"
export REDIS_KEY_PREFIX="sindico_pro:"
```

## 🚀 Uso

### Comandos Disponíveis

```bash
# Executar com pergunta padrão
sub_crew

# Modo chat interativo
sub_crew chat "Sua pergunta aqui"

# Iniciar API
sub_crew api

# Treinar o crew
sub_crew train 10 training_data.json

# Testar o crew
sub_crew test 5 "gpt-4"

# Replay de uma tarefa
sub_crew replay task_id_123
```

### Iniciar a API

```bash
# Opção 1: Usando o script de inicialização
python start_api.py

# Opção 2: Usando uvicorn diretamente
uvicorn src.sub_crew.api:app --host 0.0.0.0 --port 8000 --reload

# Opção 3: Usando o comando do projeto
sub_crew api
```

### Acessar a documentação

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📡 API Endpoints

### Chat

```http
POST /chat
Content-Type: application/json

{
  "message": "Eu preciso contratar um contador?",
  "session_id": "optional-session-id",
  "user_id": "optional-user-id"
}
```

### Histórico de Conversa

```http
GET /sessions/{session_id}/history
```

### Listar Sessões

```http
GET /sessions
```

### Limpar Conversa

```http
DELETE /sessions/{session_id}
```

## 🔧 Integração com Next.js

### 1. Instalar dependências no frontend

```bash
npm install axios
```

### 2. Configurar cliente HTTP

```javascript
// lib/chatbot.js
import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

export const chatAPI = {
  async sendMessage(message, sessionId = null) {
    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        message,
        session_id: sessionId,
      });
      return response.data;
    } catch (error) {
      console.error("Erro ao enviar mensagem:", error);
      throw error;
    }
  },

  async getHistory(sessionId) {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/sessions/${sessionId}/history`
      );
      return response.data;
    } catch (error) {
      console.error("Erro ao obter histórico:", error);
      throw error;
    }
  },
};
```

### 3. Componente de Chat

```jsx
// components/Chat.jsx
import { useState, useEffect } from "react";
import { chatAPI } from "../lib/chatbot";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    setLoading(true);
    const userMessage = { sender: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await chatAPI.sendMessage(input, sessionId);
      setSessionId(response.session_id);

      const botMessage = {
        sender: "assistant",
        content: response.response,
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Erro:", error);
    } finally {
      setLoading(false);
      setInput("");
    }
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.content}
          </div>
        ))}
      </div>
      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Digite sua pergunta sobre condomínios..."
          disabled={loading}
        />
        <button onClick={sendMessage} disabled={loading}>
          {loading ? "Enviando..." : "Enviar"}
        </button>
      </div>
    </div>
  );
}
```

## 🧠 Sistema de Memória

O chatbot mantém contexto das conversas através de:

- **Armazenamento Local**: Arquivos JSON para persistência
- **Sessões**: Cada conversa tem um ID único
- **Histórico**: Últimas 10 mensagens são consideradas no contexto
- **Limpeza Automática**: Sessões antigas são removidas automaticamente

## 🔧 Configuração Avançada

### Variáveis de Ambiente

```bash
# API do Google Gemini
GEMINI_API_KEY=your_api_key

# Servidor
API_HOST=0.0.0.0
API_PORT=8000

# Memória
MEMORY_STORAGE_PATH=memory_data

# CORS
CORS_ORIGINS=http://localhost:3000,https://localhost:3000

# Limpeza de sessões (dias)
SESSION_CLEANUP_DAYS=30
```

### Personalização dos Agentes

Edite os arquivos de configuração:

- `src/sub_crew/config/agents.yaml`: Configuração dos agentes
- `src/sub_crew/config/tasks.yaml`: Configuração das tarefas

## 🧪 Testes

```bash
# Testar o crew diretamente
python -m src.sub_crew.main

# Testar a API
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Eu preciso contratar um contador?"}'
```

## 📝 Estrutura do Projeto

```
sindicopro-sub/
├── src/sub_crew/
│   ├── api.py              # API FastAPI
│   ├── crew.py             # Definição do crew
│   ├── main.py             # Ponto de entrada original
│   ├── memory.py           # Sistema de memória
│   ├── config/
│   │   ├── agents.yaml     # Configuração dos agentes
│   │   └── tasks.yaml      # Configuração das tarefas
│   └── tools/
│       └── custom_tool.py  # Ferramentas personalizadas
├── memory_data/            # Dados de memória (criado automaticamente)
├── start_api.py            # Script de inicialização
├── config.env.example      # Exemplo de configuração
└── README.md              # Este arquivo
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte e dúvidas, entre em contato:

- **Email**: rodrigorael53@gmail.com
- **GitHub Issues**: [Criar uma issue](https://github.com/seu-usuario/sindicopro-sub/issues)

---

**Desenvolvido com ❤️ para a comunidade condominial brasileira**
