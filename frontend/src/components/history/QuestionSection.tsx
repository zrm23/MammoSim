import type { HistoryQuestion } from "../../types/SimulationHistory";

type QuestionSectionProps = {
  questions: HistoryQuestion[];
  selectedNumber: number | null;
  onSelect: (question: HistoryQuestion) => void;
};

export default function QuestionSection({
  questions,
  selectedNumber,
  onSelect,
}: QuestionSectionProps) {
  return (
    <div className="question_content">
      <h3>Preguntas del caso</h3>
      {questions.map((question) => (
        <button
          key={question.number}
          type="button"
          onClick={() => onSelect(question)}
          aria-pressed={selectedNumber === question.number}
          className="button_question"
        >
          Pregunta {question.number} : {question.statement}
        </button>
      ))}
    </div>
  );
}
