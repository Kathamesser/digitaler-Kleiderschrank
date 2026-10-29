"""Passwort-Hashing und Anmeldung (Login-Sitzung).

Verfahren nach ERM-Entscheidung 13 (Manuel, 20.10.2026): serverseitige Sitzung,
zufälliges Token im httpOnly-Cookie, Sitzungen in der Collection `sitzungen`
(TTL-Index löscht abgelaufene), Passwörter mit Argon2 (`pwdlib`).
Passwörter und Tokens werden nie im Klartext gespeichert (User Story 6): In der
Datenbank steht nur der Argon2-Hash bzw. der SHA-256-Hash des Tokens.
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

COOKIE_NAME = "sharely_sitzung"

_passwort_hash = PasswordHash.recommended()  # Argon2id
# Wird geprüft, wenn es den Nutzernamen nicht gibt, damit die Antwort gleich lange
# dauert und man an der Zeit nicht ablesen kann, ob ein Konto existiert.
_DUMMY_HASH = _passwort_hash.hash("kein-echtes-passwort")


def passwort_hashen(passwort: str) -> str:
    return _passwort_hash.hash(passwort)


def passwort_pruefen(passwort: str, passwort_hash: str | None) -> bool:
    if not passwort_hash or not passwort_hash.startswith("$argon2"):
        _passwort_hash.verify(passwort, _DUMMY_HASH)
        return False
    return _passwort_hash.verify(passwort, passwort_hash)


def _token_hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


async def sitzung_starten(nutzer_id: str) -> str:
    """Neue Sitzung anlegen. Liefert das Token für das Cookie (nur dort steht es im Klartext)."""
    token = secrets.token_urlsafe(32)
    jetzt = datetime.now(timezone.utc)
    await get_db()["sitzungen"].insert_one({
        "nutzer_id": ObjectId(nutzer_id),
        "token_hash": _token_hash(token),
        "erstellt_am": jetzt,
        "laeuft_ab_am": jetzt + timedelta(hours=get_settings().sitzung_stunden),
    })
    return token


async def sitzung_beenden(token: str) -> None:
    await get_db()["sitzungen"].delete_one({"token_hash": _token_hash(token)})


async def aktueller_nutzer(
    sitzung: Annotated[str | None, Cookie(alias=COOKIE_NAME)] = None,
) -> str:
    """Liefert die ID des angemeldeten Nutzers, sonst 401.
    Endpunkte holen den Nutzer immer über `Depends(aktueller_nutzer)`."""
    if sitzung:
        # Abgelaufene prüfen wir selbst: Der TTL-Index räumt nur etwa einmal pro Minute auf.
        eintrag = await get_db()["sitzungen"].find_one(
            {"token_hash": _token_hash(sitzung), "laeuft_ab_am": {"$gt": datetime.now(timezone.utc)}}
        )
        if eintrag:
            return str(eintrag["nutzer_id"])
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Bitte melde dich an.")
