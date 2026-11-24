"""Einstellungen aus Umgebungsvariablen bzw. der Datei Sharely_programm/backend/.env (Vorlage: .env.example)."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Sharely"
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_datenbank: str = "sharely"
    # Wo die Bilder liegen (app/core/bildspeicher.py): "ordner" = upload_ordner auf diesem
    # Rechner, "bucket" = Railway Storage Bucket, den alle gemeinsam nutzen (24.11.2026)
    bildspeicher: str = "ordner"
    # Ordner für hochgeladene Bilder, je Nutzer ein Unterordner (siehe Technische Konzeption 2.2)
    upload_ordner: str = "../uploads"
    # Zugang zum Bucket (nur bei bildspeicher="bucket"; Werte aus Railway, nie ins Repo)
    bucket_name: str = ""
    bucket_endpoint: str = ""
    bucket_region: str = "auto"
    bucket_access_key_id: str = ""
    bucket_secret_access_key: str = ""
    # Nur True, wenn der Reiter „Credentials“ des Buckets in Railway Path-Style verlangt
    bucket_pfad_stil: bool = False
    # Größte erlaubte Bilddatei beim Hochladen (User Story 8)
    max_bild_mb: int = 10
    # Adressen, von denen das Frontend im Browser zugreifen darf (CORS)
    frontend_urls: list[str] = ["http://localhost:5173"]
    # Höchstdauer einer Anmeldung (danach löscht MongoDB die Sitzung). Das Cookie selbst
    # endet schon, wenn der Browser geschlossen wird (Entscheidung Katha, 27.10.2026).
    sitzung_stunden: int = 8
    # Sitzungs-Cookie nur über HTTPS senden; lokal (http://localhost) muss es False sein
    cookie_secure: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
