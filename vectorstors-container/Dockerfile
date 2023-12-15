# vectorstors-container/Dockerfile
FROM python:3.9

WORKDIR /vectorstors

# Kopieren der requirements.txt und Installation der Abhängigkeiten
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren des vectorstors-Codes in den Container
COPY ./vectorstors /vectorstors
# Kopieren der .proto-Datei in den Container
# Unschön so, @todo: separate Docker und dann diesem Docker anhängen wäre besser.
COPY ./service.proto .

# Generieren des gRPC-Codes
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto

# here we store the db's
ENV DATA_PATH /vectorstors/data/


CMD ["python", "main.py"]



