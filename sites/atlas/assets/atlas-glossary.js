(function () {
  var app = document.querySelector("[data-atlas-glossary]");
  if (!app) return;
  var terms = [], letter = "all";
  var learn = {
    grid: "/grid-bot#glossary",
    "market-structure": "/market-structure",
    "technical-analysis": "/technical-analysis#indicators",
    risk: "/risk-academy",
    derivatives: "/futures-leverage",
    execution: "/exchanges",
    security: "/security",
    crypto: "/crypto-fundamentals",
    defi: "/defi-onchain",
    "on-chain": "/defi-onchain",
    portfolio: "/library",
    research: "/journal-lab",
    automation: "/automation",
    psychology: "/library",
    macro: "/macro-lab"
  };
  var live = {
    rsi: { overlays: "", pane: "rsi" },
    macd: { overlays: "", pane: "macd" },
    vwap: { overlays: "vwap", pane: "" },
    atr: { overlays: "", pane: "atr" },
    "bollinger-bands": { overlays: "bb20", pane: "" },
    "exponential-moving-average": { overlays: "ema20", pane: "" },
    "simple-moving-average": { overlays: "sma50", pane: "" },
    volume: { overlays: "", pane: "volume" }
  };
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function render() {
    var q = (app.querySelector("[data-glossary-q]").value || "").toLowerCase();
    var cat = app.querySelector("[data-glossary-cat]").value;
    var level = app.querySelector("[data-glossary-level]").value;
    var list = app.querySelector("[data-glossary-list]");
    list.innerHTML = "";
    var shown = 0;
    terms.forEach(function (term) {
      var L = (term.term || "?").charAt(0).toUpperCase();
      if (letter !== "all" && L !== letter) return;
      if (cat && term.category !== cat) return;
      if (level && term.level !== level) return;
      var blob = (term.term + " " + term.one_liner + " " + term.explanation).toLowerCase();
      if (q && blob.indexOf(q) < 0) return;
      shown += 1;
      var article = el("article", "term");
      article.id = term.anchor;
      article.appendChild(el("h2", null, term.term));
      article.appendChild(el("p", "def", term.one_liner));
      article.appendChild(el("p", null, term.explanation));
      article.appendChild(el("p", "meta", term.level + " · " + term.category));
      if (live[term.anchor]) {
        var btn = el("button", "btn", "See it on a chart");
        btn.type = "button";
        btn.addEventListener("click", function () {
          var box = document.getElementById("glossaryChart");
          if (!box || !window.AtlasLiveChart) return;
          var spec = live[term.anchor];
          window.AtlasLiveChart.configure(box, { symbol: "BTCUSDT", tf: "1h", overlays: spec.overlays, pane: spec.pane });
          box.scrollIntoView({ behavior: "smooth", block: "center" });
        });
        article.appendChild(btn);
      }
      if (term.see_also && term.see_also.length) {
        var see = el("p");
        see.appendChild(document.createTextNode("See also: "));
        term.see_also.forEach(function (id, i) {
          if (i) see.appendChild(document.createTextNode(", "));
          var a = el("a", null, id);
          a.href = "#" + id;
          see.appendChild(a);
        });
        article.appendChild(see);
      }
      var more = el("p");
      var href = learn[term.category] || "/library";
      var a2 = el("a", null, "Learn more");
      a2.href = href;
      more.appendChild(a2);
      article.appendChild(more);
      list.appendChild(article);
    });
    app.querySelector("[data-glossary-count]").textContent = shown + " terms";
    if (location.hash) {
      var target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
      if (target) target.scrollIntoView();
    }
  }
  fetch("/data/glossary.json").then(function (r) { return r.json(); }).then(function (data) {
    terms = data;
    var cats = {}, levels = {};
    terms.forEach(function (t) { cats[t.category] = 1; levels[t.level] = 1; });
    var catSel = app.querySelector("[data-glossary-cat]");
    Object.keys(cats).sort().forEach(function (c) {
      var o = document.createElement("option");
      o.value = c; o.textContent = c; catSel.appendChild(o);
    });
    var lvl = app.querySelector("[data-glossary-level]");
    Object.keys(levels).sort().forEach(function (c) {
      var o = document.createElement("option");
      o.value = c; o.textContent = c; lvl.appendChild(o);
    });
    app.querySelector("[data-glossary-q]").addEventListener("input", render);
    catSel.addEventListener("change", render);
    lvl.addEventListener("change", render);
    var letters = app.querySelector(".atlas-letters");
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("").forEach(function (ch) {
      var b = el("button", "atlas-letter", ch);
      b.type = "button";
      b.setAttribute("data-letter", ch);
      letters.appendChild(b);
    });
    letters.addEventListener("click", function (e) {
      var b = e.target.closest("[data-letter]");
      if (!b) return;
      letter = b.getAttribute("data-letter");
      letters.querySelectorAll("[data-letter]").forEach(function (n) { n.classList.toggle("is-on", n === b); });
      render();
    });
    render();
  }).catch(function () {
    app.querySelector("[data-glossary-list]").textContent = "The glossary file did not load.";
  });
})();
