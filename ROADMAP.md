# StyleHUB — Digitaler Kleiderschrank

Projektfahrplan für die Abschlussprüfung. Arbeitstitel **StyleHUB** (Name kann sich noch ändern).

**Team:** 3 Personen · **Zeitraum:** 26 Wochen (~6 Monate) · **Stand:** 12.07.2026

## Kurzbeschreibung

Kleidung digital erfassen, zu Outfits kombinieren, neue Teile per KI aus Online-Angeboten übernehmen — und sich über eine frei anpassbare 3D-Spielfigur ansehen, wie die ausgewählten Klamotten wirken.

*Änderung gegenüber der ersten Fassung: Statt eines KI-generierten Fotos aus eigenen Bildern nutzt der Avatar jetzt ein Sims-artiges, von Hand anpassbares 3D-Charaktermodell — Details im [AVATAR-3D-KONZEPT.md](./AVATAR-3D-KONZEPT.md). Das senkt Datenschutz- und Kostenrisiko deutlich, verlagert den Aufwand aber in ein eigenes 3D-Grafik-Thema.*

## Die vier Säulen

1. **Kleiderschrank** — Klamotten bildlich erfassen, kategorisieren und durchsuchen.
2. **Outfit-Kombinatorik** — Einzelne Teile zu vollständigen Outfits zusammenstellen und speichern.
3. **KI-Produktimport** — Aus Produktlink oder Beschreibung automatisch Bild und Daten übernehmen, als Wunschartikel markiert.
4. **Avatar-Baukasten (Kernfeature)** — Sims-artige 3D-Spielfigur mit umfangreichen Anpassungsmöglichkeiten, um eine große Ähnlichkeit zum Nutzer zu erreichen; trägt die ausgewählten Klamotten und lässt sich von allen Seiten betrachten.

## Anforderungen an den Avatar (Vorgabe aus dem Team)

- 3D-Modell, von allen Seiten betrachtbar (Rotation/Zoom)
- Anpassbar: Größe, Körperbau (dünn/dick/muskulös), Hautfarbe, Haarfarbe, Frisur, Augenfarbe, mehrere Gesichtsmodelle
- Anpassbare Körpermaße: Schultern, Taille, Beine, Brust
- Die Körpermaße dienen nicht nur dem Aussehen, sondern später auch dazu, zu bestimmen, ob ein Kleidungsstück passt und wie es entsprechend sitzt

## Tech-Stack (Team-Entscheidung vom 12.07.2026)

| Ebene | Wahl | Begründung |
|---|---|---|
| Backend | **Python** (Empfehlung: FastAPI als Framework) | Größte vorhandene Teamerfahrung; bestes Ökosystem für den KI-Produktimport (Scraping, KI-APIs); ein halbes Jahr ist zu kurz, um nebenbei eine neue Sprache auf Produktionsniveau zu lernen |
| Datenbank | **MongoDB** | Im Team bereits bekannt; die Avatar-Konfiguration und Kleidungsstücke mit variablen Attributen passen gut zum Dokumentenmodell |
| Frontend | JavaScript/TypeScript mit **Three.js** für den 3D-Avatar | Three.js läuft im Browser — die Backend-Sprache hat darauf keinen Einfluss; der Avatar-Editor ist zwingend JavaScript |
| Entwicklungsumgebung | VS Code | Standardwahl für Python + Web |

*Bewusste Konsequenz: zwei Sprachen im Projekt (Python im Backend, JavaScript im Frontend). Das ist normal für Webprojekte und macht die Arbeitsteilung sauber — Backend-Arbeit denkt in Python, Editor-Arbeit in JavaScript. Noch offen: Wahl des KI-Anbieters für den Produktimport (Phase 0/1) und endgültig Frontend-Framework (z. B. React oder Vue) fürs UI drumherum.*

## Empfehlungen vor dem Start

- **Risiko zuerst testen:** Das 3D-Charaktersystem (Rig, Regler, Blend Shapes) ist jetzt der technisch unsicherste Teil und für die meisten Teams in diesem Bereich Neuland. Schon in Phase 1 einen kleinen Machbarkeits-Prototyp bauen (ein Testmodell, zwei bis drei Regler, drehbar), statt das Risiko bis zur Mitte des Projekts aufzuschieben.
- **Kleidungs-Fitting-Ansatz früh festlegen:** Realistischerweise könnt ihr nicht jedes fotografierte Kleidungsstück einzeln 1:1 als 3D-Modell nachbauen. Empfehlung: jedes Kleidungsstück wird einer von mehreren vorgefertigten 3D-Kategorien zugeordnet (T-Shirt, Hose, Jacke, Kleid, Schuhe, …), die anhand der Körpermaße skaliert und mit Farbe/Muster aus dem Produktfoto eingefärbt wird. Das ist ein zentraler Designentscheid mit Auswirkung auf mehrere Phasen — als Team gemeinsam absegnen, bevor Phase 3/4 beginnen.
- **Umfang bei Frisuren/Gesichtern bewusst begrenzen:** Lieber 6–8 gut gemachte Presets pro Kategorie als ein offenes, frei generierbares System — sonst sprengt allein dieser Teil den Zeitrahmen.
- **Rollen grob aufteilen, nicht zementieren:** z. B. eine Person mit Schwerpunkt Backend & API, eine mit Schwerpunkt 3D/Frontend, eine mit Schwerpunkt Datenmodell, KI-Produktimport & Dokumentation. Alle drei bleiben an jeder Phase beteiligt.

## Meilenstein-Fahrplan

### Phase 0 · Woche 1–3 — Analyse & Konzept
Grundlage schaffen, bevor eine Zeile Code entsteht.
- Lasten-/Pflichtenheft mit Abnahmekriterien
- User Stories für alle vier Kernfunktionen
- Grobes Datenmodell (Nutzer, Kleidungsstück, Outfit, Wunschartikel, Avatar-Konfiguration)
- Tech-Stack-Entscheidung — Backend (Python), Datenbank (MongoDB) und 3D (Three.js) sind bereits entschieden (siehe oben); noch offen: Frontend-Framework und KI-Anbieter für den Produktimport

### Phase 1 · Woche 4–6 — Architektur, API & Design
Schnittstellen und Oberflächen festlegen, an denen alle drei parallel arbeiten können.
- API-Spezifikation (Kleidungsstücke, Outfits, Produktimport, Avatar-Konfiguration)
- Finales Datenbankschema — bei MongoDB: Struktur der Collections/Dokumente (Nutzer, Kleidungsstück, Outfit, Avatar-Konfiguration), inkl. Körpermaße und Kleidungs-Kategorien
- Klickbare Wireframes für die vier Kernbereiche
- Repository, Branching-Modell, CI/CD-Grundgerüst
- 3D-Technologie ist mit Three.js entschieden — hier nur noch: Projektaufbau festlegen (wie Frontend, Three.js-Viewer und FastAPI-Backend zusammenspielen)
- Grundsatzentscheidung zum Kleidungs-Fitting-Ansatz (Kategorie-Vorlagen statt 1:1-Rekonstruktion) im Team absegnen
- Machbarkeits-Prototyp: einfaches 3D-Testmodell mit 2–3 Reglern drehbar darstellen

### Phase 2 · Woche 7–10 — Kleiderschrank-Kernfunktion
Der digitale Kleiderschrank als erstes lauffähiges Modul.
- Registrierung/Login, Nutzerprofile
- Bild-Upload inkl. Speicherung (Objektspeicher/Cloud)
- Verwaltung von Kleidungsstücken (Kategorie, Farbe, Material, Tags)
- Erste Frontend-Ansicht: Kleiderschrank durchblättern

### Phase 3 · Woche 11–16 — Avatar-Grundgerüst (Kernfeature, höchstes Risiko)
Die Sims-artige 3D-Spielfigur als eigenständiges Modul.
- Basis-3D-Humanoid mit Rig und Blend Shapes (Morph Targets)
- Regler für Größe, Körperbau (dünn/muskulös/kräftig) und Körpermaße (Schultern, Taille, Beine, Brust)
- Auswahl für Hautfarbe, Haarfarbe, Augenfarbe
- Bibliothek an Frisuren und Gesichtsmodellen (begrenzte, kuratierte Presets)
- 360°-Viewer zum Drehen/Zoomen des Avatars in der UI
- Speichern der Avatar-Konfiguration je Nutzer

### Phase 4 · Woche 17–19 — Outfit-Kombinatorik & Kleidungs-Fitting
Aus einzelnen Teilen werden anziehbare, passende Outfits am Avatar.
- Zuordnung jedes Kleidungsstücks zu einer 3D-Kleidungs-Kategorie/-Vorlage
- Skalierung der Kleidungs-Vorlage anhand der Körpermaße des Avatars
- Einfärben/Texturieren der Vorlage anhand des Produktfotos
- Logik zum Kombinieren mehrerer Kleidungsstücke zu einem Outfit am Avatar
- „Passt/passt nicht"-Bewertung anhand Maße-Abgleich zwischen Avatar und Kleidungsstück
- Speichern/Bearbeiten/Löschen von Outfits, Filter- und Suchfunktion

### Phase 5 · Woche 20–22 — KI-Produktimport & Wunschliste
Externe Artikel per Link oder Beschreibung automatisiert übernehmen.
- Eingabemaske für Produktlink oder Freitext-Beschreibung
- Scraping/Parsing der Produktseite bzw. Text-Interpretation
- KI-gestützte Extraktion von Bild, Titel, Preis, Marke, Kategorie und — neu wichtig fürs Fitting — Größenangabe/Maßtabelle
- Wunschliste als eigener Bereich im Kleiderschrank
- Fehlerbehandlung, wenn ein Artikel nicht erkannt wird oder keine Größenangabe vorliegt

### Phase 6 · Woche 23–24 — Integration & Feinschliff
Alle Module laufen als ein System zusammen.
- Zusammenführung aller Module in einer Anwendung
- Ende-zu-Ende-Tests entlang der Kern-Nutzerpfade
- Bugfixing und Oberflächen-Feinschliff
- Performance-Optimierung (3D-Ladezeiten, Asset-Größen, Bildgrößen)

### Phase 7 · Woche 25–26 — Test, Dokumentation & Abgabe
Prüfungsreife herstellen.
- Testkonzept und -durchführung (fachlich und technisch)
- Projekt- und technische Dokumentation für die Prüfung
- Vorbereitung von Präsentation/Kolloquium inkl. Live-Demo
- Deployment der Demo-Umgebung

## Läuft die ganze Zeit mit

- **Datenschutz:** Auch ohne eigenes Foto sind Körpermaße und Aussehensmerkmale personenbezogene Daten — von Phase 0 an sauber im Datenmodell und in der Doku behandeln, nicht erst vor der Abgabe.
- **Laufende Dokumentation:** Entscheidungen direkt beim Treffen begründen und festhalten, statt sie am Ende aus dem Gedächtnis zu rekonstruieren.
- **Team-Sync:** Kurzer wöchentlicher Abgleich zu dritt, damit Abhängigkeiten zwischen den Modulen früh sichtbar werden.
