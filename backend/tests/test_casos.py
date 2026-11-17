"""Lo que sale al cliente NUNCA debe revelar la respuesta."""
from app.services.casos import caso_para_resolver, feedback_pregunta, pregunta_de, resumen_caso

PRIVADOS = (
    "respuesta_correcta", "explicacion", "opcion_ia_incorrecta",
    "recomendacion_ia_correcta", "recomendacion_ia_incorrecta",
    "hallazgos", "retroalimentacion",
)


def _claves(obj):
    """Todos los nombres de campo que aparecen en el objeto, a cualquier nivel."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from _claves(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _claves(v)


def test_caso_para_resolver_no_filtra_nada_secreto(casos):
    for caso in casos.values():
        claves = set(_claves(caso_para_resolver(caso)))
        assert not claves & set(PRIVADOS), f"{caso['id_caso']} filtra {claves & set(PRIVADOS)}"


def test_caso_para_resolver_conserva_lo_necesario(casos):
    c = caso_para_resolver(casos["caso_001"])
    assert len(c["preguntas"]) == 7
    assert set(c["preguntas"][0]) == {"numero", "enunciado", "opciones"}
    assert len(c["opciones_decision"]) == 4 and c["enunciado_decision"]


def test_resumen_no_trae_preguntas(casos):
    assert "preguntas" not in resumen_caso(casos["caso_001"])


def test_feedback_pregunta_correcta(casos):
    p = pregunta_de(casos["caso_001"], 1)
    r = feedback_pregunta(p, p["respuesta_correcta"])
    assert r["correcta"] is True
    assert r["mensaje"].startswith("Correcto.") and p["explicacion"] in r["mensaje"]


def test_feedback_pregunta_incorrecta_dice_cual_era(casos):
    p = pregunta_de(casos["caso_001"], 1)
    mala = next(l for l in "ABCD" if l != p["respuesta_correcta"])
    r = feedback_pregunta(p, mala)
    assert r["correcta"] is False
    assert r["mensaje"].startswith("Incorrecto.")
    assert p["opciones"][p["respuesta_correcta"]] in r["mensaje"]
    assert p["explicacion"] in r["mensaje"]
