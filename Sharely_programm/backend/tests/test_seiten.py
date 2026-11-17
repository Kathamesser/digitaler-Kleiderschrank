"""Das Backend liefert die Seiten selbst aus (für Railway), aber nichts aus backend/ oder uploads/."""

from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


def test_startadresse_fuehrt_zur_anmeldung():
    with TestClient(app) as client:
        antwort = client.get("/", follow_redirects=False)
    assert antwort.status_code in (302, 307)
    assert antwort.headers["location"] == "/frontend/templates/"


def test_seiten_und_dateien_werden_ausgeliefert():
    with TestClient(app) as client:
        anmeldung = client.get("/frontend/templates/")
        stil = client.get("/frontend/static/css/stil.css")
        skript = client.get("/frontend/static/js/gemeinsam.js")
        logo = client.get("/assets/branding/sharely-logo.png")
    assert anmeldung.status_code == 200 and "text/html" in anmeldung.headers["content-type"]
    assert anmeldung.headers["cache-control"] == "no-cache"
    assert stil.status_code == 200
    assert skript.status_code == 200 and 'location.port === "5173"' in skript.text
    assert logo.status_code == 200


def test_backend_und_uploads_bleiben_privat():
    with TestClient(app) as client:
        for adresse in ("/backend/.env", "/backend/app/main.py", "/uploads/", "/frontend/../backend/.env",
                        "/frontend/%2e%2e/backend/.env", "/assets/../backend/.env"):
            antwort = client.get(adresse)
            assert antwort.status_code == 404, adresse
            assert "MONGODB" not in antwort.text, adresse


def test_api_bleibt_vorrang():
    with TestClient(app) as client:
        assert client.get("/api/health").json() == {"status": "ok"}


def _pakete(datei: Path) -> set[str]:
    zeilen = datei.read_text(encoding="utf-8").splitlines()
    pakete = set()
    for zeile in zeilen:
        zeile = zeile.strip()
        if zeile.startswith("# Tests"):
            break  # ab hier nur Test-Pakete, die Railway nicht braucht
        if zeile and not zeile.startswith("#"):
            pakete.add(zeile)
    return pakete


def test_railway_pakete_wie_im_backend():
    """Sharely_programm/requirements.txt (für Railway) muss dieselben Pakete nennen wie
    backend/requirements.txt, sonst fehlt auf dem Server etwas."""
    backend = Path(__file__).resolve().parents[1]
    assert _pakete(backend.parent / "requirements.txt") == _pakete(backend / "requirements.txt")
