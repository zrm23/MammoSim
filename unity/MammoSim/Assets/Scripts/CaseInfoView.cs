using TMPro;
using UnityEngine;

// Muestra los datos del caso seleccionado: tarjeta "Caso #001" y panel "Datos del estudio".
// No muestra motivo de consulta ni síntomas (el profesor indicó que no se pueden usar).
// Va en el objeto SimulationPanel, junto a QuestionView.
public class CaseInfoView : MonoBehaviour
{
    [SerializeField] TMP_Text numeroCaso;      // "Caso #001"
    [SerializeField] TMP_Text datosPaciente;   // edad simulada y mama
    [SerializeField] TMP_Text datosEstudio;    // lado, proyecciones, fuente

    void OnEnable() => SimulationEvents.OnCasoSeleccionado += Mostrar;
    void OnDisable() => SimulationEvents.OnCasoSeleccionado -= Mostrar;

    void Mostrar(CaseModel c)
    {
        numeroCaso.text = "Caso #" + c.Id.Replace("caso_", "");
        datosPaciente.text = $"Edad: {c.EdadSimulada} años (simulada)\nMama {c.Lado}";
        datosEstudio.text = $"Mama: {c.Lado}\nProyecciones: {c.Vistas}\nFuente: CBIS-DDSM";
    }
}
