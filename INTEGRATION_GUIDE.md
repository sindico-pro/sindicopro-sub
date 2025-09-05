# Guia de Integração - ChatInterface com sindicopro-sub

## 📋 Resumo das Modificações

Este guia documenta as modificações realizadas para integrar o ChatInterface.tsx do frontend com a API do sindicopro-sub, incluindo suporte a `userId` e armazenamento Redis.

## 🔧 Modificações Realizadas

### 1. Backend (sindicopro-sub)

#### Modelos Pydantic (`api.py`)

- ✅ Adicionado `user_id` opcional ao `ChatRequest`
- ✅ Adicionado `conversation_history` ao `ChatRequest`
- ✅ Modificado `ChatResponse` para usar `message` em vez de `response`
- ✅ Adicionado `user_id` ao `ChatResponse`

#### Sistema de Memória Redis (`memory.py`)

- ✅ Modificado `_get_key()` para incluir `user_id` nas chaves Redis
- ✅ Atualizado `add_message()` para aceitar `user_id`
- ✅ Atualizado `get_conversation()` para aceitar `user_id`
- ✅ Atualizado `clear_conversation()` para aceitar `user_id`
- ✅ Atualizado `list_sessions()` para aceitar `user_id`
- ✅ Atualizado `get_session_info()` para aceitar `user_id`
- ✅ Atualizado `cleanup_old_sessions()` para aceitar `user_id`
- ✅ Atualizado `get_stats()` para aceitar `user_id`

#### Endpoints da API (`api.py`)

- ✅ Modificado `/chat` para processar `user_id`
- ✅ Modificado `/sessions/{session_id}/history` para aceitar `user_id`
- ✅ Modificado `DELETE /sessions/{session_id}` para aceitar `user_id`
- ✅ Modificado `GET /sessions` para aceitar `user_id`
- ✅ Modificado `/health` para aceitar `user_id`
- ✅ Modificado `/memory/status` para aceitar `user_id`

### 2. Frontend (sindico-pro-web)

#### ChatInterface.tsx

- ✅ Adicionado import do `useUser` hook
- ✅ Adicionado import do `env` para configuração
- ✅ Modificado `sendMessage()` para usar nova API
- ✅ Adicionado `user_id` nas requisições
- ✅ Atualizado URL da API para usar variável de ambiente
- ✅ Modificado limpeza de memória para usar nova API

#### Configuração de Ambiente (`env.ts`)

- ✅ Adicionado `NEXT_PUBLIC_SUB_CHAT_API_URL` ao schema
- ✅ Adicionado ao `runtimeEnv`

## 🗂️ Estrutura de Chaves Redis

Com as modificações, as chaves Redis agora seguem o padrão:

```
# Sem user_id (compatibilidade)
sindico_pro:messages:session_123
sindico_pro:count:session_123
sindico_pro:activity:session_123

# Com user_id (novo padrão)
sindico_pro:messages:user_456:session_123
sindico_pro:count:user_456:session_123
sindico_pro:activity:user_456:session_123
```

## 🚀 Como Usar

### 1. Configurar Variáveis de Ambiente

Adicione ao seu arquivo `.env.local`:

```bash
NEXT_PUBLIC_SUB_CHAT_API_URL=http://localhost:8000
```

### 2. Iniciar o Backend

```bash
cd sindicopro-sub
python start_api.py
```

### 3. Iniciar o Frontend

```bash
cd sindico-pro-web
npm run dev
```

### 4. Testar a Integração

1. Abra o chat no frontend
2. Envie uma mensagem
3. Verifique se o `user_id` está sendo enviado
4. Verifique se as mensagens estão sendo salvas no Redis com o `user_id`

## 🔍 Endpoints da API

### POST /chat

```json
{
  "message": "Olá, como posso ajudar?",
  "session_id": "session_123",
  "user_id": "user_456",
  "conversation_history": [
    {
      "role": "user",
      "content": "Mensagem anterior"
    }
  ]
}
```

### GET /sessions?user_id=user_456

Lista todas as sessões do usuário específico.

### DELETE /sessions/session_123?user_id=user_456

Limpa o histórico de uma sessão específica do usuário.

## 🧪 Testando a Integração

### 1. Verificar Redis

```bash
redis-cli
> KEYS sindico_pro:messages:user_*
> GET sindico_pro:count:user_456:session_123
```

### 2. Verificar API

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Teste",
    "user_id": "user_456",
    "session_id": "test_session"
  }'
```

### 3. Verificar Frontend

- Abra o DevTools do navegador
- Verifique se as requisições incluem `user_id`
- Verifique se as respostas estão corretas

## 🔒 Segurança

- O `user_id` é opcional para manter compatibilidade
- As chaves Redis são isoladas por usuário quando `user_id` é fornecido
- TTL de 30 dias para expiração automática das conversas

## 📝 Próximos Passos

1. ✅ Implementar autenticação JWT na API
2. ✅ Adicionar rate limiting por usuário
3. ✅ Implementar logs de auditoria
4. ✅ Adicionar métricas de uso por usuário
5. ✅ Implementar backup das conversas

## 🐛 Troubleshooting

### Erro de Conexão

- Verifique se o Redis está rodando
- Verifique se a API está rodando na porta 8000
- Verifique a variável `NEXT_PUBLIC_SUB_CHAT_API_URL`

### Erro de CORS

- Verifique se o CORS está configurado na API
- Verifique se a URL do frontend está na lista de origens permitidas

### Erro de Autenticação

- Verifique se o usuário está logado
- Verifique se o `user_id` está sendo enviado corretamente
