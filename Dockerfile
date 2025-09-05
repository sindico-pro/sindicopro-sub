# Dockerfile para Síndico PRO Chatbot
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de configuração
COPY pyproject.toml poetry.lock ./

# Instalar Poetry
RUN pip install poetry

# Configurar Poetry
RUN poetry config virtualenvs.create false

# Instalar dependências
RUN poetry install --no-dev

# Copiar código fonte
COPY src/ ./src/
COPY start_api.py ./
COPY config.env.example ./

# Criar diretórios necessários
RUN mkdir -p memory_data logs

# Expor porta
EXPOSE 8000

# Definir variáveis de ambiente
ENV PYTHONPATH=/app/src
ENV API_HOST=0.0.0.0
ENV API_PORT=8000

# Comando para iniciar a API
CMD ["python", "start_api.py"]
