"""Reglas de los cursos."""
import secrets

# Sin letras ni números que se confundan (O/0, I/1/L) para que sea fácil de escribir.
ALFABETO = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"


def generar_codigo() -> str:
    """Código que el estudiante escribe para unirse, por ejemplo MS-K7P2QX."""
    return "MS-" + "".join(secrets.choice(ALFABETO) for _ in range(6))
