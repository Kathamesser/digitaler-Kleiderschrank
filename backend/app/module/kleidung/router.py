"""HTTP-Endpunkte des Moduls kleidung.

Aufgabe: Kleidungsstücke anlegen (mit Foto), anzeigen, bearbeiten, löschen; Filter nach Kategorie, Suche, Favoriten.
Grundlage: User Story 1, 4, 5 und 8, Konzeption 1.3, Wireframes 5–8.

Hier nur Anfragen entgegennehmen, prüfen lassen (schemas.py) und an service.py
weitergeben. Keine Geschäftslogik und keine Datenbankzugriffe in dieser Datei.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from app.core.config import get_settings
from app.core.sicherheit import aktueller_nutzer
from app.module.kleidung import service
from app.module.kleidung.schemas import Kategorie, KleidungsstueckAntwort

router = APIRouter(prefix="/kleidung", tags=["kleidung"])

Nutzer = Annotated[str, Depends(aktueller_nutzer)]


@router.post("", status_code=status.HTTP_201_CREATED)
async def kleidungsstueck_digitalisieren(
    nutzer_id: Nutzer,
    bild: Annotated[UploadFile, File(description="Foto, JPEG/PNG/WebP")],
    name: Annotated[str, Form(min_length=1, max_length=100)],
    kategorie: Annotated[Kategorie, Form()],
    farbe: Annotated[str | None, Form(max_length=50)] = None,
    groesse: Annotated[str | None, Form(max_length=20)] = None,
) -> KleidungsstueckAntwort:
    """User Story 8: Foto hochladen und als Kleidungsstück anlegen."""
    # Ein Byte mehr als erlaubt lesen, damit der Service "zu groß" erkennt,
    # ohne beliebig große Dateien in den Speicher zu holen.
    daten = await bild.read(get_settings().max_bild_mb * 1024 * 1024 + 1)
    try:
        return await service.digitalisieren(
            nutzer_id, name.strip(), kategorie, daten, farbe or None, groesse or None
        )
    except service.BildZuGross:
        raise HTTPException(
            status.HTTP_413_CONTENT_TOO_LARGE,
            f"Das Bild ist zu groß. Erlaubt sind höchstens {get_settings().max_bild_mb} MB.",
        )
    except service.BildUngueltig:
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            "Die Datei ist kein unterstütztes Bild. Erlaubt sind JPEG, PNG und WebP.",
        )


@router.get("")
async def kleidungsstuecke_auflisten(nutzer_id: Nutzer) -> list[KleidungsstueckAntwort]:
    return await service.alle(nutzer_id)


@router.get("/{kleidungsstueck_id}")
async def kleidungsstueck_anzeigen(kleidungsstueck_id: str, nutzer_id: Nutzer) -> KleidungsstueckAntwort:
    try:
        return await service.eins(kleidungsstueck_id, nutzer_id)
    except service.NichtGefunden:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Kleidungsstück nicht gefunden.")


@router.get("/{kleidungsstueck_id}/bild", response_class=FileResponse)
async def kleidungsstueck_bild(kleidungsstueck_id: str, nutzer_id: Nutzer):
    """Bild nur für den Besitzer (kein öffentlicher Upload-Ordner, Datenschutz)."""
    try:
        return FileResponse(await service.bild_datei(kleidungsstueck_id, nutzer_id))
    except service.NichtGefunden:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Bild nicht gefunden.")
