"""HTTP-Endpunkte des Moduls produktimport.

Aufgabe: Wunschartikel per Link oder Beschreibung mit KI importieren (Bild, Titel, Preis, Marke, Kategorie, Größentabelle); Wunschliste.
Grundlage: ROADMAP Phase 5 (KI-Anbieter noch offen).

Hier nur Anfragen entgegennehmen, prüfen lassen (schemas.py) und an service.py
weitergeben. Keine Geschäftslogik und keine Datenbankzugriffe in dieser Datei.
"""

from fastapi import APIRouter

# Noch leer: Das Modul ist schon angelegt (Ordner, Dateien, Adresse /api/produktimport), hat aber noch keine
# Endpunkte. Die kommen in einer späteren Projektphase (siehe docs/planung/ROADMAP.md).
router = APIRouter(prefix="/produktimport", tags=["produktimport"])
