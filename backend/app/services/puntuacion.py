"""Nota de cada caso y puntuación de la sesión (sobre 10).

Cada caso vale 8 puntos de 1,25 (8 x 1,25 = 10):
  - 7 preguntas técnicas: 1 punto cada una.
  - La decisión: 1 punto repartido en dos mitades,
    0,5 si la inicial fue buena y 0,5 si la final fue buena.
"""
PUNTOS_POR_CASO = 8
VALOR_PUNTO = 10 / PUNTOS_POR_CASO  # 1,25
TOTAL_PREGUNTAS = 7


def nota_caso(
    preguntas_acertadas: int, acierto_inicial: bool, acierto_final: bool
) -> float:
    if not 0 <= preguntas_acertadas <= TOTAL_PREGUNTAS:
        raise ValueError("preguntas_acertadas debe estar entre 0 y 7")
    puntos = preguntas_acertadas + 0.5 * acierto_inicial + 0.5 * acierto_final
    return round(puntos * VALOR_PUNTO, 2)


def puntuacion_sesion(
    preguntas_acertadas: int,
    aciertos_iniciales: int,
    aciertos_finales: int,
    total_casos: int,
) -> float:
    """Se guarda en resultados.puntuacion."""
    if total_casos <= 0:
        raise ValueError("total_casos debe ser mayor que 0")
    puntos = preguntas_acertadas + 0.5 * aciertos_iniciales + 0.5 * aciertos_finales
    return round(puntos / (PUNTOS_POR_CASO * total_casos) * 10, 2)
