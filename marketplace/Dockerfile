FROM python:3.13-slim
RUN apt-get update && apt-get install -y curl

WORKDIR /app

COPY ./common /app/common

WORKDIR /app/marketplace
COPY ./marketplace/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./marketplace /app/marketplace

WORKDIR /app/marketplace

CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]

HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
    CMD curl -f https://localhost:8000/health || exit 1