"""Struktur der MongoDB-Datenbank: Collections, Prüfregeln und Indizes.

Grundlage ist das ERM vom 20.10.2026 (docs/datenmodell/ERM-SHARELY.md und
Reiter „MongoDB“ in ERM_Sharely.drawio). Eingerichtet wird die Datenbank mit
`python -m app.datenbank_einrichten` (im Ordner backend/).

Prüfregeln ($jsonSchema): MongoDB lehnt Dokumente ab, die nicht passen. Sie
prüfen nur das Grobe: Pflichtfelder, Datentypen und feste Wertelisten.
Feinere Regeln (höchstens 3 Figuren, Verweise auf andere Collections,
Sichtbarkeit) prüft das Backend, siehe ERM-SHARELY.md Abschnitt 7.
Zusätzliche Felder sind erlaubt, damit Erweiterungen (z. B. „Angebote“) keinen
Umbau der Datenbank brauchen.

Dieses Modul importiert absichtlich kein pymongo: Es ist reine Beschreibung
und lässt sich ohne laufende Datenbank testen.
"""

from app.core import wertelisten as wl

# ---------------------------------------------------------------- Bausteine

ID = {"bsonType": "objectId"}
ID_ODER_NULL = {"bsonType": ["objectId", "null"]}
TEXT = {"bsonType": "string"}
TEXT_ODER_NULL = {"bsonType": ["string", "null"]}
ZEITPUNKT = {"bsonType": "date"}
ZEITPUNKT_ODER_NULL = {"bsonType": ["date", "null"]}
JA_NEIN = {"bsonType": "bool"}
GANZZAHL = {"bsonType": ["int", "long"]}
ZAHL = {"bsonType": ["double", "int", "long", "decimal"]}
ZAHL_ODER_NULL = {"bsonType": ["double", "int", "long", "decimal", "null"]}
ID_LISTE = {"bsonType": "array", "uniqueItems": True, "items": ID}


def auswahl(werte, null_erlaubt: bool = False) -> dict:
    """Ein Wert aus einer festen Liste (z. B. Status)."""
    werte = list(werte)
    if null_erlaubt:
        return {"bsonType": ["string", "null"], "enum": [*werte, None]}
    return {"bsonType": "string", "enum": werte}


def mehrfachauswahl(werte) -> dict:
    """Liste aus einer festen Werteliste, ohne Doppelte (z. B. Saison)."""
    return {"bsonType": "array", "uniqueItems": True, "items": {"bsonType": "string", "enum": list(werte)}}


def dokument(pflicht: list[str], felder: dict) -> dict:
    """Prüfregel für eine Collection. `_id` vergibt MongoDB selbst (außer bei kleidungsarten)."""
    return {"$jsonSchema": {"bsonType": "object", "required": pflicht, "properties": felder}}


# ---------------------------------------------------------------- Collections

# Jede Collection: Prüfregel und Indizes.
# Index: {"felder": [(feld, 1 | -1)], optional "unique", "ttl" (Sekunden), "nur_wenn" (partialFilterExpression)}
COLLECTIONS: dict[str, dict] = {

    "nutzer": {
        "pruefregel": dokument(
            ["nutzername", "email", "passwort_hash", "erstellt_am"],
            {
                "nutzername": TEXT,  # eindeutig, darüber werden Freunde gefunden
                "email": TEXT,  # das Backend speichert sie kleingeschrieben
                "passwort_hash": TEXT,  # nur Argon2-Hash, nie das Passwort
                "profilbild_pfad": TEXT_ODER_NULL,
                # Nur direkt in der Datenbank gesetzt; die API ändert es nie.
                "ist_admin": JA_NEIN,
                "ausgeblendete_kategorie_ids": ID_LISTE,
                "erstellt_am": ZEITPUNKT,
                "geaendert_am": ZEITPUNKT,
            },
        ),
        "indizes": [
            {"felder": [("email", 1)], "unique": True},
            {"felder": [("nutzername", 1)], "unique": True},
        ],
    },

    "sitzungen": {
        "pruefregel": dokument(
            ["nutzer_id", "token_hash", "erstellt_am", "laeuft_ab_am"],
            {"nutzer_id": ID, "token_hash": TEXT, "erstellt_am": ZEITPUNKT, "laeuft_ab_am": ZEITPUNKT},
        ),
        "indizes": [
            {"felder": [("token_hash", 1)], "unique": True},
            {"felder": [("nutzer_id", 1)]},
            # TTL: MongoDB löscht die Sitzung automatisch, sobald laeuft_ab_am erreicht ist.
            {"felder": [("laeuft_ab_am", 1)], "ttl": 0},
        ],
    },

    "passwort_resets": {
        "pruefregel": dokument(
            ["nutzer_id", "token_hash", "erstellt_am", "laeuft_ab_am"],
            {
                "nutzer_id": ID,
                "token_hash": TEXT,
                "erstellt_am": ZEITPUNKT,
                "laeuft_ab_am": ZEITPUNKT,
                "eingeloest_am": ZEITPUNKT_ODER_NULL,
            },
        ),
        "indizes": [
            {"felder": [("token_hash", 1)], "unique": True},
            {"felder": [("nutzer_id", 1)]},
            {"felder": [("laeuft_ab_am", 1)], "ttl": 0},
        ],
    },

    "figuren": {
        # Felder nach docs/avatar/FIGUR-DATENMODELL.md; höchstens 3 je Nutzer prüft das Backend.
        "pruefregel": dokument(
            ["nutzer_id", "name", "regler_version", "regler", "erstellt_am"],
            {
                "nutzer_id": ID,
                "name": TEXT,
                "ist_standard": JA_NEIN,
                "fuer_freunde_sichtbar": JA_NEIN,
                "regler_version": GANZZAHL,
                # Reglerwerte −100 … +100; fehlende Regler gelten als 0.
                "regler": {
                    "bsonType": "object",
                    "additionalProperties": {"bsonType": ["int", "long"], "minimum": -100, "maximum": 100},
                },
                "figurtyp": {
                    "bsonType": ["object", "null"],
                    "required": ["typ", "staerke"],
                    "properties": {
                        "typ": TEXT,
                        "staerke": {"bsonType": ["int", "long"], "minimum": 0, "maximum": 100},
                    },
                },
                "erstellt_am": ZEITPUNKT,
                "geaendert_am": ZEITPUNKT,
            },
        ),
        "indizes": [{"felder": [("nutzer_id", 1)]}],
    },

    "freundschaften": {
        # Gegenseitige Freundschaft; ein Datensatz je Paar (beide Richtungen prüft das Backend).
        "pruefregel": dokument(
            ["anfragender_id", "angefragter_id", "status", "angefragt_am"],
            {
                "anfragender_id": ID,
                "angefragter_id": ID,
                "status": auswahl(wl.FREUNDSCHAFT_STATUS),
                "angefragt_am": ZEITPUNKT,
                "beantwortet_am": ZEITPUNKT_ODER_NULL,  # „Freunde seit“
            },
        ),
        "indizes": [
            {"felder": [("anfragender_id", 1), ("angefragter_id", 1)], "unique": True},
            {"felder": [("angefragter_id", 1)]},
        ],
    },

    "leihvorgaenge": {
        "pruefregel": dokument(
            ["kleidungsstueck_id", "besitzer_id", "empfaenger_id", "typ", "angefragt_von", "status", "angefragt_am"],
            {
                "kleidungsstueck_id": ID,
                "besitzer_id": ID_ODER_NULL,  # null = gelöschter Nutzer (Verlauf bleibt)
                "empfaenger_id": ID_ODER_NULL,
                "typ": auswahl(wl.LEIH_TYPEN),
                "angefragt_von": auswahl(wl.LEIH_ANGEFRAGT_VON),
                "status": auswahl(wl.LEIH_STATUS),
                "von": ZEITPUNKT_ODER_NULL,
                "bis": ZEITPUNKT_ODER_NULL,  # null = unbefristet
                "notiz": TEXT_ODER_NULL,
                "angefragt_am": ZEITPUNKT,
                "beantwortet_am": ZEITPUNKT_ODER_NULL,
                "abgeschlossen_am": ZEITPUNKT_ODER_NULL,
            },
        ),
        "indizes": [
            {"felder": [("kleidungsstueck_id", 1)]},
            {"felder": [("besitzer_id", 1)]},
            {"felder": [("empfaenger_id", 1)]},
        ],
    },

    "kleidungsstuecke": {
        "pruefregel": dokument(
            ["nutzer_id", "kleidungsart", "bild_pfad", "status", "erstellt_am"],
            {
                "nutzer_id": ID,
                "kleidungsart": auswahl(wl.KLEIDUNGSARTEN),
                "kategorie_ids": ID_LISTE,
                # Nur bei Status „geliehen“ über Sharely: Verweis auf den Leihvorgang.
                "leihvorgang_id": ID_ODER_NULL,
                "name": TEXT_ODER_NULL,
                "bild_pfad": TEXT,
                "status": auswahl(wl.STATUS),
                "favorit": JA_NEIN,
                "privat": JA_NEIN,
                "farbe": auswahl(wl.FARBEN, null_erlaubt=True),
                "material": auswahl(wl.MATERIALIEN, null_erlaubt=True),
                "saison": mehrfachauswahl(wl.SAISONS),
                "kaufdatum": ZEITPUNKT_ODER_NULL,  # Datum als 00:00 UTC
                "preis": {**ZAHL_ODER_NULL, "minimum": 0},
                "erstellt_am": ZEITPUNKT,
                "geaendert_am": ZEITPUNKT,
                # Maße an den Messbändern der Avatar-GLB
                "masse": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "required": ["messpunkt", "wert_cm"],
                        "properties": {"messpunkt": auswahl(wl.MESSPUNKTE), "wert_cm": {**ZAHL, "minimum": 0}},
                    },
                },
                # Nur bei importierten Wunschartikeln (KI-Import kommt später)
                "quelle": {
                    "bsonType": ["object", "null"],
                    "properties": {
                        "url": TEXT,
                        "shop": TEXT,
                        "importiert_am": ZEITPUNKT,
                        "importiert_per": auswahl(wl.IMPORTIERT_PER),
                    },
                },
            },
        ),
        "indizes": [
            {"felder": [("nutzer_id", 1), ("erstellt_am", -1)]},  # Schrank, neueste zuerst
            {"felder": [("nutzer_id", 1), ("status", 1), ("kleidungsart", 1)]},
            {"felder": [("nutzer_id", 1), ("favorit", 1)]},
            {"felder": [("nutzer_id", 1), ("privat", 1)]},  # Schrank-Ansicht für Freunde
            {"felder": [("kategorie_ids", 1)]},
            {"felder": [("leihvorgang_id", 1)], "nur_wenn": {"leihvorgang_id": {"$type": "objectId"}}},
        ],
    },

    "kleidungsarten": {
        # Feste Liste; _id ist der Schlüssel (z. B. "jacken"). Daran hängt die 3D-Vorlage.
        "pruefregel": dokument(
            ["_id", "name", "reihenfolge"],
            {
                "_id": auswahl(wl.KLEIDUNGSARTEN),
                "name": TEXT,
                "reihenfolge": GANZZAHL,
                "vorlage_id": ID_ODER_NULL,
                # Messpunkte für Eingabe und Passform, siehe wl.MESSPUNKTE_JE_KLEIDUNGSART
                "messpunkte": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "required": ["messpunkt", "pflicht", "zugabe_min", "zugabe_max", "einheit"],
                        "properties": {
                            "messpunkt": auswahl(wl.MESSPUNKTE),
                            "pflicht": JA_NEIN,
                            "zugabe_min": ZAHL,
                            "zugabe_max": ZAHL,
                            "einheit": auswahl(["prozent", "cm"]),
                        },
                    },
                },
            },
        ),
        "indizes": [],
    },

    "kleidungsvorlagen": {
        "pruefregel": dokument(
            ["name", "modell_datei", "ebene"],
            {"name": TEXT, "modell_datei": TEXT, "ebene": GANZZAHL},
        ),
        "indizes": [{"felder": [("name", 1)], "unique": True}],
    },

    "kategorien": {
        # nutzer_id = null: vorgegebene Kategorie für alle; sonst eigene Kategorie des Nutzers.
        "pruefregel": dokument(
            ["name"],
            {"nutzer_id": ID_ODER_NULL, "name": TEXT},
        ),
        "indizes": [{"felder": [("nutzer_id", 1), ("name", 1)], "unique": True}],
    },

    "outfits": {
        "pruefregel": dokument(
            ["nutzer_id", "name", "teile", "erstellt_am"],
            {
                "nutzer_id": ID,
                "name": TEXT,
                "favorit": JA_NEIN,
                "privat": JA_NEIN,
                "kategorie_ids": ID_LISTE,
                "teile": {
                    "bsonType": "array",
                    "minItems": 1,
                    "items": {
                        "bsonType": "object",
                        "required": ["kleidungsstueck_id"],
                        "properties": {"kleidungsstueck_id": ID, "position": GANZZAHL},
                    },
                },
                "erstellt_am": ZEITPUNKT,
                "geaendert_am": ZEITPUNKT,
            },
        ),
        "indizes": [
            {"felder": [("nutzer_id", 1)]},
            {"felder": [("kategorie_ids", 1)]},
            {"felder": [("teile.kleidungsstueck_id", 1)]},  # „in welchen Outfits steckt das Teil?“
        ],
    },

    "neuigkeiten": {
        # Anlegen dürfen nur Admins (nutzer.ist_admin), prüft das Backend.
        "pruefregel": dokument(
            ["typ", "titel", "text", "veroeffentlicht_am"],
            {"typ": auswahl(wl.NEUIGKEIT_TYPEN), "titel": TEXT, "text": TEXT, "veroeffentlicht_am": ZEITPUNKT},
        ),
        "indizes": [{"felder": [("veroeffentlicht_am", -1)]}],
    },

    "gelesene_neuigkeiten": {
        "pruefregel": dokument(
            ["neuigkeit_id", "nutzer_id", "gelesen_am"],
            {"neuigkeit_id": ID, "nutzer_id": ID, "gelesen_am": ZEITPUNKT},
        ),
        "indizes": [{"felder": [("nutzer_id", 1), ("neuigkeit_id", 1)], "unique": True}],
    },
}


def index_name(index: dict) -> str:
    """Fester, lesbarer Name, damit das Einrichten wiederholt werden kann."""
    return "_".join(f"{feld}_{richtung}" for feld, richtung in index["felder"])


def stammdaten() -> dict[str, list[dict]]:
    """Feste Einträge, die die App braucht: Kleidungsarten und vorgegebene
    Kategorien. Werden nur mit `--stammdaten` eingespielt."""
    return {
        "kleidungsarten": [
            {"_id": schluessel, "name": name, "reihenfolge": i, "vorlage_id": None,
             "messpunkte": [{"messpunkt": m, "pflicht": p, "zugabe_min": lo, "zugabe_max": hi,
                             "einheit": wl.einheit_der_zugabe(m)}
                            for m, (p, lo, hi) in wl.MESSPUNKTE_JE_KLEIDUNGSART[schluessel].items()]}
            for i, (schluessel, name) in enumerate(wl.KLEIDUNGSARTEN.items(), start=1)
        ],
        "kategorien": [{"nutzer_id": None, "name": name} for name in wl.VORGEGEBENE_KATEGORIEN],
    }
