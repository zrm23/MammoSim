import { useState } from "react";
import RegisterForm from "../components/auth/RegisterForm";
import "../styles/AuthPage.css";
import Logo from "../assets/Logo-bg.png";

export type UserType = "estudiante" | "docente";

export default function RegisterPage() {
  const [userType, setUserType] = useState<UserType>("estudiante");

  return (
    <main className="auth_page">
      <section className="auth_welcome">
        <img src={Logo} alt="MammoSim Logo" className="logo" width={250} />
        <h1>
          {userType === "estudiante"
            ? "¡Crea tu cuenta estudiante!"
            : "¡Crea tu cuenta docente!"}
        </h1>
        <h4>
          {userType === "estudiante"
            ? "Para acceder a la simulación de casos clínicos e interactuar con nuestro agente tutor con IA"
            : "Para acceder al historial de la simulación de casos clínicos de tus estudiantes"}
        </h4>
      </section>
      <section className="auth_page_panel">
        <RegisterForm userType={userType} onUserTypeChange={setUserType} />
      </section>
    </main>
  );
}
