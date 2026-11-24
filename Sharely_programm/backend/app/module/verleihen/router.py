"""HTTP-Endpunkte des Moduls verleihen.

Aufgabe: Leih- und Schenkanfragen stellen, annehmen, ablehnen; Rückgabe markieren; Übersicht verliehen/ausgeliehen.
Grundlage: User Story 9 und 10, Konzeption 1.4, Wireframes 13–16.

Hier nur Anfragen entgegennehmen, prüfen lassen (schemas.py) und an service.py
weitergeben. Keine Geschäftslogik und keine Datenbankzugriffe in dieser Datei.
"""

from fastapi import APIRouter

# Noch leer: Das Modul ist schon angelegt (Ordner, Dateien, Adresse /api/verleihen), hat aber noch keine
# Endpunkte. Die kommen in einer späteren Projektphase (siehe docs/planung/ROADMAP.md).
router = APIRouter(prefix="/verleihen", tags=["verleihen"])
