# streamlit/Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

# Kopieren der .proto-Datei in den Container
COPY ./service.proto .

# Generieren des gRPC-Codes
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto



EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# here we store the db's
ENV DATA_PATH /app/data/

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]