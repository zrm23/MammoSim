import { TriangleAlertIcon } from "lucide-react";

export default function AcademicAlert() {
  return (
    <div className="alert_content">
      <TriangleAlertIcon className="icon"/>
      <h1>Aviso Legal y Académico</h1>
      <p>
        Esta plataforma es un entorno de simulación estrictamente académico y
        experimental. Los casos presentados utilizan datos públicos
        anonimizados.
      </p>
      <p>MammoSim no es un dispositivo médico y sus resultados no
        sustituyen el juicio clínico real.</p>
    </div>
  );
}
