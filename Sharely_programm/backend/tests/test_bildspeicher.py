"""Tests für app/core/bildspeicher.py (Bilder im Ordner oder im Railway Storage Bucket).

Den Bucket ersetzt moto durch eine Attrappe im Arbeitsspeicher, es geht also nichts ins Netz.
"""

import asyncio

import boto3
import pytest
from bson import ObjectId
from fastapi.testclient import TestClient
from moto import mock_aws

from app.core import bildspeicher
from app.core.config import get_settings
from app.main import app
from app.module.kleidung import repository as kleidung_repository
from app.module.nutzer import repository as nutzer_repository

PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
JPEG = b"\xff\xd8\xff\xe0" + b"\x00" * 100
BUCKET = "sharely-test"


@pytest.fixture
def bucket(monkeypatch):
    """Einstellungen wie auf Railway, nur mit Attrappe statt echtem Bucket."""
    with mock_aws():
        s = get_settings()
        for name, wert in {
            "bildspeicher": "bucket",
            "bucket_name": BUCKET,
            "bucket_endpoint": "https://s3.us-east-1.amazonaws.com",
            "bucket_region": "us-east-1",
            "bucket_access_key_id": "test",
            "bucket_secret_access_key": "test",
        }.items():
            monkeypatch.setattr(s, name, wert)
        bildspeicher._s3_client.cache_clear()
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket=BUCKET)
        yield s3
        bildspeicher._s3_client.cache_clear()


def _alle_schluessel(s3) -> list[str]:
    return [o["Key"] for o in s3.list_objects_v2(Bucket=BUCKET).get("Contents", [])]


def test_bucket_speichern_laden_loeschen(bucket):
    asyncio.run(bildspeicher.speichern("nutzer1/abc.png", PNG))
    assert _alle_schluessel(bucket) == ["nutzer1/abc.png"]
    assert bucket.head_object(Bucket=BUCKET, Key="nutzer1/abc.png")["ContentType"] == "image/png"
    assert asyncio.run(bildspeicher.laden("nutzer1/abc.png")) == PNG

    asyncio.run(bildspeicher.loeschen("nutzer1/abc.png"))
    assert _alle_schluessel(bucket) == []
    with pytest.raises(bildspeicher.BildFehlt):
        asyncio.run(bildspeicher.laden("nutzer1/abc.png"))
    asyncio.run(bildspeicher.loeschen("nutzer1/abc.png"))  # zweimal löschen ist kein Fehler


def test_ordner_speichern_laden_loeschen(tmp_path, monkeypatch):
    monkeypatch.setattr(get_settings(), "upload_ordner", str(tmp_path))
    asyncio.run(bildspeicher.speichern("nutzer1/abc.jpg", JPEG))
    assert (tmp_path / "nutzer1" / "abc.jpg").read_bytes() == JPEG
    assert asyncio.run(bildspeicher.laden("nutzer1/abc.jpg")) == JPEG
    asyncio.run(bildspeicher.loeschen("nutzer1/abc.jpg"))
    with pytest.raises(bildspeicher.BildFehlt):
        asyncio.run(bildspeicher.laden("nutzer1/abc.jpg"))


@pytest.mark.parametrize("schluessel", ["../geheim.png", "/etc/passwd", "a/../../b.png", "a\\b.png", ""])
def test_kein_ausbruch_aus_dem_speicher(schluessel, tmp_path, monkeypatch):
    monkeypatch.setattr(get_settings(), "upload_ordner", str(tmp_path))
    with pytest.raises(ValueError):
        asyncio.run(bildspeicher.speichern(schluessel, PNG))


def test_fehlende_bucket_einstellungen_werden_genannt(monkeypatch):
    monkeypatch.setattr(get_settings(), "bildspeicher", "bucket")
    monkeypatch.setattr(get_settings(), "bucket_name", "")
    with pytest.raises(RuntimeError, match="BUCKET_NAME"):
        asyncio.run(bildspeicher.laden("nutzer1/abc.png"))


def test_kleidungsstueck_mit_bild_im_bucket(bucket, monkeypatch, als_test_nutzer):
    """Ganzer Weg über die API: hochladen landet im Bucket, Abruf kommt aus dem Bucket."""
    speicher: dict[str, dict] = {}

    async def anlegen(daten):
        eintrag = {**daten, "id": str(ObjectId())}
        speicher[eintrag["id"]] = eintrag
        return eintrag

    async def finden(kleidungsstueck_id, nutzer_id):
        eintrag = speicher.get(kleidungsstueck_id)
        return eintrag if eintrag and eintrag["nutzer_id"] == nutzer_id else None

    monkeypatch.setattr(kleidung_repository, "anlegen", anlegen)
    monkeypatch.setattr(kleidung_repository, "finden", finden)
    with TestClient(app) as client:
        k = client.post("/api/kleidung", data={"kleidungsart": "tops"}, files={"bild": ("shirt.png", PNG)}).json()
        assert _alle_schluessel(bucket) == [speicher[k["id"]]["bild_pfad"]]
        antwort = client.get(k["bild_url"])
    assert antwort.status_code == 200
    assert antwort.content == PNG
    assert antwort.headers["content-type"] == "image/png"


def test_kein_verwaistes_bild_im_bucket(bucket, monkeypatch, als_test_nutzer):
    async def anlegen(daten):
        raise RuntimeError("Datenbank weg")

    monkeypatch.setattr(kleidung_repository, "anlegen", anlegen)
    with TestClient(app, raise_server_exceptions=False) as client:
        client.post("/api/kleidung", data={"kleidungsart": "tops"}, files={"bild": ("shirt.png", PNG)})
    assert _alle_schluessel(bucket) == []


def test_profilbild_im_bucket_ersetzt_altes(bucket, monkeypatch, als_test_nutzer):
    speicher: dict[str, dict] = {}

    async def finden(nutzer_id):
        return speicher.get(nutzer_id)

    async def profilbild_setzen(nutzer_id, bild_pfad, geaendert_am):
        speicher.setdefault(nutzer_id, {}).update(profilbild_pfad=bild_pfad)

    monkeypatch.setattr(nutzer_repository, "finden", finden)
    monkeypatch.setattr(nutzer_repository, "profilbild_setzen", profilbild_setzen)
    with TestClient(app) as client:
        client.put("/api/nutzer/ich/profilbild", files={"bild": ("a.jpg", JPEG)})
        url = client.put("/api/nutzer/ich/profilbild", files={"bild": ("b.png", PNG)}).json()["profilbild_url"]
        assert len(_alle_schluessel(bucket)) == 1  # Datenschutz: das alte Bild ist weg
        assert client.get(url).content == PNG
        client.delete("/api/nutzer/ich/profilbild")
    assert _alle_schluessel(bucket) == []


def test_umzug_vom_ordner_in_den_bucket(bucket, tmp_path):
    from app.bilder_umziehen import umziehen

    (tmp_path / "n1").mkdir()
    (tmp_path / "n1" / "hier.png").write_bytes(PNG)
    bucket.put_object(Bucket=BUCKET, Key="n1/schon.png", Body=PNG)
    schluessel = ["n1/hier.png", "n1/schon.png", "n2/woanders.png"]

    probe = umziehen(tmp_path, schluessel, ausfuehren=False)
    assert probe == {"hochgeladen": ["n1/hier.png"], "schon_da": ["n1/schon.png"], "nicht_hier": ["n2/woanders.png"]}
    assert sorted(_alle_schluessel(bucket)) == ["n1/schon.png"]  # Probelauf ändert nichts

    umziehen(tmp_path, schluessel, ausfuehren=True)
    assert sorted(_alle_schluessel(bucket)) == ["n1/hier.png", "n1/schon.png"]
    assert (tmp_path / "n1" / "hier.png").is_file()  # Quelle bleibt unangetastet


def test_belegt_zaehlt_nur_den_eigenen_ordner(bucket):
    asyncio.run(bildspeicher.speichern("n1/a.png", PNG))
    asyncio.run(bildspeicher.speichern("n1/b.png", PNG))
    asyncio.run(bildspeicher.speichern("n10/c.png", PNG))  # anderer Nutzer mit ähnlicher ID
    assert asyncio.run(bildspeicher.belegt("n1")) == 2 * len(PNG)
    assert asyncio.run(bildspeicher.belegt("leer")) == 0


def test_speicherlimit_je_nutzer(bucket, monkeypatch, als_test_nutzer):
    """1 GB je Nutzer; hier auf 1 MB verkleinert. Ein Bild, das das Limit sprengen
    würde, wird abgelehnt und nicht gespeichert."""
    from app.core.sicherheit import TEST_NUTZER_ID

    monkeypatch.setattr(get_settings(), "max_speicher_mb_pro_nutzer", 1)
    bucket.put_object(Bucket=BUCKET, Key=f"{TEST_NUTZER_ID}/alt.png", Body=b"\x00" * (1024 * 1024 - 50))

    async def anlegen(daten):
        return {**daten, "id": str(ObjectId())}

    monkeypatch.setattr(kleidung_repository, "anlegen", anlegen)
    with TestClient(app) as client:
        antwort = client.post("/api/kleidung", data={"kleidungsart": "tops"}, files={"bild": ("s.png", PNG)})
    assert antwort.status_code == 507
    assert antwort.json()["detail"] == "Dein Speicher für Bilder ist voll (höchstens 1 MB)."
    assert _alle_schluessel(bucket) == [f"{TEST_NUTZER_ID}/alt.png"]


def test_profilbild_ersetzen_zaehlt_altes_nicht_doppelt(bucket, monkeypatch, als_test_nutzer):
    from app.core.sicherheit import TEST_NUTZER_ID

    speicher: dict[str, dict] = {}

    async def finden(nutzer_id):
        return speicher.get(nutzer_id)

    async def profilbild_setzen(nutzer_id, bild_pfad, geaendert_am):
        speicher.setdefault(nutzer_id, {}).update(profilbild_pfad=bild_pfad)

    monkeypatch.setattr(nutzer_repository, "finden", finden)
    monkeypatch.setattr(nutzer_repository, "profilbild_setzen", profilbild_setzen)
    groß = JPEG + b"\x00" * (600 * 1024)  # zwei davon passen nicht in 1 MB
    monkeypatch.setattr(get_settings(), "max_speicher_mb_pro_nutzer", 1)
    with TestClient(app) as client:
        assert client.put("/api/nutzer/ich/profilbild", files={"bild": ("a.jpg", groß)}).status_code == 200
        assert client.put("/api/nutzer/ich/profilbild", files={"bild": ("b.jpg", groß)}).status_code == 200
    assert len(_alle_schluessel(bucket)) == 1
