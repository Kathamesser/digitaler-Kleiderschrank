// Beispieldaten für die Seiten, deren Backend-Module noch fehlen (freunde, verleihen, Neuigkeiten).
// Nur zum Durchklicken der Mockups an einer Stelle gesammelt; fliegt raus, sobald die Module stehen.
// Felder nach dem ERM vom 20.10.2026 (docs/datenmodell/ERM-SHARELY.md).

const FREUNDE_BEISPIEL = [
  { id: "lena", name: "Lena Becker", ton: "gelb", seit: "März 2025", teile: 24, outfits: 5, geliehen: 2, verliehen: 1 },
  { id: "jonas", name: "Jonas Weber", ton: "", seit: "Juni 2025", teile: 12, outfits: 2, geliehen: 0, verliehen: 1 },
  { id: "mia", name: "Mia Schulz", ton: "rosa", seit: "Januar 2026", teile: 31, outfits: 8, geliehen: 1, verliehen: 0 },
  { id: "tim", name: "Tim Hoffmann", ton: "", seit: "Mai 2026", teile: 9, outfits: 1, geliehen: 0, verliehen: 0 },
  { id: "sara", name: "Sara Yilmaz", ton: "beige", seit: "August 2026", teile: 17, outfits: 3, geliehen: 0, verliehen: 0 },
];

const FREUNDSCHAFTSANFRAGEN_BEISPIEL = [{ name: "Anna Klein", ton: "lila" }, { name: "Ben Fischer", ton: "gelb" }];

// Wen „Freund hinzufügen“ über den Nutzernamen findet
const NUTZER_BEISPIEL = [
  { nutzername: "AnnaK", name: "Anna Klein", ton: "lila", teile: 31 },
  { nutzername: "paul.m", name: "Paul Meier", ton: "", teile: 8 },
];

/** Freund aus der Adresse (…?freund=lena), sonst der erste. */
function freundAusAdresse() {
  const id = new URLSearchParams(location.search).get("freund");
  return FREUNDE_BEISPIEL.find((f) => f.id === id) || FREUNDE_BEISPIEL[0];
}

// Sicht auf geteilte Teile eines Freundes; kommt später aus dem Leihvorgang (ERM, Abgleich mit den Mockups)
const VERFUEGBARKEIT = { verfuegbar: "Verfügbar", bei_dir: "Bei dir", verliehen: "Verliehen" };

// Geteilte Teile (privat = false) eines Freundes; zum Durchklicken für jeden Freund dieselben
const FREUND_TEILE_BEISPIEL = [
  { id: "f1", name: "Lederjacke", kleidungsart: "jacken", ton: "ton-gelb", verfuegbarkeit: "bei_dir", kategorien: ["Freizeit", "Abend"], saison: ["fruehling", "herbst"], material: "leder", farbe: "schwarz" },
  { id: "f2", name: "Sommerkleid", kleidungsart: "kleider", ton: "ton-tuerkis", verfuegbarkeit: "verfuegbar", kategorien: ["Freizeit", "Urlaub"], saison: ["fruehling", "sommer"], material: "leinen", farbe: "gruen" },
  { id: "f3", name: "Stiefel", kleidungsart: "schuhe", ton: "ton-rosa", verfuegbarkeit: "verfuegbar", kategorien: ["Winterkleidung"], saison: ["herbst", "winter"], material: "leder", farbe: "braun" },
  { id: "f4", name: "Seidenschal", kleidungsart: "accessoires", ton: "ton-minze", verfuegbarkeit: "bei_dir", kategorien: ["Abend"], saison: ["ganzjaehrig"], material: "seide", farbe: "bunt" },
  { id: "f5", name: "Blazer", kleidungsart: "jacken", ton: "ton-beige", verfuegbarkeit: "verfuegbar", kategorien: ["Business"], saison: ["ganzjaehrig"], material: "wolle", farbe: "dunkelblau" },
  { id: "f6", name: "Strickpullover", kleidungsart: "pullover", ton: "ton-gelb", verfuegbarkeit: "verliehen", kategorien: ["Winterkleidung"], saison: ["herbst", "winter"], material: "wolle", farbe: "beige" },
  { id: "f7", name: "Faltenrock", kleidungsart: "roecke", ton: "ton-rosa", verfuegbarkeit: "verfuegbar", kategorien: ["Business"], saison: ["fruehling", "herbst"], material: "polyester", farbe: "grau" },
  { id: "f8", name: "Jeans", kleidungsart: "hosen", ton: "ton-minze", verfuegbarkeit: "verfuegbar", kategorien: ["Freizeit"], saison: ["ganzjaehrig"], material: "jeans", farbe: "blau" },
  { id: "f9", name: "Bluse", kleidungsart: "tops", ton: "ton-tuerkis", verfuegbarkeit: "verfuegbar", kategorien: ["Business"], saison: ["fruehling", "sommer"], material: "viskose", farbe: "weiss" },
  { id: "f10", name: "Trenchcoat", kleidungsart: "jacken", ton: "ton-beige", verfuegbarkeit: "verliehen", kategorien: ["Business"], saison: ["fruehling", "herbst"], material: "baumwolle", farbe: "beige" },
  { id: "f11", name: "Clutch", kleidungsart: "accessoires", ton: "ton-gelb", verfuegbarkeit: "verfuegbar", kategorien: ["Party", "Abend"], saison: ["ganzjaehrig"], material: "leder", farbe: "gelb" },
  { id: "f12", name: "Ballerinas", kleidungsart: "schuhe", ton: "ton-minze", verfuegbarkeit: "verfuegbar", kategorien: ["Sommerkleidung"], saison: ["fruehling", "sommer"], material: "leder", farbe: "rosa" },
];

// Geteilte Outfits eines Freundes; teile = Namen aus FREUND_TEILE_BEISPIEL
const FREUND_OUTFITS_BEISPIEL = [
  { name: "Sommerfest", kategorien: ["Party", "Freizeit"], teile: ["Sommerkleid", "Clutch", "Ballerinas", "Seidenschal"] },
  { name: "Büro-Look", kategorien: ["Business"], teile: ["Blazer", "Bluse", "Jeans", "Stiefel"] },
  { name: "Herbstspaziergang", kategorien: ["Freizeit"], teile: ["Trenchcoat", "Strickpullover", "Jeans", "Stiefel"] },
  { name: "Konzertabend", kategorien: ["Abend"], teile: ["Lederjacke", "Faltenrock", "Bluse", "Stiefel"] },
  { name: "Städtetrip", kategorien: ["Urlaub"], teile: ["Blazer", "Sommerkleid", "Ballerinas", "Clutch"] },
];

// Leih- und Geschenkanfragen an mich (Leihvorgänge mit Status angefragt, ERM Entscheidung 8)
const LEIHANFRAGEN_BEISPIEL = [
  { von: "Mia Schulz", ton: "rosa", typ: "leihen", teil: "Lederjacke", teilTon: "ton-gelb", bis: "30.10.2026", wann: "vor 2 Stunden" },
  { von: "Jonas Weber", ton: "", typ: "verschenken", teil: "Handtasche", teilTon: "ton-minze", wann: "gestern" },
  { von: "Sara Yilmaz", ton: "beige", typ: "leihen", teil: "Jeans", teilTon: "ton-beige", bis: null, wann: "vor 3 Tagen" },
];

// Neuigkeiten des Entwicklerteams (Typ Update/Hinweis/Info, ERM Entscheidung 9)
const NEUIGKEITEN_BEISPIEL = [
  { typ: "update", datum: "14.10.2026", gelesen: false, titel: "Neu: Filter für Kleidung und Outfits",
    text: "Du kannst deinen Schrank jetzt nach Farbe, Status, Kaufdatum und Preis filtern. Auch Outfits lassen sich nach Kategorie und enthaltenen Teilen finden.",
    mehr: "Den Filter öffnest du im Kleiderschrank und bei den Outfits über den Knopf „Filter“. Mit „Zurücksetzen“ siehst du wieder alles." },
  { typ: "hinweis", datum: "10.10.2026", gelesen: true, titel: "Wartungsarbeiten am 20.10.2026",
    text: "Zwischen 2 und 4 Uhr nachts ist Sharely kurz nicht erreichbar.",
    mehr: "Deine Daten bleiben dabei unverändert. Danach geht alles wie gewohnt weiter." },
  { typ: "info", datum: "01.10.2026", gelesen: false, titel: "Willkommen bei Sharely!",
    text: "Schön, dass du da bist. Leg deine ersten Kleidungsstücke an und lade Freunde ein.",
    mehr: "Über „Freunde“ findest du andere über ihren Nutzernamen. Was du nicht teilen möchtest, stellst du beim Kleidungsstück auf „Privat“." },
];
