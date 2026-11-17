"""Endpoints 13 a 17: lo que pasa DENTRO de un caso.

Todas las rutas exigen: la sesión es del estudiante, está en_curso y el caso
está en casos_asignados. Orden que el servidor hace cumplir:
  1. 7 respuestas  ->  2. decisión inicial  ->  3. recomendación IA
  ->  4. decisión final  ->  5. retroalimentación.
Los documentos se crean una sola vez (repetir = 409).
"""
from fastapi import APIRouter, Depends

from app.auth import UsuarioActual, requiere_estudiante
from app.firebase import get_db
from app.schemas import (
    DecisionIn,
    GuardadaOut,
    RecomendacionOut,
    RespuestaIn,
    RespuestaOut,
    RetroalimentacionOut,
)
from app.utils import pendiente

router = APIRouter(prefix="/sesiones/{id_sesion}/casos/{id_caso}", tags=["dentro de un caso"])


@router.post("/respuestas", response_model=RespuestaOut, status_code=201)
def responder_pregunta(
    id_sesion: str,
    id_caso: str,
    datos: RespuestaIn,
    estudiante: UsuarioActual = Depends(requiere_estudiante),
    db=Depends(get_db),
):
    """13. TODO: crear respuestas/{id_sesion}_{id_caso}_p{n} (409 si ya existe) y
    devolver services.casos.feedback_pregunta(...) para mostrarlo de inmediato."""
    pendiente()


@router.post("/decision-inicial", response_model=GuardadaOut, status_code=201)
def decision_inicial(
    id_sesion: str,
    id_caso: str,
    datos: DecisionIn,
    estudiante: UsuarioActual = Depends(requiere_estudiante),
    db=Depends(get_db),
):
    """14. TODO: 409 si faltan las 7 respuestas; crear decisiones_iniciales con
    acierto calculado. NO decir si acertó."""
    pendiente()


@router.get("/recomendacion-ia", response_model=RecomendacionOut)
def recomendacion_ia(
    id_sesion: str,
    id_caso: str,
    estudiante: UsuarioActual = Depends(requiere_estudiante),
    db=Depends(get_db),
):
    """15. TODO: 409 si no hay decisión inicial; usar services.tutor.recomendar.
    Devolver solo opcion_ia y texto (nunca ia_correcta). No escribe nada."""
    pendiente()


@router.post("/decision-final", response_model=GuardadaOut, status_code=201)
def decision_final(
    id_sesion: str,
    id_caso: str,
    datos: DecisionIn,
    estudiante: UsuarioActual = Depends(requiere_estudiante),
    db=Depends(get_db),
):
    """16. TODO: 409 si no hay decisión inicial; crear decisiones_finales con
    services.tutor.evaluar_decision_final (se guarda siempre, aunque no cambie)."""
    pendiente()


@router.get("/retroalimentacion", response_model=RetroalimentacionOut)
def retroalimentacion(
    id_sesion: str,
    id_caso: str,
    estudiante: UsuarioActual = Depends(requiere_estudiante),
    db=Depends(get_db),
):
    """17. TODO: 409 si no hay decisión final; devolver hallazgos,
    retroalimentacion, respuesta_correcta y la nota (services.puntuacion.nota_caso)."""
    pendiente()
