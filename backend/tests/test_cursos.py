"""Pruebas de POST /cursos y GET /cursos/mio."""
import re

from app.services.cursos import generar_codigo

CODIGO = re.compile(r"^MS-[A-Z2-9]{6}$")


def como_docente(estado):
    estado["rol"] = "docente"


def test_el_codigo_tiene_el_formato_y_es_distinto_cada_vez():
    codigos = {generar_codigo() for _ in range(200)}
    assert len(codigos) == 200
    assert all(CODIGO.match(c) for c in codigos)


def test_el_docente_crea_su_curso(cliente):
    c, estado = cliente
    como_docente(estado)
    r = c.post("/cursos", json={"nombre": "  Gestión de Proyectos de TI  "})
    assert r.status_code == 201
    curso = r.json()
    assert CODIGO.match(curso["codigo"])
    assert curso["nombre"] == "Gestión de Proyectos de TI"  # sin espacios sobrantes
    assert curso["id_docente"] == "uid_1"  # sale del token, no del cuerpo
    guardado = estado["db"].collection("cursos").document(curso["id_curso"]).get()
    assert guardado.exists and guardado.to_dict()["fecha_creacion"]


def test_un_estudiante_no_puede_crear_cursos(cliente):
    c, estado = cliente  # el rol por defecto es estudiante
    assert c.post("/cursos", json={"nombre": "Mi curso"}).status_code == 403


def test_un_docente_no_puede_tener_dos_cursos(cliente):
    c, estado = cliente
    como_docente(estado)
    assert c.post("/cursos", json={"nombre": "Primero"}).status_code == 201
    assert c.post("/cursos", json={"nombre": "Segundo"}).status_code == 409
    assert len(estado["db"].collection("cursos").stream()) == 1


def test_el_nombre_muy_corto_da_422(cliente):
    c, estado = cliente
    como_docente(estado)
    assert c.post("/cursos", json={"nombre": "A"}).status_code == 422


def test_ver_mi_curso(cliente):
    c, estado = cliente
    como_docente(estado)
    creado = c.post("/cursos", json={"nombre": "Mi curso"}).json()
    r = c.get("/cursos/mio")
    assert r.status_code == 200 and r.json() == creado


def test_sin_curso_da_404(cliente):
    c, estado = cliente
    como_docente(estado)
    assert c.get("/cursos/mio").status_code == 404


def test_no_ve_el_curso_de_otro_docente(cliente):
    c, estado = cliente
    como_docente(estado)
    estado["db"].collection("cursos").document("ajeno").set(
        {"codigo": "MS-AAAAAA", "nombre": "De otro", "id_docente": "otro_docente"}
    )
    assert c.get("/cursos/mio").status_code == 404


def test_un_estudiante_no_ve_cursos_mio(cliente):
    c, _ = cliente
    assert c.get("/cursos/mio").status_code == 403
