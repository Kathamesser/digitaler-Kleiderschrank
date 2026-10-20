# Zentimeter-Werte des Avatars

Stand: 12.10.2026 · Gilt für `Avatar_Editorgeruest.glb` (114 Targets). Erstellt von Christian/Claude(Laptop.Code) auf Christians Wunsch: Die Zentimeter-Zuordnung wird jetzt festgelegt, weil die Werte des Modells realistischen Körpermaßen entsprechen (Prüfung in Abschnitt 3).

## 1. Grundsatz: Maße werden am Modell gemessen, nicht umgerechnet

Wir legen **keine feste Formel „Reglerwert → cm"** fest. Der Editor misst die Zentimeter direkt an der aktuell verformten Figur, mit denselben Messbändern, die MakeHuman für seine Maß-Regler verwendet. Das hat drei Vorteile:

- Das Ergebnis stimmt auch, wenn mehrere Regler zusammenwirken (z. B. Geschlecht, Gewicht und Taille). Eine Tabelle pro Regler könnte das nur schätzen.
- Was der Nutzer sieht und was in der Passform-Bewertung landet, ist garantiert dasselbe.
- In der Datenbank müssen keine cm-Werte stehen. Sie entstehen aus den gespeicherten Reglerwerten (siehe `FIGUR-DATENMODELL.md`).

## 2. Die Dateien

| Datei | Inhalt |
|---|---|
| `messpunkte.json` | 24 Messbänder als Vertex-Indizes der GLB (Körper-Mesh) und als MakeHuman-Vertex-Nummern, dazu die cm-Werte der Standardfigur und die Wirkung jedes Targets in cm |
| `ZENTIMETER-TABELLE.md` | dieselben Zahlen zum Lesen: Standardfigur und Wirkung jedes Targets auf die wichtigsten Maße |
| `skripte/zentimeter_messen.py` | erzeugt beide Dateien aus `Sharely_programm/assets/avatar/Avatar_Editorgeruest.glb` und `Sharely_programm/assets/avatar/werkstatt/figur_default.obj`. Aufruf im Repo-Ordner: `python docs/avatar/skripte/zentimeter_messen.py`. **Wird die GLB neu gebaut, muss das Skript erneut laufen**, weil sich die Vertex-Reihenfolge der GLB ändern kann. |

### Wie gemessen wird

- **Umfänge** (Brust, Taille, Hüfte …): Die Punkte eines Messbands liegen rund um den Körper. Gemessen wird die konvexe Hülle in der Ebene des Bands, also so, wie ein straff angelegtes Maßband misst. Es überbrückt Einbuchtungen, etwa zwischen den Brüsten. MakeHuman selbst addiert stattdessen die Abstände entlang der Punkte. Bei einigen Bändern, die nicht geschlossen sind (Brust, Unterbrust, Oberarm), weicht das bis zu 1,8 cm ab. Die Maßband-Methode entspricht dem, wie Größentabellen messen.
- **Längen** (Oberarm, Rückenlänge …): Abstand zwischen den MakeHuman-Messpunkten.
- **Körpergröße:** vom tiefsten bis zum höchsten Punkt des Körpers, ohne Haare und ohne Schuhe.
- **Schrittlänge (Innenbein)**, neu, für Hosen: Höhe des tiefsten Punkts im Schritt über dem Boden.
- **Fußlänge**, neu, für Schuhe: Abstand Ferse bis Zehenspitze in Laufrichtung, linker Fuß.
- **Schulterbreite über den Rücken** (`schulterbreite_ruecken`), neu seit 20.10.2026, für Oberteile, Jacken und Kleider: vom rechten Schulterpunkt über den Rücken zum linken, gemessen wie ein straff gespanntes Maßband (Art `bogen`: konvexe Hülle der Punkte minus der geraden Verbindung der beiden Schulterpunkte). So misst man auch Kleidung von Naht zu Naht. Das MakeHuman-Band `shoulder-dist` misst nur eine Seite vom Hals bis zur Schulter und bleibt nur für den Regler.
- **Armlänge** (`armlaenge`), neu seit 20.10.2026, für die Ärmellänge: Schulterpunkt über den Ellbogen bis zum Handgelenk. Ersetzt die Summe aus Ober- und Unterarmlänge, deren Bänder am Ellbogen nicht aneinander anschließen.

Grundsatz (Christian, 20.10.2026): Alle Maße werden rundum am 3D-Körper genommen, nicht als Breite von vorn. Umfänge laufen ganz um den Körper, Breiten folgen der Wölbung des Körpers.

## 3. Realitätsprüfung

Verglichen mit Größentabellen aus dem Handel ([Lidl Damen](https://www.lidl.de/c/lidl-groessentabelle/s10005239), [Lidl Herren](https://www.lidl.de/c/groessenrechner-herren/s10048945)) und der Durchschnittsgröße in Deutschland bei 18- bis 25-Jährigen (Frauen 166 cm, Männer 180 cm, [laenderdaten.info](https://www.laenderdaten.info/durchschnittliche-koerpergroessen.php)).

| Figur | Größe | Brust | Unterbrust | Taille | Hüfte | Hals | passt zu |
|---|---|---|---|---|---|---|---|
| Geschlecht −100 (weiblich), sonst neutral | 159,0 | 82,4 | 67,8 | 70,0 | 92,5 | 28,1 | Damen 36 (Tabelle: 82–86 / 67–71 / 91–95) |
| Geschlecht +100 (männlich), sonst neutral | 173,0 | 91,9 | 83,5 | 75,4 | 91,6 | 37,2 | Herren 46 bei Brust und Taille (90–94 / 75–80), Hüfte etwas schmaler (95–98) |
| weiblich, Gewicht +100 | 159,0 | 86,2 | 72,6 | 79,4 | 99,7 | 28,2 | Damen 40–42 |
| weiblich, Gewicht und Maße Brust, Taille, Hüfte −100 | 159,0 | 66,5 | 55,9 | 53,4 | 77,3 | 27,1 | sehr schlank, unter Damen 32 |
| weiblich, Gewicht und Maße +100, Figurtyp „Vollschlank" | 159,0 | 122,3 | 108,7 | 122,2 | 140,7 | 35,8 | weit über Damen 50 |
| männlich, Gewicht und Maße +100, Figurtyp „Vollschlank" | 173,0 | 117,9 | 111,9 | 122,9 | 131,7 | 41,5 | weit über Herren 56 |

**Ergebnis:** Die Standardfiguren entsprechen schlanken, aber realistischen Erwachsenen (Damen 36, Herren 46). Mit Gewicht, Maß-Reglern und Figurtypen lässt sich der ganze Bereich der Konfektionsgrößen abdecken. Zwei Abweichungen gibt es:

- **Körpergröße:** Beide Standardfiguren sind kleiner als der Durchschnitt (159 statt 166 cm, 173 statt 180 cm). Das gleicht der Größen-Regler aus: etwa +10 ergibt rund +7 cm.
- **Fußlänge:** weiblich 21,2 cm, männlich 26,0 cm. Das wirkt eher klein (Einschätzung von Claude, nicht gegen eine Quelle geprüft). Der Fußgrößen-Regler reicht von −4,7 bis +7,4 cm.

Die Figur reagiert gleichmäßig auf die Regler: Der Taillen-Regler in Viertel-Schritten ergibt 72,4 → 74,9 → 77,5 → 80,0 → 82,6 cm. Zwischenwerte sind also verlässlich.

## 4. Grenzen der Regler (Vorschlag, im Team zu entscheiden)

Einige Grundregler reichen weit über Erwachsenen-Maße hinaus, weil MakeHuman auch Kinder und Riesen abbildet:

| Regler | Wirkung bei −100 | Wirkung bei +100 | Vorschlag |
|---|---|---|---|
| Körpergröße | −36,7 cm | +72,3 cm | auf −40 bis +45 begrenzen, das ergibt etwa 144 bis 205 cm über beide Geschlechter |
| Alter | −105,8 cm (Kleinkind) | −2,2 cm | Untergrenze ist ohnehin offen (`AVATAR-REGLER.md` 3.1) |

Die Wirkung ist nicht symmetrisch: Bei der Körpergröße ist ein Schritt nach rechts etwa doppelt so groß wie ein Schritt nach links. Die Grenzen sollten deshalb in cm gedacht und dann in Reglerwerte umgerechnet werden.

## 5. Umsetzung im Editor

### Messen

Three.js verformt die Figur auf der Grafikkarte. Für die Messung rechnet der Editor die wenigen Punkte eines Messbands selbst aus: Grundposition plus Summe aus Morph-Wert mal Target-Verschiebung. glTF speichert die Targets als Verschiebungen, deshalb gilt `morphTargetsRelative = true`.

```js
// band = messpunkte.masse["waist-circ"]; mesh = Körper-Mesh (erstes Primitive der GLB)
function punkt(mesh, i) {
  const g = mesh.geometry, p = new THREE.Vector3().fromBufferAttribute(g.attributes.position, i);
  g.morphAttributes.position.forEach((attr, t) => {
    const w = mesh.morphTargetInfluences[t];
    if (w) p.addScaledVector(new THREE.Vector3().fromBufferAttribute(attr, i), w);
  });
  return p;
}
function messeCm(mesh, band) {
  const pts = band.glb_vertices.map(i => punkt(mesh, i));
  if (band.art === "laenge") return 100 * pts.slice(1).reduce((s, p, k) => s + p.distanceTo(pts[k]), 0);
  if (band.art === "hoehe_punkt") return 100 * (pts[0].y - bodenY(mesh));   // bodenY: tiefster Punkt der Figur
  if (band.art === "fuss") return 100 * Math.abs(pts[1].z - pts[0].z);
  if (band.art === "bogen") return 100 * (huellenUmfang(pts) - pts[0].distanceTo(pts[pts.length - 1]));
  return 100 * huellenUmfang(pts);   // "umfang": konvexe Hülle in der Bandebene, wie im Python-Skript
}
```

`huellenUmfang` entspricht `hull_perimeter` in `skripte/zentimeter_messen.py`: die Punkte in ihre Hauptebene projizieren, konvexe Hülle bilden, Umfang addieren. Für die Körpergröße und `bodenY` reicht die Bounding Box der verformten Figur.

### Eingabe in cm

Gibt ein Nutzer ein Maß direkt ein (z. B. „Taille 80 cm"), rechnet der Editor den Reglerwert aus:

1. Steigung aus `messpunkte.json` → `wirkung_je_target_cm` nehmen, z. B. `max_measure_waist-circ-decr-incr` = +10,2 cm pro 100.
2. Reglerwert um (Ziel − aktuell) / Steigung × 100 verschieben, je nach Richtung mit der `min_`- oder `max_`-Steigung.
3. Neu messen und Schritt 2 noch ein- oder zweimal wiederholen, bis die Abweichung unter 0,5 cm liegt.

Gespeichert wird danach wie immer nur der Reglerwert.

## 6. Bewusst nicht gelöst

- Die Messbänder hängen an festen Vertices. Bei extremen Kombinationen kann ein Band leicht schräg liegen, etwa wenn die Taillenhöhe stark verschoben ist. Für die Passform-Ampel („passt/eng/weit") ist das genau genug.
- Maße, für die es kein Messband gibt (Kopfumfang, Fußbreite), kommen bei Bedarf als neue Einträge in `EXTRA` im Skript dazu.
