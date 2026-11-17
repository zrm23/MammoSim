import type { clinicalCase } from "../../types/ClinicalCase";
import CaseCard from "./CaseCard";
import "../../styles/CasesCatalog.css";
import { useState } from "react";
import { CircleChevronLeft, CircleChevronRight } from "lucide-react";

type CaseCatalogProps = {
  cases: clinicalCase[];
  onSelectCase: (selectedCase: clinicalCase) => void;
};

export default function CaseCatalog({ cases, onSelectCase }: CaseCatalogProps) {
  const [currentCase, setCurrentCase] = useState(0);
  const totalCases = Math.ceil(cases.length / 3);

  const visibleCases = cases.slice(currentCase * 3, currentCase * 3 + 3);

  const previousPage = () => {
    setCurrentCase((page) => (page - 1 + totalCases) % totalCases);
  };

  const nextPage = () => {
    setCurrentCase((page) => (page + 1 + totalCases) % totalCases);
  };

  return (
    <div className="catalog_container">
      <div className="cases_catalog">
        {visibleCases.map((clinicalCase) => (
          <CaseCard
            key={clinicalCase.id}
            clinicalCase={clinicalCase}
            onSelect={onSelectCase}
          />
        ))}
      </div>
      <div className="catalog_buttons">
        <button
          type="button"
          className="buttons_left_right"
          aria-label="Página anterior"
          onClick={previousPage}
          disabled={totalCases <= 1}
        >
          <CircleChevronLeft aria-hidden="true" />
        </button>
        <div className="carousel">
          {Array.from({ length: totalCases }, (_, index) => (
            <button
              key={index}
              type="button"
              aria-label={`Ver página ${index + 1}`}
              aria-pressed={currentCase === index}
              onClick={() => setCurrentCase(index)}
            />
          ))}
        </div>
        <button
          type="button"
          className="buttons_left_right"
          aria-label="Página siguiente"
          onClick={nextPage}
          disabled={totalCases <= 1}
        >
          <CircleChevronRight aria-hidden="true" />
        </button>
      </div>
    </div>
  );
}
