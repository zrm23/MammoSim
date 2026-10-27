import { useState } from "react";
import "../../styles/AuthPage.css";
import { Link } from "react-router-dom";

const Facultades = [
  "Salud",
  "Ingeniería",
  "Ciencias Económicas y Empresariales",
  "Ciencias Básicas",
  "Humanidades y Artes",
  "Ciencias Políticas",
  "Derecho",
  "Educación",
  "No aplica",
];

const Semestres = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, "No aplica"
]

export default function StudentForm() {
  const [email, setEmail] = useState("");
  const [aceptado, setAceptado] = useState(false);
  const [facultad, setFacultad] = useState("");
  const [semester, setSemester] = useState("");

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

        <label htmlFor="email">Correo electrónico</label>
        <input
          id="email"
          name="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="nombre@correo.com"
          required
        />

        <label htmlFor="facultad">Facultad</label>
        <select
          id="facultad"
          value={facultad}
          onChange={(e) => setFacultad(e.target.value)}
          required
        >
          <option value="" disabled>Seleccione su facultad</option>
          {Facultades.map((facultad) => (
            <option key={facultad} value={facultad}>{facultad}</option>
          ))}
        </select>

        <label>Semestre</label>
        <select
          id="semestre"
          value={semester}
          onChange={(e) => setSemester(e.target.value)}
          required
        >
          <option value="" disabled>Seleccione su semestre</option>
          {Semestres.map((semestre) => (
            <option key={semestre} value={semestre}>{semestre}</option>
          ))}
        </select>
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
          Iniciar
        </button>

        <p>¿Ya tienes una cuenta? <Link to="/auth">Inicia Sesión</Link></p>
      </form>
    </section>
  );
}
