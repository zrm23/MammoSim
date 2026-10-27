import { useState } from "react";
import '../../styles/AuthPage.css';
import { Link } from "react-router-dom";

export default function ProfessorForm() {
  const [email, setEmail] = useState("");
  const [aceptado, setAceptado] = useState(false);
  return (
    <section className="auth">
      <h1>Crea tu cuenta</h1>
      <p>Registrate para comenzar a practicar</p>

      <form
        className="form_auth"
        onSubmit={(e) => {
          e.preventDefault();
        }}
      >
        <label htmlFor="name">Nombre completo</label>
        <input
            id="name"
            name="name"
            type="text"
            placeholder="Nombre y Apellido"
            required 
        />
        <label htmlFor="email">Correo Institucional</label>
        <input
          id="email"
          name="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="nombre@usc.edu.com"
          required
        />
        <label htmlFor="password">Contraseña</label>
        <input
          id="password"
          type="password"
          name="password"
          placeholder="******"
          autoComplete="current-password"
          required
        />

        <label className="">
          <input
            type="checkbox"
            checked={aceptado}
            onChange={(e) => setAceptado(e.target.checked)}
          />
          <span>
            Acepto el tratamiento de mis datos personales y los terminos de uso
            academico de la Universidad Santiago de Cali.
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
          Registrarse
        </button>

        <p>¿Ya tienes una cuenta? <Link to="/auth">Inicia Sesión</Link></p>
      </form>
    </section>
  );
}
