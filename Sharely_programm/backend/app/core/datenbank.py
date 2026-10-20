"""MongoDB-Verbindung. Wird beim Start der App geöffnet und beim Beenden geschlossen.

Zugriff in den Modulen: `from app.core.datenbank import get_db`, dann
`get_db()["collection_name"]`.
"""

from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.config import get_settings

_client: AsyncMongoClient | None = None


def verbinden() -> None:
    global _client
    # tz_aware: Zeitpunkte kommen als UTC mit Zeitzone zurück, nicht "naiv"
    _client = AsyncMongoClient(get_settings().mongodb_url, tz_aware=True)


async def trennen() -> None:
    global _client
    if _client is not None:
        await _client.close()
        _client = None


def get_db() -> AsyncDatabase:
    if _client is None:
        raise RuntimeError("Keine Datenbankverbindung: verbinden() wurde nicht aufgerufen.")
    return _client[get_settings().mongodb_datenbank]
