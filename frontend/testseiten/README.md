# Testseiten (Klick-Prototyp)

HTML-Seiten ohne Framework im Design der Desktop-Mockups (`docs/mockups/desktop/`, seit 20.10.2026; vorher Graustufen nach den Wireframes der Technischen Konzeption). Sie dienen zum Ausprobieren des Backends und als Klick-Prototyp, solange React oder Vue noch nicht entschieden ist. Die Felder eines Kleidungsstücks sind die von heute (Backend/ERM), nicht die abweichenden aus den Mockups (siehe offene Frage in `BRAIN.md`).

## Seiten

| Seite | Mockup | Daten |
|---|---|---|
| `index.html` | – | Übersicht aller Seiten |
| `anmeldung.html` | Desktop 1, 2 | ohne Backend (Anmeldeverfahren offen), führt direkt zum Hauptmenü |
| `hauptmenue.html` | Hauptmenü – Variante 2 | Zahlen im Kleiderschrank live (eigene, Wunsch-, verliehene, geliehene Artikel), Rest Platzhalter |
| `schrank.html` | Kleiderschrank, Kleidung filtern | live: Liste, Suche, „Alles“ und Filter-Fenster (Favorit, Privat, Farbe, Kategorie, Anlass, Material, Saison, Status, Kaufdatum, Preis) |
| `kleidung-hochladen.html` | Kleidungsstück hinzufügen | live: User Story 8; Foto per Kamera, Datei oder Ziehen; Farbe und Material per Farbkreis bzw. Pillen, gespeichert als Text |
| `kleidungsstueck.html?id=…` | Kleidungsstück – Detailansicht | live; Bearbeiten, Löschen, Verleihen, Anprobieren fehlen im Backend noch |
| `outfits.html` | Outfits | Beispieldaten; leerer Zustand mit `outfits.html?leer` |
| `outfit-erstellen.html` | Outfit erstellen, Outfit speichern | Auswahl aus dem echten Schrank, Speichern fehlt im Backend |
| `freunde.html` | Freunde | Beispieldaten |
| `verliehen.html` | Freunde-Leih Verleihansicht | Beispieldaten (für alle Freunde statt für einen) |
| `profil.html` | Mein Profil | Beispieldaten |

Noch nicht angelegt: Passwort zurücksetzen (Desktop 3, 4), Nachrichten, Angebote, Garderobe und Kleiderschrank eines Freundes, Detailansichten von Outfits und Teilen eines Freundes, Leih-Detailansicht, Anfrage stellen, Freund hinzufügen, Outfits filtern.

Schriften (DM Sans, Fraunces) kommen von Google Fonts; ohne Internet fallen die Seiten auf Systemschriften zurück.

## Aufbau

- `stil.css`: das gesamte Aussehen. Ganz oben stehen alle Farben, Schrift, Rundungen und Abstände als Variablen (`:root`). **Design ändern = zuerst diese Variablen ändern, dann die Bausteine darunter.** Alle Seiten ziehen automatisch mit.
- `gemeinsam.js`: Backend-Adresse, Beschriftungen der Auswahlwerte (wie im Backend), Farb- und Materialwerte, Symbole als SVG, Kopfzeile (`seitenkopf`) und Fußleiste (`fussleiste`), Hilfsfunktionen (`holeJson`, `kleidungsKarte` …).
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
