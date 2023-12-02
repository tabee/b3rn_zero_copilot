from concurrent import futures
import grpc
import service_pb2
import service_pb2_grpc
from chuck_norris import chuck_norris_joke_about

class PromptService(service_pb2_grpc.PromptServiceServicer):
    def GetResponse(self, request, context):
        res = chuck_norris_joke_about(topic=request.prompt)
        print(res)
        return service_pb2.PromptReply(answer='Joke: ' + res)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_PromptServiceServicer_to_server(PromptService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

serve()
if __name__ == '__main__':
    print("Starting server. Listening on port 50051.")
    serve()
    print("Server stopped.")
