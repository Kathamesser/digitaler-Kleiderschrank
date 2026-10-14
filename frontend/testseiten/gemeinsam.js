// Gemeinsame Bausteine aller Testseiten: Backend-Adresse, Beschriftungen, Symbole, Navigation.
// Später in React/Vue: Aufrufe → src/api/, Symbole/Navigation → src/komponenten/.

const BACKEND = "http://localhost:8000";
const API = `${BACKEND}/api`;
const MAX_BILD_MB = 10; // wie max_bild_mb im Backend; das Backend prüft trotzdem selbst

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

// Symbole als SVG (keine Emojis). Farbe folgt currentColor bzw. den Variablen in stil.css.
const SYMBOL = {
  zurueck: '<svg width="16" height="28" viewBox="0 0 16 28" aria-hidden="true"><path d="M14 2 2 14l12 12" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>',
  herz: '<svg width="12" height="11" viewBox="0 0 12 11" aria-label="Favorit"><path d="M6 10.5 1.2 5.8A3 3 0 0 1 6 2a3 3 0 0 1 4.8 3.8Z" fill="currentColor"/></svg>',
  schloss: '<svg width="10" height="12" viewBox="0 0 10 12" aria-label="Privat"><rect x="1" y="5" width="8" height="6.5" rx="1" fill="currentColor"/><path d="M2.8 5V3.5a2.2 2.2 0 0 1 4.4 0V5" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>',
  haken: '<svg width="11" height="9" viewBox="0 0 11 9" aria-label="ausgewählt"><path d="M1 4.5 4 7.5 10 1.5" fill="none" stroke="#fff" stroke-width="1.8"/></svg>',
  plus: '<svg width="22" height="22" viewBox="0 0 22 22" aria-hidden="true"><path d="M11 2v18M2 11h18" stroke="#fff" stroke-width="2.2"/></svg>',
  filter: '<svg width="16" height="15" viewBox="0 0 16 15" aria-hidden="true"><path d="M1 1.5h14L9.6 7.8v5.4l-3.2-1.6V7.8Z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>',
  schliessen: '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="m2 2 10 10M12 2 2 12" stroke="currentColor" stroke-width="1.6"/></svg>',
  lupe: '<svg width="13" height="13" viewBox="0 0 13 13" aria-hidden="true"><circle cx="5.5" cy="5.5" r="4.3" fill="none" stroke="currentColor" stroke-width="1.3"/><path d="m8.7 8.7 3.6 3.6" stroke="currentColor" stroke-width="1.3"/></svg>',
  person: '<svg width="55%" height="55%" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="4.6" fill="#fff"/><path d="M3 22a9 9 0 0 1 18 0Z" fill="#fff"/></svg>',
  zahnrad: '<svg width="22" height="22" viewBox="0 0 24 24" aria-label="Einstellungen"><circle cx="12" cy="12" r="3.2" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1 7 17M17 7l2.1-2.1" stroke="currentColor" stroke-width="1.4"/></svg>',
  // Bild-Platzhalter wie in den Wireframes (Rahmen, Kreis, Berg)
  bild: '<svg width="70%" height="70%" viewBox="0 0 60 44" aria-hidden="true"><rect x="1" y="1" width="58" height="42" fill="none" stroke="#9a9a9a"/><circle cx="14" cy="12" r="4.5" fill="none" stroke="#9a9a9a"/><path d="M1 43 28 22l31 21" fill="none" stroke="#9a9a9a"/></svg>',
};

/** Untere Navigation (Schrank, Outfits, Verliehen, Freunde) ans Seitenende hängen. */
function navigation(aktiv) {
  const seiten = { schrank: "Schrank", outfits: "Outfits", verliehen: "Verliehen", freunde: "Freunde" };
  const nav = document.createElement("nav");
  nav.className = "navigation";
  for (const [datei, text] of Object.entries(seiten)) {
    const link = document.createElement("a");
    link.href = `${datei}.html`;
    link.textContent = text;
    if (datei === aktiv) { link.className = "aktiv"; link.setAttribute("aria-current", "page"); }
    nav.append(link);
  }
  document.body.append(nav);
}

/** Symbole in Platzhalter-Elemente setzen: <span data-symbol="zurueck"></span> */
function symboleEinsetzen() {
  for (const el of document.querySelectorAll("[data-symbol]")) el.innerHTML = SYMBOL[el.dataset.symbol];
}
document.addEventListener("DOMContentLoaded", symboleEinsetzen);

/** Auswahl-Pillen in den Container mit der id `ziel` setzen (Hinzufügen, Filter im Schrank).
 *  werte: { wert: Beschriftung }, typ: "radio" oder "checkbox". */
function pillen(ziel, name, werte, typ) {
  const box = document.getElementById(ziel);
  for (const [wert, text] of Object.entries(werte)) {
    const label = document.createElement("label");
    const eingabe = document.createElement("input");
    Object.assign(eingabe, { type: typ, name, value: wert });
    const span = document.createElement("span");
    span.textContent = text; // textContent, weil Filterwerte auch aus Freitext der Nutzer kommen
    label.append(eingabe, span);
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

/** Kachel eines Kleidungsstücks für Raster (Schrank, Profil, Outfit erstellen). */
function kleidungsKarte(k, { link = true } = {}) {
  const karte = document.createElement(link ? "a" : "button");
  karte.className = "karte";
  if (link) karte.href = `kleidungsstueck.html?id=${encodeURIComponent(k.id)}`;
  else karte.type = "button";
  const kachel = document.createElement("div");
  kachel.className = "kachel";
  const img = document.createElement("img");
  img.src = bildUrl(k);
  img.alt = titelVon(k);
  img.loading = "lazy";
  kachel.append(img);
  if (k.favorit) kachel.insertAdjacentHTML("beforeend", `<span class="abzeichen rechts">${SYMBOL.herz}</span>`);
  if (k.privat) kachel.insertAdjacentHTML("beforeend", `<span class="abzeichen links">${SYMBOL.schloss}</span>`);
  const text = document.createElement("p");
  text.textContent = titelVon(k);
  karte.append(kachel, text);
  return karte;
}
