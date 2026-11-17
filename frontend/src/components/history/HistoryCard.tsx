import type { SimulationHistory } from "../../types/SimulationHistory";

type HistoryCardProps = {
  simulation: SimulationHistory;
  onSelect: (simulation: SimulationHistory) => void;
  showDetailButton?: boolean;
};
export default function HistoryCard({
  simulation,
  onSelect,
  showDetailButton = true,
}: HistoryCardProps) {
  return (
    <article className="history_card">
      <div>
        <h1>{simulation.simulationId}</h1>
        <p>
          Fecha de realizacion:{" "}
          {new Date(simulation.completedAt).toLocaleString("es-CO")}
        </p>
      </div>
      <div>
        <img
          src={simulation.imgUrl}
          alt={`Vista previa de ${simulation.caseTitle}`}
          width={80}
        />
      </div>
      <div className="history_detail_case">
        <h4>Resultado de simulación: {simulation.score}/10</h4>
        {showDetailButton && (
          <button type="button" onClick={() => onSelect(simulation)}>
            Ver detalle
          </button>
        )}
      </div>
    </article>
  );
}
