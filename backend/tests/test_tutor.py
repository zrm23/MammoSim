"""El tutor (opción A) debe seguir la regla acordada en los 7 casos."""
import pytest

from app.services.tutor import evaluar_decision_final, recomendar

OPCIONES = ["biopsiar", "seguimiento", "ignorar", "estudio_adicional"]


def test_si_acerto_la_ia_defiende_la_opcion_incorrecta_fija(casos):
    for caso in casos.values():
        rec = recomendar(caso, caso["respuesta_correcta"])
        assert rec["opcion_ia"] == caso["opcion_ia_incorrecta"]
        assert rec["opcion_ia"] != caso["respuesta_correcta"]
        assert rec["texto"] == caso["recomendacion_ia_incorrecta"]
        assert rec["ia_correcta"] is False


def test_si_fallo_la_ia_recomienda_la_correcta(casos):
    for caso in casos.values():
        for mala in (o for o in OPCIONES if o != caso["respuesta_correcta"]):
            rec = recomendar(caso, mala)
            assert rec["opcion_ia"] == caso["respuesta_correcta"]
            assert rec["texto"] == caso["recomendacion_ia_correcta"]
            assert rec["ia_correcta"] is True


def test_acierta_y_mantiene_su_decision(casos):
    caso = casos["caso_001"]
    r = evaluar_decision_final(caso, caso["respuesta_correcta"], caso["respuesta_correcta"])
    assert r["acierto"] is True and r["siguio_ia"] is False and r["ia_correcta"] is False


def test_acierta_y_se_deja_llevar_por_la_ia_incorrecta(casos):
    caso = casos["caso_001"]
    r = evaluar_decision_final(caso, caso["respuesta_correcta"], caso["opcion_ia_incorrecta"])
    assert r["acierto"] is False and r["siguio_ia"] is True and r["ia_correcta"] is False


def test_falla_y_la_ia_lo_corrige(casos):
    caso = casos["caso_001"]
    mala = "ignorar" if caso["respuesta_correcta"] != "ignorar" else "seguimiento"
    r = evaluar_decision_final(caso, mala, caso["respuesta_correcta"])
    assert r["acierto"] is True and r["siguio_ia"] is True and r["ia_correcta"] is True


def test_falla_y_no_hace_caso_a_la_ia(casos):
    caso = casos["caso_001"]
    mala = "ignorar" if caso["respuesta_correcta"] != "ignorar" else "seguimiento"
    r = evaluar_decision_final(caso, mala, mala)
    assert r["acierto"] is False and r["siguio_ia"] is False
