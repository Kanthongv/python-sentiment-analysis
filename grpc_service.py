import grpc.aio
import httpx
from concurrent import futures

# Import generated protobuf code
from protos import service_pb2
from protos import service_pb2_grpc

from logger import logger
from config import API_URL, TIMEOUT_TOTAL, TIMEOUT_CONNECT


class ItemService(service_pb2_grpc.ItemServiceServicer):
    async def GetItem(self, request, context):
        """
        Implements the GetItem RPC method.
        """
        try:
            timeout = httpx.Timeout(TIMEOUT_TOTAL, connect=TIMEOUT_CONNECT)
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(f"{API_URL}{request.item_id}")
                response.raise_for_status()
                data = response.json()
                
                return service_pb2.ItemResponse(
                    id=data.get('id', 0),
                    title=data.get('title', ''),
                    body=data.get('body', ''),
                    user_id=data.get('userId', 0)
                )
        except Exception as e:
            logger.error(f"gRPC error: {str(e)}")
            return service_pb2.ItemResponse(error=str(e))


async def serve_grpc(host: str, port: int):
    """
    Start the gRPC server
    """
    server = grpc.aio.server()
    service_pb2_grpc.add_ItemServiceServicer_to_server(ItemService(), server)
    server.add_insecure_port(f'{host}:{port}')
    return server 