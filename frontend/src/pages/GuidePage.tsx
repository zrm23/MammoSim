import AcademicAlert from "../components/guide/AcademicAlert";
import BiradsReferences from "../components/guide/BiradsReferences";
import TutorGuide from "../components/guide/TutorGuide";
import Sidebar from "../components/layout/Sidebar";
import { biradsReferences } from "../components/data/biradsReferences";
import HowToStart from "../components/guide/HowToStart";
export default function GuidePage() {
  return (
    <div className="sidebar_container">
      <Sidebar />
      <main className="guide_main">
        <h1 className="tittle">Guía de Usuario y Referencia Clínica</h1>
        <section className="guide_container">
          <div className="guide_content">
            <TutorGuide />
            <BiradsReferences birads={biradsReferences} />
          </div>
          <div className="guide_right">
            <div  className="alert_container">
              <AcademicAlert />
            </div>
            <section className="start_simulation_container">
              <HowToStart />
            </section>
          </div>
        </section>
      </main>
    </div>
  );
}
