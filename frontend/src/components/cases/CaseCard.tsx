import type { clinicalCase } from "../../types/ClinicalCase";
import "../../styles/CasesCatalog.css";

type CaseCardProps = {
  clinicalCase: clinicalCase;
  onSelect: (selectedCase: clinicalCase) => void;
};

export default function CaseCard({ clinicalCase, onSelect }: CaseCardProps) {
  const dificultad =
    clinicalCase.dificultad === "baja"
      ? "#22C55E"
      : clinicalCase.dificultad === "media"
        ? "#F5B301"
        : "#EF4444";

  
  return (
    <article className="card">
      <h2>{clinicalCase.id}</h2>
      <img src={clinicalCase.imgUrl} alt="mamografía" width={100} />
      <p style={{ color: dificultad }}>Dificultad: {clinicalCase.dificultad}</p>
      <h3>{clinicalCase.title} </h3>
      <p>
        Edad estimada del paciente: <br /> {clinicalCase.pacientAge}
      </p>
      <p>
        Tipo de estudio: <br /> {clinicalCase.imagingStudy}
      </p>
      <button type="button" className="detail_button" onClick={() => onSelect(clinicalCase)}>Ver detalle</button>
    </article>
  );
}
