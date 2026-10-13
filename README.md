# Sharely — Digitaler Kleiderschrank

Abschlussprüfungsprojekt (3-Personen-Team): Kleidung bildlich erfassen und kategorisieren, zu Outfits kombinieren, Wunschartikel per KI importieren — und als Kernfeature ein frei anpassbarer 3D-Avatar, der die ausgewählten Klamotten trägt.

Die Umsetzung startet neu nach dem Zielbild (Python/FastAPI, MongoDB, JavaScript/Three.js). Der frühere Flask-Experimentierstand wurde am 06.10.2026 entfernt und ist bei Bedarf in der Git-Historie nachlesbar.

## Projektstruktur

```
backend/            Python/FastAPI, modularer Monolith (Start und Aufbau: backend/README.md)
frontend/           Web-App im Browser, Three.js-Avatar-Editor (Framework noch offen: frontend/README.md)
uploads/            hochgeladene Bilder, nur lokal, nicht im Repo
assets/             Avatar-Dateien (GLB, Werkstatt) und Logo
docs/datenmodell/   ERM und Abbildung auf MongoDB-Collections
docs/api/           Absprachen zur REST-API
docs/avatar/        Avatar: Regler, Pipeline, Figur-Datenmodell, Zentimeter
docs/konzeption/    Technische Konzeption (PDF, inkl. Wireframes)
```

## Dokumente

- `BRAIN.md` — gemeinsames Team-Gedächtnis (aktueller Stand, offene Entscheidungen, Log)
- `ROADMAP.md` / `roadmap.html` — Meilensteinplan und Tech-Stack-Entscheidung
- `AVATAR-3D-KONZEPT.md` — Umsetzungskonzept 3D-Avatar
- `Userstory.md` — User Stories
- `CLAUDE.md` — Projektkontext für Claude-Sitzungen
