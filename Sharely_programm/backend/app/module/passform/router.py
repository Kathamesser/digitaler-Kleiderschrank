"""HTTP-Endpunkte des Moduls passform.

Aufgabe: Passform-Bewertung „passt/eng/weit“: Körpermaße einer Figur gegen die Größentabelle eines Kleidungsstücks.
Grundlage: ROADMAP Phase 4, docs/avatar/ZENTIMETER.md.

Hier nur Anfragen entgegennehmen, prüfen lassen (schemas.py) und an service.py
weitergeben. Keine Geschäftslogik und keine Datenbankzugriffe in dieser Datei.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/passform", tags=["passform"])
