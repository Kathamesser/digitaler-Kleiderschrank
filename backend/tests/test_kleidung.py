"""Tests für User Story 8 (Kleidungsstück digitalisieren).

Die Datenbank wird durch einen Speicher im Arbeitsspeicher ersetzt, die Bilder
landen in einem temporären Ordner. So laufen die Tests ohne MongoDB.
"""

from datetime import date, timedelta

import pytest
from bson import ObjectId
from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app
from app.module.kleidung import repository

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
    daten = {"kategorie": "oberteile", **felder}
    return client.post("/api/kleidung", data=daten, files={"bild": (dateiname, bild)})


def test_nur_bild_und_kategorie_genuegen(client, tmp_path):
    antwort = hochladen(client)
    assert antwort.status_code == 201
    k = antwort.json()
    assert k["kategorie"] == "oberteile"
    assert k["favorit"] is False
    assert k["privat"] is False
    assert k["saison"] == [] and k["anlass"] == []
    assert k["marke"] is None and k["preis"] is None and k["kaufdatum"] is None
    assert k["status"] == "aktiv"
    assert k["bild_url"] == f"/api/kleidung/{k['id']}/bild"
    assert len(list(tmp_path.rglob("*.png"))) == 1


def test_alle_eigenschaften(client):
    antwort = hochladen(
        client,
        kategorie="jacken",
        favorit="true",
        privat="true",
        groesse="M",
        marke="Vaude",
        farbe="dunkelgrün",
        saison=["herbst", "winter"],
        anlass=["alltag", "sport"],
        preis="89.999",
        kaufdatum="2025-11-02",
        herkunft="flohmarkt",
        notiz="Reißverschluss klemmt etwas",
    )
    assert antwort.status_code == 201
    k = antwort.json()
    assert k["favorit"] is True and k["privat"] is True
    assert (k["groesse"], k["marke"], k["farbe"]) == ("M", "Vaude", "dunkelgrün")
    assert k["saison"] == ["herbst", "winter"]
    assert k["anlass"] == ["alltag", "sport"]
    assert k["preis"] == 90.0
    assert k["kaufdatum"] == "2025-11-02"
    assert k["herkunft"] == "flohmarkt"
    assert k["notiz"] == "Reißverschluss klemmt etwas"


def test_leere_textfelder_werden_none(client):
    k = hochladen(client, marke="   ", notiz="").json()
    assert k["marke"] is None and k["notiz"] is None


def test_roecke_und_kleider_sind_getrennt(client):
    assert hochladen(client, kategorie="roecke").status_code == 201
    assert hochladen(client, kategorie="kleider").status_code == 201
    assert hochladen(client, kategorie="roecke_kleider").status_code == 422


def test_kaufdatum_in_zukunft_wird_abgelehnt(client):
    morgen = (date.today() + timedelta(days=1)).isoformat()
    assert hochladen(client, kaufdatum=morgen).status_code == 422


def test_ungueltige_auswahl_wird_abgelehnt(client):
    assert hochladen(client, herkunft="geklaut").status_code == 422
    assert hochladen(client, saison=["keine"]).status_code == 422
    assert hochladen(client, anlass=["party"]).status_code == 422
    assert hochladen(client, preis="-5").status_code == 422


def test_bild_und_liste_abrufen(client):
    k = hochladen(client, bild=JPEG, dateiname="foto.jpg").json()
    bild = client.get(k["bild_url"])
    assert bild.status_code == 200
    assert bild.content == JPEG
    assert [e["id"] for e in client.get("/api/kleidung").json()] == [k["id"]]
    assert client.get(f"/api/kleidung/{k['id']}").json()["kategorie"] == "oberteile"


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


def test_unbekannte_kategorie_wird_abgelehnt(client):
    assert hochladen(client, kategorie="socken").status_code == 422


def test_fehlende_kategorie_wird_abgelehnt(client):
    antwort = client.post("/api/kleidung", files={"bild": ("shirt.png", PNG)})
    assert antwort.status_code == 422


def test_fehlendes_bild_wird_abgelehnt(client):
    assert client.post("/api/kleidung", data={"kategorie": "hosen"}).status_code == 422


def test_unbekanntes_kleidungsstueck(client):
    assert client.get("/api/kleidung/gibtsnicht").status_code == 404
    assert client.get("/api/kleidung/gibtsnicht/bild").status_code == 404
