from fastapi import APIRouter
from pydantic import BaseModel
import subprocess
import threading
import os

router = APIRouter()

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