# Backend (Python, FastAPI)

Client-Server-Architektur mit einem **modular aufgebauten Monolithen** als Backend und einer REST-API (Technische Konzeption 2.3). Datenbank: MongoDB.

## Starten

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env               # macOS/Linux: cp .env.example .env
uvicorn app.main:app --reload
```

Dann im Browser: http://localhost:8000/api/health (Lebenszeichen) und http://localhost:8000/docs (alle Endpunkte zum Ausprobieren). MongoDB muss für die Fach-Endpunkte laufen, lokal oder über MongoDB Atlas (Adresse in `.env`).

Tests: `.venv\Scripts\python -m pytest` im Ordner `backend/` (macOS/Linux: `.venv/bin/python -m pytest`). In VS Code: einmal „Python: Select Interpreter“ → `backend\.venv\Scripts\python.exe`, dann laufen die Tests im Testing-Bereich (Reagenzglas links); die Einstellungen dafür stehen in `.vscode/settings.json`. **Nicht** die Testdatei mit ▶ „Run Python File“ starten: Das nimmt oft das globale Python ohne pytest (Fehler `No module named 'pytest'`) und führt keine Tests aus.

## Aufbau

```
backend/
├── app/
│   ├── main.py            Einstieg: App, Router der Module, /api/health
│   ├── core/
│   │   ├── config.py      Einstellungen aus .env
│   │   ├── datenbank.py   MongoDB-Verbindung (get_db)
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

Die Router sind in `main.py` schon eingehängt und erscheinen unter `/api/<modul>`, sobald sie den ersten Endpunkt haben. Das Datenmodell steht in `docs/datenmodell/README.md`.
