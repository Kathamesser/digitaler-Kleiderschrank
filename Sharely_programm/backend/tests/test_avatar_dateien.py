"""Avatar-Dateien: Die Kopie von messpunkte.json neben der GLB (für den Avatar-Konfigurator im Browser)
muss gleich der Fassung in docs/avatar/ sein. Beide schreibt docs/avatar/skripte/zentimeter_messen.py."""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]  # tests → backend → Sharely_programm → Repo


def test_messpunkte_kopie_fuer_konfigurator_ist_aktuell():
    doku = json.loads((REPO / "docs/avatar/messpunkte.json").read_text(encoding="utf-8"))
    editor = json.loads((REPO / "Sharely_programm/assets/avatar/messpunkte.json").read_text(encoding="utf-8"))
    assert editor == doku, "zentimeter_messen.py neu laufen lassen, es schreibt beide Dateien"
