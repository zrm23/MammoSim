export type clinicalCase = {
    clinical_id: string;
    title: string; 
    imgUrl:string;
    dificultad: "baja" | "media" | "alta";
    pacientAge: number;
    descripcion_breve: string;
    imagingStudy: string;
};

export type birads = {
    id: string;
    descripcion: string;
}