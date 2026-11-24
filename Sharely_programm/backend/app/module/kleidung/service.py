"""Geschäftslogik des Moduls kleidung (reines Python, ohne HTTP).

Hier stehen Regeln und Abläufe, z. B. Berechtigungen ("gehört das dem Nutzer?"),
Obergrenzen und Berechnungen. Datenbankzugriffe laufen über repository.py.
"""

import uuid
from datetime import datetime, time, timezone
from app.core import bildspeicher
from app.core.config import get_settings
from app.module.kleidung import repository
from app.module.kleidung.schemas import KleidungsstueckAntwort, KleidungsstueckNeu


class BildUngueltig(Exception):
    """Datei ist kein unterstütztes Bild (JPEG, PNG, WebP)."""


class BildZuGross(Exception):
    """Datei ist größer als max_bild_mb."""


class SpeicherVoll(Exception):
    """Mit dem neuen Bild wäre der Speicher des Nutzers (max_speicher_mb_pro_nutzer) überschritten."""


def speichergrenze_text() -> str:
    """Für Meldungen: „1 GB“ statt „1024 MB“."""
    mb = get_settings().max_speicher_mb_pro_nutzer
    return f"{mb // 1024} GB" if mb % 1024 == 0 else f"{mb} MB"


async def platz_pruefen(nutzer_id: str, neu: int, frei_wird: int = 0) -> None:
    """Speicherlimit je Nutzer (1 GB, Vorschlag Christian 24.11.2026). `frei_wird`: Größe
    eines Bildes, das durch das neue ersetzt wird (z. B. altes Profilbild)."""
    grenze = get_settings().max_speicher_mb_pro_nutzer * 1024 * 1024
    if await bildspeicher.belegt(nutzer_id) - frei_wird + neu > grenze:
        raise SpeicherVoll()


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


def _antwort(kleidungsstueck: dict) -> KleidungsstueckAntwort:
    kaufdatum = kleidungsstueck.get("kaufdatum")
    return KleidungsstueckAntwort(
        **{**kleidungsstueck, "kaufdatum": kaufdatum.date() if kaufdatum else None},
        bild_url=f"/api/kleidung/{kleidungsstueck['id']}/bild",
    )


async def _bild_speichern(nutzer_id: str, bild: bytes, frei_wird: int = 0) -> str:
    """Bild prüfen (Größe, Format, Speicherlimit) und im Bildspeicher
    (app/core/bildspeicher.py) ablegen; liefert den Schlüssel `<nutzer_id>/<zufall>.<endung>`.
    `frei_wird`: Größe eines Bildes, das durch das neue ersetzt wird."""
    if len(bild) > get_settings().max_bild_mb * 1024 * 1024:
        raise BildZuGross()
    endung = bild_format(bild)
    await platz_pruefen(nutzer_id, len(bild), frei_wird)
    # Dateiname wird nie vom Nutzer übernommen, sondern zufällig erzeugt.
    bild_pfad = f"{nutzer_id}/{uuid.uuid4().hex}.{endung}"
    await bildspeicher.speichern(bild_pfad, bild)
    return bild_pfad


async def _groesse(schluessel: str) -> int:
    try:
        return len(await bildspeicher.laden(schluessel))
    except bildspeicher.BildFehlt:
        return 0


def _fuer_datenbank(angaben: KleidungsstueckNeu) -> dict:
    daten = angaben.model_dump(mode="json")
    # MongoDB kennt nur Zeitpunkte, kein reines Datum: Kaufdatum als 00:00 UTC
    if angaben.kaufdatum:
        daten["kaufdatum"] = datetime.combine(angaben.kaufdatum, time(), timezone.utc)
    return daten


async def digitalisieren(
    nutzer_id: str,
    angaben: KleidungsstueckNeu,
    bild: bytes,
) -> KleidungsstueckAntwort:
    """User Story 8: Foto prüfen, im Bildspeicher (app/core/bildspeicher.py) ablegen und das
    Kleidungsstück anlegen. Den Status wählt der Nutzer (Eigenes, Geliehen,
    Wunschartikel); `leihvorgang_id` bleibt leer, das setzt nur das Modul
    verleihen."""
    bild_pfad = await _bild_speichern(nutzer_id, bild)
    daten = _fuer_datenbank(angaben)
    try:
        kleidungsstueck = await repository.anlegen({
            **daten,
            "nutzer_id": nutzer_id,
            "leihvorgang_id": None,
            "bild_pfad": bild_pfad,
            "erstellt_am": datetime.now(timezone.utc),
        })
    except Exception:
        await bildspeicher.loeschen(bild_pfad)  # kein verwaistes Bild ohne Eintrag
        raise
    return _antwort(kleidungsstueck)


async def aendern(
    kleidungsstueck_id: str,
    nutzer_id: str,
    angaben: KleidungsstueckNeu,
    bild: bytes | None = None,
) -> KleidungsstueckAntwort:
    """Kleidungsstück bearbeiten (Wunsch Katha, 24.11.2026). Alle Angaben werden
    ersetzt, wie beim Anlegen: Was fehlt, ist danach leer. Ein neues Foto ist
    freiwillig und ersetzt das alte, das dann gelöscht wird.

    Ist das Teil gerade verliehen oder über einen Leihvorgang geliehen, bleibt
    der Status, wie er ist: Den ändert nur das Modul verleihen."""
    alt = await repository.finden(kleidungsstueck_id, nutzer_id)
    if alt is None:
        raise NichtGefunden()
    alter_pfad = alt["bild_pfad"]  # vorher merken, das Speichern überschreibt ihn

    daten = _fuer_datenbank(angaben)
    if alt["status"] == "verliehen" or alt.get("leihvorgang_id"):
        daten["status"] = alt["status"]
    neuer_pfad = None
    if bild is not None:
        # Das alte Foto wird ersetzt und zählt beim Speicherlimit nicht doppelt
        neuer_pfad = await _bild_speichern(nutzer_id, bild, frei_wird=await _groesse(alter_pfad))
        daten["bild_pfad"] = neuer_pfad

    try:
        neu = await repository.aendern(kleidungsstueck_id, nutzer_id, daten)
    except Exception:
        if neuer_pfad:
            await bildspeicher.loeschen(neuer_pfad)
        raise
    if neu is None:  # in der Zwischenzeit gelöscht
        if neuer_pfad:
            await bildspeicher.loeschen(neuer_pfad)
        raise NichtGefunden()
    if neuer_pfad:
        await bildspeicher.loeschen(alter_pfad)
    return _antwort(neu)


async def favorit_setzen(kleidungsstueck_id: str, nutzer_id: str, favorit: bool) -> KleidungsstueckAntwort:
    """Nur das Herz umschalten, alles andere bleibt (Wunsch Katha, 24.11.2026)."""
    neu = await repository.aendern(kleidungsstueck_id, nutzer_id, {"favorit": favorit})
    if neu is None:
        raise NichtGefunden()
    return _antwort(neu)


async def alle(nutzer_id: str) -> list[KleidungsstueckAntwort]:
    return [_antwort(k) for k in await repository.alle_des_nutzers(nutzer_id)]


async def eins(kleidungsstueck_id: str, nutzer_id: str) -> KleidungsstueckAntwort:
    kleidungsstueck = await repository.finden(kleidungsstueck_id, nutzer_id)
    if kleidungsstueck is None:
        raise NichtGefunden()
    return _antwort(kleidungsstueck)


async def bild(kleidungsstueck_id: str, nutzer_id: str) -> tuple[bytes, str]:
    """Bildinhalt und Medientyp, nur für den Besitzer des Kleidungsstücks."""
    kleidungsstueck = await repository.finden(kleidungsstueck_id, nutzer_id)
    if kleidungsstueck is None:
        raise NichtGefunden()
    schluessel = kleidungsstueck["bild_pfad"]
    try:
        return await bildspeicher.laden(schluessel), bildspeicher.medientyp(schluessel)
    except bildspeicher.BildFehlt:
        raise NichtGefunden()
