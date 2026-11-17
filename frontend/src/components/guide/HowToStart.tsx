import { Link } from "react-router-dom";
import "../../styles/Guide.css";

export default function HowToStart() {
  return (
    <div className="how_to_start_content">
      <h2>¿Cómo iniciar una simulación?</h2>
      <ol>
        <li>Ve a Casos clínicos.</li>
        <li>Da click en "Ver detalle" del caso.</li>
        <li>Visualiza la información.</li>
        <li>Da click en "Iniciar simulación".</li>
        <li>
          Revisa el estudio, responde las preguntas y registra tu decisión
          inicial.
        </li>
        <li>Lee la recomendación del tutor y confirma o cambia tu decisión.</li>
        <li>Al terminar ve a "Historial" y visualiza el análisis de tu simulación.</li>
      </ol>
      <Link to="/cases" className="guide_cases_link">Ir a casos clínicos</Link>
    </div>
  );
}
