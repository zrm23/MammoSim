import { useState } from "react";
import RegisterForm from "../components/auth/RegisterForm";
import "../styles/AuthPage.css";

export type UserType = "estudiante" | "docente";

export default function RegisterPage() { 
const [userType, serUserType] = useState<UserType>("estudiante");

  return (
    <main className="auth_page">
      <section className="auth_welcome">
        <h1>{userType === "estudiante" ? "¡Bienvenido estudiante!": "¡Bienvenido docente!"}</h1>
        <h4>
          Accede a la simulación de casos clínicos e interactúa con nuestro
          agente tutor con IA
        </h4>
      </section>
      <section className="auth_page_panel">
        <RegisterForm userType={userType} onUserTypeChange={serUserType}/>
      </section>
    </main>
  );
}
