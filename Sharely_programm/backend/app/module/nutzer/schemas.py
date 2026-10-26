"""Pydantic-Modelle des Moduls nutzer: wie Daten in die API hinein- und herauskommen.

Typisch je Objekt: ein Modell zum Anlegen, eins zum Ändern, eins für die Antwort.
Die Felder richten sich nach dem Datenmodell in docs/datenmodell/.
"""

from pydantic import BaseModel


class ProfilAntwort(BaseModel):
    """Das eigene Profil. Bisher nur das Profilbild (ERM: Nutzer.Profilbild);
    Nutzername, E-Mail und „Mitglied seit“ kommen mit Registrierung und Login."""

    id: str
    # Adresse des Bildes oder None, wenn keins hochgeladen ist
    profilbild_url: str | None = None
