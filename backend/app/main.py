"""Punto de entrada de la API de MammoSim.

Ejecutar:  uvicorn app.main:app --reload
Documentación automática:  http://localhost:8000/docs
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import caso_en_sesion, casos, cursos, sesiones, usuarios

app = FastAPI(title="MammoSim API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().origenes_permitidos,
    allow_methods=["*"],
    allow_headers=["*"],
)

for r in (usuarios.router, cursos.router, casos.router, sesiones.router, caso_en_sesion.router):
    app.include_router(r)


@app.get("/salud", tags=["sistema"])
def salud():
    """Render usa esta ruta para saber que el servicio está vivo."""
    return {"estado": "ok"}
