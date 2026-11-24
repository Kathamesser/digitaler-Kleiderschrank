"""Ablage der Bilddateien (Kleidungsfotos, Profilbilder) an EINER Stelle für alle.

Warum: Die Datenbank (MongoDB Atlas) teilen sich alle, die Bilder lagen bisher aber
im Ordner des jeweiligen Rechners bzw. auf dem Railway-Volume. Ein Kleidungsstück,
das jemand lokal angelegt hat, hatte bei den anderen und auf Railway kein Foto.
Deshalb gibt es jetzt zwei Speicherarten (Einstellung `bildspeicher`):

- ``ordner``: Dateien im `upload_ordner` (Vorgabe; für Tests und Arbeiten ohne Netz).
- ``bucket``: Railway Storage Bucket (S3-kompatibel). Lokal und auf Railway dieselben
  Zugangsdaten, also sehen alle dieselben Bilder.

Ein Bild wird über seinen Schlüssel angesprochen, z. B. ``<nutzer_id>/<zufall>.jpg``.
Das ist derselbe Wert, der im Dokument als `bild_pfad`/`profilbild_pfad` steht, darum
ändert sich an der Datenbank nichts. Der Bucket ist privat: Bilder gibt es nur über die
geschützten Bild-Endpunkte der API (Datenschutz, wie vorher beim Ordner).
"""

import asyncio
from functools import lru_cache
from pathlib import Path, PurePosixPath

from app.core.config import get_settings

MEDIENTYPEN = {"jpg": "image/jpeg", "png": "image/png", "webp": "image/webp"}


class BildFehlt(Exception):
    """Unter dem Schlüssel liegt kein Bild (mehr)."""


def medientyp(schluessel: str) -> str:
    return MEDIENTYPEN.get(PurePosixPath(schluessel).suffix.lstrip("."), "application/octet-stream")


def _pruefen(schluessel: str) -> str:
    """Schlüssel kommen nur aus unserem eigenen Code, trotzdem kein Ausbruch aus dem Ordner."""
    teile = PurePosixPath(schluessel).parts
    if not teile or schluessel.startswith("/") or ".." in teile or "\\" in schluessel:
        raise ValueError(f"Ungültiger Bildschlüssel: {schluessel!r}")
    return schluessel


# ------------------------------------------------------------------ Ordner

def _datei(schluessel: str) -> Path:
    return Path(get_settings().upload_ordner) / _pruefen(schluessel)


def _ordner_speichern(schluessel: str, daten: bytes) -> None:
    datei = _datei(schluessel)
    datei.parent.mkdir(parents=True, exist_ok=True)
    datei.write_bytes(daten)


def _ordner_laden(schluessel: str) -> bytes:
    datei = _datei(schluessel)
    if not datei.is_file():
        raise BildFehlt()
    return datei.read_bytes()


def _ordner_loeschen(schluessel: str) -> None:
    _datei(schluessel).unlink(missing_ok=True)


def _ordner_belegt(praefix: str) -> int:
    ordner = _datei(praefix)
    return sum(d.stat().st_size for d in ordner.rglob("*") if d.is_file()) if ordner.is_dir() else 0


# ------------------------------------------------------------------ Bucket

@lru_cache
def _s3_client(endpoint: str, region: str, zugang: str, geheimnis: str, pfad_stil: bool):
    import boto3  # erst hier, damit Tests und der Ordner-Modus ohne boto3 auskommen
    from botocore.config import Config

    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        region_name=region,
        aws_access_key_id=zugang,
        aws_secret_access_key=geheimnis,
        config=Config(s3={"addressing_style": "path" if pfad_stil else "virtual"}),
    )


def _bucket():
    s = get_settings()
    fehlt = [n for n in ("bucket_name", "bucket_endpoint", "bucket_access_key_id", "bucket_secret_access_key")
             if not getattr(s, n)]
    if fehlt:
        raise RuntimeError(
            "BILDSPEICHER=bucket, aber es fehlen Einstellungen: "
            + ", ".join(n.upper() for n in fehlt)
            + " (siehe backend/README.md, Abschnitt „Bilder“)."
        )
    client = _s3_client(s.bucket_endpoint, s.bucket_region, s.bucket_access_key_id,
                        s.bucket_secret_access_key, s.bucket_pfad_stil)
    return client, s.bucket_name


def _bucket_speichern(schluessel: str, daten: bytes) -> None:
    client, name = _bucket()
    client.put_object(Bucket=name, Key=_pruefen(schluessel), Body=daten, ContentType=medientyp(schluessel))


def _bucket_laden(schluessel: str) -> bytes:
    client, name = _bucket()
    try:
        return client.get_object(Bucket=name, Key=_pruefen(schluessel))["Body"].read()
    except client.exceptions.NoSuchKey:
        raise BildFehlt()


def _bucket_loeschen(schluessel: str) -> None:
    client, name = _bucket()
    client.delete_object(Bucket=name, Key=_pruefen(schluessel))  # fehlt es schon, ist das kein Fehler


def _bucket_belegt(praefix: str) -> int:
    client, name = _bucket()
    seiten = client.get_paginator("list_objects_v2").paginate(Bucket=name, Prefix=_pruefen(praefix) + "/")
    return sum(o["Size"] for seite in seiten for o in seite.get("Contents", []))


# ------------------------------------------------------------------ öffentliche Funktionen

def _art() -> str:
    art = get_settings().bildspeicher
    if art not in ("ordner", "bucket"):
        raise RuntimeError(f"Unbekannte Einstellung BILDSPEICHER={art!r} (erlaubt: ordner, bucket).")
    return art


async def speichern(schluessel: str, daten: bytes) -> None:
    funktion = _bucket_speichern if _art() == "bucket" else _ordner_speichern
    await asyncio.to_thread(funktion, schluessel, daten)


async def laden(schluessel: str) -> bytes:
    """Bildinhalt; wirft BildFehlt, wenn es kein Bild unter dem Schlüssel gibt."""
    funktion = _bucket_laden if _art() == "bucket" else _ordner_laden
    return await asyncio.to_thread(funktion, schluessel)


async def belegt(nutzer_id: str) -> int:
    """Wie viele Bytes die Bilder eines Nutzers zusammen belegen (sein Ordner <nutzer_id>/)."""
    funktion = _bucket_belegt if _art() == "bucket" else _ordner_belegt
    return await asyncio.to_thread(funktion, nutzer_id)


async def loeschen(schluessel: str) -> None:
    funktion = _bucket_loeschen if _art() == "bucket" else _ordner_loeschen
    await asyncio.to_thread(funktion, schluessel)
