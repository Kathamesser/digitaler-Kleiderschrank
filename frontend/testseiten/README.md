# Testseiten (Klick-Prototyp)

Schlichte HTML-Seiten ohne Framework nach den Wireframes der Technischen Konzeption (`docs/konzeption/`, Kapitel 3). Sie dienen zum Ausprobieren des Backends und als Klick-Prototyp, solange React oder Vue noch nicht entschieden ist.

## Seiten

| Seite | Wireframe | Daten |
|---|---|---|
| `index.html` | – | Übersicht aller Seiten |
| `anmeldung.html` | 1, 2 | ohne Backend (Anmeldeverfahren offen), führt direkt zum Schrank |
| `schrank.html` | 5, 6 | live: Liste, Suche, Filterleiste (Alles, Favoriten, Kategorien) und Filtermenü über das Symbol neben der Suche, Aufbau nach dem Desktop-Mockup „Kleidung filtern“ (Favorit, Privat, Farbe, Kategorie, Anlass, Material, Saison, Status, Kaufdatum, Preis) |
| `kleidung-hochladen.html` | 7 | live: User Story 8, Foto + Eigenschaften speichern |
| `kleidungsstueck.html?id=…` | 8 | live: Detailansicht; Bearbeiten/Löschen fehlen im Backend noch |
| `outfits.html` | 9, 10 | Beispieldaten; leerer Zustand mit `outfits.html?leer` |
| `outfit-erstellen.html` | 11 | Auswahl aus dem echten Schrank, Speichern fehlt im Backend |
| `verliehen.html` | 13 | Beispieldaten |
| `freunde.html` | 17 | Beispieldaten |
| `profil.html` | 18 | Anzahl und „Zuletzt hinzugefügt“ live, Rest Beispieldaten |

Noch nicht angelegt: Passwort zurücksetzen (3, 4), Outfit-Detail (12), Anfrage senden (14), Anfragen (15), Leihdetails (16), fremdes Profil (19), Einstellungen (20), Passwort ändern (21).

## Aufbau

- `stil.css`: das gesamte Aussehen. Ganz oben stehen alle Farben, Schrift, Rundungen und Abstände als Variablen (`:root`). **Design an die Mockups anpassen = zuerst diese Variablen ändern, dann die Bausteine darunter.** Alle Seiten ziehen automatisch mit.
- `gemeinsam.js`: Backend-Adresse, Beschriftungen der Auswahlwerte (wie im Backend), Symbole als SVG, untere Navigation, Hilfsfunktionen (`holeJson`, `kleidungsKarte` …).
- Je Seite eine HTML-Datei mit nur dem, was die Seite selbst braucht.

## Weiterverwenden mit React oder Vue

- `stil.css` kann fast unverändert übernommen werden (Klassennamen bleiben).
- Das HTML jeder Seite wird zur Seiten-Komponente in `frontend/src/seiten/`, wiederkehrende Teile (Kachel, Navigation, Kopfband) zu Komponenten in `src/komponenten/`. In React wird dabei z. B. `class` zu `className`.
- Die Backend-Aufrufe aus `gemeinsam.js` und den Seiten wandern nach `src/api/`.

Bleibt das Team ohne Framework, können die Seiten direkt weiterentwickelt werden.

## Starten

1. MongoDB und Backend starten (siehe `backend/README.md`).
2. In einem zweiten Terminal **im Hauptordner des Repos** einen einfachen Webserver auf Port 5173 starten (Hauptordner, damit die Seiten das Logo aus `assets/branding/` finden). Das Backend erlaubt Zugriffe nur von dieser Adresse (CORS, `FRONTEND_URLS` in `.env`):

   ```bash
   python -m http.server 5173
   ```

3. Im Browser öffnen: http://localhost:5173/frontend/testseiten/

Direktes Öffnen per Doppelklick (`file://…`) funktioniert nicht, weil der Browser die Anfragen ans Backend dann blockiert.
