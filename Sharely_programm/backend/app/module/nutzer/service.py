"""Geschäftslogik des Moduls nutzer (reines Python, ohne HTTP).

Hier stehen Regeln und Abläufe, z. B. Berechtigungen ("gehört das dem Nutzer?"),
Obergrenzen und Berechnungen. Datenbankzugriffe laufen über repository.py.
"""

import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

from pymongo.errors import DuplicateKeyError

from app.core.config import get_settings
from app.core.sicherheit import passwort_hashen, passwort_pruefen
# Bildprüfung wie beim Kleidungsstück, über dessen service.py (Regel in backend/README.md)
from app.module.kleidung.service import BildUngueltig, BildZuGross, bild_format
from app.module.nutzer import repository
from app.module.nutzer.schemas import ProfilAntwort, RegistrierenAnfrage


class NichtGefunden(Exception):
    """Der Nutzer hat kein Profilbild."""


class EingabeUngueltig(Exception):
    """Registrierung mit falschem Format; die Nachricht wird so angezeigt."""


class SchonVergeben(Exception):
    """E-Mail oder Nutzername gehört schon zu einem Konto; die Nachricht wird so angezeigt."""


class AnmeldungFalsch(Exception):
    """Nutzername oder Passwort stimmt nicht."""


# Buchstaben, Ziffern, Punkt, Unterstrich, Bindestrich (z. B. „kleiderliebe“, „paul.m“)
NUTZERNAME_MUSTER = re.compile(r"[A-Za-z0-9._-]{3,30}")
EMAIL_MUSTER = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")
# Wie im Formular: mindestens 8 Zeichen und ein Sonderzeichen
PASSWORT_MIN = 8


def _upload_ordner() -> Path:
    return Path(get_settings().upload_ordner)


def _antwort(nutzer_id: str, nutzer: dict | None) -> ProfilAntwort:
    nutzer = nutzer or {}
    pfad = nutzer.get("profilbild_pfad")
    # ?v=… ändert sich mit jedem neuen Bild, damit der Browser nicht das alte aus dem Speicher zeigt
    url = f"/api/nutzer/ich/profilbild?v={Path(pfad).stem}" if pfad else None
    return ProfilAntwort(
        id=nutzer_id,
        nutzername=nutzer.get("nutzername"),
        email=nutzer.get("email"),
        mitglied_seit=nutzer.get("erstellt_am"),
        profilbild_url=url,
    )


async def registrieren(anfrage: RegistrierenAnfrage) -> str:
    """Konto anlegen und seine ID liefern. Die E-Mail wird kleingeschrieben gespeichert."""
    email = anfrage.email.strip().lower()
    nutzername = anfrage.nutzername.strip()
    if not EMAIL_MUSTER.fullmatch(email):
        raise EingabeUngueltig("Bitte eine gültige E-Mail-Adresse eingeben.")
    if not NUTZERNAME_MUSTER.fullmatch(nutzername):
        raise EingabeUngueltig(
            "Der Nutzername braucht 3 bis 30 Zeichen: Buchstaben, Ziffern, Punkt, Unterstrich oder Bindestrich."
        )
    if len(anfrage.passwort) < PASSWORT_MIN or anfrage.passwort.isalnum():
        raise EingabeUngueltig("Das Passwort braucht mindestens 8 Zeichen und ein Sonderzeichen.")
    if await repository.finden_per_email(email):
        raise SchonVergeben("Zu dieser E-Mail-Adresse gibt es schon ein Konto.")
    if await repository.finden_per_nutzername(nutzername):
        raise SchonVergeben("Dieser Nutzername ist schon vergeben.")
    jetzt = datetime.now(timezone.utc)
    try:
        return await repository.anlegen({
            "nutzername": nutzername,
            "email": email,
            "passwort_hash": passwort_hashen(anfrage.passwort),
            "profilbild_pfad": None,
            "ist_admin": False,
            "ausgeblendete_kategorie_ids": [],
            "erstellt_am": jetzt,
            "geaendert_am": jetzt,
        })
    except DuplicateKeyError:
        # Zwei Registrierungen gleichzeitig mit denselben Daten: der eindeutige Index greift
        raise SchonVergeben("E-Mail-Adresse oder Nutzername ist schon vergeben.")


async def anmelden(nutzername: str, passwort: str) -> str:
    """Prüft Nutzername und Passwort und liefert die Nutzer-ID. Bewusst eine Meldung
    für beide Fälle, damit niemand ausprobieren kann, welche Nutzernamen es gibt."""
    nutzer = await repository.finden_per_nutzername(nutzername.strip())
    if not passwort_pruefen(passwort, (nutzer or {}).get("passwort_hash")):
        raise AnmeldungFalsch()
    return str(nutzer["_id"])


async def profil(nutzer_id: str) -> ProfilAntwort:
    return _antwort(nutzer_id, await repository.finden(nutzer_id))


async def profilbild_speichern(nutzer_id: str, bild: bytes) -> ProfilAntwort:
    """Neues Profilbild prüfen und ablegen, das alte löschen (Datenschutz: keine Altbilder)."""
    if len(bild) > get_settings().max_bild_mb * 1024 * 1024:
        raise BildZuGross()
    endung = bild_format(bild)

    alt = (await repository.finden(nutzer_id) or {}).get("profilbild_pfad")
    # Dateiname wird nie vom Nutzer übernommen, sondern zufällig erzeugt.
    bild_pfad = f"{nutzer_id}/profilbild_{uuid.uuid4().hex}.{endung}"
    datei = _upload_ordner() / bild_pfad
    datei.parent.mkdir(parents=True, exist_ok=True)
    datei.write_bytes(bild)
    try:
        await repository.profilbild_setzen(nutzer_id, bild_pfad, datetime.now(timezone.utc))
    except Exception:
        datei.unlink(missing_ok=True)  # kein verwaistes Bild ohne Eintrag
        raise
    if alt:
        (_upload_ordner() / alt).unlink(missing_ok=True)
    return await profil(nutzer_id)


async def profilbild_entfernen(nutzer_id: str) -> ProfilAntwort:
    alt = (await repository.finden(nutzer_id) or {}).get("profilbild_pfad")
    if alt:
        await repository.profilbild_setzen(nutzer_id, None, datetime.now(timezone.utc))
        (_upload_ordner() / alt).unlink(missing_ok=True)
    return await profil(nutzer_id)


async def profilbild_datei(nutzer_id: str) -> Path:
    pfad = (await repository.finden(nutzer_id) or {}).get("profilbild_pfad")
    if not pfad or not (_upload_ordner() / pfad).is_file():
        raise NichtGefunden()
    return _upload_ordner() / pfad
