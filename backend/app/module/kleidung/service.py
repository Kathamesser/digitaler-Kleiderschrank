"""Geschäftslogik des Moduls kleidung (reines Python, ohne HTTP).

Hier stehen Regeln und Abläufe, z. B. Berechtigungen ("gehört das dem Nutzer?"),
Obergrenzen und Berechnungen. Datenbankzugriffe laufen über repository.py.
"""

import uuid
from datetime import datetime, timezone
from pathlib import Path

from app.core.config import get_settings
from app.module.kleidung import repository
from app.module.kleidung.schemas import Kategorie, KleidungsstueckAntwort, Status


class BildUngueltig(Exception):
    """Datei ist kein unterstütztes Bild (JPEG, PNG, WebP)."""


class BildZuGross(Exception):
    """Datei ist größer als max_bild_mb."""


class NichtGefunden(Exception):
    """Kleidungsstück gibt es nicht oder es gehört einem anderen Nutzer."""


def bild_format(daten: bytes) -> str:
    """Erkennt das Bildformat am Dateianfang und liefert die Dateiendung.

    Bewusst nicht der Dateiname oder der vom Browser gemeldete Typ: Beides kann
    beliebig sein. HEIC (iPhone-Standard) fehlt noch, Browser wandeln beim
    Hochladen aus der Galerie aber meist in JPEG um.
    """
    if daten.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if daten.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if daten[:4] == b"RIFF" and daten[8:12] == b"WEBP":
        return "webp"
    raise BildUngueltig()


def _upload_ordner() -> Path:
    return Path(get_settings().upload_ordner)


def _antwort(kleidungsstueck: dict) -> KleidungsstueckAntwort:
    return KleidungsstueckAntwort(
        **kleidungsstueck,
        bild_url=f"/api/kleidung/{kleidungsstueck['id']}/bild",
    )


async def digitalisieren(
    nutzer_id: str,
    name: str,
    kategorie: Kategorie,
    bild: bytes,
    farbe: str | None = None,
    groesse: str | None = None,
) -> KleidungsstueckAntwort:
    """User Story 8: Foto prüfen, im Upload-Ordner des Nutzers ablegen und das
    Kleidungsstück anlegen."""
    if len(bild) > get_settings().max_bild_mb * 1024 * 1024:
        raise BildZuGross()
    endung = bild_format(bild)

    # Dateiname wird nie vom Nutzer übernommen, sondern zufällig erzeugt.
    bild_pfad = f"{nutzer_id}/{uuid.uuid4().hex}.{endung}"
    datei = _upload_ordner() / bild_pfad
    datei.parent.mkdir(parents=True, exist_ok=True)
    datei.write_bytes(bild)

    try:
        kleidungsstueck = await repository.anlegen({
            "nutzer_id": nutzer_id,
            "name": name,
            "kategorie": kategorie.value,
            "farbe": farbe,
            "groesse": groesse,
            "favorit": False,
            "status": Status.aktiv.value,
            "bild_pfad": bild_pfad,
            "erstellt_am": datetime.now(timezone.utc),
        })
    except Exception:
        datei.unlink(missing_ok=True)  # kein verwaistes Bild ohne Eintrag
        raise
    return _antwort(kleidungsstueck)


async def alle(nutzer_id: str) -> list[KleidungsstueckAntwort]:
    return [_antwort(k) for k in await repository.alle_des_nutzers(nutzer_id)]


async def eins(kleidungsstueck_id: str, nutzer_id: str) -> KleidungsstueckAntwort:
    kleidungsstueck = await repository.finden(kleidungsstueck_id, nutzer_id)
    if kleidungsstueck is None:
        raise NichtGefunden()
    return _antwort(kleidungsstueck)


async def bild_datei(kleidungsstueck_id: str, nutzer_id: str) -> Path:
    """Pfad zur Bilddatei, nur für den Besitzer des Kleidungsstücks."""
    kleidungsstueck = await repository.finden(kleidungsstueck_id, nutzer_id)
    if kleidungsstueck is None:
        raise NichtGefunden()
    datei = _upload_ordner() / kleidungsstueck["bild_pfad"]
    if not datei.is_file():
        raise NichtGefunden()
    return datei
