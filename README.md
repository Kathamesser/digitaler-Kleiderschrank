
Sharely — Digitaler Kleiderschrank
Sharely-Logo

Sharely („style and share“) ist ein digitaler Kleiderschrank als Web-App. Man fotografiert seine Kleidung, ordnet sie ein und stellt daraus Outfits zusammen. Teile lassen sich mit Freunden teilen, verleihen oder verschenken, und Wunschartikel aus Online-Shops kommen per KI in den Schrank. Das Herzstück ist ein frei anpassbarer 3D-Avatar, der die ausgewählte Kleidung trägt und zeigt, ob sie passt.

Abschlussprüfungsprojekt, 3-Personen-Team, Projektzeitraum Juli 2026 bis Januar 2027.

Team
Name	Schwerpunkte
Katharina Lutzky (Katha)	Repo-Inhaberin, User Storys, Wireframes, Projektgerüst, Kleidung erfassen, Registrierung und Login, Seiten der Web-App
Manuel Herrmann (Manu)	Datenmodell (ERM), MongoDB-Struktur mit Prüfregeln und Indizes
Christian Maschke (Chris)	Roadmap und Avatar-Konzept, 3D-Avatar-Pipeline (MakeHuman → Blender → GLB), Passform-Messung, Desktop-Mockups, Team-Organisation
Alleinstellungsmerkmale
3D-Avatar statt Foto: Jeder baut sich eine eigene Spielfigur und passt Körperform, Größe und Proportionen mit Reglern an. Es werden keine echten Fotos der Person gebraucht, das schützt die Privatsphäre.
Passform-Check: Der Avatar wird an 22 Messpunkten in Zentimetern vermessen. Die Maße eines Kleidungsstücks werden an denselben Stellen erfasst, so zeigt die App „passt“, „eng“ oder „weit“, ohne Größentabellen der Hersteller.
Teilen unter Freunden: Freunde sehen den Schrank (außer privaten Teilen), können sich Kleidung ausleihen oder geschenkt bekommen. Der Verleih wird mit Verlauf festgehalten.
Wunschartikel per KI: Ein Link oder eine Beschreibung eines Online-Angebots genügt, Bild und Daten landen als Wunschartikel im Schrank.
Datenschutz von Anfang an: Körpermaße gelten als personenbezogene Daten. Gespeichert werden nur die Reglerwerte der Figur, private Teile und Outfits sieht nie jemand anderes.
Technik
Python mit FastAPI im Backend (modularer Monolith), MongoDB als Datenbank, JavaScript mit Three.js für den 3D-Avatar im Browser. Der Avatar entsteht aus einem MakeHuman-Modell, das in Blender zu einer GLB-Datei mit Morph Targets aufbereitet wird.

Starten
cd Sharely_programm
python start.py
start.py ist der einzige Einstiegspunkt: Es startet das Backend (Port 8000) und den Seiten-Server (Port 5173) und öffnet den Browser. Strg+C beendet alles. Die einmalige Einrichtung (Pakete, .env, Datenbank) steht in Sharely_programm/backend/README.md. Die App unter http://localhost:5173 öffnen, nicht unter 127.0.0.1.

Projektstruktur
README.md                   diese Datei
BRAIN.md                    gemeinsames Team-Gedächtnis: Stand, offene Entscheidungen, Log
CLAUDE.md                   Projektkontext für die Claude-Sitzungen
Sharely_programm/           alles, was die App zum Laufen braucht
  start.py                  startet alle Dienste mit einem Befehl
  seiten_server.py          liefert die Seiten aus (Port 5173)
  backend/                  FastAPI-Backend
    app/core/               Einstellungen, Datenbank, Sicherheit, feste Wertelisten
    app/module/             ein Ordner je Fachbereich (router → service → repository):
                            kleidung, outfits, nutzer, freunde, verleihen,
                            figuren, passform, produktimport
    app/datenbank_einrichten.py   legt Collections, Prüfregeln und Indizes an
    tests/                  Tests mit pytest
  frontend/                 Web-App im Browser
    templates/              die Seiten (HTML), Start: index.html (Anmeldung)
    static/css/             Aussehen (stil.css)
    static/js/              gemeinsame Bausteine und Beispieldaten
    src/avatar-editor/      3D-Avatar-Editor mit Three.js
  assets/
    avatar/                 Avatar als GLB plus Werkstatt-Dateien zum Neubauen
    branding/               Logo
  uploads/                  hochgeladene Bilder, nur lokal, nicht im Repo
docs/                       Dokumentation
  PROJEKTDOKUMENTATION.md   Verlauf, Entscheidungen, Soll-Ist-Vergleich
  planung/                  Roadmap, Avatar-Konzept, User Storys
  konzeption/               Technische Konzeption (PDF mit Wireframes)
  mockups/desktop/          Desktop-Mockups aller Seiten
  datenmodell/              ERM und Abbildung auf MongoDB
  api/                      Absprachen zur REST-API
  avatar/                   Regler, Pipeline, Figurtypen, Zentimeter-Messung, Skripte
Wichtige Dokumente
docs/PROJEKTDOKUMENTATION.md: Projektdokumentation
docs/planung/ROADMAP.md: Meilensteinplan und Tech-Stack-Entscheidung
docs/planung/AVATAR-3D-KONZEPT.md: Konzept des 3D-Avatars
docs/planung/Userstory.md: User Storys
docs/datenmodell/ERM-SHARELY.md: Datenmodell
BRAIN.md: aktueller Stand und Team-Log
