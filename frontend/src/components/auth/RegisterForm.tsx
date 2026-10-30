import TypeUserButton from "../ButtonUser";
import "../../styles/AuthPage.css";
import type { UserType } from "../../pages/RegisterPage";
import StudentForm from "./StudentRegisterForm";
import ProfessorForm from "./ProfessorRegisterForm";


type RegisterFormProps = {
  userType: UserType;
  onUserTypeChange: (type: UserType) => void; 
};


export default function RegisterForm({userType, onUserTypeChange}: RegisterFormProps) {

  return (
    <div className="auth_access">
        <TypeUserButton userType={userType} onUserTypeChange={onUserTypeChange}/>
      {userType === "estudiante" ? (
        <StudentForm/>
      ) : (
        <ProfessorForm/>
      )}
    </div>
  );
}
