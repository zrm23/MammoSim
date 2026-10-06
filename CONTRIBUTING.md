# Flujo de trabajo

Los cambios del proyecto deben realizarse mediante ramas de trabajo y Pull Request

### Ramas

Seguirán una convencións según el tipo de trabajo 

- `feature/` - Nuevas funcionalidades
- `fix/` - Correcciones
- `docs/` - Documentación
- `test/` - Pruebas
- `experiment/` - Experimentos con la IA

### Pull Request

Los cambios destinados a `main` deberán realizarse mediante Pull Request.

Antes de realizar el merge validar que: 
- El cambio corresponda a una tarea o Issue
- Las pruebas correspondientes fueron ejecutadas
- La documentación necesaria fue actualizada
- El Pull Request fue revisado

### Commits

Los mensajes de los commits deben describir claramente el cambio realizado y siguiendo una estructura convencional: 
 - <tipo>(<alcance opcional>): <descripción clara>

- [cuerpo opcional: explicación detallada de la razón del cambio y el 'por qué']

- [pie de página opcional: referencias a tareas, issues o breaking changes]

### Tipos de commits 
- feat: Una nueva funcionalidad (feature)
- fix: Corrección de un error o bug
- docs: Cambios exclusivamente en la documentación
- style: Cambios que no afectan el significado del código como espacios, formato, comas faltantes, etc...
- refactor: Cambio en el código que no corrige un bug ni añade una funcionalidad (reestructuración)
- perf: Cambio en el código que mejora el rendimiento (performance)
- test: Añadir pruebas faltantes o corregir pruebas existentes
- chore: Tareas de mantenimiento, actualización de dependencias o configuración sin tocar código de producción