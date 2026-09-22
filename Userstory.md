# User Stories — StyleHUB

*Aus dem GitHub-Kanban-Board (Kathamesser/digitaler-Kleiderschrank) übernommen, Stand 22.09.2026. Für die zuvor leeren Storys hat Claude Entwurfs-Anforderungen ergänzt (als "Vorschlag von Claude" markiert) — vor dem nächsten Team-Sync bitte gemeinsam prüfen und anpassen.*


## User Story 1: Kleiderschrank-Übersicht

**Als Nutzer möchte ich meinen gesamten Kleiderschrank im Überblick haben, damit ich entspannt auf dem Sofa meine Outfits planen kann.**

**Anforderungen:**

- Der Nutzer kann alle Kleidungsstücke seines Kleiderschranks in einer Übersicht anzeigen lassen
- Jedes Kleidungsstück wird mit Bild und Bezeichnung angezeigt
- Der Nutzer kann die Kleidungsstücke nach Kategorien filtern, z. B. Hosen, Oberteile, Schuhe
- Der Nutzer kann ein Kleidungsstück auswählen und weitere Informationen dazu anzeigen
- Die Übersicht wird automatisch aktualisiert, wenn ein Kleidungsstück hinzugefügt oder gelöscht wird


## User Story 2: Kleiderschrank mit Freunden teilen

**Als Nutzerin möchte ich einzelne Kleidungsstücke und geplante Outfits mit Freunden teilen können, damit sie mir Feedback zu meinen Outfits geben können.**

**Anforderungen:**

- Der Nutzer kann einzelne Kleidungsstücke und/oder Outfits auswählen
- Der Nutzer kann ausgewählte Kleidungsstücke und Outfits mit Freunden teilen
- Der Nutzer kann bestimmte Freunde (einen oder mehrere Nutzer) als Empfänger auswählen
- Der Empfänger sieht Bild und Informationen zum geteilten Kleidungsstück oder Outfit
- Der Nutzer kann die Freigabe eines Kleidungsstücks oder Outfits wieder entfernen
- Geteilte Inhalte sind nur für die ausgewählten Freunde sichtbar


## User Story 3: Kleidungssimulation

**Als Nutzer möchte ich mit meinem Avatar Outfits anprobieren, damit ich vorab sehe welches Outfit zu mir passt.**

**Anforderungen:**

- Der Nutzer kann einen Avatar erstellen (einen oder mehrere??)
- Der Nutzer kann seinen Avatar bearbeiten
- Der Nutzer kann Kleidungsstücke aus seinem Kleiderschrank für den Avatar auswählen
- Der Nutzer kann mehrere Kleidungsstücke zu einem Outfit kombinieren
- Der Avatar zeigt die ausgewählten Kleidungsstücke visuell an
- Der Nutzer kann Kleidungsstücke an- und ausziehen oder austauschen
- Der Nutzer kann das zusammengestellte Outfit speichern
- Der Nutzer kann das gespeicherte Outfit jederzeit unter "gespeicherte Outfits" einsehen
- Der Nutzer kann ein gespeichertes Outfit wieder löschen
- Der Nutzer kann gespeicherte Outfits erneut am Avatar anzeigen


## User Story 4: Kleidungsstücke/Outfits kennzeichnen

**Als Nutzer möchte ich Kleidungsstücke und Outfits für besondere Anlässe markieren können (z. B. mit einem Herz), damit ich sie später schnell wiederfinden und gezielt für diese Anlässe verwenden kann.**

**Anforderungen:**

- Der Nutzer kann Kleidungsstücke mit einem Herz markieren
- Der Nutzer kann Outfits mit einem Herz markieren
- Der Nutzer kann die Markierung wieder entfernen, indem er das Herz erneut anklickt
- Der Nutzer kann seinen Kleiderschrank nach "Favoriten" filtern, damit nur mit Herz markierte Outfits und Kleidungsstücke angezeigt werden
- Beim Löschen eines Kleidungsstücks wird es auch aus den Favoriten entfernt


## User Story 5: Kleidung nach Kategorie filtern

**Als Nutzer möchte ich meine Kleidungsstücke nach Kategorien filtern können, damit ich schneller das passende Kleidungsstück finde.**

**Anforderungen:**

*Vorschlag von Claude — im GitHub-Issue #5 bislang nichts hinterlegt, bitte im Team prüfen/anpassen.*

- Der Nutzer kann im Kleiderschrank eine oder mehrere Kategorien auswählen (z. B. Hosen, Oberteile, Schuhe, Jacken)
- Nach der Auswahl werden nur Kleidungsstücke der gewählten Kategorie(n) angezeigt
- Der Nutzer kann die Filterung jederzeit zurücksetzen, um wieder alle Kleidungsstücke zu sehen
- Die Kategorie eines Kleidungsstücks wird beim Hinzufügen festgelegt oder per KI-Erkennung vorgeschlagen
- Mehrere Filter (z. B. Kategorie + Favoriten) lassen sich kombinieren


## User Story 6: Login/Logout

**Als registrierter Nutzer möchte ich mich mit meinen Zugangsdaten ein- und ausloggen können, damit ich auf meine gespeicherten Kleidungsstücke und Outfits zugreifen kann.**

**Anforderungen:**

*Vorschlag von Claude — im GitHub-Issue #6 bislang nichts hinterlegt, bitte im Team prüfen/anpassen.*

- Der Nutzer kann sich mit E-Mail/Benutzername und Passwort einloggen
- Bei falschen Zugangsdaten erhält der Nutzer eine verständliche Fehlermeldung
- Der Nutzer kann sich jederzeit über eine Logout-Funktion abmelden
- Nach dem Login gelangt der Nutzer direkt zu seiner Kleiderschrank-Übersicht
- Die Sitzung bleibt bestehen, bis sich der Nutzer aktiv abmeldet oder die Sitzung abläuft
- Passwörter werden niemals im Klartext gespeichert


## User Story 7: Passwort zurücksetzen

**Als Nutzer möchte ich mein Passwort zurücksetzen können, falls ich es vergessen habe, damit ich trotzdem wieder Zugriff auf mein Konto bekomme.**

**Anforderungen:**

*Vorschlag von Claude — im GitHub-Issue #7 bislang nichts hinterlegt, bitte im Team prüfen/anpassen.*

- Der Nutzer kann auf der Login-Seite "Passwort vergessen" auswählen
- Der Nutzer gibt seine registrierte E-Mail-Adresse ein
- Der Nutzer erhält einen zeitlich begrenzten Link zum Zurücksetzen des Passworts per E-Mail
- Über den Link kann der Nutzer ein neues Passwort vergeben
- Der Link verliert nach einmaliger Nutzung oder nach Ablauf der Frist seine Gültigkeit


## User Story 8: Kleidungsstück digitalisieren

**Als Nutzer möchte ich ein Foto von einem Kleidungsstück hochladen, um es in meinem digitalen Kleiderschrank zu sehen.**

**Anforderungen:**

*Vorschlag von Claude — im GitHub-Issue #8 bislang nichts hinterlegt, bitte im Team prüfen/anpassen.*

- Der Nutzer kann ein Foto von einem Kleidungsstück über die Kamera aufnehmen oder aus der Galerie hochladen
- Das hochgeladene Bild wird dem Kleidungsstück im digitalen Kleiderschrank zugeordnet
- Der Nutzer kann dem Kleidungsstück eine Kategorie und weitere Angaben zuordnen (z. B. Farbe, Größe)
- Der Nutzer erhält eine Bestätigung, sobald das Kleidungsstück erfolgreich digitalisiert wurde
- Fehlerhafte oder zu große Bilddateien werden mit einer verständlichen Meldung abgelehnt


## User Story 9: Kleidungsstück verleihen

**Als Nutzer möchte ich Kleidungsstücke an Freunde verleihen können, damit ich selten getragene Teile trotzdem sinnvoll nutzen kann.**

*Hinweis: Für Issue #15 ("verleihen") war ursprünglich kein eigener Story-Text hinterlegt — Satz und Anforderungen sind komplett Vorschlag von Claude.*

**Anforderungen:**

*Vorschlag von Claude — bitte im Team prüfen/anpassen.*

- Der Nutzer kann ein Kleidungsstück als "verliehen" markieren
- Der Nutzer kann auswählen, an wen (welchen Freund) das Kleidungsstück verliehen wurde
- Verliehene Kleidungsstücke werden im Kleiderschrank entsprechend gekennzeichnet
- Der Nutzer kann optional ein Rückgabedatum hinterlegen
- Der Nutzer kann ein Kleidungsstück wieder als "zurückerhalten" markieren, wodurch die Markierung entfernt wird


## User Story 10: Kleidungsstück verschenken

**"Nutzer möchte ich Kleidungsstücke an Freunde verschenken können, damit ich nicht mehr benötigte Kleidung unkompliziert weitergeben kann."**

*Hinweis: Dieser Story-Text stand ursprünglich unter Issue #15 ("verleihen"), passt inhaltlich aber zu diesem Issue ("verschenken") — hier entsprechend zugeordnet. Nur in diesem Dokument korrigiert; in GitHub (Issue #15/#16) unverändert, bitte bei Gelegenheit dort nachziehen.*

**Anforderungen:**

*Vorschlag von Claude — im GitHub-Issue #16 bislang nichts hinterlegt, bitte im Team prüfen/anpassen.*

- Der Nutzer kann ein Kleidungsstück als "verschenkt" markieren
- Der Nutzer kann optional auswählen, an wen das Kleidungsstück verschenkt wurde
- Ein verschenktes Kleidungsstück wird automatisch aus dem aktiven Kleiderschrank entfernt bzw. archiviert
- Der Nutzer erhält eine Bestätigung, bevor die Aktion endgültig ausgeführt wird
- Verschenkte Kleidungsstücke lassen sich optional in einer Archiv-Ansicht einsehen
