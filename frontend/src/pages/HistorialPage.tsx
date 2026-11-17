import HistoryList from "../components/history/HistoryList";
import Sidebar from "../components/layout/Sidebar";
import "../styles/CasesCatalog.css";
import type { SimulationHistory } from "../types/SimulationHistory";
import "../styles/History.css";
import { useState } from "react";
import HistoryDetails from "../components/history/HistoryDetails";

export default function HistorialPage() {
  const exampleSimulation: SimulationHistory[] = [
    {
      simulationId: "sim-001",
      caseId: "caso-001",
      caseTitle: "Caso de práctica 1",
      completedAt: "2026-11-05T10:00:00-05:00",
      imgUrl: "",
      score: 8,
      questions: [
        {
          number: 1,
          statement: "Pregunta de prueba 1",
          selectedAnswer: "Opción A",
        },
        {
          number: 2,
          statement: "Pregunta de prueba 2",
          selectedAnswer: "Opción C",
        },
        {
          number: 3,
          statement: "Pregunta de prueba 2",
          selectedAnswer: "Opción C",
        },
        {
          number: 4,
          statement: "Pregunta de prueba 2",
          selectedAnswer: "Opción C",
        },
        {
          number: 5,
          statement: "Pregunta de prueba 2",
          selectedAnswer: "Opción C",
        },
        {
          number: 6,
          statement: "Pregunta de prueba 2",
          selectedAnswer: "Opción C",
        },
        
      ],
    },
  ];

  const [selectedSimulation, setSelectedSimulation] =
    useState<SimulationHistory | null>(null);

  return (
    <div className="sidebar_container">
      <Sidebar />
      <main className="history_container">
        {selectedSimulation ? (
          <div>
            <HistoryDetails
              simulation={selectedSimulation}
              onBack={() => setSelectedSimulation(null)}
            />
          </div>
        ) : (
          <HistoryList
            simulations={exampleSimulation}
            onSelectSimulation={setSelectedSimulation}
          />
        )}
      </main>
    </div>
  );
}
