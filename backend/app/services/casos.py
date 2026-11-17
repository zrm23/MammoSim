"""Qué se le muestra al cliente de un caso y cuándo.

Se usa una LISTA BLANCA: solo sale lo que está escrito aquí. Si mañana se
agrega un campo nuevo al caso en Firestore, no se filtra por accidente.
"""

CAMPOS_RESUMEN = (
    "id_caso", "titulo", "descripcion_breve", "lado",
    "vistas", "dificultad", "modelo_3d_ref",
)
CAMPOS_CASO = CAMPOS_RESUMEN + (
    "edad_simulada", "datos_estudio", "enunciado_decision", "opciones_decision", "fuente",
)


def resumen_caso(caso: dict) -> dict:
    return {k: caso[k] for k in CAMPOS_RESUMEN if k in caso}


def caso_para_resolver(caso: dict) -> dict:
    """Caso sin respuesta_correcta, explicacion, IA, hallazgos ni retroalimentación."""
    salida = {k: caso[k] for k in CAMPOS_CASO if k in caso}
    salida["preguntas"] = [
        {"numero": p["numero"], "enunciado": p["enunciado"], "opciones": p["opciones"]}
        for p in caso["preguntas"]
    ]
    return salida


def pregunta_de(caso: dict, numero: int) -> dict:
    for p in caso["preguntas"]:
        if p["numero"] == numero:
            return p
    raise KeyError(f"El caso no tiene la pregunta {numero}")


def feedback_pregunta(pregunta: dict, opcion_elegida: str) -> dict:
    """Se muestra de inmediato al contestar cada pregunta técnica."""
    correcta_letra = pregunta["respuesta_correcta"]
    correcta = opcion_elegida == correcta_letra
    explicacion = pregunta["explicacion"]
    if correcta:
        mensaje = f"Correcto. {explicacion}"
    else:
        texto = pregunta["opciones"][correcta_letra]
        mensaje = (
            f"Incorrecto. La respuesta correcta es {correcta_letra} ({texto}). "
            f"{explicacion}"
        )
    return {
        "correcta": correcta,
        "respuesta_correcta": correcta_letra,
        "explicacion": explicacion,
        "mensaje": mensaje,
    }
