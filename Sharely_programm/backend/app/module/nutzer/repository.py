"""Datenbankzugriffe des Moduls nutzer: MongoDB-Collection `nutzer`.

Nur hier wird die Collection gelesen und geschrieben. Die Verbindung kommt aus
app/core/datenbank.py. Die Sitzungen (Collection `sitzungen`) verwaltet
app/core/sicherheit.py, weil jeder Endpunkt sie über `aktueller_nutzer` prüft.
"""

from datetime import datetime

from bson import ObjectId

from app.core.datenbank import get_db

COLLECTION = "nutzer"

# Groß-/Kleinschreibung egal: „AnnaK“ und „annak“ gelten als derselbe Nutzername.
OHNE_GROSS_KLEIN = {"locale": "de", "strength": 2}


def _collection():
    return get_db()[COLLECTION]


async def finden(nutzer_id: str) -> dict | None:
    return await _collection().find_one({"_id": ObjectId(nutzer_id)})


async def finden_per_nutzername(nutzername: str) -> dict | None:
    return await _collection().find_one({"nutzername": nutzername}, collation=OHNE_GROSS_KLEIN)


async def finden_per_email(email: str) -> dict | None:
    return await _collection().find_one({"email": email})


async def anlegen(daten: dict) -> str:
    """Neuen Nutzer speichern. Doppelte E-Mail oder doppelter Nutzername löst über
    die eindeutigen Indizes `DuplicateKeyError` aus."""
    ergebnis = await _collection().insert_one(daten)
    return str(ergebnis.inserted_id)


async def profilbild_setzen(nutzer_id: str, bild_pfad: str | None, geaendert_am: datetime) -> None:
    await _collection().update_one(
        {"_id": ObjectId(nutzer_id)}, {"$set": {"profilbild_pfad": bild_pfad, "geaendert_am": geaendert_am}}
    )
