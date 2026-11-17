import type { birads } from "../../types/ClinicalCase";

type BiradsReferencesProps = {
    birads: birads[];
}

export default function BiradsReferences({birads}:BiradsReferencesProps){

    return(
        <div className="birads">
            <h2>Clasificación BI-RADS</h2>
            {birads.map((birad)=>(
                <p>{birad.id}: {birad.descripcion}</p>
            ))}
        </div>
    );
}