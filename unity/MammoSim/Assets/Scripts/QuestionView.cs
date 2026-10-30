using TMPro;
using UnityEngine;
using UnityEngine.UI;

// Vista (V de MVC) de la pantalla de preguntas: enunciado + 4 opciones + botón de acción,
// retroalimentación y panel del agente tutor (este SOLO se ve en la fase DecisionFinal, RF-004.2).
// Va en el objeto SimulationPanel.
public class QuestionView : MonoBehaviour
{
    [Header("Pregunta")]
    [SerializeField] TMP_Text progreso;          // "Pregunta 3 de 8"
    [SerializeField] TMP_Text enunciado;
    [SerializeField] Button[] botonesOpcion;     // Option_A, B, C, D (en ese orden)
    [SerializeField] TMP_Text[] textosOpcion;    // el TMP hijo de cada botón, mismo orden

    [Header("Botón de acción")]
    [SerializeField] Button botonAccion;
    [SerializeField] TMP_Text textoAccion;

    [Header("Panel derecho superior")]
    [SerializeField] GameObject panelTutor;
    [SerializeField] TMP_Text textoTutor;
    [SerializeField] GameObject panelRetro;
    [SerializeField] TMP_Text textoRetro;

    [Header("Colores de las opciones")]
    [SerializeField] Color normal = new Color(0.12f, 0.17f, 0.47f);
    [SerializeField] Color seleccionado = new Color(0.91f, 0.12f, 0.55f);
    [SerializeField] Color correcto = new Color(0.10f, 0.65f, 0.35f);
    [SerializeField] Color incorrecto = new Color(0.80f, 0.20f, 0.20f);

    PreguntaModel _pregunta;
    string _seleccion;
    FaseSimulacion _fase;

    void OnEnable()
    {
        SimulationEvents.OnFase += AlCambiarFase;
        SimulationEvents.OnPreguntaMostrada += Mostrar;
        SimulationEvents.OnRetroalimentacion += MostrarRetro;
        SimulationEvents.OnRecomendacionRecibida += MostrarRecomendacion;
        SimulationEvents.OnEvaluacionDisponible += MostrarResultado;
        SimulationEvents.OnError += MostrarError;

        botonAccion.onClick.AddListener(AlPulsarAccion);
        for (int i = 0; i < botonesOpcion.Length; i++)
        {
            int k = i; // captura para el closure
            botonesOpcion[i].onClick.AddListener(() => Elegir(k));
        }
    }

    void OnDisable()
    {
        SimulationEvents.OnFase -= AlCambiarFase;
        SimulationEvents.OnPreguntaMostrada -= Mostrar;
        SimulationEvents.OnRetroalimentacion -= MostrarRetro;
        SimulationEvents.OnRecomendacionRecibida -= MostrarRecomendacion;
        SimulationEvents.OnEvaluacionDisponible -= MostrarResultado;
        SimulationEvents.OnError -= MostrarError;

        botonAccion.onClick.RemoveListener(AlPulsarAccion);
        foreach (var b in botonesOpcion) b.onClick.RemoveAllListeners();
    }

    void AlCambiarFase(FaseSimulacion f)
    {
        _fase = f;

        panelTutor.SetActive(f == FaseSimulacion.DecisionFinal);
        panelRetro.SetActive(f == FaseSimulacion.Retroalimentacion || f == FaseSimulacion.Resultado || f == FaseSimulacion.Error);

        bool opcionesActivas = f == FaseSimulacion.Pregunta || f == FaseSimulacion.DecisionInicial || f == FaseSimulacion.DecisionFinal;
        foreach (var b in botonesOpcion) b.interactable = opcionesActivas;

        if (f == FaseSimulacion.Cargando)
        {
            progreso.text = "";
            enunciado.text = "Cargando caso...";
            foreach (var b in botonesOpcion) b.gameObject.SetActive(false);
        }

        textoAccion.text = f switch
        {
            FaseSimulacion.Pregunta => "Responder",
            FaseSimulacion.Retroalimentacion => "Siguiente",
            FaseSimulacion.DecisionInicial => "Enviar decisión",
            FaseSimulacion.DecisionFinal => "Confirmar decisión final",
            FaseSimulacion.Resultado => "Volver a casos",
            FaseSimulacion.Error => "Volver a casos",
            _ => "..."
        };
        botonAccion.interactable = f == FaseSimulacion.Retroalimentacion || f == FaseSimulacion.Resultado || f == FaseSimulacion.Error;
    }

    void Mostrar(PreguntaModel p, int indice, int total)
    {
        _pregunta = p;
        progreso.text = $"Pregunta {indice + 1} de {total}";
        enunciado.text = p.Enunciado;

        for (int i = 0; i < botonesOpcion.Length; i++)
        {
            bool existe = i < p.Opciones.Length;
            botonesOpcion[i].gameObject.SetActive(existe);
            if (!existe) continue;
            var o = p.Opciones[i];
            textosOpcion[i].text = p.EsDiagnostica ? o.Texto : $"{o.Id}. {o.Texto}";
        }

        // En la decisión final se precarga la inicial: el estudiante la confirma o la cambia.
        _seleccion = _fase == FaseSimulacion.DecisionFinal ? GameManager.Instance.DecisionInicial : null;
        PintarSeleccion();
        botonAccion.interactable = _seleccion != null;
    }

    void Elegir(int indice)
    {
        _seleccion = _pregunta.Opciones[indice].Id;
        PintarSeleccion();
        botonAccion.interactable = true;
    }

    void PintarSeleccion()
    {
        for (int i = 0; i < _pregunta.Opciones.Length; i++)
            Pintar(i, _pregunta.Opciones[i].Id == _seleccion ? seleccionado : normal);
    }

    void Pintar(int i, Color c) => botonesOpcion[i].image.color = c;

    void AlPulsarAccion()
    {
        var gm = GameManager.Instance;
        switch (_fase)
        {
            case FaseSimulacion.Retroalimentacion: gm.Siguiente(); break;
            case FaseSimulacion.Resultado:
            case FaseSimulacion.Error: gm.Terminar(); break;
            default:
                if (_seleccion == null) return;
                botonAccion.interactable = false;   // bloquea doble clic
                foreach (var b in botonesOpcion) b.interactable = false;
                gm.EnviarOpcion(_seleccion);
                break;
        }
    }

    void MostrarRetro(RespuestaRes r)
    {
        for (int i = 0; i < _pregunta.Opciones.Length; i++)
        {
            string id = _pregunta.Opciones[i].Id;
            if (id == r.opcion_correcta) Pintar(i, correcto);
            else if (id == _seleccion) Pintar(i, incorrecto);
        }
        textoRetro.text = r.correcta
            ? $"¡Correcto! {r.explicacion}"
            : $"No es esa. La respuesta correcta es: {r.texto_correcto}\n{r.explicacion}";
    }

    void MostrarRecomendacion(RecomendacionRes r) => textoTutor.text = r.texto;

    void MostrarResultado(ResultadoCasoRes r)
    {
        string ia = r.siguio_ia
            ? "Tu decisión final fue la que recomendó la IA."
            : "Tu decisión final fue distinta a la recomendación de la IA.";
        textoRetro.text = $"{r.retroalimentacion}\n\nHallazgos: {r.hallazgos}\n\n{ia}";
        botonAccion.interactable = true;
    }

    void MostrarError(string msg)
    {
        textoRetro.text = "No se pudo comunicar con el servidor. Si es la primera petición, espera unos segundos e inténtalo de nuevo.";
    }
}
