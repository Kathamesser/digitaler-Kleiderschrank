"""Pydantic-Modelle des Moduls nutzer: wie Daten in die API hinein- und herauskommen.

Typisch je Objekt: ein Modell zum Anlegen, eins zum Ändern, eins für die Antwort.
Die Felder richten sich nach dem Datenmodell in docs/datenmodell/.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class RegistrierenAnfrage(BaseModel):
    """Mockup „Desktop 2 · Registrierung“. Die Regeln (Format, Länge, Sonderzeichen)
    prüft service.py, damit die Fehlermeldungen auf Deutsch und verständlich sind."""

    email: str = Field(max_length=254)
    nutzername: str = Field(max_length=100)
    passwort: str = Field(max_length=200)


class AnmeldenAnfrage(BaseModel):
    """Mockup „Desktop 1 · Anmeldung“: mit Nutzername und Passwort."""

    nutzername: str = Field(max_length=100)
    passwort: str = Field(max_length=200)


class ProfilAntwort(BaseModel):
    """Das eigene Profil (ERM: Nutzer). Passwort-Hash und Ist_Admin gibt die API nie heraus."""

    id: str
    nutzername: str | None = None
    email: str | None = None
    # „Mitglied seit“ im Profil (ERM: erstellt am)
    mitglied_seit: datetime | None = None
    # Adresse des Bildes oder None, wenn keins hochgeladen ist
    profilbild_url: str | None = None
