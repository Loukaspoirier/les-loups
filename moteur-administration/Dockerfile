# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY admin-engine.py .
COPY admin_console.py .

CMD ["python", "admin-engine.py"]
