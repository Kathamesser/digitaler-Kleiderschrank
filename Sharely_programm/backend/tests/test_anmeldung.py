"""Tests für Registrierung, Login und Logout (User Story 6, ERM-Entscheidung 13).

Nutzer und Sitzungen liegen in einem Speicher im Arbeitsspeicher. So laufen die
Tests ohne MongoDB.
"""

from datetime import datetime, timedelta, timezone

import pytest
from bson import ObjectId
from fastapi.testclient import TestClient
from pymongo.errors import DuplicateKeyError

from app.core import sicherheit
from app.main import app
from app.module.nutzer import repository

PASSWORT = "geheim!123"
NEU = {"email": "Lena@Beispiel.de", "nutzername": "lena.k", "passwort": PASSWORT}


class SitzungenSpeicher:
    """Ersatz für die Collection `sitzungen`, kann genau die Abfragen aus sicherheit.py."""

    def __init__(self):
        self.eintraege: list[dict] = []

    async def insert_one(self, dok):
        self.eintraege.append(dok)

    async def find_one(self, filter):
        for e in self.eintraege:
            if e["token_hash"] == filter["token_hash"] and e["laeuft_ab_am"] > filter["laeuft_ab_am"]["$gt"]:
                return e
        return None

    async def delete_one(self, filter):
        self.eintraege = [e for e in self.eintraege if e["token_hash"] != filter["token_hash"]]


@pytest.fixture
def client(monkeypatch):
    nutzer: dict[str, dict] = {}
    sitzungen = SitzungenSpeicher()

    async def finden(nutzer_id):
        return nutzer.get(nutzer_id)

    async def finden_per_nutzername(name):
        return next((n for n in nutzer.values() if n["nutzername"].lower() == name.lower()), None)

    async def finden_per_email(email):
        return next((n for n in nutzer.values() if n["email"] == email), None)

    async def anlegen(daten):
        if any(n["email"] == daten["email"] for n in nutzer.values()):
            raise DuplicateKeyError("email")
        nutzer_id = str(ObjectId())
        nutzer[nutzer_id] = {**daten, "_id": ObjectId(nutzer_id)}
        return nutzer_id

    for name, ersatz in [("finden", finden), ("finden_per_nutzername", finden_per_nutzername),
                         ("finden_per_email", finden_per_email), ("anlegen", anlegen)]:
        monkeypatch.setattr(repository, name, ersatz)
    monkeypatch.setattr(sicherheit, "get_db", lambda: {"sitzungen": sitzungen})
    with TestClient(app) as c:
        c.nutzer, c.sitzungen = nutzer, sitzungen
        yield c


def registrieren(client, **felder):
    return client.post("/api/nutzer/registrieren", json={**NEU, **felder})


def test_ohne_anmeldung_kein_zugriff(client):
    antwort = client.get("/api/nutzer/ich")
    assert antwort.status_code == 401
    assert antwort.json()["detail"] == "Bitte melde dich an."
    assert client.get("/api/kleidung").status_code == 401


def test_registrieren_meldet_gleich_an(client):
    antwort = registrieren(client)
    assert antwort.status_code == 201
    profil = antwort.json()
    assert profil["nutzername"] == "lena.k"
    assert profil["email"] == "lena@beispiel.de"  # kleingeschrieben gespeichert
    assert profil["mitglied_seit"] is not None
    assert client.get("/api/nutzer/ich").json()["id"] == profil["id"]


def test_passwort_nur_als_argon2_hash(client):
    registrieren(client)
    gespeichert = next(iter(client.nutzer.values()))
    assert gespeichert["passwort_hash"].startswith("$argon2id$")
    assert PASSWORT not in str(gespeichert)


def test_cookie_ist_httponly_und_token_nur_als_hash(client):
    antwort = registrieren(client)
    cookie = antwort.headers["set-cookie"]
    assert cookie.startswith("sharely_sitzung=")
    assert "HttpOnly" in cookie and "samesite=lax" in cookie.lower()
    token = client.cookies["sharely_sitzung"]
    assert len(client.sitzungen.eintraege) == 1
    assert token not in str(client.sitzungen.eintraege)


@pytest.mark.parametrize("felder, text", [
    ({"email": "keine-adresse"}, "E-Mail"),
    ({"nutzername": "ab"}, "Nutzername"),
    ({"nutzername": "mit leerzeichen"}, "Nutzername"),
    ({"passwort": "kurz!"}, "8 Zeichen"),
    ({"passwort": "ohnesonderzeichen1"}, "Sonderzeichen"),
])
def test_registrieren_prueft_eingaben(client, felder, text):
    antwort = registrieren(client, **felder)
    assert antwort.status_code == 422
    assert text in antwort.json()["detail"]
    assert client.nutzer == {}


def test_email_und_nutzername_nur_einmal(client):
    registrieren(client)
    client.cookies.clear()
    doppelt = registrieren(client, email="LENA@beispiel.de", nutzername="anders")
    assert doppelt.status_code == 409 and "E-Mail" in doppelt.json()["detail"]
    doppelt = registrieren(client, email="neu@beispiel.de", nutzername="Lena.K")
    assert doppelt.status_code == 409 and "Nutzername" in doppelt.json()["detail"]
    assert len(client.nutzer) == 1


def test_anmelden_und_abmelden(client):
    registrieren(client)
    client.post("/api/nutzer/abmelden")
    assert client.get("/api/nutzer/ich").status_code == 401

    antwort = client.post("/api/nutzer/anmelden", json={"nutzername": "LENA.K", "passwort": PASSWORT})
    assert antwort.status_code == 200
    assert antwort.json()["nutzername"] == "lena.k"
    assert client.get("/api/nutzer/ich").status_code == 200

    assert client.post("/api/nutzer/abmelden").status_code == 204
    assert client.sitzungen.eintraege == []  # Sitzung ist in der Datenbank gelöscht
    assert client.get("/api/nutzer/ich").status_code == 401


def test_abmelden_ohne_sitzung_klappt(client):
    assert client.post("/api/nutzer/abmelden").status_code == 204


@pytest.mark.parametrize("nutzername, passwort", [("lena.k", "falsch!123"), ("gibtsnicht", PASSWORT)])
def test_falsche_anmeldung_gleiche_meldung(client, nutzername, passwort):
    registrieren(client)
    client.cookies.clear()
    antwort = client.post("/api/nutzer/anmelden", json={"nutzername": nutzername, "passwort": passwort})
    assert antwort.status_code == 401
    assert antwort.json()["detail"] == "Nutzername oder Passwort ist falsch."
    assert "sharely_sitzung" not in client.cookies


def test_test_nutzer_kann_sich_nicht_anmelden(client):
    """Der Platzhalter-Test-Nutzer aus dem Einrichtungsskript hat keinen echten Hash."""
    client.nutzer[sicherheit.TEST_NUTZER_ID] = {
        "_id": ObjectId(sicherheit.TEST_NUTZER_ID), "nutzername": "testnutzer_platzhalter",
        "email": "test-nutzer@sharely.invalid", "passwort_hash": "!kein-login-platzhalter",
    }
    antwort = client.post("/api/nutzer/anmelden", json={"nutzername": "testnutzer_platzhalter", "passwort": "!kein-login-platzhalter"})
    assert antwort.status_code == 401


def test_abgelaufene_sitzung_gilt_nicht(client):
    registrieren(client)
    client.sitzungen.eintraege[0]["laeuft_ab_am"] = datetime.now(timezone.utc) - timedelta(seconds=1)
    assert client.get("/api/nutzer/ich").status_code == 401
