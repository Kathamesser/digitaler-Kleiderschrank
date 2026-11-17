// Oberfläche des Avatar-Konfigurators (Seite templates/avatar-konfigurator.html):
// Schieberegler bauen, Werte auf den Avatar übertragen, Maße in cm anzeigen und eingeben, Entwurf merken.

import { AvatarAnsicht, MESSPUNKTE_URL } from "./avatar.js";
import {
  GRUPPEN, REGLER, GESAMTUMFANG, FIGURTYPEN, FUER_BEIDE, REGLER_VERSION, morphWerte, alterInJahren,
} from "./regler.js";

// Bis es /api/figuren gibt, bleibt die Figur nur in diesem Browser (localStorage).
const SPEICHER_SCHLUESSEL = "sharely.avatar.entwurf";

// Maße in der Übersicht neben dem Avatar: [Schlüssel in messpunkte.json bzw. koerpergroesse, Anzeige]
const UEBERSICHT = [
  ["koerpergroesse", "Körpergröße"],
  ["bust-circ", "Brustumfang"],
  ["underbust-circ", "Unterbrust"],
  ["waist-circ", "Taille"],
  ["hips-circ", "Hüfte"],
  ["schulterbreite_ruecken", "Schulterbreite"],
  ["armlaenge", "Armlänge"],
  ["schrittlaenge", "Schrittlänge"],
  ["fusslaenge", "Fußlänge"],
];

const zustand = {
  name: "Meine Figur",
  regler: Object.fromEntries(REGLER.map((r) => [r.schluessel, 0])),
  figurtyp: null, // { typ, staerke }
};
let gesamtumfangVorher = 0;
let messpunkte = null;
let cm = {};
const zeilen = {}; // schluessel → { eingabe, wert, ruecksetzen, cmFeld }

const $ = (id) => document.getElementById(id);
const ansicht = new AvatarAnsicht($("buehne"));

// ---------- Oberfläche aufbauen ----------

function reglerZeile({ schluessel, name, links, rechts, min, max, band }, beiAenderung) {
  const zeile = document.createElement("div");
  zeile.className = "regler-zeile";
  zeile.innerHTML = `
    <div class="regler-kopf">
      <label for="r-${schluessel}"></label>
      <span class="regler-wert"></span>
      <button type="button" class="regler-null" title="Auf neutral zurücksetzen" aria-label="${name} zurücksetzen">↺</button>
    </div>
    <input type="range" id="r-${schluessel}" min="${min}" max="${max}" step="1" value="0">
    <div class="regler-enden"><span></span><span></span></div>`;
  zeile.querySelector("label").textContent = name;
  const [l, r] = zeile.querySelectorAll(".regler-enden span");
  l.textContent = links;
  r.textContent = rechts;

  const eingabe = zeile.querySelector("input");
  eingabe.style.setProperty("--null", `${(-min / (max - min)) * 100}%`);
  eingabe.addEventListener("input", () => beiAenderung(Number(eingabe.value)));
  eingabe.addEventListener("dblclick", () => beiAenderung(0));
  const ruecksetzen = zeile.querySelector(".regler-null");
  ruecksetzen.onclick = () => beiAenderung(0);

  let cmFeld = null;
  if (band) {
    const box = document.createElement("label");
    box.className = "regler-cm";
    box.innerHTML = `<span>Gemessen</span><input type="number" step="0.5" inputmode="decimal"> <span>cm</span>`;
    box.querySelector("input").setAttribute("aria-label", `${name} in Zentimetern`);
    cmFeld = box.querySelector("input");
    cmFeld.addEventListener("change", () => zentimeterEingeben(schluessel, band, Number(cmFeld.value.replace(",", "."))));
    zeile.append(box);
  }
  zeilen[schluessel] = { eingabe, wert: zeile.querySelector(".regler-wert"), ruecksetzen, cmFeld, min, max, links, rechts };
  return zeile;
}

function bereich(titel, offen, hinweis) {
  const d = document.createElement("details");
  d.className = "regler-bereich";
  d.open = offen;
  d.innerHTML = `<summary></summary><div class="regler-liste"></div>`;
  d.querySelector("summary").textContent = titel;
  if (hinweis) {
    const p = document.createElement("p");
    p.className = "leise";
    p.textContent = hinweis;
    d.querySelector(".regler-liste").append(p);
  }
  $("regler").append(d);
  return d.querySelector(".regler-liste");
}

function oberflaecheBauen() {
  const hinweise = {
    grundform: "Fang hier an: Diese Regler bestimmen die Figur im Großen. Doppelklick auf einen Regler setzt ihn auf neutral.",
    masse: "Wie die Spalten einer Größentabelle. Du kannst auch direkt einen Wert in cm eintragen, der Regler stellt sich dann passend ein.",
    koerperform: "Feinschliff der Silhouette.",
    arme_beine: null,
  };
  for (const gruppe of GRUPPEN) {
    if (gruppe.id === "masse") figurtypBereich();
    const liste = bereich(gruppe.name, gruppe.id === "grundform", hinweise[gruppe.id]);
    if (gruppe.id === "masse") {
      // Verknüpfter Regler: bewegt alle Umfänge gleichzeitig, wird nicht gespeichert
      const zeile = reglerZeile(
        { schluessel: "gesamtumfang", name: "Gesamtumfang (alle Umfänge)", links: "schmaler", rechts: "breiter", min: -100, max: 100 },
        gesamtumfangSetzen,
      );
      zeile.classList.add("verknuepft");
      liste.append(zeile);
    }
    for (const r of gruppe.regler) liste.append(reglerZeile(r, (v) => reglerSetzen(r.schluessel, v)));
  }
}

function figurtypBereich() {
  const liste = bereich("Figurtyp", false,
    "Fertige Körperform als Schnellauswahl. Es ist immer nur ein Typ aktiv, die Stärke bestimmt, wie deutlich er wirkt.");
  liste.insertAdjacentHTML("beforeend", `
    <div class="pillen" id="figurtypen-a"></div>
    <p class="feldname" id="figurtypen-b-titel"></p>
    <div class="pillen" id="figurtypen-b"></div>`);
  const staerke = reglerZeile(
    { schluessel: "figurtyp_staerke", name: "Stärke", links: "schwach", rechts: "voll", min: 0, max: 100 },
    (v) => { if (zustand.figurtyp) zustand.figurtyp.staerke = v; aktualisieren(); },
  );
  liste.append(staerke);
}

/** Figurtypen als Pillen; der zum Geschlechtsregler passende Satz steht oben. */
function figurtypenZeigen() {
  const frauZuerst = zustand.regler.geschlecht <= 0;
  const saetze = {
    frau: FIGURTYPEN.filter((f) => f.typ.startsWith("frau_") || FUER_BEIDE.includes(f.typ)),
    mann: FIGURTYPEN.filter((f) => f.typ.startsWith("mann_")),
  };
  const [oben, unten] = frauZuerst ? ["frau", "mann"] : ["mann", "frau"];
  $("figurtypen-b-titel").textContent = oben === "frau" ? "Weitere (männliche Figurtypen)" : "Weitere (weibliche Figurtypen)";
  for (const [ziel, satz, mitKeiner] of [["figurtypen-a", saetze[oben], true], ["figurtypen-b", saetze[unten], false]]) {
    const box = $(ziel);
    box.replaceChildren();
    const eintraege = mitKeiner ? [{ typ: "", name: "Keiner", bild: "nur die Regler" }, ...satz] : satz;
    for (const f of eintraege) {
      const label = document.createElement("label");
      label.title = f.bild;
      const eingabe = Object.assign(document.createElement("input"), { type: "radio", name: "figurtyp", value: f.typ });
      eingabe.checked = (zustand.figurtyp?.typ || "") === f.typ && (ziel === "figurtypen-a" || !mitKeiner);
      eingabe.onchange = () => figurtypWaehlen(f.typ);
      const text = document.createElement("span");
      text.textContent = f.name;
      label.append(eingabe, text);
      box.append(label);
    }
  }
  // Hüftbetont kann in beiden Sätzen stehen: nur eine Pille markieren
  const markiert = document.querySelectorAll('input[name="figurtyp"]:checked');
  markiert.forEach((e, i) => { if (i > 0) e.checked = false; });
}

// ---------- Werte ändern ----------

function begrenzt(schluessel, v) {
  const { min, max } = zeilen[schluessel];
  return Math.max(min, Math.min(max, Math.round(v)));
}

function reglerSetzen(schluessel, v) {
  const vorher = zustand.regler.geschlecht;
  zustand.regler[schluessel] = begrenzt(schluessel, v);
  if (schluessel === "geschlecht" && Math.sign(vorher || -1) !== Math.sign(zustand.regler.geschlecht || -1)) figurtypenZeigen();
  aktualisieren();
}

function gesamtumfangSetzen(v) {
  const schritt = v - gesamtumfangVorher;
  gesamtumfangVorher = v;
  for (const [schluessel, gewicht] of Object.entries(GESAMTUMFANG)) {
    zustand.regler[schluessel] = begrenzt(schluessel, zustand.regler[schluessel] + schritt * gewicht);
  }
  aktualisieren();
}

function figurtypWaehlen(typ) {
  zustand.figurtyp = typ ? { typ, staerke: zustand.figurtyp?.staerke || 60 } : null;
  aktualisieren();
}

/**
 * Wunschwert in cm → Reglerstellung (ZENTIMETER.md 5, „Eingabe in cm“): Steigung aus messpunkte.json,
 * Regler verschieben, neu messen, bis die Abweichung unter 0,3 cm liegt.
 */
function zentimeterEingeben(schluessel, band, ziel) {
  if (!Number.isFinite(ziel) || !messpunkte) return;
  const r = REGLER.find((x) => x.schluessel === schluessel);
  const wirkung = messpunkte.wirkung_je_target_cm;
  for (let runde = 0; runde < 6; runde++) {
    cm = ansicht.messen(messpunkte);
    const fehlt = ziel - cm[band];
    if (Math.abs(fehlt) < 0.3) break;
    const v = zustand.regler[schluessel];
    // cm je Reglerschritt auf der Seite, auf der der Regler steht bzw. in die er sich bewegt
    const seiteMax = v > 0 || (v === 0 && fehlt * (wirkung[`max_${r.target}`]?.[band] || 0) > 0);
    const steigung = seiteMax ? (wirkung[`max_${r.target}`]?.[band] || 0) / 100 : -(wirkung[`min_${r.target}`]?.[band] || 0) / 100;
    if (Math.abs(steigung) < 1e-3) break;
    let neu = begrenzt(schluessel, v + fehlt / steigung);
    if (v !== 0 && Math.sign(neu) !== Math.sign(v) && neu !== 0) neu = 0; // erst bis neutral, dann die andere Seite
    if (neu === v) break;
    zustand.regler[schluessel] = neu;
    ansicht.setzeMorphWerte(morphWerte(zustand.regler, zustand.figurtyp));
  }
  aktualisieren();
  const ergebnis = cm[band];
  if (Math.abs(ergebnis - ziel) >= 0.5) {
    meldung(`${r.name}: ${zahl(ziel)} cm geht mit dieser Figur nicht ganz, am nächsten kommt ${zahl(ergebnis)} cm.`);
  }
}

// ---------- Anzeige ----------

let messungGeplant = false;
function aktualisieren() {
  ansicht.setzeMorphWerte(morphWerte(zustand.regler, zustand.figurtyp));
  for (const [schluessel, z] of Object.entries(zeilen)) {
    const v = schluessel === "gesamtumfang" ? gesamtumfangVorher
      : schluessel === "figurtyp_staerke" ? (zustand.figurtyp?.staerke ?? 0)
      : zustand.regler[schluessel];
    z.eingabe.value = v;
    z.eingabe.style.setProperty("--wert", `${((v - z.min) / (z.max - z.min)) * 100}%`);
    z.wert.textContent = wertText(schluessel, v, z);
    z.ruecksetzen.hidden = v === 0 || schluessel === "figurtyp_staerke";
  }
  zeilen.figurtyp_staerke.eingabe.disabled = !zustand.figurtyp;
  speichern();
  if (!messungGeplant && messpunkte) {
    messungGeplant = true;
    requestAnimationFrame(() => { messungGeplant = false; masseZeigen(); });
  }
}

function wertText(schluessel, v, z) {
  if (schluessel === "alter") return `≈ ${Math.round(alterInJahren(v))} Jahre`;
  if (schluessel === "figurtyp_staerke") return `${v} %`;
  if (v === 0) return "neutral";
  return `${v < 0 ? z.links : z.rechts} ${Math.abs(v)}`;
}

const zahl = (x) => x.toLocaleString("de-DE", { minimumFractionDigits: 1, maximumFractionDigits: 1 });

function masseZeigen() {
  cm = ansicht.messen(messpunkte);
  for (const r of REGLER) {
    const feld = zeilen[r.schluessel].cmFeld;
    if (feld && document.activeElement !== feld) feld.value = cm[r.band].toFixed(1);
  }
  const liste = $("masse-liste");
  liste.replaceChildren();
  for (const [schluessel, name] of UEBERSICHT) {
    const dt = document.createElement("dt");
    dt.textContent = name;
    const dd = document.createElement("dd");
    dd.textContent = `${zahl(cm[schluessel])} cm`;
    liste.append(dt, dd);
  }
}

let meldungsZeit;
function meldung(text) {
  const el = $("konf-meldung");
  el.textContent = text;
  el.hidden = false;
  clearTimeout(meldungsZeit);
  meldungsZeit = setTimeout(() => (el.hidden = true), 6000);
}

// ---------- Entwurf merken (Format wie FIGUR-DATENMODELL.md) ----------

/** Figur im Speicherformat: nur Reglerwerte ≠ 0, dazu Name, Figurtyp und regler_version. */
export function alsFigur() {
  return {
    name: zustand.name,
    regler_version: REGLER_VERSION,
    regler: Object.fromEntries(Object.entries(zustand.regler).filter(([, v]) => v !== 0)),
    figurtyp: zustand.figurtyp,
  };
}

function speichern() {
  try { localStorage.setItem(SPEICHER_SCHLUESSEL, JSON.stringify(alsFigur())); } catch { /* privates Fenster o. Ä. */ }
}

function entwurfLaden() {
  try {
    const figur = JSON.parse(localStorage.getItem(SPEICHER_SCHLUESSEL));
    if (!figur || figur.regler_version !== REGLER_VERSION) return;
    zustand.name = figur.name || zustand.name;
    for (const [schluessel, v] of Object.entries(figur.regler || {})) {
      if (schluessel in zustand.regler) zustand.regler[schluessel] = begrenzt(schluessel, v);
    }
    if (figur.figurtyp && FIGURTYPEN.some((f) => f.typ === figur.figurtyp.typ)) zustand.figurtyp = figur.figurtyp;
  } catch { /* kein oder kaputter Entwurf: Standardfigur */ }
}

function allesZuruecksetzen() {
  for (const r of REGLER) zustand.regler[r.schluessel] = 0;
  zustand.figurtyp = null;
  gesamtumfangVorher = 0;
  figurtypenZeigen();
  aktualisieren();
}

/** Schnellstart: weibliche bzw. männliche Grundfigur, sonst alles neutral. */
function schnellstart(geschlecht) {
  allesZuruecksetzen();
  reglerSetzen("geschlecht", geschlecht);
  figurtypenZeigen();
}

// ---------- Start ----------

oberflaecheBauen();
entwurfLaden();
$("figur-name").value = zustand.name;
$("figur-name").addEventListener("input", (e) => { zustand.name = e.target.value.trim() || "Meine Figur"; speichern(); });
$("zuruecksetzen").onclick = allesZuruecksetzen;
$("start-frau").onclick = () => schnellstart(-100);
$("start-mann").onclick = () => schnellstart(100);
for (const knopf of document.querySelectorAll("[data-ansicht]")) knopf.onclick = () => ansicht.ansicht(knopf.dataset.ansicht);
figurtypenZeigen();
aktualisieren();

try {
  const [, antwort] = await Promise.all([
    ansicht.laden((anteil) => ($("laden-text").textContent = `Avatar wird geladen … ${Math.round(anteil * 100)} %`)),
    fetch(MESSPUNKTE_URL),
  ]);
  messpunkte = await antwort.json();
  $("laden").hidden = true;
  aktualisieren();
} catch (fehler) {
  console.error(fehler);
  $("laden-text").textContent = "Der Avatar konnte nicht geladen werden. Läuft der Seiten-Server im Ordner Sharely_programm?";
}

// Für Tests und spätere Speicherung über die API
window.avatarKonfigurator = { zustand, alsFigur, reglerSetzen, figurtypWaehlen, zentimeterEingeben, messen: () => ansicht.messen(messpunkte) };
