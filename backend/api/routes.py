from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from typing import List
from pydantic import BaseModel
import subprocess
import threading
import os

router = APIRouter()

connections: List[WebSocket] = []

class DownloadRequest(BaseModel):
    url: str

@router.get("/")
def home():
    return {"message": "SIGED Reloaded Backend is running 🚀"}

@router.post("/descargar")
def iniciar_descarga(data: DownloadRequest):
    print(f"🔗 Iniciando descarga para: {data.url}")

    def run():
        script_path = os.path.join(os.path.dirname(__file__), "..", "downloader.py")
        download_path = "/Users/sultan/Downloads/testdescarga"  # Ruta fija de destino
        subprocess.run(["python3", script_path, data.url, download_path])

    threading.Thread(target=run).start()

    return {"status": "Descarga iniciada", "url": data.url}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connections.remove(websocket)

async def enviar_a_todos(mensaje: str):
    for conn in connections:
        try:
            await conn.send_text(mensaje)
        except Exception:
            pass

import asyncio
from notifier import cola_mensajes, enviar_mensaje_ws

async def procesar_cola_mensajes():
    while True:
        mensaje = await cola_mensajes.get()
        await enviar_a_todos(mensaje)