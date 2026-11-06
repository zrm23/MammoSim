"""Endpoints 1 y 2: usuarios."""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from app.auth import UsuarioActual, get_token_data, get_usuario_actual
from app.firebase import get_db
from app.schemas import RegistroIn, RegistroOut, UsuarioOut

router = APIRouter(tags=["usuarios"])


@router.post("/auth/registro", response_model=RegistroOut, status_code=201)
def registrar(
    datos: RegistroIn, token: dict = Depends(get_token_data), db=Depends(get_db)
):
    """1. Crea usuarios/{uid} la primera vez que alguien entra.

    El uid y el correo salen del TOKEN (ya verificado), nunca del cuerpo de la
    petición: así nadie puede registrarse a nombre de otro.
    """
    # Validaciones: si algo no cumple, se corta aquí con un código de error.
    if not datos.acepto_terminos:
        raise HTTPException(422, "Debes aceptar el tratamiento de datos para registrarte")

    uid = token["uid"]
    correo = (token.get("email") or "").lower()
    if not correo:
        raise HTTPException(422, "La cuenta no tiene correo")

    ref = db.collection("usuarios").document(uid)
    if ref.get().exists:
        raise HTTPException(409, "El usuario ya está registrado")

    # El rol lo decide el servidor, no el cliente: docente solo si el correo
    # está en docentes_autorizados (el ID del documento es el correo) y activo.
    docente = db.collection("docentes_autorizados").document(correo).get()
    es_docente = docente.exists and docente.to_dict().get("activo") is True
    rol = "docente" if es_docente else "estudiante"

    aviso = None
    if rol == "estudiante" and correo.endswith("@usc.edu.co"):
        aviso = (
            "Tu correo es institucional pero no está en la lista de docentes "
            "autorizados, así que quedaste registrado como estudiante."
        )

    # Se guarda el usuario. Los campos de rol y fechas los pone el servidor.
    ahora = datetime.now(timezone.utc)
    usuario = {
        "id_usuario": uid,
        "nombre_completo": datos.nombre_completo.strip(),
        "correo": correo,
        "rol": rol,
        "carrera": datos.carrera,
        "semestre": datos.semestre if rol == "estudiante" else None,
        "acepto_terminos": True,
        "fecha_aceptacion": ahora,
        "fecha_registro": ahora,
    }
    ref.set(usuario)

    return {"usuario": usuario, "aviso": aviso}


@router.get("/usuarios/me", response_model=UsuarioOut)
def mi_perfil(
    usuario: UsuarioActual = Depends(get_usuario_actual), db=Depends(get_db)
):
    """2. Perfil del usuario que inició sesión (ya implementado, sirve de modelo)."""
    doc = db.collection("usuarios").document(usuario.uid).get()
    if not doc.exists:
        raise HTTPException(404, "Usuario no registrado")
    return doc.to_dict()
