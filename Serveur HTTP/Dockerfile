FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY serveur-http.py .

CMD ["python", "serveur-http.py"]
