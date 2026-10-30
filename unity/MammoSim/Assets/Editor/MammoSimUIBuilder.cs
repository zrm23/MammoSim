// COLOCAR EN: Assets/Editor/MammoSimUIBuilder.cs   (crea la carpeta "Editor" si no existe)
// Uso: menú superior  MammoSim > Crear pantalla de simulación
using System.Collections.Generic;
using TMPro;
using UnityEditor;
using UnityEditor.Events;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public static class MammoSimUIBuilder
{
    static readonly Color Navy = Hex("0B1033");
    static readonly Color Navy2 = Hex("16206B");
    static readonly Color Pink = Hex("E91E8C");
    static readonly Color PinkSoft = Hex("F7C6DD");
    static readonly Color OptionBlue = Hex("1E2A78");

    [MenuItem("MammoSim/Crear pantalla de simulación")]
    static void Crear()
    {
        var hudGo = GameObject.Find("CanvasHUD");
        if (hudGo == null)
        {
            EditorUtility.DisplayDialog("MammoSim", "No encuentro el objeto CanvasHUD en la escena abierta.", "OK");
            return;
        }
        var hud = hudGo.GetComponent<RectTransform>();

        var viejo = hud.Find("SimulationPanel");
        if (viejo != null)
        {
            if (!EditorUtility.DisplayDialog("MammoSim", "Ya existe un SimulationPanel. ¿Lo borro y lo creo de nuevo?", "Sí, reemplazar", "Cancelar"))
                return;
            Undo.DestroyObjectImmediate(viejo.gameObject);
        }

        PrepararManagers();

        // ---- Hasta dónde llega la barra de navegación (para que el panel empiece justo a su derecha) ----
        float izquierda = 340f;
        var nav = hud.Find("NavigationPanel") as RectTransform;
        if (nav != null)
        {
            var c = new Vector3[4];
            nav.GetWorldCorners(c);
            izquierda = hud.InverseTransformPoint(c[2]).x - hud.rect.xMin + 20f;
        }

        // ================= Contenedor =================
        var panel = Panel("SimulationPanel", hud, V(0, 0), V(1, 1), Navy, 0).rectTransform;
        panel.offsetMin = new Vector2(izquierda, 20);
        panel.offsetMax = new Vector2(-20, -20);
        panel.SetAsLastSibling();

        // ================= Visor (arriba izquierda) =================
        var visor = Panel("ViewerPanel", panel, V(0, 0.40f), V(0.495f, 1), Color.black, 5).rectTransform;
        Texto("ViewerTitle", visor, V(0.03f, 0.88f), V(0.97f, 0.99f), "Modelo 3D / mamografía", 16, 34, Color.white, TextAlignmentOptions.Left, true, 0);

        // ================= Panel derecho superior: tutor / retroalimentación =================
        var derecha = Nodo("RightTopPanel", panel, V(0.505f, 0.40f), V(1, 1), 0);

        var tutor = Panel("TutorPanel", derecha, V(0, 0), V(1, 1), Pink, 5).rectTransform;
        Texto("TutorTitle", tutor, V(0.04f, 0.86f), V(0.70f, 0.98f), "Agente tutor", 16, 30, Color.white, TextAlignmentOptions.Left, true, 0);
        Panel("TutorMascot", tutor, V(0.04f, 0.04f), V(0.40f, 0.66f), Hex("F4A6CF"), 0);   // reemplazar por la mascota (PNG de Figma)
        var burbuja = Panel("TutorBubble", tutor, V(0.40f, 0.36f), V(0.97f, 0.90f), PinkSoft, 0).rectTransform;
        var textoTutor = Texto("TutorText", burbuja, V(0, 0), V(1, 1), "Recomendación del agente", 14, 26, Hex("3A0A2A"), TextAlignmentOptions.Center, false, 14);

        var retro = Panel("FeedbackPanel", derecha, V(0, 0), V(1, 1), Navy2, 5).rectTransform;
        Texto("FeedbackTitle", retro, V(0.04f, 0.86f), V(0.96f, 0.98f), "Retroalimentación", 16, 30, Color.white, TextAlignmentOptions.Left, true, 0);
        var textoRetro = Texto("FeedbackText", retro, V(0.04f, 0.04f), V(0.96f, 0.84f), "...", 14, 26, Color.white, TextAlignmentOptions.TopLeft, false, 0);

        // ================= Panel de preguntas (centro-abajo) =================
        var qp = Panel("QuestionPanel", panel, V(0, 0.11f), V(1, 0.39f), Navy, 5).rectTransform;
        var progreso = Texto("ProgressText", qp, V(0.02f, 0.84f), V(0.77f, 0.98f), "Pregunta 1 de 8", 12, 22, Hex("FF7AC0"), TextAlignmentOptions.Left, true, 0);
        var enunciado = Texto("QuestionText", qp, V(0.02f, 0.58f), V(0.77f, 0.84f), "Enunciado de la pregunta", 14, 28, Color.white, TextAlignmentOptions.Left, true, 0);

        var grid = Nodo("OptionsGrid", qp, V(0.02f, 0.05f), V(0.77f, 0.55f), 0);
        Configurar(grid.gameObject.AddComponent<VerticalLayoutGroup>());
        var botones = new Button[4];
        var textos = new TMP_Text[4];
        for (int fila = 0; fila < 2; fila++)
        {
            var row = NodoLibre("Row" + (fila + 1), grid);
            Configurar(row.gameObject.AddComponent<HorizontalLayoutGroup>());
            for (int col = 0; col < 2; col++)
            {
                int i = fila * 2 + col;
                botones[i] = BotonOpcion("Option_" + "ABCD"[i], row, out var lbl);
                textos[i] = lbl;
            }
        }

        var estudio = Panel("StudyDataPanel", qp, V(0.79f, 0.05f), V(0.99f, 0.95f), Navy2, 0).rectTransform;
        Texto("StudyDataTitle", estudio, V(0.06f, 0.80f), V(0.94f, 0.96f), "Datos del estudio", 12, 22, Color.white, TextAlignmentOptions.Left, true, 0);
        var datosEstudio = Texto("StudyDataText", estudio, V(0.06f, 0.04f), V(0.94f, 0.78f), "...", 12, 22, Hex("FF7AC0"), TextAlignmentOptions.TopLeft, true, 0);

        // ================= Barra inferior =================
        var barra = Nodo("BottomBar", panel, V(0, 0), V(1, 0.10f), 0);

        var card = Panel("CaseInfoCard", barra, V(0, 0), V(0.30f, 1), Navy, 4).rectTransform;
        var numeroCaso = Texto("CaseNumberText", card, V(0.05f, 0.50f), V(0.95f, 0.96f), "Caso #001", 14, 26, Color.white, TextAlignmentOptions.Left, true, 0);
        var datosPaciente = Texto("PatientText", card, V(0.05f, 0.04f), V(0.95f, 0.52f), "Edad / mama", 10, 18, Color.white, TextAlignmentOptions.TopLeft, false, 0);

        var accion = Panel("ActionButton", barra, V(0.70f, 0.10f), V(1, 0.90f), Pink, 0);
        var botonAccion = accion.gameObject.AddComponent<Button>();
        botonAccion.targetGraphic = accion;
        botonAccion.transition = Selectable.Transition.None;
        var textoAccion = Texto("ActionLabel", accion.rectTransform, V(0, 0), V(1, 1), "Responder", 14, 28, Color.white, TextAlignmentOptions.Center, true, 8);

        // ================= Scripts y campos =================
        var qv = panel.gameObject.AddComponent<QuestionView>();
        Asignar(qv, "progreso", progreso);
        Asignar(qv, "enunciado", enunciado);
        AsignarArray(qv, "botonesOpcion", botones);
        AsignarArray(qv, "textosOpcion", textos);
        Asignar(qv, "botonAccion", botonAccion);
        Asignar(qv, "textoAccion", textoAccion);
        Asignar(qv, "panelTutor", tutor.gameObject);
        Asignar(qv, "textoTutor", textoTutor);
        Asignar(qv, "panelRetro", retro.gameObject);
        Asignar(qv, "textoRetro", textoRetro);

        var info = panel.gameObject.AddComponent<CaseInfoView>();
        Asignar(info, "numeroCaso", numeroCaso);
        Asignar(info, "datosPaciente", datosPaciente);
        Asignar(info, "datosEstudio", datosEstudio);

        var screen = panel.gameObject.AddComponent<SimulationScreen>();
        var ocultar = new List<GameObject>();
        foreach (Transform hijo in hud)
            if (hijo != nav && hijo != panel) ocultar.Add(hijo.gameObject);
        var caseCanvas = GameObject.Find("CaseCanvas");
        if (caseCanvas != null) ocultar.Add(caseCanvas);
        AsignarArray(screen, "pantallaCatalogo", ocultar.ToArray());

        // ================= Botón "Iniciar Simulación" =================
        var iniciar = hud.Find("DetailCasePanel/Button");
        if (iniciar != null && iniciar.TryGetComponent(out Button btn))
        {
            for (int i = btn.onClick.GetPersistentEventCount() - 1; i >= 0; i--)
                UnityEventTools.RemovePersistentListener(btn.onClick, i);
            UnityEventTools.AddStringPersistentListener(btn.onClick, screen.Abrir, "caso_001");
            EditorUtility.SetDirty(btn);
        }
        else
        {
            Debug.LogWarning("[MammoSim] No encontré DetailCasePanel/Button. Conecta a mano el OnClick a SimulationScreen.Abrir.");
        }

        panel.gameObject.SetActive(false);   // arranca apagado: la simulación lo enciende
        EditorSceneManager.MarkSceneDirty(SceneManager.GetActiveScene());
        Selection.activeGameObject = panel.gameObject;

        EditorUtility.DisplayDialog("MammoSim",
            "Pantalla creada.\n\nPara verla: selecciona SimulationPanel y marca la casilla de arriba a la izquierda del Inspector (desmárcala antes de dar Play).\n\nGuarda la escena con Ctrl+S.",
            "OK");
    }

    // ---------- GameManager y ApiClient ----------
    static void PrepararManagers()
    {
        var apiGo = GameObject.Find("ApiClient");
        if (apiGo == null) { apiGo = new GameObject("ApiClient"); Undo.RegisterCreatedObjectUndo(apiGo, "ApiClient"); }
        var api = apiGo.GetComponent<ApiClient>();
        if (api == null) api = Undo.AddComponent<ApiClient>(apiGo);

        var gmGo = GameObject.Find("GameManager");
        if (gmGo == null) { gmGo = new GameObject("GameManager"); Undo.RegisterCreatedObjectUndo(gmGo, "GameManager"); }
        var gm = gmGo.GetComponent<GameManager>();
        if (gm == null) gm = Undo.AddComponent<GameManager>(gmGo);

        Asignar(gm, "api", api);
    }

    // ---------- Ayudantes de construcción ----------
    static Vector2 V(float x, float y) => new Vector2(x, y);

    static Color Hex(string h)
    {
        ColorUtility.TryParseHtmlString("#" + h, out var c);
        return c;
    }

    static Sprite Redondeado() => AssetDatabase.GetBuiltinExtraResource<Sprite>("UI/Skin/UISprite.psd");

    static RectTransform NodoLibre(string nombre, Transform padre)
    {
        var go = new GameObject(nombre, typeof(RectTransform));
        Undo.RegisterCreatedObjectUndo(go, "Crear " + nombre);
        var rt = go.GetComponent<RectTransform>();
        rt.SetParent(padre, false);
        return rt;
    }

    static RectTransform Nodo(string nombre, Transform padre, Vector2 min, Vector2 max, float margen)
    {
        var rt = NodoLibre(nombre, padre);
        rt.anchorMin = min;
        rt.anchorMax = max;
        rt.offsetMin = new Vector2(margen, margen);
        rt.offsetMax = new Vector2(-margen, -margen);
        return rt;
    }

    static Image Panel(string nombre, Transform padre, Vector2 min, Vector2 max, Color color, float margen)
    {
        var rt = Nodo(nombre, padre, min, max, margen);
        var img = rt.gameObject.AddComponent<Image>();
        img.sprite = Redondeado();
        img.type = Image.Type.Sliced;
        img.color = color;
        return img;
    }

    static TextMeshProUGUI Texto(string nombre, Transform padre, Vector2 min, Vector2 max, string texto,
        float tamMin, float tamMax, Color color, TextAlignmentOptions alineacion, bool negrita, float margen)
    {
        var rt = Nodo(nombre, padre, min, max, margen);
        var t = rt.gameObject.AddComponent<TextMeshProUGUI>();
        t.text = texto;
        t.color = color;
        t.alignment = alineacion;
        t.enableAutoSizing = true;
        t.fontSizeMin = tamMin;
        t.fontSizeMax = tamMax;
        if (negrita) t.fontStyle = FontStyles.Bold;
        t.raycastTarget = false;   // para que los clics lleguen al botón que está debajo
        return t;
    }

    static Button BotonOpcion(string nombre, Transform padre, out TextMeshProUGUI label)
    {
        var rt = NodoLibre(nombre, padre);
        var img = rt.gameObject.AddComponent<Image>();
        img.sprite = Redondeado();
        img.type = Image.Type.Sliced;
        img.color = OptionBlue;
        var b = rt.gameObject.AddComponent<Button>();
        b.targetGraphic = img;
        b.transition = Selectable.Transition.None;   // el color lo pinta QuestionView
        label = Texto("Label", rt, V(0, 0), V(1, 1), "Opción", 14, 26, Color.white, TextAlignmentOptions.Left, false, 14);
        return b;
    }

    static void Configurar(HorizontalOrVerticalLayoutGroup g)
    {
        g.spacing = 10;
        g.childControlWidth = true;
        g.childControlHeight = true;
        g.childForceExpandWidth = true;
        g.childForceExpandHeight = true;
    }

    // Los campos de los scripts son [SerializeField] privados: se asignan por SerializedObject.
    static void Asignar(Object componente, string campo, Object valor)
    {
        var so = new SerializedObject(componente);
        so.FindProperty(campo).objectReferenceValue = valor;
        so.ApplyModifiedProperties();
    }

    static void AsignarArray(Object componente, string campo, Object[] valores)
    {
        var so = new SerializedObject(componente);
        var p = so.FindProperty(campo);
        p.arraySize = valores.Length;
        for (int i = 0; i < valores.Length; i++)
            p.GetArrayElementAtIndex(i).objectReferenceValue = valores[i];
        so.ApplyModifiedProperties();
    }
}
