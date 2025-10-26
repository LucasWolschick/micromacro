FROM python:3.13-slim
WORKDIR /app

COPY ./common /app/common

WORKDIR /app/catalog
COPY ./catalog/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./catalog /app/catalog

WORKDIR /app/catalog

CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]