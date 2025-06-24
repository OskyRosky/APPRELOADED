import sys
import asyncio
import importlib.util
import os

def ejecutar_descarga(url: str, ruta_salida: str):
    # Cargar dinámicamente el archivo DESCARGA.py
    script_path = os.path.join(os.path.dirname(__file__), "DESCARGA.py")
    spec = importlib.util.spec_from_file_location("descarga", script_path)
    descarga = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(descarga)

    async def run():
        await descarga.descargar_documentos(url, ruta_salida)

    asyncio.run(run())

# Si se ejecuta desde consola (para pruebas directas)
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("❌ Faltan argumentos: url y ruta de descarga")
    else:
        ejecutar_descarga(sys.argv[1], sys.argv[2])