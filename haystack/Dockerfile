# langchain-container/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Kopieren der requirements.txt und Installation der Abhängigkeiten
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren des chatbot-Codes in den Container
COPY ./app /app

# gRPC-Server starten
CMD ["python", "main.py"]
