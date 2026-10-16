# ERM: Vorschläge zur Besprechung (16.10.2026)

Stand: 16.10.2026 · Christian/Claude(Laptop.Code) für Christian · **Noch nicht im Team beschlossen.** Grundlage: Prüfung von `ERM_Sharely.pdf` und Christians Folgefragen. Bezieht sich auf `ERM-SHARELY.md` (Manuel).

## Ergebnis der Prüfung

Das ERM ist technisch in Ordnung: Kardinalitäten, Zuordnungstabellen und MongoDB-Abbildung passen zusammen. Klassenzuordnung (Kategorie → Kleidungsart → 3D-Vorlage), Figur und Passform über die Größentabelle können bleiben, wie sie sind.

## Grundregel

**Hat ein Wert eine technische Wirkung, kommt er aus einer festen Liste. Dient er nur dem Filter, ist er ein freier Tag.**

- Eigene Tabelle (ERM) bzw. Collection (MongoDB) nur, wenn der Wert selbst Daten trägt (z. B. Reihenfolge, Vorlage) oder ohne Code-Änderung erweiterbar sein soll.
- Feste, kleine Wertelisten ohne eigene Daten: im ERM als Wertetabelle, in MongoDB als Enum im Code (Pydantic), am Dokument als Liste der Schlüssel.

## 1. Kleidungsart und 3D-Vorlagen

- **Kleidungsart:** große feste Liste, aus der der Nutzer wählt. Jede Art ist nur ein Datensatz (Name, Kategorie, `Vorlage_ID`); neue Arten brauchen keinen Code.
- **3D-Vorlage:** wenige, sie sind die eigentliche Arbeit. Viele Arten zeigen auf dieselbe Vorlage. Eine neue Vorlage braucht es nur bei deutlich anderer Form am Körper (kurz/lang, Rock/Kleid), nicht bei anderem Namen. Startvorschlag (passt zur Empfehlung „5–6 Vorlagen“ in `AVATAR-3D-KONZEPT.md`):

| Vorlage | Kleidungsarten (Beispiele) |
|---|---|
| Oberteil | T-Shirt, Top, Hemd/Bluse, Pullover |
| Hose lang | Jeans, Stoffhose |
| Hose kurz | Shorts |
| Jacke | Jacke, Wintermantel |
| Rock | Rock |
| Kleid | Kleid, Einteiler |
| Schuh | Sneaker, Stiefel, Sandalen |
| – | Accessoires: keine Vorlage, keine Passform |

- **Kategorie** gruppiert nur (Filter, Auswahl der passenden Arten) und hat keine technische Wirkung aufs 3D-Modell.

## 2. Passform („passt / eng / weit“)

- Läuft nicht über das 3D-Modell, sondern: Kleidungsstück (`Groesse`, `Groessentabelle_ID`) → Größeneintrag (`Min_cm`/`Max_cm` je Maß) ↔ cm der Figur (vom Editor gemessen, `docs/avatar/ZENTIMETER.md`).
- Die 3D-Vorlage sitzt optisch immer, weil sie mit denselben Morph-Werten mitwächst. Eng/weit kommt nur aus der Rechnung und kann am Avatar z. B. farbig markiert werden.
- **Im Code nichts je Kleidungstyp:** eine Funktion vergleicht die Maße, die im Größeneintrag stehen (eine Hosen-Tabelle hat keinen Brustumfang). Optional später: Liste `masse` an der Kleidungsvorlage (nicht an der Kleidungsart, die relevanten Maße hängen an der Körperregion).

## 3. Tags (neu, freie Etiketten)

- Der Nutzer vergibt beliebige Tags, die nur dem Filter und der Suche dienen und sonst keine technische Wirkung haben.
- **Eigene Kategorien und eigene Anlässe der Nutzer werden Tags.** Die feste Kategorie bleibt Pflicht.
- **ERM:** `Tag` (ID, Nutzer_ID, Name) + `Zuordnung_KS_Tag` (n:m).
- **MongoDB:** keine eigene Collection, Liste `tags` am Kleidungsstück, Index `(nutzer_id, tags)`, Vorschläge beim Tippen per `distinct("tags")` über die Teile des Nutzers. Eigene Collection erst, wenn Tags eigene Daten bekommen (z. B. Farbe) oder zentral umbenannt werden sollen.
- **Backend:** Tags vereinheitlichen (kleingeschrieben, ohne Leerzeichen am Rand, keine Doppelten).
- Hinweis: `tags` wurde am 13.10.2026 von Manuel gestrichen, die Wiederaufnahme muss das Team beschließen.

## 4. Anlass und Saison

- Bleiben **feste Auswahl**, weil sie technisch wirken sollen: Outfit-Vorschläge (USP), User Story 4 („Outfits für besondere Anlässe“), KI-Vorschlag beim Import.
- **ERM:** je eine Wertetabelle `Saison` und `Anlass` (ID, Name, Reihenfolge) plus `Zuordnung_KS_Saison` und `Zuordnung_KS_Anlass`, da mehrere Werte je Teil möglich sind (löst die 1.-Normalform-Frage).
- **MongoDB:** keine eigene Collection, Enum im Code (wie heute in `kleidung/schemas.py`), am Kleidungsstück Liste der Schlüssel, z. B. `anlass: ["sport", "alltag"]`.
- **Oberfläche:** Anlass als Pillen-Auswahl, darunter freies Feld „Eigene Tags“; im Filter stehen beide nebeneinander.

## 5. Kleinere Korrekturen

1. `herkunft` um den Wert `geschenk` ergänzen (Kopie beim Verschenken), optional Verweis auf Leihvorgang bzw. Original.
2. **Folgen oder Freundschaft** festlegen (Entscheidung vom 04.10.2026: gegenseitige Freundschaft; `ERM-SHARELY.md` offene Frage 1) und auf ERM- und MongoDB-Seite gleich benennen. Bei gegenseitiger Freundschaft: A→B und B→A nicht doppelt zulassen (Backend-Regel oder IDs sortiert speichern).
3. `Geaendert_am` bei Figur und Outfit auf der ERM-Seite ergänzen; rote Markierung bei `Typ` (Leihvorgang) entfernen.
4. Figur: beim Attribut `Regler` Fußnote „47 Werte −100…+100, eingebettet, siehe `docs/avatar/FIGUR-DATENMODELL.md`“.
5. `Kategorie_ID` und `Kleidungsart_ID` am Kleidungsstück sind bewusst doppelt (Art ist optional); Regel 7.2 in `ERM-SHARELY.md` sichert die Konsistenz.
6. In `ERM-SHARELY.md` begründen: Im ERM wird fachlich normalisiert, in MongoDB werden kleine feste Wertelisten als Enum und Mehrfachwerte als Liste im Dokument gespeichert.

## Zu entscheiden beim nächsten Treffen

- [ ] Tags wieder aufnehmen (Abschnitt 3)?
- [ ] Eigene Kategorien/Anlässe der Nutzer als Tags statt eigener Tabellen?
- [ ] Anlass und Saison als feste Listen mit Wertetabellen im ERM (Abschnitt 4)?
- [ ] Startliste der 3D-Vorlagen (Abschnitt 1)?
- [ ] Folgen oder gegenseitige Freundschaft?
- [ ] Kleinere Korrekturen (Abschnitt 5) ins ERM übernehmen?
