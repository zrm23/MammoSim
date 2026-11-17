import type { SimulationHistory } from "../../types/SimulationHistory";

type AnalysisSummaryProps = {
  simulacion: SimulationHistory;
};

export default function AnalysisSummary({ simulacion }: AnalysisSummaryProps) {
  return (
    <div className="summary_container">
      <h3>Resumen del análisis</h3>
      <div className="table_wrap">
        <table className="summary_table">
          <tbody>
            <tr>
              <th scope="row">Caso analizado</th>
              <td>{simulacion.caseTitle}</td>
            </tr>
            <tr>
              <th scope="row">Resultado</th>
              <td>Descripción del resultado</td>
            </tr>
            <tr>
              <th scope="row">Puntuación</th>
              <td>{simulacion.score}/10</td>
            </tr>
            <tr>
              <th scope="row">Estado</th>
              <td>Completado</td>
            </tr>
            <tr>
              <th scope="row">Fecha y hora</th>
              <td>{simulacion.completedAt}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
