"""Geschäftslogik des Moduls nutzer (reines Python, ohne HTTP).

Hier stehen Regeln und Abläufe, z. B. Berechtigungen ("gehört das dem Nutzer?"),
Obergrenzen und Berechnungen. Datenbankzugriffe laufen über repository.py.
"""

import uuid
from pathlib import Path

from app.core.config import get_settings
# Bildprüfung wie beim Kleidungsstück, über dessen service.py (Regel in backend/README.md)
from app.module.kleidung.service import BildUngueltig, BildZuGross, bild_format
from app.module.nutzer import repository
from app.module.nutzer.schemas import ProfilAntwort


class NichtGefunden(Exception):
    """Der Nutzer hat kein Profilbild."""


def _upload_ordner() -> Path:
    return Path(get_settings().upload_ordner)


def _antwort(nutzer_id: str, nutzer: dict | None) -> ProfilAntwort:
    pfad = (nutzer or {}).get("profilbild_pfad")
    # ?v=… ändert sich mit jedem neuen Bild, damit der Browser nicht das alte aus dem Speicher zeigt
    url = f"/api/nutzer/ich/profilbild?v={Path(pfad).stem}" if pfad else None
    return ProfilAntwort(id=nutzer_id, profilbild_url=url)


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
        await repository.profilbild_setzen(nutzer_id, bild_pfad)
    except Exception:
        datei.unlink(missing_ok=True)  # kein verwaistes Bild ohne Eintrag
        raise
    if alt:
        (_upload_ordner() / alt).unlink(missing_ok=True)
    return await profil(nutzer_id)


async def profilbild_entfernen(nutzer_id: str) -> ProfilAntwort:
    alt = (await repository.finden(nutzer_id) or {}).get("profilbild_pfad")
    if alt:
        await repository.profilbild_setzen(nutzer_id, None)
        (_upload_ordner() / alt).unlink(missing_ok=True)
    return await profil(nutzer_id)


async def profilbild_datei(nutzer_id: str) -> Path:
    pfad = (await repository.finden(nutzer_id) or {}).get("profilbild_pfad")
    if not pfad or not (_upload_ordner() / pfad).is_file():
        raise NichtGefunden()
    return _upload_ordner() / pfad
