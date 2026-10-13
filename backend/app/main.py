"""Einstiegspunkt des Backends. Start (im Ordner backend/): uvicorn app.main:app --reload"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import datenbank
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
