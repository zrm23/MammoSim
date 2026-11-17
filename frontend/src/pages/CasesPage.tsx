import { useState } from "react";
import CaseCatalog from "../components/cases/CaseCatalog";
import { mockCases } from "../components/data/mockCases";
import "../styles/CasesCatalog.css";
import "../styles/CaseDetails.css";
import CaseDetails from "../components/cases/CaseDetails";
import type { clinicalCase } from "../types/ClinicalCase";
import Sidebar from "../components/layout/Sidebar";
import "../styles/Sidebar.css";
import PageHeader from "../components/layout/PageHeader";

export default function CasesPage() {
  const cases = mockCases;
  const [selectedCase, setSelectedCase] = useState<clinicalCase | null>(null);
  return (
    <div className="sidebar_container">
      <Sidebar />
      <main className="content">
      <PageHeader/>
        {cases.length === 0 ? (
          <p>No hay casos disponibles en el momento</p>
        ) : (
          <div className="cases_container">
            <CaseCatalog cases={mockCases} onSelectCase={setSelectedCase} />
            {selectedCase && <CaseDetails clinicalCase={selectedCase} />}{" "}
          </div>
        )}
      </main>
    </div>
  );
}
