from fastapi import HTTPException, status


def pendiente():
    """Marca un endpoint que todavía no está programado."""
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, "Pendiente de implementar")
