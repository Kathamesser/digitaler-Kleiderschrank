"""Passwort-Hashing und Anmeldung (Login-Sitzung bzw. Token).

Noch offen und im Team zu entscheiden: Verfahren für die Anmeldung
(z. B. JWT-Token oder Session-Cookie). Fest steht: Passwörter werden nie im
Klartext gespeichert (User Story 6).
"""

# PLATZHALTER bis zum echten Login: Alle Anfragen gehören diesem Test-Nutzer.
# Endpunkte holen den Nutzer immer über `Depends(aktueller_nutzer)`. Steht das
# Anmeldeverfahren fest, wird nur diese Funktion ersetzt (Sitzung prüfen, sonst
# 401), die Endpunkte bleiben unverändert.
TEST_NUTZER_ID = "000000000000000000000001"


async def aktueller_nutzer() -> str:
    """Liefert die ID des angemeldeten Nutzers (vorerst immer den Test-Nutzer)."""
    return TEST_NUTZER_ID
