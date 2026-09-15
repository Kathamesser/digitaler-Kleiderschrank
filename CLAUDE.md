# StyleHUB — Digitaler Kleiderschrank

Abschlussprüfungsprojekt, 3-Personen-Team, 26 Wochen (bis ca. Januar 2027). Arbeitstitel StyleHUB, Repo-Name „digitaler-Kleiderschrank".

## Was die App tut

Kleidung bildlich erfassen und kategorisieren, zu Outfits kombinieren, Wunschartikel per KI aus Online-Angeboten importieren (Link oder Beschreibung → Bild + Daten), und als Kernfeature: ein Sims-artiger, frei anpassbarer 3D-Avatar, der die ausgewählten Klamotten trägt. Die Körpermaße des Avatars (Schultern, Taille, Beine, Brust) dienen auch der Passform-Bewertung („passt/eng/weit") gegen Größentabellen.

## Zentrale Dokumente (im Repo)

- `BRAIN.md` — **gemeinsames Team-Gedächtnis, zuerst lesen:** aktueller Stand, offene Entscheidungen, wer woran arbeitet, Sitzungskennungen, Log. Nach **jeder** Aktion für das Projekt dort einen Log-Eintrag mit Datum und Sitzungskennung ergänzen und die betroffenen Abschnitte aktualisieren.
- `ROADMAP.md` — Meilensteinplan mit 8 Phasen, Tech-Stack-Entscheidung und Empfehlungen
- `AVATAR-3D-KONZEPT.md` — Umsetzungskonzept 3D-Avatar: MakeHuman-Asset-Pipeline („Werkstatt/Schaufenster"-Prinzip), Three.js-Editor, Fitting-Logik
- `roadmap.html` — visuelle Version der Roadmap (im Browser öffnen)

Bei Architektur- oder Feature-Entscheidungen zuerst dort nachsehen; Änderungen an Entscheidungen auch dort nachziehen.

## Tech-Stack (entschieden 12.07.2026)

- **Backend:** Python (Zielbild: FastAPI)
- **Datenbank:** MongoDB
- **Frontend:** JavaScript mit Three.js für den 3D-Avatar-Editor
- Noch offen: Frontend-Framework (React/Vue), KI-Anbieter für den Produktimport

Hinweis: Der aktuelle Code im Repo (Flask-artige Webapp mit Server-Templates) ist ein Experimentierstand aus der Claude-Pro-Testphase des Teams und entspricht noch nicht dem Zielbild — vor größeren Umbauten im Team klären, was übernommen wird.

## Arbeitsweise & Konventionen

- **GitHub ist die zentrale Quelle.** Lokale Arbeitskopien werden manuell über GitHub abgeglichen. Christians Obsidian-Vault (`OneDrive\AI_Unibrain\Obsidian_Vault\StyleHUB`) ist ein Clone dieses Repos und wird von Claude Code synchron gehalten.
- Dokumentation auf Deutsch, Commit-Messages auf Englisch oder Deutsch — Hauptsache aussagekräftig.
- Entscheidungen mit Datum und Begründung in den Docs festhalten (prüfungsrelevant).
- Maschinen-spezifische Claude-Permissions gehören in `.claude/settings.local.json` (nicht committen), nicht in die geteilte `.claude/settings.json`.

## Für Claude wichtig

- **Zu Beginn jeder Sitzung:** aktuellen Stand von `main` holen (`git pull`), dann `BRAIN.md` komplett lesen und deine Sitzungskennung (`Mensch/KI(Gerät.Anwendung)`) nach dem Abschnitt „🪪 Deine Sitzungskennung" bestimmen — nicht raten, im Zweifel deinen Menschen fragen.
- **Protokollpflicht:** Jede Aktion für das Projekt (Code, Doku, Entscheidungen, Recherchen, Setup) kommt mit Datum und Sitzungskennung ins Log von `BRAIN.md`, danach committen und nach `main` bringen. Details: Abschnitt „📌 Protokollpflicht für alle KI-Sitzungen" in `BRAIN.md`.
- **Nur eine BRAIN.md:** Gültig ist ausschließlich die Fassung auf `main`. Arbeitest du auf einem eigenen Branch (z. B. Claude Code im Browser: `claude/…`), führst du deine `BRAIN.md`-Änderungen noch in derselben Sitzung nach `main` zusammen (Merge oder Pull Request); geht das nicht, bittest du deinen Menschen darum. Bei Konflikten beide Stände übernehmen, nie fremde Einträge überschreiben.
- Projektphase beachten: Solange die Planung läuft, keine ungefragten Code-Umbauten — erst fragen, was übernommen werden soll.
- Datenschutz ist prüfungsrelevantes Querschnittsthema: Körpermaße/Aussehen sind personenbezogene Daten; keine echten Nutzerfotos nötig (bewusste Design-Entscheidung gegen Foto-Avatare).
- Der 3D-Avatar ist das Alleinstellungsmerkmal und höchste Risiko — Machbarkeits-Prototyp hat Vorrang vor Feinschliff anderswo.
