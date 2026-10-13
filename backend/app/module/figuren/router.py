"""HTTP-Endpunkte des Moduls figuren.

Aufgabe: 3D-Avatar-Figuren des Nutzers (0 bis 3) speichern und laden; gespeichert werden nur Reglerwerte.
Grundlage: docs/avatar/FIGUR-DATENMODELL.md, AVATAR-3D-KONZEPT.md, ROADMAP Phase 3.

Hier nur Anfragen entgegennehmen, prüfen lassen (schemas.py) und an service.py
weitergeben. Keine Geschäftslogik und keine Datenbankzugriffe in dieser Datei.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/figuren", tags=["figuren"])
