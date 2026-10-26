# Zugaben für die Passform

Stand: 26.10.2026 · Christian/Claude(Laptop.Code) · **Startwerte entschieden von Christian (26.10.2026), werden nach Tests mit echten Teilen angepasst.** Die gültigen Zahlen stehen im Code: `Sharely_programm/backend/app/core/wertelisten.py` → `MESSPUNKTE_JE_KLEIDUNGSART`, in der Datenbank an `kleidungsarten.messpunkte`.

## 1. Worum es geht

Die Passform vergleicht je Messpunkt das Maß des Kleidungsstücks mit dem Maß der Figur. Ein Teil muss größer sein als der Körper, sonst kann man sich darin nicht bewegen (Bewegungszugabe). Wie viel größer, hängt von Kleidungsart und Messpunkt ab. Diese Spanne nennen wir **Zugabe**.

## 2. Was die Recherche ergeben hat

| Quelle | Aussage |
|---|---|
| [Europa-Lehrmittel, Konstruktionstabelle Shirt](https://www.europa-lehrmittel.de/media/8a/e8/6e/1756301265/Konstruktionstabelle%20Shirt.pdf) | Passform in 11 Klassen: Brustumfang 0 bis 20 cm Zugabe, Taille 0 bis 24 cm, Hüfte 0 bis 24 cm. Klasse 0 = hauteng, Klasse 10 = sehr weit. |
| [VHS Hamburg, Kleiderschnitt](https://www.vhs-hamburg.de/sites/default/files/user-generated/editor/161701/Kleiderschnitt.pdf) | Brustumfang gesamt: Kleid eng +5 cm, Kleid normal +8 cm, Hemdbluse +12 cm |
| [Love Notions, Ease](https://lovenotions.com/?p=577818) | Mindestzugabe bei Webware: Brust ca. 5 cm, Taille ca. 2,5 cm, Hüfte ca. 4 cm. Strickware darf kleiner sein als der Körper (negative Zugabe, ca. −2,5 bis −12 cm an der Brust). |
| [Threads, Forum „Ease“](https://www.threadsmagazine.com/forum/ease) | Oberarm: Bluse +2,5 bis 4 cm, Kleid +4 bis 5 cm, Jacke +7,5 bis 11 cm, Mantel +10 bis 14 cm. Größere Größen brauchen mehr Zugabe. |
| [Cashmerette, Negative Ease](https://blog.cashmerette.com/2019/02/what-is-negative-ease-and-how-does-it-work.html) | Leggings ca. 20 % kleiner als der Körper, eng anliegendes Kleid ca. 3 % kleiner |
| [Haflinger, Pariser Stich](https://haflinger.com/en/blogs/news/schuhgroessee-berechnen-mit-dem-pariser-stich) | Schuh-Innenlänge = Fußlänge + 1,5 cm; EU-Größe = (Fußlänge + 1,5) × 1,5 |

Daraus folgen zwei Erkenntnisse:
- Die Zugabe wächst mit der Körpergröße. Deshalb rechne ich **Umfänge in Prozent** des Körpermaßes, **Längen in cm**.
- Dehnbare Stoffe (Jersey, Strick, Elasthan) brauchen weniger oder sogar negative Zugabe. Das berücksichtigt der Startvorschlag noch nicht, siehe Abschnitt 6.

## 3. Rechnung

```
Differenz = Maß Kleidungsstück − Maß Figur
Umfang:  Zugabe = Differenz / Maß Figur × 100   (in Prozent)
Länge:   Zugabe = Differenz                     (in cm)

Zugabe < min  → eng       (bei Längen: zu kurz)
min … max     → passt
Zugabe > max  → weit      (bei Längen: zu lang)
```

Gesamtampel = schlechtestes Ergebnis aller **Pflicht**-Messpunkte. Optionale Messpunkte erzeugen nur einen Hinweis. Fehlt ein Pflichtmaß: „keine Bewertung“.

Beispiel: Figur Brust 90 cm, T-Shirt Brust 100 cm → +11 % → liegt in 4 bis 15 % → passt.

## 4. Startwerte (Spanne „passt“)

Umfänge in % des Körpermaßes, Längen in cm. Die Werte sind aus den Quellen oben abgeleitet und auf ein typisches Körpermaß umgerechnet (Brust 90, Taille 72, Hüfte 96 cm). Sie sind Schätzungen zum Start und sollten mit echten Teilen getestet werden.

| Kleidungsart | Pflicht | Optional |
|---|---|---|
| Tops | Brust +4 bis +15 %, Taille +3 bis +25 % | Schulterbreite −1 bis +3 cm, Armlänge −3 bis +3 cm, Hals +2 bis +6 %, Oberarm +8 bis +25 %, Rückenlänge −2 bis +6 cm |
| Pullover | Brust +6 bis +25 %, Taille +5 bis +35 % | Schulterbreite −1 bis +6 cm, Armlänge −2 bis +4 cm, Oberarm +10 bis +35 %, Rückenlänge −2 bis +8 cm |
| Jacken | Brust +10 bis +25 %, Taille +10 bis +35 % | Hüfte +5 bis +25 %, Schulterbreite 0 bis +4 cm, Armlänge 0 bis +4 cm, Oberarm +25 bis +45 % |
| Hosen | Taille 0 bis +5 %, Hüfte +3 bis +15 % | Schrittlänge −6 bis 0 cm, Oberschenkel +5 bis +30 %, Knöchel 0 bis +100 % |
| Röcke | Taille 0 bis +5 %, Hüfte +3 bis +20 % | – |
| Kleider | Brust +5 bis +15 %, Taille +3 bis +20 %, Hüfte +4 bis +25 % | Unterbrust +3 bis +15 %, Schulterbreite −1 bis +3 cm |
| Einteiler | Brust +5 bis +20 %, Taille +3 bis +25 %, Hüfte +4 bis +20 % | Schrittlänge −6 bis 0 cm, Rückenlänge −1 bis +4 cm |
| Unterwäsche | – | Unterbrust −10 bis 0 %, Brust −5 bis +5 %, Taille −15 bis 0 %, Hüfte −15 bis 0 % |
| Schuhe | Fußlänge +1 bis +2 cm | Wade (Stiefel) 0 bis +6 cm |

Begründungen in Kurzform:
- **Taille bei Hosen und Röcken** nur 0 bis 5 %: Der Bund sitzt, der Gürtel hält, mehr ist sofort „weit“.
- **Schrittlänge** negativ: Das Körpermaß geht bis zum Boden, die Hose endet 0 bis 6 cm darüber.
- **Schuhe:** Innenlänge Fußlänge + 1,5 cm. Gibt der Nutzer eine EU-Größe ein, rechnet die App sie mit EU ÷ 1,5 in die Innenlänge um.

## 5. Speicherort

Die Zugaben gehören zu „Kleidungsart + Messpunkt“, also genau dorthin, wo auch `pflicht` steht:

```js
// kleidungsarten, Dokument „hosen“
messpunkte: [
  { messpunkt: "waist-circ", pflicht: true, zugabe_min: 0, zugabe_max: 5, einheit: "prozent" },
  { messpunkt: "schrittlaenge", pflicht: false, zugabe_min: -6, zugabe_max: 0, einheit: "cm" },
  …
]
```

Im Code ist `wertelisten.MESSPUNKTE_JE_KLEIDUNGSART` die eine Quelle, je Messpunkt `(pflicht, zugabe_min, zugabe_max)`. Die Einheit folgt aus dem Messpunkt (`einheit_der_zugabe`: Umfänge in Prozent, Längen in cm). `datenbank_einrichten --stammdaten` spielt sie ein. Die Prüfregel verlangt `zugabe_min`, `zugabe_max` (Zahl) und `einheit` (`prozent` oder `cm`).

Ändern: Werte in `wertelisten.py` anpassen, dann `python -m app.datenbank_einrichten --stammdaten` laufen lassen (überschreibt die Messpunkt-Listen in `kleidungsarten`).

## 6. Noch offen

1. **Dehnbare Stoffe:** Sollen Teile ein Feld „dehnbar“ (ja/nein) bekommen? Dann gilt bei dehnbaren Teilen eine eigene, niedrigere Spanne, z. B. T-Shirt Brust −5 bis +8 %. Das Material allein reicht nicht, denn auch Baumwolle kann Jersey sein.
2. **Wie fein soll die Ampel sein?** Drei Stufen (eng/passt/weit) oder fünf (zu eng/eher eng/passt/eher weit/zu weit)? Fünf Stufen gingen mit einer zweiten Grenze je Seite.
3. **Oversize-Teile:** Ein bewusst weiter Pullover würde als „weit“ markiert. Entweder akzeptieren oder später einen Schalter „Oversize“ am Teil.
