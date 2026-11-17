import { NavLink } from "react-router-dom";
import "../../styles/Sidebar.css";
import { BookUser, FolderOpen, Settings, StickyNotes } from "lucide-react";
import LogoutButton from "../auth/LogoutButton";
import logo from '../../assets/Logo-bg.png';
export default function Sidebar() {
  return (
    <nav className="sidebar" aria-label="Menú principal">
      <div className="logo_container">
        <img src={logo} alt="MammoSim"/>
        <h5>Simulador de casos clínicos</h5>
      </div>
      <ul>
        <li>
          <NavLink to="/cases">
            <FolderOpen className="icons" />
            <span>Casos Clínicos</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/historial">
            <StickyNotes className="icons"/>
            <span>Historial</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/guide">
            <BookUser className="icons"/>
            <span>Guía</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/setting">
            <Settings className="icons"/>
            <span>Ajustes</span>
          </NavLink>
        </li>
      </ul>
      <div className="sidebar_footer">
        <LogoutButton />
      </div>
    </nav>
  );
}
