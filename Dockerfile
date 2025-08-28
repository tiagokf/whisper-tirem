FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements
COPY requirements-flask.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements-flask.txt

# Copiar código da aplicação
COPY . .

# Expor porta
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "--threads=4", "wsgi:app"]