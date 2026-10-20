"""Datenbankzugriffe des Moduls nutzer: MongoDB-Collection `nutzer`.

Nur hier wird die Collection gelesen und geschrieben. Die Verbindung kommt aus
app/core/datenbank.py.
"""

from bson import ObjectId

from app.core.datenbank import get_db

COLLECTION = "nutzer"


def _collection():
    return get_db()[COLLECTION]


async def finden(nutzer_id: str) -> dict | None:
    return await _collection().find_one({"_id": ObjectId(nutzer_id)})


async def profilbild_setzen(nutzer_id: str, bild_pfad: str | None) -> None:
    """upsert, weil es den Test-Nutzer (core/sicherheit.py) noch nicht in der Collection
    gibt. Mit der echten Registrierung existiert der Eintrag immer schon."""
    await _collection().update_one(
        {"_id": ObjectId(nutzer_id)}, {"$set": {"profilbild_pfad": bild_pfad}}, upsert=True
    )
