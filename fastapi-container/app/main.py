'''FastAPI app to call the gRPC agent service and stream the response'''
import asyncio
import httpx
import grpc
import service_pb2
import service_pb2_grpc
from fastapi import FastAPI
from starlette.responses import StreamingResponse

app = FastAPI(
    title="b3rn-zero-copilot",
    description="my sofa project",
    summary="Deadpool's favorite app. Nuff said.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Mario Bee",
        "url": "http://x-force.example.com/contact/",
        "email": "bee.mario@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

http_client = httpx.AsyncClient()

@app.get("/")
def root():
    '''Root endpoint to test the API'''
    return {"message": "use .../agent/topic to call the agent service"}

@app.get("/agent/{parameter}")
async def call_agent_for(parameter: str):
    '''Call the gRPC agent service with the given parameter and stream the response'''
    q = asyncio.Queue()

    async def grpc_async():
        async with grpc.aio.insecure_channel('langchain:50051') as channel:
            stub = service_pb2_grpc.PromptServiceStub(channel)
            buffer = ""  # Buffer to aggregate fragments
            async for response in stub.GetResponseStream(
                service_pb2.PromptRequest(prompt=parameter)):
                buffer += response.answer
                if buffer.endswith('.'):  # buffer condition
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
