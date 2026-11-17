"""Conexión a Firebase (Firestore y Authentication) con firebase-admin."""
import firebase_admin
from firebase_admin import credentials, firestore

from app.config import get_settings


def init_firebase() -> None:
    """Inicia firebase-admin una sola vez."""
    if firebase_admin._apps:
        return
    settings = get_settings()
    if settings.google_application_credentials:
        cred = credentials.Certificate(settings.google_application_credentials)
    else:
        cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {"projectId": settings.firebase_project_id})


def get_db():
    """Dependencia de FastAPI: entrega el cliente de Firestore.

    En las pruebas se reemplaza por una base falsa (ver tests/conftest.py).
    """
    init_firebase()
    return firestore.client()
