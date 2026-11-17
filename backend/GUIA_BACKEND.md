# Backend de MammoSim (FastAPI) — guía rápida

## Cómo correrlo (PowerShell, dentro de la carpeta `backend`)
```
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env      # luego edita .env con la ruta a TU llave de Firebase
uvicorn app.main:app --reload
```
- API en http://localhost:8000 y documentación automática en http://localhost:8000/docs
- Pruebas: `pytest` (no necesitan Firebase ni la llave)

Antes de subir nada, confirma con `git status` que no aparezca `.venv`, `.env` ni ninguna llave.

## Cómo está organizado
| Carpeta / archivo | Para qué sirve |
|---|---|
| `app/main.py` | Crea la app, CORS y registra las rutas |
| `app/config.py` | Lee las variables de entorno (`.env`) |
| `app/firebase.py` | Conexión a Firestore (`get_db`) |
| `app/auth.py` | Verifica el token de Firebase y el rol (`requiere_estudiante`, `requiere_docente`) |
| `app/schemas.py` | Modelos que validan lo que entra y sale |
| `app/routers/` | Los 21 endpoints, agrupados |
| `app/services/` | Lógica sin Firebase, ya probada: `tutor.py`, `puntuacion.py`, `casos.py` |
| `tests/` | Pruebas |

## Qué está hecho y qué falta
- Hecho y probado: tutor (opción A), nota del caso, puntuación de la sesión, qué se oculta del caso, mensaje de cada pregunta técnica.
- Hechos como ejemplo: `GET /usuarios/me` y `GET /casos`.
- Pendientes: los demás endpoints devuelven **501**. Cada uno trae un `TODO` con las reglas de la lista de endpoints.

## Cómo programar un endpoint
1. Abre su función en `app/routers/` y lee el `TODO`.
2. Borra `pendiente()` y escribe la lógica con `db.collection("...")`.
3. Si hay cálculo (tutor, nota, qué mostrar), usa lo de `app/services/`; no lo repitas.
4. Agrega una prueba en `tests/`. La base falsa de `tests/conftest.py` permite probar sin Firebase.
5. `pytest` debe seguir en verde.

## Reglas que no se pueden romper
- El `uid` y el correo salen del token, nunca del cuerpo de la petición.
- Nunca enviar al cliente `respuesta_correcta`, `opcion_ia_incorrecta`, hallazgos ni retroalimentación antes de tiempo (usa `app/services/casos.py`).
- `respuestas`, `decisiones_iniciales` y `decisiones_finales` se crean una sola vez (repetir = 409).
