"""HTTP-Endpunkte des Moduls passform.

Aufgabe: Passform-Bewertung „passt/eng/weit“: Körpermaße einer Figur gegen die Größentabelle eines Kleidungsstücks.
Grundlage: ROADMAP Phase 4, docs/avatar/ZENTIMETER.md.

Hier nur Anfragen entgegennehmen, prüfen lassen (schemas.py) und an service.py
weitergeben. Keine Geschäftslogik und keine Datenbankzugriffe in dieser Datei.
"""

from fastapi import APIRouter

# Noch leer: Das Modul ist schon angelegt (Ordner, Dateien, Adresse /api/passform), hat aber noch keine
# Endpunkte. Die kommen in einer späteren Projektphase (siehe docs/planung/ROADMAP.md).
router = APIRouter(prefix="/passform", tags=["passform"])
