"""Einstellungen aus Umgebungsvariablen bzw. der Datei backend/.env (Vorlage: .env.example)."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Sharely"
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_datenbank: str = "sharely"
    # Ordner für hochgeladene Bilder, je Nutzer ein Unterordner (siehe Technische Konzeption 2.2)
    upload_ordner: str = "../uploads"
    # Größte erlaubte Bilddatei beim Hochladen (User Story 8)
    max_bild_mb: int = 10
    # Adressen, von denen das Frontend im Browser zugreifen darf (CORS)
    frontend_urls: list[str] = ["http://localhost:5173"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
