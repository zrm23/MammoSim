
using UnityEngine;
using UnityEngine.InputSystem;

public class RotarModelo3D : MonoBehaviour
{
    [SerializeField] float sensibilidad = 0.3f;
    [SerializeField] Camera camara;

    bool arrastrando;
    Transform modelo;

    void Start()
    {
        if (camara == null)
            camara = Camera.main;
    }

    void Update()
    {
        if (Mouse.current == null || camara == null)
            return;

        // Buscar el modelo generado dentro de MammoAnchor
        if (transform.childCount == 0)
        {
            modelo = null;
            arrastrando = false;
            return;
        }

        modelo = transform.GetChild(0);

        // Detectar si el clic comenzó sobre el modelo
        if (Mouse.current.leftButton.wasPressedThisFrame)
        {
            arrastrando = false;

            Vector2 posicionMouse = Mouse.current.position.ReadValue();
            Ray rayo = camara.ScreenPointToRay(posicionMouse);

            if (Physics.Raycast(rayo, out RaycastHit impacto))
            {
                Debug.Log("El rayo tocó: " + impacto.transform.name);
                
                if (impacto.transform == modelo ||
                    impacto.transform.IsChildOf(modelo))
                {
                    arrastrando = true;
                    Debug.Log("ROTACIÓN ACTIVADA");
                }
            }
        }

        // Terminar el arrastre al soltar el clic
        if (Mouse.current.leftButton.wasReleasedThisFrame)
            arrastrando = false;

        if (!arrastrando)
            return;

        Vector2 movimiento = Mouse.current.delta.ReadValue();

        modelo.Rotate(
            Vector3.up,
            -movimiento.x * sensibilidad,
            Space.World
        );

        modelo.Rotate(
            Vector3.right,
            movimiento.y * sensibilidad,
            Space.World
        );
    }
}
