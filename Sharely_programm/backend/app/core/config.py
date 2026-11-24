"""Einstellungen aus Umgebungsvariablen bzw. der Datei Sharely_programm/backend/.env (Vorlage: .env.example).

Warum eine eigene Datei für Einstellungen? Manche Werte sind auf jedem Rechner anders
(z. B. die Adresse der Datenbank) oder geheim (Passwörter, Zugangsschlüssel). Sie stehen
deshalb nicht im Code, sondern in der Datei .env, die nicht ins Git-Repo hochgeladen wird.
Hier steht nur, WELCHE Einstellungen es gibt und welchen Wert sie haben, wenn in .env nichts steht.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Alle Einstellungen der App. Jede Zeile „name: typ = wert“ ist eine Einstellung mit Standardwert.
    Steht in .env z. B. MONGODB_URL=…, wird automatisch dieser Wert statt des Standards benutzt."""

    # Woher die Werte kommen: aus der Datei .env (im Ordner, in dem das Backend gestartet wird)
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Sharely"
    # Adresse der MongoDB-Datenbank (lokal oder bei MongoDB Atlas im Internet)
    mongodb_url: str = "mongodb://localhost:27017"
    # Name der Datenbank innerhalb von MongoDB
    mongodb_datenbank: str = "sharely"
    # Wo die Bilder liegen (app/core/bildspeicher.py): "bucket" = Railway Storage Bucket, den
    # alle gemeinsam nutzen (Vorgabe seit 24.11.2026, Christian); "ordner" = upload_ordner auf
    # diesem Rechner, nur für Tests oder Arbeiten ohne Netz
    bildspeicher: str = "bucket"
    upload_ordner: str = "../uploads"
    # Zugang zum Bucket (nur bei bildspeicher="bucket"; Werte aus Railway, nie ins Repo)
    # Ein „Bucket“ ist ein Online-Speicher für Dateien, ähnlich einem Cloud-Ordner.
    bucket_name: str = ""
    bucket_endpoint: str = ""
    bucket_region: str = "auto"
    bucket_access_key_id: str = ""
    bucket_secret_access_key: str = ""
    # Nur True, wenn der Reiter „Credentials“ des Buckets in Railway Path-Style verlangt
    bucket_pfad_stil: bool = False
    # Größte erlaubte Bilddatei beim Hochladen (User Story 8)
    max_bild_mb: int = 10
    # Speicher für Bilder je Nutzer (Kleidungsfotos + Profilbild), Vorschlag Christian 24.11.2026
    max_speicher_mb_pro_nutzer: int = 1024
    # Adressen, von denen das Frontend im Browser zugreifen darf (CORS, siehe main.py)
    frontend_urls: list[str] = ["http://localhost:5173"]
    # Höchstdauer einer Anmeldung (danach löscht MongoDB die Sitzung). Das Cookie selbst
    # endet schon, wenn der Browser geschlossen wird (Entscheidung Katha, 27.10.2026).
    sitzung_stunden: int = 8
    # Sitzungs-Cookie nur über HTTPS senden; lokal (http://localhost) muss es False sein
    # (HTTPS = verschlüsselte Verbindung, erkennbar am Schloss im Browser)
    cookie_secure: bool = False


# @lru_cache merkt sich das Ergebnis: Die .env-Datei wird nur beim ersten Aufruf gelesen,
# danach bekommt jeder Aufruf dieselben, schon geladenen Einstellungen zurück.
@lru_cache
def get_settings() -> Settings:
    return Settings()
