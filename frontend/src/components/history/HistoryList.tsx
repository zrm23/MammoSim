import type { SimulationHistory } from "../../types/SimulationHistory";
import HistoryCard from "./HistoryCard";
import '../../styles/History.css';


type HistoryListProps = {
    simulations: SimulationHistory[];
    onSelectSimulation: (simulation: SimulationHistory) => void;
}

export default function HistoryList({simulations, onSelectSimulation}:HistoryListProps){
    if (simulations.length === 0) {
        return <p>Aún no se han realizado simulaciones</p>
    }
    return(
        <div className="history_list">
            {simulations.map((simulation)=>(
                <HistoryCard key={simulation.simulationId} simulation={simulation} onSelect={onSelectSimulation}/>
            ))}
        </div>
    );
}