using System;
using System.Collections.Generic;
using UnityEngine;

// Va en el objeto raíz "Lab". Es un OBSERVADOR: escucha SimulationEvents y no conoce la UI.
//  1) Pone el modelo 3D del caso (modelo_3d_ref) flotando sobre la mesa.
//  2) Hace reaccionar al robot (RobotTutor) según lo que pasa en la simulación.
// La cámara (OrbitCamera) y la UI son independientes: el laboratorio solo reacciona al flujo.
public class LabSceneManager : MonoBehaviour
{
    [Serializable]
    public class ModeloCaso
    {
        public string referencia;   // igual a modelo_3d_ref del caso, p. ej. mama_caso_001
        public GameObject prefab;
    }

    [Header("Escena")]
    [SerializeField] Transform anclaMamografia;   // punto sobre la mesa donde flota el modelo
    [SerializeField] RobotTutor robot;

    [Header("Modelos 3D del hallazgo")]
    [Tooltip("Para desarrollo: arrastra aquí los prefabs. Si no hay prefab, se muestra un marcador (esfera).")]
    [SerializeField] List<ModeloCaso> modelosLocales = new List<ModeloCaso>();
    [Tooltip("Para WebGL: URL de la carpeta de Firebase Hosting con los .glb (requiere glTFast y el símbolo MAMMOSIM_GLTFAST).")]
    [SerializeField] string urlBaseModelos = "";
    [Tooltip("Lado mayor del modelo, en metros, para que siempre quepa sobre la mesa.")]
    [SerializeField] float tamanoModelo = 0.6f;

    [Header("Movimiento del modelo")]
    [SerializeField] float giroAutomatico = 0f;    // grados por segundo; 0 = quieto (el estudiante orbita la cámara)
    [SerializeField] float flotacion = 0.03f;      // metros de subida y bajada

    GameObject _modelo;
    Vector3 _posBase;
    float _yaw;
    int _version;

    void Awake()
    {
        _posBase = anclaMamografia.localPosition;
    }

    void OnEnable()
    {
        SimulationEvents.OnCasoSeleccionado += CargarCaso;
        SimulationEvents.OnPreguntaMostrada += AlMostrarPregunta;
        SimulationEvents.OnRetroalimentacion += AlRetroalimentar;
        SimulationEvents.OnRecomendacionRecibida += AlRecomendar;
        SimulationEvents.OnEvaluacionDisponible += AlEvaluar;
        SimulationEvents.OnSimulacionFinalizada += AlTerminar;
    }

    void OnDisable()
    {
        SimulationEvents.OnCasoSeleccionado -= CargarCaso;
        SimulationEvents.OnPreguntaMostrada -= AlMostrarPregunta;
        SimulationEvents.OnRetroalimentacion -= AlRetroalimentar;
        SimulationEvents.OnRecomendacionRecibida -= AlRecomendar;
        SimulationEvents.OnEvaluacionDisponible -= AlEvaluar;
        SimulationEvents.OnSimulacionFinalizada -= AlTerminar;
    }

    void Update()
    {
        if (_modelo == null) return;

        _yaw += giroAutomatico * Time.deltaTime;
        anclaMamografia.localRotation = Quaternion.Euler(0f, _yaw, 0f);
        anclaMamografia.localPosition = _posBase + Vector3.up * (Mathf.Sin(Time.time * 1.5f) * flotacion);
    }

    // ---------- Reacciones a los eventos del flujo ----------
    void AlMostrarPregunta(PreguntaModel p, int indice, int total)
    {
        if (robot != null) robot.Reposo();
    }

    void AlRetroalimentar(RespuestaRes r)
    {
        if (robot != null) robot.Reaccionar(r.correcta ? EstadoRobot.Feliz : EstadoRobot.Triste, 2.5f);
    }

    void AlRecomendar(RecomendacionRes r)
    {
        if (robot != null) robot.Hablar(Mathf.Clamp(r.texto.Length * 0.05f, 2f, 8f));
    }

    void AlEvaluar(ResultadoCasoRes r)
{
    Debug.Log("[MammoSim] Resultado final recibido: " +
              JsonUtility.ToJson(r));

    if (robot == null) return;

    if (r.siguio_ia && !r.acierto_final)
    {
        // El estudiante siguió una recomendación incorrecta.
        // El tutor no muestra tristeza por su propio error.
        robot.Reposo();
    }
    else
    {
        robot.Reaccionar(
            r.acierto_final ? EstadoRobot.Feliz : EstadoRobot.Triste,
            4f
        );
    }
}

    void AlTerminar()
    {
        _version++;               // invalida cualquier descarga de modelo en curso
        LimpiarModelo();
        if (robot != null) robot.Reposo();
    }

    // ---------- Modelo 3D del hallazgo ----------
    void CargarCaso(CaseModel c)
    {
        LimpiarModelo();
        _version++;

        var entrada = modelosLocales.Find(m => m.referencia == c.Modelo3dRef && m.prefab != null);
        if (entrada != null)
        {
            Colocar(Instantiate(entrada.prefab));
        }
        else if (!string.IsNullOrEmpty(urlBaseModelos))
        {
#if MAMMOSIM_GLTFAST
            CargarRemoto(c.Modelo3dRef, _version);
#else
            Debug.LogWarning("[MammoSim] urlBaseModelos está definida pero falta glTFast (símbolo MAMMOSIM_GLTFAST). Uso un marcador.");
            Colocar(Marcador(c.Modelo3dRef));
#endif
        }
        else
        {
            Debug.LogWarning($"[MammoSim] No hay modelo 3D para '{c.Modelo3dRef}'. Uso un marcador (esfera).");
            Colocar(Marcador(c.Modelo3dRef));
        }

        if (robot != null) robot.Saludar();
    }

#if MAMMOSIM_GLTFAST
    async void CargarRemoto(string referencia, int version)
    {
        var gltf = new GLTFast.GltfImport();
        bool ok = await gltf.Load(urlBaseModelos.TrimEnd('/') + "/" + referencia + ".glb");
        if (!ok || version != _version) return;            // falló, o ya se cambió de caso

        var contenedor = new GameObject("Modelo_" + referencia);
        if (await gltf.InstantiateMainSceneAsync(contenedor.transform) && version == _version) Colocar(contenedor);
        else Destroy(contenedor);
    }
#endif

    
static GameObject Marcador(string referencia)
{
    var go = GameObject.CreatePrimitive(PrimitiveType.Sphere);

    go.name = "Marcador_" + referencia;
    go.transform.localScale = new Vector3(1f, 0.7f, 1f);

    // CreatePrimitive ya incluye Sphere Collider.
    // Lo conservamos para permitir la rotación con el mouse.

    return go;
}


    void LimpiarModelo()
    {
        if (_modelo != null) Destroy(_modelo);
        _modelo = null;
    }

    // Lo coloca en el ancla, lo escala para que su lado mayor mida "tamanoModelo" y lo centra sobre ella.
    void Colocar(GameObject go)
    {
        _yaw = 0f;
        anclaMamografia.localRotation = Quaternion.identity;
        anclaMamografia.localPosition = _posBase;

        var t = go.transform;
        t.SetParent(anclaMamografia, false);
        t.localPosition = Vector3.zero;
        t.localRotation = Quaternion.identity;

        if (Limites(go, out Bounds b))
        {
            float mayor = Mathf.Max(b.size.x, b.size.y, b.size.z);
            if (mayor > 0.0001f) t.localScale *= tamanoModelo / mayor;
            if (Limites(go, out b)) t.position += anclaMamografia.position - b.center;
        }
        _modelo = go;
    }

    static bool Limites(GameObject go, out Bounds b)
    {
        var rs = go.GetComponentsInChildren<Renderer>();
        b = default;
        if (rs.Length == 0) return false;
        b = rs[0].bounds;
        for (int i = 1; i < rs.Length; i++) b.Encapsulate(rs[i].bounds);
        return true;
    }

    // Ayuda visual en la Scene: dónde flotará el modelo (círculo rosa) y dónde está el robot (caja cian).
    void OnDrawGizmos()
    {
        if (anclaMamografia != null)
        {
            Gizmos.color = new Color(0.91f, 0.12f, 0.55f);
            Gizmos.DrawWireSphere(anclaMamografia.position, tamanoModelo * 0.5f);
        }
        if (robot != null)
        {
            Gizmos.color = Color.cyan;
            Gizmos.DrawWireCube(robot.transform.position + Vector3.up * 0.45f, new Vector3(0.5f, 0.9f, 0.5f));
        }
    }
}
