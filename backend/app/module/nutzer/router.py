"""HTTP-Endpunkte des Moduls nutzer.

Aufgabe: Registrierung, Login/Logout, Passwort zurücksetzen und ändern, Profil und Einstellungen, Konto löschen.
Grundlage: User Story 6 und 7, Konzeption 1.2, Wireframes 1–4 und 18–21.

Hier nur Anfragen entgegennehmen, prüfen lassen (schemas.py) und an service.py
weitergeben. Keine Geschäftslogik und keine Datenbankzugriffe in dieser Datei.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/nutzer", tags=["nutzer"])
