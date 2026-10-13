"""HTTP-Endpunkte des Moduls kleidung.

Aufgabe: Kleidungsstücke anlegen (mit Foto), anzeigen, bearbeiten, löschen; Filter nach Kategorie, Suche, Favoriten.
Grundlage: User Story 1, 4, 5 und 8, Konzeption 1.3, Wireframes 5–8.

Hier nur Anfragen entgegennehmen, prüfen lassen (schemas.py) und an service.py
weitergeben. Keine Geschäftslogik und keine Datenbankzugriffe in dieser Datei.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/kleidung", tags=["kleidung"])
