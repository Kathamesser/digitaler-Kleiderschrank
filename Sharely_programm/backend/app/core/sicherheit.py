"""Passwort-Hashing und Anmeldung (Login-Sitzung).

Verfahren nach ERM-Entscheidung 13 (Manuel, 20.10.2026): serverseitige Sitzung,
zufälliges Token im httpOnly-Cookie, Sitzungen in der Collection `sitzungen`
(TTL-Index löscht abgelaufene), Passwörter mit Argon2 (`pwdlib`).
Passwörter und Tokens werden nie im Klartext gespeichert (User Story 6): In der
Datenbank steht nur der Argon2-Hash bzw. der SHA-256-Hash des Tokens.

Einfach erklärt:
- „Hash“: Ein Passwort wird durch eine Einbahn-Rechnung in eine lange Zeichenkette verwandelt.
  Aus dem Hash kann man das Passwort nicht zurückrechnen. Beim Anmelden rechnet man das
  eingegebene Passwort genauso um und vergleicht die Ergebnisse.
- „Sitzung“ und „Token“: Nach dem Anmelden bekommt der Browser eine lange Zufallszahl (Token)
  in einem Cookie. Bei jeder weiteren Anfrage schickt er sie mit, und das Backend erkennt
  daran, wer angemeldet ist, ohne jedes Mal das Passwort zu brauchen.
- „httpOnly-Cookie“: Ein Cookie, das JavaScript im Browser nicht auslesen kann. Schutz davor,
  dass fremder Code das Token stiehlt.
"""

import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Annotated

from bson import ObjectId
from fastapi import Cookie, HTTPException, status
from pwdlib import PasswordHash

from app.core.config import get_settings
from app.core.datenbank import get_db

# Der Test-Nutzer aus der Zeit vor dem Login (Einrichtungsskript, `--stammdaten`).
# Er kann sich nicht anmelden, weil sein Passwort-Hash nur ein Platzhalter ist.
TEST_NUTZER_ID = "000000000000000000000001"

# Name des Cookies, in dem das Anmelde-Token im Browser liegt
COOKIE_NAME = "sharely_sitzung"

_passwort_hash = PasswordHash.recommended()  # Argon2id (ein besonders sicheres Hash-Verfahren)
# Wird geprüft, wenn es den Nutzernamen nicht gibt, damit die Antwort gleich lange
# dauert und man an der Zeit nicht ablesen kann, ob ein Konto existiert.
_DUMMY_HASH = _passwort_hash.hash("kein-echtes-passwort")


def passwort_hashen(passwort: str) -> str:
    """Passwort in seinen Hash verwandeln (beim Registrieren). Gespeichert wird nur dieser Hash."""
    return _passwort_hash.hash(passwort)


def passwort_pruefen(passwort: str, passwort_hash: str | None) -> bool:
    """Stimmt das eingegebene Passwort zum gespeicherten Hash? Liefert True (ja) oder False (nein)."""
    if not passwort_hash or not passwort_hash.startswith("$argon2"):
        # Kein echter Hash (Konto gibt es nicht oder Test-Nutzer): trotzdem einmal rechnen,
        # damit die Antwort gleich lange dauert, dann „falsch“ melden
        _passwort_hash.verify(passwort, _DUMMY_HASH)
        return False
    return _passwort_hash.verify(passwort, passwort_hash)


def _token_hash(token: str) -> str:
    """Auch das Token wird nur als Hash gespeichert: Wer die Datenbank liest, kann sich damit nicht anmelden."""
    return hashlib.sha256(token.encode()).hexdigest()


async def sitzung_starten(nutzer_id: str) -> str:
    """Neue Sitzung anlegen. Liefert das Token für das Cookie (nur dort steht es im Klartext)."""
    token = secrets.token_urlsafe(32)  # lange, nicht erratbare Zufallszeichenkette
    jetzt = datetime.now(timezone.utc)
    # Sitzung in der Datenbank merken: wem sie gehört und wann sie abläuft
    await get_db()["sitzungen"].insert_one({
        "nutzer_id": ObjectId(nutzer_id),
        "token_hash": _token_hash(token),
        "erstellt_am": jetzt,
        "laeuft_ab_am": jetzt + timedelta(hours=get_settings().sitzung_stunden),
    })
    return token


async def sitzung_beenden(token: str) -> None:
    """Abmelden: die Sitzung aus der Datenbank löschen, das Token gilt danach nicht mehr."""
    await get_db()["sitzungen"].delete_one({"token_hash": _token_hash(token)})


async def aktueller_nutzer(
    sitzung: Annotated[str | None, Cookie(alias=COOKIE_NAME)] = None,
) -> str:
    """Liefert die ID des angemeldeten Nutzers, sonst 401.
    Endpunkte holen den Nutzer immer über `Depends(aktueller_nutzer)`.

    401 ist der Web-Fehlercode für „nicht angemeldet“; die Seiten leiten dann zur Anmeldung weiter.
    „Depends“ heißt: FastAPI ruft diese Funktion vor jedem geschützten Endpunkt automatisch auf."""
    if sitzung:
        # Abgelaufene prüfen wir selbst: Der TTL-Index räumt nur etwa einmal pro Minute auf.
        # „$gt“ = greater than (größer als): Ablaufzeit muss noch in der Zukunft liegen
        eintrag = await get_db()["sitzungen"].find_one(
            {"token_hash": _token_hash(sitzung), "laeuft_ab_am": {"$gt": datetime.now(timezone.utc)}}
        )
        if eintrag:
            return str(eintrag["nutzer_id"])
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Bitte melde dich an.")
