import httpx
import grpc
import service_pb2
import service_pb2_grpc
from fastapi import FastAPI
from contextlib import contextmanager
import asyncio
import grpc
import service_pb2
import service_pb2_grpc
from contextlib import contextmanager
from starlette.responses import StreamingResponse
from starlette.responses import JSONResponse

app = FastAPI()

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


@app.get("/agent/{parameter}")
async def call_agent_for(parameter: str):
    '''Call the gRPC agent service with the given parameter and stream the response'''
    q = asyncio.Queue()

    async def grpc_async():
        async with grpc.aio.insecure_channel('langchain:50051') as channel:
            stub = service_pb2_grpc.PromptServiceStub(channel)
            buffer = ""  # Buffer to aggregate fragments
            async for response in stub.GetResponseStream(service_pb2.PromptRequest(prompt=parameter)):
                buffer += response.answer
                if buffer.endswith('.'):  # Replace this condition with a more appropriate one for your use case
                    await q.put(buffer)
                    buffer = ""  # Reset the buffer
            await q.put(None)  # Signal the end of the stream

    async def stream_generator():
        asyncio.create_task(grpc_async())
        while True:
            result = await q.get()
            if result is None:
                break
            yield result + "\n"  # Send the complete sentence or paragraph

    return StreamingResponse(stream_generator(), media_type="text/plain")
