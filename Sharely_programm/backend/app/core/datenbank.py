"""MongoDB-Verbindung. Wird beim Start der App geöffnet und beim Beenden geschlossen.

MongoDB ist unsere Datenbank. Sie speichert Daten als „Dokumente“ (ähnlich wie Karteikarten
mit Feldern wie name, farbe, preis), sortiert in „Collections“ (ähnlich wie Karteikästen,
z. B. eine für Nutzer und eine für Kleidungsstücke).

Zugriff in den Modulen: `from app.core.datenbank import get_db`, dann
`get_db()["collection_name"]`.
"""

from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.config import get_settings

# Die eine Verbindung zur Datenbank, die sich die ganze App teilt.
# „None“ heißt: noch nicht verbunden. Der Unterstrich am Anfang heißt: nur in dieser Datei benutzen.
_client: AsyncMongoClient | None = None


def verbinden() -> None:
    """Verbindung zur Datenbank öffnen (beim Start der App, siehe main.py)."""
    global _client  # „global“: wir ändern die Variable oben, nicht eine neue innerhalb der Funktion
    # tz_aware: Zeitpunkte kommen als UTC mit Zeitzone zurück, nicht "naiv"
    _client = AsyncMongoClient(get_settings().mongodb_url, tz_aware=True)


async def trennen() -> None:
    """Verbindung schließen (beim Beenden der App)."""
    global _client
    if _client is not None:
        await _client.close()
        _client = None


def get_db() -> AsyncDatabase:
    """Die Datenbank zurückgeben, mit der die Module arbeiten. Fehler, falls noch nicht verbunden."""
    if _client is None:
        raise RuntimeError("Keine Datenbankverbindung: verbinden() wurde nicht aufgerufen.")
    return _client[get_settings().mongodb_datenbank]
