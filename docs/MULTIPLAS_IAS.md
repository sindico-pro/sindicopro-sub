# 🤖 Suporte a Múltiplas IAs - Sub (Subsíndico IA)

## 🎯 Visão Geral

O Sub agora suporta múltiplos provedores de IA, permitindo flexibilidade na escolha do modelo de linguagem e facilidade para alternar entre diferentes provedores.

## 🔧 Provedores Suportados

### 1. **Google Gemini** (Padrão)

- **Modelo**: `gemini-pro`
- **Vantagens**:
  - Gratuito para uso básico
  - Boa performance em português
  - Integração nativa com Google
- **Configuração**: `GOOGLE_AI_API_KEY`

### 2. **OpenAI GPT**

- **Modelo**: `gpt-4`
- **Vantagens**:
  - Alta qualidade de resposta
  - Boa compreensão de contexto
  - API estável e confiável
- **Configuração**: `OPENAI_API_KEY`

## ⚙️ Configuração

### Variáveis de Ambiente

```bash
# Provedor de IA padrão (gemini ou openai)
DEFAULT_AI_PROVIDER=gemini

# Google AI Configuration
GOOGLE_AI_API_KEY=your_google_ai_api_key_here

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
```

### Como Configurar

1. **Copie o arquivo de exemplo:**

   ```bash
   cp env.example .env
   ```

2. **Configure as chaves de API:**

   ```bash
   # Para usar Gemini (padrão)
   GOOGLE_AI_API_KEY=sua_chave_do_google_ai
   DEFAULT_AI_PROVIDER=gemini

   # Para usar OpenAI
   OPENAI_API_KEY=sua_chave_da_openai
   DEFAULT_AI_PROVIDER=openai
   ```

## 🔄 Como Alternar Entre Provedores

### 1. **Via Variável de Ambiente**

```bash
# Usar Gemini
export DEFAULT_AI_PROVIDER=gemini

# Usar OpenAI
export DEFAULT_AI_PROVIDER=openai
```

### 2. **Via Arquivo .env**

```bash
# Editar o arquivo .env
DEFAULT_AI_PROVIDER=gemini  # ou openai
```

### 3. **Verificar Provedor Atual**

```bash
# Verificar qual provedor está ativo
curl "http://localhost:8000/api/chat/providers"
```

## 📡 Endpoints da API

### **GET /api/chat/providers**

Lista os provedores disponíveis e o atual.

**Response:**

```json
{
  "current_provider": "gemini",
  "available_providers": ["openai", "gemini"],
  "description": "Provedores de IA suportados pelo Sub"
}
```

### **GET /api/chat**

Informações do chat incluindo o provedor atual.

**Response:**

```json
{
  "service": "Sub Chat API",
  "description": "API do Subsíndico IA - Assistente de Gestão Condominial",
  "ai_provider": "gemini",
  "available_providers": ["openai", "gemini"],
  "endpoints": {
    "POST /api/chat/message": "Enviar mensagem para o Sub",
    "GET /api/chat/health": "Verificar saúde da API",
    "GET /api/chat/providers": "Listar provedores de IA disponíveis"
  }
}
```

## 🧪 Testando Diferentes Provedores

### Script de Teste Atualizado

O script `test_api.py` agora mostra informações sobre o provedor:

```bash
python test_api.py
```

**Saída esperada:**

```
🧪 Iniciando testes da API do Sub...
==================================================
⏳ Aguardando API inicializar...

ℹ️  Testando Informações da API...
✅ Chat API: Sub Chat API
🤖 Provedor de IA: gemini
📋 Provedores disponíveis: openai, gemini
✅ Provedores: gemini (atual)
```

### Teste Manual

```bash
# Verificar provedor atual
curl "http://localhost:8000/api/chat/providers"

# Enviar mensagem de teste
curl -X POST "http://localhost:8000/api/chat/message" \
     -H "Content-Type: application/json" \
     -d '{"message": "Olá Sub! Qual IA você está usando?", "user_id": "test123"}'
```

## 🏗️ Arquitetura Modular

### Estrutura de Classes

```
AIProvider (ABC)
├── OpenAIProvider
└── GoogleGeminiProvider

AIServiceFactory
└── create_provider(provider_name)

ChatService
└── __init__(ai_provider)
```

### Adicionando Novos Provedores

Para adicionar um novo provedor de IA:

1. **Criar nova classe:**

   ```python
   class NovoProvedorProvider(AIProvider):
       def __init__(self):
           # Configuração do provedor
           pass

       async def generate_response(self, message: str, context=None) -> str:
           # Implementação da geração de resposta
           pass
   ```

2. **Atualizar o Factory:**

   ```python
   @staticmethod
   def create_provider(provider_name: str = "gemini") -> AIProvider:
       if provider_name == "novo_provedor":
           return NovoProvedorProvider()
       # ... outros provedores
   ```

3. **Adicionar variáveis de ambiente:**
   ```bash
   NOVO_PROVEDOR_API_KEY=sua_chave
   ```

## 💡 Comparação de Provedores

| Aspecto        | Google Gemini     | OpenAI GPT   |
| -------------- | ----------------- | ------------ |
| **Custo**      | Gratuito (básico) | Pago por uso |
| **Qualidade**  | Boa               | Excelente    |
| **Português**  | Nativo            | Muito bom    |
| **Velocidade** | Rápido            | Moderado     |
| **Limitações** | Rate limits       | Rate limits  |
| **Integração** | Google Cloud      | OpenAI API   |

## 🎯 Recomendações de Uso

### **Para Desenvolvimento/Teste:**

- Use **Google Gemini** (gratuito e suficiente)

### **Para Produção:**

- Use **OpenAI GPT** (melhor qualidade)
- Considere **Google Gemini** para reduzir custos

### **Para Alta Demanda:**

- Implemente **fallback** entre provedores
- Use **load balancing** entre múltiplas IAs

## 🔮 Próximos Passos

### Funcionalidades Planejadas

1. **Fallback Automático**

   - Se um provedor falhar, usar outro automaticamente

2. **Load Balancing**

   - Distribuir requisições entre múltiplos provedores

3. **Provedores Adicionais**

   - Claude (Anthropic)
   - Llama (Meta)
   - Local models

4. **Configuração Dinâmica**

   - Mudar provedor via API sem reiniciar

5. **Métricas por Provedor**
   - Monitorar performance de cada IA
   - Comparar qualidade das respostas

## 🛠️ Troubleshooting

### Problemas Comuns

1. **Erro: "Provedor de IA não suportado"**

   - Verifique se `DEFAULT_AI_PROVIDER` está correto
   - Valores aceitos: `gemini`, `openai`

2. **Erro: "API_KEY não configurada"**

   - Verifique se a chave está no arquivo `.env`
   - Reinicie a API após mudar as variáveis

3. **Respostas lentas ou erros**
   - Verifique a conectividade com o provedor
   - Considere alternar para outro provedor

### Logs de Debug

```bash
# Ativar logs detalhados
export LOG_LEVEL=DEBUG
python run_api.py
```

---

**O sistema modular permite fácil expansão e manutenção, garantindo que o Sub sempre tenha a melhor IA disponível para ajudar os síndicos!** 🏢🤖
