import { LogOut } from "lucide-react";
import "../../styles/Sidebar.css";

export default function LogoutButton() {
  return (
    <button type="button" className="sidebar_logout">
      <LogOut className="icons" aria-hidden="true"/>
      <span>Cerrar Sesión</span>
    </button> 
  );
}
