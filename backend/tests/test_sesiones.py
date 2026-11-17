"""Pruebas de POST /sesiones, GET /sesiones/mias y GET /sesiones/activa."""
from datetime import datetime, timedelta, timezone


def guarda(db, coleccion, id_, datos):
    db.collection(coleccion).document(id_).set(datos)


def sesion(id_, estado="en_curso", dias=0, id_curso=None, casos=("caso_001",)):
    return {
        "id_sesion": id_, "id_usuario": "uid_1", "id_curso": id_curso,
        "casos_asignados": list(casos), "estado": estado,
        "fecha_inicio": datetime(2026, 11, 1, tzinfo=timezone.utc) + timedelta(days=dias),
        "fecha_fin": None,
    }


# ---------- POST /sesiones ----------
def test_crea_una_sesion_de_practica_libre(cliente):
    c, estado = cliente
    r = c.post("/sesiones", json={"id_curso": None, "casos": ["caso_001", "caso_002"]})
    assert r.status_code == 201
    s = r.json()
    assert s["estado"] == "en_curso"
    assert s["id_usuario"] == "uid_1"
    assert s["casos_asignados"] == ["caso_001", "caso_002"]
    assert s["id_curso"] is None and s["fecha_fin"] is None
    # quedó guardada con el mismo ID que se devolvió
    assert estado["db"].collection("sesiones").document(s["id_sesion"]).get().exists


def test_segunda_sesion_en_curso_da_409(cliente):
    c, estado = cliente
    guarda(estado["db"], "sesiones", "s1", sesion("s1"))
    r = c.post("/sesiones", json={"casos": ["caso_001"]})
    assert r.status_code == 409


def test_se_puede_abrir_otra_si_la_anterior_esta_completada(cliente):
    c, estado = cliente
    guarda(estado["db"], "sesiones", "s1", sesion("s1", estado="completada"))
    assert c.post("/sesiones", json={"casos": ["caso_001"]}).status_code == 201


def test_caso_que_no_existe_da_404_y_no_guarda(cliente):
    c, estado = cliente
    r = c.post("/sesiones", json={"casos": ["caso_001", "caso_999"]})
    assert r.status_code == 404
    assert c.get("/sesiones/activa").status_code == 404


def test_casos_repetidos_dan_422(cliente):
    c, _ = cliente
    r = c.post("/sesiones", json={"casos": ["caso_001", "caso_001"]})
    assert r.status_code == 422


def test_sin_casos_da_422(cliente):
    c, _ = cliente
    assert c.post("/sesiones", json={"casos": []}).status_code == 422


def test_con_curso_exige_inscripcion_activa(cliente):
    c, estado = cliente
    db = estado["db"]
    # sin inscripción
    r = c.post("/sesiones", json={"id_curso": "cur1", "casos": ["caso_001"]})
    assert r.status_code == 403
    # inscripción dada de baja
    guarda(db, "inscripciones", "uid_1_cur1", {"activo": False})
    r = c.post("/sesiones", json={"id_curso": "cur1", "casos": ["caso_001"]})
    assert r.status_code == 403
    # inscripción activa
    guarda(db, "inscripciones", "uid_1_cur1", {"activo": True})
    r = c.post("/sesiones", json={"id_curso": "cur1", "casos": ["caso_001"]})
    assert r.status_code == 201
    assert r.json()["id_curso"] == "cur1"


def test_un_docente_no_puede_abrir_sesiones(cliente):
    c, estado = cliente
    estado["rol"] = "docente"
    assert c.post("/sesiones", json={"casos": ["caso_001"]}).status_code == 403


# ---------- GET /sesiones/mias ----------
def test_mis_sesiones_de_la_mas_reciente_a_la_mas_antigua(cliente):
    c, estado = cliente
    db = estado["db"]
    guarda(db, "sesiones", "vieja", sesion("vieja", estado="completada", dias=0))
    guarda(db, "sesiones", "nueva", sesion("nueva", estado="completada", dias=5))
    guarda(db, "sesiones", "media", sesion("media", estado="completada", dias=2))
    r = c.get("/sesiones/mias")
    assert r.status_code == 200
    assert [s["id_sesion"] for s in r.json()] == ["nueva", "media", "vieja"]


def test_mis_sesiones_no_incluye_las_de_otros(cliente):
    c, estado = cliente
    ajena = sesion("ajena")
    ajena["id_usuario"] = "otro"
    guarda(estado["db"], "sesiones", "ajena", ajena)
    assert c.get("/sesiones/mias").json() == []


def test_mis_sesiones_filtra_por_curso(cliente):
    c, estado = cliente
    db = estado["db"]
    guarda(db, "sesiones", "a", sesion("a", estado="completada", id_curso="cur1"))
    guarda(db, "sesiones", "b", sesion("b", estado="completada", id_curso=None))
    r = c.get("/sesiones/mias", params={"id_curso": "cur1"})
    assert [s["id_sesion"] for s in r.json()] == ["a"]
    # sin filtro salen ambas (la práctica libre también)
    assert len(c.get("/sesiones/mias").json()) == 2


# ---------- GET /sesiones/activa ----------
def test_sin_sesion_en_curso_da_404(cliente):
    c, _ = cliente
    assert c.get("/sesiones/activa").status_code == 404


def test_sesion_activa_empieza_en_el_primer_caso(cliente):
    c, estado = cliente
    guarda(estado["db"], "sesiones", "s1",
           sesion("s1", casos=("caso_001", "caso_002", "caso_003")))
    r = c.get("/sesiones/activa")
    assert r.status_code == 200
    s = r.json()
    assert s["id_sesion"] == "s1"
    assert s["casos_terminados"] == []
    assert s["caso_actual"] == "caso_001"


def test_sesion_activa_sabe_donde_va(cliente):
    c, estado = cliente
    db = estado["db"]
    guarda(db, "sesiones", "s1",
           sesion("s1", casos=("caso_001", "caso_002", "caso_003")))
    guarda(db, "decisiones_finales", "s1_caso_001", {"id_sesion": "s1"})
    s = c.get("/sesiones/activa").json()
    assert s["casos_terminados"] == ["caso_001"]
    assert s["caso_actual"] == "caso_002"


def test_sesion_activa_con_todos_los_casos_terminados(cliente):
    c, estado = cliente
    db = estado["db"]
    guarda(db, "sesiones", "s1", sesion("s1", casos=("caso_001",)))
    guarda(db, "decisiones_finales", "s1_caso_001", {"id_sesion": "s1"})
    s = c.get("/sesiones/activa").json()
    assert s["casos_terminados"] == ["caso_001"]
    assert s["caso_actual"] is None


def test_sesion_activa_ignora_las_completadas_y_las_ajenas(cliente):
    c, estado = cliente
    db = estado["db"]
    guarda(db, "sesiones", "vieja", sesion("vieja", estado="completada"))
    ajena = sesion("ajena")
    ajena["id_usuario"] = "otro"
    guarda(db, "sesiones", "ajena", ajena)
    assert c.get("/sesiones/activa").status_code == 404
