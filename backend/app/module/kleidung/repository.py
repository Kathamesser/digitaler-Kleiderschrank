"""Datenbankzugriffe des Moduls kleidung: MongoDB-Collection `kleidungsstuecke`.

Nur hier wird die Collection gelesen und geschrieben. Die Verbindung kommt aus
app/core/datenbank.py.
"""

from bson import ObjectId
from bson.errors import InvalidId

from app.core.datenbank import get_db

COLLECTION = "kleidungsstuecke"


def _collection():
    return get_db()[COLLECTION]


def _als_dict(dokument: dict) -> dict:
    """MongoDB-Dokument → einfaches dict, alle Verweise (`…_id`) als Text."""
    dokument = dict(dokument)
    dokument["id"] = str(dokument.pop("_id"))
    dokument["nutzer_id"] = str(dokument["nutzer_id"])
    dokument["kategorie_ids"] = [str(k) for k in dokument.get("kategorie_ids", [])]
    if dokument.get("leihvorgang_id") is not None:
        dokument["leihvorgang_id"] = str(dokument["leihvorgang_id"])
    return dokument


async def anlegen(daten: dict) -> dict:
    """Verweise werden als ObjectId gespeichert (ERM, Reiter „MongoDB“)."""
    daten = {
        **daten,
        "nutzer_id": ObjectId(daten["nutzer_id"]),
        "kategorie_ids": [ObjectId(k) for k in daten.get("kategorie_ids", [])],
    }
    if daten.get("leihvorgang_id") is not None:
        daten["leihvorgang_id"] = ObjectId(daten["leihvorgang_id"])
    ergebnis = await _collection().insert_one(daten)
    return _als_dict({**daten, "_id": ergebnis.inserted_id})


async def finden(kleidungsstueck_id: str, nutzer_id: str) -> dict | None:
    """Ein Kleidungsstück des Nutzers, oder None (auch bei ungültiger ID)."""
    try:
        oid = ObjectId(kleidungsstueck_id)
    except InvalidId:
        return None
    dokument = await _collection().find_one({"_id": oid, "nutzer_id": ObjectId(nutzer_id)})
    return _als_dict(dokument) if dokument else None


async def alle_des_nutzers(nutzer_id: str) -> list[dict]:
    """Alle Kleidungsstücke des Nutzers, neueste zuerst."""
    zeiger = _collection().find({"nutzer_id": ObjectId(nutzer_id)}).sort("erstellt_am", -1)
    return [_als_dict(d) async for d in zeiger]
