# Avatar-Editor (Three.js)

Machbarkeits-Prototyp hat Vorrang (siehe `CLAUDE.md`). Seit 27.10.2026 gibt es den **Avatar-Konfigurator**: Seite `templates/avatar-konfigurator.html`, die Logik liegt hier.

## Starten

Wie alle Seiten: im Ordner `Sharely_programm` `python -m http.server 5173` starten, dann http://localhost:5173/frontend/templates/avatar-konfigurator.html öffnen (oder in `outfits.html` auf das Zahnrad am Avatar klicken). Das Backend ist nicht nötig. Three.js kommt vom CDN (jsDelivr, Version 0.170.0, eingebunden per Import-Map in der Seite), also braucht der Browser Internet.

## Dateien

| Datei | Inhalt |
|---|---|
| `regler.js` | Alle 47 Regler mit Schlüssel (`FIGUR-DATENMODELL.md`), Beschriftung links/rechts und Morph Target (`AVATAR-REGLER.md`), die 20 Figurtypen, der verknüpfte Regler „Gesamtumfang“, Reglergrenzen und `morphWerte()` (Reglerstellung → Morph-Werte nach `AVATAR-REGLER.md` Abschnitt 1). **Ändert sich ein Regler, zuerst `AVATAR-REGLER.md` anpassen, dann diese Datei.** |
| `avatar.js` | `AvatarAnsicht`: GLB laden, Morph-Werte auf Körper und Augen setzen, Drehen/Zoomen (`OrbitControls`), Ansichten vorne/seite/hinten, Zentimeter messen (`messen()`, Methode wie `docs/avatar/ZENTIMETER.md` Abschnitt 5). Ohne Oberfläche, damit React/Vue es übernehmen können. |
| `konfigurator.js` | Die Oberfläche: Regler-Bereiche bauen, Werte anzeigen (z. B. „weiblich 60“, Alter in Jahren), cm-Werte anzeigen und eingeben, Figurtyp wählen, Entwurf merken. |

Die Avatar-Dateien liegen in `Sharely_programm/assets/avatar/`: `Avatar_Editorgeruest.glb` und `messpunkte.json`. Die `messpunkte.json` dort ist eine Kopie von `docs/avatar/messpunkte.json`, weil der Seiten-Server den Ordner `docs/` nicht ausliefert. Beide schreibt `docs/avatar/skripte/zentimeter_messen.py`, ein Test im Backend prüft, dass sie gleich sind.

## Was der Konfigurator kann

- **Bereiche:** Grundform (offen), Figurtyp, Maße, Körperform, Arme/Beine/Füße, genau nach `AVATAR-REGLER.md` Abschnitt 3.
- **Regler −100…+100**, 0 = neutral. Die Spur ist von neutral bis zum Wert eingefärbt. ↺ oder Doppelklick setzt einen Regler zurück. Schnellstart „Weiblich“, „Männlich“, „Neutral“.
- **Grenzen** (Vorschläge, Teamentscheidung offen, in `regler.js` → `GRENZEN`): Alter −31 bis +100 (≈ 18 bis 90 Jahre), Körpergröße −40 bis +45 (≈ 144 bis 205 cm).
- **Figurtyp:** Pillen, der zum Geschlechtsregler passende Satz steht oben, dazu Stärke 0–100. Immer höchstens ein Typ aktiv.
- **Gesamtumfang:** verschiebt alle 11 Umfang-Maße gleichzeitig (Vorschlag aus `AVATAR-REGLER.md` 4). Wird nicht gespeichert, nur die einzelnen Regler.
- **Zentimeter:** Übersicht „Deine Maße“ neben dem Avatar, dazu bei jedem Maß-Regler, bei Körpergröße und Fußgröße der gemessene Wert. Wer dort einen Wert in cm einträgt, bekommt den Regler passend gestellt (ZENTIMETER.md 5, „Eingabe in cm“). Geht der Wert mit den Grenzen nicht, sagt die Seite, wie nah sie herankommt. Die Messung stimmt auf 0,1 cm mit dem Python-Skript überein (geprüft 27.10.2026 an Standard-, Frauen- und Männerfigur).
- **Entwurf merken:** Die Figur steht im Format von `FIGUR-DATENMODELL.md` (`name`, `regler_version`, `regler` nur mit Werten ≠ 0, `figurtyp`) im `localStorage` des Browsers und ist nach dem Neuladen wieder da.

## Noch offen

- **Speichern über die API** (`/api/figuren`, 0–3 Figuren je Nutzer): Das Backend-Modul `figuren` ist noch leer. `alsFigur()` in `konfigurator.js` liefert schon das passende Format.
- **Alter:** Die Morph Targets wirken linear. `min_age` bei −31 macht die Figur deshalb rund 33 cm kleiner (laut `messpunkte.json`: `min_age` = −105,8 cm bei −100), obwohl 18 Jahre gemeint sind. Die Untergrenze sollte das Team mit Blick darauf entscheiden.
- Beschriftung von „Proportionen“ am Modell prüfen (`AVATAR-REGLER.md` 5).
