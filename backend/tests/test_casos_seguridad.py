"""Pruebas de seguridad de GET /casos y GET /usuarios/me.

Regla de la guía (sección 6): ningún caso entrega respuestas antes de tiempo
y solo sale lo que está en la lista blanca de services/casos.py.
"""
from fastapi.testclient import TestClient

from app.auth import UsuarioActual, get_usuario_actual
from app.main import app
from app.services.casos import resumen_caso

# Lista blanca esperada, escrita a mano (no importada) para que la prueba
# falle si alguien agrega un campo al resumen sin pensarlo.
CAMPOS_RESUMEN = {
    "id_caso", "titulo", "descripcion_breve", "lado",
    "vistas", "dificultad", "modelo_3d_ref",
}
CAMPOS_PRIVADOS = {
    "respuesta_correcta", "explicacion", "opcion_ia_incorrecta",
    "recomendacion_ia_correcta", "recomendacion_ia_incorrecta",
    "hallazgos", "retroalimentacion", "preguntas",
}


def _claves(obj):
    """Todos los nombres de campo que aparecen en el objeto, a cualquier nivel."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from _claves(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _claves(v)


# ---------- GET /casos ----------
def test_casos_sin_token_responde_401():
    assert TestClient(app).get("/casos").status_code == 401


def test_casos_cada_item_trae_solo_la_lista_blanca(cliente):
    c, _ = cliente
    for caso in c.get("/casos").json():
        assert set(caso) == CAMPOS_RESUMEN


def test_casos_no_filtra_campos_privados_a_ningun_nivel(cliente):
    c, _ = cliente
    assert not set(_claves(c.get("/casos").json())) & CAMPOS_PRIVADOS


def test_casos_devuelve_los_7_ordenados_y_sin_repetir(cliente):
    c, _ = cliente
    ids = [caso["id_caso"] for caso in c.get("/casos").json()]
    assert ids == sorted(ids)
    assert ids == [f"caso_00{n}" for n in range(1, 8)]


def test_casos_usuario_sin_registrar_responde_403(cliente):
    c, _ = cliente
    app.dependency_overrides[get_usuario_actual] = lambda: UsuarioActual(
        uid="uid_sin_registro", correo="nadie@correo.com", rol=None
    )
    r = c.get("/casos")
    assert r.status_code == 403
    assert r.json()["detail"] == "Primero debes registrarte"


def test_casos_un_campo_nuevo_en_firestore_no_se_filtra(casos):
    caso = {**casos["caso_001"], "campo_nuevo_secreto": "x"}
    assert "campo_nuevo_secreto" not in resumen_caso(caso)


def test_casos_lo_puede_ver_un_docente(cliente):
    c, estado = cliente
    estado["rol"] = "docente"
    assert c.get("/casos").status_code == 200


# ---------- GET /usuarios/me ----------
def test_perfil_sin_token_responde_401():
    assert TestClient(app).get("/usuarios/me").status_code == 401


def test_perfil_devuelve_solo_los_campos_del_esquema(cliente):
    c, _ = cliente
    assert set(c.get("/usuarios/me").json()) == {
        "id_usuario", "nombre_completo", "correo", "rol",
        "carrera", "semestre", "acepto_terminos",
    }


def test_perfil_de_usuario_no_registrado_responde_404(cliente):
    c, _ = cliente
    app.dependency_overrides[get_usuario_actual] = lambda: UsuarioActual(
        uid="uid_sin_registro", correo="nadie@correo.com", rol=None
    )
    assert c.get("/usuarios/me").status_code == 404