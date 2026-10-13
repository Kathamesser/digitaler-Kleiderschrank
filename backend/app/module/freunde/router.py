"""HTTP-Endpunkte des Moduls freunde.

Aufgabe: Freunde suchen, Anfragen senden und bestätigen, entfernen; Kleiderschrank von Freunden einsehen.
Grundlage: User Story 2, Konzeption 1.4, Wireframes 17 und 19.

Hier nur Anfragen entgegennehmen, prüfen lassen (schemas.py) und an service.py
weitergeben. Keine Geschäftslogik und keine Datenbankzugriffe in dieser Datei.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/freunde", tags=["freunde"])
