
import { Unity, useUnityContext } from "react-unity-webgl";
import { useEffect, useRef, useState } from "react";
import "../../styles/UnitySimulation.css";

type UnitySimulationProps = {
  caseId: string;
  onClose: () => void;
};

export default function UnitySimulation({
  caseId,
  onClose,
}: UnitySimulationProps) {
  const [closing, setClosing] = useState(false);

  const {
    unityProvider,
    isLoaded,
    loadingProgression,
    unload,
    sendMessage,
  } = useUnityContext({
    loaderUrl: "/unity-build/Build/Builds.loader.js",
    dataUrl: "/unity-build/Build/Builds.data.br",
    frameworkUrl: "/unity-build/Build/Builds.framework.js.br",
    codeUrl: "/unity-build/Build/Builds.wasm.br",
  });
  console.log("Caso recibido desde React:", caseId);
  const casoIniciado = useRef(false);

useEffect(() => {
  if (isLoaded && !casoIniciado.current) {
    casoIniciado.current = true;

    const unityCaseId = (caseId || "caso_001").replace("-", "_");

    console.log("MammoSim: iniciando", unityCaseId);

    sendMessage("WebBridge", "IniciarCaso", unityCaseId);
  }
}, [isLoaded, sendMessage, caseId]);
  const handleClose = async () => {
    if (closing) return;

    setClosing(true);

    try {
      if (isLoaded) {
        await unload();
      }
      onClose();
    } catch (error) {
      console.error("Error al cerrar Unity:", error);
      setClosing(false);
    }
  };

  return (
    <div
      className="unity_overlay"
      role="dialog"
      aria-modal="true"
      aria-label="Simulación MammoSim"
    >
      <div className="unity_header">
        <h2>MammoSim - Simulación clínica</h2>

        <button
          type="button"
          onClick={handleClose}
          disabled={closing}
        >
          {closing ? "Cerrando..." : "Cerrar simulación"}
        </button>
      </div>

      <div className="unity_content">
        {!isLoaded && (
          <p className="unity_loading">
            Cargando simulación...
            {Math.round(loadingProgression * 100)}%
          </p>
        )}

        <Unity
          unityProvider={unityProvider}
          className="unity_canvas"
          tabIndex={0}
        />
      </div>
    </div>
  );
}
