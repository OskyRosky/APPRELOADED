from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router, procesar_cola_mensajes
import asyncio

app = FastAPI()

# 👇 Este bloque es obligatorio
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend (React) local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(procesar_cola_mensajes())