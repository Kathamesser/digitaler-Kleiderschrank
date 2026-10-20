# Frontend (Web-App)

Single-Page-App im Browser, responsiv für Desktop und Smartphone (Technische Konzeption 2.1). Spricht über die REST-API mit dem Backend (`/api/...`).

**Noch offen:** Frontend-Framework React oder Vue (siehe `BRAIN.md`, offene Fragen). Deshalb ist hier noch kein Projekt generiert. Sobald das entschieden ist, wird das Gerüst mit Vite in diesem Ordner erzeugt (`npm create vite@latest`, Vorlage `react` oder `vue`). Die Unterordner unten bleiben dabei erhalten.

## Klick-Prototyp

Bis das Framework feststeht, gibt es in `testseiten/` HTML-Seiten im Design der Desktop-Mockups (Anmeldung, Hauptmenü, Schrank, Hinzufügen, Detail, Outfits, Freunde, Leihen, Profil), teils live am Backend. Das Aussehen steckt komplett in `testseiten/stil.css` mit Variablen in `:root`; die Datei kann später ins Framework übernommen werden. Details: `testseiten/README.md`.

## Ordner

| Ordner | Inhalt |
|---|---|
| `src/avatar-editor/` | 3D-Avatar-Editor mit Three.js: lädt die GLB, setzt die Regler auf die Morph Targets, Drehen/Zoomen. Bewusst **unabhängig vom Framework** gehalten, kann also schon jetzt entstehen. Grundlage: `docs/avatar/AVATAR-REGLER.md`, `AVATAR-3D-KONZEPT.md` |
| `src/api/` | Aufrufe ans Backend, je Modul eine Datei (`kleidung.js`, `outfits.js` …) |
| `src/seiten/` | Seiten aus den Wireframes: Anmeldung, Schrank, Outfits, Verliehen, Freunde, Profil/Einstellungen (Technische Konzeption Kapitel 3) |
| `src/komponenten/` | Wiederverwendbare Bausteine, z. B. Kleidungsstück-Karte, untere Navigationsleiste, Empty State |
| `public/` | Statische Dateien, z. B. Logo (Original: `assets/branding/sharely-logo.png`) |

Die Avatar-GLB liegt zentral in `assets/avatar/Avatar_Editorgeruest.glb` und wird nicht kopiert. Wie sie im Browser ankommt (Build-Schritt kopiert sie nach `public/` oder das Backend liefert sie aus), wird mit dem Framework festgelegt.
