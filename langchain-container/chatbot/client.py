import asyncio
import grpc
import service_pb2
import service_pb2_grpc

async def call_agent_for(parameter: str):
    '''Call the gRPC agent service with the given parameter and stream the response'''
    # change localhost to the IP address of the agent service !!!!!!!!!!!
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.PromptServiceStub(channel)
        buffer = ""  # Buffer to aggregate fragments
        async for response in stub.GetResponseStream(
            service_pb2.PromptRequest(prompt=parameter)):
            buffer += response.answer
            if buffer.endswith('.'):  # Check if buffer ends with a period
                print(buffer, end="", flush=True)
                buffer = ""  # Reset the buffer

if __name__ == "__main__":
    asyncio.run(call_agent_for(parameter="Elefanten sind besser als Autos."))
