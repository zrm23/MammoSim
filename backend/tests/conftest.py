import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.auth import UsuarioActual, get_token_data, get_usuario_actual
from app.firebase import get_db
from app.main import app

CASOS = Path(__file__).resolve().parents[2] / "scripts" / "casos_clinicos.json"


@pytest.fixture(scope="session")
def casos() -> dict:
    """Los 7 casos reales (scripts/casos_clinicos.json)."""
    return json.loads(CASOS.read_text(encoding="utf-8"))


# ---- Base de datos falsa mínima (sin Firebase) ----
class _Doc:
    def __init__(self, id_, data):
        self.id = id_
        self._data = data
        self.exists = data is not None

    def to_dict(self):
        return dict(self._data) if self._data is not None else None


class _Consulta:
    """Lo que devuelve .where(): filtra por igualdad, como Firestore."""

    def __init__(self, docs, filtros=(), limite=None):
        self._docs, self._filtros, self._limite = docs, tuple(filtros), limite

    def where(self, campo=None, op=None, valor=None, *, filter=None):
        if filter is not None:  # FieldFilter de Firestore
            campo, op, valor = filter.field_path, filter.op_string, filter.value
        assert op == "==", "El FakeDb solo entiende filtros de igualdad"
        return _Consulta(self._docs, self._filtros + ((campo, valor),), self._limite)

    def limit(self, n):
        return _Consulta(self._docs, self._filtros, n)

    def stream(self):
        salida = [
            _Doc(id_, d)
            for id_, d in self._docs.items()
            if all(d.get(campo) == valor for campo, valor in self._filtros)
        ]
        return salida[: self._limite] if self._limite else salida


class _Coleccion(_Consulta):
    def __init__(self, docs):
        super().__init__(docs)

    def document(self, id_=None):
        coleccion = self
        if id_ is None:  # ID automático, como en Firestore
            id_ = f"auto_{len(coleccion._docs) + 1}"

        class _Ref:
            id = id_

            def get(self_inner):
                return _Doc(id_, coleccion._docs.get(id_))

            def set(self_inner, datos):
                coleccion._docs[id_] = dict(datos)

        return _Ref()


class FakeDb:
    def __init__(self, datos: dict):
        self._datos = datos

    def collection(self, nombre):
        return _Coleccion(self._datos.setdefault(nombre, {}))


@pytest.fixture
def cliente(casos):
    """Cliente de pruebas; el usuario y la base se ajustan por prueba."""
    estado = {"rol": "estudiante"}
    db = FakeDb(
        {
            "casos_clinicos": casos,
            "usuarios": {
                "uid_1": {
                    "id_usuario": "uid_1", "nombre_completo": "Ana Prueba",
                    "correo": "ana@correo.com", "rol": "estudiante",
                    "carrera": "Medicina", "semestre": 8, "acepto_terminos": True,
                }
            },
        }
    )
    estado["db"] = db
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_token_data] = lambda: {"uid": "uid_1", "email": "ana@correo.com"}
    app.dependency_overrides[get_usuario_actual] = lambda: UsuarioActual(
        uid="uid_1", correo="ana@correo.com", rol=estado["rol"]
    )
    yield TestClient(app), estado
    app.dependency_overrides.clear()
