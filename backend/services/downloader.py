# downloader.py (ubicado en backend/)
import sys
import time

def descargar_archivos(url):
    print(f"📥 Descargando desde: {url}")
    # Simulación por ahora
    for i in range(1, 6):
        print(f"Descargando archivo {i} desde {url}...")
        time.sleep(1)
    print("✅ Descarga completa.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ No se proporcionó URL")
    else:
        descargar_archivos(sys.argv[1])