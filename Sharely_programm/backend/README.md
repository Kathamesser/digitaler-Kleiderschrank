# Backend (Python, FastAPI)

Client-Server-Architektur mit einem **modular aufgebauten Monolithen** als Backend und einer REST-API (Technische Konzeption 2.3). Datenbank: MongoDB.

## Starten

```bash
cd Sharely_programm/backend
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env               # macOS/Linux: cp .env.example .env
uvicorn app.main:app --reload
```

Dann im Browser: http://localhost:8000/api/health (Lebenszeichen) und http://localhost:8000/docs (alle Endpunkte zum Ausprobieren). MongoDB muss für die Fach-Endpunkte laufen, lokal oder über MongoDB Atlas (Adresse in `.env`).

Tests: `.venv\Scripts\python -m pytest` im Ordner `Sharely_programm/backend/` (macOS/Linux: `.venv/bin/python -m pytest`). In VS Code: einmal „Python: Select Interpreter“ → `backend\.venv\Scripts\python.exe`, dann laufen die Tests im Testing-Bereich (Reagenzglas links); die Einstellungen dafür stehen in `.vscode/settings.json`. **Nicht** die Testdatei mit ▶ „Run Python File“ starten: Das nimmt oft das globale Python ohne pytest (Fehler `No module named 'pytest'`) und führt keine Tests aus.

## Datenbank einrichten

Einmal nach dem ersten Start und immer, wenn sich das Datenmodell ändert (MongoDB muss laufen, Adresse in `.env`):

```bash
cd Sharely_programm/backend
.venv\Scripts\python -m app.datenbank_einrichten               # macOS/Linux: .venv/bin/python -m …
.venv\Scripts\python -m app.datenbank_einrichten --pruefen     # nur anzeigen, was fehlt oder abweicht
.venv\Scripts\python -m app.datenbank_einrichten --stammdaten  # zusätzlich Kleidungsarten, vorgegebene Kategorien und Test-Nutzer
```

Das legt alle 13 Collections aus dem ERM an (`docs/datenmodell/ERM-SHARELY.md`), jeweils mit Prüfregel (`$jsonSchema`) und Indizes. Ohne `--stammdaten` legt es keine Daten an. Mit `--stammdaten` kommt auch der Test-Nutzer aus `app/core/sicherheit.py` dazu (Platzhalter bis zum echten Login, ohne gültiges Passwort), damit z. B. das Profilbild die Prüfregel für `nutzer` erfüllt; es löscht nie etwas, mehrfaches Ausführen schadet nicht. Was eingerichtet wird, steht in `app/core/datenbank_struktur.py`. Die Prüfregeln prüfen nur Pflichtfelder, Datentypen und feste Wertelisten (Farbe, Material, Saison, Status, Messpunkte …); die Listen stehen an einer Stelle in `app/core/wertelisten.py`, die Module bauen ihre Enums daraus. Ändert sich dort etwas, das Skript erneut ausführen. Tests dazu: `tests/test_datenbank_struktur.py`.

## Aufbau

```
Sharely_programm/backend/
├── app/
│   ├── main.py            Einstieg: App, Router der Module, /api/health
│   ├── datenbank_einrichten.py  Skript: Datenbank nach dem ERM einrichten
│   ├── core/
│   │   ├── config.py      Einstellungen aus .env
│   │   ├── datenbank.py   MongoDB-Verbindung (get_db)
│   │   ├── datenbank_struktur.py  Collections, Prüfregeln, Indizes (nach dem ERM)
│   │   ├── wertelisten.py  feste Listen (Kleidungsart, Farbe, Material, …)
│   │   └── sicherheit.py  Passwort-Hashing, Anmeldung (Verfahren noch offen)
│   └── module/            ein Ordner je Fachbereich
│       ├── nutzer/        Registrierung, Login, Passwort, Profil
│       ├── kleidung/      Kleiderschrank: Kleidungsstücke, Filter, Favoriten
│       ├── outfits/       Outfits
│       ├── freunde/       Freunde, Anfragen
│       ├── verleihen/     Leihen und Verschenken
│       ├── figuren/       3D-Avatar-Figuren (Reglerwerte)
│       ├── produktimport/ KI-Import, Wunschliste
│       └── passform/      Passform-Bewertung passt/eng/weit
├── tests/
├── requirements.txt
└── .env.example           Vorlage für die lokale .env (wird nie committet)
```

## Aufbau eines Moduls

Jedes Modul hat dieselben vier Dateien. Die Richtung ist immer **router → service → repository**:

| Datei | Aufgabe |
|---|---|
| `router.py` | HTTP-Endpunkte (`@router.get(...)`). Nimmt Anfragen an, gibt Antworten zurück, sonst nichts. |
| `schemas.py` | Pydantic-Modelle: Form der Daten, die rein- und rausgehen, inkl. Prüfung (z. B. Wärmegrad 1–5). |
| `service.py` | Geschäftslogik in reinem Python: Regeln, Berechtigungen, Berechnungen. Gut testbar. |
| `repository.py` | Einziger Ort, der die MongoDB-Collection liest und schreibt. |

`passform` hat keine eigene Collection und deshalb kein `repository.py`. Es nutzt die Daten aus `figuren` und `kleidung`.

Module rufen sich untereinander nur über ihre `service.py` auf, nie direkt über die Repositories eines anderen Moduls. So bleiben die Module austauschbar und könnten später einzeln herausgelöst werden (z. B. der KI-Import).

Die Router sind in `main.py` schon eingehängt und erscheinen unter `/api/<modul>`, sobald sie den ersten Endpunkt haben. Das Datenmodell steht in `docs/datenmodell/ERM-SHARELY.md`.
