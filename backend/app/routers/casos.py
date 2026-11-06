"""Endpoints 8 y 9: casos clínicos."""
from fastapi import APIRouter, Depends

from app.auth import UsuarioActual, get_usuario_actual, requiere_registrado
from app.firebase import get_db
from app.schemas import CasoResumen
from app.services.casos import resumen_caso
from app.utils import pendiente

router = APIRouter(tags=["casos"])


@router.get("/casos", response_model=list[CasoResumen])
def listar_casos(
    usuario: UsuarioActual = Depends(requiere_registrado), db=Depends(get_db)
):
    """8. Lista de casos sin ningún campo que revele la respuesta.
    Cualquier rol, pero exige estar registrado (403 si no)."""
    docs = db.collection("casos_clinicos").stream()
    casos = [resumen_caso(d.to_dict()) for d in docs]
    return sorted(casos, key=lambda c: c["id_caso"])


@router.get("/casos/{id_caso}")
def ver_caso(
    id_caso: str,
    usuario: UsuarioActual = Depends(get_usuario_actual),
    db=Depends(get_db),
):
    """9. TODO: devolver caso_para_resolver(caso) SOLO si el caso está en una
    sesión en_curso del estudiante (403 si no); 404 si no existe.
    Sin esa comprobación se podrían leer las preguntas fuera del examen."""
    pendiente()
