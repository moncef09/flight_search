FROM python:3.12-slim

WORKDIR /app

# System deps needed to build psycopg2 from source on slim images
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Apply migrations, then start the API - keeps "docker compose up" a true
# one-command bootstrap instead of requiring a separate `alembic upgrade head` step.
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
