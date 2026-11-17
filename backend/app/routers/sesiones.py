"""Endpoints 10, 11, 12, 18 y 21: sesiones y resultados.

MODO EXAMEN: una vez que el estudiante empieza una sesión no puede salirse
ni repetirla. Solo puede haber una sesión en_curso por estudiante y no se
puede cerrar a medias.
"""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from google.cloud.firestore_v1.base_query import FieldFilter

from app.auth import UsuarioActual, requiere_estudiante
from app.firebase import get_db
from app.schemas import ResultadoOut, SesionActivaOut, SesionIn, SesionOut
from app.utils import pendiente

router = APIRouter(tags=["sesiones"])


def _sesion_en_curso(db, uid):
    """Devuelve el documento de la sesión en_curso del estudiante, o None."""
    docs = (
        db.collection("sesiones")
        .where(filter=FieldFilter("id_usuario", "==", uid))
        .where(filter=FieldFilter("estado", "==", "en_curso"))
        .limit(1)
        .stream()
    )
    for doc in docs:
        return doc
    return None


@router.post("/sesiones", response_model=SesionOut, status_code=201)
def crear_sesion(
    datos: SesionIn,
    estudiante: UsuarioActual = Depends(requiere_estudiante),
    db=Depends(get_db),
):
    """10. Abre una sesión de examen (modo examen: una sola en curso a la vez)."""
    # Validaciones: si algo no cumple, se corta aquí con un código de error.
    if len(set(datos.casos)) != len(datos.casos):
        raise HTTPException(422, "No repitas casos en la sesión")

    if _sesion_en_curso(db, estudiante.uid) is not None:
        raise HTTPException(409, "Ya tienes una sesión en curso")

    # Si la sesión es de un curso, el estudiante debe estar inscrito (activo).
    if datos.id_curso is not None:
        inscripcion = (
            db.collection("inscripciones")
            .document(f"{estudiante.uid}_{datos.id_curso}")
            .get()
        )
        if not inscripcion.exists or inscripcion.to_dict().get("activo") is not True:
            raise HTTPException(403, "No estás inscrito en ese curso")

    for id_caso in datos.casos:
        if not db.collection("casos_clinicos").document(id_caso).get().exists:
            raise HTTPException(404, f"El caso {id_caso} no existe")

    # Se guarda la sesión; el ID lo genera Firestore y se copia dentro del documento.
    ref = db.collection("sesiones").document()
    sesion = {
        "id_sesion": ref.id,
        "id_usuario": estudiante.uid,
        "id_curso": datos.id_curso,
        "casos_asignados": datos.casos,
        "estado": "en_curso",
        "fecha_inicio": datetime.now(timezone.utc),
        "fecha_fin": None,
    }
    ref.set(sesion)
    return sesion


# OJO: estas dos rutas fijas van ANTES de las que llevan {id_sesion}.
@router.get("/sesiones/mias", response_model=list[SesionOut])
def mis_sesiones(
    id_curso: str | None = None,
    estudiante: UsuarioActual = Depends(requiere_estudiante),
    db=Depends(get_db),
):
    """11. Historial del estudiante, de la más reciente a la más antigua.
    Incluye las prácticas libres; con ?id_curso= se filtra por un curso."""
    consulta = db.collection("sesiones").where(
        filter=FieldFilter("id_usuario", "==", estudiante.uid)
    )
    if id_curso is not None:
        consulta = consulta.where(filter=FieldFilter("id_curso", "==", id_curso))
    sesiones = [doc.to_dict() for doc in consulta.stream()]
    # Un estudiante tiene pocas sesiones: se ordena aquí y no hace falta índice.
    return sorted(sesiones, key=lambda s: s["fecha_inicio"], reverse=True)


@router.get("/sesiones/activa", response_model=SesionActivaOut)
def sesion_activa(
    estudiante: UsuarioActual = Depends(requiere_estudiante), db=Depends(get_db)
):
    """21. La sesión en_curso, con los casos ya terminados y el caso donde va,
    para continuar la misma si cerró la ventana. 404 si no tiene."""
    doc = _sesion_en_curso(db, estudiante.uid)
    if doc is None:
        raise HTTPException(404, "No tienes una sesión en curso")
    sesion = doc.to_dict()

    # Un caso está terminado cuando ya existe su decisión final.
    terminados = [
        id_caso
        for id_caso in sesion["casos_asignados"]
        if db.collection("decisiones_finales")
        .document(f"{sesion['id_sesion']}_{id_caso}")
        .get()
        .exists
    ]
    pendientes = [c for c in sesion["casos_asignados"] if c not in terminados]
    sesion["casos_terminados"] = terminados
    sesion["caso_actual"] = pendientes[0] if pendientes else None
    return sesion


@router.post("/sesiones/{id_sesion}/cerrar", response_model=ResultadoOut)
def cerrar_sesion(
    id_sesion: str,
    estudiante: UsuarioActual = Depends(requiere_estudiante),
    db=Depends(get_db),
):
    """12. TODO:
    - 403 si la sesión no es suya.
    - 409 si ya está completada o si falta terminar algún caso.
    - estado='completada', fecha_fin; crear resultados/{id_sesion} usando
      services.puntuacion.puntuacion_sesion."""
    pendiente()


@router.get("/sesiones/{id_sesion}/resultado", response_model=ResultadoOut)
def ver_resultado(
    id_sesion: str,
    estudiante: UsuarioActual = Depends(requiere_estudiante),
    db=Depends(get_db),
):
    """18. TODO: resultados/{id_sesion}; 409 si la sesión no está completada."""
    pendiente()
