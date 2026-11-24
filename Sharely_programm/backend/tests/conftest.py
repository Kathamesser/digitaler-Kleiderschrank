"""Gemeinsame Fixtures für die Tests.

Was sind diese Tests? Kleine Programme, die das Backend automatisch ausprobieren, z. B.
„lade ein Bild hoch und prüfe, ob das Kleidungsstück danach in der Liste steht“. Man startet
alle mit `python -m pytest` im Ordner backend/. Grün heißt: alles verhält sich wie erwartet.
So merkt man sofort, wenn eine Änderung etwas anderes kaputt macht.

Begriffe:
- Jede Funktion, deren Name mit test_ beginnt, ist ein Test.
- „assert“ heißt „stelle sicher, dass …“: Stimmt die Aussage nicht, schlägt der Test fehl.
- Eine „Fixture“ (@pytest.fixture) bereitet etwas für Tests vor und räumt danach auf.
  Code vor „yield“ läuft vor dem Test, Code danach hinterher.
- TestClient spielt den Browser: Er schickt Anfragen ans Backend, ohne dass ein Server läuft.
- monkeypatch ersetzt für die Dauer eines Tests etwas durch eine Attrappe (z. B. die echte
  Datenbank durch einen Speicher im Arbeitsspeicher), damit Tests ohne Internet laufen.
"""

import pytest

from app.core.sicherheit import TEST_NUTZER_ID, aktueller_nutzer
from app.main import app


@pytest.fixture
def als_test_nutzer():
    """Anmeldung überspringen: Alle Anfragen gehören dem Test-Nutzer. Für Tests, die
    nicht die Anmeldung selbst prüfen (die steht in test_anmeldung.py)."""
    app.dependency_overrides[aktueller_nutzer] = lambda: TEST_NUTZER_ID
    yield
    app.dependency_overrides.pop(aktueller_nutzer, None)


@pytest.fixture(autouse=True)
def bilder_im_ordner(monkeypatch):
    """Tests legen Bilder nie im gemeinsamen Bucket ab, auch wenn die eigene .env
    BILDSPEICHER=bucket enthält (das ist auch die Vorgabe). Den Bucket prüft test_bildspeicher.py mit einer Attrappe."""
    from app.core.config import get_settings

    monkeypatch.setattr(get_settings(), "bildspeicher", "ordner")
