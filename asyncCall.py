import uvicorn
import asyncio
from fastapi import FastAPI
import httpx
import grpc.aio

from logger import logger
from grpc_service import serve_grpc
from config import HOST, PORT, GRPC_PORT, API_URL, TIMEOUT_TOTAL, TIMEOUT_CONNECT

app = FastAPI()


@app.get("/")
async def read_root():
    """Return the home page response.

    Returns:
        message (str): A welcome message
    """
    logger.info("Root endpoint accessed.")
    return {"message": "Hello, World!"}


@app.get("/async-item/{item_id}")
async def read_item(item_id: int):
    """Fetch an item by its ID from the JSONPlaceholder API.

    Args:
        item_id (int): The ID of the item to fetch

    Returns:
        dict: The fetched item data or error message
    """
    logger.info(f"Fetching item with ID: {item_id}")
    timeout = httpx.Timeout(TIMEOUT_TOTAL, connect=TIMEOUT_CONNECT)
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.get(f"{API_URL}{item_id}")
            response.raise_for_status()
            logger.info(f"Successfully fetched item: {item_id}")
            return response.json()
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            return {"error": f"Request error: {e}"}
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code}")
            return {"error": f"HTTP error: {e.response.status_code}"}


async def start_servers():
    """Start both FastAPI and gRPC servers."""
    # Create and start the gRPC server
    grpc_server = await serve_grpc(host=HOST, port=GRPC_PORT)
    await grpc_server.start()
    logger.info(f"gRPC server started on {HOST}:{GRPC_PORT}")

    # Start FastAPI server
    config = uvicorn.Config(app, host=HOST, port=PORT, loop="asyncio")
    server = uvicorn.Server(config)
    logger.info(f"FastAPI server started on {HOST}:{PORT}")
    
    await server.serve()
    await asyncio.Event().wait()  # Keep the server running indefinitely


if __name__ == "__main__":
    logger.info("Starting the servers...")
    # Initialize grpc.aio
    grpc.aio.init_grpc_aio()
    asyncio.run(start_servers())

