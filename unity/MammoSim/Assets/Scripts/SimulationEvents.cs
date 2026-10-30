using System;

// Patrón Observer: GameManager publica, las vistas se suscriben (en OnEnable) y se desuscriben (en OnDisable).
public static class SimulationEvents
{
    public static Action<FaseSimulacion> OnFase;
    public static Action<CaseModel> OnCasoSeleccionado;
    public static Action<PreguntaModel, int, int> OnPreguntaMostrada;   // pregunta, índice (0-based), total
    public static Action<RespuestaRes> OnRetroalimentacion;
    public static Action<string> OnDecisionRegistrada;                  // "inicial" | "final"
    public static Action<RecomendacionRes> OnRecomendacionRecibida;
    public static Action<ResultadoCasoRes> OnEvaluacionDisponible;
    public static Action<string> OnError;
    public static Action OnSimulacionFinalizada;                        // volver al catálogo
}
