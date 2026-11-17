
using UnityEngine;

public enum EstadoRobot { Reposo, Hablando, Feliz, Triste }

public class RobotTutor : MonoBehaviour
{
    [Header("Movimiento")]
    [Tooltip("A qué mira el robot (normalmente MammoAnchor).")]
    [SerializeField] Transform objetivoMirada;
    [SerializeField] float correccionYaw = 0f;
    [SerializeField] float alturaFlotacion = 0.05f;

    [Header("Expresiones faciales")]
    [SerializeField] Renderer pantallaRobot;
    [SerializeField] Material caraNeutral;
    [SerializeField] Material caraHablando;
    [SerializeField] Material caraFeliz;
    [SerializeField] Material caraTriste;

    Vector3 _posBase;
    Quaternion _rotBase;
    Vector3 _escalaBase;

    EstadoRobot _estado = EstadoRobot.Reposo;
    float _hasta;

    void Awake()
    {
        _posBase = transform.localPosition;
        _rotBase = transform.localRotation;
        _escalaBase = transform.localScale;

        ActualizarCara();
    }

    public void Reposo()
    {
        _estado = EstadoRobot.Reposo;
        ActualizarCara();
    }

    public void Saludar() => Hablar(2f);

    public void Hablar(float segundos) =>
        Reaccionar(EstadoRobot.Hablando, segundos);

    public void Reaccionar(EstadoRobot estado, float segundos)
    {
        _estado = estado;
        _hasta = Time.time + segundos;
        ActualizarCara();
    }

    void ActualizarCara()
    {
        if (pantallaRobot == null) return;

        Material material = null;

        switch (_estado)
        {
            case EstadoRobot.Reposo:
                material = caraNeutral;
                break;

            case EstadoRobot.Hablando:
                material = caraHablando;
                break;

            case EstadoRobot.Feliz:
                material = caraFeliz;
                break;

            case EstadoRobot.Triste:
                material = caraTriste;
                break;
        }

        if (material != null)
            pantallaRobot.sharedMaterial = material;
    }

    void Update()
    {
        if (_estado != EstadoRobot.Reposo && Time.time > _hasta)
        {
            _estado = EstadoRobot.Reposo;
            ActualizarCara();
        }

        float t = Time.time;
        Vector3 pos = _posBase;
        Quaternion rot = _rotBase;
        Vector3 esc = _escalaBase;
        
        // Mirar hacia la cámara, girando solo en el eje Y.
        if (objetivoMirada != null)
        {
            Vector3 direccion = objetivoMirada.position - transform.position;
            direccion.y = 0f;

            if (direccion.sqrMagnitude > 0.001f)
            {
                Quaternion mirada = Quaternion.LookRotation(direccion);
                Quaternion ajuste = Quaternion.Euler(0f, correccionYaw, 0f);

                // Conserva la inclinación original del modelo FBX.
                rot = mirada * ajuste * Quaternion.Euler(
                    _rotBase.eulerAngles.x,
                    0f,
                    _rotBase.eulerAngles.z
                );
            }
        }


        // Flotación permanente
        pos.y += Mathf.Sin(t * 1.6f) * alturaFlotacion;

        switch (_estado)
        {
            case EstadoRobot.Hablando:
                esc *= 1f + Mathf.Abs(Mathf.Sin(t * 9f)) * 0.04f;
                break;

            case EstadoRobot.Feliz:
                pos.y += Mathf.Abs(Mathf.Sin(t * 6f)) * 0.18f;
                rot *= Quaternion.Euler(
                    0f, Mathf.Sin(t * 6f) * 12f, 0f
                );
                break;

            case EstadoRobot.Triste:
                rot *= Quaternion.Euler(
                    0f, Mathf.Sin(t * 10f) * 15f, 0f
                );
                break;
        }

        transform.localPosition = pos;
        transform.localRotation = rot;
        transform.localScale = esc;
    }
}
