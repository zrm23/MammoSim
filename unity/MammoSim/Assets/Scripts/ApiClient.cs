using System;
using System.Collections;
using System.Text;
using UnityEngine;
using UnityEngine.Networking;

// Cliente de la API FastAPI. En WebGL solo funciona UnityWebRequest (no System.Net).
// El GameObject debe llamarse exactamente "ApiClient": React le entrega el token con
//   unityInstance.SendMessage("ApiClient", "SetToken", idToken);
public class ApiClient : MonoBehaviour
{
    [Header("Conexión")]
    [SerializeField] string baseUrl = "https://TU-SERVICIO.onrender.com";

    [Header("Pruebas")]
    [Tooltip("Responde con datos de ejemplo (MockApi) sin llamar al backend. Desmárcalo al conectar la API real.")]
    [SerializeField] bool usarDatosDeEjemplo = true;

    string _token;

    // El token (JWT) caduca: React debe volver a llamar a SetToken cuando lo renueve.
    public event Action OnTokenExpired;

    public void SetToken(string token) => _token = token;

    public IEnumerator Get<T>(string path, Action<T> ok, Action<string> fail)
    {
        if (usarDatosDeEjemplo)
        {
            yield return null;
            Entregar(MockApi.Responder(path, null), ok, fail);
            yield break;
        }

        using (var req = UnityWebRequest.Get(baseUrl + path))
            yield return Send(req, ok, fail);
    }

    public IEnumerator Post<TReq, TRes>(string path, TReq body, Action<TRes> ok, Action<string> fail)
    {
        var json = JsonUtility.ToJson(body);

        if (usarDatosDeEjemplo)
        {
            yield return null;
            Entregar(MockApi.Responder(path, json), ok, fail);
            yield break;
        }

        using (var req = new UnityWebRequest(baseUrl + path, "POST"))
        {
            req.uploadHandler = new UploadHandlerRaw(Encoding.UTF8.GetBytes(json));
            req.downloadHandler = new DownloadHandlerBuffer();
            yield return Send(req, ok, fail);
        }
    }

    IEnumerator Send<T>(UnityWebRequest req, Action<T> ok, Action<string> fail)
    {
        req.SetRequestHeader("Content-Type", "application/json");
        req.SetRequestHeader("Authorization", "Bearer " + _token);
        req.timeout = 60; // Render gratuito puede tardar en "despertar" en la primera petición

        yield return req.SendWebRequest();

        if (req.result == UnityWebRequest.Result.Success)
        {
            Entregar(req.downloadHandler.text, ok, fail);
            yield break;
        }

        if (req.responseCode == 401) OnTokenExpired?.Invoke();
        // 409 = la API rechazó reescribir una respuesta/decisión (son de escritura única)
        fail($"HTTP {req.responseCode}: {req.error}");
    }

    static void Entregar<T>(string json, Action<T> ok, Action<string> fail)
    {
        if (string.IsNullOrEmpty(json)) { fail("Sin datos para esta ruta"); return; }

        T valor;
        try { valor = JsonUtility.FromJson<T>(json); }
        catch (Exception e) { fail("Respuesta inválida: " + e.Message); return; }

        ok(valor);
    }
}
