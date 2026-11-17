"""Agente Tutor, opción A: textos fijos del Excel, sin entrenar ningún modelo.

Regla (acordada con Zaira):
  - Si la decisión INICIAL del estudiante fue correcta, la IA defiende una
    opción incorrecta fija  (opcion_ia_incorrecta + recomendacion_ia_incorrecta).
  - Si la decisión inicial fue incorrecta, la IA recomienda la correcta
    (respuesta_correcta + recomendacion_ia_correcta).

Son funciones puras (no tocan Firebase), por eso son fáciles de probar.
"""


def recomendar(caso: dict, decision_inicial: str) -> dict:
    acerto = decision_inicial == caso["respuesta_correcta"]
    if acerto:
        opcion = caso["opcion_ia_incorrecta"]
        texto = caso["recomendacion_ia_incorrecta"]
    else:
        opcion = caso["respuesta_correcta"]
        texto = caso["recomendacion_ia_correcta"]
    return {"opcion_ia": opcion, "texto": texto, "ia_correcta": not acerto}


def evaluar_decision_final(
    caso: dict, decision_inicial: str, decision_final: str
) -> dict:
    """Campos que se guardan en decisiones_finales."""
    rec = recomendar(caso, decision_inicial)
    return {
        "decision": decision_final,
        "acierto": decision_final == caso["respuesta_correcta"],
        "opcion_ia": rec["opcion_ia"],
        "ia_correcta": rec["ia_correcta"],
        "siguio_ia": decision_final == rec["opcion_ia"],
    }
