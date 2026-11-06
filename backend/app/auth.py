"""Autenticación: verifica el token de Firebase y el rol del usuario.

El cliente manda el encabezado  Authorization: Bearer <token>.
El uid y el correo salen SIEMPRE del token verificado, nunca del cuerpo
de la petición, para que nadie pueda hacerse pasar por otro usuario.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth as fb_auth
from pydantic import BaseModel

from app.firebase import get_db, init_firebase

bearer = HTTPBearer(auto_error=False)


class UsuarioActual(BaseModel):
    uid: str
    correo: str
    rol: str | None  # None = tiene cuenta en Firebase pero aún no se registró


def get_token_data(
    cred: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> dict:
    """Verifica el token. Úsalo solo en el registro (el usuario aún no existe)."""
    if cred is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Falta el token")
    try:
        init_firebase()
        return fb_auth.verify_id_token(cred.credentials)
    except Exception:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token inválido o vencido")


def get_usuario_actual(
    token: dict = Depends(get_token_data), db=Depends(get_db)
) -> UsuarioActual:
    """Usuario que hace la petición, con su rol leído de la colección usuarios."""
    doc = db.collection("usuarios").document(token["uid"]).get()
    rol = doc.to_dict().get("rol") if doc.exists else None
    return UsuarioActual(
        uid=token["uid"], correo=(token.get("email") or "").lower(), rol=rol
    )


def requiere_rol(rol: str):
    """Dependencia que exige un rol: Depends(requiere_rol("docente"))."""

    def verificar(usuario: UsuarioActual = Depends(get_usuario_actual)) -> UsuarioActual:
        if usuario.rol != rol:
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"Solo para {rol}")
        return usuario

    return verificar


def requiere_registrado(
    usuario: UsuarioActual = Depends(get_usuario_actual),
) -> UsuarioActual:
    """Cualquier rol, pero la persona debe haberse registrado (rol distinto de None)."""
    if usuario.rol is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Primero debes registrarte")
    return usuario


requiere_estudiante = requiere_rol("estudiante")
requiere_docente = requiere_rol("docente")
