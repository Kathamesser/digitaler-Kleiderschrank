# ERM – Sharely

Stand: 20.10.2026 (mit Manuels Entscheidungen von 10:24, 10:36 und 11:11) · Entwurf von Manuel/Claude(Laptop.Cowork) für Manuel (Aufgabe „ERM festlegen“ aus `BRAIN.md`). **Grundlage sind jetzt die Desktop-Mockups vom 20.10.2026** (`docs/mockups/desktop/`, von Christian hochgeladen). Wo sie von den Wireframes der Technischen Konzeption oder von früheren Fassungen dieses ERM abweichen, gelten die Mockups. **Von Manuel am 20.10.2026 festgelegt.** Offen sind nur noch die zwei Punkte in Abschnitt 9; beide ändern die Struktur nicht.

Datenbank: **MongoDB** (Technische Konzeption 2.2). Das ERM beschreibt die Daten fachlich, Abschnitt 6 zeigt, wie daraus Collections werden.

## 1. Grundlagen

- **Desktop-Mockups vom 20.10.2026** (26 Bildschirme): Anmeldung, Hauptmenü, Kleiderschrank, Kleidungsstück hinzufügen/Detail/Filter, Outfits, Freunde, Leihen/Verschenken, Nachrichten, Profil, Garderobe
- `docs/planung/Userstory.md` (User Stories 1–10), Use Cases der Technischen Konzeption
- `docs/avatar/FIGUR-DATENMODELL.md` (Figur, entschieden am 12.10.2026)
- Christians Vorschläge vom 16.10.2026 (`ERM-VORSCHLAEGE-2026-10-16.md`): Tags, Wertetabellen, 3D-Vorlagen
- Kathas Umsetzung von User Story 8 (`Sharely_programm/backend/app/module/kleidung`)

## 2. Diagramme

`ERM_Sharely.drawio` (draw.io) hat zwei Reiter, beide auch als Bild:

| Reiter | Inhalt | Bild |
|---|---|---|
| ERM | Das ERM im Stil des Unterrichtsbeispiels: ein Kasten je Tabelle, Primärschlüssel `ID` unterstrichen, Fremdschlüssel als `…_ID`, rechtwinklige Verbindungen mit Kardinalitäten | `erm_sharely.png` |
| MongoDB | Umsetzung in MongoDB: Collections, Felder mit Datentyp, eingebettete Teile, Indizes, feste Wertelisten | `erm_teil3_mongodb.png` |

**Notation der Kardinalitäten** (steht jeweils am Ende der Linie bei der Tabelle):

| Zeichen | Bedeutung |
|---|---|
| 1 | genau eins |
| c | keins oder eins |
| n | eins oder mehrere |
| cn | keins, eins oder mehrere |

Beispiel: Nutzer **1** —— **cn** Kleidungsstueck heißt: Ein Nutzer hat keins, eins oder mehrere Kleidungsstücke, jedes Kleidungsstück gehört genau einem Nutzer.

**n:m-Beziehungen** sind über Zuordnungstabellen aufgelöst:
- `Zuordnung_Outfit_KS`: welches Kleidungsstück in welchem Outfit steckt, mit `Position`
- `Zuordnung_KS_Kategorie` und `Zuordnung_Outfit_Kat`: Kategorien eines Kleidungsstücks bzw. Outfits
- `Zuordnung_KS_Saison`: Saisons eines Kleidungsstücks
- `Kleidungsmass`: Maße eines Kleidungsstücks je Messpunkt, mit `Wert_cm`
- `Zuordnung_Neuigk_Nutzer`: welche Neuigkeit ein Nutzer gelesen hat
- `Ausgeblendete_Kategorie`: welche Kategorien ein Nutzer in seinen Auswahl- und Filterlisten ausgeblendet hat
- `Freundschaft`: Nutzer ↔ Nutzer, mit Status

## 3. Entitäten

| Entität | Bedeutung | Wichtigste Attribute | Mockup |
|---|---|---|---|
| **Nutzer** | registriertes Konto | Nutzername (eindeutig, darüber werden Freunde gefunden), E-Mail, Passwort-Hash, Profilbild, **Ist_Admin** (nur direkt in der Datenbank setzbar), erstellt am („Mitglied seit“) | Registrierung, Mein Profil, Freund hinzufügen |
| **Sitzung** / **Passwort_Reset** | Anmeldung und „Passwort vergessen“, Verfahren wie in `BRAIN.md` empfohlen (siehe Entscheidung 13) | Token-Hash, läuft ab am | Desktop 1–4 |
| **Figur** | 3D-Avatar, 0 bis 3 je Nutzer: die Hauptfigur (`Ist_Standard`) und bis zu zwei weitere in „Slot 1“ und „Slot 2“ | Reglerwerte, Figurtyp, ist Standard, **für Freunde sichtbar** | Garderobe („Lena hat ihren Avatar für Freunde freigegeben“), Meine Outfits (Avatar + Slot 1/2) |
| **Freundschaft** | gegenseitige Freundschaft mit Anfrage | Anfragender, Angefragter, Status (angefragt/angenommen/abgelehnt/blockiert), beantwortet am („Freunde seit“) | Meine Freunde, Freund hinzufügen |
| **Kleidungsstueck** | ein Teil im Schrank: eigenes, geliehenes oder Wunschartikel | Name, Bild, Kleidungsart, Farbe, Material, Saisons, Kategorien, Status (Eigenes/Geliehen/Verliehen/Wunschartikel), Favorit, Privat, Kaufdatum, Preis, Maße, bei geliehenen Teilen der Leihvorgang | Kleidungsstück hinzufügen / Detail / filtern |
| **Kleidungsart** | feste Liste: Tops, Pullover, Hosen, Röcke, Kleider, Jacken, Schuhe, Unterwäsche, Einteiler, Accessoires | Name, Reihenfolge, 3D-Vorlage, Messpunkte (je Messpunkt Pflicht oder optional und Zugabe-Spanne, `ZUGABEN.md`) | Hinzufügen, Filter („eine Auswahl“), Passform |
| **Kleidungsvorlage** | 3D-Modell zum Anziehen am Avatar | Name, Modelldatei, Ebene | „Kleidung anprobieren“ |
| **Farbe** | feste Farbpalette: Schwarz, Weiß, Grau, Beige, Braun, Rot, Rosa, Orange, Gelb, Grün, Blau, Dunkelblau, Lila, Bunt | Name, Hexwert | Farbkreise in Hinzufügen und Filter |
| **Material** | feste Liste: Baumwolle, Polyester, Wolle, Leinen, Seide, Leder, Jeans, Viskose, Sonstiges | Name | Hinzufügen, Filter |
| **Saison** | Frühling, Sommer, Herbst, Winter, Ganzjährig | Name | Hinzufügen, Filter |
| **Kategorie** | freie Etiketten für Kleidungsstücke und Outfits. Vorgegebene (Business, Freizeit, Abend, Sport, Party, Urlaub, Feiertage, Winterkleidung, Sommerkleidung, Lieblingsteile, Second Hand, Geschenk) gelten für alle, eigene („Neue Kategorie, z. B. Festival“) nur für ihren Nutzer | Name, Nutzer (leer = vorgegeben) | Hinzufügen, Outfit speichern, Filter |
| **Kleidungsmass** | ein Maß des Kleidungsstücks in cm, für die Passform | Messpunkt, Wert in cm | Bereich „Maße“ |
| **Messpunkt** | feste Liste der 24 Messbänder aus der Avatar-GLB (`docs/avatar/messpunkte.json`): Brust-, Taillen-, Hüftumfang, Schulterbreite, Schrittlänge, Fußlänge … | Name, Art (Umfang/Länge) | entschieden von Manuel: „Maße sind alle aus der GLB-Datei“ |
| **Produktquelle** (schwach) | Herkunft eines importierten Wunschartikels | URL, Shop, importiert am/per | Roadmap Phase 5 (KI-Import) |
| **Outfit** | Kombination mehrerer Teile | Name, Favorit, Privat, Kategorien | Meine Outfits, Outfit speichern, Detail |
| **Leihvorgang** | Anfrage zum Leihen oder Verschenken samt Verlauf | Typ, angefragt von, Status, von, bis (leer = unbefristet), Notiz, Zeitstempel | Anfrage stellen, Anfrage an Freund, Leihdetails, Leihen mit …, Nachrichten |
| **Neuigkeit** | Mitteilung des Entwicklerteams, angelegt von Admins | Typ (Update/Hinweis/Info), Titel, Text, veröffentlicht am | Nachrichten („Neuigkeiten von Sharely“) |
| **Ausgeblendete_Kategorie** | Kategorie, die ein Nutzer für sich ausgeblendet hat (Kategorien sind Filter) | Nutzer, Kategorie | entschieden von Manuel, 20.10.2026 |

## 4. Beziehungen

| Beziehung | Kardinalität | Begründung |
|---|---|---|
| Nutzer – Kleidungsstück | 1 : cn | Jedes Teil gehört genau einem Nutzer. |
| Kleidungsart – Kleidungsstück | 1 : cn | Pflicht, genau eine Art („eine Auswahl“ im Filter). |
| Farbe – Kleidungsstück, Material – Kleidungsstück | c : cn | Je höchstens eine Farbe und ein Material, beide optional. |
| Kleidungsstück – Saison | n:m über `Zuordnung_KS_Saison` | Mehrere Saisons wählbar (Herbst + Winter). |
| Kleidungsstück – Kategorie | n:m über `Zuordnung_KS_Kategorie` | Mehrere Kategorien je Teil, jede Kategorie an vielen Teilen. |
| Nutzer – Kategorie (eigene) | c : cn | Eigene Kategorien gehören einem Nutzer, vorgegebene keinem. |
| Nutzer – Kategorie (ausgeblendet) | n:m über `Ausgeblendete_Kategorie` | Jeder Nutzer kann beliebige Kategorien, auch vorgegebene, aus seinen Listen ausblenden. |
| Kleidungsstück – Messpunkt | n:m über `Kleidungsmass` (mit `Wert_cm`) | Je Teil die passenden Maße, z. B. bei einer Hose Taillenumfang und Schrittlänge. |
| Leihvorgang – Kleidungsstück (geliehen) | c : c | Der Eintrag „Geliehen“ im Schrank des Empfängers verweist auf seinen Leihvorgang; selbst eingetragene geliehene Teile (z. B. von jemandem ohne Sharely) haben keinen. |
| Kleidungsstück – Produktquelle | 1 : c | Nur importierte Teile haben eine Quelle (schwach). |
| Kleidungsart – Kleidungsvorlage | cn : c | Mehrere Arten teilen sich eine 3D-Vorlage; Accessoires haben keine. |
| Nutzer – Outfit | 1 : cn | |
| Outfit – Kleidungsstück | n:m über `Zuordnung_Outfit_KS` | Ein Outfit braucht mindestens ein Teil (n), ein Teil kann in vielen Outfits stecken (cn). |
| Outfit – Kategorie | n:m über `Zuordnung_Outfit_Kat` | Gleiche Kategorien wie bei den Teilen. |
| Nutzer – Nutzer | n:m über `Freundschaft` | Zwei Fremdschlüssel auf Nutzer. |
| Nutzer – Leihvorgang | 1 : cn (zweimal) | Besitzer und Empfänger. |
| Kleidungsstück – Leihvorgang | 1 : cn | Verlauf aller Anfragen zu einem Teil. |
| Nutzer – Figur | 1 : cn | Entschieden 12.10.2026: 0 bis 3 Figuren, die Grenze prüft das Backend. |
| Nutzer – Sitzung, Nutzer – Passwort_Reset | 1 : cn | |
| Neuigkeit – Nutzer | n:m über `Zuordnung_Neuigk_Nutzer` | Merkt sich, wer was wann gelesen hat („Neu“, „Alle gelesen“). |

### Abgleich mit den Mockups

| Mockup | Was dort steht | Im ERM |
|---|---|---|
| Kleidungsstück hinzufügen | Foto, Name, Farbe (Farbkreise), Kleidungsart, Kategorie (Auswahl + „Neue Kategorie“), Maße, Saison, Material, Kaufdatum, Preis, Favorit, Privat, Status Eigenes/Geliehen/Verliehen/Wunschartikel | alle Felder; Status `im_schrank`/`geliehen`/`verliehen`/`wunsch` |
| Kleidungsstück – Detail | „Kategorien“ (Plural), Leihdetails „an Lena Becker, überfällig seit …“, Kleidung anprobieren | n:m Kategorie, Leihvorgang, Kleidungsvorlage |
| Kleidung filtern | Favorit, Privat, Farbe, Kleidungsart, Kategorie, Material, Saison, Status, Kaufdatum und Preis von–bis | Indizes, feste Listen |
| Kleiderschrank (eines Freundes) | Kacheln mit Name und Kleidungsart, Status „Verfügbar / Bei dir / Verliehen“, „Nur verfügbare“ | Status aus Leihvorgang abgeleitet |
| Outfit speichern / Detail / filtern | Name, Kategorien, enthaltene Teile, Favorit | Outfit, Zuordnungen; `Privat` entschieden von Manuel |
| Meine Freunde, Freund hinzufügen | Anfragen annehmen/ablehnen/blockieren, Suche über Nutzername, „Freunde seit“, geteilte Teile/Outfits, „Von dir geliehen / verliehen“ | Freundschaft, Leihvorgang |
| Anfrage stellen / Anfrage an Freund | Leihen oder Verschenken bzw. „Geschenkt bekommen“, an wen, Zeitraum von–bis oder unbefristet, Notiz/Nachricht | Leihvorgang mit `Angefragt_von`, `Von`, `Bis`, `Notiz` |
| Nachrichten | Leih- und Geschenkanfragen, „Neuigkeiten von Sharely“ mit „Neu“ und „Alle gelesen“ | Leihvorgang (Status angefragt), Neuigkeit + Zuordnung |
| Hauptmenü | Zähler Eigene/Wunsch/Verliehene/Geliehene Artikel, gespeicherte Outfits | berechnet, nicht gespeichert |
| Garderobe (eines Freundes) | Outfits und freigegebener Avatar | Outfit, `Figur.Fuer_Freunde_sichtbar` |

## 5. Designentscheidungen (Vorschläge mit Begründung)

1. **Kleidungsart statt Kategorie als Pflicht-Einordnung.** In den Mockups ist die Kleidungsart (Tops, Hosen, Jacken …) die eine feste Einordnung, unter jedem Teil steht „Name / Kleidungsart“ („Wintermantel / Jacken“). Sie bestimmt die 3D-Vorlage. Die frühere zweite Ebene (Jeans unter Hose) entfällt, das übernimmt jetzt der Name.
2. **Kategorien sind freie Etiketten, Anlass geht darin auf.** Anlässe (Business, Freizeit …) und Gruppen wie Winterkleidung stehen in den Mockups in derselben Liste, jedes Teil und jedes Outfit kann mehrere haben, Nutzer können eigene ergänzen. Deshalb eine Entität `Kategorie` mit optionalem Nutzer (leer = vorgegeben). Das entspricht Christians Tag-Vorschlag vom 16.10.2026.
3. **Status: `im_schrank` („Eigenes“), `geliehen`, `verliehen`, `wunsch` (entschieden von Manuel, 20.10.2026).** Geliehene Teile und Wunschartikel stehen als eigene Einträge im Schrank des Nutzers. Wird eine Leihanfrage angenommen, bekommt das Teil des Besitzers `verliehen`, und im Schrank des Empfängers entsteht ein Eintrag mit `geliehen` (Name, Kleidungsart, Bild usw. übernommen) und Verweis auf den Leihvorgang. Bei der Rückgabe wird dieser Eintrag entfernt und das Original wieder `im_schrank`. Ein Nutzer kann ein Teil auch selbst als `geliehen` eintragen (dann ohne Leihvorgang). „Verfügbar / Bei dir“ beim Freund wird aus dem Leihvorgang abgeleitet.
4. **Verschenken wie in den Mockups (entschieden von Manuel, 20.10.2026):** Der Besitzer bietet an („Verschenken“) oder der Freund fragt an („Geschenkt bekommen“), der andere nimmt in „Nachrichten“ an. Danach gehört das Teil dem Empfänger: `Nutzer_ID` wechselt, Status `im_schrank`. Einen Status „verschenkt“ und ein Archiv gibt es nicht; der Verlauf bleibt im Leihvorgang (`Typ = verschenken`). Das ersetzt die Lösung mit Kopie und Archiv vom 13.10.2026.
5. **Farbe, Material, Saison als feste Wertetabellen.** Die Mockups bieten nur feste Auswahlen. Im ERM sind sie eigene Tabellen (1. Normalform, Saison mehrwertig über Zuordnung), in MongoDB feste Listen im Code (Christians Grundregel: kleine feste Listen ohne eigene Daten nicht als Collection). Die Listen hat Manuel am 20.10.2026 Claude überlassen: Farbe mit allen 14 Farben aus dem Filter-Mockup (auch im Hinzufügen-Fenster, dort sind nur 8 zu sehen), Material mit allen 8 Werten aus dem Filter plus „Sonstiges“, damit jedes Teil einen passenden Wert bekommt.
6. **Maße aus der GLB-Datei (entschieden von Manuel, 20.10.2026).** Die Maße eines Kleidungsstücks werden an denselben 24 Messbändern genommen, die der Avatar hat (`docs/avatar/messpunkte.json`). Deshalb die feste Liste `Messpunkt` und je Kleidungsstück ein `Kleidungsmass` mit Wert in cm. Die Passform („passt / eng / weit“) vergleicht Messpunkt für Messpunkt die cm des Teils mit den cm der Figur, ohne Umrechnung. Größentabelle und Größeneintrag entfallen.
7. **Gegenseitige Freundschaft statt Folgen.** Die Mockups zeigen „Freund hinzufügen“, Anfragen mit Annehmen/Ablehnen/Blockieren und „Freunde seit“ (passt zur Entscheidung vom 04.10.2026). Ein Datensatz je Paar, Status `angefragt`, `angenommen`, `abgelehnt`, `blockiert`.
8. **Leihvorgang mit Zeitraum.** Die Anfrage enthält „Gewünschter Zeitraum von–bis“ bzw. „Rückgabedatum“ und „unbefristet“, dazu eine Notiz. „Überfällig“ wird berechnet (`Bis` < heute und Status `aktiv`). Leih- und Geschenkanfragen in „Nachrichten“ sind Leihvorgänge mit Status `angefragt`.
9. **Neuigkeiten und Admins (entschieden von Manuel, 20.10.2026):** Neuigkeiten sind Mitteilungen des Entwicklerteams für alle; gelesen wird je Nutzer gemerkt. Anlegen dürfen nur Admins. Admin ist ein ganz normales Konto mit `Ist_Admin = true`; das Feld wird nur direkt in der Datenbank gesetzt, in der App wählt niemand eine Rolle. Ein Admin meldet sich normal an und hat danach mehr Rechte.
10. **Freigabe und Feedback (User Story 2) sind gestrichen.** Die Mockups zeigen kein Teilen an einzelne Freunde und kein Feedback. „Geteilt“ heißt: für alle Freunde sichtbar, bei Kleidungsstücken und Outfits über `Privat = false` (Schalter am Outfit entschieden von Manuel, 20.10.2026).
11. **Nicht gespeichert, weil berechnet:** Zähler im Hauptmenü und bei Freunden, „überfällig“, „Verfügbar / Bei dir“, Passform-Bewertung, Zentimeter der Figur.
12. **Kategorien ausblenden (entschieden von Manuel, 20.10.2026):** Kategorien sind Filter. Jeder Nutzer kann jede Kategorie, auch eine vorgegebene, für sich ausblenden; eigene Kategorien kann er zusätzlich löschen. Ausgeblendete Kategorien erscheinen nicht mehr in Auswahl und Filter, bleiben an bestehenden Teilen und Outfits aber erhalten.
13. **Anmeldeverfahren wie in `BRAIN.md` empfohlen (entschieden von Manuel, 20.10.2026):** serverseitige Sitzung, zufälliges Token im httpOnly-Cookie, Sitzungen in der Collection `sitzungen` mit TTL-Index, Passwörter mit Argon2. Dazu Passwort-Reset per befristetem Link.
14. **Löschen (entschieden von Manuel, 20.10.2026):** Jeder Nutzer kann seine Kleidungsstücke jederzeit löschen, ohne Schnappschuss für den Verlauf (siehe Abschnitt 8).

## 6. Abbildung auf MongoDB

Grundregel: **Jede Entität mit eigenem Lebenszyklus wird eine Collection, Beziehungen werden als `…_id` gespeichert. Eingebettet wird nur, was ausschließlich zu einem Dokument gehört. Kleine feste Wertelisten ohne eigene Daten stehen im Code.**

| Entität / Beziehung | Umsetzung |
|---|---|
| Nutzer, Sitzung, Passwort_Reset, Figur, Freundschaft, Leihvorgang, Kleidungsstück, Kleidungsart, Kleidungsvorlage, Kategorie, Outfit, Neuigkeit | je eine Collection (`nutzer`, `sitzungen`, `passwort_resets`, `figuren`, `freundschaften`, `leihvorgaenge`, `kleidungsstuecke`, `kleidungsarten`, `kleidungsvorlagen`, `kategorien`, `outfits`, `neuigkeiten`) |
| Zuordnung_Neuigk_Nutzer | Collection `gelesene_neuigkeiten` (wächst mit jedem Nutzer, gehört deshalb in keine Liste) |
| Kleidungsart | `_id` ist der Schlüssel (`jacken`, `hosen` …), das Kleidungsstück speichert ihn in `kleidungsart` |
| Farbe, Material, Saison | feste Listen im Code (Pydantic-Enum), am Kleidungsstück als Schlüssel bzw. Liste von Schlüsseln |
| Ausgeblendete_Kategorie | Liste `ausgeblendete_kategorie_ids` im Nutzer-Dokument (wenige Einträge, gehört nur zu diesem Nutzer) |
| Ist_Admin | Feld `ist_admin` im Nutzer-Dokument, Standard `false`; die API ändert es nie |
| Kleidungsstück – Kategorie, Outfit – Kategorie | Liste `kategorie_ids` im Dokument |
| Outfit – Kleidungsstück | Liste `teile` mit `kleidungsstueck_id` und `position` |
| Kleidungsmass, Produktquelle | eingebettet in `kleidungsstuecke.masse` (`messpunkt`, `wert_cm`) bzw. `kleidungsstuecke.quelle` |
| Messpunkt | feste Liste aus `docs/avatar/messpunkte.json` (Schlüssel wie `waist-circ`), keine Collection |
| Figur – Reglerwerte | eingebettetes Objekt `regler` (entschieden in `FIGUR-DATENMODELL.md`) |

Indizes und die festen Listen stehen im Reiter „MongoDB“.

## 7. Regeln, die MongoDB nicht selbst prüft

MongoDB kennt keine Fremdschlüssel. Diese Regeln setzt das Backend (Service-Schicht) durch:

1. Höchstens 3 Figuren je Nutzer, höchstens eine davon `ist_standard = true`.
2. Ein Kleidungsstück oder Outfit nutzt nur vorgegebene Kategorien oder eigene seines Besitzers. Kategoriename je Nutzer eindeutig.
3. Ein Outfit enthält nur Teile aus dem eigenen Schrank, mindestens eins. Erlaubt sind alle Status: eigene, Wunschartikel, geliehene und verliehene Teile (entschieden von Manuel, 20.10.2026). Wird ein geliehener Eintrag nach der Rückgabe gelöscht oder ein Teil verschenkt, verschwindet es aus den Outfits; ein Outfit ohne Teile wird gelöscht.
4. Freundschaft: nicht mit sich selbst, je Paar höchstens ein Datensatz (A→B und B→A gelten als dasselbe Paar). Blockierte Nutzer können keine neue Anfrage stellen.
5. Leihen und Verschenken nur zwischen Freunden (`angenommen`), nicht an sich selbst, nicht mit Wunschartikeln und nicht mit privaten Teilen.
6. Je Kleidungsstück höchstens ein Leihvorgang mit Status `angefragt` oder `aktiv`. Wird ein Leihvorgang `aktiv`, bekommt das Teil `status = verliehen`, und der Empfänger bekommt einen Eintrag mit `status = geliehen` und `leihvorgang_id`; bei `zurueckgegeben` wird dieser Eintrag gelöscht und das Original wieder `im_schrank`. Ein Eintrag mit `geliehen` kann nicht weiterverliehen oder verschenkt werden. Ein abgeschlossenes Geschenk setzt `nutzer_id` auf den Empfänger und `status = im_schrank`; Kategorien des Schenkenden werden vom Teil entfernt, Outfits des Schenkenden verlieren das Teil.
7. Maße nur an Messpunkten aus `messpunkte.json`, je Messpunkt höchstens ein Wert pro Teil.
8. Andere Nutzer sehen **nie** private Kleidungsstücke oder private Outfits (entschieden von Manuel, 20.10.2026), auch nicht als Teil eines sichtbaren Outfits: Dort werden private Teile ausgeblendet. Figuren sehen Freunde nur mit `fuer_freunde_sichtbar = true`.
9. Nur Nutzer mit `ist_admin = true` dürfen Neuigkeiten anlegen, ändern und löschen. `ist_admin` lässt sich über die API nicht setzen.

## 8. Löschen und Datenschutz

Körpermaße, Fotos und Kleidungsdaten sind personenbezogene Daten.

- **Kleidungsstück löschen** (jeder Nutzer, jederzeit): Läuft noch eine Anfrage oder Leihe, wird sie beendet und der Eintrag „geliehen“ beim Empfänger entfernt. Das Teil wird aus allen Outfits entfernt, das Bild im Upload-Ordner gelöscht. Leihvorgänge zu dem Teil werden mitgelöscht, ein Schnappschuss für den Verlauf wird nicht gespeichert.
- **Konto löschen** („Account löschen“ im Profil): Alle Dokumente mit seiner `nutzer_id` (Teile, Outfits, Figuren, eigene Kategorien, Sitzungen, Reset-Links, Freundschaften in beide Richtungen, gelesene Neuigkeiten) und sein Upload-Ordner werden gelöscht. Offene Leihvorgänge werden beendet; in abgeschlossenen Leihvorgängen anderer Nutzer wird die ID durch `null` („gelöschter Nutzer“) ersetzt.
- **Passwörter** nur als Argon2-Hash, Tokens nur als Hash.

## 9. Offene Fragen fürs Team

Alle anderen Fragen sind von Manuel am 20.10.2026 entschieden (siehe Abschnitt 5 und 7). Bewusst für später vorgesehen und noch nicht im ERM: **„Angebote“** im Hauptmenü. Der **KI-Import für Wunschartikel** kommt ebenfalls in Zukunft; die Tabelle `Produktquelle` ist dafür schon vorbereitet.

Noch offen (Manuel: „bleibt erstmal offen“):
1. **Welche Maße je Kleidungsart?** Z. B. Hose: Taillenumfang, Hüftumfang, Schrittlänge; Schuhe: Fußlänge. Lässt sich später als Liste an der Kleidungsvorlage hinterlegen, ohne das ERM umzubauen.
2. **Welche Kleidungsart nutzt welche 3D-Vorlage?** Startvorschlag von Christian: Oberteil (Tops, Pullover), Hose, Jacke, Rock, Kleid (Kleider, Einteiler), Schuh; Accessoires und Unterwäsche ohne Vorlage. Betrifft nur die Daten in `kleidungsarten`, nicht die Struktur.

## 10. Auswirkungen auf den bestehenden Code

Kathas Modul `Sharely_programm/backend/app/module/kleidung` (User Story 8) entsprach dem ERM vom 13.10.2026. **Umgesetzt am 20.10.2026 (Katha/Claude(Laptop.Code)):** alle Punkte der Tabelle; `kategorie_ids`, `masse` und `leihvorgang_id` sind vorbereitet, aber noch ohne eigene Logik. Prüfregeln und Indizes in MongoDB fehlen noch. Felder: `docs/api/README.md`.

| Heute im Code | Laut ERM vom 20.10.2026 |
|---|---|
| `kategorie` (oberteile, hosen, roecke, kleider, jacken, schuhe, accessoires) | `kleidungsart` (tops, pullover, hosen, roecke, kleider, jacken, schuhe, unterwaesche, einteiler, accessoires) |
| – | `name` (optional), `kategorie_ids` (Liste), `masse` (Liste aus Messpunkt + cm), `leihvorgang_id` |
| `farbe`, `material` als Freitext | Schlüssel aus fester Liste |
| `saison` ohne „ganzjährig“ | mit `ganzjaehrig` |
| `anlass` | entfällt, geht in den Kategorien auf |
| `groesse`, `marke`, `herkunft`, `notiz` | entfallen (nicht in den Mockups) |
| Status `im_schrank`, `verliehen`, `verschenkt` | `im_schrank`, `geliehen`, `verliehen`, `wunsch` |

## 11. Änderungsverlauf

| Datum | Wer | Änderung |
|---|---|---|
| 13.10.2026 | Manuel/Claude(Laptop.Cowork) | Erster Entwurf, danach im Stil des Unterrichtsbeispiels neu gezeichnet |
| 13.10.2026 | Manuel (umgesetzt von Manuel/Claude(Laptop.Cowork)) | Kleidungsstück: `name`, `waermegrad`, `wasserdicht`, `tags` gestrichen; `privat` (Standard `false`) neu; `favorit` Standard `false`; `farbe`, `saisons` u. a. optional; Status-Standard `im_schrank`; Index `(nutzer_id, privat)` |
| 13.10.2026 | Manuel/Claude(Laptop.Cowork) | Klassenzuordnung an Wireframes und User Stories angeglichen: Kategorie feste Liste (ohne Nutzer_ID), neue Entität Kleidungsart, 3D-Vorlage an der Kleidungsart; Kleidungsstück um Anlass, Preis, Kaufdatum, Herkunft, Notiz ergänzt (wie Kathas Code); Preis/Währung aus Produktquelle entfernt |
| 13.10.2026 | Manuel (umgesetzt von Manuel/Claude(Laptop.Cowork)) | Absprache bestätigt: Name, Wärmegrad, Wasserdicht bleiben gestrichen. Status vorerst `im_schrank` und `verliehen`, dazu optional `wunsch` und `archiviert` |
| 13.10.2026 | Manuel (umgesetzt von Manuel/Claude(Laptop.Cowork)) | Status `verschenkt` bleibt (Kernfunktion). Geschenk: Teil des Schenkenden wird `verschenkt` (Archiv), Empfänger bekommt eine Kopie mit `im_schrank` statt Besitzwechsel |
| 20.10.2026 | Manuel (umgesetzt von Manuel/Claude(Laptop.Cowork)) | **An die Desktop-Mockups vom 20.10.2026 angepasst:** Kleidungsart (feste Liste, Pflicht) ersetzt Kategorie als Einordnung; Kategorie wird freies Etikett (vorgegeben oder eigen, n:m zu Kleidungsstück und Outfit), Anlass geht darin auf; Name wieder da; Farbe, Material, Saison (mit Ganzjährig) als Wertetabellen; Maße am Kleidungsstück statt Größentabelle/Größeneintrag; Status `im_schrank`, `verliehen`, `wunsch` („Geliehen“ abgeleitet, Verschenken als Besitzwechsel); Folgen → gegenseitige Freundschaft mit Blockieren; Leihvorgang mit `Von`/`Bis`; Figur `Fuer_Freunde_sichtbar`; neu Neuigkeit + gelesen; gestrichen: Freigabe, Feedback, Größentabelle, Größeneintrag, `Zuletzt_getragen`, Herkunft, Notiz, Größe, Marke |
| 20.10.2026 | Manuel (umgesetzt von Manuel/Claude(Laptop.Cowork)) | Status um `geliehen` ergänzt (eigener Eintrag im Schrank, Verweis auf den Leihvorgang), `wunsch` bleibt; Verschenken wie in den Mockups (Besitzwechsel) bestätigt; Maße an den 22 Messbändern der GLB (neue Tabelle `Messpunkt`, `Kleidungsmass` mit `Messpunkt_ID`); Outfit bekommt `Privat`; „Angebote“ kommen später |
| 20.10.2026 | Manuel (umgesetzt von Manuel/Claude(Laptop.Cowork)) | Offene Fragen beantwortet: private Teile und Outfits nie für andere sichtbar (auch nicht im Outfit); Outfits dürfen Wunschartikel, geliehene und verliehene Teile enthalten; Name keine Pflicht; Avatar-Slots = weitere Figuren (max. 3); Maße je Kleidungsart noch festzulegen |
| 20.10.2026 | Manuel (umgesetzt von Manuel/Claude(Laptop.Cowork)) | Letzte offene Fragen entschieden: Kleidungsstücke jederzeit löschbar, ohne Schnappschuss; Anmeldeverfahren aus `BRAIN.md`; Farb- und Materialliste festgelegt (14 Farben, 8 Materialien + Sonstiges); neue Tabelle `Ausgeblendete_Kategorie` (Kategorien ausblenden); `Nutzer.Ist_Admin` (nur in der DB, Admins legen Neuigkeiten an); Angebote und KI-Import später. Offen bleiben Maße je Kleidungsart und Zuordnung Kleidungsart → 3D-Vorlage |
| 20.10.2026 | Christian (umgesetzt von Christian/Claude(Laptop.Code)) | Zwei Messbänder ergänzt (jetzt 24): `schulterbreite_ruecken` (Schulterpunkt über den Rücken bis Schulterpunkt) und `armlaenge` (Schulter–Ellbogen–Handgelenk). Grundsatz: alle Maße rundum am 3D-Körper; Details `docs/avatar/ZENTIMETER.md` |
| 26.10.2026 | Christian (umgesetzt von Christian/Claude(Laptop.Code)) | Kleidungsart bekommt die Liste ihrer Messpunkte mit Pflicht/optional (`kleidungsarten.messpunkte`, Werte in `wertelisten.MESSPUNKTE_JE_KLEIDUNGSART`); Pflicht-Messpunkte bestimmen die Passform-Ampel, optionale geben nur Hinweise |
| 26.10.2026 | Christian (umgesetzt von Christian/Claude(Laptop.Code)) | Je Messpunkt einer Kleidungsart die Zugabe-Spanne für „passt“ (`zugabe_min`, `zugabe_max`, `einheit` Prozent bei Umfängen, cm bei Längen); Startwerte und Herleitung in `ZUGABEN.md` |
