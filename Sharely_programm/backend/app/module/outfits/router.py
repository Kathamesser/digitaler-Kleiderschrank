"""HTTP-Endpunkte des Moduls outfits.

Aufgabe: Outfits aus Kleidungsstücken zusammenstellen, bearbeiten, löschen, als Favorit markieren, „heute getragen“.
Grundlage: User Story 3 und 4, Konzeption 1.3, Wireframes 9–12.

Hier nur Anfragen entgegennehmen, prüfen lassen (schemas.py) und an service.py
weitergeben. Keine Geschäftslogik und keine Datenbankzugriffe in dieser Datei.
"""

from fastapi import APIRouter

# Noch leer: Das Modul ist schon angelegt (Ordner, Dateien, Adresse /api/outfits), hat aber noch keine
# Endpunkte. Die kommen in einer späteren Projektphase (siehe docs/planung/ROADMAP.md).
router = APIRouter(prefix="/outfits", tags=["outfits"])
