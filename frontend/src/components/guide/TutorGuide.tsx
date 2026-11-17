import "../../styles/Guide.css";
import bot from "../../assets/bot.png";
export default function TutorGuide() {
  return (
    <div className="tutor_guide">
      <div className="tittle_bot">
        <img src={bot} alt="Bot" />
        <h2>¿Cómo interactuar con el Agente Tutor?</h2>
      </div>
      <p>
        MammoSim está diseñado para evaluar tu pensamiento crítico. El agente
        tutor de IA te dará una recomendación.
      </p>
      <p>
        Ojo: La IA puede equivocarse o tener sesgos intencionales. Tu objetivo
        no es estar siempre de acuerdo con la máquina, sino analizar su
        justificación y mantener o corregir tu criterio clínico.
      </p>
    </div>
  );
}
