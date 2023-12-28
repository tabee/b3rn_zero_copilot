# Use the official Python image as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application code into the container
COPY ./app /app

# Kopieren der .proto-Datei in den Container
# Unschön so, @todo: separate Docker und dann diesem Docker anhängen wäre besser.
COPY ./service.proto .

# Generieren des gRPC-Codes
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto

# Expose port 80 for the FastAPI application
EXPOSE 80

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
