import sys
import asyncio
import importlib.util
import os
from notifier import enviar_mensaje_ws


async def main(url, ruta_salida):
    # Cargar dinámicamente DESCARGA.py
    import importlib.util
    import os

    script_path = os.path.join(os.path.dirname(__file__), "DESCARGA.py")
    spec = importlib.util.spec_from_file_location("descarga", script_path)
    descarga = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(descarga)

    # Enviar mensaje de inicio
    await enviar_mensaje_ws("🚀 Iniciando descarga...")

    # Llamar la función real de descarga
    await descarga.descargar_documentos(url, ruta_salida, enviar_mensaje_ws)

    await enviar_mensaje_ws("✅ Descarga completada.")


# Si se ejecuta desde consola (para pruebas directas)
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("❌ Faltan argumentos")
    else:
        url = sys.argv[1]
        ruta = sys.argv[2]
        asyncio.run(main(url, ruta))