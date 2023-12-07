import httpx
import grpc
import service_pb2
import service_pb2_grpc
from fastapi import FastAPI
from starlette.responses import JSONResponse

app = FastAPI()

# Eine Instanz des HTTP-Clients erstellen
http_client = httpx.AsyncClient()

def some_function():
    return "Hello fastapi-container!"

@app.get("/")
def root():
    return {"message": some_function()}

@app.get("/call-grpc")
def call_grpc():
    '''Call the gRPC service with a default parameter'''
    try:
        with grpc.insecure_channel('langchain:50051') as channel:
            stub = service_pb2_grpc.PromptServiceStub(channel)
            response = stub.GetResponse(service_pb2.PromptRequest(prompt='Hallo Welt'))
            print("PromptService client received: " + response.answer)
            return response.answer
    except httpx.RequestError as exc:
        print(f"Anfrage fehlgeschlagen: {exc}")
        return JSONResponse(status_code=500, content={"message": "gRPC-Service call_grpc ist nicht erreichbar"})
    

@app.get("/call-grpc/{parameter}")
def call_grpc_parameter(parameter: str):
    '''Call the gRPC service with the given parameter'''
    try:
        with grpc.insecure_channel('langchain:50051') as channel:
            stub = service_pb2_grpc.PromptServiceStub(channel)
            response = stub.GetResponse(service_pb2.PromptRequest(prompt=parameter))
            print("PromptService client received: " + response.answer)
            return response.answer
    except httpx.RequestError as exc:
        print(f"Anfrage fehlgeschlagen: {exc}")
        return JSONResponse(status_code=500, content={"message": "gRPC-Service call_grpc_parameter ist nicht erreichbar"})
