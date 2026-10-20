"""HTTP-Endpunkte des Moduls kleidung.

Aufgabe: Kleidungsstücke anlegen (mit Foto), anzeigen, bearbeiten, löschen; Filter nach Kleidungsart, Suche, Favoriten.
Grundlage: User Story 1, 4, 5 und 8, Konzeption 1.3, Wireframes 5–8.

Hier nur Anfragen entgegennehmen, prüfen lassen (schemas.py) und an service.py
weitergeben. Keine Geschäftslogik und keine Datenbankzugriffe in dieser Datei.
"""

import json
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse
from pydantic import ValidationError

from app.core.config import get_settings
from app.core.sicherheit import aktueller_nutzer
from app.module.kleidung import service
from app.module.kleidung.schemas import (
    Farbe,
    Kleidungsart,
    KleidungsstueckAntwort,
    KleidungsstueckNeu,
    Material,
    Saison,
    StatusBeimAnlegen,
)

router = APIRouter(prefix="/kleidung", tags=["kleidung"])

Nutzer = Annotated[str, Depends(aktueller_nutzer)]


def angaben_aus_formular(
    kleidungsart: Annotated[Kleidungsart, Form()],
    name: Annotated[str | None, Form()] = None,
    favorit: Annotated[bool, Form()] = False,
    privat: Annotated[bool, Form()] = False,
    farbe: Annotated[Farbe | None, Form()] = None,
    material: Annotated[Material | None, Form()] = None,
    saison: Annotated[list[Saison] | None, Form()] = None,
    preis: Annotated[float | None, Form(description="in Euro")] = None,
    kaufdatum: Annotated[date | None, Form()] = None,
    status_: Annotated[
        StatusBeimAnlegen, Form(alias="status", description="im_schrank (Eigenes), geliehen oder wunsch")
    ] = StatusBeimAnlegen.im_schrank,
    kategorie_ids: Annotated[list[str] | None, Form()] = None,
    masse: Annotated[
        str | None, Form(description='JSON-Liste, z. B. [{"messpunkt": "waist-circ", "wert_cm": 80}]')
    ] = None,
) -> KleidungsstueckNeu:
    """Formularfelder → KleidungsstueckNeu. Nötig, weil FastAPI ein
    Formular-Modell nicht zusammen mit einer Datei annimmt. Regelverstöße aus
    dem Modell (z. B. Kaufdatum in der Zukunft) werden zu einer 422-Antwort."""
    try:
        masse_liste = json.loads(masse) if masse else []
    except json.JSONDecodeError:
        raise RequestValidationError([{
            "type": "json_invalid", "loc": ("body", "masse"),
            "msg": "Maße müssen eine JSON-Liste sein.", "input": masse,
        }])
    try:
        return KleidungsstueckNeu(
            kleidungsart=kleidungsart, name=name, favorit=favorit, privat=privat,
            farbe=farbe, material=material, saison=saison or [], preis=preis,
            kaufdatum=kaufdatum, status=status_, kategorie_ids=kategorie_ids or [],
            masse=masse_liste,
        )
    except ValidationError as fehler:
        raise RequestValidationError(fehler.errors(include_url=False, include_context=False))


@router.post("", status_code=status.HTTP_201_CREATED)
async def kleidungsstueck_digitalisieren(
    nutzer_id: Nutzer,
    bild: Annotated[UploadFile, File(description="Foto, JPEG/PNG/WebP")],
    angaben: Annotated[KleidungsstueckNeu, Depends(angaben_aus_formular)],
) -> KleidungsstueckAntwort:
    """User Story 8: Foto hochladen und als Kleidungsstück anlegen.

    Pflicht sind nur `bild` und `kleidungsart`. Mehrfachauswahl (`saison`,
    `kategorie_ids`) wird als wiederholtes Feld geschickt:
    `saison=herbst&saison=winter`. `masse` kommt als JSON-Text.
    """
    # Ein Byte mehr als erlaubt lesen, damit der Service "zu groß" erkennt,
    # ohne beliebig große Dateien in den Speicher zu holen.
    daten = await bild.read(get_settings().max_bild_mb * 1024 * 1024 + 1)
    try:
        return await service.digitalisieren(nutzer_id, angaben, daten)
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
