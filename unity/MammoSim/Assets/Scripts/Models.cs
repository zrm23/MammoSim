using System;
using System.Linq;

// ============ DTOs: lo que viaja por la API (nombres = campos del JSON / de Firestore) ============

[Serializable] public class OpcionDto { public string id; public string texto; }

[Serializable]
public class PreguntaDto
{
    public int numero;        // 1..7 técnicas, 8 diagnóstica
    public string tipo;       // "tecnica" | "diagnostica"
    public string enunciado;
    public OpcionDto[] opciones;   // técnicas: ids A-D. Diagnóstica: ids = biopsiar|seguimiento|estudio_adicional|ignorar
}

[Serializable]
public class CasoDto
{
    public string id_caso;
    public string titulo;
    public string descripcion_breve;
    public string lado;
    public string[] vistas;
    public string dificultad;
    public int edad_simulada;
    public string modelo_3d_ref;
    public PreguntaDto[] preguntas;   // el backend NUNCA envía respuesta_correcta ni explicacion aquí
}

[Serializable] public class VacioReq { }
[Serializable] public class SesionRes { public string sesion_id; public string[] casos_asignados; }

[Serializable] public class RespuestaReq { public int numero_pregunta; public string opcion; }
[Serializable]
public class RespuestaRes
{
    public bool correcta;
    public string opcion_correcta;
    public string texto_correcto;
    public string explicacion;
}

[Serializable] public class DecisionReq { public string decision; }   // biopsiar | seguimiento | estudio_adicional | ignorar
[Serializable] public class RecomendacionRes { public string conducta; public string texto; }

[Serializable]
public class ResultadoCasoRes
{
    public bool acierto_inicial;
    public bool acierto_final;
    public bool siguio_ia;
    public string hallazgos;
    public string retroalimentacion;
}

// ============ Modelos internos de Unity (lo único que conoce la UI) ============

public class OpcionModel { public string Id; public string Texto; }

public class PreguntaModel
{
    public int Numero;
    public bool EsDiagnostica;
    public string Enunciado;
    public OpcionModel[] Opciones;
}

public class CaseModel
{
    public string Id;
    public string Titulo;
    public string Descripcion;
    public string Lado;
    public string Vistas;
    public string Dificultad;
    public int EdadSimulada;
    public string Modelo3dRef;
    public PreguntaModel[] Preguntas;
}

// Patrón Adapter: traduce el DTO de FastAPI al modelo interno.
public static class CaseDtoAdapter
{
    public static CaseModel Adaptar(CasoDto d) => new CaseModel
    {
        Id = d.id_caso,
        Titulo = d.titulo,
        Descripcion = d.descripcion_breve,
        Lado = d.lado,
        Vistas = d.vistas == null ? "" : string.Join(" y ", d.vistas),
        Dificultad = d.dificultad,
        EdadSimulada = d.edad_simulada,
        Modelo3dRef = d.modelo_3d_ref,
        Preguntas = d.preguntas
            .OrderBy(p => p.numero)
            .Select(p => new PreguntaModel
            {
                Numero = p.numero,
                EsDiagnostica = p.tipo == "diagnostica",
                Enunciado = p.enunciado,
                Opciones = p.opciones.Select(o => new OpcionModel { Id = o.id, Texto = o.texto }).ToArray()
            }).ToArray()
    };
}

// Estados del flujo (patrón State, versión simplificada: enum + transiciones válidas en GameManager).
public enum FaseSimulacion
{
    Cargando,
    Pregunta,           // técnicas 1..7
    Retroalimentacion,  // tras responder una técnica
    DecisionInicial,    // pregunta 8, IA oculta
    DecisionFinal,      // IA ya recomendó; confirmar o cambiar
    Resultado,
    Error
}
