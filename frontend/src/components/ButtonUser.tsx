import type { UserType } from "../pages/RegisterPage";
import "../styles/ButtonUser.css";

type TypeUserButtonProps = {
  userType: UserType;
  onUserTypeChange: (type: UserType) => void;
};

export default function TypeUserButton({
  userType,
  onUserTypeChange,
}: TypeUserButtonProps) {
  return (
    <div className="type_user">
      <button
        type="button"
        className="type_user_color"
        aria-pressed={userType === "estudiante"}
        onClick={() => onUserTypeChange("estudiante")}
      >
        Estudiante
      </button>
      <button
        type="button"
        className="type_user_color"
        aria-pressed={userType === "docente"}
        onClick={() => onUserTypeChange("docente")}
      >
        Docente
      </button>
    </div>
  );
}
