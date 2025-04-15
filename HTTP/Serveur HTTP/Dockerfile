FROM python:3.11-slim

WORKDIR /app

COPY serveur-http.py /app/serveur-http.py
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "serveur-http.py"]
