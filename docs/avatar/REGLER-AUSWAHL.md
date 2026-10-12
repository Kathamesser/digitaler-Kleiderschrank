# Regler-Auswahl für den Web-Avatar (Vorschlag)

Stand: 12.10.2026 · Ziel: alle Körperstellen abdecken, die für die Passform von Oberteilen, Hosen, Kleidern und Schuhen zählen. Kopf und Gesicht kommen nicht hinein.

Wenn bei einem Regler nichts anderes steht, kommt er mit Min und Max hinein, also mit 2 Shape Keys.

## 1. Grundform (6 Regler, 12 Keys)
| Regler | Wofür |
|---|---|
| Gender | Grundkörper weiblich ↔ männlich |
| Age | Körperbau jung ↔ alt |
| Weight | Gesamtumfang (alle Größen) |
| Muscle | Muskelmasse (Schultern, Arme, Oberschenkel) |
| Height | Körpergröße (Längen-Größen, z. B. Langgrößen) |
| BodyProportions | Verhältnis Beine zu Oberkörper |

## 2. Maße aus Größentabellen (alle 20 `measure`-Regler, 40 Keys)
Diese Regler sind am wichtigsten, weil sie 1:1 den Spalten in Größentabellen entsprechen.

| Kleidung | Regler |
|---|---|
| Oberteile, Kleider | Brustumfang (bust), Unterbrustumfang (underbust), Taillenumfang (waist), Halsumfang (neck-circ), Halshöhe (neck-height), Schulterbreite (shoulder-dist), Brustbreite vorn (frontchest-dist), Rückenlänge Nacken bis Taille (napetowaist-dist) |
| Ärmel | Oberarmumfang (upperarm-circ), Oberarmlänge (upperarm-length), Unterarmlänge (lowerarm-length), Handgelenk (wrist-circ) |
| Hosen, Röcke, Kleider | Hüftumfang (hips-circ), Taille bis Hüfte (waisttohip-dist), Oberschenkelumfang (thigh-circ), Knieumfang (knee-circ), Wadenumfang (calf-circ), Oberschenkellänge (upperleg-height), Unterschenkellänge (lowerleg-height) |
| Schuhe, Socken | Knöchelumfang (ankle-circ) |

## 3. Körperform-Feinheiten (14 Regler, 28 Keys)
| Bereich | Regler | Wofür |
|---|---|---|
| Rumpf | torso-scale-horiz, torso-scale-depth, torso-scale-vert, torso-vshape, torso-muscle-pectoral, torso-muscle-dorsi | Schnitt von Shirts und Jacken (Breite, Tiefe, V-Form, Brust- und Rückenmuskeln) |
| Hüfte | hip-scale-horiz, hip-scale-depth, hip-scale-vert, hip-waist-down/up | Sitz von Hosen und Röcken, Höhe der Taille |
| Bauch | stomach-pregnant | Bauchumfang, auch für Umstandsmode |
| Po | buttocks-volume | Sitz von Hosen |
| Brust | BreastSize, BreastFirmness | Oberteile, Kleider, BHs |

## 4. Arme, Beine und Füße (7 Regler, 14 Keys)
Links und rechts werden in Blender zu einem gemeinsamen Shape Key zusammengelegt. Das spart die Hälfte der Keys, und der Avatar bleibt symmetrisch.

| Regler | Wofür |
|---|---|
| foot-scale (l+r) | Fußgröße, daraus wird die Schuhgröße berechnet |
| upperarm-fat (l+r) | Ärmelweite |
| upperleg-fat (l+r) | Hosenbein oben |
| lowerleg-fat (l+r) | Hosenbein unten, Stiefelschaft |
| leg-valgus (l+r) | X- oder O-Beine, beeinflusst den Fall der Hose |
| upperlegs-height / lowerlegs-height | Beinlänge, also Innenbeinlänge der Hose |

## 5. Optional: Figurtypen (22 Keys, jeweils nur Max)
Die `bodyshapes` (z. B. Apfel, Sanduhr, Dreieck, V-Form, getrennt nach Frau und Mann) sind fertige Mischungen. Sie eignen sich als Schnellauswahl „Figurtyp“ im Editor, bevor man an einzelnen Maßen feilt.

## Nicht enthalten
Gesicht und Kopf (Ohren, Nase, Mund, Augen, Wangen, Kinn, Stirn, Kopfform), Hände und Finger, Genitalien, Herkunft (die Hautfarbe läuft besser über das Material), reine Verschiebungen (`trans-*`) und Detailregler wie die Brustwarzen.

Kopf und Gesicht kann man später als eigenen kleinen „Aussehen“-Satz ergänzen, z. B. 5 bis 10 Regler.

## Umfang
Ohne Figurtypen sind es 94 Shape Keys, mit Figurtypen 116. Umgesetzt mit Figurtypen: Die GLB-Datei ist 8 MB groß, als Download komprimiert etwa 3 MB. Mit allen 547 Keys wären es über 100 MB.
