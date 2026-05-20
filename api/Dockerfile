FROM python:3.12-slim

# ===============================
# VARIÁVEIS DE AMBIENTE
# ===============================
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# ===============================
# INSTALA DEPENDÊNCIAS DO SISTEMA
# ===============================
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice \
    libreoffice-writer \
    libreoffice-common \
    fonts-dejavu-core \
    fontconfig \
    libfbclient2 \
    gcc \
    libffi-dev \
    libssl-dev \
    python3-dev \
    curl \
    nano \
 && rm -rf /var/lib/apt/lists/*

# ===============================
# INSTALA DEPENDÊNCIAS PYTHON
# ===============================
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# ===============================
# REMOVE DEPENDÊNCIAS DE BUILD
# ===============================
RUN apt-get purge -y gcc python3-dev \
 && apt-get autoremove -y

# ===============================
# COPIA A APLICAÇÃO
# ===============================
COPY . .

# ===============================
# CRIA DIRETÓRIOS NECESSÁRIOS
# ===============================
RUN mkdir -p /app/storage/temp

# ===============================
# DECLARA VOLUME (IMPORTANTE)
# ===============================
VOLUME ["/app/storage/temp"]

# ===============================
# CRIA USUÁRIO NÃO ROOT
# ===============================
RUN useradd -m appuser \
 && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# ===============================
# WORKERS DINÂMICOS
# ===============================
ENV WORKERS=2

CMD ["sh", "-c", "gunicorn main:app -w ${WORKERS} -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --access-logfile - --error-logfile - --log-level info --capture-output"]