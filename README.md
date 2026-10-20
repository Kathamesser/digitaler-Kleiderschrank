# Sharely — Digitaler Kleiderschrank

Abschlussprüfungsprojekt (3-Personen-Team): Kleidung bildlich erfassen und kategorisieren, zu Outfits kombinieren, Wunschartikel per KI importieren — und als Kernfeature ein frei anpassbarer 3D-Avatar, der die ausgewählten Klamotten trägt.

Die Umsetzung startet neu nach dem Zielbild (Python/FastAPI, MongoDB, JavaScript/Three.js). Der frühere Flask-Experimentierstand wurde am 06.10.2026 entfernt und ist bei Bedarf in der Git-Historie nachlesbar.

## Projektstruktur

```
README.md, CLAUDE.md, BRAIN.md   Einstieg, Kontext für Claude, Team-Gedächtnis
Sharely_programm/         alles, was die Anwendung zum Laufen braucht
  backend/                Python/FastAPI, modularer Monolith (Start und Aufbau: Sharely_programm/backend/README.md)
    app/core/             Einstellungen, Datenbank, Sicherheit
    app/module/           ein Ordner je Fachbereich (router → service → repository)
    tests/                pytest
  frontend/               Web-App im Browser (Sharely_programm/frontend/README.md)
    templates/            die Seiten (HTML), Start: templates/index.html
    static/css/           Aussehen (stil.css)
    static/js/            gemeinsame Bausteine (gemeinsam.js)
    src/avatar-editor/    3D-Avatar-Editor mit Three.js
  assets/                 Avatar-Dateien (GLB, Werkstatt) und Logo
  uploads/                hochgeladene Bilder, nur lokal, nicht im Repo
docs/                     Dokumentation (nicht nötig, damit die Anwendung läuft)
  PROJEKTDOKUMENTATION.md Verlauf, Entscheidungen, Soll-Ist-Vergleich
  planung/                Roadmap, Avatar-Konzept, User Stories
  konzeption/             Technische Konzeption (PDF, inkl. Wireframes)
  mockups/                Desktop-Mockups (PNG)
  datenmodell/            ERM und Abbildung auf MongoDB-Collections
  api/                    Absprachen zur REST-API
  avatar/                 Avatar: Regler, Pipeline, Skripte, Figur-Datenmodell, Zentimeter
```

## Dokumente

- `docs/PROJEKTDOKUMENTATION.md` — Projektdokumentation (Verlauf, Entscheidungen, Soll-Ist-Vergleich)
- `BRAIN.md` — gemeinsames Team-Gedächtnis (aktueller Stand, offene Entscheidungen, Log)
- `docs/planung/ROADMAP.md` / `docs/planung/roadmap.html` — Meilensteinplan und Tech-Stack-Entscheidung
- `docs/planung/AVATAR-3D-KONZEPT.md` — Umsetzungskonzept 3D-Avatar
- `docs/planung/Userstory.md` — User Stories
- `CLAUDE.md` — Projektkontext für Claude-Sitzungen
