import type {
  HistoryQuestion,
  SimulationHistory,
} from "../../types/SimulationHistory";
import HistoryCard from "./HistoryCard";
import QuestionSection from "./QuestionSection";
import "../../styles/History.css";
import AnalysisSummary from "./AnalysisSummary";
import { useState } from "react";

type HistoryDetailsProps = {
  simulation: SimulationHistory;
  onBack: () => void;
};

export default function HistoryDetails({
  simulation,
  onBack,
}: HistoryDetailsProps) {
  const [selectedQuestion, setSelectedQuestion] =
    useState<HistoryQuestion | null>(null);

  const [showDecision, setShowDecision] = useState(false);
  return (
    <section className="history_details">
      <HistoryCard
        simulation={simulation}
        onSelect={() => {}}
        showDetailButton={false}
      />
      <div className="history_details_columns">
        <section className="questions_summary">
          {showDecision ? (
            <>
              <h2>Interacción con el agente tutor</h2>
              <p>
                Observa la recomendacion del agente, tu decision y como se
                evaluo
              </p>
              <div>
                <h3>Respuesta inicial del estudiante</h3>
                <p>Pregunta </p>
                <p>Respuesta {simulation.score}</p>
              </div>
              <div>
                <h2>Recomendación del agente tutor</h2>
                <p>recomendacion</p>
              </div>
              <div>
                <h3>Decisión final del estudiante</h3>
                <p>Respuesta {simulation.score}</p>
              </div>
            </>
          ) : selectedQuestion ? (
            <>
              <h3>Pregunta {selectedQuestion.number}</h3>
              <p>{selectedQuestion.statement}</p>
              <p>Respuesta registrada: {selectedQuestion.selectedAnswer}</p>
            </>
          ) : (
            <p>Selecciona una pregunta</p>
          )}
        </section>

        <div className="history_details_right">
          <AnalysisSummary simulacion={simulation} />
          <section className="question_container">
            <QuestionSection
              questions={simulation.questions}
              selectedNumber={selectedQuestion?.number ?? null}
              onSelect={(question) => {
                setSelectedQuestion(question);
                setShowDecision(false);
              }}
            />
            <button
              type="button"
              aria-pressed={showDecision}
              onClick={() => {
                setSelectedQuestion(null);
                setShowDecision(true);
              }}
              className="button_question"
            >
              Decisión final
            </button>
          </section>
        </div>
      </div>
      <div style={{display: "flex", justifyContent:"end"}}>
        <button type="button" onClick={onBack} className="back_button">
          Volver al historial
        </button>
      </div>
    </section>
  );
}
