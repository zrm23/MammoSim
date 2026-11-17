"""Endpoints 3 a 7 (cursos e inscripciones) y 19 y 20 (vista del docente)."""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from google.cloud.firestore_v1.base_query import FieldFilter

from app.auth import UsuarioActual, requiere_docente, requiere_estudiante
from app.firebase import get_db
from app.schemas import CursoIn, CursoOut, InscripcionIn
from app.services.cursos import generar_codigo
from app.utils import pendiente

router = APIRouter(tags=["cursos"])


def _curso_del_docente(db, uid):
    """El único curso del docente (o None). Un docente tiene un solo curso."""
    consulta = db.collection("cursos").where(filter=FieldFilter("id_docente", "==", uid))
    for doc in consulta.limit(1).stream():
        return doc
    return None


def _a_curso_out(doc) -> dict:
    """El ID del curso es el del documento, no un campo guardado."""
    datos = doc.to_dict()
    return {
        "id_curso": doc.id,
        "codigo": datos["codigo"],
        "nombre": datos["nombre"],
        "id_docente": datos["id_docente"],
    }


@router.post("/cursos", response_model=CursoOut, status_code=201)
def crear_curso(
    datos: CursoIn, docente: UsuarioActual = Depends(requiere_docente), db=Depends(get_db)
):
    """3. Crea el curso del docente con un código único generado por el servidor."""
    if _curso_del_docente(db, docente.uid) is not None:
        raise HTTPException(409, "Ya tienes un curso creado")

    # El código lo genera el servidor; se repite si ya lo tiene otro curso.
    for _ in range(10):
        codigo = generar_codigo()
        repetido = db.collection("cursos").where(filter=FieldFilter("codigo", "==", codigo))
        if not list(repetido.limit(1).stream()):
            break
    else:
        raise HTTPException(500, "No se pudo generar un código único, intenta de nuevo")

    ref = db.collection("cursos").document()  # ID automático
    ref.set(
        {
            "codigo": codigo,
            "nombre": datos.nombre.strip(),
            "id_docente": docente.uid,
            "fecha_creacion": datetime.now(timezone.utc),
        }
    )
    return _a_curso_out(ref.get())


@router.get("/cursos/mio", response_model=CursoOut)
def mi_curso(docente: UsuarioActual = Depends(requiere_docente), db=Depends(get_db)):
    """4. El curso del docente que hace la petición."""
    doc = _curso_del_docente(db, docente.uid)
    if doc is None:
        raise HTTPException(404, "Todavía no tienes un curso")
    return _a_curso_out(doc)


@router.post("/inscripciones", response_model=CursoOut)
def unirse_a_curso(
    datos: InscripcionIn,
    estudiante: UsuarioActual = Depends(requiere_estudiante),
    db=Depends(get_db),
):
    """5. TODO: buscar el curso por codigo (404); crear o reactivar
    inscripciones/{uid}_{id_curso} con activo=True."""
    pendiente()


@router.delete("/inscripciones/{id_curso}", status_code=204)
def salirse_del_curso(
    id_curso: str,
    estudiante: UsuarioActual = Depends(requiere_estudiante),
    db=Depends(get_db),
):
    """6. TODO: activo=False (el historial se conserva); 404 si no estaba inscrito."""
    pendiente()


@router.get("/inscripciones/mias", response_model=list[CursoOut])
def mis_cursos(
    estudiante: UsuarioActual = Depends(requiere_estudiante), db=Depends(get_db)
):
    """7. TODO: cursos donde la inscripción esté activa."""
    pendiente()


@router.get("/cursos/mio/sesiones")
def sesiones_de_mi_curso(
    docente: UsuarioActual = Depends(requiere_docente), db=Depends(get_db)
):
    """19. TODO: sesiones con id_curso == el de su curso, con nombre del estudiante,
    estado, fecha_inicio y puntuacion. Puede pedir índice (id_curso + fecha_inicio)."""
    pendiente()


@router.get("/cursos/mio/sesiones/{id_sesion}")
def detalle_de_sesion(
    id_sesion: str,
    docente: UsuarioActual = Depends(requiere_docente),
    db=Depends(get_db),
):
    """20. TODO: respuestas, decisiones inicial y final, siguio_ia y nota de cada
    caso. 404 si la sesión no es de su curso."""
    pendiente()
