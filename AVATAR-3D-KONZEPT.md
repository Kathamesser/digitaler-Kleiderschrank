# 3D-Avatar-Baukasten — Umsetzungskonzept

Vertiefung zu Phase 3 der [ROADMAP.md](./ROADMAP.md). Ersetzt das frühere KI-AVATAR-KONZEPT.md (fotobasierte KI-Generierung — Idee verworfen zugunsten einer anpassbaren 3D-Spielfigur). Reine Planungsgrundlage, noch kein Code. Stand der Recherche: Juli 2026.

## Ziel

Eine Sims-artige 3D-Spielfigur, die der Nutzer von allen Seiten betrachten (drehen/zoomen) und so anpassen kann, dass sie ihm möglichst ähnlich sieht:

- **Aussehen:** Größe, Körperbau (dünn/dick/muskulös), Hautfarbe, Haarfarbe, Frisur, Augenfarbe, mehrere Gesichtsmodelle
- **Körpermaße:** Schultern, Taille, Beine, Brust — nicht nur fürs Aussehen, sondern als Datengrundlage für das spätere Kleidungs-Fitting („passt/passt nicht" und wie es sitzt)

## Das Grundprinzip: Werkstatt und Schaufenster

Die wichtigste Einordnung vorweg, weil sie beim ersten Kontakt mit MakeHuman regelmäßig für Verwirrung sorgt: **MakeHuman ist nicht das Tool für eure Nutzer — es ist euer Entwickler-Werkzeug, um den „Rohling" zu bauen.** Eure Nutzer sehen MakeHuman nie. Sie sehen euren eigenen Charaktereditor in der Web-App, der diesen Rohling lädt und interaktiv macht.

Als Bild: MakeHuman ist die **Werkstatt**, in der ihr einmal eine Gliederpuppe mit allen Gelenken und Verstellschrauben baut. Eure App ist das **Schaufenster**, in dem jeder Nutzer an genau dieser Puppe selbst drehen darf. Die Sims machen es intern genauso — deren Charaktereditor ist auch nur eine Regler-Oberfläche über einem vorgefertigten Modell mit eingebauten Verformungen.

## Die Asset-Pipeline im Detail

### Stufe 1 — Einmalig, bei euch: den Rohling bauen (MakeHuman/Blender)

Ihr erstellt keine konkrete Person, sondern eine **neutrale Basis-Figur**, in die alle Verformungsmöglichkeiten als **Morph Targets** (auch Blend Shapes genannt) eingebacken werden. Ein Morph Target ist eine im Modell gespeicherte Extremform: Für jedes Target merkt sich die Datei, wohin sich jeder Punkt der Körperoberfläche bewegt, wenn das Merkmal voll ausgeprägt ist. Für eure Anforderungen heißt das konkret:

| Anforderung | Umsetzung im Rohling |
|---|---|
| Größe | Morph Target „groß ↔ klein" (oder Skalierung + Proportions-Target) |
| Körperbau dünn/dick | Morph Target „Gewicht" |
| Körperbau muskulös | Morph Target „Muskelmasse" |
| Schultern, Taille, Beine, Brust | je ein eigenes Morph Target pro Maß |
| Gesichtsmodelle | mehrere Gesichts-Morphs oder austauschbare Kopf-Varianten |
| Frisuren | separate Meshes (kein Morphing), 6–8 Presets |
| Haut-, Haar-, Augenfarbe | keine Geometrie — reine Farbwerte am Material |

Die Regler, die ihr in MakeHuman seht (Gewicht, Muskeln, Proportionen …), sind genau die Kandidaten dafür: **Ihr entscheidet, welche dieser Regler ihr als Morph Targets in den Export mitnehmt** — das wird der Funktionsumfang eures Editors. Export als eine **GLB-Datei** (das Standard-3D-Format fürs Web; unterstützt Morph Targets, Skelett und Materialien). Erfahrungsgemäß braucht dieser Schritt einen Zwischenstopp in Blender (mit dem MPFB-2-Plugin), um die Targets zu prüfen, zu benennen und den Export sauber einzustellen.

**Ergebnis der Stufe 1:** eine einzige Datei, z. B. `avatar-base.glb`, die im Projekt liegt wie ein Bild oder eine Schriftart — sie ist Teil eurer App, nicht der Nutzerdaten.

### Stufe 2 — In der App: der Charaktereditor macht den Rohling interaktiv

Three.js lädt die GLB-Datei und stellt jedes eingebaute Morph Target als Zahl zwischen 0 und 1 zur Verfügung. Euer Editor ist dann im Kern eine simple Abbildung: **ein Schieberegler im UI = ein Morph Target im Modell.** Zieht der Nutzer „Schulterbreite" auf 70 %, setzt euer Code den Wert auf 0,7 und die Figur verformt sich live in der 3D-Ansicht — flüssig, ohne Server-Anfrage, denn die Verformung rechnet die Grafikkarte des Nutzers.

- **Maße-Regler:** Morph-Target-Werte setzen (Schultern, Taille, Beine, Brust, Gewicht, Muskeln, Größe)
- **Farben:** Farbwert des jeweiligen Materials ändern (Haut, Haare, Augen) — technisch der einfachste Teil
- **Frisur/Gesicht wechseln:** das jeweilige Teil-Mesh ein-/ausblenden
- **Rundum-Ansicht:** Kamera-Steuerung (Orbit) für Drehen und Zoomen — Standardbaustein in Three.js

### Stufe 3 — Gespeichert wird die Reglerstellung, nicht das Modell

Pro Nutzer landet in der Datenbank nur ein kleiner Konfigurations-Datensatz, sinngemäß: „Schultern 0,7 · Taille 0,4 · Gewicht 0,55 · Frisur Nr. 3 · Hautfarbe #C68863 · Gesicht Nr. 2". Beim nächsten Login lädt die App denselben Rohling und stellt die Regler wieder ein. Das hat drei angenehme Folgen:

1. **Winzig und schnell:** kein 3D-Modell pro Nutzer speichern, nur ein paar Zahlen.
2. **Fitting-Grundlage:** genau dieser Datensatz (auf cm-Bereiche gemappt) ist später der Input für den Kleidungs-Abgleich — Avatar-Aussehen und Passform-Logik speisen sich aus derselben Quelle.
3. **Saubere Trennung für die Doku:** Asset (Rohling, Teil der App) vs. Nutzerdaten (Reglerstellung, personenbezogen, in eurer DB) — das lässt sich im Datenschutzkonzept klar auseinanderhalten.

## Technologie-Entscheidung: Womit anzeigen?

| Option | Was es ist | Bewertung fürs Projekt |
|---|---|---|
| **Three.js** (Empfehlung) | JavaScript-3D-Bibliothek für den Browser | Läuft direkt in der Web-App, kein Plugin/Installation, riesige Community, volle Unterstützung für glTF-Morph-Targets. Passt am besten, wenn StyleHUB eine Web-Anwendung wird. |
| Babylon.js | Ebenfalls JavaScript-3D für den Browser | Gleichwertig fähig, etwas „Framework-artiger". Geschmacksfrage — nur eine von beiden wählen. |
| Unity (WebGL-Export oder App) | Spiele-Engine | Mächtiger Charaktereditor möglich, aber eigene Entwicklungsumgebung, C# statt Web-Stack, klobiger WebGL-Export, Lizenzthema. Nur sinnvoll, falls ihr sowieso eine native App bauen wollt. |

**Empfehlung:** Web-App mit Three.js. Dann ist der Avatar-Viewer einfach eine Komponente in derselben Anwendung wie Kleiderschrank und Outfit-Builder — keine Brüche im Stack, und alle drei Teammitglieder bleiben in einer Sprache (JavaScript/TypeScript).

## Woher kommt das 3D-Modell? (der kritische Teil)

Das ist der Engpass des Features — hier die realistischen Quellen:

### Empfohlener Weg: MakeHuman / MPFB 2
- [MakeHuman](https://static.makehumancommunity.org/makehuman.html) ist ein Open-Source-Programm genau für diesen Zweck: Es erzeugt menschliche 3D-Modelle über Regler für Geschlecht, Alter, Gewicht, Muskeln, Proportionen — also genau eure Anpassungslogik, nur als Desktop-Werkzeug.
- Die exportierten Modelle stehen unter **CC0-Lizenz** (frei nutzbar, auch kommerziell, keine Namensnennung nötig) — für ein Prüfungsprojekt ideal und rechtlich sauber dokumentierbar.
- [MPFB 2](https://www.cgchannel.com/2025/03/check-out-open-source-blender-character-generation-plugin-mpfb-2/) ist die modernere Variante als Blender-Plugin und exportiert direkt nach glTF.
- **Workflow:** In MakeHuman/Blender ein Basis-Modell bauen, die benötigten Morph Targets (Schultern, Taille, Beine, Brust, Körperbau, Größe) als Blend Shapes hineinbacken, als GLB exportieren → im Browser lädt Three.js das Modell und legt Regler auf die Targets. Einmaliger Asset-Aufwand, danach reine Programmierarbeit.

### Ergänzende Quellen
- **Frisuren/Zubehör:** MakeHuman bringt Basis-Frisuren mit; zusätzliche Assets über Sketchfab o. Ä. (Lizenz je Asset prüfen und dokumentieren!).
- [CharacterStudio](https://github.com/M3-org/CharacterStudio) — offene Web-Avatar-Plattform auf Three.js-Basis; als Inspiration und Code-Referenz nützlich.
- **Mixamo** (Adobe, kostenlos): automatisches Rigging und Animationen, falls der Avatar später mal posieren soll — fürs Pflichtprogramm nicht nötig, nettes Stretch-Goal.

### Warnung aus der Recherche
**Ready Player Me** — bis vor Kurzem die bekannteste „fertige" Avatar-Plattform — wurde nach der Netflix-Übernahme **zum 31.01.2026 abgeschaltet**. Das ist eine wichtige Lehre für eure Anbieterwahl im ganzen Projekt: Nicht auf proprietäre Plattformen bauen, die verschwinden können. Der MakeHuman-Weg hat dieses Risiko nicht — die Assets liegen als Dateien bei euch.

## Körpermaße & Kleidungs-Fitting

Die Maße-Regler haben eine Doppelrolle, deshalb vorab im Team klären:

- **Einheit festlegen:** echte Zentimeter (präziser Abgleich mit Größentabellen der Shops, aber Nutzer müssen sich vermessen) oder normierte Regler 0–100 mit hinterlegter cm-Spanne (bequemer, etwas ungenauer). **Empfehlung:** Regler im UI, intern aber auf cm-Bereiche gemappt — dann geht beides.
- **Fitting-Logik:** Kleidungsstück hat Größenangabe (aus Phase 5 per KI extrahiert) → Größentabelle ordnet der Größe cm-Bereiche zu (Brustumfang, Taillenumfang, …) → Abgleich mit den Avatar-Maßen ergibt „passt / eng / weit". Das ist klassische Programmlogik ohne KI und eignet sich hervorragend als dokumentierbare Eigenleistung für die Prüfung.
- **Darstellung am Avatar:** Kleidungs-Vorlagen (T-Shirt, Hose, Jacke, …) werden über dieselben Morph-Werte mitskaliert, damit die Kleidung der Körperform folgt.

## Datenschutz-Hinweis

Auch ohne Foto: Körpermaße plus Aussehensmerkmale sind personenbezogene Daten. Sie bleiben aber **in eurer eigenen Datenbank** statt bei einem KI-Anbieter — das ist die größte Vereinfachung gegenüber dem alten Konzept und gehört so begründet in die Projektdokumentation.

## Aufwands- und Risiko-Einschätzung

| Baustein | Aufwand | Risiko |
|---|---|---|
| 3D-Viewer (laden, drehen, zoomen, Licht) | gering | gering — Standardaufgabe in Three.js |
| Regler auf Morph Targets, Farbwechsel | mittel | gering — sobald das Modell die Targets hat |
| Basis-Modell mit allen Morph Targets erstellen | mittel bis hoch | **hoch — hier entscheidet sich das Feature.** Einarbeitung in MakeHuman/Blender nötig; früh prototypen! |
| Frisuren-/Gesichts-Preset-Bibliothek | mittel | mittel — Fleißarbeit + Lizenzprüfung je Asset |
| Kleidungs-Vorlagen (3D) je Kategorie | mittel bis hoch | mittel — bewusst auf wenige Kategorien begrenzen |
| Fitting-Logik (Maße-Abgleich) | mittel | gering — reine Programmlogik |

## Was ich beitragen kann

**Jetzt (Planung):** Prototyp-Plan detaillieren, Pflichtenheft-Textbausteine, Datenmodell für Avatar-Konfiguration und Größentabellen entwerfen.

**Später (Umsetzung):** Den kompletten Code-Anteil — Three.js-Viewer, Regler-/Morph-Target-Steuerung, Farbsystem, Preset-Verwaltung, Speichern/Laden der Konfiguration, Fitting-Logik, API dahinter. Auch beim Blender/MakeHuman-Export kann ich Schritt-für-Schritt anleiten und Exportprobleme mit debuggen.

**Was bei euch liegt:** Die künstlerische Arbeit am Modell selbst (Regler in MakeHuman einstellen, Presets aussuchen, Ästhetik beurteilen) und die Lizenz-Dokumentation der verwendeten Assets.

## Nächste konkrete Schritte (noch kein Code)

1. Entscheidung Web-App ja/nein → damit steht auch Three.js vs. Unity.
2. MakeHuman herunterladen und eine Stunde herumspielen — ihr seht sofort, ob die Regler-Qualität euren Ansprüchen genügt.
3. Einheiten-Frage für Körpermaße im Team entscheiden (Empfehlung: Regler mit cm-Mapping).
4. Liste der Kleidungs-Kategorien festlegen, die als 3D-Vorlage existieren sollen (Empfehlung: mit 5–6 starten).
5. Danach der Phase-1-Prototyp: ein MakeHuman-Export mit 2–3 Morph Targets, in Three.js geladen und drehbar — das ist der Punkt, an dem ich das erste Mal Code beisteuern würde.
