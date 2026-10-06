# Sprint 01 · 06.10.–19.10.2026

**Planning am:** 06.10.2026
**Teilnehmende:** Manuel Herrmann, Katharina Lutzky, Christian Maschke
**Sprintlänge:** 2 Wochen *(Annahme — im Team bestätigen)*
**Roadmap-Bezug:** Phase 1 „Architektur, API & Design" (Datenbankschema, klickbare Wireframes) — siehe [ROADMAP.md](../../ROADMAP.md)

---

## 1. Warum ist dieser Sprint wertvoll? (Sprint Goal)

> **Sprintziel:** Am Ende des Sprints steht das Fundament, auf dem alle drei parallel weiterarbeiten können: ein abgestimmtes Datenmodell, eine laufende MongoDB-Datenbank mit Testdaten und Mockups der Kernbildschirme.

Begründung:
- Datenmodell und Mockups sind die **gemeinsamen Schnittstellen** des Teams — Backend, Frontend und Avatar-Editor hängen davon ab. Ohne sie arbeitet jede Person gegen eigene Annahmen.
- Die Mockups machen die User Stories (siehe [Userstory.md](../../Userstory.md)) zum ersten Mal **sichtbar und überprüfbar** — Lücken und Widersprüche fallen jetzt billig auf statt später im Code.
- Das Datenmodell ist der Ort, an dem **Datenschutz** von Anfang an mitgedacht wird (Körpermaße/Aussehen = personenbezogene Daten) — prüfungsrelevant.

## 2. Was kann in diesem Sprint umgesetzt werden? (Sprint Backlog)

| # | Aufgabe | Ergebnis (wann ist es fertig?) | Verantwortlich | Schätzung |
|---|---|---|---|---|
| 1 | **Datenbankmodell festlegen** | Collections und Felder für Nutzer, Kleidungsstück, Outfit, Wunschartikel, Avatar-Konfiguration dokumentiert (Diagramm + Beschreibung in `docs/`), vom Team abgenommen; personenbezogene Felder markiert | ? | ? |
| 2 | **Datenbank erstellen** | MongoDB läuft (lokal oder Atlas — entscheiden), Collections mit Schema-Validierung angelegt, Testdaten-Skript im Repo, Anleitung zum Aufsetzen in der README | ? | ? |
| 3 | **Mockups erstellen** | Mockups für Kleiderschrank-Übersicht, Kleidungsstück erfassen/Detail, Outfit zusammenstellen, Avatar-Editor, Login — Bilder/Link im Repo abgelegt, im Team besprochen | ? | ? |
| 4 | *(Vorschlag)* Offene Entscheidungen klären, die das Modell betreffen | Entscheidungen zu Kleidungs-Kategorien und Körpermaßen (Regler mit cm-Mapping) in `BRAIN.md` festgehalten | ? | ? |

**Bewusst nicht in diesem Sprint:** Programmierung von Backend-Endpunkten und Frontend, 3D-Prototyp *(falls Kapazität frei ist, ggf. als Stretch-Goal — siehe Empfehlung „Risiko zuerst" in der Roadmap)*.

## 3. Wie wird die Arbeit umgesetzt? (Plan)

**Reihenfolge und Abhängigkeiten**
1. **Woche 1 — Modell zuerst:** Aufgabe 4 und 1 gemeinsam starten (kurze Session zu dritt), da DB und Mockups davon abhängen. Ausgangspunkt: User Stories + bestehender Experimentier-Code (`models.py`, dort SQL-basiert — nur als Ideensammlung, nicht 1:1 übernehmen, Zielbild ist MongoDB).
2. **Parallel ab Mitte Woche 1:** Mockups (Aufgabe 3) — Bildschirme direkt aus den User Stories ableiten; welche Daten auf einem Screen stehen, fließt ins Modell zurück.
3. **Woche 2:** Datenbank aufsetzen (Aufgabe 2) auf Basis des abgenommenen Modells, Testdaten einspielen.

**Werkzeuge und Ablage**
- Jede Aufgabe als Issue im GitHub-Board, diesem Sprint (Milestone „Sprint 01") zugeordnet
- Datenbankmodell: Diagramm z. B. mit draw.io oder Mermaid, abgelegt unter `docs/`
- Mockups: z. B. Figma oder Excalidraw; Export/Link im Repo
- Fertig ist eine Aufgabe erst nach der Definition of Done (Issue #11)

**Abstimmung im Sprint**
- Kurzer Sync *(Termin festlegen, z. B. 2× pro Woche 15 Min.)*: Was habe ich gemacht, was mache ich, wo hänge ich?
- Entscheidungen sofort in `BRAIN.md` bzw. hier unter „Entscheidungen" eintragen

**Risiken**
- Körpermaße/Kategorien noch nicht entschieden → blockiert das Avatar- und Kleidungsmodell; daher als Aufgabe 4 zuerst
- Frontend-Framework (React/Vue) noch offen → für Mockups egal, für spätere Umsetzung nicht

## Entscheidungen in diesem Sprint

| Datum | Entscheidung | Begründung |
|---|---|---|
| | | |

---

## Sprint Review (19.10.2026)
*Nach dem Sprint ausfüllen: Was ist laut Definition of Done fertig? Was wurde gezeigt? Was geht zurück ins Backlog?*

## Retrospektive
*Was lief gut? · Was lief schlecht? · Was ändern wir im nächsten Sprint?*
