# Integração Next.js - Síndico PRO Chatbot

Este guia mostra como integrar o chatbot Síndico PRO em um projeto Next.js.

## 🚀 Configuração Inicial

### 1. Criar projeto Next.js

```bash
npx create-next-app@latest sindico-pro-frontend
cd sindico-pro-frontend
```

### 2. Instalar dependências

```bash
npm install axios
npm install @types/node  # Se usando TypeScript
```

## 📁 Estrutura do Projeto

```
sindico-pro-frontend/
├── components/
│   ├── Chat.tsx
│   ├── Message.tsx
│   └── ChatInput.tsx
├── lib/
│   ├── chatbot.ts
│   └── types.ts
├── pages/
│   ├── api/
│   │   └── chat.ts
│   └── index.tsx
├── styles/
│   └── Chat.module.css
└── package.json
```

## 🔧 Implementação

### 1. Tipos TypeScript (`lib/types.ts`)

```typescript
export interface ChatMessage {
  id: string;
  content: string;
  sender: "user" | "assistant";
  timestamp: Date;
}

export interface ChatResponse {
  response: string;
  session_id: string;
  timestamp: string;
  message_id: string;
}

export interface ChatRequest {
  message: string;
  session_id?: string;
  user_id?: string;
}
```

### 2. Cliente da API (`lib/chatbot.ts`)

```typescript
import axios from "axios";
import { ChatRequest, ChatResponse } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class ChatbotAPI {
  private baseURL: string;

  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async sendMessage(
    message: string,
    sessionId?: string
  ): Promise<ChatResponse> {
    try {
      const response = await axios.post<ChatResponse>(`${this.baseURL}/chat`, {
        message,
        session_id: sessionId,
      } as ChatRequest);

      return response.data;
    } catch (error) {
      console.error("Erro ao enviar mensagem:", error);
      throw new Error("Falha ao comunicar com o chatbot");
    }
  }

  async getHistory(sessionId: string) {
    try {
      const response = await axios.get(
        `${this.baseURL}/sessions/${sessionId}/history`
      );
      return response.data;
    } catch (error) {
      console.error("Erro ao obter histórico:", error);
      throw new Error("Falha ao obter histórico da conversa");
    }
  }

  async clearHistory(sessionId: string) {
    try {
      await axios.delete(`${this.baseURL}/sessions/${sessionId}`);
    } catch (error) {
      console.error("Erro ao limpar histórico:", error);
      throw new Error("Falha ao limpar histórico");
    }
  }
}

export const chatbotAPI = new ChatbotAPI();
```

### 3. Componente de Mensagem (`components/Message.tsx`)

```tsx
import React from "react";
import { ChatMessage } from "../lib/types";
import styles from "../styles/Chat.module.css";

interface MessageProps {
  message: ChatMessage;
}

export default function Message({ message }: MessageProps) {
  return (
    <div className={`${styles.message} ${styles[message.sender]}`}>
      <div className={styles.messageContent}>{message.content}</div>
      <div className={styles.messageTime}>
        {message.timestamp.toLocaleTimeString()}
      </div>
    </div>
  );
}
```

### 4. Componente de Input (`components/ChatInput.tsx`)

```tsx
import React, { useState } from "react";
import styles from "../styles/Chat.module.css";

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
}

export default function ChatInput({ onSendMessage, disabled }: ChatInputProps) {
  const [input, setInput] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !disabled) {
      onSendMessage(input.trim());
      setInput("");
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.inputForm}>
      <div className={styles.inputContainer}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Digite sua pergunta sobre condomínios..."
          disabled={disabled}
          className={styles.textInput}
        />
        <button
          type="submit"
          disabled={disabled || !input.trim()}
          className={styles.sendButton}
        >
          {disabled ? "Enviando..." : "Enviar"}
        </button>
      </div>
    </form>
  );
}
```

### 5. Componente Principal do Chat (`components/Chat.tsx`)

```tsx
import React, { useState, useEffect, useRef } from "react";
import { ChatMessage } from "../lib/types";
import { chatbotAPI } from "../lib/chatbot";
import Message from "./Message";
import ChatInput from "./ChatInput";
import styles from "../styles/Chat.module.css";

export default function Chat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll para a última mensagem
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Mensagem de boas-vindas
  useEffect(() => {
    const welcomeMessage: ChatMessage = {
      id: "welcome",
      content:
        "Olá! Sou o assistente virtual do Síndico PRO. Como posso ajudá-lo com questões condominiais hoje?",
      sender: "assistant",
      timestamp: new Date(),
    };
    setMessages([welcomeMessage]);
  }, []);

  const sendMessage = async (content: string) => {
    if (!content.trim()) return;

    setLoading(true);

    // Adicionar mensagem do usuário
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      content,
      sender: "user",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);

    try {
      // Enviar para a API
      const response = await chatbotAPI.sendMessage(
        content,
        sessionId || undefined
      );

      // Atualizar session ID se necessário
      if (!sessionId) {
        setSessionId(response.session_id);
      }

      // Adicionar resposta do assistente
      const assistantMessage: ChatMessage = {
        id: response.message_id,
        content: response.response,
        sender: "assistant",
        timestamp: new Date(response.timestamp),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Erro ao enviar mensagem:", error);

      // Adicionar mensagem de erro
      const errorMessage: ChatMessage = {
        id: `error-${Date.now()}`,
        content:
          "Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente.",
        sender: "assistant",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const clearChat = async () => {
    if (sessionId) {
      try {
        await chatbotAPI.clearHistory(sessionId);
      } catch (error) {
        console.error("Erro ao limpar histórico:", error);
      }
    }

    setMessages([]);
    setSessionId(null);

    // Adicionar mensagem de boas-vindas novamente
    const welcomeMessage: ChatMessage = {
      id: "welcome-new",
      content: "Conversa limpa! Como posso ajudá-lo com questões condominiais?",
      sender: "assistant",
      timestamp: new Date(),
    };
    setMessages([welcomeMessage]);
  };

  return (
    <div className={styles.chatContainer}>
      <div className={styles.chatHeader}>
        <h1>Síndico PRO Chatbot</h1>
        <button onClick={clearChat} className={styles.clearButton}>
          Limpar Conversa
        </button>
      </div>

      <div className={styles.messagesContainer}>
        {messages.map((message) => (
          <Message key={message.id} message={message} />
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className={styles.inputArea}>
        <ChatInput onSendMessage={sendMessage} disabled={loading} />
      </div>
    </div>
  );
}
```

### 6. Estilos CSS (`styles/Chat.module.css`)

```css
.chatContainer {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 800px;
  margin: 0 auto;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
}

.chatHeader {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #f5f5f5;
  border-bottom: 1px solid #e0e0e0;
}

.chatHeader h1 {
  margin: 0;
  color: #333;
  font-size: 1.5rem;
}

.clearButton {
  padding: 0.5rem 1rem;
  background-color: #ff4444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.clearButton:hover {
  background-color: #cc3333;
}

.messagesContainer {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background-color: #fafafa;
}

.message {
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
}

.message.user {
  align-items: flex-end;
}

.message.assistant {
  align-items: flex-start;
}

.messageContent {
  max-width: 70%;
  padding: 0.75rem 1rem;
  border-radius: 18px;
  word-wrap: break-word;
}

.message.user .messageContent {
  background-color: #007bff;
  color: white;
}

.message.assistant .messageContent {
  background-color: white;
  color: #333;
  border: 1px solid #e0e0e0;
}

.messageTime {
  font-size: 0.75rem;
  color: #666;
  margin-top: 0.25rem;
  padding: 0 0.5rem;
}

.inputArea {
  padding: 1rem;
  background-color: white;
  border-top: 1px solid #e0e0e0;
}

.inputForm {
  width: 100%;
}

.inputContainer {
  display: flex;
  gap: 0.5rem;
}

.textInput {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 20px;
  outline: none;
  font-size: 1rem;
}

.textInput:focus {
  border-color: #007bff;
}

.sendButton {
  padding: 0.75rem 1.5rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
}

.sendButton:hover:not(:disabled) {
  background-color: #0056b3;
}

.sendButton:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

/* Responsividade */
@media (max-width: 768px) {
  .chatContainer {
    height: 100vh;
    border-radius: 0;
    border: none;
  }

  .messageContent {
    max-width: 85%;
  }
}
```

### 7. Página Principal (`pages/index.tsx`)

```tsx
import React from "react";
import Head from "next/head";
import Chat from "../components/Chat";

export default function Home() {
  return (
    <>
      <Head>
        <title>Síndico PRO Chatbot</title>
        <meta
          name="description"
          content="Assistente virtual para questões condominiais"
        />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        <Chat />
      </main>
    </>
  );
}
```

### 8. Variáveis de Ambiente (`.env.local`)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🚀 Executando o Projeto

### 1. Iniciar o backend (Chatbot API)

```bash
cd sindicopro-sub
python start_api.py
```

### 2. Iniciar o frontend (Next.js)

```bash
cd sindico-pro-frontend
npm run dev
```

### 3. Acessar a aplicação

- Frontend: http://localhost:3000
- API: http://localhost:8000

## 🔧 Funcionalidades Implementadas

- ✅ Chat em tempo real
- ✅ Contexto de conversa mantido
- ✅ Interface responsiva
- ✅ Mensagens de erro
- ✅ Limpeza de conversa
- ✅ Scroll automático
- ✅ Indicador de carregamento
- ✅ TypeScript support

## 🎨 Personalização

Você pode personalizar:

- Cores e estilos no CSS
- Mensagens de boas-vindas
- Layout e componentes
- Funcionalidades adicionais

## 📱 Recursos Mobile

O design é responsivo e funciona bem em dispositivos móveis:

- Interface adaptável
- Touch-friendly
- Scroll suave
- Input otimizado para mobile

---

**Pronto! Seu chatbot Síndico PRO está integrado ao Next.js! 🎉**
