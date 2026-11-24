"""Gemeinsame Fixtures für die Tests."""

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
    BILDSPEICHER=bucket enthält. Den Bucket prüft test_bildspeicher.py mit einer Attrappe."""
    from app.core.config import get_settings

    monkeypatch.setattr(get_settings(), "bildspeicher", "ordner")
