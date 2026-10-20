"""Tests fürs Profilbild (Modul nutzer, Mockup „Mein Profil“).

Die Datenbank wird durch einen Speicher im Arbeitsspeicher ersetzt, die Bilder
landen in einem temporären Ordner. So laufen die Tests ohne MongoDB.
"""

import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.core.sicherheit import TEST_NUTZER_ID
from app.main import app
from app.module.nutzer import repository

PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
JPEG = b"\xff\xd8\xff\xe0" + b"\x00" * 100


@pytest.fixture
def client(monkeypatch, tmp_path):
    speicher: dict[str, dict] = {}

    async def finden(nutzer_id):
        return speicher.get(nutzer_id)

    async def profilbild_setzen(nutzer_id, bild_pfad, geaendert_am):
        speicher.setdefault(nutzer_id, {}).update(profilbild_pfad=bild_pfad, geaendert_am=geaendert_am)

    monkeypatch.setattr(repository, "finden", finden)
    monkeypatch.setattr(repository, "profilbild_setzen", profilbild_setzen)
    monkeypatch.setattr(get_settings(), "upload_ordner", str(tmp_path))
    with TestClient(app) as c:
        c.speicher = speicher  # für Prüfungen auf das gespeicherte Dokument
        yield c


def hochladen(client, bild=JPEG, dateiname="ich.jpg"):
    return client.put("/api/nutzer/ich/profilbild", files={"bild": (dateiname, bild)})


def test_ohne_profilbild(client):
    antwort = client.get("/api/nutzer/ich")
    assert antwort.status_code == 200
    assert antwort.json() == {"id": TEST_NUTZER_ID, "profilbild_url": None}
    assert client.get("/api/nutzer/ich/profilbild").status_code == 404


def test_profilbild_hochladen_und_abrufen(client, tmp_path):
    antwort = hochladen(client)
    assert antwort.status_code == 200
    url = antwort.json()["profilbild_url"]
    assert url.startswith("/api/nutzer/ich/profilbild?v=profilbild_")
    assert client.get(url).content == JPEG
    # Datei liegt im Ordner des Nutzers, mit zufälligem Namen statt „ich.jpg“
    dateien = list((tmp_path / TEST_NUTZER_ID).iterdir())
    assert len(dateien) == 1 and dateien[0].name.startswith("profilbild_") and dateien[0].suffix == ".jpg"


def test_neues_bild_ersetzt_altes(client, tmp_path):
    erste = hochladen(client).json()["profilbild_url"]
    zweite = hochladen(client, PNG, "neu.png").json()["profilbild_url"]
    assert erste != zweite  # neue Adresse, damit der Browser nicht das alte Bild zeigt
    dateien = list((tmp_path / TEST_NUTZER_ID).iterdir())
    assert [d.suffix for d in dateien] == [".png"]  # altes Bild ist gelöscht


def test_aenderung_setzt_geaendert_am(client):
    hochladen(client)
    erstes = client.speicher[TEST_NUTZER_ID]["geaendert_am"]
    assert erstes.tzinfo is not None  # Zeitpunkt in UTC wie erstellt_am beim Kleidungsstück
    client.delete("/api/nutzer/ich/profilbild")
    assert client.speicher[TEST_NUTZER_ID]["geaendert_am"] >= erstes


def test_profilbild_entfernen(client, tmp_path):
    hochladen(client)
    antwort = client.delete("/api/nutzer/ich/profilbild")
    assert antwort.status_code == 200
    assert antwort.json()["profilbild_url"] is None
    assert list((tmp_path / TEST_NUTZER_ID).iterdir()) == []
    assert client.get("/api/nutzer/ich/profilbild").status_code == 404


def test_keine_bilddatei(client):
    antwort = hochladen(client, b"kein Bild", "ich.jpg")
    assert antwort.status_code == 415
    assert "kein unterstütztes Bild" in antwort.json()["detail"]


def test_bild_zu_gross(client, monkeypatch):
    monkeypatch.setattr(get_settings(), "max_bild_mb", 0)
    assert hochladen(client).status_code == 413
