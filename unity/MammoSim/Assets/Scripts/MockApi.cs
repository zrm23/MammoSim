using UnityEngine;

// Respuestas de ejemplo (caso_001 recortado a 2 preguntas técnicas + la diagnóstica) para probar la UI sin backend.
// Se usa cuando ApiClient tiene marcada la casilla "Usar Datos De Ejemplo". Se puede borrar al conectar la API real.
public static class MockApi
{
    // Se escribe con comilla simple y se convierte a doble al final, para no llenar el código de escapes.
    const string Caso =
        "{'id_caso':'caso_001','titulo':'Mamografía de mama izquierda','descripcion_breve':'Mujer de 62 años (edad simulada)'," +
        "'lado':'izquierda','vistas':['CC','MLO'],'dificultad':'medio','edad_simulada':62,'modelo_3d_ref':'mama_caso_001','preguntas':[" +
        "{'numero':1,'tipo':'tecnica','enunciado':'En la lectura sistemática del estudio, ¿qué lateralidad corresponde a la anomalía anotada?'," +
        "'opciones':[{'id':'A','texto':'Derecha'},{'id':'B','texto':'Izquierda'},{'id':'C','texto':'Ambas'},{'id':'D','texto':'No está especificado'}]}," +
        "{'numero':2,'tipo':'tecnica','enunciado':'Según la taxonomía de hallazgos mamográficos del dataset, ¿cuál es la clase de anomalía?'," +
        "'opciones':[{'id':'A','texto':'Calcificaciones'},{'id':'B','texto':'Asimetría aislada'},{'id':'C','texto':'Masa'},{'id':'D','texto':'Distorsión sin masa identificada'}]}," +
        "{'numero':8,'tipo':'diagnostica','enunciado':'Con lo observado, ¿cuál es la conducta clínica más adecuada para esta paciente?'," +
        "'opciones':[{'id':'estudio_adicional','texto':'Estudios de imagen adicionales (proyecciones focalizadas, ecografía)'}," +
        "{'id':'biopsiar','texto':'Biopsia guiada por imagen'},{'id':'seguimiento','texto':'Seguimiento por imagen a corto plazo (6 meses)'}," +
        "{'id':'ignorar','texto':'Control de rutina (continuar el tamizaje)'}]}]}";

    public static string Responder(string path, string body)
    {
        string j = null;

        if (path == "/sesiones")
            j = "{'sesion_id':'ses_prueba_001','casos_asignados':['caso_001']}";
        else if (path.StartsWith("/casos/"))
            j = Caso;
        else if (path.EndsWith("/respuestas"))
        {
            var r = JsonUtility.FromJson<RespuestaReq>(body);
            string correctaId = r.numero_pregunta == 1 ? "B" : "C";
            string correctaTxt = r.numero_pregunta == 1 ? "Izquierda" : "Masa";
            string expl = r.numero_pregunta == 1
                ? "El lado se confirma siempre antes de interpretar el estudio."
                : "Una masa es una lesión con volumen, visible en más de una proyección.";
            string ok = r.opcion == correctaId ? "true" : "false";
            j = "{'correcta':" + ok + ",'opcion_correcta':'" + correctaId + "','texto_correcto':'" + correctaTxt + "','explicacion':'" + expl + "'}";
        }
        else if (path.EndsWith("/decision-inicial"))
            j = "{'conducta':'Seguimiento por imagen a corto plazo (6 meses)','texto':'La masa podría corresponder a un cambio benigno; se recomienda control por imagen en 6 meses.'}";
        else if (path.EndsWith("/decision-final"))
            j = "{'acierto_inicial':true,'acierto_final':true,'siguio_ia':false," +
                "'hallazgos':'Masa irregular de bordes espiculados en la mama izquierda (texto de ejemplo).'," +
                "'retroalimentacion':'La masa presenta forma irregular y bordes espiculados, características muy sospechosas de malignidad; la conducta adecuada es biopsia guiada por imagen.'}";

        return j?.Replace('\'', '"');
    }
}
