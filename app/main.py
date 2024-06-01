import os
import socketio
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.user_router import router as user_router
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the user router
app.include_router(user_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Project Serin API"}

# Create Socket.IO server with CORS configuration
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=settings.allowed_origins.split(",")
)
app_sio = socketio.ASGIApp(sio, app, socketio_path="/ws/socket.io")

# Define Socket.IO events
@sio.event
async def connect(sid, environ):
    try:
        logger.info(f"Client connected: {sid}")
    except Exception as e:
        logger.error(f"Error during connect: {e}")

@sio.event
async def disconnect(sid):
    try:
        logger.info(f"Client disconnected: {sid}")
    except Exception as e:
        logger.error(f"Error during disconnect: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app_sio, host=settings.host, port=settings.port)
