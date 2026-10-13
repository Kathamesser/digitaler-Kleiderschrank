"""HTTP-Endpunkte des Moduls produktimport.

Aufgabe: Wunschartikel per Link oder Beschreibung mit KI importieren (Bild, Titel, Preis, Marke, Kategorie, Größentabelle); Wunschliste.
Grundlage: ROADMAP Phase 5 (KI-Anbieter noch offen).

Hier nur Anfragen entgegennehmen, prüfen lassen (schemas.py) und an service.py
weitergeben. Keine Geschäftslogik und keine Datenbankzugriffe in dieser Datei.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/produktimport", tags=["produktimport"])
