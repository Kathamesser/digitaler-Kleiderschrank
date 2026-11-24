# Backend (Python, FastAPI)

Client-Server-Architektur mit einem **modular aufgebauten Monolithen** als Backend und einer REST-API (Technische Konzeption 2.3). Datenbank: MongoDB.

## Starten

Alles zusammen (Backend und Seiten): im Ordner `Sharely_programm` `python start.py`. Die Einrichtung unten (`.venv`, Pakete, `.env`) braucht es trotzdem einmal vorher. Nur das Backend:

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

## Auf Railway bereitstellen

Entscheidung Team, 27.10.2026: Sharely läuft auf Railway als **ein** Dienst. Das Backend liefert dort auch die Seiten aus (`/frontend/…`, `/assets/…`, `/` führt zur Anmeldung); `backend/` und `uploads/` sind nicht öffentlich. Die Datenbank bleibt MongoDB Atlas. Einstellungen im Railway-Dienst:

| Einstellung | Wert |
|---|---|
| Root Directory | `Sharely_programm` (dort liegt eine eigene `requirements.txt` mit denselben Paketen wie `backend/requirements.txt`, ohne Test-Pakete; ein Test prüft, dass beide zusammenpassen. Neue Pakete also in beide Dateien eintragen.) |
| Custom Start Command | `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Healthcheck Path | `/api/health` |
| Bilder | Railway Storage Bucket, siehe Abschnitt „Bilder“ unten. Das frühere Volume (`/data`, `UPLOAD_ORDNER=/data/uploads`) wird nicht mehr gebraucht; alte Bilder wurden bewusst nicht übernommen |
| Variablen | `MONGODB_URL` (Atlas-Adresse mit eigenem Datenbank-Benutzer, nie ins Repo), `MONGODB_DATENBANK=sharely`, `COOKIE_SECURE=true`, dazu die `BUCKET_…`-Variablen aus dem Abschnitt „Bilder“ |

In Atlas muss Railway zugreifen dürfen: Railway hat keine feste IP, daher unter „Network Access“ `0.0.0.0/0` (abgesichert über eigene Datenbank-Benutzer mit starken Passwörtern). Lokal ändert sich nichts: weiter `python start.py`; die Seiten erkennen am Port 5173, dass das Backend auf `localhost:8000` läuft.

## Bilder

Kleidungsfotos und Profilbilder liegen an **einer** Stelle für alle: im privaten **Railway Storage Bucket** (S3-kompatibel) im Railway-Projekt (24.11.2026, Christian). Vorher lagen sie im Ordner des jeweiligen Rechners bzw. auf dem Railway-Volume; weil sich alle dieselbe Atlas-Datenbank teilen, fehlten dann bei den anderen die Fotos. Die alten Bilder wurden nicht übernommen (Entscheidung Christian, 24.11.2026): Kleidungsstücke von vorher zeigen kein Foto mehr, den lokalen Ordner `Sharely_programm/uploads/` kann jeder löschen. Code: `app/core/bildspeicher.py`. In der Datenbank steht weiter nur der Schlüssel (`bild_pfad`, `profilbild_pfad`, z. B. `<nutzer_id>/<zufall>.jpg`); Bilder gibt es nur über die geschützten Bild-Endpunkte der API, der Bucket ist nicht öffentlich.

Einstellungen (in `backend/.env` bzw. als Railway-Variablen):

| Variable | Wert |
|---|---|
| `BILDSPEICHER` | `bucket` (Vorgabe, gemeinsamer Bucket) oder `ordner` (nur `UPLOAD_ORDNER` auf diesem Rechner, z. B. ohne Netz; die Tests nutzen immer `ordner`) |
| `BUCKET_NAME` | Wert `BUCKET` aus dem Reiter „Credentials“ des Buckets in Railway (nicht der Anzeigename) |
| `BUCKET_ENDPOINT` | Wert `ENDPOINT` |
| `BUCKET_REGION` | Wert `REGION` (meist `auto`) |
| `BUCKET_ACCESS_KEY_ID` | Wert `ACCESS_KEY_ID` |
| `BUCKET_SECRET_ACCESS_KEY` | Wert `SECRET_ACCESS_KEY` |
| `BUCKET_PFAD_STIL` | nur `true`, wenn der Reiter „Credentials“ Path-Style verlangt |

Zugangsdaten nie ins Repo oder in Chats. Auf Railway setzt man sie als Verweise auf den Bucket (z. B. `BUCKET_NAME=${{Bucket.BUCKET}}`, „Bucket“ = Name des Buckets im Projekt); lokal kopiert jeder die Werte aus Railway in seine `.env`. Fehlen sie, meldet das Backend beim Start eine WARNUNG; die App läuft, nur Hochladen und Bilder gehen dann nicht.

**Speicherlimit:** Jeder Nutzer darf für seine Bilder zusammen höchstens `MAX_SPEICHER_MB_PRO_NUTZER` belegen (Vorgabe 1024 = 1 GB, Vorschlag Christian 24.11.2026). Gezählt wird alles in seinem Ordner `<nutzer_id>/`; ein ersetztes Profilbild zählt dabei nicht doppelt. Wird es überschritten, antwortet die API mit 507 und „Dein Speicher für Bilder ist voll (höchstens 1 GB).“

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
│   │   └── sicherheit.py  Passwort-Hashing (Argon2), Sitzungen, aktueller_nutzer
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
