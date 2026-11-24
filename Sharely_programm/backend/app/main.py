"""Einstiegspunkt des Backends. Start (im Ordner Sharely_programm/backend/): uvicorn app.main:app --reload

Liefert neben der API (/api/...) auch die Seiten aus (/frontend/..., /assets/...), damit Sharely
auf einem Server wie Railway als EIN Dienst läuft (Entscheidung Team, 27.10.2026). Lokal geht
weiterhin `python start.py` mit dem eigenen Seiten-Server auf Port 5173.
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.core import bildspeicher, datenbank
from app.core.config import get_settings
from app.module.nutzer.router import router as nutzer_router
from app.module.kleidung.router import router as kleidung_router
from app.module.outfits.router import router as outfits_router
from app.module.freunde.router import router as freunde_router
from app.module.verleihen.router import router as verleihen_router
from app.module.figuren.router import router as figuren_router
from app.module.produktimport.router import router as produktimport_router
from app.module.passform.router import router as passform_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    datenbank.verbinden()
    if meldung := bildspeicher.fehlende_einstellungen():
        print(f"WARNUNG: {meldung}", flush=True)  # App läuft trotzdem, nur Hochladen/Bilder gehen nicht
    yield
    await datenbank.trennen()


settings = get_settings()
app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.frontend_urls,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(nutzer_router, prefix="/api")
app.include_router(kleidung_router, prefix="/api")
app.include_router(outfits_router, prefix="/api")
app.include_router(freunde_router, prefix="/api")
app.include_router(verleihen_router, prefix="/api")
app.include_router(figuren_router, prefix="/api")
app.include_router(produktimport_router, prefix="/api")
app.include_router(passform_router, prefix="/api")


@app.get("/api/health", tags=["system"])
async def health() -> dict:
    """Lebenszeichen: zeigt, dass das Backend läuft (prüft nicht die Datenbank)."""
    return {"status": "ok"}


# ---------------------------------------------------------------- Seiten ausliefern

PROGRAMM = Path(__file__).resolve().parents[2]  # Ordner Sharely_programm

# Nur diese Ordner sind öffentlich. backend/ (mit .env) und ein evtl. vorhandener uploads/-Ordner
# bleiben es nicht: Bilder gibt es nur über die geschützten Bild-Endpunkte der API.
OEFFENTLICHE_ORDNER = {"/frontend": PROGRAMM / "frontend", "/assets": PROGRAMM / "assets"}


class OhneVeralteteDateien(StaticFiles):
    """Wie seiten_server.py: Der Browser fragt bei jeder Datei nach, ob sie sich geändert hat,
    damit nach einem Update keine alte gemeinsam.js mehr läuft."""

    async def get_response(self, path, scope):
        antwort = await super().get_response(path, scope)
        antwort.headers["Cache-Control"] = "no-cache"
        return antwort


for adresse, ordner in OEFFENTLICHE_ORDNER.items():
    if ordner.is_dir():
        app.mount(adresse, OhneVeralteteDateien(directory=ordner, html=True), name=adresse.strip("/"))


@app.get("/", include_in_schema=False)
async def startseite() -> RedirectResponse:
    """Wie Sharely_programm/index.html: von der Startadresse direkt zur Anmeldung."""
    return RedirectResponse("/frontend/templates/")
