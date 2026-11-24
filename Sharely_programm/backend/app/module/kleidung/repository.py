"""Datenbankzugriffe des Moduls kleidung: MongoDB-Collection `kleidungsstuecke`.

Nur hier wird die Collection gelesen und geschrieben. Die Verbindung kommt aus
app/core/datenbank.py.

Wichtig für die Sicherheit: Jede Suche enthält auch die nutzer_id. So findet ein Nutzer
nur seine eigenen Kleidungsstücke, selbst wenn er die ID eines fremden Teils kennt.
"""

from bson import ObjectId
from bson.errors import InvalidId
from pymongo import ReturnDocument

from app.core.datenbank import get_db

COLLECTION = "kleidungsstuecke"


def _collection():
    """Den „Karteikasten“ kleidungsstuecke in der Datenbank holen."""
    return get_db()[COLLECTION]


def _als_dict(dokument: dict) -> dict:
    """MongoDB-Dokument → einfaches dict, alle Verweise (`…_id`) als Text.

    MongoDB speichert IDs in einem eigenen Format (ObjectId). Der Rest der App und der
    Browser arbeiten mit normalem Text, deshalb wird hier umgewandelt."""
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


async def aendern(kleidungsstueck_id: str, nutzer_id: str, daten: dict) -> dict | None:
    """Die übergebenen Felder eines Kleidungsstücks des Nutzers überschreiben (andere
    bleiben, wie sie sind); das geänderte Kleidungsstück zurück, oder None, wenn es
    keins des Nutzers gibt."""
    try:
        oid = ObjectId(kleidungsstueck_id)
    except InvalidId:
        return None
    if "kategorie_ids" in daten:  # nur umwandeln, wenn mitgeschickt (z. B. nicht beim Favorit-Herz)
        daten = {**daten, "kategorie_ids": [ObjectId(k) for k in daten["kategorie_ids"]]}
    dokument = await _collection().find_one_and_update(
        {"_id": oid, "nutzer_id": ObjectId(nutzer_id)},
        {"$set": daten},
        return_document=ReturnDocument.AFTER,
    )
    return _als_dict(dokument) if dokument else None


async def loeschen(kleidungsstueck_id: str, nutzer_id: str) -> bool:
    """Ein Kleidungsstück des Nutzers aus der Datenbank löschen.
    Liefert True, wenn wirklich etwas gelöscht wurde, sonst False (gibt es nicht oder gehört
    jemand anderem). Auch hier steht die nutzer_id in der Suche, damit niemand fremde Teile löscht."""
    try:
        oid = ObjectId(kleidungsstueck_id)
    except InvalidId:
        return False
    ergebnis = await _collection().delete_one({"_id": oid, "nutzer_id": ObjectId(nutzer_id)})
    return ergebnis.deleted_count == 1


async def alle_des_nutzers(nutzer_id: str) -> list[dict]:
    """Alle Kleidungsstücke des Nutzers, neueste zuerst."""
    zeiger = _collection().find({"nutzer_id": ObjectId(nutzer_id)}).sort("erstellt_am", -1)
    return [_als_dict(d) async for d in zeiger]
