# knowledge_base/Dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

#gRPC
COPY ./service.proto .
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto

# here we store the db's
ENV DATA_PATH /app/data/

CMD ["python", "main.py"]
