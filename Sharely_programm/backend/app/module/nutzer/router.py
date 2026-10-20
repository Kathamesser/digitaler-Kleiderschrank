"""HTTP-Endpunkte des Moduls nutzer.

Aufgabe: Registrierung, Login/Logout, Passwort zurücksetzen und ändern, Profil und Einstellungen, Konto löschen.
Grundlage: User Story 6 und 7, Konzeption 1.2, Wireframes 1–4 und 18–21, Mockup „Mein Profil“.

Hier nur Anfragen entgegennehmen, prüfen lassen (schemas.py) und an service.py
weitergeben. Keine Geschäftslogik und keine Datenbankzugriffe in dieser Datei.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from app.core.config import get_settings
from app.core.sicherheit import aktueller_nutzer
from app.module.nutzer import service
from app.module.nutzer.schemas import ProfilAntwort

router = APIRouter(prefix="/nutzer", tags=["nutzer"])

Nutzer = Annotated[str, Depends(aktueller_nutzer)]


@router.get("/ich")
async def mein_profil(nutzer_id: Nutzer) -> ProfilAntwort:
    return await service.profil(nutzer_id)


@router.put("/ich/profilbild")
async def profilbild_hochladen(
    nutzer_id: Nutzer,
    bild: Annotated[UploadFile, File(description="Foto, JPEG/PNG/WebP")],
) -> ProfilAntwort:
    """Profilbild hochladen oder ersetzen (Datei oder Kamera-Aufnahme)."""
    # Ein Byte mehr als erlaubt lesen, damit der Service "zu groß" erkennt.
    daten = await bild.read(get_settings().max_bild_mb * 1024 * 1024 + 1)
    try:
        return await service.profilbild_speichern(nutzer_id, daten)
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


@router.delete("/ich/profilbild")
async def profilbild_entfernen(nutzer_id: Nutzer) -> ProfilAntwort:
    """Profilbild löschen; Datei und Verweis werden entfernt (Datenschutz)."""
    return await service.profilbild_entfernen(nutzer_id)


@router.get("/ich/profilbild", response_class=FileResponse)
async def profilbild(nutzer_id: Nutzer):
    """Bild nur für den Nutzer selbst (kein öffentlicher Upload-Ordner). Ob Freunde es
    sehen dürfen, regelt später das Modul freunde."""
    try:
        return FileResponse(await service.profilbild_datei(nutzer_id))
    except service.NichtGefunden:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Kein Profilbild vorhanden.")
