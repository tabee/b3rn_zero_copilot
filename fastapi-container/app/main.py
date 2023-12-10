import httpx
import grpc
import service_pb2
import service_pb2_grpc
from fastapi import FastAPI
from contextlib import contextmanager
from starlette.responses import StreamingResponse
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



from contextlib import contextmanager

@contextmanager
def grpc_channel():
    channel = grpc.insecure_channel('langchain:50051')
    try:
        yield channel
    finally:
        channel.close()

import anyio

import threading
import queue

@app.get("/agent/{parameter}")
async def call_agent_for(parameter: str):
    '''Call the gRPC agent service with the given parameter and stream the response'''
    try:
        q = queue.Queue()

        def grpc_thread():
            with grpc.insecure_channel('langchain:50051') as channel:
                stub = service_pb2_grpc.PromptServiceStub(channel)
                stream = stub.GetResponseStream(service_pb2.PromptRequest(prompt=parameter))
                for response in stream:
                    q.put(response.answer + "")
                q.put(None)  # Signal the end of the stream

        threading.Thread(target=grpc_thread).start()

        async def stream_generator():
            while True:
                result = q.get()
                if result is None:
                    break
                yield result

        return StreamingResponse(stream_generator(), media_type="text/plain")
    except httpx.RequestError as exc:
        print(f"Anfrage fehlgeschlagen: {exc}")
        return JSONResponse(status_code=500, content={"message": "gRPC-Service agent call_grpc_parameter ist nicht erreichbar"})
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return JSONResponse(status_code=500, content={"message": "Ein unerwarteter Fehler ist aufgetreten."})
