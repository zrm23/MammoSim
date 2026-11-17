"""Configuración: se lee de variables de entorno o del archivo .env."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    firebase_project_id: str = "mammosim"
    # Ruta a la llave de la cuenta de servicio. Si está vacía se usan las
    # credenciales por defecto del entorno (útil en Render).
    google_application_credentials: str | None = None
    cors_origins: str = "http://localhost:5173"

    @property
    def origenes_permitidos(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
