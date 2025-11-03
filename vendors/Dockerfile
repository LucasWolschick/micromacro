FROM python:3.13-slim
WORKDIR /app

COPY ./common /app/common

WORKDIR /app/vendors
COPY ./vendors/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./vendors /app/vendors

WORKDIR /app/vendors

CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]