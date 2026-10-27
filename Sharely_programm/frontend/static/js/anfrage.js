// Fenster „Anfrage an …“ (Mockup „Anfrage an Freund – Leihen / Geschenkt bekommen (Fenster)“):
// Ich frage ein Teil eines Freundes an. Wird ein Leihvorgang mit Typ, von, bis (leer = unbefristet) und Notiz
// (ERM Entscheidung 8). Genutzt von freund-schrank.html und freund-garderobe.html. Noch ohne Backend.

let anfrageFenster;

/** Fenster einmal bauen und an den <body> hängen. */
function anfrageFensterBauen() {
  const fenster = document.createElement("dialog");
  fenster.className = "blatt klein";
  fenster.setAttribute("aria-labelledby", "anfrage-titel");
  fenster.innerHTML = `
    <form method="dialog" novalidate>
      <header class="blatt-kopf">
        <h2 id="anfrage-titel"></h2>
        <button type="button" class="symbolknopf" data-schliessen aria-label="Schließen">${SYMBOL.schliessen}</button>
      </header>
      <div class="blatt-inhalt">
        <div class="teil-kopf"><span class="vorschau">${SYMBOL.buegel}</span><span><strong class="a-teil"></strong><small class="a-herkunft"></small></span></div>
        <span class="titel">Was möchtest du?</span>
        <div class="umschalter dunkel" role="radiogroup">
          <button type="button" role="radio" data-typ="leihen">${SYMBOL.links} Leihen</button>
          <button type="button" role="radio" data-typ="verschenken">${SYMBOL.geschenk} Geschenkt bekommen</button>
        </div>
        <div class="a-zeitraum">
          <span class="titel">Gewünschter Zeitraum</span>
          <div class="von-bis">
            <span>von</span><input type="date" name="von" aria-label="Von">
            <span>bis</span><input type="date" name="bis" aria-label="Bis">
          </div>
          <label class="haekchen"><input type="checkbox" name="unbefristet"> Unbefristet</label>
        </div>
        <label><span class="titel"><span class="a-nachricht-titel"></span> <small style="display: inline">(optional)</small></span>
          <textarea name="notiz" maxlength="500" placeholder="z. B. Für die Hochzeit meiner Schwester am 08.11."></textarea></label>
        <div class="meldung" role="status"></div>
      </div>
      <footer class="blatt-fuss">
        <button type="button" class="knopf-rand" data-schliessen>Abbrechen</button>
        <button type="submit" class="knopf">${SYMBOL.senden} Anfrage senden</button>
      </footer>
    </form>`;
  document.body.append(fenster);
  fensterVerdrahten(fenster);

  const f = fenster.querySelector("form");
  const heute = new Date().toISOString().slice(0, 10);
  f.von.min = heute;
  f.bis.min = heute;
  for (const knopf of fenster.querySelectorAll("[data-typ]")) knopf.onclick = () => typSetzen(knopf.dataset.typ);
  f.unbefristet.onchange = () => { f.bis.disabled = f.unbefristet.checked; if (f.unbefristet.checked) f.bis.value = ""; };

  f.onsubmit = (e) => {
    e.preventDefault();
    const meldung = fenster.querySelector(".meldung");
    const leihen = fenster.dataset.typ === "leihen";
    if (leihen && !f.von.value) return zeigeMeldung(meldung, "Bitte angeben, ab wann du das Teil möchtest.", "fehler");
    if (leihen && !f.bis.value && !f.unbefristet.checked) return zeigeMeldung(meldung, "Bitte ein Enddatum wählen oder „Unbefristet“ ankreuzen.", "fehler");
    if (leihen && f.bis.value && f.bis.value < f.von.value) return zeigeMeldung(meldung, "„bis“ liegt vor „von“.", "fehler");
    zeigeMeldung(meldung, `Anfrage an ${fenster.dataset.vorname} wäre jetzt gesendet. Das Backend-Modul verleihen fehlt noch.`, "ok");
  };
  return fenster;
}

function typSetzen(typ) {
  anfrageFenster.dataset.typ = typ;
  for (const knopf of anfrageFenster.querySelectorAll("[data-typ]")) {
    const an = knopf.dataset.typ === typ;
    knopf.classList.toggle("aktiv", an);
    knopf.setAttribute("aria-checked", an);
  }
  anfrageFenster.querySelector(".a-zeitraum").hidden = typ !== "leihen"; // Geschenke haben keinen Zeitraum
}

/** Fenster für ein Teil (aus FREUND_TEILE_BEISPIEL) eines Freundes öffnen. */
function anfrageOeffnen(freund, teil) {
  anfrageFenster ||= anfrageFensterBauen();
  const vorname = freund.name.split(" ")[0];
  anfrageFenster.dataset.vorname = vorname;
  anfrageFenster.querySelector("form").reset();
  anfrageFenster.querySelector("[name=bis]").disabled = false;
  anfrageFenster.querySelector(".meldung").textContent = "";
  anfrageFenster.querySelector("#anfrage-titel").textContent = `Anfrage an ${vorname}`;
  anfrageFenster.querySelector(".a-nachricht-titel").textContent = `Nachricht an ${vorname}`;
  anfrageFenster.querySelector(".vorschau").className = `vorschau ${teil.ton}`;
  anfrageFenster.querySelector(".a-teil").textContent = teil.name;
  anfrageFenster.querySelector(".a-herkunft").textContent = `${KLEIDUNGSARTEN[teil.kleidungsart]} · aus ${genitiv(freund.name)} Kleiderschrank`;
  typSetzen("leihen");
  anfrageFenster.showModal();
}
