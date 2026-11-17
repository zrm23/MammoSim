import pytest

from app.services.puntuacion import nota_caso, puntuacion_sesion


def test_caso_perfecto_es_10():
    assert nota_caso(7, True, True) == 10


def test_caso_en_blanco_es_0():
    assert nota_caso(0, False, False) == 0


def test_la_decision_vale_la_mitad_inicial_y_la_mitad_final():
    # 7 preguntas bien y solo una de las dos decisiones buena: pierde 0,625
    assert nota_caso(7, True, False) == 9.38
    assert nota_caso(7, False, True) == 9.38
    assert nota_caso(7, False, False) == 8.75


def test_ejemplo_de_la_guia():
    # 3 casos, 18 preguntas, 2 iniciales y 2 finales buenas -> 8,33
    assert puntuacion_sesion(18, 2, 2, 3) == 8.33


def test_la_sesion_es_el_promedio_de_las_notas_de_los_casos():
    casos = [(7, True, True), (5, True, False), (3, False, False)]
    promedio = sum(nota_caso(*c) for c in casos) / len(casos)
    sesion = puntuacion_sesion(
        preguntas_acertadas=sum(c[0] for c in casos),
        aciertos_iniciales=sum(c[1] for c in casos),
        aciertos_finales=sum(c[2] for c in casos),
        total_casos=len(casos),
    )
    assert sesion == pytest.approx(promedio, abs=0.01)


def test_entradas_invalidas():
    with pytest.raises(ValueError):
        nota_caso(8, True, True)
    with pytest.raises(ValueError):
        puntuacion_sesion(0, 0, 0, 0)
