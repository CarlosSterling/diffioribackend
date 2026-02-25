#!/bin/sh
set -e

echo "⌛ Esperando PostgreSQL (${POSTGRES_HOST})..."
for i in $(seq 1 30); do
  pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" && break
  sleep 1
done

echo "🗄️  Migraciones + collectstatic"
python manage.py migrate --noinput
python manage.py collectstatic --noinput
chmod -R 755 /app/staticfiles

echo "🚀 Iniciando Gunicorn"
exec gunicorn back_viva.wsgi:application -w 4 -b 0.0.0.0:8000
