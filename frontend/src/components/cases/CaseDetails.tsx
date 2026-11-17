
import type { clinicalCase } from "../../types/ClinicalCase";
import "../../styles/CaseDetails.css";
import { Unity, useUnityContext } from "react-unity-webgl";
import { useEffect, useState } from "react";

type CaseDetailsProps = {
  clinicalCase: clinicalCase;
};

export default function CaseDetails({ clinicalCase }: CaseDetailsProps) {
  const [started, setStarted] = useState(false);

  const {
    unityProvider,
    isLoaded,
    loadingProgression,
    sendMessage,
  } = useUnityContext({
    loaderUrl: "/build/myunityapp.loader.js",
    dataUrl: "/build/myunityapp.data",
    frameworkUrl: "/build/myunityapp.framework.js",
    codeUrl: "/build/myunityapp.wasm",
  });

  const startSimulation = () => {
    setStarted(true);
  };

  useEffect(() => {
    if (started && isLoaded) {
      sendMessage("SimulationManager", "StartSimulation");
    }
  }, [started, isLoaded, sendMessage]);

  return (
    <aside className="detail_container">
      <h2>{clinicalCase.clinical_id}</h2>
      <h4>{clinicalCase.title}</h4>

      <img
        src={clinicalCase.imgUrl}
        alt="mamografía"
        width={250}
      />

      <h4>Descripción del caso</h4>
      <p>{clinicalCase.descripcion_breve}</p>

      <p>Objetivos de aprendizaje</p>

      {!started && (
        <button
          type="button"
          className="start_sim"
          onClick={startSimulation}
        >
          <span>Iniciar Simulación</span>
        </button>
      )}

      {started && (
        <div className="simulation_container">
          {!isLoaded && (
            <p>
              Cargando Simulación...
              {Math.round(loadingProgression * 100)}%
            </p>
          )}

          <Unity
            unityProvider={unityProvider}
            style={{ width: "100%", height: 600 }}
          />
        </div>
      )}
    </aside>
  );
}
