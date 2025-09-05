# Troubleshooting - Erro 422 (Unprocessable Entity)

## 🚨 Problema Identificado

O erro `422 Unprocessable Entity` indica que há um problema com a validação dos dados enviados para o endpoint `/chat/stream`.

## 🔍 Possíveis Causas

### 1. **Problema no Modelo Pydantic**

- O campo `conversation_history` estava definido como `List[Dict]` sem especificar o tipo do Dict
- **Solução**: Criado modelo específico `ConversationMessage`

### 2. **Problema no Frontend**

- O `useCompletion` do AI SDK estava enviando dados em formato incorreto
- **Solução**: Implementado streaming manual com fetch

### 3. **Problema de Validação**

- Dados não estavam passando na validação do Pydantic
- **Solução**: Modelos mais específicos e validação melhorada

## ✅ Correções Implementadas

### 1. **Backend (api.py)**

```python
# Antes
conversation_history: Optional[List[Dict]] = None

# Depois
class ConversationMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    conversation_history: Optional[List[ConversationMessage]] = None
```

### 2. **Frontend (ChatInterface.tsx)**

```typescript
// Antes - useCompletion com problemas
const { completion, complete, isLoading: isStreaming } = useCompletion({...})

// Depois - Streaming manual
const [isStreaming, setIsStreaming] = useState(false)
const [streamingText, setStreamingText] = useState('')

// Requisição manual com controle total
const response = await fetch('http://localhost:8000/chat/stream', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: currentMessage,
    session_id: sessionId,
    user_id: user?.id || null,
    conversation_history: messages.map((msg) => ({
      role: msg.role,
      content: msg.content,
    })),
  }),
})
```

## 🧪 Como Testar

### 1. **Teste da API**

```bash
cd sindicopro-sub
python test_api_simple.py
```

### 2. **Teste Manual com cURL**

```bash
curl -X POST "http://localhost:8000/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Olá, como você pode me ajudar?",
    "session_id": "test_123",
    "user_id": "user_456",
    "conversation_history": [
      {"role": "user", "content": "Mensagem anterior"}
    ]
  }'
```

### 3. **Verificar Logs**

```bash
# No terminal onde a API está rodando
# Deve mostrar:
# INFO: 127.0.0.1:XXXXX - "POST /chat/stream HTTP/1.1" 200 OK
```

## 🔧 Debugging

### 1. **Verificar Validação Pydantic**

```python
# Adicionar no endpoint para debug
print(f"Request data: {request.dict()}")
```

### 2. **Verificar Headers CORS**

```python
# No api.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. **Verificar Console do Navegador**

- Abrir DevTools (F12)
- Ir para Network tab
- Enviar mensagem
- Verificar se a requisição está sendo feita corretamente

## 📋 Checklist de Verificação

- [ ] API está rodando na porta 8000
- [ ] Frontend está rodando na porta 3000
- [ ] CORS está configurado corretamente
- [ ] Modelos Pydantic estão corretos
- [ ] Dados estão sendo enviados no formato correto
- [ ] Headers estão corretos
- [ ] Não há erros no console do navegador

## 🚀 Solução Final

A implementação atual usa:

1. **Streaming Manual** - Controle total sobre a requisição
2. **Modelos Pydantic Específicos** - Validação correta dos dados
3. **Estados de UI Separados** - `isStreaming` e `streamingText`
4. **Tratamento de Erros** - Mensagens de erro claras

## 📞 Se Ainda Houver Problemas

1. **Verificar logs da API** para erros específicos
2. **Testar com Postman/Insomnia** para isolar o problema
3. **Verificar se Redis está rodando** (necessário para a API)
4. **Verificar se todas as dependências estão instaladas**

A implementação atual deve resolver o erro 422 e permitir o streaming funcionar corretamente! 🎉
