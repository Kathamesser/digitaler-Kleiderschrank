# Templates (Seiten der Web-App)

HTML-Seiten ohne Framework im Design der Desktop-Mockups (`docs/mockups/desktop/`, seit 20.10.2026; vorher Graustufen nach den Wireframes der Technischen Konzeption). Seit 20.10.2026 sind sie keine Testseiten mehr, sondern die Seiten der Web-App (Ordner bis dahin `Sharely_programm/frontend/testseiten/`, Entscheidung Katha). Sie laufen ohne Framework, solange React oder Vue noch nicht entschieden ist. Die Felder eines Kleidungsstücks folgen seit 20.10.2026 Manuels ERM (`docs/datenmodell/ERM-SHARELY.md`), das selbst nach den Mockups gebaut ist.

## Seiten

| Seite | Mockup | Daten |
|---|---|---|
| `index.html` | Desktop 1, 2 | live: Anmeldung und Registrierung (`/api/nutzer/anmelden`, `/registrieren`), danach ins Hauptmenü; zeigt immer das Formular, auch wenn man noch angemeldet ist |
| `passwort-vergessen.html` | Desktop 3 | E-Mail für den Reset-Link, ohne Backend; Meldung verrät nicht, ob es das Konto gibt |
| `passwort-neu.html` | Desktop 4 | Ziel des Reset-Links: neues Passwort mit Prüfliste (8 Zeichen, Sonderzeichen, gleich), ohne Backend |
| `hauptmenue.html` | Hauptmenü – Variante 2 | Zahlen im Kleiderschrank live (eigene, Wunsch-, verliehene, geliehene Artikel), „x neu“ bei Nachrichten aus Beispieldaten, Rest Platzhalter |
| `schrank.html` | Kleiderschrank, Kleidung filtern | live: Liste, Suche (Name, Kleidungsart, Farbe, Material), „Alles“ und Filter-Fenster (Favorit, Privat, Farbe, Kleidungsart, Material, Saison, Status, Kaufdatum, Preis; Kategorie nur zur Ansicht, bis es das Modul Kategorien gibt). Ganzjährige Teile passen zu jeder Saison. „Geliehen“ = Status `geliehen` |
| `kleidung-hochladen.html` | Kleidungsstück hinzufügen | live: User Story 8; Foto per Kamera, Datei oder Ziehen; Name, Farbe, Kleidungsart, Maße (24 Messpunkte), Saison, Material, Kaufdatum, Preis, Favorit, Privat, Status (Eigenes/Geliehen/Wunschartikel; „Verliehen“ gesperrt). Kategorien nur zur Ansicht |
| `kleidungsstueck.html?id=…` | Kleidungsstück – Detailansicht, Anfrage stellen – Leihen / Verschenken | live, mit Maßen; Kategorien nur als Anzahl (Namen kommen mit dem Modul Kategorien). „Verleihen / Verschenken“ öffnet das Fenster „Anfrage senden“ (Beispiel-Freunde, nur bei Status Eigenes); Bearbeiten, Löschen, Anprobieren und das Senden fehlen im Backend noch |
| `outfits.html` | Outfits, Outfit – Detailansicht, Outfits filtern | Beispieldaten; Klick auf ein Outfit öffnet die Detailansicht (Favorit, Löschen nur in der Anzeige), Filter nach Name, Kategorie und Kleidungsstück; leerer Zustand mit `outfits.html?leer` |
| `outfit-erstellen.html` | Outfit erstellen, Outfit speichern | Auswahl aus dem echten Schrank, Speichern fehlt im Backend |
| `freunde.html` | Freunde, Freund hinzufügen | Beispieldaten; „Freund hinzufügen“ sucht über den genauen Nutzernamen (Beispiele: `AnnaK`, `paul.m`); Links zu Kleiderschrank und Garderobe des Freundes |
| `freund-schrank.html?freund=lena` | Kleiderschrank eines Freundes, Kleidungsstück eines Freundes – Detailansicht, Anfrage an Freund | Beispieldaten; Status Verfügbar / Bei dir / Verliehen, „Nur verfügbare“; Detail und Anfrage (Leihen oder Geschenkt bekommen) als Fenster |
| `freund-garderobe.html?freund=lena` | Garderobe eines Freundes, Outfit eines Freundes – Detailansicht | Beispieldaten; freigegebener Avatar, Klick auf ein verfügbares Teil im Outfit öffnet die Anfrage |
| `nachrichten.html` | Nachrichten | Beispieldaten: Leih- und Geschenkanfragen annehmen/ablehnen, Neuigkeiten mit „Neu“, „Mehr lesen“ und „Alle gelesen“ |
| `verliehen.html` | Freunde-Leih Verleihansicht, Leih-Detailansicht | Beispieldaten (für alle Freunde statt für einen); Klick auf einen Eintrag öffnet die Leihdetails, „überfällig“ wird aus dem Rückgabedatum berechnet |
| `profil.html` | Mein Profil | Profilbild live: hochladen, mit der Kamera aufnehmen, entfernen; Name und „Mitglied seit“ live; „Nutzer wechseln“ meldet ab |

**Anmeldung (seit 27.10.2026):** Alle Seiten mit Kopfzeile laden über `seitenkopf()` den angemeldeten Nutzer (`ich()` in `gemeinsam.js`) und zeigen dessen Namen. Ohne Anmeldung leitet `api()` zu `index.html` weiter. Knöpfe und Links mit `data-abmelden` melden ab (Hauptmenü „Abmelden“, Profil „Nutzer wechseln“). Ohne Anmeldung erreichbar sind nur `index.html` und die beiden Passwort-Seiten.

Seit 27.10.2026 hat jedes Desktop-Mockup eine Seite oder ein Fenster. Fenster (Mockups „Overlay“/„Fenster“) sind `<dialog>`-Elemente in der Seite, aus der sie geöffnet werden. Noch nicht angelegt: Angebote (kein Mockup, laut ERM „kommen später“).

Wo die Mockups vom ERM abweichen, gilt das ERM: Farbe „Mint“ gibt es nicht (Beispiel jetzt Grün), Outfits zeigen Kategorien statt Anlass, Outfit-Detail zeigt zusätzlich „Privat“.

Beispieldaten für alles ohne Backend stehen gesammelt in `../static/js/beispieldaten.js` und fliegen raus, sobald die Module stehen.

Schriften (DM Sans, Fraunces) kommen von Google Fonts; ohne Internet fallen die Seiten auf Systemschriften zurück.

## Aufbau

- `../static/css/stil.css`: das gesamte Aussehen. Ganz oben stehen alle Farben, Schrift, Rundungen und Abstände als Variablen (`:root`). **Design ändern = zuerst diese Variablen ändern, dann die Bausteine darunter.** Alle Seiten ziehen automatisch mit.
- `../static/js/beispieldaten.js`: Beispieldaten für Freunde, Teile und Outfits eines Freundes, Leihanfragen und Neuigkeiten.
- `../static/js/anfrage.js`: Fenster „Anfrage an …“ (Teil eines Freundes anfragen), genutzt von `freund-schrank.html` und `freund-garderobe.html`.
- `../static/js/gemeinsam.js`: Backend-Adresse, Beschriftungen der Auswahlwerte (wie im Backend: Kleidungsarten, Farben, Materialien, Saisons, Status, Messpunkte), vorgegebene Kategorien, Symbole als SVG, Kopfzeile (`seitenkopf`) und Fußleiste (`fussleiste`), Hilfsfunktionen (`holeJson`, `kleidungsKarte` …).
- Je Seite eine HTML-Datei hier in `templates/` mit nur dem, was die Seite selbst braucht. Sie binden `../static/css/stil.css` und `../static/js/gemeinsam.js` ein.

## Weiterverwenden mit React oder Vue

- `stil.css` kann fast unverändert übernommen werden (Klassennamen bleiben).
- Das HTML jeder Seite wird zur Seiten-Komponente (z. B. in `Sharely_programm/frontend/src/seiten/`), wiederkehrende Teile (Kachel, Kopf- und Fußleiste) zu Komponenten (z. B. `src/komponenten/`). In React wird dabei z. B. `class` zu `className`.
- Die Backend-Aufrufe aus `gemeinsam.js` und den Seiten wandern in ein eigenes Modul (z. B. `src/api/`).

Bleibt das Team ohne Framework, können die Seiten direkt weiterentwickelt werden.

## Starten

**Kurzweg (seit 29.10.2026):** Im Ordner `Sharely_programm` `python start.py` ausführen. Das startet Backend und Seiten-Server zusammen, öffnet http://localhost:5173/ und beendet mit Strg+C beides. Voraussetzung ist die einmalige Einrichtung des Backends (`.venv`, `.env`, siehe `Sharely_programm/backend/README.md`); fehlt etwas, sagt das Skript, was. Die einzelnen Schritte darunter funktionieren weiterhin.

1. MongoDB und Backend starten (siehe `Sharely_programm/backend/README.md`).
2. In einem zweiten Terminal den Seiten-Server auf Port 5173 starten:

   ```bash
   cd Sharely_programm
   python seiten_server.py
   ```

   Er arbeitet wie `python -m http.server 5173 --bind 127.0.0.1` (nur auf dem eigenen Rechner erreichbar), sagt dem Browser aber, dass er bei jeder Datei nachfragen soll, ob sie sich geändert hat. Mit `http.server` lief nach einem `git pull` sonst oft noch die alte `gemeinsam.js` aus dem Browser-Zwischenspeicher (14.10. und 27.10.2026).

   Das Backend erlaubt Zugriffe nur von dieser Adresse (CORS, `FRONTEND_URLS` in `.env`).

3. Im Browser öffnen: http://localhost:5173/ (leitet zur Anmeldung weiter) oder direkt http://localhost:5173/frontend/templates/. `localhost` verwenden, nicht `127.0.0.1`, sonst klappt die Anmeldung nicht. Sieht eine Seite trotzdem nach einem alten Stand aus: **Strg+F5**.

Direktes Öffnen per Doppelklick (`file://…`) funktioniert nicht, weil der Browser die Anfragen ans Backend dann blockiert.
