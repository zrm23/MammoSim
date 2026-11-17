export type SimulationHistory = {
  simulationId: string;
  caseId: string;
  caseTitle: string;
  completedAt: string;
  imgUrl: string;
  score: number;
  questions: HistoryQuestion[];
};

export type HistoryQuestion = {
  number: number;
  statement: string;
  selectedAnswer: string;
};
