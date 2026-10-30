using UnityEngine;

// Va en SimulationPanel. El botón "Iniciar Simulación" del catálogo llama a Abrir("caso_001") desde su OnClick.
// "Pantalla Catalogo" = los paneles que se ocultan mientras dura la simulación (y reaparecen al volver).
public class SimulationScreen : MonoBehaviour
{
    [SerializeField] GameObject[] pantallaCatalogo;

    public void Abrir(string casoId)
    {
        if (GameManager.Instance == null)
        {
            Debug.LogError("[MammoSim] Falta el objeto GameManager en la escena.");
            return;
        }

        foreach (var g in pantallaCatalogo) g.SetActive(false);
        gameObject.SetActive(true);                 // aquí se suscriben las vistas (OnEnable)
        GameManager.Instance.IniciarCaso(casoId);
    }

    void OnEnable() => SimulationEvents.OnSimulacionFinalizada += Cerrar;
    void OnDisable() => SimulationEvents.OnSimulacionFinalizada -= Cerrar;

    void Cerrar()
    {
        gameObject.SetActive(false);
        foreach (var g in pantallaCatalogo) g.SetActive(true);
    }
}
