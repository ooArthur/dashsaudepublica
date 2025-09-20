# Usa uma imagem Python oficial e leve
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /appdatasaude

# Copia somente o requirements primeiro (melhora cache de build)
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código do projeto para dentro do container
COPY . .

# Cria diretórios de dados (se não existirem)
RUN mkdir -p /appdatasaude/data/raw /appdatasaude/data/processed

# Expõe a porta do Streamlit
EXPOSE 8080

# Configurações de ambiente do Streamlit
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8080 \
    STREAMLIT_SERVER_ENABLECORS=false \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Comando padrão para iniciar a aplicação
CMD ["streamlit", "run", "Dashboard.py"]
