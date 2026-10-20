"""Tests für User Story 8 (Kleidungsstück digitalisieren), Felder nach dem ERM vom 20.10.2026.

Die Datenbank wird durch einen Speicher im Arbeitsspeicher ersetzt, die Bilder
landen in einem temporären Ordner. So laufen die Tests ohne MongoDB.
"""

import json
from datetime import date, timedelta
from pathlib import Path

import pytest
from bson import ObjectId
from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app
from app.module.kleidung import repository
from app.module.kleidung.schemas import Messpunkt

PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
JPEG = b"\xff\xd8\xff\xe0" + b"\x00" * 100


@pytest.fixture
def client(monkeypatch, tmp_path):
    speicher: dict[str, dict] = {}

    async def anlegen(daten):
        eintrag = {**daten, "id": str(ObjectId())}
        speicher[eintrag["id"]] = eintrag
        return eintrag

    async def finden(kleidungsstueck_id, nutzer_id):
        eintrag = speicher.get(kleidungsstueck_id)
        return eintrag if eintrag and eintrag["nutzer_id"] == nutzer_id else None

    async def alle_des_nutzers(nutzer_id):
        return [e for e in speicher.values() if e["nutzer_id"] == nutzer_id]

    monkeypatch.setattr(repository, "anlegen", anlegen)
    monkeypatch.setattr(repository, "finden", finden)
    monkeypatch.setattr(repository, "alle_des_nutzers", alle_des_nutzers)
    monkeypatch.setattr(get_settings(), "upload_ordner", str(tmp_path))
    with TestClient(app) as c:
        yield c


def hochladen(client, bild=PNG, dateiname="shirt.png", **felder):
    daten = {"kleidungsart": "tops", **felder}
    return client.post("/api/kleidung", data=daten, files={"bild": (dateiname, bild)})


def test_nur_bild_und_kleidungsart_genuegen(client, tmp_path):
    antwort = hochladen(client)
    assert antwort.status_code == 201
    k = antwort.json()
    assert k["kleidungsart"] == "tops"
    assert k["name"] is None
    assert k["favorit"] is False
    assert k["privat"] is False
    assert k["saison"] == [] and k["kategorie_ids"] == [] and k["masse"] == []
    assert k["farbe"] is None and k["material"] is None and k["preis"] is None and k["kaufdatum"] is None
    assert k["status"] == "im_schrank"
    assert k["leihvorgang_id"] is None
    assert k["bild_url"] == f"/api/kleidung/{k['id']}/bild"
    assert len(list(tmp_path.rglob("*.png"))) == 1


def test_alle_eigenschaften(client):
    kategorie = str(ObjectId())
    antwort = hochladen(
        client,
        kleidungsart="jacken",
        name="  Wintermantel ",
        favorit="true",
        privat="true",
        farbe="dunkelblau",
        material="wolle",
        saison=["herbst", "winter"],
        preis="89.999",
        kaufdatum="2025-11-02",
        status="wunsch",
        kategorie_ids=[kategorie, kategorie],
        masse=json.dumps([
            {"messpunkt": "bust-circ", "wert_cm": 104.04},
            {"messpunkt": "upperarm-length", "wert_cm": 34},
        ]),
    )
    assert antwort.status_code == 201
    k = antwort.json()
    assert k["name"] == "Wintermantel"
    assert k["favorit"] is True and k["privat"] is True
    assert (k["farbe"], k["material"]) == ("dunkelblau", "wolle")
    assert k["saison"] == ["herbst", "winter"]
    assert k["preis"] == 90.0
    assert k["kaufdatum"] == "2025-11-02"
    assert k["status"] == "wunsch"
    assert k["kategorie_ids"] == [kategorie]
    assert k["masse"] == [
        {"messpunkt": "bust-circ", "wert_cm": 104.0},
        {"messpunkt": "upperarm-length", "wert_cm": 34.0},
    ]


def test_entfallene_felder_werden_ignoriert(client):
    k = hochladen(client, marke="Vaude", groesse="M", anlass="sport", notiz="x", herkunft="laden").json()
    for feld in ("marke", "groesse", "anlass", "notiz", "herkunft", "kategorie"):
        assert feld not in k


def test_leerer_name_wird_none(client):
    assert hochladen(client, name="   ").json()["name"] is None


def test_alle_kleidungsarten(client):
    for art in ("tops", "pullover", "hosen", "roecke", "kleider", "jacken", "schuhe",
                "unterwaesche", "einteiler", "accessoires"):
        assert hochladen(client, kleidungsart=art).status_code == 201
    assert hochladen(client, kleidungsart="oberteile").status_code == 422


def test_status_beim_anlegen(client):
    assert hochladen(client, status="geliehen").json()["status"] == "geliehen"
    assert hochladen(client, status="wunsch").json()["status"] == "wunsch"
    # verliehen setzt nur das Modul verleihen, verschenkt gibt es nicht mehr
    assert hochladen(client, status="verliehen").status_code == 422
    assert hochladen(client, status="verschenkt").status_code == 422


def test_leihvorgang_id_setzt_nur_das_system(client):
    k = hochladen(client, status="geliehen", leihvorgang_id=str(ObjectId())).json()
    assert k["leihvorgang_id"] is None


def test_ganzjaehrig(client):
    assert hochladen(client, saison=["ganzjaehrig"]).json()["saison"] == ["ganzjaehrig"]
    assert hochladen(client, saison=["ganzjaehrig", "sommer"]).status_code == 422


def test_kaufdatum_in_zukunft_wird_abgelehnt(client):
    morgen = (date.today() + timedelta(days=1)).isoformat()
    assert hochladen(client, kaufdatum=morgen).status_code == 422


def test_ungueltige_auswahl_wird_abgelehnt(client):
    assert hochladen(client, farbe="dunkelgrün").status_code == 422
    assert hochladen(client, material="Denim").status_code == 422
    assert hochladen(client, saison=["keine"]).status_code == 422
    assert hochladen(client, preis="-5").status_code == 422
    assert hochladen(client, kategorie_ids=["business"]).status_code == 422


def test_ungueltige_masse_werden_abgelehnt(client):
    def masse(*eintraege):
        return hochladen(client, masse=json.dumps(list(eintraege))).status_code

    assert masse({"messpunkt": "ellenbogen", "wert_cm": 30}) == 422
    assert masse({"messpunkt": "waist-circ", "wert_cm": 0}) == 422
    assert masse({"messpunkt": "waist-circ", "wert_cm": 80}, {"messpunkt": "waist-circ", "wert_cm": 82}) == 422
    assert hochladen(client, masse="kein json").status_code == 422


def test_messpunkte_wie_in_der_glb():
    datei = Path(__file__).parents[2] / "docs" / "avatar" / "messpunkte.json"
    schluessel = json.loads(datei.read_text(encoding="utf-8"))["masse"].keys()
    assert {m.value for m in Messpunkt} == set(schluessel)


def test_bild_und_liste_abrufen(client):
    k = hochladen(client, bild=JPEG, dateiname="foto.jpg").json()
    bild = client.get(k["bild_url"])
    assert bild.status_code == 200
    assert bild.content == JPEG
    assert [e["id"] for e in client.get("/api/kleidung").json()] == [k["id"]]
    assert client.get(f"/api/kleidung/{k['id']}").json()["kleidungsart"] == "tops"


def test_kein_bild_wird_abgelehnt(client, tmp_path):
    antwort = hochladen(client, bild=b"%PDF-1.7 kein Bild", dateiname="trick.png")
    assert antwort.status_code == 415
    assert "kein unterstütztes Bild" in antwort.json()["detail"]
    assert list(tmp_path.rglob("*.*")) == []


def test_zu_grosses_bild_wird_abgelehnt(client, monkeypatch):
    monkeypatch.setattr(get_settings(), "max_bild_mb", 1)
    antwort = hochladen(client, bild=PNG + b"\x00" * (1024 * 1024))
    assert antwort.status_code == 413
    assert "zu groß" in antwort.json()["detail"]


def test_fehlende_kleidungsart_wird_abgelehnt(client):
    antwort = client.post("/api/kleidung", files={"bild": ("shirt.png", PNG)})
    assert antwort.status_code == 422


def test_fehlendes_bild_wird_abgelehnt(client):
    assert client.post("/api/kleidung", data={"kleidungsart": "hosen"}).status_code == 422


def test_unbekanntes_kleidungsstueck(client):
    assert client.get("/api/kleidung/gibtsnicht").status_code == 404
    assert client.get("/api/kleidung/gibtsnicht/bild").status_code == 404
