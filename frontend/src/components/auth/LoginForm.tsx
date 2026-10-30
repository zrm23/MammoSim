import TypeUserButton from "../ButtonUser";
import "../../styles/AuthPage.css";
import { useState } from "react";
import { Link } from "react-router-dom";
import type { UserType } from "../../pages/LoginPage";

type LoginFormProps = {
  userType: UserType;
  onUserTypeChange: (type: UserType) => void;
};

export default function LoginForm({
  userType,
  onUserTypeChange,
}: LoginFormProps) {
  const isProfessor = userType === "docente";
  const [aceptado, setAceptado] = useState(false);

  return (
    <div className="auth_access">
      <TypeUserButton userType={userType} onUserTypeChange={onUserTypeChange} />
      <section className="auth">
        <h1>Accede a tu cuenta</h1>
        <p>Para comenzar a practicar</p>
      </section>

      <section className="auth_page_panel">
        <form className="form_auth">
          <label>
            {isProfessor
              ? "Correo electrónico institucional"
              : "Correo electrónico"}
          </label>
          <input
            id="email"
            name="email"
            type="email"
            placeholder="nombre@correo.com"
            required
          />
          <label>Contraseña</label>
          <input
            id="password"
            name="password"
            type="password"
            placeholder="*******"
            required
          />
          <label>
            <input
              type="checkbox"
              checked={aceptado}
              onChange={(e) => setAceptado(e.target.checked)}
            />
            <span>
              Acepto el tratamiento de mis datos personales y los terminos de
              uso academico de la Universidad Santiago de Cali.
            </span>
          </label>
          <button
            type="submit"
            disabled={!aceptado}
            style={{
              width: "100%",
              borderRadius: 12,
              border: "none",
              padding: 10,
              fontSize: 18,
              fontWeight: "bold",
              backgroundColor: aceptado ? "#E6397E" : "#D6DCE3",
              cursor: aceptado ? "pointer" : "not-allowed",
            }}
          >
            Iniciar
          </button>
          <p className="auth_link">
            ¿Ya tienes una cuenta?<Link to="/register"> Registrate </Link>
          </p>
        </form>
      </section>
    </div>
  );
}
