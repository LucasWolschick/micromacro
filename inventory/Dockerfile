FROM python:3.13-slim
WORKDIR /app

COPY ./common /app/common

WORKDIR /app/inventory
COPY ./inventory/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./inventory /app/inventory

WORKDIR /app/inventory

CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]