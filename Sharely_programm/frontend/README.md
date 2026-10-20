# Frontend (Web-App)

Single-Page-App im Browser, responsiv für Desktop und Smartphone (Technische Konzeption 2.1). Spricht über die REST-API mit dem Backend (`/api/...`).

**Noch offen:** Frontend-Framework React oder Vue (siehe `BRAIN.md`, offene Fragen). Deshalb ist hier noch kein Projekt generiert. Sobald das entschieden ist, wird das Gerüst mit Vite in diesem Ordner erzeugt (`npm create vite@latest`, Vorlage `react` oder `vue`). Die Unterordner unten bleiben dabei erhalten.

## Seiten (Templates)

Bis das Framework feststeht, liegen die Seiten der Web-App in `templates/`: HTML-Seiten im Design der Desktop-Mockups (Anmeldung, Hauptmenü, Schrank, Hinzufügen, Detail, Outfits, Freunde, Leihen, Profil), teils live am Backend. Das Aussehen steckt komplett in `static/css/stil.css` mit Variablen in `:root`; die Datei kann später ins Framework übernommen werden. Details: `templates/README.md`.

## Ordner

| Ordner | Inhalt |
|---|---|
| `src/avatar-editor/` | 3D-Avatar-Editor mit Three.js: lädt die GLB, setzt die Regler auf die Morph Targets, Drehen/Zoomen. Bewusst **unabhängig vom Framework** gehalten, kann also schon jetzt entstehen. Grundlage: `docs/avatar/AVATAR-REGLER.md`, `docs/planung/AVATAR-3D-KONZEPT.md` |
| `templates/` | Die Seiten der Web-App als HTML, eine Datei je Seite (Übersicht und Start: `templates/README.md`) |
| `static/css/` | `stil.css`: das gesamte Aussehen, Farben und Schriften als Variablen in `:root` |
| `static/js/` | `gemeinsam.js`: Backend-Adresse, Auswahlwerte, Symbole, Kopf- und Fußleiste, Kacheln |
| `src/avatar-editor/` | siehe oben |

Das Logo liegt nur in `Sharely_programm/assets/branding/` und wird von den Seiten direkt von dort geladen. Ordner für ein Framework (z. B. `src/seiten/`, `src/komponenten/`, `src/api/`) werden erst angelegt, wenn React oder Vue entschieden ist (Ordnerstruktur aufgeräumt am 20.10.2026).

Die Avatar-GLB liegt zentral in `Sharely_programm/assets/avatar/Avatar_Editorgeruest.glb` und wird nicht kopiert. Wie sie im Browser ankommt (Build-Schritt kopiert sie oder das Backend liefert sie aus), wird mit dem Framework festgelegt.
