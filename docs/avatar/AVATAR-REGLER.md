# Avatar-Regler: Zuordnung UI ↔ Morph Targets

Stand: 12.10.2026 · Gilt für `Avatar_Editorgeruest.glb` (114 Morph Targets). Wie die Datei entsteht, steht in `AVATAR-PIPELINE.md`, warum genau diese Regler drin sind, in `REGLER-AUSWAHL.md`.

Dieses Dokument ist die verbindliche Übersetzung zwischen den Namen in der GLB-Datei (z. B. `max_gender`) und dem, was Nutzerinnen und Nutzer im Editor sehen (z. B. Regler „Geschlecht"). Wer am Editor-Code arbeitet oder neue Regler ergänzt, hält sich an diese Tabelle und trägt Änderungen hier nach.

## 1. Grundprinzip: ein UI-Regler steuert ein Min/Max-Paar

In der GLB-Datei hat fast jedes Merkmal **zwei** Morph Targets: `min_…` (Extrem in die eine Richtung) und `max_…` (Extrem in die andere). Beide stehen beim Laden auf 0, dann zeigt der Avatar genau die neutrale Standardfigur (`figur_default`).

Im Editor wird daraus **ein** Regler mit der Mitte als Neutralstellung:

```
UI-Wert v von -100 bis +100, 0 = neutral

v < 0  →  min_… = -v / 100,  max_… = 0
v > 0  →  max_… =  v / 100,  min_… = 0
v = 0  →  beide 0
```

Es sind also **nie beide** Targets eines Paares gleichzeitig größer als 0. Beispiel Geschlecht: Regler ganz nach links („weiblich") → `min_gender = 1`, `max_gender = 0`. Halb nach rechts → `min_gender = 0`, `max_gender = 0,5`.

### Technische Regeln für den Code

- **Zwei Meshes:** Die GLB enthält Körper und Augen als getrennte Meshes mit denselben 114 Target-Namen in derselben Reihenfolge. Jeder Wert muss auf **beide** Meshes gesetzt werden, sonst bleiben die Augen beim Verformen stehen.
- **Index über den Namen holen,** nie fest verdrahten: `mesh.morphTargetDictionary["max_gender"]` liefert den Index für `mesh.morphTargetInfluences`.
- **Gespeichert werden die UI-Werte,** nicht die Morph-Werte (z. B. `{ "geschlecht": -100, "gewicht": 20 }`). So bleibt das Speicherformat stabil, auch wenn wir später Targets austauschen. Das passt zum Werkstatt/Schaufenster-Prinzip in `AVATAR-3D-KONZEPT.md`.
- **Lineare Näherung:** In MakeHuman beeinflussen sich die Grundregler gegenseitig (z. B. hängt die Gewichtsform vom Geschlecht ab). Unsere Targets sind jeweils vom neutralen Avatar aus gemessen und werden einfach addiert. Für den Editor reicht das. Extreme Kombinationen, etwa Gewicht und Muskeln gleichzeitig auf Maximum, können aber leicht von MakeHuman abweichen.

## 2. Namensschema der Targets

`<richtung>_<gruppe>_<merkmal>`, abgeleitet aus dem MakeHuman-Reglernamen.

| Teil | Bedeutung |
|---|---|
| `min_` | linke Seite des MakeHuman-Namens: `decr` (kleiner/weniger), `down` (tiefer), `in` (nach innen), `backward` (nach hinten) |
| `max_` | rechte Seite: `incr` (größer/mehr), `up` (höher), `out` (nach außen), `forward` (nach vorn) |
| Gruppe | MakeHuman-Bereich, z. B. `measure`, `torso`, `hip`, `armslegs` |
| Merkmal | MakeHuman-Name ohne Gruppen-Präfix, `|` durch `-` ersetzt |

Beispiel: MakeHuman-Regler `measure/measure-waist-circ-decr|incr` → `min_measure_waist-circ-decr-incr` (Taille schmaler) und `max_measure_waist-circ-decr-incr` (Taille breiter).

Die Grundregler (`gender`, `age`, `weight` …) haben keine Gruppe im Namen. Bei Armen und Beinen sind links und rechts schon zu einem Target zusammengelegt (`armslegs_foot-scale-…` statt `l-foot`/`r-foot`).

## 3. Die UI-Regler

Spalten: **links** = Beschriftung bei −100 (`min_`-Target), **rechts** = Beschriftung bei +100 (`max_`-Target). Die Target-Namen in der letzten Spalte stehen ohne `min_`/`max_`.

### 3.1 Grundform (immer sichtbar)

| UI-Regler | links (min) | rechts (max) | Target |
|---|---|---|---|
| Geschlecht | weiblich | männlich | `gender` |
| Alter | jünger | älter | `age` |
| Gewicht | schlanker | fülliger | `weight` |
| Muskeln | weniger | mehr | `muscle` |
| Körpergröße | kleiner | größer | `height` |
| Proportionen | weniger idealisiert | idealisierter | `bodyproportions` |

**Alter begrenzen:** In MakeHuman bedeutet `age` 0 = 1 Jahr, 0,1875 = 11 Jahre, 0,5 = 25 Jahre (unser Standard), 1 = 90 Jahre. Ganz links wäre der Avatar also ein Kleinkind. Wo die linke Seite endet, entscheidet das Team noch (offen seit 12.10.2026). Vorschlag: bei etwa `min_age = 0,31`, das entspricht ungefähr 18 Jahren. Technisch ist das nur eine Grenze am Regler. Die rechte Seite reicht bis 90 Jahre.

**Proportionen:** Die genaue Wirkung von `bodyproportions` haben wir noch nicht am Modell geprüft. Die Beschriftung ist vorläufig und muss beim ersten Test im Editor bestätigt werden.

### 3.2 Maße (Bereich „Feinanpassung")

Diese Regler entsprechen den Spalten in Größentabellen. Links ist immer kleiner, schmaler oder kürzer, rechts größer, breiter oder länger.

| UI-Regler | Target | wichtig für |
|---|---|---|
| Brustumfang | `measure_bust-circ-decr-incr` | Oberteile, Kleider |
| Unterbrustumfang | `measure_underbust-circ-decr-incr` | BHs, Oberteile |
| Taillenumfang | `measure_waist-circ-decr-incr` | alles |
| Hüftumfang | `measure_hips-circ-decr-incr` | Hosen, Röcke, Kleider |
| Halsumfang | `measure_neck-circ-decr-incr` | Hemden (Kragenweite) |
| Halslänge | `measure_neck-height-decr-incr` | Kragen |
| Schulterbreite | `measure_shoulder-dist-decr-incr` | Oberteile, Jacken |
| Brustbreite vorn | `measure_frontchest-dist-decr-incr` | Oberteile |
| Rückenlänge (Nacken bis Taille) | `measure_napetowaist-dist-decr-incr` | Oberteile, Kleider |
| Abstand Taille bis Hüfte | `measure_waisttohip-dist-decr-incr` | Hosen, Röcke |
| Oberarmumfang | `measure_upperarm-circ-decr-incr` | Ärmel |
| Oberarmlänge | `measure_upperarm-length-decr-incr` | Ärmellänge |
| Unterarmlänge | `measure_lowerarm-length-decr-incr` | Ärmellänge |
| Handgelenkumfang | `measure_wrist-circ-decr-incr` | Bündchen |
| Oberschenkelumfang | `measure_thigh-circ-decr-incr` | Hosen |
| Knieumfang | `measure_knee-circ-decr-incr` | Hosen, Stiefel |
| Wadenumfang | `measure_calf-circ-decr-incr` | Hosen, Stiefel |
| Knöchelumfang | `measure_ankle-circ-decr-incr` | Schuhe, Socken |
| Oberschenkellänge | `measure_upperleg-height-decr-incr` | Hosenlänge |
| Unterschenkellänge | `measure_lowerleg-height-decr-incr` | Hosenlänge |

### 3.3 Körperform (Bereich „Feinanpassung")

| UI-Regler | links (min) | rechts (max) | Target |
|---|---|---|---|
| Oberkörper Breite | schmaler | breiter | `torso_scale-horiz-decr-incr` |
| Oberkörper Tiefe | flacher | tiefer | `torso_scale-depth-decr-incr` |
| Oberkörper Länge | kürzer | länger | `torso_scale-vert-decr-incr` |
| V-Form | weniger | mehr | `torso_vshape-decr-incr` |
| Brustmuskeln | weniger | mehr | `torso_muscle-pectoral-decr-incr` |
| Rückenmuskeln | weniger | mehr | `torso_muscle-dorsi-decr-incr` |
| Hüfte Breite | schmaler | breiter | `hip_scale-horiz-decr-incr` |
| Hüfte Tiefe | flacher | tiefer | `hip_scale-depth-decr-incr` |
| Hüfte Höhe | niedriger | höher | `hip_scale-vert-decr-incr` |
| Taillenhöhe | tiefer | höher | `hip_waist-down-up` |
| Bauch | flacher | runder | `stomach_pregnant-decr-incr` |
| Po | kleiner | größer | `buttocks_volume-decr-incr` |
| Brustgröße | kleiner | größer | `breast_breastsize` |
| Brustform | weicher | fester | `breast_breastfirmness` |

### 3.4 Arme, Beine, Füße (Bereich „Feinanpassung")

| UI-Regler | links (min) | rechts (max) | Target |
|---|---|---|---|
| Fußgröße | kleiner | größer | `armslegs_foot-scale-decr-incr` |
| Oberarme | schlanker | kräftiger | `armslegs_upperarm-fat-decr-incr` |
| Oberschenkel | schlanker | kräftiger | `armslegs_upperleg-fat-decr-incr` |
| Unterschenkel | schlanker | kräftiger | `armslegs_lowerleg-fat-decr-incr` |
| Beinstellung | O-Beine | X-Beine | `armslegs_leg-valgus-decr-incr` |
| Oberschenkel-Länge | kürzer | länger | `armslegs_upperlegs-height-decr-incr` |
| Unterschenkel-Länge | kürzer | länger | `armslegs_lowerlegs-height-decr-incr` |

### 3.5 Figurtyp (Schnellauswahl)

Die 20 Figurtypen gibt es nur als `max_`. Es sind fertige Körperform-Mischungen. Im Editor ist das eine Auswahl (Kacheln oder Dropdown) plus ein Stärke-Regler von 0 bis 100, und es ist immer nur ein Figurtyp aktiv. Die `frau_`-Typen stehen bei der weiblichen, die `mann_`-Typen bei der männlichen Seite des Geschlechtsreglers. Der Editor zeigt je nach Geschlechtsregler zuerst den passenden Satz. „Hüftbetont" erscheint in beiden Sätzen. Für füllige Figuren lassen sich die Typen mit dem Gewichtsregler kombinieren.

Auswahl, Umbenennung und das Aussortieren von `adrenal` hat Christian am 12.10.2026 entschieden. Vorschaubilder und Begründung stehen in `FIGURTYPEN.md`.

| Target | Anzeige | Bild | ursprünglicher MakeHuman-Name (`bodyshapes/…`) |
|---|---|---|---|
| `max_figur_frau_apfel` | Apfel | Mitte fülliger, Beine schlank | `elvs-fem-apple` |
| `max_figur_frau_birne` | Birne | Hüfte breiter als Schultern | `elvs-fem-triangle` |
| `max_figur_frau_birne-kraeftig` | Birne, kräftig | breite Hüften, kräftige Oberschenkel | `elvs-fem-ovary` |
| `max_figur_frau_sanduhr-kurvig` | Sanduhr, kurvig | schmale Taille, kurvige Brust und Hüfte | `elvs-fem-full-hourglass` |
| `max_figur_frau_sanduhr-schlank` | Sanduhr, schlank | wie oben, schlanker | `elvs-fem-neat-hourglass` |
| `max_figur_frau_v-form` | V-Form | Schultern betont, Hüfte schmal | `elvs-fem-invert-triangle` |
| `max_figur_frau_rechteck` | Rechteck | Taille kaum betont | `elvs-fem-rectangle` |
| `max_figur_frau_raute` | Raute | Mitte und Hüfte etwas breiter, Schultern schmal | `elvs-fem-diamond` |
| `max_figur_frau_saeule` | Schlanke Säule | schlank, gerade | `elvs-fem-lean-column` |
| `max_figur_frau_bauchbetont` | Bauchbetont | runder Bauch, sonst schlank | `elvs-fem-liver` |
| `max_figur_frau_vollschlank` | Vollschlank | rundum füllig | `elvs-fem-thyroid` |
| `max_figur_mann_apfel` | Apfel | Bauch und Brust fülliger | `elvs-man-apple` |
| `max_figur_mann_birne` | Birne | Hüfte breiter als Schultern | `elvs-man-triangle` |
| `max_figur_mann_hueftbetont` | Hüftbetont (für beide Geschlechter) | Hüfte und Oberschenkel weicher | `elvs-man-gonadal` |
| `max_figur_mann_v-form` | V-Form | breite Schultern, schmale Hüfte | `elvs-man-invert-triangle` |
| `max_figur_mann_trapez` | Trapez (athletisch) | breite Schultern, mittlere Taille | `elvs-man-trapezoid` |
| `max_figur_mann_rechteck` | Rechteck | gerade, Taille kaum abgesetzt | `elvs-man-rectangle` |
| `max_figur_mann_saeule` | Schlanke Säule | schlank, gerade | `elvs-man-lean-column` |
| `max_figur_mann_bauchbetont` | Bauchbetont | runder Bauch | `elvs-man-liver` |
| `max_figur_mann_vollschlank` | Vollschlank | sehr füllig, großer Bauch | `elvs-man-thyroid` |

Aussortiert, aber in `Avatar_Aussehen_spaeter.blend` erhalten: `elvs-fem-adrenal` und `elvs-man-adrenal` (wirken unnatürlich). Die ursprünglichen Namen der übrigen Typen stammen aus einem unwissenschaftlichen „Drüsentyp"-Modell (adrenal, liver, ovary, thyroid, gonadal) und dürfen in der App nicht auftauchen.

## 4. Verknüpfte Regler

Ein UI-Regler darf mehrere Targets gleichzeitig bewegen. Das kostet keinen Speicher, weil nur Werte gesetzt werden. Jede Verknüpfung wird hier mit Gewichtung eingetragen, damit klar bleibt, was ein Regler wirklich tut.

| UI-Regler | bewegt | Status |
|---|---|---|
| Geschlecht | `gender` | entschieden (Christian, 12.10.2026) |
| Gesamtumfang | alle Umfang-Maße aus 3.2 (bust, underbust, waist, hips, neck-circ, upperarm-circ, wrist, thigh, knee, calf, ankle) je mit Gewicht 1,0 | Vorschlag, im Editor testen |

Weitere Verknüpfungen, etwa Geschlecht mit Brustgröße oder passendem Figurtyp, sind ausdrücklich erwünscht. Sie kommen aber erst in diese Tabelle, wenn das Team sie beschlossen hat.

## 5. Offen

- **Zentimeter-Zuordnung:** Welcher Morph-Wert entspricht wie vielen Zentimetern, z. B. Taillenumfang bei `max_…waist… = 1`? Das ist nötig für die Passform-Bewertung gegen Größentabellen und wird am Modell nachgemessen.
- Beschriftung von `bodyproportions` am Modell prüfen.
- Aussehen (Gesicht, Kopf, Hände) liegt in `Avatar_Aussehen_spaeter.blend` und bekommt später eine eigene Tabelle hier.
