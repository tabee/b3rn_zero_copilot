''' The main entry point for the chatbot service. '''
from concurrent import futures
import grpc
import service_pb2
import service_pb2_grpc
from agent import agent_for

class PromptService(service_pb2_grpc.PromptServiceServicer):
    '''The gRPC service implementation.'''
    def GetResponseStream(self, request, context):
        '''Get the response stream for the given request.'''
        for chunk in agent_for(topic=request.prompt):
            yield service_pb2.PromptReply(answer=chunk)

def serve():
    '''Serve the gRPC service.'''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_PromptServiceServicer_to_server(PromptService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

serve()
