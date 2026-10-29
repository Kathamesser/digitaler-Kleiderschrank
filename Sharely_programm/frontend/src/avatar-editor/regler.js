// Alle Regler des Avatar-Konfigurators: Schlüssel, Beschriftung und Morph Target.
// Verbindliche Quelle ist docs/avatar/AVATAR-REGLER.md, die Schlüssel kommen aus
// docs/avatar/FIGUR-DATENMODELL.md. Wer hier etwas ändert, zieht beide Dokumente nach.

/** Version der Regler-Zuordnung, wird mit jeder Figur gespeichert (FIGUR-DATENMODELL.md). */
export const REGLER_VERSION = 1;

/**
 * Grenzen einzelner Regler, wo die volle Spanne −100…+100 keinen erwachsenen Menschen ergibt.
 * Beide sind noch VORSCHLÄGE, die Entscheidung im Team ist offen (BRAIN.md, offene Fragen):
 * - alter: −31 entspricht min_age = 0,31, also etwa 18 Jahre (AVATAR-REGLER.md 3.1)
 * - koerpergroesse: −40 bis +45, etwa 144 bis 205 cm (ZENTIMETER.md Abschnitt 4)
 */
export const GRENZEN = {
  alter: { min: -31, max: 100 },
  koerpergroesse: { min: -40, max: 45 },
};

// Ein Eintrag: [schluessel, Anzeige, Target ohne min_/max_, links, rechts, Messband aus messpunkte.json]
const GRUNDFORM = [
  ["geschlecht", "Geschlecht", "gender", "weiblich", "männlich"],
  ["alter", "Alter", "age", "jünger", "älter"],
  ["gewicht", "Gewicht", "weight", "schlanker", "fülliger"],
  ["muskeln", "Muskeln", "muscle", "weniger", "mehr"],
  ["koerpergroesse", "Körpergröße", "height", "kleiner", "größer", "koerpergroesse"],
  ["proportionen", "Proportionen", "bodyproportions", "weniger idealisiert", "idealisierter"],
];

// Maße: Target measure_<band>-decr-incr, links kleiner/kürzer, rechts größer/länger
const MASSE = [
  ["brustumfang", "Brustumfang", "bust-circ"],
  ["unterbrustumfang", "Unterbrustumfang", "underbust-circ"],
  ["taillenumfang", "Taillenumfang", "waist-circ"],
  ["hueftumfang", "Hüftumfang", "hips-circ"],
  ["halsumfang", "Halsumfang", "neck-circ"],
  ["halslaenge", "Halslänge", "neck-height"],
  ["schulterbreite", "Schulterbreite", "shoulder-dist"],
  ["brustbreite_vorn", "Brustbreite vorn", "frontchest-dist"],
  ["rueckenlaenge", "Rückenlänge", "napetowaist-dist"],
  ["abstand_taille_huefte", "Abstand Taille bis Hüfte", "waisttohip-dist"],
  ["oberarmumfang", "Oberarmumfang", "upperarm-circ"],
  ["oberarmlaenge", "Oberarmlänge", "upperarm-length"],
  ["unterarmlaenge", "Unterarmlänge", "lowerarm-length"],
  ["handgelenkumfang", "Handgelenkumfang", "wrist-circ"],
  ["oberschenkelumfang", "Oberschenkelumfang", "thigh-circ"],
  ["knieumfang", "Knieumfang", "knee-circ"],
  ["wadenumfang", "Wadenumfang", "calf-circ"],
  ["knoechelumfang", "Knöchelumfang", "ankle-circ"],
  ["oberschenkellaenge_mass", "Oberschenkellänge", "upperleg-height"],
  ["unterschenkellaenge_mass", "Unterschenkellänge", "lowerleg-height"],
].map(([schluessel, name, band]) => [schluessel, name, `measure_${band}-decr-incr`, "kleiner", "größer", band]);

const KOERPERFORM = [
  ["oberkoerper_breite", "Oberkörper Breite", "torso_scale-horiz-decr-incr", "schmaler", "breiter"],
  ["oberkoerper_tiefe", "Oberkörper Tiefe", "torso_scale-depth-decr-incr", "flacher", "tiefer"],
  ["oberkoerper_laenge", "Oberkörper Länge", "torso_scale-vert-decr-incr", "kürzer", "länger"],
  ["v_form", "V-Form", "torso_vshape-decr-incr", "weniger", "mehr"],
  ["brustmuskeln", "Brustmuskeln", "torso_muscle-pectoral-decr-incr", "weniger", "mehr"],
  ["rueckenmuskeln", "Rückenmuskeln", "torso_muscle-dorsi-decr-incr", "weniger", "mehr"],
  ["huefte_breite", "Hüfte Breite", "hip_scale-horiz-decr-incr", "schmaler", "breiter"],
  ["huefte_tiefe", "Hüfte Tiefe", "hip_scale-depth-decr-incr", "flacher", "tiefer"],
  ["huefte_hoehe", "Hüfte Höhe", "hip_scale-vert-decr-incr", "niedriger", "höher"],
  ["taillenhoehe", "Taillenhöhe", "hip_waist-down-up", "tiefer", "höher"],
  ["bauch", "Bauch", "stomach_pregnant-decr-incr", "flacher", "runder"],
  ["po", "Po", "buttocks_volume-decr-incr", "kleiner", "größer"],
  ["brustgroesse", "Brustgröße", "breast_breastsize", "kleiner", "größer"],
  ["brustform", "Brustform", "breast_breastfirmness", "weicher", "fester"],
];

const ARME_BEINE = [
  ["fussgroesse", "Fußgröße", "armslegs_foot-scale-decr-incr", "kleiner", "größer", "fusslaenge"],
  ["oberarme", "Oberarme", "armslegs_upperarm-fat-decr-incr", "schlanker", "kräftiger"],
  ["oberschenkel", "Oberschenkel", "armslegs_upperleg-fat-decr-incr", "schlanker", "kräftiger"],
  ["unterschenkel", "Unterschenkel", "armslegs_lowerleg-fat-decr-incr", "schlanker", "kräftiger"],
  ["beinstellung", "Beinstellung", "armslegs_leg-valgus-decr-incr", "O-Beine", "X-Beine"],
  ["oberschenkel_laenge", "Oberschenkel-Länge", "armslegs_upperlegs-height-decr-incr", "kürzer", "länger"],
  ["unterschenkel_laenge", "Unterschenkel-Länge", "armslegs_lowerlegs-height-decr-incr", "kürzer", "länger"],
];

const alsRegler = (gruppe) => ([schluessel, name, target, links, rechts, band]) =>
  ({ schluessel, name, target, links, rechts, band, gruppe, ...(GRENZEN[schluessel] || { min: -100, max: 100 }) });

/** Bereiche des Editors in Anzeige-Reihenfolge. */
export const GRUPPEN = [
  { id: "grundform", name: "Grundform", regler: GRUNDFORM.map(alsRegler("grundform")) },
  { id: "masse", name: "Maße", regler: MASSE.map(alsRegler("masse")) },
  { id: "koerperform", name: "Körperform", regler: KOERPERFORM.map(alsRegler("koerperform")) },
  { id: "arme_beine", name: "Arme, Beine, Füße", regler: ARME_BEINE.map(alsRegler("arme_beine")) },
];

/** Alle 47 Regler als flache Liste. */
export const REGLER = GRUPPEN.flatMap((g) => g.regler);

/**
 * Verknüpfter Regler „Gesamtumfang“ (AVATAR-REGLER.md Abschnitt 4, Vorschlag): verschiebt alle
 * Umfang-Maße gleichzeitig, jeweils mit Gewicht 1,0. Er ist nur eine Bedienhilfe und wird nicht gespeichert.
 */
export const GESAMTUMFANG = {
  brustumfang: 1, unterbrustumfang: 1, taillenumfang: 1, hueftumfang: 1, halsumfang: 1, oberarmumfang: 1,
  handgelenkumfang: 1, oberschenkelumfang: 1, knieumfang: 1, wadenumfang: 1, knoechelumfang: 1,
};

/** Die 20 Figurtypen (AVATAR-REGLER.md 3.5). Schlüssel = Target ohne max_figur_. */
export const FIGURTYPEN = [
  ["frau_apfel", "Apfel", "Mitte fülliger, Beine schlank"],
  ["frau_birne", "Birne", "Hüfte breiter als Schultern"],
  ["frau_birne-kraeftig", "Birne, kräftig", "breite Hüften, kräftige Oberschenkel"],
  ["frau_sanduhr-kurvig", "Sanduhr, kurvig", "schmale Taille, kurvige Brust und Hüfte"],
  ["frau_sanduhr-schlank", "Sanduhr, schlank", "schmale Taille, schlanker"],
  ["frau_v-form", "V-Form", "Schultern betont, Hüfte schmal"],
  ["frau_rechteck", "Rechteck", "Taille kaum betont"],
  ["frau_raute", "Raute", "Mitte und Hüfte etwas breiter, Schultern schmal"],
  ["frau_saeule", "Schlanke Säule", "schlank, gerade"],
  ["frau_bauchbetont", "Bauchbetont", "runder Bauch, sonst schlank"],
  ["frau_vollschlank", "Vollschlank", "rundum füllig"],
  ["mann_apfel", "Apfel", "Bauch und Brust fülliger"],
  ["mann_birne", "Birne", "Hüfte breiter als Schultern"],
  ["mann_hueftbetont", "Hüftbetont", "Hüfte und Oberschenkel weicher"],
  ["mann_v-form", "V-Form", "breite Schultern, schmale Hüfte"],
  ["mann_trapez", "Trapez (athletisch)", "breite Schultern, mittlere Taille"],
  ["mann_rechteck", "Rechteck", "gerade, Taille kaum abgesetzt"],
  ["mann_saeule", "Schlanke Säule", "schlank, gerade"],
  ["mann_bauchbetont", "Bauchbetont", "runder Bauch"],
  ["mann_vollschlank", "Vollschlank", "sehr füllig, großer Bauch"],
].map(([typ, name, bild]) => ({ typ, name, bild, target: `max_figur_${typ}` }));

/** „Hüftbetont“ gibt es nur als mann_-Target, es wird bei beiden Geschlechtern angeboten. */
export const FUER_BEIDE = ["mann_hueftbetont"];

/**
 * Reglerstellung → Morph-Werte (AVATAR-REGLER.md Abschnitt 1):
 * v < 0 → min_ = −v/100, v > 0 → max_ = v/100, nie beide. Figurtyp: max_figur_<typ> = staerke/100.
 * Fehlende Regler zählen als 0. Ergebnis enthält alle Targets, auch die auf 0.
 */
export function morphWerte(regler, figurtyp) {
  const werte = {};
  for (const r of REGLER) {
    const v = Math.max(r.min, Math.min(r.max, regler[r.schluessel] || 0));
    werte[`min_${r.target}`] = v < 0 ? -v / 100 : 0;
    werte[`max_${r.target}`] = v > 0 ? v / 100 : 0;
  }
  for (const f of FIGURTYPEN) werte[f.target] = 0;
  if (figurtyp && figurtyp.typ) werte[`max_figur_${figurtyp.typ}`] = (figurtyp.staerke || 0) / 100;
  return werte;
}

/**
 * Alter in Jahren zur Anzeige. MakeHuman: age 0 = 1 Jahr, 0,1875 = 11, 0,5 = 25 (Standard), 1 = 90.
 * Der Regler verschiebt age von 0,5 aus nach links bis 0 bzw. nach rechts bis 1.
 */
export function alterInJahren(v) {
  const age = 0.5 + v / 200;
  if (age < 0.1875) return 1 + (age / 0.1875) * 10;
  if (age < 0.5) return 11 + ((age - 0.1875) / 0.3125) * 14;
  return 25 + ((age - 0.5) / 0.5) * 65;
}
