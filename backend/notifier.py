import asyncio

cola_mensajes = asyncio.Queue()

async def enviar_mensaje_ws(mensaje: str):
    await cola_mensajes.put(mensaje)