# MammoSim: esquema de la base de datos (Firestore), versión de implementación

Proyecto Firebase `mammosim`, región southamerica-east1. Solo el backend (FastAPI con firebase-admin) lee y escribe; las reglas de seguridad niegan todo acceso desde clientes.

Cambios respecto al informe entregado (25-10-26):
- Las decisiones pasan de una colección `decisiones` con campo `tipo` a **dos colecciones**: `decisiones_iniciales` y `decisiones_finales`.
- `edad_paciente` se reemplaza por `edad_simulada`.
- Un estudiante puede estar en **varios cursos** (puede entrar, salirse y cambiarse); cada docente tiene **un solo curso con un solo código**. La pertenencia a cursos vive en la colección nueva `inscripciones`, y `usuarios` ya no guarda el curso.
- `sesiones.id_curso` indica en qué curso se hizo la sesión (`null` = practicó solo).
- `usuarios`: `alias` pasa a `nombre_completo`, `carrera_facultad` pasa a `carrera`, y se agregan `acepto_terminos` y `fecha_aceptacion`.
- `resultados` agrega `puntuacion` (sobre 10).

## Contenido fijo (lo carga el equipo desde la consola o con `cargar_casos.py`)

### casos_clinicos  (ID: caso_001 a caso_007)
| Campo | Tipo | Nota |
|---|---|---|
| id_caso | string | igual al ID del documento |
| titulo | string | texto de la tarjeta |
| descripcion_breve | string | panel derecho; no revela la respuesta |
| lado | string | izquierda o derecha |
| vistas | array | ["CC","MLO"] o ["MLO"] |
| dificultad | string | facil, medio o dificil |
| edad_simulada | number | dato ficticio, marcado como simulado |
| modelo_3d_ref | string | archivo .glb sin extensión |
| datos_estudio | array de strings | líneas de "Datos del estudio" del panel: cada caso muestra solo lo que sus preguntas necesitan |
| preguntas | array de 7 mapas | numero, enunciado, opciones {A,B,C,D}, respuesta_correcta (letra), explicacion |
| enunciado_decision | string | pregunta diagnóstica |
| opciones_decision | array de 4 | {valor, texto} en el orden en que se muestran |
| hallazgos | string | se muestra al final |
| respuesta_correcta | string | biopsiar, seguimiento, ignorar o estudio_adicional |
| recomendacion_ia_correcta | string | la IA lo dice si el estudiante falló |
| opcion_ia_incorrecta | string | opción incorrecta fija que defiende la IA si el estudiante acertó |
| recomendacion_ia_incorrecta | string | texto de esa recomendación |
| retroalimentacion | string | se muestra al terminar el caso |
| fuente | string | CBIS-DDSM, paciente, licencia |

El servidor **no envía** al cliente: `respuesta_correcta` (del caso y de cada pregunta) ni `opcion_ia_incorrecta`. Las preguntas técnicas van dentro del caso (un arreglo), no como colección aparte. La IA recomienda solo en la decisión final (no en las preguntas técnicas).

### docentes_autorizados  (ID: correo institucional en minúsculas)
Documento `{ "activo": true }`. Hoy solo está `jairsanclemente00@usc.edu.co`. Si alguien se registra con correo institucional que no está en la lista, se registra como estudiante con aviso.

## Lo que escribe FastAPI durante el uso

### usuarios  (ID: uid de Firebase Authentication)
| Campo | Tipo | Nota |
|---|---|---|
| id_usuario | string | igual al ID |
| nombre_completo | string | se pide al registrarse |
| correo | string | estudiante: cualquier correo; docente: institucional |
| rol | string | estudiante o docente; solo lo asigna el servicio |
| carrera | string | texto libre |
| semestre | number | solo estudiantes; `null` si no aplica |
| acepto_terminos | boolean | autorización de tratamiento de datos (Ley 1581 de 2012) |
| fecha_aceptacion | timestamp | cuándo aceptó |
| fecha_registro | timestamp | |

El curso del estudiante **no** se guarda aquí: está en `inscripciones`.

### cursos  (ID automático)
| Campo | Tipo | Nota |
|---|---|---|
| codigo | string | el que escribe el estudiante para unirse (ej. GPTI-2026B); único |
| nombre | string | |
| id_docente | string | uid del docente; un solo curso por docente |
| fecha_creacion | timestamp | |

### inscripciones  (ID: {id_usuario}_{id_curso})
| Campo | Tipo | Nota |
|---|---|---|
| id_usuario | string | |
| id_curso | string | |
| activo | boolean | false si se salió del curso (se conserva el historial) |
| fecha_union | timestamp | |

Unirse: el estudiante escribe el código, el backend busca el curso por `codigo` y crea (o reactiva) la inscripción. Salirse: `activo` pasa a false.

### sesiones  (ID automático)
| Campo | Tipo | Nota |
|---|---|---|
| id_sesion | string | |
| id_usuario | string | |
| id_curso | string o null | curso elegido al empezar; `null` = practicó solo |
| casos_asignados | array | IDs de los casos |
| estado | string | `en_curso` o `completada` |
| fecha_inicio, fecha_fin | timestamp | |

Practicar solo también queda en el historial del estudiante. El docente solo ve las sesiones cuyo `id_curso` es el de su curso; lo hecho antes de unirse o practicando solo no aparece.

### respuestas  (ID: {id_sesion}_{id_caso}_p{n})
id_sesion, id_usuario, id_caso, numero_pregunta (1 a 7), opcion_elegida, correcta (la calcula el servicio), fecha. Se crean una sola vez. La colección aparece en la consola cuando se guarda la primera respuesta.

### decisiones_iniciales  (ID: {id_sesion}_{id_caso})
id_sesion, id_usuario, id_caso, decision, acierto, fecha. Se crean una sola vez.

### decisiones_finales  (ID: {id_sesion}_{id_caso})
Los mismos campos más **opcion_ia** (lo que mostró la IA), **ia_correcta** (si era la correcta) y **siguio_ia** (si el estudiante eligió lo que dijo la IA). Se crean una sola vez.

### resultados  (ID: igual al de la sesión)
id_usuario, id_curso, total_casos, aciertos_iniciales, aciertos_finales, preguntas_acertadas, veces_siguio_ia, siguio_ia_correcta, siguio_ia_incorrecta, **puntuacion** (number, sobre 10; ver «Cómo se calcula la puntuación»), fecha_calculo.

## Cómo se calcula la puntuación
Cada caso vale 8 puntos de 1,25 cada uno (8 × 1,25 = 10): 7 preguntas técnicas y la decisión. La decisión vale 1,25 repartido en dos mitades: inicial 0,625 y final 0,625.

| Decisión inicial | Decisión final | Puntos de la decisión |
|---|---|---|
| Buena | Buena | 1,25 |
| Buena | Mala (la cambió por la IA) | 0,625 |
| Mala | Buena (la IA la corrigió) | 0,625 |
| Mala | Mala | 0 |

La nota de cada caso se calcula al vuelo con sus `respuestas` y sus decisiones (no se guarda) y se muestra al terminar el caso. La de la sesión es el promedio de los casos y se guarda en `resultados.puntuacion`:

```
puntuacion = (preguntas_acertadas + 0.5 × aciertos_iniciales + 0.5 × aciertos_finales) / (8 × total_casos) × 10
```

Ejemplo: 3 casos, 18 preguntas acertadas, 2 decisiones iniciales y 2 finales correctas → (18 + 1 + 1) / 24 × 10 = 8,33. Siempre se guardan las dos decisiones (inicial y final), aunque el estudiante no cambie de opinión.

## Valores permitidos de decision
biopsiar, seguimiento, ignorar, estudio_adicional.

## Consultas e índices
- Historial del estudiante: sesiones por id_usuario ordenado por fecha_inicio descendente → **índice compuesto** (ya creado en la consola).
- Sesiones de un curso (vista del docente): sesiones por id_curso, probablemente ordenadas por fecha → puede pedir un índice compuesto; Firebase muestra un enlace que lo crea.
- Detalle de una sesión: respuestas, decisiones_iniciales y decisiones_finales por id_sesion → índice automático.
- Todo lo demás: lectura por ID o filtro por un solo campo → automático.

Una sesión completa escribe unos 65 documentos: 49 respuestas + 14 decisiones + sesión + resultado.

## Reglas de seguridad
Denegar toda lectura y escritura desde clientes. Solo FastAPI accede con firebase-admin. La llave de la cuenta de servicio no va a GitHub ni al chat; se guarda en una variable de entorno o en `.env`, y cada persona genera la suya.

## Datos de ejemplo (borrar cuando haya datos reales)
`sesiones/ses_prueba_001`, `resultados/ses_prueba_001`, `decisiones_iniciales/ses_prueba_001_caso_001`, `decisiones_finales/ses_prueba_001_caso_001`, `usuarios/uid de Firebase Authentication`, `cursos/curso_prueba_001` e `inscripciones/uid_prueba_001_curso_prueba_001`.

## Cómo cargar los casos
1. `pip install firebase-admin`
2. Guardar la clave de cuenta de servicio en el computador (nunca en el chat ni en GitHub) y pasar su ruta con `--clave`, o apuntar a ella:
   `export GOOGLE_APPLICATION_CREDENTIALS=/ruta/clave.json`  (en Windows: `set GOOGLE_APPLICATION_CREDENTIALS=C:\ruta\clave.json`)
3. `python cargar_casos.py` valida sin escribir.
4. `python cargar_casos.py --listar --clave "ruta\clave.json"` muestra las colecciones actuales.
5. `python cargar_casos.py --escribir --clave "ruta\clave.json"` escribe los 7 casos (reemplaza los documentos completos, así desaparece `edad_paciente`).
6. Agregar correos en `docentes_autorizados.json` y correr con `--escribir --docentes`.
7. Al terminar, eliminar la llave en Firebase (Cuentas de servicio → Claves) y borrar el archivo.
