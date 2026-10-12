# Figur: Vorschlag für das Datenmodell

Stand: 12.10.2026 · Vorschlag von Christian/Claude(Laptop.Code) als Vorlage für das Datenbankmodell. Die Felder leiten sich aus `AVATAR-REGLER.md` ab. Wer das Datenbankmodell erstellt, kann den Vorschlag übernehmen oder anpassen. Änderungen bitte hier und in `AVATAR-REGLER.md` nachziehen.

## Entschieden (Christian, 12.10.2026)

- Ein Nutzer kann **0 bis 3 Figuren** anlegen. Eine Figur ist freiwillig. Die Obergrenze 3 kann sich noch ändern, deshalb wird sie im Backend geprüft und nicht fest ins Schema geschrieben.
- Die Figuren liegen in einer eigenen Collection `figuren`. Jedes Dokument verweist über `nutzer_id` auf seinen Nutzer.
- Figuren sind nur nach Login abrufbar. Ein Nutzer sieht ausschließlich seine eigenen Figuren.

## Grundsatz: gespeichert werden nur Reglerwerte

Die 3D-Datei `Avatar_Editorgeruest.glb` ist für alle Nutzer gleich und liegt nicht in der Datenbank. Pro Figur speichern wir nur die Stellung der UI-Regler, jeweils als ganze Zahl von −100 bis +100. 0 bedeutet neutral. Der Editor lädt die GLB und rechnet die Werte nach `AVATAR-REGLER.md` Abschnitt 1 in Morph-Werte um. Damit ist eine Figur nur wenige hundert Byte groß. Morph-Werte und 3D-Daten werden nicht gespeichert.

Fehlt ein Regler im Dokument, gilt er als 0. So bleiben alte Figuren gültig, wenn später neue Regler dazukommen.

## Dokument `figuren`

| Feld | Typ | Pflicht | Bedeutung |
|---|---|---|---|
| `_id` | ObjectId | ja | von MongoDB vergeben |
| `nutzer_id` | ObjectId | ja | Verweis auf den Nutzer, mit Index |
| `name` | String | ja | vom Nutzer vergeben, z. B. „Ich im Sommer" |
| `regler_version` | Int | ja | Version der Regler-Zuordnung, aktuell `1`. Ändert sich die GLB so, dass alte Werte anders wirken, wird hochgezählt und umgerechnet. |
| `regler` | Objekt | ja | Reglerwerte −100 bis +100, Schlüssel siehe unten |
| `figurtyp` | Objekt oder `null` | nein | `{ "typ": "frau_sanduhr-kurvig", "staerke": 40 }`, `staerke` 0 bis 100. Es ist immer höchstens ein Typ aktiv. |
| `erstellt_am` | Date | ja | |
| `geaendert_am` | Date | ja | |

Beispiel:

```json
{
  "nutzer_id": "ObjectId(...)",
  "name": "Meine Figur",
  "regler_version": 1,
  "regler": { "geschlecht": -80, "koerpergroesse": 15, "taillenumfang": -20, "fussgroesse": 5 },
  "figurtyp": { "typ": "frau_sanduhr-kurvig", "staerke": 40 },
  "erstellt_am": "2026-10-12T14:30:00Z",
  "geaendert_am": "2026-10-12T14:30:00Z"
}
```

## Schlüssel in `regler` (47 Stück)

Die Schlüssel sind kleingeschrieben, ohne Umlaute und mit `_` getrennt. Rechts steht das Target aus `AVATAR-REGLER.md`, jeweils ohne `min_`/`max_`.

**Grundform (6):** `geschlecht` (gender), `alter` (age), `gewicht` (weight), `muskeln` (muscle), `koerpergroesse` (height), `proportionen` (bodyproportions)

**Maße (20):** `brustumfang` (bust-circ), `unterbrustumfang` (underbust-circ), `taillenumfang` (waist-circ), `hueftumfang` (hips-circ), `halsumfang` (neck-circ), `halslaenge` (neck-height), `schulterbreite` (shoulder-dist), `brustbreite_vorn` (frontchest-dist), `rueckenlaenge` (napetowaist-dist), `abstand_taille_huefte` (waisttohip-dist), `oberarmumfang` (upperarm-circ), `oberarmlaenge` (upperarm-length), `unterarmlaenge` (lowerarm-length), `handgelenkumfang` (wrist-circ), `oberschenkelumfang` (thigh-circ), `knieumfang` (knee-circ), `wadenumfang` (calf-circ), `knoechelumfang` (ankle-circ), `oberschenkellaenge_mass` (measure upperleg-height), `unterschenkellaenge_mass` (measure lowerleg-height)

**Körperform (14):** `oberkoerper_breite`, `oberkoerper_tiefe`, `oberkoerper_laenge`, `v_form`, `brustmuskeln`, `rueckenmuskeln`, `huefte_breite`, `huefte_tiefe`, `huefte_hoehe`, `taillenhoehe`, `bauch`, `po`, `brustgroesse`, `brustform`

**Arme, Beine, Füße (7):** `fussgroesse`, `oberarme`, `oberschenkel`, `unterschenkel`, `beinstellung`, `oberschenkel_laenge`, `unterschenkel_laenge`

Zuordnung zu den Targets in derselben Reihenfolge wie in `AVATAR-REGLER.md` 3.3 und 3.4. Die Längen gibt es doppelt (einmal aus `measure_`, einmal aus `armslegs_`), deshalb tragen die `measure_`-Varianten den Zusatz `_mass`.

**Figurtyp-Schlüssel (20):** wie die Target-Namen in `AVATAR-REGLER.md` 3.5 ohne `max_figur_`, z. B. `frau_apfel`, `mann_trapez`.

## Was bewusst nicht gespeichert wird

- **Verknüpfte Regler** wie „Gesamtumfang" (`AVATAR-REGLER.md` 4) sind Bedienhilfen. Sie verschieben die einzelnen Maß-Regler, gespeichert werden nur deren Werte.
- **Zentimeter-Werte** (Taille 74 cm …) werden aus den Reglern berechnet, sobald die cm-Zuordnung feststeht (offen, siehe `AVATAR-REGLER.md` 5). Ob wir sie zusätzlich zwischenspeichern, etwa für schnelle Passform-Abfragen, entscheidet das Team mit dem Datenbankmodell.
- **Aussehen** (Gesicht, Haare, Hautfarbe) kommt später. Dafür ist ein zweites Objekt `aussehen` neben `regler` vorgesehen, damit das bestehende Format nicht umgebaut werden muss.

## Noch offen fürs Team

- Ob die Altersgrenze (offen, `AVATAR-REGLER.md` 3.1) gespeicherte Werte begrenzt: Das Backend sollte Werte außerhalb der erlaubten Spanne ablehnen.
- Welche Figur bei mehreren für die Passform-Bewertung gilt: z. B. ein Feld `standard: true` an einer Figur oder ein Verweis im Nutzer-Dokument.
- **Datenschutz:** Körpermaße sind personenbezogene Daten. Beim Löschen des Kontos werden alle Figuren mitgelöscht. Das Datenmodell sollte das als Regel nennen.
