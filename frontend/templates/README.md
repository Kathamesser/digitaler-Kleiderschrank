# Templates (Seiten der Web-App)

HTML-Seiten ohne Framework im Design der Desktop-Mockups (`docs/mockups/desktop/`, seit 20.10.2026; vorher Graustufen nach den Wireframes der Technischen Konzeption). Seit 20.10.2026 sind sie keine Testseiten mehr, sondern die Seiten der Web-App (Ordner bis dahin `frontend/testseiten/`, Entscheidung Katha). Sie laufen ohne Framework, solange React oder Vue noch nicht entschieden ist. Die Felder eines Kleidungsstücks folgen seit 20.10.2026 Manuels ERM (`docs/datenmodell/ERM-SHARELY.md`), das selbst nach den Mockups gebaut ist.

## Seiten

| Seite | Mockup | Daten |
|---|---|---|
| `index.html` | – | Übersicht aller Seiten |
| `anmeldung.html` | Desktop 1, 2 | ohne Backend (Anmeldeverfahren offen), führt direkt zum Hauptmenü |
| `hauptmenue.html` | Hauptmenü – Variante 2 | Zahlen im Kleiderschrank live (eigene, Wunsch-, verliehene, geliehene Artikel), Rest Platzhalter |
| `schrank.html` | Kleiderschrank, Kleidung filtern | live: Liste, Suche (Name, Kleidungsart, Farbe, Material), „Alles“ und Filter-Fenster (Favorit, Privat, Farbe, Kleidungsart, Material, Saison, Status, Kaufdatum, Preis; Kategorie nur zur Ansicht, bis es das Modul Kategorien gibt). Ganzjährige Teile passen zu jeder Saison. „Geliehen“ = Status `geliehen` |
| `kleidung-hochladen.html` | Kleidungsstück hinzufügen | live: User Story 8; Foto per Kamera, Datei oder Ziehen; Name, Farbe, Kleidungsart, Maße (22 Messpunkte), Saison, Material, Kaufdatum, Preis, Favorit, Privat, Status (Eigenes/Geliehen/Wunschartikel; „Verliehen“ gesperrt). Kategorien nur zur Ansicht |
| `kleidungsstueck.html?id=…` | Kleidungsstück – Detailansicht | live, mit Maßen; Kategorien nur als Anzahl (Namen kommen mit dem Modul Kategorien); Bearbeiten, Löschen, Verleihen, Anprobieren fehlen im Backend noch |
| `outfits.html` | Outfits | Beispieldaten; leerer Zustand mit `outfits.html?leer` |
| `outfit-erstellen.html` | Outfit erstellen, Outfit speichern | Auswahl aus dem echten Schrank, Speichern fehlt im Backend |
| `freunde.html` | Freunde | Beispieldaten |
| `verliehen.html` | Freunde-Leih Verleihansicht | Beispieldaten (für alle Freunde statt für einen) |
| `profil.html` | Mein Profil | Beispieldaten |

Noch nicht angelegt: Passwort zurücksetzen (Desktop 3, 4), Nachrichten, Angebote, Garderobe und Kleiderschrank eines Freundes, Detailansichten von Outfits und Teilen eines Freundes, Leih-Detailansicht, Anfrage stellen, Freund hinzufügen, Outfits filtern.

Schriften (DM Sans, Fraunces) kommen von Google Fonts; ohne Internet fallen die Seiten auf Systemschriften zurück.

## Aufbau

- `../static/css/stil.css`: das gesamte Aussehen. Ganz oben stehen alle Farben, Schrift, Rundungen und Abstände als Variablen (`:root`). **Design ändern = zuerst diese Variablen ändern, dann die Bausteine darunter.** Alle Seiten ziehen automatisch mit.
- `../static/js/gemeinsam.js`: Backend-Adresse, Beschriftungen der Auswahlwerte (wie im Backend: Kleidungsarten, Farben, Materialien, Saisons, Status, Messpunkte), vorgegebene Kategorien, Symbole als SVG, Kopfzeile (`seitenkopf`) und Fußleiste (`fussleiste`), Hilfsfunktionen (`holeJson`, `kleidungsKarte` …).
- Je Seite eine HTML-Datei hier in `templates/` mit nur dem, was die Seite selbst braucht. Sie binden `../static/css/stil.css` und `../static/js/gemeinsam.js` ein.

## Weiterverwenden mit React oder Vue

- `stil.css` kann fast unverändert übernommen werden (Klassennamen bleiben).
- Das HTML jeder Seite wird zur Seiten-Komponente (z. B. in `frontend/src/seiten/`), wiederkehrende Teile (Kachel, Kopf- und Fußleiste) zu Komponenten (z. B. `src/komponenten/`). In React wird dabei z. B. `class` zu `className`.
- Die Backend-Aufrufe aus `gemeinsam.js` und den Seiten wandern in ein eigenes Modul (z. B. `src/api/`).

Bleibt das Team ohne Framework, können die Seiten direkt weiterentwickelt werden.

## Starten

1. MongoDB und Backend starten (siehe `backend/README.md`).
2. In einem zweiten Terminal **im Hauptordner des Repos** einen einfachen Webserver auf Port 5173 starten (Hauptordner, damit die Seiten das Logo aus `assets/branding/` finden). Das Backend erlaubt Zugriffe nur von dieser Adresse (CORS, `FRONTEND_URLS` in `.env`):

   ```bash
   python -m http.server 5173
   ```

3. Im Browser öffnen: http://localhost:5173/frontend/templates/

Direktes Öffnen per Doppelklick (`file://…`) funktioniert nicht, weil der Browser die Anfragen ans Backend dann blockiert.
