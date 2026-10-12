# Avatar-Pipeline: von MakeHuman zur GLB-Datei

Stand: 12.10.2026 · Umsetzung des Konzepts aus `AVATAR-3D-KONZEPT.md` (Werkstatt/Schaufenster). Die Arbeitsdateien liegen auf Christians Rechner unter `Abschlussprojekt\Avatar-Editor_Datein\`, die Skripte zusätzlich hier in `skripte/`.

## Ergebnis

| Datei | Inhalt |
|---|---|
| `Figuren\Avatar_Editorgeruest.glb` | Web-Avatar für Three.js: neutrale Standardfigur plus 116 Morph Targets (Auswahl: `REGLER-AUSWAHL.md`, Bedeutung: `AVATAR-REGLER.md`). 8 MB, komprimiert etwa 3 MB. Alle Targets starten auf 0. |
| `Figuren\Avatar_Aussehen_spaeter\` | `.blend` mit den übrigen 421 Shape Keys (Gesicht, Kopf, Hände, Herkunft …) plus Namensliste, für später |
| `Figuren\avatar_shapekeys.blend` | Zwischenstand mit allen 547 Shape Keys |
| `Figuren\Formsammlung\` | 554 MakeHuman-Exporte (OBJ und MTL), je Regler eine Min- und eine Max-Figur |
| `Figuren\_export_liste.txt` | Zuordnung Datei → MakeHuman-Regler und Wert |

## Ablauf

1. **MakeHuman**, Standardfigur einstellen. Export-Optionen: Wavefront OBJ, Meter, Feet on Ground an, Normals aus, Helper geometry aus.
2. `skripte/makehuman_export_alle_regler.py` in MakeHuman über Utilities > Shell ausführen. Vorher unter Settings > Plugins die Plugins `7_scripting` und `7_shell` aktivieren. Das Skript stellt jeden Regler einzeln auf Min und Max, lädt dazwischen die Ausgangsfigur neu (statt Reset, weil Reset die Augen entfernt) und exportiert als `figur_min_<regler>` und `figur_max_<regler>`.
3. **Blender:** `skripte/blender_figuren_zu_shapekeys.py` im Scripting-Tab ausführen. Es liest nur die Vertex-Positionen der OBJ-Dateien, statt jede Datei zu importieren und „Join as Shapes" zu benutzen, und erzeugt `avatar_shapekeys.blend`. Regler ohne Wirkung werden übersprungen (6 Genital-Regler, weil die Standardfigur dort keine Geometrie hat).
4. `skripte/blender_editorgeruest_bauen.py` erzeugt aus der .blend die GLB-Datei mit der Auswahl und den Ordner für später.

## Stolperfallen (gelöst)

- **Gleiche Vertex-Zahl ist Pflicht:** Alle Exporte müssen mit identischen Optionen entstehen. Alle 554 Dateien haben 14.444 Vertices und 14.398 Faces.
- **Blender 5 dreht beim OBJ-Import das Objekt,** statt die Koordinaten umzurechnen. Das Skript erkennt beide Varianten.
- **Flache Schattierung vervierfacht die GLB-Größe,** weil der Export jede Fläche in eigene Vertices teilt. Deshalb wird vor dem Export glatt schattiert.
- **Startwerte der Targets:** Die erste GLB hatte alle 116 Werte auf 1, die Figur war dadurch völlig verformt. Das Skript setzt jetzt alle Werte auf 0.
