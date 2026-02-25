FROM python:3.13.5-alpine3.22

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# ─── Dependencias del sistema ───
RUN apk add --no-cache \
        postgresql-client \        
        libpq \
    && apk add --no-cache --virtual .build-deps \
        build-base gcc musl-dev postgresql-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ─── Copiamos el proyecto ───
COPY . .

# ─── Script de arranque ───
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
