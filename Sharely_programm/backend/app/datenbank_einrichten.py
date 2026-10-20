"""Richtet die MongoDB-Datenbank nach dem ERM ein: Collections, Prüfregeln, Indizes.

Aufruf im Ordner backend/ mit aktivierter .venv:

    python -m app.datenbank_einrichten               # einrichten bzw. aktualisieren
    python -m app.datenbank_einrichten --pruefen     # nur anzeigen, was fehlt oder abweicht
    python -m app.datenbank_einrichten --stammdaten  # zusätzlich Kleidungsarten und
                                                     # vorgegebene Kategorien einspielen

Die Verbindung kommt aus backend/.env (MONGODB_URL, MONGODB_DATENBANK).
Das Skript kann beliebig oft laufen: Vorhandenes bleibt, Fehlendes kommt dazu,
geänderte Prüfregeln werden übernommen. Es legt ohne `--stammdaten` keine Daten
an und löscht nie etwas, auch keine Collections, die nicht im ERM stehen.

Was eingerichtet wird, steht in app/core/datenbank_struktur.py.
"""

import argparse
import sys

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import OperationFailure, PyMongoError

from app.core.config import get_settings
from app.core.datenbank_struktur import COLLECTIONS, index_name, stammdaten

# „moderate“: Bereits gespeicherte Dokumente, die nicht passen, bleiben änderbar.
# Neue und korrekte Dokumente werden voll geprüft.
PRUEFUNG = {"validationLevel": "moderate", "validationAction": "error"}


def _adresse_ohne_zugangsdaten(url: str) -> str:
    """Für Meldungen: Benutzername und Passwort aus der Adresse entfernen."""
    schema, _, rest = url.partition("://")
    return f"{schema}://{rest.rsplit('@', 1)[-1]}"


def _index_optionen(index: dict) -> dict:
    optionen = {"name": index_name(index)}
    if index.get("unique"):
        optionen["unique"] = True
    if "ttl" in index:
        optionen["expireAfterSeconds"] = index["ttl"]
    if "nur_wenn" in index:
        optionen["partialFilterExpression"] = index["nur_wenn"]
    return optionen


def _aktuelle_pruefregel(db: Database, name: str) -> dict | None:
    antwort = db.command("listCollections", filter={"name": name})
    return antwort["cursor"]["firstBatch"][0].get("options", {}).get("validator")


def einrichten(db: Database, nur_pruefen: bool = False) -> tuple[list[str], list[str]]:
    """Gleicht die Datenbank mit COLLECTIONS ab. Liefert (Meldungen, Fehler)."""
    meldungen: list[str] = []
    fehler: list[str] = []
    vorhanden = set(db.list_collection_names())

    for name, teil in COLLECTIONS.items():
        regel = teil["pruefregel"]

        if name not in vorhanden:
            if nur_pruefen:
                meldungen.append(f"{name}: Collection fehlt")
                continue
            db.create_collection(name, validator=regel, **PRUEFUNG)
            meldungen.append(f"{name}: Collection angelegt")
        elif _aktuelle_pruefregel(db, name) != regel:
            if nur_pruefen:
                meldungen.append(f"{name}: Prüfregel weicht ab")
            else:
                db.command("collMod", name, validator=regel, **PRUEFUNG)
                meldungen.append(f"{name}: Prüfregel aktualisiert")

        bestehende = db[name].index_information() if name in vorhanden else {}
        for index in teil["indizes"]:
            iname = index_name(index)
            if iname in bestehende:
                continue
            if nur_pruefen:
                meldungen.append(f"{name}: Index {iname} fehlt")
                continue
            try:
                db[name].create_index(index["felder"], **_index_optionen(index))
                meldungen.append(f"{name}: Index {iname} angelegt")
            except OperationFailure as e:
                # z. B. doppelte Werte bei einem eindeutigen Index oder ein
                # gleicher Index unter anderem Namen
                fehler.append(f"{name}: Index {iname} nicht angelegt: {(e.details or {}).get('errmsg', e)}")

    for name in sorted(vorhanden - COLLECTIONS.keys()):
        if not name.startswith("system."):
            meldungen.append(f"{name}: steht nicht im ERM (bleibt unverändert)")

    return meldungen, fehler


def stammdaten_einspielen(db: Database) -> list[str]:
    """Kleidungsarten und vorgegebene Kategorien anlegen, falls sie fehlen.
    Vorhandene Einträge bleiben, eine schon gesetzte 3D-Vorlage wird nicht überschrieben."""
    daten = stammdaten()
    neu_arten = 0
    for art in daten["kleidungsarten"]:
        ergebnis = db["kleidungsarten"].update_one(
            {"_id": art["_id"]},
            {"$set": {"name": art["name"], "reihenfolge": art["reihenfolge"]},
             "$setOnInsert": {"vorlage_id": art["vorlage_id"]}},
            upsert=True,
        )
        neu_arten += ergebnis.upserted_id is not None
    neu_kategorien = 0
    for kategorie in daten["kategorien"]:
        ergebnis = db["kategorien"].update_one(kategorie, {"$setOnInsert": kategorie}, upsert=True)
        neu_kategorien += ergebnis.upserted_id is not None
    return [
        f"kleidungsarten: {neu_arten} neu, {len(daten['kleidungsarten']) - neu_arten} schon vorhanden",
        f"kategorien (vorgegeben): {neu_kategorien} neu, {len(daten['kategorien']) - neu_kategorien} schon vorhanden",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="MongoDB-Datenbank nach dem ERM einrichten.")
    parser.add_argument("--pruefen", action="store_true", help="nichts ändern, nur Abweichungen anzeigen")
    parser.add_argument("--stammdaten", action="store_true", help="Kleidungsarten und vorgegebene Kategorien einspielen")
    args = parser.parse_args()

    settings = get_settings()
    adresse = _adresse_ohne_zugangsdaten(settings.mongodb_url)
    print(f"Datenbank „{settings.mongodb_datenbank}“ auf {adresse}")

    client = MongoClient(settings.mongodb_url, serverSelectionTimeoutMS=5000, tz_aware=True)
    try:
        client.admin.command("ping")
        db = client[settings.mongodb_datenbank]
        meldungen, fehler = einrichten(db, nur_pruefen=args.pruefen)
        if args.stammdaten and not args.pruefen and not fehler:
            meldungen += stammdaten_einspielen(db)
    except PyMongoError as e:
        print(f"MongoDB nicht erreichbar oder Fehler: {e}")
        print("Läuft MongoDB? Stimmt MONGODB_URL in backend/.env?")
        return 1
    finally:
        client.close()

    for zeile in meldungen:
        print(f"  {zeile}")
    for zeile in fehler:
        print(f"  FEHLER {zeile}")
    if not meldungen and not fehler:
        print("  Alles schon auf dem Stand des ERM.")
    print("Fertig." if not fehler else "Fertig, aber mit Fehlern (siehe oben).")
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
