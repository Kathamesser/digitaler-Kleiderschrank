# Avatar-Dateien

Stand: 12.10.2026 · Hier liegt alles, was man für den 3D-Avatar braucht: die fertige Datei für den Editor und die Werkstatt-Dateien, um sie neu zu bauen. Für Menschen und KI-Sitzungen gleichermaßen: **Erst diese Datei lesen, dann `docs/avatar/AVATAR-REGLER.md`.**

## Was liegt hier?

| Datei | Wozu | Anfassen? |
|---|---|---|
| `Avatar_Editorgeruest.glb` | **Der Avatar für den Web-Editor** (Three.js). Neutrale Standardfigur plus 114 Morph Targets, alle starten auf 0. 8 MB. | Nur lesen. Wird vom Bauskript erzeugt, nie von Hand bearbeiten. |
| `messpunkte.json` | Kopie von `docs/avatar/messpunkte.json` für den Avatar-Konfigurator im Browser (der Seiten-Server liefert `docs/` nicht aus). | Nur lesen. Schreibt `docs/avatar/skripte/zentimeter_messen.py` zusammen mit dem Original, ein Backend-Test prüft, dass beide gleich sind. |
| `werkstatt/avatar_shapekeys.blend` | **Quelle für jeden Neubau.** Blender-Datei mit allen 547 Formen aus MakeHuman, auch Gesicht, Kopf, Hände usw. für später. | Nicht ändern. Neu erzeugt wird sie nur, wenn MakeHuman neu exportiert wird (siehe unten). |
| `werkstatt/figur_default.obj` (+ `.mtl`) | Die neutrale Standardfigur aus MakeHuman. Das Zentimeter-Skript braucht sie, um die Messpunkte zu finden. | Nicht ändern. |
| `werkstatt/textures/` | Augentextur, wird von der .blend und der .obj benutzt. | Nicht ändern. |

Beim Neubau entsteht zusätzlich `werkstatt/Avatar_Aussehen_spaeter/` mit allen Formen, die nicht im Editor sind. Der Ordner ist absichtlich nicht im Repo (`.gitignore`), weil er sich jederzeit neu bauen lässt.

Die zugehörigen Skripte liegen in `docs/avatar/skripte/`, die Erklärungen in `docs/avatar/`.

## Den Avatar im Code benutzen

- `Avatar_Editorgeruest.glb` mit dem `GLTFLoader` von Three.js laden.
- Welcher Regler im Editor welches Target bewegt und wie: `docs/avatar/AVATAR-REGLER.md`. Grundregel: ein UI-Regler von −100 bis +100 steuert ein `min_…`/`max_…`-Paar, nie beide gleichzeitig.
- Die GLB hat **zwei Meshes** (Körper und Augen) mit denselben Target-Namen. Werte immer auf beide setzen.
- Zentimeter misst der Editor direkt an der Figur: `docs/avatar/ZENTIMETER.md` und `docs/avatar/messpunkte.json`.
- Gespeichert werden pro Nutzer nur Reglerwerte: `docs/avatar/FIGUR-DATENMODELL.md`.

## Die GLB neu bauen (Regler hinzufügen, Figurtyp aussortieren …)

Man braucht nur **Blender** (Version 5) und einen aktuellen Repo-Clone. MakeHuman ist nicht nötig.

1. In `docs/avatar/skripte/blender_editorgeruest_bauen.py` die Listen oben anpassen:
   - `MACRO`, `SINGLE`: Regler mit Min/Max-Paar. Hier einen Namen ergänzen, um ihn in den Editor zu holen.
   - `SIDED`: Regler, die es links und rechts gibt. Sie werden zu einem Target zusammengelegt.
   - `EXCLUDE`: Formen, die bewusst nicht in den Editor sollen.
   - `RENAME`: verständliche Namen für die Figurtypen.
   - Welche Namen es überhaupt gibt, steht in `werkstatt/Avatar_Aussehen_spaeter/Shape_Keys_Liste.txt`. Die Datei entsteht beim ersten Neubau.
2. Blender öffnen, Reiter **Scripting**, **Open**, das Skript aus `docs/avatar/skripte/` wählen und **Run Script** klicken. Ohne Oberfläche geht es auch, im Repo-Ordner:
   ```
   blender -b --python docs/avatar/skripte/blender_editorgeruest_bauen.py
   ```
   Die Pfade findet das Skript selbst über den Repo-Ordner. Es überschreibt `Avatar_Editorgeruest.glb`.
3. Zentimeter neu messen, weil sich die Messpunkte in der GLB verschieben können. Im Repo-Ordner (Python 3 mit numpy):
   ```
   python docs/avatar/skripte/zentimeter_messen.py
   ```
4. Die neue GLB im three.js-Editor (https://threejs.org/editor/) laden und prüfen: Bei allen Reglern auf 0 steht die neutrale Figur da, und die neuen Targets sind vorhanden.
5. Doku nachziehen: neue oder geänderte Regler in `docs/avatar/AVATAR-REGLER.md`, bei neuen Reglern auch die Schlüssel in `docs/avatar/FIGUR-DATENMODELL.md`. Dann Log-Eintrag in `BRAIN.md` und Pull Request.

**Ohne Änderung an den Listen ergibt der Neubau dieselbe GLB** mit denselben 114 Targets. Mit Blender 5.0 ist sie sogar bit-identisch (geprüft am 12.10.2026), andere Blender-Versionen können sich in einzelnen Bytes unterscheiden. Ein Neubau ohne Änderungen ist der einfachste Test, ob das eigene Setup stimmt.

**Target-Namen möglichst nicht umbenennen.** Der Code holt die Targets über den Namen. Was Nutzer sehen, steht ohnehin in `AVATAR-REGLER.md` und lässt sich dort frei ändern.

## Ganz von vorn: neuer Export aus MakeHuman

Nur nötig, wenn sich die Grundfigur selbst ändern soll (z. B. eine andere Standardfigur). Das geht nur mit MakeHuman 1.x. Ablauf und Stolperfallen: `docs/avatar/AVATAR-PIPELINE.md`. Die beiden Skripte dafür (`makehuman_export_alle_regler.py`, `blender_figuren_zu_shapekeys.py`) zeigen noch auf Christians Rechner und müssen vorher im Pfad angepasst werden. Danach die neue `avatar_shapekeys.blend` und `figur_default.obj` hier ablegen.

Die rund 550 OBJ-Einzelexporte liegen bewusst nicht im Repo (über 700 MB). Sie stecken vollständig in `werkstatt/avatar_shapekeys.blend`.

## Herkunft und Lizenz

Alle Formen stammen aus MakeHuman (Modelle und Targets unter CC0). Die Messpunkt-Nummern im Zentimeter-Skript stammen aus dem Messmodul im MakeHuman-Quellcode (`plugins/0_modeling_a_measurement.py`, Lizenz AGPL); übernommen sind nur diese Zahlenlisten.
