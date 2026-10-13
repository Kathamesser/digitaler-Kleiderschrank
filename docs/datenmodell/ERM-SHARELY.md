# ERM – Sharely

Stand: 13.10.2026 (überarbeitet nach Manuels Anpassungen und abgeglichen mit Wireframes, User Stories und Kathas Umsetzung von User Story 8) · Entwurf von Manuel/Claude(Laptop.Cowork) für Manuel (Aufgabe „ERM festlegen“ aus `BRAIN.md`). **Noch nicht im Team beschlossen.** Offene Punkte stehen in Abschnitt 9.

Datenbank: **MongoDB** (Technische Konzeption 2.2). Das ERM beschreibt die Daten fachlich, Abschnitt 6 zeigt, wie daraus Collections werden.

## 1. Grundlagen

Ausgewertet wurden alle Quellen, auf die `BRAIN.md` verweist:

- Technische Konzeption vom 04.10.2026: Use Cases 1.1–1.4 und die 21 Wireframes
- `Userstory.md` (User Stories 1–10)
- `ROADMAP.md` (vier Säulen, Phasen 2–5) und `AVATAR-3D-KONZEPT.md` (Passform)
- `docs/avatar/FIGUR-DATENMODELL.md`, `AVATAR-REGLER.md`, `ZENTIMETER.md` (Figur, entschieden am 12.10.2026)
- Katha/Claudes Entwurf in `docs/datenmodell/README.md` und das Backend-Gerüst (Module und Collection-Namen)

## 2. Diagramme

`ERM_Sharely.drawio` (draw.io) hat zwei Reiter, beide auch als Bild:

| Reiter | Inhalt | Bild |
|---|---|---|
| ERM | Das ERM im Stil des Unterrichtsbeispiels: ein Kasten je Tabelle, Primärschlüssel `ID` unterstrichen, Fremdschlüssel als `…_ID`, rechtwinklige Verbindungen mit Kardinalitäten | `erm_sharely.png` |
| MongoDB | Umsetzung in MongoDB: Collections, Felder mit Datentyp, eingebettete Teile, Indizes | `erm_teil3_mongodb.png` |

**Notation der Kardinalitäten** (wie im Beispiel, steht jeweils am Ende der Linie bei der Tabelle):

| Zeichen | Bedeutung |
|---|---|
| 1 | genau eins |
| c | keins oder eins |
| n | eins oder mehrere |
| cn | keins, eins oder mehrere |

Beispiel: Nutzer **1** —— **cn** Kleidungsstueck heißt: Ein Nutzer hat keins, eins oder mehrere Kleidungsstücke, jedes Kleidungsstück gehört genau einem Nutzer.

**n:m-Beziehungen** sind wie im Beispiel (`Zuordnung_SF_FZ`) über Zuordnungstabellen aufgelöst:
- `Zuordnung_Outfit_KS`: welches Kleidungsstück in welchem Outfit steckt, mit `Position`
- `Zuordnung_FG_Empf`: an welche Nutzer eine Freigabe geht
- `Folgen`: wer wem folgt (mit `Status`)

Teile, die nur zu einem Datensatz gehören (Produktquelle, Größeneintrag, Feedback, Zuordnungen), sind im ERM eigene Tabellen. In MongoDB werden sie eingebettet, siehe Abschnitt 6 und Reiter „MongoDB".

## 3. Entitäten

| Entität | Bedeutung | Wichtigste Attribute (vollständig im Diagramm) | Herkunft |
|---|---|---|---|
| **Nutzer** | registriertes Konto | nutzername, email (beide eindeutig), passwort_hash, profilbild_pfad, erstellt_am | Wireframes 1, 2, 18, 20 |
| **Sitzung** | angemeldete Sitzung | token_hash, laeuft_ab_am | US 6, Empfehlung Anmeldeverfahren in `BRAIN.md` |
| **Passwort-Reset** | einmaliger, befristeter Link | token_hash, laeuft_ab_am, eingeloest_am | US 7, Wireframes 3, 4 |
| **Figur** | 3D-Avatar des Nutzers | name, ist_standard, regler_version, regler (47 Werte), figurtyp | `FIGUR-DATENMODELL.md` |
| **Kategorie** | Oberbegriff zum Filtern und Zuordnen (Oberteil, Hose, Rock, Kleid, Jacke, Schuhe, Accessoire); feste Liste für alle | name, reihenfolge | Wireframes 5, 7, 12, US 1, 5, Use Case 1.3, Kathas Liste in `kleidung/schemas.py` |
| **Kleidungsart** | genauere Art innerhalb einer Kategorie (Jeans, Pullover, Wintermantel …); feste Liste; ersetzt die freie Bezeichnung | name, kategorie_id, vorlage_id | Wireframes 5, 11, 12 („Pullover / Oberteil“), US 1 („Bild und Bezeichnung“) |
| **3D-Kleidungsvorlage** | Schnittmuster am Avatar (T-Shirt, Hose …) | name, modell_datei, ebene | Roadmap Phase 4 |
| **Kleidungsstück** | ein Teil im Schrank oder auf der Wunschliste | Pflicht: bild_pfad, kategorie, status (`im_schrank` Standard, `verliehen`, `verschenkt`; optional später `wunsch`, `archiviert`); optional: kleidungsart, groesse, marke, farbe, material, saison, anlass, preis, kaufdatum, herkunft, notiz; favorit und privat (Standard `false`); erstellt_am/geaendert_am setzt das System | Wireframes 5, 7, 8, US 1, 4, 5, 8, Kathas Festlegung vom 13.10.2026 |
| **Produktquelle** (schwach) | Herkunft eines importierten Teils | url, shop, importiert_am, importiert_per (der Preis steht am Kleidungsstück) | Roadmap Phase 5 |
| **Größentabelle** | Zuordnung Größe → cm-Bereiche | bezeichnung, marke, abteilung, herkunft | `AVATAR-3D-KONZEPT.md` (Passform), Roadmap Phase 5 |
| **Größeneintrag** (schwach) | eine Zeile der Tabelle | groesse, masse (min/max cm je Maß) | wie oben |
| **Outfit** | Kombination mehrerer Teile | name, favorit, zuletzt_getragen | Wireframes 9–12 („Heute getragen“), US 3, 4 |
| **Freigabe** | Teil oder Outfit gezielt mit Freunden teilen | nachricht, erstellt_am | US 2 |
| **Feedback** | Rückmeldung zu einer Freigabe | text, erstellt_am | US 2 („damit sie mir Feedback geben können“) |
| **Leihvorgang** | Anfrage zum Leihen oder Verschenken samt Verlauf | typ, status, angefragt_von, rueckgabe_bis, notiz, Zeitstempel | Use Case 1.4, Wireframes 13–16, US 9, 10 |

Dazu kommen die Tabellen `Folgen` (wer wem folgt, mit Status und Datum; in MongoDB die Collection `freundschaften`) sowie die Zuordnungstabellen `Zuordnung_Outfit_KS` und `Zuordnung_FG_Empf` für die n:m-Beziehungen.

## 4. Beziehungen

| Beziehung | Kardinalität | Begründung |
|---|---|---|
| Nutzer – gehört – Kleidungsstück | (0,n) : (1,1) | Jedes Teil hat genau einen Besitzer. |
| Nutzer – erstellt – Outfit | (0,n) : (1,1) | Outfits sind privat und gehören einem Nutzer. |
| Outfit – enthält – Kleidungsstück | (1,n) : (0,n) | n:m. Ein Outfit braucht mindestens ein Teil, ein Teil kann in vielen Outfits stecken. Attribut der Beziehung: position (Reihenfolge am Avatar). |
| Nutzer – hat – Figur | (0,3) : (1,1) | Entschieden 12.10.2026: 0 bis 3 Figuren. Die Grenze prüft das Backend. |
| Kategorie – ordnet ein – Kleidungsstück | (0,n) : (1,1) | Jedes Teil hat genau eine Kategorie (Pflicht laut Katha, Filter aus Wireframe 5 und US 5). |
| Kategorie – umfasst – Kleidungsart | (0,n) : (1,1) | Jede Art gehört zu genau einer Kategorie (Jeans → Hose, Pullover → Oberteil). |
| Kleidungsart – beschreibt – Kleidungsstück | (0,n) : (0,1) | Optional, weil laut Katha nur Bild und Kategorie Pflicht sind. Ohne Art zeigt die App den Kategorienamen. |
| Kleidungsart – dargestellt durch – 3D-Kleidungsvorlage | (0,1) : (0,n) | Ein Pullover und ein T-Shirt brauchen am Avatar verschiedene Modelle, deshalb hängt die Vorlage an der Art und nicht an der Kategorie. Accessoires wie Handtaschen haben keine Vorlage. |
| Kleidungsstück – stammt aus – Produktquelle | (0,1) : (1,1) | Nur importierte Teile haben eine Quelle. Sie existiert nicht ohne das Teil (schwach). |
| Kleidungsstück – Größe laut – Größentabelle | (0,1) : (0,n) | Ohne Größentabelle keine Passform-Bewertung, das Teil ist trotzdem gültig. |
| Größentabelle – umfasst – Größeneintrag | (1,n) : (1,1) | Eine Tabelle besteht aus ihren Zeilen (schwach). |
| Nutzer – folgt – Nutzer | (0,n) : (0,n) | Rekursiv, Rollen Follower und Gefolgter. Mit Bestätigung durch den Gefolgten. |
| Nutzer – teilt – Freigabe | (0,n) : (1,1) | Absender. |
| Nutzer – sieht – Freigabe | (0,n) : (1,n) | n:m, eine Freigabe hat mindestens einen Empfänger. |
| Freigabe – zeigt Teil / zeigt Outfit | (0,1) : (0,n) | Genau eins von beiden (Regel, siehe 7). |
| Freigabe – erhält – Feedback | (0,n) : (1,1) | |
| Nutzer – schreibt – Feedback | (0,n) : (1,1) | |
| Kleidungsstück – betrifft – Leihvorgang | (0,n) : (1,1) | Ein Teil kann über die Zeit oft verliehen werden. |
| Nutzer – gibt / empfängt – Leihvorgang | je (0,n) : (1,1) | Zwei Rollen: Besitzer und Empfänger. |

### Abgleich Kleidung und Outfits mit Wireframes und User Stories

| Quelle | Was dort steht | Im ERM |
|---|---|---|
| Wireframe 5 (Schrank) | Filterleiste „Alles \| Favoriten \| Hosen \| Jacken \| Schuhe \| Tops \| Einteiler“, Kacheln mit Bild, Beschriftung, Herz | Kategorie (mit `Reihenfolge` für die Leiste), Kleidungsart als Beschriftung, `Favorit`, `Bild_Pfad` |
| Wireframe 7 (Hinzufügen) | Foto, Name, Kategorie als Auswahl, Farbe, Wärmegrad, Wasserdicht, Saison | Foto, Kategorie, Farbe, Saison übernommen; Name durch Kleidungsart ersetzt; Wärmegrad und Wasserdicht nach Kathas Festlegung gestrichen |
| Wireframe 8 (Detail) | Titel „Wintermantel“, Kategorie, Farbe, Saison, Bearbeiten, Löschen | Titel = Kleidungsart, sonst wie oben |
| Wireframe 9 (Outfits) | Kacheln aus 4 Teilbildern, Name („Business Look“) | Outfit `Name`, Teile über `Zuordnung_Outfit_KS`, Reihenfolge über `Position` |
| Wireframe 11 (Outfit erstellen) | Name des Outfits, Teile suchen und auswählen | Outfit `Name`, Zuordnung zu Kleidungsstücken (n:m); Suche über Kleidungsart, Kategorie, Marke, Farbe |
| Wireframe 12 (Outfit-Detail) | „Enthaltene Teile“ als Art und Kategorie („Jeans / Hose“), „Heute getragen“ | Kleidungsart + Kategorie, `Zuletzt_getragen` |
| US 1 | Übersicht mit Bild und Bezeichnung, Filter nach Kategorie | Bild, Kleidungsart, Kategorie |
| US 3 | Outfits speichern, löschen, am Avatar zeigen | Outfit, Zuordnung, 3D-Vorlage über die Kleidungsart |
| US 4 | Herz für Kleidungsstücke und Outfits, Filter „Favoriten“ | `Favorit` an beiden; Index `(nutzer_id, favorit)` |
| US 5 | Mehrere Kategorien filtern, mit Favoriten kombinierbar, Kategorie per KI vorgeschlagen | feste Liste, damit die KI aus bekannten Werten wählt |
| US 8 / Kathas Umsetzung | Pflicht nur Foto und Kategorie; Favorit, Privat, Größe, Marke, Farbe, Material, Saison, Anlass, Preis, Kaufdatum, Herkunft, Notiz | alle Felder 1:1 übernommen, gleiche Namen wie im Code |

Startliste der Kleidungsarten (Vorschlag, Werte aus den Wireframes **fett**): Oberteil: **T-Shirt**, Top, **Pullover**, Hemd/Bluse · Hose: **Jeans**, Stoffhose, Shorts · Rock: Rock · Kleid: Kleid, Einteiler · Jacke: Jacke, **Wintermantel** · Schuhe: Sneaker, Stiefel, Sandalen · Accessoire: **Handtasche**, **Schal**, **Mütze**.

## 5. Designentscheidungen (Vorschläge mit Begründung)

1. **Wunschartikel sind Kleidungsstücke mit `status = wunsch`**, keine eigene Entität (der Status `wunsch` ist optional und kommt erst mit der Wunschliste). Die Roadmap spricht von Teilen, die „als Wunschartikel markiert“ werden, und von der Wunschliste „als eigenem Bereich im Kleiderschrank“. So funktionieren Kategorie, Größe, Passform-Bewertung und Anprobieren am Avatar für Wunschteile ohne doppelten Code, und beim Kauf ändert sich nur der Status. Die Importdaten (URL, Shop, Preis) stehen in der eingebetteten Produktquelle.
2. **Zweistufige Klassenzuordnung: Kategorie und Kleidungsart, beide als feste Liste.** Die Wireframes zeigen zwei Ebenen: Filter und Auswahl nach Kategorie (Wireframe 5 „Hosen | Jacken | Schuhe …“, Wireframe 7 „Oberteil | Hose | Jacke | Schuhe“) und unter jedem Teil eine genauere Bezeichnung („Jeans“, „Pullover“, „Wintermantel“), in Wireframe 12 beides zusammen („Pullover / Oberteil“). Katha hat die freie Bezeichnung gestrichen. Die Kleidungsart liefert diese Beschriftung trotzdem, aus einer festen Liste statt als Freitext. Dadurch ist sie einheitlich, die KI kann sie vorschlagen (US 5), und die 3D-Vorlage lässt sich daran festmachen. Eigene Kategorien der Nutzer sind gestrichen, weil Wireframes und User Stories sie nicht zeigen; „Kategorien zuordnen“ aus Use Case 1.3 heißt hier: Kategorie und Art beim Anlegen und Bearbeiten wählen.
3. **Folgen statt Freundschaft:** Die Wireframes zeigen „möchte dir folgen“, „Folgt dir“, Follower- und Folgt-Zähler, die Konzeption „Freundschaftsanfrage bestätigen“. Beides passt zu einer gerichteten Beziehung, die der Gefolgte bestätigt. „Freunde“ im Sinne von Teilen und Leihen sind Nutzer mit bestätigter Beziehung (siehe offene Frage 1).
4. **Leihvorgang statt Status-Häkchen:** Die Wireframes zeigen Anfragen in beide Richtungen („Anfrage senden“ vom Besitzer, „möchte deinen Wintermantel leihen“ vom Freund), Annehmen/Ablehnen, Rückgabedatum, Notiz und „Als zurückgegeben markieren“. Das ist ein Vorgang mit Verlauf, deshalb eine eigene Entität mit `angefragt_von`. Verleihen und Verschenken teilen sich die Entität über `typ`.
5. **Verschenken bekommt einen eigenen Status (entschieden von Manuel, 13.10.2026, Kernfunktion; Ablauf mit Kopie für den Empfänger von Manuel bestätigt):** Ist ein Geschenk abgeschlossen, bekommt das Teil beim Schenkenden `status = verschenkt`. Es verschwindet aus seinem aktiven Schrank, bleibt aber in seiner Archiv-Ansicht sichtbar (US 10). Der Empfänger bekommt ein neues Kleidungsstück in seinem Schrank (Daten und Bild werden kopiert, `status = im_schrank`). So bleibt beim Schenkenden der Verlauf vollständig, und das Teil des Empfängers kann unabhängig davon bearbeitet, verliehen oder weiterverschenkt werden. Der Besitzer steht trotzdem im Leihvorgang selbst, damit der Vorgang auch nach Änderungen am Teil lesbar bleibt.
6. **Größentabelle als eigene Entität:** Für „passt / eng / weit“ braucht das System pro Größe cm-Bereiche (`AVATAR-3D-KONZEPT.md`). Tabellen kommen als Standard (z. B. Damen/Herren) oder aus dem KI-Import und werden von mehreren Teilen genutzt. Die Maß-Schlüssel entsprechen den Messbändern in `docs/avatar/messpunkte.json`, damit der Abgleich direkt funktioniert.
7. **Freigabe und Feedback** setzen User Story 2 um (einzelne Teile oder Outfits mit ausgewählten Freunden teilen, Freigabe zurücknehmen, Feedback bekommen). In den Wireframes kommt das noch nicht vor, siehe offene Frage 3.
8. **Sitzung und Passwort-Reset** sind technische Entitäten, aber echte Daten mit Ablaufzeit. In MongoDB löscht ein TTL-Index abgelaufene Einträge automatisch. Sie hängen an der noch offenen Entscheidung zum Anmeldeverfahren.
9. **Bilder liegen als Datei** im Ordner `uploads/<nutzer_id>/`, in der Datenbank steht nur der Pfad (Technische Konzeption 2.2).
10. **Nicht gespeichert, weil berechnet:** Zähler im Profil (Kleidungsstücke, Follower, Folgt), Passform-Bewertung, Zentimeter-Maße der Figur (`ZENTIMETER.md`) und der Status „verliehen“ als Wahrheit (er wird aus dem Leihvorgang gesetzt, siehe Regel 6).

## 6. Abbildung auf MongoDB

Grundregel wie im Entwurf: **Jede Entität mit eigenem Lebenszyklus wird eine Collection, Beziehungen werden als `…_id` gespeichert. Eingebettet wird nur, was ausschließlich zu einem Dokument gehört und mit ihm gelöscht wird.**

| Entität / Beziehung | Umsetzung | Warum |
|---|---|---|
| Nutzer, Sitzung, Passwort-Reset, Figur, Kategorie, 3D-Kleidungsvorlage, Kleidungsstück, Größentabelle, Outfit, Leihvorgang, Freigabe | je eine Collection (`nutzer`, `sitzungen`, `passwort_resets`, `figuren`, `kategorien`, `kleidungsvorlagen`, `kleidungsstuecke`, `groessentabellen`, `outfits`, `leihvorgaenge`, `freigaben`) | eigener Lebenszyklus, wird einzeln gesucht und geändert |
| Produktquelle | eingebettet in `kleidungsstuecke.quelle` | gehört nur zu diesem Teil (schwache Entität) |
| Größeneintrag | eingebettet in `groessentabellen.eintraege` | Teil der Tabelle, wird immer mit ihr gelesen |
| Outfit – enthält – Kleidungsstück (n:m) | Liste `outfits.teile` mit `kleidungsstueck_id` und `position` | Ein Outfit hat wenige Teile; es wird immer komplett geladen |
| Nutzer – folgt – Nutzer (n:m mit Attributen) | Collection `freundschaften` (`von_nutzer_id` folgt `an_nutzer_id`) | Hat Status und Datum und wächst unbegrenzt, gehört also in keine Liste im Nutzer |
| Nutzer – sieht – Freigabe (n:m) | Liste `freigaben.empfaenger_ids` | wenige Empfänger je Freigabe; Abfrage „was wurde mit mir geteilt“ über Index |
| Feedback | eingebettet in `freigaben.feedback` | existiert nur mit der Freigabe, überschaubare Menge |
| Figur – Reglerwerte | eingebettetes Objekt `regler` | entschieden in `FIGUR-DATENMODELL.md` |
| 3D-Kleidungsvorlage | Collection oder feste Liste im Code | Die Modelle selbst sind Dateien im Repo wie die Avatar-GLB; eine Collection lohnt sich erst, wenn Vorlagen ohne neuen Code dazukommen sollen |

Kategorien und Kleidungsarten sind feste Listen: Collection `kategorien` mit sprechendem Schlüssel als `_id` (`hosen`, `oberteile` …, wie in Kathas Code) und den Arten als eingebetteter Liste `arten`. Das Kleidungsstück speichert die Schlüssel (`kategorie: "hosen"`, `kleidungsart: "jeans"`). So passt Kathas bestehende Umsetzung ohne Umbau, und die Listen lassen sich ändern, ohne Code anzufassen.

Die Collection-Namen entsprechen dem Backend-Gerüst. Neu dazu kommen `sitzungen`, `passwort_resets`, `kategorien`, `kleidungsvorlagen`, `groessentabellen` und `freigaben`; `wunschartikel` entfällt (Entscheidung 1).

Indizes stehen im Reiter „MongoDB“. Wichtig sind vor allem die eindeutigen Indizes (E-Mail, Nutzername, Token, Folgen-Paar, Schlüssel der Kleidungsarten), die TTL-Indizes für Sitzungen und Reset-Links sowie `(nutzer_id, favorit)` und `(nutzer_id, privat)` für Favoriten-Filter und die Schrank-Ansicht von Followern.

## 7. Regeln, die MongoDB nicht selbst prüft

MongoDB kennt keine Fremdschlüssel. Diese Regeln muss das Backend (Service-Schicht) durchsetzen:

1. Höchstens 3 Figuren je Nutzer, höchstens eine davon `ist_standard = true`.
2. Kategorie und Kleidungsart müssen in der festen Liste stehen. Ist eine Kleidungsart gesetzt, muss sie zur Kategorie des Teils gehören (Jeans nur bei Hose).
3. Ein Outfit enthält nur Teile seines eigenen Besitzers.
4. Eine Freigabe zeigt genau ein Objekt: `kleidungsstueck_id` **oder** `outfit_id`. Empfänger und Feedback-Autoren müssen mit dem Absender eine bestätigte Folgen-Beziehung haben.
5. Leihen und Verschenken nur zwischen Nutzern mit bestätigter Folgen-Beziehung, nicht an sich selbst, nicht mit Wunschartikeln.
6. Je Kleidungsstück höchstens ein Leihvorgang mit Status `angefragt` oder `aktiv`. Wird ein Leihvorgang `aktiv`, bekommt das Teil `status = verliehen`; bei `zurueckgegeben` wieder `im_schrank`. Ein abgeschlossenes Geschenk setzt beim Teil des Schenkenden `status = verschenkt` und legt für den Empfänger eine Kopie mit `status = im_schrank` an (Bild wird in seinen Upload-Ordner kopiert). Ein Teil mit `verschenkt` kann nicht mehr verliehen, verschenkt oder in neue Outfits gelegt werden.
7. Folgen-Paar eindeutig, niemand folgt sich selbst.
8. Statuswerte und Wertebereiche (z. B. Reglerwerte −100…+100) per Pydantic-Schema prüfen, zusätzlich optional per JSON-Schema-Validierung in MongoDB.

## 8. Löschen und Datenschutz

Körpermaße, Fotos und Kleidungsdaten sind personenbezogene Daten.

- **Kleidungsstück löschen:** nicht möglich, solange ein Leihvorgang `angefragt` oder `aktiv` ist. Sonst wird es aus allen Outfits entfernt, Freigaben dazu werden gelöscht, das Bild im Upload-Ordner auch. Abgeschlossene Leihvorgänge bleiben als Verlauf (siehe offene Frage 4).
- **Konto löschen:** Alle Dokumente mit seiner `nutzer_id` (Teile, Outfits, Figuren, Sitzungen, Reset-Links, Freigaben, Folgen-Beziehungen in beide Richtungen) und sein Upload-Ordner werden gelöscht. Offene Leihvorgänge werden beendet; in abgeschlossenen Leihvorgängen anderer Nutzer und in deren Feedback-Listen wird die ID durch `null` („gelöschter Nutzer“) ersetzt.
- **Passwörter** nur als Argon2-Hash, Tokens nur als Hash.

## 9. Offene Fragen fürs Team

1. **Wer zählt als Freund?** Vorschlag: Leihen, Teilen und Kleiderschrank-Ansicht für alle, die mir bestätigt folgen. Alternative: nur gegenseitiges Folgen.
2. ~~Sichtbarkeit des Kleiderschranks~~ **entschieden (Manuel, 13.10.2026):** Bestätigte Follower sehen den Schrank (Wireframe 19), außer Teilen mit `privat = true`. Diese sind auch nicht leihbar und nicht teilbar.
3. **Freigabe und Feedback (US 2)** kommen in den Wireframes nicht vor: umsetzen, später umsetzen oder streichen?
4. **Verlauf nach dem Löschen:** Sollen abgeschlossene Leihvorgänge einen Schnappschuss (Bild, Kategorie) des Teils behalten, damit der Verlauf lesbar bleibt?
5. **Wunschartikel in Outfits:** zulassen (zum Kombinieren vor dem Kauf) oder nur am Avatar anprobieren?
6. **Leere Outfits:** Wenn das letzte Teil eines Outfits gelöscht wird: Outfit mitlöschen (Vorschlag) oder leer behalten?
7. **Tragehistorie:** Reicht `zuletzt_getragen`, oder soll jedes „Heute getragen“ gespeichert werden (Statistik, z. B. „seit 6 Monaten nicht getragen“)?
8. **Anmeldeverfahren:** Sitzung und Passwort-Reset setzen die Empfehlung aus `BRAIN.md` voraus.
9. **Wireframes nachziehen:** Name, Wärmegrad und Wasserdicht sind im Team gestrichen (Absprache, bestätigt von Manuel am 13.10.2026), stehen aber noch in den Wireframes 7 und 8; die Beschriftung übernimmt die Kleidungsart. Wireframe 5 nennt „Tops“ und „Einteiler“ als Kategorien; nach Kathas Liste sind das Kleidungsarten (Top unter Oberteil, Einteiler unter Kleid). Passt das so?
10. ~~Statuswerte~~ **entschieden (Manuel, 13.10.2026):** `im_schrank` (Standard), `verliehen`, `verschenkt`; `wunsch` und `archiviert` sind optional und kommen nur, wenn Wunschliste bzw. Archiv umgesetzt werden. In Kathas Code ist `aktiv` bereits in `im_schrank` umbenannt (Commit `20b985f`).
11. **Anlass und Saison auch für Outfits?** US 4 spricht von Outfits „für besondere Anlässe“; die Wireframes zeigen dafür nur das Herz. Vorschlag: vorerst nur Favorit, Anlass aus den Teilen ableiten.

## 10. Unterschiede zum Entwurf in `docs/datenmodell/README.md`

| Entwurf | Hier | Grund |
|---|---|---|
| eigene Entität Wunschartikel | Kleidungsstück mit `status = wunsch` + Produktquelle | Entscheidung 1 |
| Kategorie als String | feste Liste `kategorien` (Schlüssel wie in Kathas Code) plus Kleidungsart | Wireframes 5, 11, 12, US 1, 5 |
| Freundschaft angefragt/bestätigt | Folgen mit Bestätigung, Rollen Follower/Gefolgter | Wireframes 17–19 |
| Leihvorgang ohne Anfragerichtung | `angefragt_von`, Status `aktiv` und `abgeschlossen` | Wireframes 13–16, Geschenke |
| – | Größentabelle, Freigabe, Feedback, Sitzung, Passwort-Reset, 3D-Kleidungsvorlage | Passform, US 2, US 6/7, Roadmap Phase 4 |
| Kleidungsstück ohne Größe/Marke/Sichtbarkeit | `groesse`, `marke`, `material`, `privat` | US 8, Roadmap Phase 2 und 5, offene Frage 2 |
| Figur ohne Standard-Kennzeichen | `ist_standard` | offene Frage aus `FIGUR-DATENMODELL.md` |
| Outfit: Liste von IDs | Liste `teile` mit `position` | Reihenfolge am Avatar |

## 11. Änderungsverlauf

| Datum | Wer | Änderung |
|---|---|---|
| 13.10.2026 | Manuel/Claude(Laptop.Cowork) | Erster Entwurf, danach im Stil des Unterrichtsbeispiels neu gezeichnet |
| 13.10.2026 | Manuel (umgesetzt von Manuel/Claude(Laptop.Cowork)) | Kleidungsstück: `name`, `waermegrad`, `wasserdicht`, `tags` gestrichen; `privat` (Standard `false`) neu; `favorit` Standard `false`; `farbe`, `saisons` u. a. optional; Status-Standard `im_schrank`; Index `(nutzer_id, privat)` |
| 13.10.2026 | Manuel/Claude(Laptop.Cowork) | Klassenzuordnung an Wireframes und User Stories angeglichen: Kategorie feste Liste (ohne Nutzer_ID), neue Entität Kleidungsart, 3D-Vorlage an der Kleidungsart; Kleidungsstück um Anlass, Preis, Kaufdatum, Herkunft, Notiz ergänzt (wie Kathas Code); Preis/Währung aus Produktquelle entfernt |
| 13.10.2026 | Manuel (umgesetzt von Manuel/Claude(Laptop.Cowork)) | Absprache bestätigt: Name, Wärmegrad, Wasserdicht bleiben gestrichen. Status vorerst `im_schrank` und `verliehen`, dazu optional `wunsch` und `archiviert` |
| 13.10.2026 | Manuel (umgesetzt von Manuel/Claude(Laptop.Cowork)) | Status `verschenkt` bleibt (Kernfunktion). Geschenk: Teil des Schenkenden wird `verschenkt` (Archiv), Empfänger bekommt eine Kopie mit `im_schrank` statt Besitzwechsel |
