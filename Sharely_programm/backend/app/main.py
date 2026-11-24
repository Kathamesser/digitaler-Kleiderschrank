"""Einstiegspunkt des Backends. Start (im Ordner Sharely_programm/backend/): uvicorn app.main:app --reload

Was ist das „Backend“? Der Teil von Sharely, der auf dem Server läuft. Er nimmt Anfragen
aus dem Browser entgegen (z. B. „zeig mir meine Kleidungsstücke“), spricht mit der
Datenbank und schickt die Antwort zurück. Der Browser-Teil (die Seiten) heißt „Frontend“.

Diese Datei baut die App zusammen: Sie verbindet die Datenbank, hängt alle Module
(Nutzer, Kleidung, Outfits …) ein und legt fest, welche Ordner der Browser sehen darf.

Liefert neben der API (/api/...) auch die Seiten aus (/frontend/..., /assets/...), damit Sharely
auf einem Server wie Railway als EIN Dienst läuft (Entscheidung Team, 27.10.2026). Lokal geht
weiterhin `python start.py` mit dem eigenen Seiten-Server auf Port 5173.
"""

# „import“ holt fertige Bausteine aus anderen Dateien oder Bibliotheken, damit man sie hier nutzen kann.
from contextlib import asynccontextmanager
from pathlib import Path

# FastAPI ist die Bibliothek, mit der wir das Backend bauen: Sie nimmt Web-Anfragen an
# und leitet sie an die passende Funktion weiter.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.core import bildspeicher, datenbank
from app.core.config import get_settings
# Jedes Modul (Nutzer, Kleidung, …) hat einen eigenen „Router“: eine Sammlung von Adressen
# (z. B. /api/kleidung) mit den Funktionen, die dort antworten.
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
    """Läuft einmal beim Start und einmal beim Beenden der App.
    Alles vor `yield` passiert beim Start, alles danach beim Herunterfahren."""
    datenbank.verbinden()  # Verbindung zur MongoDB-Datenbank öffnen
    # Fehlen die Zugangsdaten für den Bildspeicher, nur warnen statt abzustürzen
    if meldung := bildspeicher.fehlende_einstellungen():
        print(f"WARNUNG: {meldung}", flush=True)  # App läuft trotzdem, nur Hochladen/Bilder gehen nicht
    yield  # ab hier läuft die App und beantwortet Anfragen
    await datenbank.trennen()  # beim Beenden die Datenbankverbindung sauber schließen


# Einstellungen (Datenbank-Adresse usw.) aus der Datei .env lesen
settings = get_settings()
# Die eigentliche App anlegen; „lifespan“ sagt ihr, was beim Start/Ende passieren soll
app = FastAPI(title=settings.app_name, lifespan=lifespan)

# CORS = Sicherheitsregel der Browser: Eine Seite von Adresse A darf nur dann Daten von
# Adresse B holen, wenn B das erlaubt. Lokal laufen Seiten (Port 5173) und Backend (Port 8000)
# auf verschiedenen Adressen, deshalb erlauben wir hier ausdrücklich die Seiten-Adressen.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.frontend_urls,  # nur diese Adressen dürfen zugreifen
    allow_credentials=True,  # Anmelde-Cookie darf mitgeschickt werden
    allow_methods=["*"],  # alle Anfragearten (lesen, anlegen, ändern …)
    allow_headers=["*"],
)

# Alle Module unter der Adresse /api einhängen, z. B. wird der Kleidung-Router zu /api/kleidung
app.include_router(nutzer_router, prefix="/api")
app.include_router(kleidung_router, prefix="/api")
app.include_router(outfits_router, prefix="/api")
app.include_router(freunde_router, prefix="/api")
app.include_router(verleihen_router, prefix="/api")
app.include_router(figuren_router, prefix="/api")
app.include_router(produktimport_router, prefix="/api")
app.include_router(passform_router, prefix="/api")


# „@app.get(...)“ heißt: Ruft jemand diese Adresse auf, antwortet die Funktion darunter.
@app.get("/api/health", tags=["system"])
async def health() -> dict:
    """Lebenszeichen: zeigt, dass das Backend läuft (prüft nicht die Datenbank)."""
    return {"status": "ok"}


# ---------------------------------------------------------------- Seiten ausliefern

PROGRAMM = Path(__file__).resolve().parents[2]  # Ordner Sharely_programm (zwei Ebenen über dieser Datei)

# Nur diese Ordner sind öffentlich. backend/ (mit .env) und ein evtl. vorhandener uploads/-Ordner
# bleiben es nicht: Bilder gibt es nur über die geschützten Bild-Endpunkte der API.
OEFFENTLICHE_ORDNER = {"/frontend": PROGRAMM / "frontend", "/assets": PROGRAMM / "assets"}


class OhneVeralteteDateien(StaticFiles):
    """Wie seiten_server.py: Der Browser fragt bei jeder Datei nach, ob sie sich geändert hat,
    damit nach einem Update keine alte gemeinsam.js mehr läuft.

    StaticFiles liefert Dateien (HTML, Bilder, CSS) einfach so aus, wie sie im Ordner liegen.
    Wir ergänzen nur die Anweisung „no-cache“ (= nicht ungeprüft aus dem Zwischenspeicher nehmen)."""

    async def get_response(self, path, scope):
        antwort = await super().get_response(path, scope)  # Datei ganz normal holen …
        antwort.headers["Cache-Control"] = "no-cache"  # … und den Hinweis an den Browser anhängen
        return antwort


# Jeden öffentlichen Ordner unter seiner Adresse erreichbar machen (falls es ihn gibt)
for adresse, ordner in OEFFENTLICHE_ORDNER.items():
    if ordner.is_dir():
        app.mount(adresse, OhneVeralteteDateien(directory=ordner, html=True), name=adresse.strip("/"))


@app.get("/", include_in_schema=False)
async def startseite() -> RedirectResponse:
    """Wie Sharely_programm/index.html: von der Startadresse direkt zur Anmeldung."""
    return RedirectResponse("/frontend/templates/")
