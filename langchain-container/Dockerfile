# langchain-container/Dockerfile
FROM python:3.9

WORKDIR /chatbot

# Kopieren der requirements.txt und Installation der Abhängigkeiten
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI und Uvicorn installieren
RUN pip install fastapi uvicorn

# Kopieren des chatbot-Codes in den Container
COPY ./chatbot /chatbot

# FastAPI-Server starten
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
