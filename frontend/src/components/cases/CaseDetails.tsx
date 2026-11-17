
import type { clinicalCase } from "../../types/ClinicalCase";
import "../../styles/CaseDetails.css";
import { useState } from "react";
import UnitySimulation from "../simulation/UnitySimulation";

type CaseDetailsProps = {
  clinicalCase: clinicalCase;
};

export default function CaseDetails({
  clinicalCase,
}: CaseDetailsProps) {
  const [started, setStarted] = useState(false);

  return (
    <aside className="detail_container">
      <h2>{clinicalCase.id}</h2>
      <h4>{clinicalCase.title}</h4>

      <img
        src={clinicalCase.imgUrl}
        alt="mamografía"
        width={250}
      />

      <h4>Descripción del caso</h4>
      <p>{clinicalCase.descripcion_breve}</p>

      <p>Objetivos de aprendizaje</p>

      <button
        type="button"
        className="start_sim"
        onClick={() => setStarted(true)}
      >
        <span>Iniciar Simulación</span>
      </button>

      {started && (
        <UnitySimulation
        caseId={clinicalCase.id}
        onClose={() => setStarted(false)}
      />
      )}
    </aside>
  );
}
