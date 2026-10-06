# MammoSim
Simulador web de carácter académico y experimental para el entrenamiento y evaluación de la toma de decisiones humano-IA en escenarios de cáncer de mama

# Estado del proyecto
En desarrollo 

# Objetivo
Desarrollar un simulador web (MammoSim) de carácter académico y experimental, mediante casos clínicos e imágenes de cáncer de mama con retroalimentación de un agente tutor inteligente, aplicando las guías PMBOK y TSP, para la evaluación del desempeño del usuario en la toma de decisiones, su capacidad de identificación de errores de la IA y su independencia frente a las recomendaciones de esta, sin sustituir el criterio del profesional clínico.

# Alcance del proyecto
Simulador web: donde el usuario se registrará, seleccionará el caso, consultará la información del caso, visualizará la imagen médica correspondiente y tomará las decisiones frente al caso. 

Agente tutor: se desarrollará para el proyecto con el fin de generar recomendaciones y retroalimentaciones durante la simulación. En ciertas secciones de los escenarios, se proporcionarán decisiones incorrectas de forma que se evalúe la capacidad del usuario de identificar las falencias de la IA y cuestionar, aceptar o rechazar las recomendaciones de este. 

Integración mediante API: la comunicación entre el simulador y el agente será mediante API facilitando así las posibles modificaciones que se presenten en un futuro. 

Registro de interacción humano-IA: se guardará la detección e interpretación registrada por el usuario durante la simulación para la evaluación en la interacción humano-IA. 

Evaluación del desempeño: se comparará la decisión del usuario con la respuesta clínica correcta definida para el caso y las recomendaciones del agente para generar información y evaluar el desempeño del usuario y la interacción humano-IA 

Historial y visualización de resultados: el usuario podrá consultar el historial de los casos evaluados y los resultados obtenidos, así como también las decisiones y la retroalimentación recibida. 

Pruebas y validación: se realizarán diferentes tipos de pruebas como funcionales de integración y usabilidad para verificar el funcionamiento del simulador. 

Casos clínicos e imágenes médicas: los datos presentados en cada caso serán públicos anonimizados. 

# Uso académico

*"MammoSim se desarrolla únicamente con fines adémicos y experimentales"*

# Estructura del proyecto

```text
MammoSim/
├── .github/ 
├── docs/
├── frontend/
├── backend/
├── ml/
├── test/
├── infra/
├── scripts/
├── .gitignore
└── README.md

