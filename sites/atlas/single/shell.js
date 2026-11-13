(function () {
  "use strict";
  var data = window.ATLAS;
  var seenKey = "atlas-path-seen";
  var checkKey = "atlas-study-checks";
  var memorySeen = [];
  var memoryChecks = {};
  var booted = false;

  function readJson(key, fallback) {
    try { return JSON.parse(localStorage.getItem(key)) || fallback; }
    catch (e) { return fallback; }
  }
  function writeJson(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); }
    catch (e) { /* file origins can block storage; memory copies still work */ }
  }
  function seen() {
    var stored = readJson(seenKey, null);
    return stored || memorySeen;
  }
  function markSeen(id) {
    var ids = data.path.map(function (step) { return step.id; });
    if (ids.indexOf(id) === -1) return;
    var list = seen().slice();
    if (list.indexOf(id) === -1) list.push(id);
    memorySeen = list;
    writeJson(seenKey, list);
    paintProgress();
  }
  function checks() {
    return readJson(checkKey, null) || memoryChecks;
  }
  function paintProgress() {
    var el = document.getElementById("path-progress");
    if (!el) return;
    el.textContent = seen().length + " of " + data.path.length + " steps opened on this device";
  }

  function parseHash() {
    var raw = location.hash.replace(/^#/, "") || "/";
    try { raw = decodeURIComponent(raw); } catch (e) { /* keep raw */ }
    if (raw.charAt(0) !== "/") raw = "/" + raw;
    var query = "";
    var q = raw.indexOf("?");
    if (q >= 0) { query = raw.slice(q + 1); raw = raw.slice(0, q); }
    var parts = raw.split("/").filter(Boolean);
    return { parts: parts, query: new URLSearchParams(query) };
  }

  function resolve(parts) {
    var key = parts.join("/");
    if (!parts.length || key === "home") return { page: "home" };
    if (parts[0] === "markets" && parts[1] && data.markets[parts[1]]) {
      return { page: "market:" + parts[1], anchor: parts[2] || "" };
    }
    if (data.pages[key]) return { page: key };
    if (parts.length > 1) {
      var parent = parts.slice(0, -1).join("/");
      if (data.pages[parent]) return { page: parent, anchor: parts[parts.length - 1] };
    }
    if (parts[0] === "search") return { page: "search" };
    return { page: "missing", missing: key };
  }

  function frame(page, body) {
    var fits = page.fitsHref
      ? '<p class="fits">This fits <a href="#/' + page.fitsHref + '">' + escapeHtml(page.fitsLabel) + "</a>.</p>"
      : "";
    var banner = page.banner ? '<div class="draft">' + page.banner + "</div>" : "";
    return (
      '<p class="learn">What you\'ll learn about grid bots here: ' + escapeHtml(page.learn) + "</p>" +
      "<h1>" + escapeHtml(page.title) + "</h1>" +
      fits + banner +
      '<div class="prose">' + body + "</div>" +
      '<p class="next"><span class="next-label">Next step</span> <a href="#/' + page.next + '">' + escapeHtml(page.nextLabel) + "</a></p>"
    );
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function renderGlossary(anchor) {
    var letters = {};
    data.glossary.forEach(function (term) {
      var letter = (term.term[0] || "#").toUpperCase();
      if (!/[A-Z]/.test(letter)) letter = "#";
      (letters[letter] = letters[letter] || []).push(term);
    });
    var keys = Object.keys(letters).sort();
    var alpha = keys.map(function (k) {
      return '<a href="#/glossary/letter-' + encodeURIComponent(k) + '">' + k + "</a>";
    }).join("");
    var cats = {};
    data.glossary.forEach(function (t) { cats[t.category] = true; });
    var options = Object.keys(cats).sort().map(function (c) {
      return '<option value="' + escapeHtml(c) + '">' + escapeHtml(c) + "</option>";
    }).join("");
    var blocks = keys.map(function (k) {
      var items = letters[k].map(function (t) {
        var see = (t.see_also || []).map(function (id) {
          var match = data.glossary.filter(function (g) { return g.anchor === id; })[0];
          var label = match ? match.term : id;
          return '<a href="#/glossary/' + encodeURIComponent(id) + '">' + escapeHtml(label) + "</a>";
        }).join(", ");
        return (
          '<article class="term" id="' + escapeHtml(t.anchor) + '" data-cat="' + escapeHtml(t.category) + '" data-name="' + escapeHtml(t.term.toLowerCase()) + '">' +
          "<h2>" + escapeHtml(t.term) + "</h2>" +
          "<p><strong>" + escapeHtml(t.one_liner) + "</strong></p>" +
          "<p>" + escapeHtml(t.explanation) + "</p>" +
          '<p class="fits">Category: ' + escapeHtml(t.category) + " · " + escapeHtml(t.level) +
          (see ? ". See also: " + see : "") + ".</p></article>"
        );
      }).join("");
      return '<h2 id="letter-' + escapeHtml(k) + '">' + escapeHtml(k) + "</h2>" + items;
    }).join("");
    var page = data.pages.glossary;
    return frame(page,
      '<div class="filter-bar"><label>Filter <input id="glossary-filter" type="search" placeholder="Type a word"></label>' +
      '<label>Category <select id="glossary-cat"><option value="">All words</option>' + options + "</select></label></div>" +
      '<nav class="alpha" aria-label="Letters">' + alpha + "</nav>" + blocks
    );
  }

  function renderMarket(id) {
    var m = data.markets[id];
    var series = m.series || {};
    var keys = Object.keys(series);
    var controls = keys.length
      ? '<div class="chart-wrap"><div class="replay"><label>Sample timeframe <select class="js-tf">' +
        keys.map(function (k) { return '<option value="' + k + '">' + k + "</option>"; }).join("") +
        '</select></label><label>Bars shown <input class="js-replay" type="range" min="20" value="240"></label></div>' +
        '<canvas class="chart js-chart" aria-hidden="true"></canvas><p class="js-chart-summary"></p></div>'
      : "<p>This asset has a short primer in the file and no bundled candle sample. Use a charted sample, such as Bitcoin or Solana, to practise the same question: did price spend time going back and forth inside a box?</p>";
    var page = {
      title: m.name,
      learn: m.learn,
      fitsHref: "path/range",
      fitsLabel: "step 4, choosing ranges and grids",
      next: "path/range",
      nextLabel: "Choosing ranges and grids"
    };
    return frame(page, "<p>" + escapeHtml(m.blurb) + "</p>" + controls + (m.primer || ""));
  }

  function renderSearch(query) {
    var q = (query.get("q") || "").trim();
    var page = data.pages.search;
    var results = "";
    if (q) {
      var needle = q.toLowerCase();
      var hits = [];
      Object.keys(data.pages).forEach(function (id) {
        if (id === "search" || id === "missing") return;
        var p = data.pages[id];
        var hay = (p.title + " " + p.learn + " " + (p.text || "")).toLowerCase();
        if (hay.indexOf(needle) !== -1) hits.push({ href: "#/" + id, title: p.title, kind: "Page", note: p.learn });
      });
      data.glossary.forEach(function (t) {
        var hay = (t.term + " " + t.one_liner + " " + t.explanation).toLowerCase();
        if (hay.indexOf(needle) !== -1) hits.push({ href: "#/glossary/" + encodeURIComponent(t.anchor), title: t.term, kind: "Glossary", note: t.one_liner });
      });
      Object.keys(data.markets).forEach(function (id) {
        var m = data.markets[id];
        var hay = (m.name + " " + m.blurb + " " + (m.text || "")).toLowerCase();
        if (hay.indexOf(needle) !== -1) hits.push({ href: "#/markets/" + id, title: m.name, kind: "Market", note: m.blurb });
      });
      results = hits.length
        ? '<p>' + hits.length + ' matches for “' + escapeHtml(q) + '”.</p><ul class="index">' + hits.slice(0, 40).map(function (h) {
          return '<li><a href="' + h.href + '"><strong>' + escapeHtml(h.title) + "</strong><span>" + escapeHtml(h.kind) + " · " + escapeHtml(h.note) + "</span></a></li>";
        }).join("") + "</ul>"
        : "<p>No match. Try a shorter word, such as range, fee, or stop.</p>";
    } else {
      results = "<p>Type a word in the search box. The search looks through lesson titles and the glossary saved in this file.</p>";
    }
    return frame(page, results);
  }

  function render() {
    var parsed = parseHash();
    var route = resolve(parsed.parts);
    if (route.page === "search") route.query = parsed.query;
    var html;
    var pageId = route.page;
    if (route.page === "glossary") html = renderGlossary(route.anchor);
    else if (route.page.indexOf("market:") === 0) {
      pageId = "markets/" + route.page.slice(7);
      html = renderMarket(route.page.slice(7));
    } else if (route.page === "search") html = renderSearch(parsed.query);
    else if (route.page === "missing") {
      html = frame(data.pages.missing, "<p>There is no lesson at <span class=\"fits\">" + escapeHtml(route.missing) + "</span>. Choose a step on the path, or search for the word you need.</p>");
      pageId = "missing";
    } else html = frame(data.pages[route.page], data.pages[route.page].html);

    var main = document.getElementById("main");
    main.innerHTML = html;
    document.title = (main.querySelector("h1") ? main.querySelector("h1").textContent : "Atlas") + " — Atlas";
    markSeen(pageId.indexOf("path/") === 0 ? pageId : "");
    setCurrent(pageId);
    bind(main, route);
    var focusTarget = route.anchor && document.getElementById(route.anchor);
    if (!focusTarget) focusTarget = main.querySelector("h1");
    if (booted && focusTarget) {
      if (!focusTarget.hasAttribute("tabindex")) focusTarget.setAttribute("tabindex", "-1");
      focusTarget.focus();
    }
    if (route.anchor && document.getElementById(route.anchor)) {
      document.getElementById(route.anchor).scrollIntoView();
    } else if (booted) {
      window.scrollTo(0, 0);
    }
    booted = true;
    closeNav(false);
  }

  function setCurrent(pageId) {
    document.querySelectorAll("[data-nav]").forEach(function (a) {
      var id = a.getAttribute("data-nav");
      var on = pageId === id || (id !== "home" && pageId.indexOf(id + "/") === 0) || (id === "markets" && pageId.indexOf("markets/") === 0);
      if (on) a.setAttribute("aria-current", "page");
      else a.removeAttribute("aria-current");
    });
  }

  function closeNav(returnFocus) {
    document.body.classList.remove("nav-open");
    var btn = document.getElementById("menu-btn");
    if (btn) btn.setAttribute("aria-expanded", "false");
    if (returnFocus && btn) btn.focus();
  }

  function num(v) {
    var n = Number(v);
    return isFinite(n) ? n : NaN;
  }
  function money(n) {
    return n.toLocaleString(undefined, { maximumFractionDigits: 2 });
  }

  function sizePosition(input) {
    var account = num(input.account), riskPct = num(input.riskPct), entry = num(input.entry), stop = num(input.stop);
    var feeBps = num(input.feeBps), slipBps = num(input.slipBps), leverage = num(input.leverage);
    if (!isFinite(feeBps) || feeBps < 0) feeBps = 0;
    if (!isFinite(slipBps) || slipBps < 0) slipBps = 0;
    if (!(account > 0) || !(riskPct > 0) || !(entry > 0) || !(stop > 0)) return { error: "Enter a positive account, risk percent, entry, and stop." };
    var distance = Math.abs(entry - stop);
    if (distance === 0) return { error: "The stop has to be a different price from the entry." };
    var riskCash = account * (riskPct / 100);
    var qty = riskCash / distance;
    var notional = qty * entry;
    var friction = notional * ((feeBps + slipBps) / 10000) * 2;
    var implied = notional / account;
    var mode = input.mode === "futures" ? "futures" : "spot";
    var warning = "";
    if (mode === "spot" && implied > 1.001) warning = "The notional is larger than the account. On spot, that means the position needs more cash than the account figure, or the stop is very close.";
    if (mode === "futures" && isFinite(leverage) && leverage > 0 && implied > leverage + 0.001) warning = "Risk-based size implies about " + implied.toFixed(2) + "×, above the leverage cap you entered.";
    return { qty: qty, notional: notional, riskCash: riskCash, distancePct: distance / entry * 100, friction: friction, lossAtStop: riskCash + friction, impliedLeverage: implied, warning: warning, side: stop < entry ? "long" : "short" };
  }

  function gridLevels(lower, upper, gaps, mode) {
    var levels = [];
    var i;
    if (mode === "geometric") {
      var ratio = Math.pow(upper / lower, 1 / gaps);
      for (i = 0; i <= gaps; i++) levels.push(lower * Math.pow(ratio, i));
    } else {
      var step = (upper - lower) / gaps;
      for (i = 0; i <= gaps; i++) levels.push(lower + step * i);
    }
    return levels;
  }

  function bind(root, route) {
    root.querySelectorAll("[data-mount]").forEach(function (el) {
      var kind = el.getAttribute("data-mount");
      if (kind === "risk") el.innerHTML = riskForm();
      if (kind === "grid") el.innerHTML = gridForm();
      if (kind === "journal") el.innerHTML = journalForm();
    });
    root.querySelectorAll("form.js-risk").forEach(function (form) {
      var read = function () {
        var result = sizePosition({
          account: form.account.value, riskPct: form.riskPct.value, entry: form.entry.value, stop: form.stop.value,
          feeBps: form.feeBps.value, slipBps: form.slipBps.value, leverage: form.leverage.value, mode: form.mode.value
        });
        var warn = form.querySelector(".warning");
        if (result.error) { warn.textContent = result.error; return; }
        form.querySelector("[data-out=qty]").textContent = result.qty.toLocaleString(undefined, { maximumFractionDigits: 6 });
        form.querySelector("[data-out=notional]").textContent = money(result.notional);
        form.querySelector("[data-out=cash]").textContent = money(result.riskCash);
        form.querySelector("[data-out=distance]").textContent = result.distancePct.toFixed(2) + "%";
        form.querySelector("[data-out=friction]").textContent = money(result.friction);
        form.querySelector("[data-out=loss]").textContent = money(result.lossAtStop);
        form.querySelector("[data-out=implied]").textContent = result.impliedLeverage.toFixed(2) + "×";
        warn.textContent = "Hypothetical " + result.side + " model. Fees and slippage are applied on the way in and the way out. This is not an order." + (result.warning ? " " + result.warning : "");
      };
      form.addEventListener("input", read);
      read();
    });
    root.querySelectorAll("form.js-grid").forEach(function (form) {
      var read = function () {
        var lower = num(form.lower.value), upper = num(form.upper.value), gaps = num(form.gaps.value);
        var feeBps = num(form.feeBps.value), capital = num(form.capital.value);
        var warn = form.querySelector(".warning");
        if (!(lower > 0) || !(upper > lower) || !(gaps >= 1)) { warn.textContent = "Enter a lower price, a higher upper price, and at least one gap."; return; }
        gaps = Math.round(gaps);
        var levels = gridLevels(lower, upper, gaps, form.mode.value);
        var gapsCash = [];
        var tight = false;
        for (var i = 0; i < levels.length - 1; i++) {
          var gap = levels[i + 1] - levels[i];
          var fee = levels[i] * 2 * (feeBps / 10000);
          if (gap <= fee) tight = true;
          gapsCash.push(gap);
        }
        var per = capital > 0 ? capital / gaps : NaN;
        form.querySelector("[data-out=step]").textContent = form.mode.value === "geometric"
          ? "percentage steps, smallest gap " + gapsCash[0].toFixed(4)
          : gapsCash[0].toFixed(4) + " price units";
        form.querySelector("[data-out=levels]").textContent = levels.map(function (n) { return n.toFixed(4); }).join(", ");
        form.querySelector("[data-out=per]").textContent = isFinite(per) ? money(per) : "—";
        warn.textContent = tight
          ? "Hypothetical model. At least one gap is smaller than the round-trip fee on one unit at that level. More fills would not repair that. This is not an order."
          : "Hypothetical model. The smallest gap is larger than the round-trip fee on one unit in this example. Real fills also pay spread and slippage. This is not an order.";
      };
      form.addEventListener("input", read);
      read();
    });
    root.querySelectorAll("form.js-journal").forEach(function (form) {
      var read = function () {
        var rows = form.sample.value.split(/\n/).map(function (line) { return line.trim(); }).filter(function (line) { return line && line.charAt(0) !== "#"; });
        var values = [];
        var bad = false;
        rows.forEach(function (line) {
          var n = Number(line);
          if (!isFinite(n)) bad = true;
          else values.push(n);
        });
        var warn = form.querySelector(".warning");
        if (!values.length || bad) { warn.textContent = bad ? "Each line should be one number, in R." : "Paste one result per line."; return; }
        var wins = values.filter(function (n) { return n > 0; });
        var losses = values.filter(function (n) { return n < 0; });
        var avg = function (arr) { return arr.length ? arr.reduce(function (a, b) { return a + b; }, 0) / arr.length : 0; };
        var expectancy = (wins.length / values.length) * avg(wins) + (losses.length / values.length) * avg(losses);
        var peak = 0, equity = 0, dd = 0;
        values.forEach(function (n) {
          equity += n;
          peak = Math.max(peak, equity);
          dd = Math.min(dd, equity - peak);
        });
        form.querySelector("[data-out=count]").textContent = String(values.length);
        form.querySelector("[data-out=expectancy]").textContent = expectancy.toFixed(3) + " R";
        form.querySelector("[data-out=dd]").textContent = dd.toFixed(3) + " R";
        warn.textContent = "Hypothetical journal. Expectancy is the average R per row. Drawdown is the deepest drop in the running sum. This is not a forecast.";
      };
      form.addEventListener("input", read);
      read();
    });
    root.querySelectorAll("form.js-quiz").forEach(function (form) {
      form.querySelector(".js-quiz-check").addEventListener("click", function () {
        var fields = form.querySelectorAll("fieldset");
        var correct = 0;
        fields.forEach(function (fs) {
          var picked = fs.querySelector("input:checked");
          if (picked && picked.value === fs.getAttribute("data-answer")) correct += 1;
        });
        form.querySelector(".quiz-result").textContent = correct + " of " + fields.length + " match the lesson. The point is the reason, not the score. This is a reading check, not a test of you as a trader.";
      });
    });
    var filter = root.querySelector("#glossary-filter");
    var cat = root.querySelector("#glossary-cat");
    if (filter) {
      var apply = function () {
        var q = filter.value.trim().toLowerCase();
        var c = cat.value;
        root.querySelectorAll(".term").forEach(function (term) {
          var show = (!q || term.getAttribute("data-name").indexOf(q) !== -1 || term.textContent.toLowerCase().indexOf(q) !== -1) && (!c || term.getAttribute("data-cat") === c);
          term.hidden = !show;
        });
      };
      filter.addEventListener("input", apply);
      cat.addEventListener("change", apply);
    }
    root.querySelectorAll("[data-save]").forEach(function (box) {
      var saved = checks();
      box.checked = !!saved[box.getAttribute("data-save")];
      box.addEventListener("change", function () {
        var all = checks();
        all[box.getAttribute("data-save")] = box.checked;
        memoryChecks = all;
        writeJson(checkKey, all);
      });
    });
    var canvas = root.querySelector(".js-chart");
    if (canvas && route.page.indexOf("market:") === 0) {
      var market = data.markets[route.page.slice(7)];
      var tf = root.querySelector(".js-tf");
      var slider = root.querySelector(".js-replay");
      var draw = function () {
        var series = market.series[tf.value];
        var previousMax = Number(slider.max);
        slider.max = String(series.length);
        if (!slider.dataset.ready || previousMax === 100) {
          slider.value = String(series.length);
          slider.dataset.ready = "1";
        } else if (Number(slider.value) > series.length) {
          slider.value = String(series.length);
        }
        var upto = Number(slider.value);
        paintCandles(canvas, series.slice(0, upto));
        var highs = series.slice(0, upto).map(function (c) { return c.high; });
        var lows = series.slice(0, upto).map(function (c) { return c.low; });
        var hi = Math.max.apply(null, highs);
        var lo = Math.min.apply(null, lows);
        root.querySelector(".js-chart-summary").textContent = "Study series, " + tf.value + ", " + upto + " bars. Highest " + hi.toFixed(2) + ", lowest " + lo.toFixed(2) + ". Not a live quote and not a historical claim. Ask whether price went back and forth, or left and did not return.";
      };
      tf.addEventListener("change", draw);
      slider.addEventListener("input", draw);
      draw();
    }
  }

  function paintCandles(canvas, candles) {
    var ctx = canvas.getContext("2d");
    var dpr = window.devicePixelRatio || 1;
    var w = canvas.clientWidth || 640;
    var h = canvas.clientHeight || 240;
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);
    if (!candles.length) return;
    var lo = Infinity, hi = -Infinity;
    candles.forEach(function (c) { lo = Math.min(lo, c.low); hi = Math.max(hi, c.high); });
    var pad = (hi - lo) * 0.08 || 1;
    lo -= pad; hi += pad;
    var y = function (p) { return (1 - (p - lo) / (hi - lo)) * (h - 16) + 8; };
    var slot = w / candles.length;
    ctx.fillStyle = "#d5e4f0";
    ctx.font = "12px 'IBM Plex Mono', monospace";
    ctx.fillText(hi.toFixed(2), 6, 14);
    ctx.fillText(lo.toFixed(2), 6, h - 4);
    candles.forEach(function (c, i) {
      var x = i * slot + slot / 2;
      var up = c.close >= c.open;
      ctx.strokeStyle = up ? "#8ddec0" : "#ffb4b4";
      ctx.fillStyle = ctx.strokeStyle;
      ctx.beginPath();
      ctx.moveTo(x, y(c.high));
      ctx.lineTo(x, y(c.low));
      ctx.stroke();
      var top = y(Math.max(c.open, c.close));
      var bot = y(Math.min(c.open, c.close));
      ctx.fillRect(x - Math.max(1.2, slot * 0.28), top, Math.max(2, slot * 0.56), Math.max(1, bot - top));
    });
  }

  function riskForm() {
    return (
      '<form class="js-risk" data-risk-calc>' +
      '<div class="fields">' +
      '<label>Mode <select name="mode"><option value="spot">Spot</option><option value="futures">Futures</option></select></label>' +
      '<label>Account <input name="account" type="number" min="0" step="1" value="10000"></label>' +
      '<label>Risk percent <input name="riskPct" type="number" min="0" step="0.1" value="1"></label>' +
      '<label>Entry <input name="entry" type="number" min="0" step="any" value="100"></label>' +
      '<label>Stop <input name="stop" type="number" min="0" step="any" value="95"></label>' +
      '<label>Fee, basis points <input name="feeBps" type="number" min="0" step="1" value="10"></label>' +
      '<label>Slippage, basis points <input name="slipBps" type="number" min="0" step="1" value="5"></label>' +
      '<label>Leverage cap <input name="leverage" type="number" min="0" step="0.1" value="2"></label>' +
      "</div>" +
      '<div class="results"><div><dt>Quantity</dt><dd data-out="qty"></dd></div><div><dt>Notional</dt><dd data-out="notional"></dd></div><div><dt>Cash at risk</dt><dd data-out="cash"></dd></div><div><dt>Stop distance</dt><dd data-out="distance"></dd></div><div><dt>Fee and slippage</dt><dd data-out="friction"></dd></div><div><dt>Loss if stopped</dt><dd data-out="loss"></dd></div><div><dt>Implied leverage</dt><dd data-out="implied"></dd></div></div>' +
      '<p class="warning" role="status"></p></form>'
    );
  }
  function gridForm() {
    return (
      '<form class="js-grid">' +
      '<div class="fields">' +
      '<label>Lower price <input name="lower" type="number" min="0" step="any" value="100"></label>' +
      '<label>Upper price <input name="upper" type="number" min="0" step="any" value="110"></label>' +
      '<label>Gaps <input name="gaps" type="number" min="1" step="1" value="5"></label>' +
      '<label>Spacing <select name="mode"><option value="arithmetic">Arithmetic, equal price gaps</option><option value="geometric">Geometric, equal percentage gaps</option></select></label>' +
      '<label>Capital for the split <input name="capital" type="number" min="0" step="1" value="1000"></label>' +
      '<label>Fee, basis points each side <input name="feeBps" type="number" min="0" step="1" value="10"></label>' +
      "</div>" +
      '<div class="results"><div><dt>Gap</dt><dd data-out="step"></dd></div><div><dt>Cash per gap, equal split</dt><dd data-out="per"></dd></div></div>' +
      '<p><span>Levels: </span><span data-out="levels"></span></p>' +
      '<p class="warning" role="status"></p></form>'
    );
  }
  function journalForm() {
    return (
      '<form class="js-journal"><label>Results in R, one per line <textarea class="journal-box" name="sample">1\n-1\n1.5\n-1\n0.5\n-1\n2</textarea></label>' +
      '<div class="results"><div><dt>Rows</dt><dd data-out="count"></dd></div><div><dt>Expectancy</dt><dd data-out="expectancy"></dd></div><div><dt>Deepest drop</dt><dd data-out="dd"></dd></div></div>' +
      '<p class="warning" role="status"></p></form>'
    );
  }

  function buildNav() {
    var path = data.path.map(function (step, i) {
      return '<li><a data-nav="' + step.id + '" href="#/' + step.id + '"><span class="step-num">' + (i + 1) + '</span><span>' + escapeHtml(step.label) + "</span></a></li>";
    }).join("");
    var directory = data.directory.map(function (item) {
      return '<li><a data-nav="' + item.id + '" href="#/' + item.id + '">' + escapeHtml(item.label) + "</a></li>";
    }).join("");
    document.getElementById("path-nav").innerHTML =
      '<p id="path-progress"></p><h2>The path</h2><ol>' + path + '</ol><h2>Directory</h2><ul>' + directory + "</ul>";
    paintProgress();
  }

  document.getElementById("menu-btn").addEventListener("click", function () {
    var open = !document.body.classList.contains("nav-open");
    document.body.classList.toggle("nav-open", open);
    this.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) {
      var first = document.querySelector("#path-nav a");
      if (first) first.focus();
    }
  });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") closeNav(true);
  });
  document.getElementById("search-form").addEventListener("submit", function (event) {
    event.preventDefault();
    var value = document.getElementById("q").value.trim();
    location.hash = "#/search?q=" + encodeURIComponent(value);
  });
  window.addEventListener("hashchange", render);
  buildNav();
  render();

  window.atlasSelfTest = function () {
    var failures = [];
    var a = sizePosition({ account: 10000, riskPct: 1, entry: 100, stop: 95, feeBps: 10, slipBps: 5, leverage: 2, mode: "spot" });
    if (Math.abs(a.qty - 20) > 1e-9) failures.push("qty");
    if (Math.abs(a.notional - 2000) > 1e-6) failures.push("notional");
    if (Math.abs(a.friction - 6) > 1e-6) failures.push("friction");
    if (a.side !== "long") failures.push("side");
    var b = sizePosition({ account: 1000, riskPct: 10, entry: 100, stop: 99, feeBps: 0, slipBps: 0, leverage: 2, mode: "futures" });
    if (!b.warning || b.impliedLeverage < 2) failures.push("leverage warning");
    var same = sizePosition({ account: 10, riskPct: 1, entry: 5, stop: 5, feeBps: 0, slipBps: 0, leverage: 1, mode: "spot" });
    if (!same.error) failures.push("equal stop");
    var levels = gridLevels(100, 110, 5, "arithmetic");
    if (Math.abs(levels[1] - 102) > 1e-9 || Math.abs(levels[5] - 110) > 1e-9) failures.push("arithmetic");
    var geo = gridLevels(100, 110, 5, "geometric");
    if (Math.abs(geo[0] - 100) > 1e-6 || Math.abs(geo[5] - 110) > 1e-4) failures.push("geometric");
    return { ok: failures.length === 0, failures: failures };
  };
})();
