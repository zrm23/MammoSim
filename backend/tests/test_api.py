import json

import pytest
from fastapi.testclient import TestClient

from app.main import app

# (método, ruta) de los 21 endpoints
RUTAS = {
    ("POST", "/auth/registro"), ("GET", "/usuarios/me"),
    ("POST", "/cursos"), ("GET", "/cursos/mio"), ("POST", "/inscripciones"),
    ("DELETE", "/inscripciones/{id_curso}"), ("GET", "/inscripciones/mias"),
    ("GET", "/casos"), ("GET", "/casos/{id_caso}"),
    ("POST", "/sesiones"), ("GET", "/sesiones/mias"), ("GET", "/sesiones/activa"),
    ("POST", "/sesiones/{id_sesion}/cerrar"), ("GET", "/sesiones/{id_sesion}/resultado"),
    ("POST", "/sesiones/{id_sesion}/casos/{id_caso}/respuestas"),
    ("POST", "/sesiones/{id_sesion}/casos/{id_caso}/decision-inicial"),
    ("GET", "/sesiones/{id_sesion}/casos/{id_caso}/recomendacion-ia"),
    ("POST", "/sesiones/{id_sesion}/casos/{id_caso}/decision-final"),
    ("GET", "/sesiones/{id_sesion}/casos/{id_caso}/retroalimentacion"),
    ("GET", "/cursos/mio/sesiones"), ("GET", "/cursos/mio/sesiones/{id_sesion}"),
}


def test_estan_los_21_endpoints():
    publicados = {
        (metodo.upper(), ruta)
        for ruta, metodos in app.openapi()["paths"].items()
        for metodo in metodos
        if ruta != "/salud"
    }
    assert publicados == RUTAS and len(RUTAS) == 21


def test_salud():
    assert TestClient(app).get("/salud").json() == {"estado": "ok"}


def test_sin_token_responde_401():
    assert TestClient(app).get("/casos").status_code == 401


def test_listar_casos_no_revela_respuestas(cliente):
    c, _ = cliente
    r = c.get("/casos")
    assert r.status_code == 200 and len(r.json()) == 7
    assert "respuesta_correcta" not in json.dumps(r.json())


def test_mi_perfil(cliente):
    c, _ = cliente
    assert c.get("/usuarios/me").json()["nombre_completo"] == "Ana Prueba"


def test_un_estudiante_no_entra_a_rutas_de_docente(cliente):
    c, _ = cliente
    assert c.get("/cursos/mio").status_code == 403


def test_un_docente_no_entra_a_rutas_de_estudiante(cliente):
    c, estado = cliente
    estado["rol"] = "docente"
    assert c.get("/sesiones/activa").status_code == 403


def test_lo_pendiente_responde_501(cliente):
    c, _ = cliente
    r = c.post("/sesiones/s1/cerrar")
    assert r.status_code == 501


def test_valida_el_cuerpo(cliente):
    c, _ = cliente
    assert c.post("/sesiones", json={"casos": []}).status_code == 422
    r = c.post("/sesiones/s1/casos/caso_001/respuestas",
               json={"numero_pregunta": 9, "opcion_elegida": "A"})
    assert r.status_code == 422
