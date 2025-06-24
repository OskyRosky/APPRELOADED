from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Request
from typing import List
import subprocess
import threading
import os
import asyncio
from notifier import cola_mensajes, enviar_mensaje_ws

router = APIRouter()

connections: List[WebSocket] = []

@router.get("/")
def home():
    return {"message": "SIGED Reloaded Backend is running 🚀"}

# ✅ Permitir solicitudes OPTIONS para evitar CORS 400
@router.options("/descargar")
def options_descargar():
    return {}

# ✅ Usamos Request plano (no Pydantic) para evitar error con OPTIONS
@router.post("/descargar")
async def iniciar_descarga(request: Request):
    body = await request.json()
    url = body.get("url")
    ruta = body.get("ruta")

    print(f"🔗 Iniciando descarga para: {url}")
    print(f"📁 Ruta de descarga: {ruta}")

    def run():
        script_path = os.path.join(os.path.dirname(__file__), "..", "downloader.py")
        subprocess.run(["python3", script_path, url, ruta])

    threading.Thread(target=run).start()

    return {"status": "Descarga iniciada", "url": url}

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

async def procesar_cola_mensajes():
    while True:
        mensaje = await cola_mensajes.get()
        await enviar_a_todos(mensaje)