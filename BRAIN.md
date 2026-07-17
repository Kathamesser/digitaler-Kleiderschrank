# BRAIN — Gemeinsames Team-Gedächtnis

Lebendes Dokument für alles, was zwischen den Sessions und Teammitgliedern nicht verloren gehen soll. Wird von Menschen **und** von Claude gepflegt.

**Regeln für alle (Menschen wie Claudes):**
- Vor der Arbeit lesen, nach der Arbeit relevante Änderungen eintragen — mit Datum und Namen.
- Einträge kurz halten; Details gehören in die Fachdokumente (ROADMAP.md, AVATAR-3D-KONZEPT.md), hier stehen Stand, Entscheidungen und Übergaben.
- Erledigtes aus „Offene Fragen" und „Nächste Schritte" entfernen statt anzusammeln — das Log unten ist das Archiv.
- Über Git synchronisieren: vor dem Lesen pullen, nach dem Eintragen committen und pushen.

---

## 👋 An die anderen Claudes

Hallo Kollegen! Hier schreibt Christians Claude-Code-Session (17.07.2026). Schön, dass ihr da seid — ab jetzt arbeiten wir zu mehreren an diesem Projekt, und diese Datei ist unser gemeinsames Gedächtnis.

Kurz zur Orientierung, bevor ihr loslegt: Die Planungsphase ist weitgehend abgeschlossen — Roadmap und Avatar-Konzept liegen im Repo und sind mit dem Team abgestimmt. Bitte lest `CLAUDE.md` und die dort verlinkten Dokumente, bevor ihr größere Vorschläge macht; einige naheliegende Ideen (KI-Foto-Avatar, Unity, eigenes VTON-Modell hosten) wurden bereits bewusst verworfen, die Begründungen stehen in `AVATAR-3D-KONZEPT.md`. Der Flask-Code im Repo ist ein Experimentierstand aus der Testphase, nicht die Zielarchitektur — bitte nicht ungefragt umbauen, das Team entscheidet noch, was davon übernommen wird (siehe offene Fragen unten).

Was ihr für eure Menschen tun könnt: die offenen Entscheidungen unten vorantreiben, Einträge in „Wer macht gerade was" aktuell halten, und Erkenntnisse in den Wissensspeicher schreiben, statt sie in euren Sessions versickern zu lassen. Und tragt euch nach getaner Arbeit ins Log ein — Datum und Name eures Menschen genügt.

Gute Zusammenarbeit! 🤝

*(Diesen Abschnitt gerne löschen, sobald alle drei Claudes einmal hier waren — dann hat er seinen Zweck erfüllt.)*

## Aktueller Stand (Kurzfassung)

- Projektphase: Planung abgeschlossen bis auf offene Punkte unten; Team experimentiert parallel mit Claude Pro und einem ersten Code-Stand (Flask-artige Webapp — gilt als Experimentierstand, nicht als Zielarchitektur).
- Tech-Stack entschieden: Python-Backend (Zielbild FastAPI), MongoDB, JavaScript/Three.js-Frontend. Details und Begründung: ROADMAP.md.
- Avatar-Ansatz entschieden: anpassbare 3D-Spielfigur (MakeHuman-Rohling + Three.js-Editor) statt KI-Foto-Generierung. Details: AVATAR-3D-KONZEPT.md.
- KI-Infrastruktur: GitHub = zentrale Quelle; Christians Obsidian-Vault ist ein synchronisierter Clone; CLAUDE.md gibt allen Claude-Sessions den Projektkontext.

## Offene Fragen / anstehende Entscheidungen

- [ ] Frontend-Framework wählen (React oder Vue) — betrifft Phase 1
- [ ] KI-Anbieter für den Produktimport wählen — betrifft Phase 5
- [ ] Körpermaße: Regler mit internem cm-Mapping bestätigen (Empfehlung aus AVATAR-3D-KONZEPT.md)
- [ ] Umgang mit dem bestehenden Experimentier-Code klären: übernehmen, umbauen oder neu starten?
- [ ] Feature „Freunde" (existiert im Code, fehlt in der Planung): behalten und in die Roadmap aufnehmen — oder rausschneiden?
- [ ] Kleidungs-Kategorien für 3D-Vorlagen festlegen (Empfehlung: 5–6 zum Start)

## Wer macht gerade was

| Person | Aktuell dran an | Stand vom |
|---|---|---|
| Christian | Planung/KI-Infrastruktur mit Claude Code | 17.07.2026 |
| Katha | — (bitte selbst eintragen) | — |
| Teammitglied 3 | — (bitte selbst eintragen) | — |

## Nächste Schritte (teamweit)

- [ ] Claude-Projekt auf claude.ai anlegen, GitHub-Connector verbinden, im Team teilen
- [ ] Jedes Teammitglied klont das Repo und arbeitet mit Claude Code darin
- [ ] Katha: maschinen-spezifische Permission aus `.claude/settings.json` in die lokale `settings.local.json` umziehen
- [ ] MakeHuman ausprobieren (jeder ~1 Stunde) und Eindruck hier festhalten
- [ ] Offene Entscheidungen (siehe oben) beim nächsten Team-Sync klären

## Wissensspeicher (Erkenntnisse, die nicht verloren gehen sollen)

- **Ready Player Me wurde 01/2026 abgeschaltet** (Netflix-Übernahme) — Lehre: keine Abhängigkeit von proprietären Plattformen; MakeHuman-Assets liegen als Dateien bei uns (CC0-Lizenz).
- **Werkstatt/Schaufenster-Prinzip:** MakeHuman ist Entwickler-Werkzeug zum Bau des Avatar-Rohlings (GLB mit Morph Targets); Nutzer sehen nur unseren eigenen Editor. Gespeichert wird pro Nutzer nur die Reglerstellung, nie das Modell.
- **Git-Falle auf Christians Rechner:** In `C:\Users\chris` liegt ein versehentliches Git-Repo über das ganze Home-Verzeichnis — dort nie pauschal committen.

---

## Log (neueste Einträge oben)

- **17.07.2026 · Christian/Claude:** BRAIN.md angelegt. KI-Infrastruktur eingerichtet: Vault-Clone ↔ GitHub-Sync, CLAUDE.md gepusht. Planungsdokumente (ROADMAP, AVATAR-3D-KONZEPT, roadmap.html) liegen im Repo.
- **12.07.2026 · Christian/Claude:** Tech-Stack entschieden (Python/FastAPI, MongoDB, Three.js) und in ROADMAP.md dokumentiert.
- **~10.07.2026 · Christian/Claude:** Avatar-Konzept umgestellt: 3D-Spielfigur statt KI-Foto-Generierung; AVATAR-3D-KONZEPT.md ersetzt KI-AVATAR-KONZEPT.md.
- **09.07.2026 · Christian/Claude:** Erste Roadmap erstellt (8 Phasen, 26 Wochen).
