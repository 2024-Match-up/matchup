from fastapi import APIRouter, WebSocket
from auth import AuthJWT
from fastapi.responses import HTMLResponse
from template import html

router = APIRouter(
    prefix="/api/v1/exercise",
    tags=["exercise"],
)

@router.get("/")
async def get():
    return HTMLResponse(html)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
