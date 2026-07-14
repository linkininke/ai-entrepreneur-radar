FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "until python -c \"import psycopg2; psycopg2.connect('${DATABASE_URL}')\" 2>/dev/null; do echo 'Waiting for PostgreSQL...'; sleep 2; done && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
