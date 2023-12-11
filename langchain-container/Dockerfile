# langchain-container/Dockerfile
FROM python:3.9

WORKDIR /chatbot

# Kopieren der requirements.txt und Installation der Abhängigkeiten
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren des chatbot-Codes in den Container
COPY ./chatbot /chatbot
# Kopieren der .proto-Datei in den Container
# Unschön so, @todo: separate Docker und dann diesem Docker anhängen wäre besser.
COPY ./service.proto .

# Generieren des gRPC-Codes
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto

# gRPC-Server starten
CMD ["python", "main.py"]
