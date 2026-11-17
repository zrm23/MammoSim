#!/usr/bin/env python3
"""
Carga de datos fijos de MammoSim en Firestore.

Escribe:
  - casos_clinicos/caso_001 ... caso_007   (desde casos_clinicos.json)
  - docentes_autorizados/{correo}          (desde docentes_autorizados.json)

Por defecto NO escribe nada: valida los archivos y muestra qué haría (modo prueba).
Para escribir de verdad hay que agregar --escribir.

La clave de la cuenta de servicio NUNCA va en el chat ni en GitHub. Se indica la ruta
del archivo .json de la clave en la variable de entorno GOOGLE_APPLICATION_CREDENTIALS
o con --clave (ruta). Instalar antes:  pip install firebase-admin

Uso:
  python cargar_casos.py                      # solo valida (sin conexión)
  python cargar_casos.py --listar             # muestra las colecciones que hay hoy y cuántos documentos
  python cargar_casos.py --escribir           # escribe los 7 casos (reemplaza el documento completo)
  python cargar_casos.py --escribir --docentes  # además carga docentes_autorizados
"""
import argparse, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
DECISIONES = {"biopsiar", "seguimiento", "ignorar", "estudio_adicional"}
CAMPOS = ["id_caso", "titulo", "descripcion_breve", "lado", "vistas", "dificultad", "edad_simulada",
          "modelo_3d_ref", "datos_estudio", "preguntas", "enunciado_decision", "opciones_decision",
          "hallazgos", "respuesta_correcta", "recomendacion_ia_correcta", "opcion_ia_incorrecta",
          "recomendacion_ia_incorrecta", "retroalimentacion", "fuente"]

CAMPOS_PREGUNTA = ["numero", "enunciado", "opciones", "respuesta_correcta", "explicacion"]


def validar(casos):
    errores = []
    if sorted(casos) != [f"caso_00{i}" for i in range(1, 8)]:
        errores.append("Deben ser exactamente caso_001 a caso_007")
    for cid, c in casos.items():
        if not isinstance(c, dict):
            errores.append(f"{cid}: el caso debe ser un objeto")
            continue
        faltan = [k for k in CAMPOS if k not in c]
        if faltan:
            errores.append(f"{cid}: faltan campos {faltan}")
            continue
        if c["id_caso"] != cid:
            errores.append(f"{cid}: id_caso no coincide con el ID del documento")
        if c["lado"] not in ("izquierda", "derecha"):
            errores.append(f"{cid}: lado inválido")
        if c["dificultad"] not in ("facil", "medio", "dificil"):
            errores.append(f"{cid}: dificultad inválida")
        if not isinstance(c["edad_simulada"], int):
            errores.append(f"{cid}: edad_simulada debe ser número")
        if not isinstance(c["preguntas"], list) or len(c["preguntas"]) != 7:
            errores.append(f"{cid}: debe tener 7 preguntas técnicas")
        preguntas = c["preguntas"] if isinstance(c["preguntas"], list) else []
        for n, p in enumerate(preguntas, 1):
            if not isinstance(p, dict):
                errores.append(f"{cid} p{n}: la pregunta debe ser un objeto")
                continue
            faltan_p = [k for k in CAMPOS_PREGUNTA if k not in p]
            if faltan_p:
                errores.append(f"{cid} p{n}: faltan campos {faltan_p}")
                continue
            if p["numero"] != n:
                errores.append(f"{cid} p{n}: numeración incorrecta")
            if not isinstance(p["opciones"], dict) or sorted(p["opciones"]) != ["A", "B", "C", "D"]:
                errores.append(f"{cid} p{n}: debe tener 4 opciones A-D")
            elif p["respuesta_correcta"] not in p["opciones"]:
                errores.append(f"{cid} p{n}: la clave no es una opción")
            if not p["explicacion"]:
                errores.append(f"{cid} p{n}: falta explicación")
        for campo in ("respuesta_correcta", "opcion_ia_incorrecta"):
            if c[campo] not in DECISIONES:
                errores.append(f"{cid}: {campo} inválido ({c[campo]})")
        if c["respuesta_correcta"] == c["opcion_ia_incorrecta"]:
            errores.append(f"{cid}: la opción incorrecta de la IA es igual a la correcta")
        opciones_dec = c["opciones_decision"] if isinstance(c["opciones_decision"], list) else []
        if any(not isinstance(o, dict) or "valor" not in o for o in opciones_dec):
            errores.append(f"{cid}: cada opción de opciones_decision debe tener el campo 'valor'")
        elif {o["valor"] for o in opciones_dec} != DECISIONES:
            errores.append(f"{cid}: opciones_decision debe tener las 4 decisiones")
        if "edad_paciente" in c:
            errores.append(f"{cid}: no debe existir edad_paciente (se usa edad_simulada)")
    return errores


def conectar(ruta_clave):
    import firebase_admin
    from firebase_admin import credentials, firestore
    if ruta_clave:
        firebase_admin.initialize_app(credentials.Certificate(ruta_clave))
    else:
        firebase_admin.initialize_app()
    return firestore.client()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--escribir", action="store_true", help="escribe en Firestore (sin esto solo valida)")
    ap.add_argument("--docentes", action="store_true", help="también carga docentes_autorizados")
    ap.add_argument("--listar", action="store_true", help="lista las colecciones actuales y su número de documentos")
    ap.add_argument("--clave", help="ruta del .json de la cuenta de servicio (o usa GOOGLE_APPLICATION_CREDENTIALS)")
    a = ap.parse_args()

    with open(os.path.join(AQUI, "casos_clinicos.json"), encoding="utf-8") as f:
        casos = json.load(f)
    errores = validar(casos)
    if errores:
        print("ERRORES en casos_clinicos.json:")
        for e in errores:
            print(" -", e)
        sys.exit(1)
    print(f"casos_clinicos.json válido: {len(casos)} casos, 7 preguntas técnicas cada uno.")

    correos = []
    if a.docentes:   # el archivo de docentes solo se necesita con --docentes
        ruta_docentes = os.path.join(AQUI, "docentes_autorizados.json")
        if not os.path.exists(ruta_docentes):
            print(f"ERROR: con --docentes hace falta el archivo {ruta_docentes}")
            sys.exit(1)
        with open(ruta_docentes, encoding="utf-8") as f:
            correos = [c.strip().lower() for c in json.load(f)["correos"] if c.strip()]

    if not (a.escribir or a.listar):
        print("Modo prueba: no se escribió nada. Se escribirían:")
        for cid, c in casos.items():
            print(f"  casos_clinicos/{cid}  ({c['titulo']}, edad simulada {c['edad_simulada']}, correcta: {c['respuesta_correcta']})")
        if a.docentes:
            print(f"  docentes_autorizados: {len(correos)} correos")
        print("Agrega --escribir para escribir de verdad.")
        return

    db = conectar(a.clave)   # sin --clave usa GOOGLE_APPLICATION_CREDENTIALS
    if a.listar:
        print("Colecciones actuales:")
        for col in db.collections():
            n = sum(1 for _ in col.limit(1000).stream())
            print(f"  {col.id}: {n} documentos")
    if a.escribir:
        for cid, c in casos.items():
            db.collection("casos_clinicos").document(cid).set(c)   # set() reemplaza todo el documento
            print("escrito casos_clinicos/" + cid)
        if a.docentes:
            for correo in correos:
                db.collection("docentes_autorizados").document(correo).set({"activo": True})
                print("escrito docentes_autorizados/" + correo)
        print("Listo.")


if __name__ == "__main__":
    main()
