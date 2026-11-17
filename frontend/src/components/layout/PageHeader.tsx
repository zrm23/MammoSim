import UserProfileSummary from "./UserProfileSummary";
import "../../styles/Header.css";

export default function PageHeader() {
  return (
    <header className="header_container">
      <div style={{ flex: 1, minWidth: 0 }}>
        <h1>Selecciona un caso clínico</h1>
        <p>
          Cada caso presenta una situación clinica diferente para desarrollar
          tus habilidades de análisis, decisión y uso de la IA
        </p>
      </div>
      <div className="profile_container">
        <UserProfileSummary name="Zaira Ramírez Mejía " carrera="Ingeniería de Sistemas" avatarColor="#FFC1DA" />
      </div>
    </header>
  );
}
