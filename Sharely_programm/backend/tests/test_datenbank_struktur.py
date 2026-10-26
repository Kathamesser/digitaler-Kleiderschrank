"""Tests für die Datenbankstruktur (app/core/datenbank_struktur.py), ohne MongoDB.

Ein kleiner Nachbau der MongoDB-Prüfung (`verstoesse`) prüft Beispieldokumente
gegen die Prüfregeln. So fällt ein Fehler in einer Prüfregel hier auf und nicht
erst, wenn MongoDB das Speichern ablehnt.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest
from bson import ObjectId

from app.core import wertelisten as wl
from app.core.datenbank_struktur import COLLECTIONS, index_name, stammdaten

REPO = Path(__file__).resolve().parents[3]  # tests → backend → Sharely_programm → Repo
JETZT = datetime.now(timezone.utc)

# Collections laut ERM vom 20.10.2026 (docs/datenmodell/ERM-SHARELY.md, Abschnitt 6)
ERM_COLLECTIONS = {
    "nutzer", "sitzungen", "passwort_resets", "figuren", "freundschaften", "leihvorgaenge",
    "kleidungsstuecke", "kleidungsarten", "kleidungsvorlagen", "kategorien", "outfits",
    "neuigkeiten", "gelesene_neuigkeiten",
}

BSON_TYPEN = {
    ObjectId: "objectId", str: "string", bool: "bool", int: "int", float: "double",
    datetime: "date", type(None): "null", list: "array", dict: "object",
}


def verstoesse(wert, regel: dict, pfad: str = "") -> list[str]:
    """Nachbau der MongoDB-Prüfung für die Schlüsselwörter, die wir nutzen."""
    fehler = []
    erlaubt = regel.get("bsonType")
    if erlaubt is not None:
        erlaubt = [erlaubt] if isinstance(erlaubt, str) else erlaubt
        typ = BSON_TYPEN.get(type(wert))
        if typ not in erlaubt and not (typ == "int" and "long" in erlaubt):
            return [f"{pfad or 'Dokument'}: Typ {typ}, erlaubt {erlaubt}"]
    if "enum" in regel and wert not in regel["enum"]:
        fehler.append(f"{pfad}: {wert!r} nicht in der Liste")
    if isinstance(wert, (int, float)) and not isinstance(wert, bool):
        if "minimum" in regel and wert < regel["minimum"]:
            fehler.append(f"{pfad}: {wert} < {regel['minimum']}")
        if "maximum" in regel and wert > regel["maximum"]:
            fehler.append(f"{pfad}: {wert} > {regel['maximum']}")
    if isinstance(wert, dict):
        for feld in regel.get("required", []):
            if feld not in wert:
                fehler.append(f"{pfad}.{feld}: Pflichtfeld fehlt")
        for feld, unterregel in regel.get("properties", {}).items():
            if feld in wert:
                fehler += verstoesse(wert[feld], unterregel, f"{pfad}.{feld}")
        if isinstance(regel.get("additionalProperties"), dict):
            for feld, w in wert.items():
                if feld not in regel.get("properties", {}):
                    fehler += verstoesse(w, regel["additionalProperties"], f"{pfad}.{feld}")
    if isinstance(wert, list):
        if len(wert) < regel.get("minItems", 0):
            fehler.append(f"{pfad}: weniger als {regel['minItems']} Einträge")
        if regel.get("uniqueItems") and len(wert) != len({repr(w) for w in wert}):
            fehler.append(f"{pfad}: doppelte Einträge")
        if "items" in regel:
            for i, eintrag in enumerate(wert):
                fehler += verstoesse(eintrag, regel["items"], f"{pfad}[{i}]")
    return fehler


def schema(name: str) -> dict:
    return COLLECTIONS[name]["pruefregel"]["$jsonSchema"]


# Ein gültiges Beispiel je Collection, so wie das Backend speichern soll.
BEISPIELE = {
    "nutzer": {"nutzername": "chris", "email": "chris@example.org", "passwort_hash": "$argon2id$…",
               "profilbild_pfad": None, "ist_admin": False, "ausgeblendete_kategorie_ids": [ObjectId()],
               "erstellt_am": JETZT, "geaendert_am": JETZT},
    "sitzungen": {"nutzer_id": ObjectId(), "token_hash": "abc", "erstellt_am": JETZT, "laeuft_ab_am": JETZT},
    "passwort_resets": {"nutzer_id": ObjectId(), "token_hash": "abc", "erstellt_am": JETZT,
                        "laeuft_ab_am": JETZT, "eingeloest_am": None},
    "figuren": {"nutzer_id": ObjectId(), "name": "Meine Figur", "ist_standard": True,
                "fuer_freunde_sichtbar": False, "regler_version": 1,
                "regler": {"geschlecht": -80, "taillenumfang": -20},
                "figurtyp": {"typ": "frau_sanduhr-kurvig", "staerke": 40},
                "erstellt_am": JETZT, "geaendert_am": JETZT},
    "freundschaften": {"anfragender_id": ObjectId(), "angefragter_id": ObjectId(), "status": "angenommen",
                       "angefragt_am": JETZT, "beantwortet_am": JETZT},
    "leihvorgaenge": {"kleidungsstueck_id": ObjectId(), "besitzer_id": ObjectId(), "empfaenger_id": ObjectId(),
                      "typ": "leihen", "angefragt_von": "empfaenger", "status": "aktiv", "von": JETZT,
                      "bis": None, "notiz": "Bitte nur chemisch reinigen.", "angefragt_am": JETZT,
                      "beantwortet_am": JETZT, "abgeschlossen_am": None},
    "kleidungsstuecke": {"nutzer_id": ObjectId(), "kleidungsart": "jacken", "kategorie_ids": [ObjectId()],
                         "leihvorgang_id": None, "name": "Wintermantel", "bild_pfad": "x/y.png",
                         "status": "im_schrank", "favorit": True, "privat": False, "farbe": "beige",
                         "material": "polyester", "saison": ["herbst", "winter"], "kaufdatum": JETZT,
                         "preis": 149.0, "erstellt_am": JETZT, "geaendert_am": JETZT,
                         "masse": [{"messpunkt": "bust-circ", "wert_cm": 104.5}], "quelle": None},
    "kleidungsarten": {"_id": "jacken", "name": "Jacken", "reihenfolge": 6, "vorlage_id": None,
                       "messpunkte": [{"messpunkt": "bust-circ", "pflicht": True}]},
    "kleidungsvorlagen": {"name": "Jacke", "modell_datei": "assets/kleidung/jacke.glb", "ebene": 3},
    "kategorien": {"nutzer_id": None, "name": "Business"},
    "outfits": {"nutzer_id": ObjectId(), "name": "Business Look", "favorit": True, "privat": False,
                "kategorie_ids": [ObjectId()], "teile": [{"kleidungsstueck_id": ObjectId(), "position": 1}],
                "erstellt_am": JETZT, "geaendert_am": JETZT},
    "neuigkeiten": {"typ": "update", "titel": "Neu: Filter", "text": "…", "veroeffentlicht_am": JETZT},
    "gelesene_neuigkeiten": {"neuigkeit_id": ObjectId(), "nutzer_id": ObjectId(), "gelesen_am": JETZT},
}


def test_alle_collections_aus_dem_erm():
    assert set(COLLECTIONS) == ERM_COLLECTIONS


@pytest.mark.parametrize("name", sorted(ERM_COLLECTIONS))
def test_pflichtfelder_sind_beschrieben(name):
    assert set(schema(name)["required"]) <= set(schema(name)["properties"])


@pytest.mark.parametrize("name", sorted(ERM_COLLECTIONS))
def test_beispiel_erfuellt_pruefregel(name):
    assert verstoesse(BEISPIELE[name], schema(name)) == []


def test_indexnamen_eindeutig():
    for name, teil in COLLECTIONS.items():
        namen = [index_name(i) for i in teil["indizes"]]
        assert len(namen) == len(set(namen)), name


def test_messpunkte_wie_in_der_glb():
    """Die Messpunkte müssen genau die Messbänder der Avatar-GLB sein."""
    datei = json.loads((REPO / "docs/avatar/messpunkte.json").read_text(encoding="utf-8"))
    assert set(wl.MESSPUNKTE) == set(datei["masse"])


def test_messpunkte_je_kleidungsart():
    """Jede Kleidungsart hat eine Liste, nur bekannte Messpunkte."""
    assert set(wl.MESSPUNKTE_JE_KLEIDUNGSART) == set(wl.KLEIDUNGSARTEN)
    for art, punkte in wl.MESSPUNKTE_JE_KLEIDUNGSART.items():
        assert set(punkte) <= set(wl.MESSPUNKTE), art
    assert wl.MESSPUNKTE_JE_KLEIDUNGSART["accessoires"] == {}
    assert wl.MESSPUNKTE_JE_KLEIDUNGSART["hosen"]["waist-circ"] is True


def test_stammdaten_erfuellen_pruefregeln():
    for name, eintraege in stammdaten().items():
        for eintrag in eintraege:
            assert verstoesse(eintrag, schema(name)) == [], eintrag
    assert len(stammdaten()["kleidungsarten"]) == len(wl.KLEIDUNGSARTEN)


@pytest.mark.parametrize("name, falsch, feld", [
    ("kleidungsstuecke", {"status": "verschenkt"}, "status"),
    ("kleidungsstuecke", {"kleidungsart": "socken"}, "kleidungsart"),
    ("kleidungsstuecke", {"farbe": "tuerkis"}, "farbe"),
    ("kleidungsstuecke", {"masse": [{"messpunkt": "nase", "wert_cm": 3}]}, "messpunkt"),
    ("kleidungsstuecke", {"saison": ["winter", "winter"]}, "saison"),
    ("kleidungsstuecke", {"nutzer_id": "kein ObjectId"}, "nutzer_id"),
    ("outfits", {"teile": []}, "teile"),
    ("figuren", {"regler": {"gewicht": 150}}, "gewicht"),
    ("freundschaften", {"status": "folgt"}, "status"),
    ("kleidungsarten", {"messpunkte": [{"messpunkt": "nase", "pflicht": True}]}, "messpunkt"),
])
def test_pruefregel_lehnt_falsches_ab(name, falsch, feld):
    """Gegenprobe: Falsche Werte werden erkannt."""
    fehler = verstoesse({**BEISPIELE[name], **falsch}, schema(name))
    assert any(feld in f for f in fehler), fehler


def test_pflichtfeld_fehlt_wird_erkannt():
    dokument = {k: v for k, v in BEISPIELE["kleidungsstuecke"].items() if k != "kleidungsart"}
    assert any("kleidungsart" in f for f in verstoesse(dokument, schema("kleidungsstuecke")))


# ---------------------------------------------------------------- Zusammenspiel mit dem Modul kleidung

def _kleidung_nach_erm_20_10() -> bool:
    from app.module.kleidung.schemas import KleidungsstueckAngaben
    return "kleidungsart" in KleidungsstueckAngaben.model_fields


@pytest.mark.skipif(not _kleidung_nach_erm_20_10(),
                    reason="Modul kleidung ist noch nicht auf das ERM vom 20.10.2026 umgestellt")
def test_modul_kleidung_speichert_passend(monkeypatch, tmp_path):
    """Ein Kleidungsstück, wie das Repository es wirklich an MongoDB schickt,
    muss die Prüfregel erfüllen. Läuft, sobald das Modul umgestellt ist."""
    from fastapi.testclient import TestClient

    from app.core.config import get_settings
    from app.main import app
    from app.module.kleidung import repository

    gespeichert: list[dict] = []

    class Ergebnis:
        inserted_id = ObjectId()

    class FakeCollection:
        async def insert_one(self, dokument):
            gespeichert.append(dict(dokument))
            return Ergebnis()

    monkeypatch.setattr(repository, "_collection", lambda: FakeCollection())
    monkeypatch.setattr(get_settings(), "upload_ordner", str(tmp_path))
    png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
    with TestClient(app) as client:
        antwort = client.post("/api/kleidung", data={"kleidungsart": "jacken"}, files={"bild": ("teil.png", png)})
    assert antwort.status_code == 201, antwort.text
    assert verstoesse(gespeichert[0], schema("kleidungsstuecke")) == []
