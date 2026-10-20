// Gemeinsame Bausteine aller Testseiten: Backend-Adresse, Beschriftungen, Symbole, Kopf- und Fußleiste.
// Aussehen nach den Desktop-Mockups (docs/mockups/desktop/).
// Später in React/Vue: Aufrufe → src/api/, Symbole/Kopf/Fußleiste → src/komponenten/.

const BACKEND = "http://localhost:8000";
const API = `${BACKEND}/api`;
const MAX_BILD_MB = 10; // wie max_bild_mb im Backend; das Backend prüft trotzdem selbst

// Platzhalter, bis es Anmeldung und Modul nutzer gibt
const NUTZER = { name: "Test-Nutzer" };

// Werte wie in backend/app/module/kleidung/schemas.py
const KATEGORIEN = {
  oberteile: "Oberteil", hosen: "Hose", roecke: "Rock", kleider: "Kleid",
  jacken: "Jacke", schuhe: "Schuhe", accessoires: "Accessoire",
};
const KATEGORIEN_MEHRZAHL = {
  oberteile: "Oberteile", hosen: "Hosen", roecke: "Röcke", kleider: "Kleider",
  jacken: "Jacken", schuhe: "Schuhe", accessoires: "Accessoires",
};
const SAISONS = { fruehling: "Frühling", sommer: "Sommer", herbst: "Herbst", winter: "Winter" };
const ANLAESSE = { alltag: "Alltag", sport: "Sport", edel: "Edel" };
const HERKUENFTE = { laden: "Laden", flohmarkt: "Flohmarkt", online: "Online" };

// Farbe und Material sind im Backend Freitext. Die Seiten bieten wie die Mockups feste Werte an
// (Farbkreise, Material-Pillen) und erkennen sie im Text am Wortteil (woerter),
// z. B. „Hellblau“ → Blau, „Denim“ → Jeans.
const FARBEN = [
  { wert: "schwarz", text: "Schwarz", farbe: "#2b2b2b", woerter: ["schwarz"] },
  { wert: "weiss", text: "Weiß", farbe: "#ffffff", woerter: ["weiß", "weiss"] },
  { wert: "grau", text: "Grau", farbe: "#9a9a9a", woerter: ["grau", "silber"] },
  { wert: "beige", text: "Beige", farbe: "#e3d3b4", woerter: ["beige", "creme", "sand"] },
  { wert: "braun", text: "Braun", farbe: "#8b5a3c", woerter: ["braun", "cognac"] },
  { wert: "rot", text: "Rot", farbe: "#c94040", woerter: ["rot", "bordeaux"] },
  { wert: "rosa", text: "Rosa", farbe: "#eda5b4", woerter: ["rosa", "pink"] },
  { wert: "orange", text: "Orange", farbe: "#ef8c3a", woerter: ["orange"] },
  { wert: "gelb", text: "Gelb", farbe: "#f0c63c", woerter: ["gelb", "gold"] },
  { wert: "gruen", text: "Grün", farbe: "#4f9a58", woerter: ["grün", "gruen", "oliv", "khaki"] },
  { wert: "blau", text: "Blau", farbe: "#3a72c4", woerter: ["blau", "türkis"] },
  { wert: "dunkelblau", text: "Dunkelblau", farbe: "#2c3a5e", woerter: ["dunkelblau", "navy", "marine"] },
  { wert: "lila", text: "Lila", farbe: "#8a5bb5", woerter: ["lila", "violett", "flieder"] },
  { wert: "bunt", text: "Bunt", farbe: "conic-gradient(#c94040, #f0c63c, #4f9a58, #3a72c4, #8a5bb5, #c94040)", woerter: ["bunt", "mehrfarbig", "gemustert"] },
];
const MATERIALIEN = [
  { wert: "baumwolle", text: "Baumwolle", woerter: ["baumwolle", "cotton"] },
  { wert: "polyester", text: "Polyester", woerter: ["polyester"] },
  { wert: "wolle", text: "Wolle", woerter: ["wolle", "merino", "kaschmir"] },
  { wert: "leinen", text: "Leinen", woerter: ["leinen"] },
  { wert: "seide", text: "Seide", woerter: ["seide"] },
  { wert: "leder", text: "Leder", woerter: ["leder"] },
  { wert: "jeans", text: "Jeans", woerter: ["jeans", "denim"] },
  { wert: "viskose", text: "Viskose", woerter: ["viskose"] },
];

/** Welche festen Werte (FARBEN, MATERIALIEN) in einem Freitext stecken. Längere Wörter zuerst und dann
 *  aus dem Text streichen, damit „Baumwolle“ nicht zusätzlich als „Wolle“ und „Dunkelblau“ nicht als „Blau“ zählt. */
function erkannteWerte(text, werte) {
  let rest = (text || "").toLowerCase();
  const gefunden = new Set();
  const paare = werte.flatMap((w) => w.woerter.map((wort) => [wort, w.wert])).sort((a, b) => b[0].length - a[0].length);
  for (const [wort, wert] of paare) {
    if (rest.includes(wort)) { gefunden.add(wert); rest = rest.split(wort).join(" "); }
  }
  return gefunden;
}

// Symbole als SVG (keine Emojis), Linien im Stil der Mockups. Farbe folgt currentColor.
const svg = (inhalt, groesse = 18) =>
  `<svg width="${groesse}" height="${groesse}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${inhalt}</svg>`;
const SYMBOL = {
  zurueck: svg('<path d="m15 5-7 7 7 7"/>'),
  weiter: svg('<path d="m9 5 7 7-7 7"/>', 16),
  unten: svg('<path d="m5 9 7 7 7-7"/>'),
  herz: svg('<path d="M12 20s-7.5-4.6-7.5-10A4.2 4.2 0 0 1 12 7.4 4.2 4.2 0 0 1 19.5 10c0 5.4-7.5 10-7.5 10Z"/>'),
  herzVoll: '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-7.5-4.6-7.5-10A4.2 4.2 0 0 1 12 7.4 4.2 4.2 0 0 1 19.5 10c0 5.4-7.5 10-7.5 10Z" fill="#e05545"/></svg>',
  schloss: svg('<rect x="5" y="10.5" width="14" height="10" rx="2"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5"/>'),
  haken: svg('<path d="m5 12.5 4.5 4.5L19 7.5"/>', 16),
  ok: svg('<path d="m5 12.5 4.5 4.5L19 7.5"/>'),
  plus: svg('<path d="M12 5v14M5 12h14"/>', 20),
  filter: svg('<path d="M4 7h16M7 12h10M10 17h4"/>'),
  schliessen: svg('<path d="m6 6 12 12M18 6 6 18"/>'),
  haus: svg('<path d="M4 11 12 4l8 7v9H4Z"/>'),
  schrank: svg('<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M12 3v18M10 11v2M14 11v2"/>'),
  buegel: svg('<path d="M12 7.5a2 2 0 1 1 2-2c0 1.2-2 1.6-2 3l8.6 6.4a1.2 1.2 0 0 1-.7 2.1H4.1a1.2 1.2 0 0 1-.7-2.1L12 8.5"/>'),
  links: svg('<path d="M19 12H5m6-6-6 6 6 6"/>'),
  rechts: svg('<path d="M5 12h14m-6-6 6 6-6 6"/>'),
  tausch: svg('<path d="M5 8h13l-3-3M19 16H6l3 3"/>'),
  stern: svg('<path d="m12 3.5 2.6 5.4 5.9.8-4.3 4.1 1 5.8L12 16.9l-5.2 2.7 1-5.8-4.3-4.1 5.9-.8Z"/>'),
  ruecksetzen: svg('<path d="M4.5 12a7.5 7.5 0 1 0 2.2-5.3M4.5 4v4h4"/>'),
  lupe: svg('<circle cx="11" cy="11" r="6.5"/><path d="m16 16 4 4"/>', 20),
  zahnrad: svg('<circle cx="12" cy="12" r="3"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M5.3 18.7l2.1-2.1M16.6 7.4l2.1-2.1"/>', 20),
  kamera: svg('<path d="M4 8h3l2-2.5h6L17 8h3v11H4Z"/><circle cx="12" cy="13" r="3.5"/>'),
  hochladen: svg('<path d="M12 15V4m-4.5 4.5L12 4l4.5 4.5M5 15v4h14v-4"/>'),
  kalender: svg('<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M8 3v4M16 3v4"/>', 16),
  etikett: svg('<path d="M3.5 12V4.5h7.5l9 9-7.5 7.5Z"/><circle cx="8" cy="8.5" r="1.2"/>', 16),
  senden: svg('<path d="M21 3 10 14M21 3l-7 18-4-7-7-4Z"/>'),
  muell: svg('<path d="M4 7h16M9 7V4h6v3M6.5 7l1 13h9l1-13"/>'),
  stift: svg('<path d="m4 20 1-4.5L16 4.5l3.5 3.5L8.5 19Z"/>'),
  person: svg('<circle cx="12" cy="8" r="4"/><path d="M4.5 21a7.5 7.5 0 0 1 15 0"/>'),
  personPlus: svg('<circle cx="10" cy="8" r="4"/><path d="M3 21a7 7 0 0 1 14 0M19 8v6M16 11h6"/>'),
  personWechsel: svg('<circle cx="9" cy="8" r="4"/><path d="M2 21a7 7 0 0 1 14 0M17 6h5m-2-2 2 2-2 2"/>'),
  anprobieren: svg('<circle cx="12" cy="4.5" r="2"/><path d="M8 21v-6.5L6 9.5l6-2.5 6 2.5-2 5V21M12 7v14"/>'),
  abmelden: svg('<path d="M10 4H5v16h5M14 8l4 4-4 4M18 12H9"/>'),
  brief: svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6 8.5 7 8.5-7"/>'),
  lineal: svg('<rect x="2.5" y="8" width="19" height="8" rx="1.5"/><path d="M6.5 8v3M10 8v4M13.5 8v3M17 8v4"/>'),
  auge: svg('<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12Z"/><circle cx="12" cy="12" r="3"/>', 20),
  sperren: svg('<circle cx="12" cy="12" r="8"/><path d="m6.5 6.5 11 11"/>'),
  mehr: svg('<circle cx="5" cy="12" r=".8"/><circle cx="12" cy="12" r=".8"/><circle cx="19" cy="12" r=".8"/>'),
  ausdehnen: svg('<path d="M14 4h6v6M10 20H4v-6M20 4l-7 7M4 20l7-7"/>'),
};

/** Kopfzeile wie in den Mockups: Logo mit SHARELY links, Seitentitel mittig, Nutzer rechts. */
function seitenkopf(titel) {
  const kopf = document.createElement("header");
  kopf.className = "seitenkopf";
  kopf.innerHTML = `
    <a class="marke-klein" href="hauptmenue.html" aria-label="Sharely – zum Hauptmenü">
      <span class="logo-kachel"><img src="../../assets/branding/sharely-logo.png" alt=""></span>
      <span class="wortmarke">SHARELY</span>
    </a>
    <h1></h1>
    <a class="nutzer-chip" href="profil.html" aria-label="Mein Profil"><span class="initiale"></span><span class="name"></span></a>`;
  kopf.querySelector("h1").textContent = titel;
  kopf.querySelector(".initiale").textContent = NUTZER.name[0];
  kopf.querySelector(".name").textContent = NUTZER.name;
  document.querySelector("main").prepend(kopf);
}

/** Leiste am Seitenende mit großen Knöpfen (Mockups: „Hauptmenü“, „Garderobe“ …).
 *  knoepfe: [{ text, symbol, href | onclick, art: "" | "dunkel" | "rand" }] */
function fussleiste(knoepfe) {
  const leiste = document.createElement("nav");
  leiste.className = "fussleiste";
  for (const { text, symbol, href, onclick, art = "", id } of knoepfe) {
    const knopf = document.createElement(href ? "a" : "button");
    if (href) knopf.href = href;
    else { knopf.type = "button"; knopf.onclick = onclick; }
    if (id) knopf.id = id;
    knopf.className = `knopf ${art}`;
    knopf.innerHTML = SYMBOL[symbol] || "";
    knopf.append(` ${text}`);
    leiste.append(knopf);
  }
  document.querySelector("main").append(leiste);
}

/** Symbole in Platzhalter-Elemente setzen: <span data-symbol="zurueck"></span> */
function symboleEinsetzen(wurzel = document) {
  for (const el of wurzel.querySelectorAll("[data-symbol]")) el.innerHTML = SYMBOL[el.dataset.symbol];
}
document.addEventListener("DOMContentLoaded", () => symboleEinsetzen());

/** Auswahl-Pillen in den Container mit der id `ziel` setzen (Hinzufügen, Filter im Schrank).
 *  werte: { wert: Beschriftung }, typ: "radio" oder "checkbox". */
function pillen(ziel, name, werte, typ) {
  const box = document.getElementById(ziel);
  for (const [wert, text] of Object.entries(werte)) {
    const label = document.createElement("label");
    const eingabe = document.createElement("input");
    Object.assign(eingabe, { type: typ, name, value: wert });
    const span = document.createElement("span");
    span.textContent = text;
    label.append(eingabe, span);
    box.append(label);
  }
}

/** Farbkreise als Auswahl (Filter: mehrere, Hinzufügen: einer). */
function farbkreise(ziel, name, typ) {
  const box = document.getElementById(ziel);
  for (const { wert, text, farbe } of FARBEN) {
    const label = document.createElement("label");
    label.title = text;
    const eingabe = Object.assign(document.createElement("input"), { type: typ, name, value: wert });
    eingabe.setAttribute("aria-label", text);
    const kreis = document.createElement("span");
    kreis.style.background = farbe;
    label.append(eingabe, kreis);
    box.append(label);
  }
}

/** GET ans Backend; wirft bei Fehlern eine Meldung, die man direkt anzeigen kann. */
async function holeJson(pfad) {
  let antwort;
  try {
    antwort = await fetch(`${API}${pfad}`);
  } catch {
    throw new Error("Keine Verbindung zum Backend. Läuft es auf Port 8000?");
  }
  const inhalt = await antwort.json();
  if (!antwort.ok) throw new Error(fehlerText(inhalt));
  return inhalt;
}

/** Fehlerantwort des Backends ({"detail": …}) als lesbarer Text. */
function fehlerText(inhalt) {
  if (typeof inhalt.detail === "string") return inhalt.detail;
  if (Array.isArray(inhalt.detail)) {
    return inhalt.detail.map((f) => `${f.loc.at(-1)}: ${f.msg.replace(/^Value error, /, "")}`).join("\n");
  }
  return "Unbekannter Fehler.";
}

function zeigeMeldung(el, text, art) {
  el.textContent = text;
  el.className = `meldung ${art}`;
}

/** Anzeigename eines Kleidungsstücks, solange es keine Bezeichnung gibt: „Jacke · Vaude“ */
function titelVon(k) {
  return [KATEGORIEN[k.kategorie], k.marke].filter(Boolean).join(" · ");
}

function bildUrl(k) {
  return BACKEND + k.bild_url;
}

/** Pastellton der Kachel wie in den Mockups, fest je Teil (aus der id berechnet). */
function tonVon(id) {
  const TOENE = ["ton-beige", "ton-tuerkis", "ton-gelb", "ton-rosa", "ton-minze"];
  let summe = 0;
  for (const zeichen of String(id)) summe += zeichen.charCodeAt(0);
  return TOENE[summe % TOENE.length];
}

/** Kachel eines Kleidungsstücks (Schrank, Outfit erstellen): Bild, Herz, Name, Kategorie. */
function kleidungsKarte(k, { link = true } = {}) {
  const karte = document.createElement(link ? "a" : "button");
  karte.className = "karte";
  if (link) karte.href = `kleidungsstueck.html?id=${encodeURIComponent(k.id)}`;
  else karte.type = "button";
  const kachel = document.createElement("div");
  kachel.className = `kachel ${tonVon(k.id)}`;
  const img = document.createElement("img");
  img.src = bildUrl(k);
  img.alt = titelVon(k);
  img.loading = "lazy";
  img.onerror = () => { // Bild fehlt: Bügel wie im Mockup, Herz und Schloss bleiben
    const ersatz = document.createElement("template");
    ersatz.innerHTML = SYMBOL.buegel;
    img.replaceWith(ersatz.content);
  };
  kachel.append(img);
  if (link) {
    kachel.insertAdjacentHTML("beforeend",
      `<span class="abzeichen rechts" ${k.favorit ? 'aria-label="Favorit"' : 'aria-hidden="true"'}>${k.favorit ? SYMBOL.herzVoll : SYMBOL.herz}</span>`);
  }
  if (k.privat) kachel.insertAdjacentHTML("beforeend", `<span class="abzeichen links" aria-label="Privat">${SYMBOL.schloss}</span>`);
  const name = document.createElement("strong");
  name.textContent = k.marke || KATEGORIEN[k.kategorie];
  const art = document.createElement("small");
  art.textContent = KATEGORIEN_MEHRZAHL[k.kategorie];
  karte.append(kachel, name, art);
  return karte;
}
