# MammoSim — Endpoints del backend (FastAPI)

La API tiene 21 endpoints que cubren todo el recorrido del estudiante y la vista del docente; el cliente (Unity WebGL y la web) solo habla con FastAPI, y FastAPI es lo único que toca Firestore.

## Resumen y convenciones

- **Autenticación.** Todos los endpoints exigen el encabezado `Authorization: Bearer <token de Firebase Auth>`. El backend verifica el token y saca de él el `uid` y el correo; el cliente nunca envía su propio `id_usuario`.
- **Roles.** `estudiante` o `docente`, leído de `usuarios/{uid}`. Un rol incorrecto responde 403.
- **Formato.** JSON en ambos sentidos; fechas en formato ISO 8601; los campos llevan los mismos nombres que en Firestore.
- **Errores comunes.** 401 token inválido o ausente · 403 rol o dueño incorrecto · 404 no existe · 409 el estado no lo permite o el documento ya existe · 422 el cuerpo no es válido.
- **Nunca sale del servidor** antes de tiempo: la `respuesta_correcta` de las preguntas aún no contestadas, la respuesta correcta de la decisión, `opcion_ia_incorrecta`, las recomendaciones de la IA que no correspondan, `hallazgos` y `retroalimentacion`. La `explicacion` y la respuesta correcta de cada pregunta técnica salen en el momento de contestarla; lo demás, al terminar el caso.
- **Documentos inmutables.** `respuestas`, `decisiones_iniciales` y `decisiones_finales` se crean una sola vez; repetir la escritura responde 409, así que no se puede volver a contestar una pregunta para ver la respuesta.
- **Orden dentro de un caso** (el servidor lo hace cumplir):
  1. Responder las 7 preguntas técnicas.
  2. Enviar la decisión inicial.
  3. Pedir la recomendación de la IA.
  4. Enviar la decisión final.
  5. Ver la retroalimentación y la nota del caso.
- **Nota del caso (0 a 10)** = (preguntas acertadas + 0,5 si la inicial fue buena + 0,5 si la final fue buena) × 1,25. La de la sesión es el promedio de sus casos (fórmula completa en la guía de la base de datos).

**Modo examen.** Cuando el estudiante empieza una sesión no puede salirse ni repetirla: solo puede tener una sesión `en_curso` a la vez (`POST /sesiones` responde 409 si ya hay una) y no puede cerrarla a medias. Si cierra la ventana, solo puede continuar la misma con `GET /sesiones/activa`, sin poder volver a contestar lo ya respondido. Un caso solo se puede leer dentro de una sesión activa que lo incluya (endpoint 9), así no se consultan las preguntas fuera del examen.

## 1. Usuarios

El registro crea el documento de `usuarios` y decide el rol; después el cliente puede leer su propio perfil.

| # | Endpoint | Rol | Qué recibe | Qué hace y responde |
| --- | --- | --- | --- | --- |
| 1 | `POST /auth/registro` | Cualquiera con token nuevo | `nombre_completo`, `carrera`, `semestre` (o `null`), `acepto_terminos` (debe ser `true`) | Toma `uid` y correo del token. Si el correo está en `docentes_autorizados` con `activo: true`, el rol es `docente`; si no, `estudiante` (con aviso si el correo es institucional). Crea `usuarios/{uid}` con `fecha_aceptacion` y `fecha_registro`. Responde 201 con el perfil y el aviso. Errores: 409 si ya está registrado, 422 si no aceptó los términos. |
| 2 | `GET /usuarios/me` | Cualquiera registrado | Nada | Devuelve el perfil del usuario que inició sesión. 404 si todavía no se registró. |

## 2. Cursos e inscripciones

Un docente tiene un solo curso con un solo código; un estudiante puede unirse a varios cursos, salirse y volver a entrar.

| # | Endpoint | Rol | Qué recibe | Qué hace y responde |
| --- | --- | --- | --- | --- |
| 3 | `POST /cursos` | Docente | `nombre` | Crea el curso con `id_docente` = su `uid` y un `codigo` único generado por el servidor (ej. `GPTI-2026B`). Responde 201 con el curso. 409 si el docente ya tiene curso. |
| 4 | `GET /cursos/mio` | Docente | Nada | Devuelve su curso y su código. 404 si todavía no lo ha creado. |
| 5 | `POST /inscripciones` | Estudiante | `codigo` | Busca el curso por `codigo`. Crea `inscripciones/{uid}_{id_curso}` con `activo: true`, o la reactiva si existía. Responde con el curso. 404 si el código no existe. |
| 6 | `DELETE /inscripciones/{id_curso}` | Estudiante | Nada | Pone `activo: false`; el historial se conserva. 404 si no estaba inscrito. |
| 7 | `GET /inscripciones/mias` | Estudiante | Nada | Lista los cursos donde `activo` es `true`, con nombre y código. |

## 3. Casos

Los casos son contenido fijo; el servidor los entrega sin ningún campo que revele la respuesta.

| # | Endpoint | Rol | Qué recibe | Qué hace y responde |
| --- | --- | --- | --- | --- |
| 8 | `GET /casos` | Cualquiera registrado | Nada | Lista los 7 casos con `id_caso`, `titulo`, `descripcion_breve`, `lado`, `vistas`, `dificultad` y `modelo_3d_ref`. |
| 9 | `GET /casos/{id_caso}` | Cualquiera registrado | Nada | Devuelve el caso para resolverlo: `datos_estudio`, `edad_simulada`, las 7 `preguntas` (solo `numero`, `enunciado` y `opciones`), `enunciado_decision` y `opciones_decision`. Se quitan `respuesta_correcta` (del caso y de cada pregunta), `explicacion`, `opcion_ia_incorrecta`, las recomendaciones de la IA, `hallazgos` y `retroalimentacion`. Solo se entrega si el caso está en una sesión en_curso del estudiante (403 si no). 404 si no existe. |

## 4. Sesiones

Una sesión es cada vez que un estudiante practica; puede pertenecer a un curso o ser práctica libre.

| # | Endpoint | Rol | Qué recibe | Qué hace y responde |
| --- | --- | --- | --- | --- |
| 10 | `POST /sesiones` | Estudiante | `id_curso` (o `null` si practica solo) y casos (lista de id_caso elegidos, mínimo 1) | Si trae `id_curso`, comprueba que la inscripción esté activa (403 si no). Crea `sesiones/{id}` con `estado: en_curso`, `casos_asignados` (los que elija el estudiante) y `fecha_inicio`. Responde 201 con la sesión. 409 si ya tiene una sesión en curso. |
| 11 | `GET /sesiones/mias` | Estudiante | Opcional: `id_curso` | Historial del estudiante, de la más reciente a la más antigua (usa el índice compuesto `id_usuario` + `fecha_inicio`). Incluye las prácticas libres. |
| 12 | `POST /sesiones/{id}/cerrar` | Estudiante dueño | Nada | Pasa `estado` a `completada`, guarda `fecha_fin`, calcula y crea `resultados/{id_sesion}` (aciertos, uso de la IA y `puntuacion`). 403 si la sesión no es suya, 409 si ya estaba completada o si aún falta terminar algún caso (no se puede cerrar a medias). |
| 21 | GET /sesiones/activa | Estudiante | Nada | Devuelve la sesión en_curso del estudiante, con los casos ya terminados y el caso donde va, para continuar la misma si cerró la ventana. 404 si no tiene una. |

## 5. Dentro de un caso

Todas las rutas cuelgan de `/sesiones/{id}/casos/{id_caso}`, exigen que la sesión sea del estudiante, esté `en_curso` y el caso esté en `casos_asignados` (403 o 422 si no). La explicación de cada pregunta técnica se muestra al contestarla; la decisión, la IA y los hallazgos, al final del caso.

| # | Endpoint | Qué recibe | Qué hace y responde |
| --- | --- | --- | --- |
| 13 | `POST .../respuestas` | `numero_pregunta` (1 a 7), `opcion_elegida` (A a D) | Crea `respuestas/{id_sesion}_{id_caso}_p{n}` con `correcta` calculada por el servidor. Responde 201 con `correcta`, la `respuesta_correcta` y la `explicacion` de esa pregunta (la del Excel: por qué es correcta, o por qué es incorrecta y cuál era la respuesta), para mostrarla de inmediato. 409 si esa pregunta ya se respondió, así no se puede repetir para copiar la respuesta. |
| 14 | `POST .../decision-inicial` | `decision` (`biopsiar`, `seguimiento`, `ignorar` o `estudio_adicional`) | Exige las 7 respuestas del caso (409 si faltan). Crea `decisiones_iniciales/{id_sesion}_{id_caso}` con `acierto` calculado. Responde 201 `{guardada: true}`. |
| 15 | `GET .../recomendacion-ia` | Nada | Solo después de la decisión inicial (409 si no existe). Si la inicial fue buena, devuelve `la opcion_ia (la incorrecta fija)` con `recomendacion_ia_incorrecta`; si fue mala, devuelve la opción correcta con `recomendacion_ia_correcta`. Es determinista y no escribe nada; nunca dice si la recomendación es la correcta. |
| 16 | `POST .../decision-final` | `decision` | Exige la decisión inicial (409 si no). Recalcula en el servidor qué recomendó la IA y crea `decisiones_finales/{id_sesion}_{id_caso}` con `decision`, `acierto`, `opcion_ia`, `ia_correcta` y `siguio_ia`. Se guarda siempre, aunque no cambie de opinión. Responde 201 `{guardada: true}`. |
| 17 | `GET .../retroalimentacion` | Nada | Solo después de la decisión final (409 si no). Devuelve `hallazgos`, `retroalimentacion`, la `respuesta_correcta` del caso, por cada pregunta si acertó (la explicación ya se mostró al contestarla), si la recomendación de la IA era correcta y la **nota del caso** (0 a 10) con su desglose. La nota se calcula al vuelo y no se guarda. |

## 6. Resultados y vista del docente

El docente solo ve las sesiones cuyo `id_curso` es el de su curso; lo hecho antes de unirse o practicando solo no aparece.

| # | Endpoint | Rol | Qué recibe | Qué hace y responde |
| --- | --- | --- | --- | --- |
| 18 | `GET /sesiones/{id}/resultado` | Estudiante dueño | Nada | Devuelve `resultados/{id}`: totales, aciertos iniciales y finales, uso de la IA y `puntuacion`. 409 si la sesión aún no está completada. |
| 19 | `GET /cursos/mio/sesiones` | Docente | Opcional: página y filtro por estudiante | Lista las sesiones de su curso (`id_curso` = el suyo) con nombre del estudiante, `estado`, `fecha_inicio` y `puntuacion`. Puede pedir un índice compuesto en `sesiones` (`id_curso` + `fecha_inicio`); Firebase muestra el enlace para crearlo. |
| 20 | `GET /cursos/mio/sesiones/{id}` | Docente | Nada | Detalle de una sesión de su curso: respuestas, decisiones inicial y final, `siguio_ia` y nota de cada caso. 404 si la sesión no es de su curso. |
