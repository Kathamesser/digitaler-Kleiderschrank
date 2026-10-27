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
