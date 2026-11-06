"""Pruebas de POST /auth/registro."""
import pytest
from fastapi.testclient import TestClient

from app.auth import get_token_data
from app.firebase import get_db
from app.main import app
from tests.conftest import FakeDb

CUERPO = {
    "nombre_completo": "  Marlin Pérez  ",
    "carrera": "Ingeniería de Sistemas",
    "semestre": 8,
    "acepto_terminos": True,
}


@pytest.fixture
def registro():
    """Cliente con una base vacía y un token que se puede cambiar."""
    db = FakeDb({"docentes_autorizados": {"profe@usc.edu.co": {"activo": True}}})
    token = {"uid": "nuevo_1", "email": "Marlin@Correo.com"}
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_token_data] = lambda: token
    yield TestClient(app), db, token
    app.dependency_overrides.clear()


def guardado(db, uid):
    return db.collection("usuarios").document(uid).get().to_dict()


def test_registra_un_estudiante(registro):
    c, db, _ = registro
    r = c.post("/auth/registro", json=CUERPO)
    assert r.status_code == 201
    usuario = r.json()["usuario"]
    assert usuario["rol"] == "estudiante"
    assert usuario["correo"] == "marlin@correo.com"  # en minúsculas
    assert usuario["nombre_completo"] == "Marlin Pérez"  # sin espacios sobrantes
    assert r.json()["aviso"] is None
    guardado_ = guardado(db, "nuevo_1")
    assert guardado_["acepto_terminos"] is True
    assert guardado_["fecha_registro"] and guardado_["fecha_aceptacion"]


def test_sin_aceptar_terminos_da_422_y_no_guarda(registro):
    c, db, _ = registro
    r = c.post("/auth/registro", json={**CUERPO, "acepto_terminos": False})
    assert r.status_code == 422
    assert guardado(db, "nuevo_1") is None


def test_si_ya_existe_da_409_y_no_lo_pisa(registro):
    c, db, _ = registro
    assert c.post("/auth/registro", json=CUERPO).status_code == 201
    r = c.post("/auth/registro", json={**CUERPO, "carrera": "Otra"})
    assert r.status_code == 409
    assert guardado(db, "nuevo_1")["carrera"] == "Ingeniería de Sistemas"


def test_correo_de_docente_autorizado_queda_docente(registro):
    c, db, token = registro
    token.update(uid="doc_1", email="Profe@usc.edu.co")
    r = c.post("/auth/registro", json=CUERPO)
    assert r.status_code == 201
    assert r.json()["usuario"]["rol"] == "docente"
    assert r.json()["usuario"]["semestre"] is None  # el semestre es solo de estudiantes


def test_docente_inactivo_queda_estudiante(registro):
    c, db, token = registro
    db.collection("docentes_autorizados").document("baja@usc.edu.co").set({"activo": False})
    token.update(uid="x", email="baja@usc.edu.co")
    r = c.post("/auth/registro", json=CUERPO)
    assert r.json()["usuario"]["rol"] == "estudiante"


def test_correo_institucional_no_autorizado_da_aviso(registro):
    c, db, token = registro
    token.update(uid="x", email="otro@usc.edu.co")
    r = c.post("/auth/registro", json=CUERPO)
    assert r.json()["usuario"]["rol"] == "estudiante"
    assert r.json()["aviso"]


def test_no_se_puede_pedir_rol_docente_en_el_cuerpo(registro):
    c, db, _ = registro
    r = c.post("/auth/registro", json={**CUERPO, "rol": "docente"})
    assert r.json()["usuario"]["rol"] == "estudiante"


def test_token_sin_correo_da_422(registro):
    c, db, token = registro
    token.pop("email")
    assert c.post("/auth/registro", json=CUERPO).status_code == 422
