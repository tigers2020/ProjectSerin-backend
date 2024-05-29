import asyncio

import aiohttp
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Message from client: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)


async def fetch_streaming_data():
    url = "https://thirdpartyapi.com/stream"  # 제3자 API의 스트리밍 URL
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            async for data in response.content:
                await manager.broadcast(data.decode('utf-8'))


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(fetch_streaming_data())


@app.get("/")
async def read_root():
    return {"message": "Welcome to the streaming server"}
