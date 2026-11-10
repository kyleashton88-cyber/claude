/* Restored shell behaviour. The original site.js / atlas-shell.js files
   were not in the upload. Enhancers no-op when their markup is absent. */
(function () {
  if (window.__atlasBoot) return;
  window.__atlasBoot = true;

  var MISSING = {
    "/markets/sol": "Solana market page",
    "/markets/link": "Chainlink market page",
    "/markets/sui": "Sui market page",
    "/markets/ltc": "Litecoin market page",
    "/markets/hbar": "Hedera market page",
    "/market-sol": "Solana market page",
    "/market-link": "Chainlink market page",
    "/market-sui": "Sui market page",
    "/market-ltc": "Litecoin market page",
    "/market-hbar": "Hedera market page",
    "/academy/ta": "Technical Analysis module",
    "/academy/structure": "Market Structure module",
    "/academy/risk": "Risk Management module",
    "/academy/02-technical-analysis": "Technical Analysis module",
    "/academy/03-market-structure": "Market Structure module",
    "/academy/04-risk-management": "Risk Management module",
    "/technical-analysis": "Technical Analysis module",
    "/market-structure": "Market Structure module",
    "/risk-academy": "Risk Academy",
    "/tools": "Tools index",
    "/tools/risk-calc": "Risk / position-size calculator",
    "/tools/replay-lab": "Replay Lab",
    "/replay-lab": "Replay Lab",
    "/search": "Library search",
    "/privacy": "Privacy policy",
    "/terms": "Terms of use",
    "/library/module-2": "Market Strategies module",
    "/library/02-market-strategies": "Market Strategies module",
    "/market-strategies": "Market Strategies module",
    "/psychology": "Trading Psychology module",
    "/portfolio-lab": "Portfolio & Capital module",
    "/quant-lab": "Quant & Data Lab",
    "/mastery": "Professional Mastery module",
    "/strategy-library": "Strategy library"
  };

  function pathOf(href) {
    try {
      return new URL(href, location.origin).pathname.replace(/\/$/, "") || "/";
    } catch (e) {
      return "";
    }
  }

  document.querySelectorAll("a[href]").forEach(function (a) {
    var path = pathOf(a.getAttribute("href"));
    if (!MISSING[path] || a.querySelector(".not-in-build")) return;
    var mark = document.createElement("span");
    mark.className = "not-in-build";
    mark.textContent = "Not in this build";
    a.appendChild(mark);
    if (!a.getAttribute("title")) a.setAttribute("title", MISSING[path] + " is not in this build");
  });

  var toggle = document.querySelector("[data-nav-toggle]");
  var nav = document.querySelector("[data-primary-nav]");
  function setNav(open) {
    if (!nav || !toggle) return;
    nav.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
  }
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      setNav(!nav.classList.contains("is-open"));
    });
  }

  document.querySelectorAll(".atlas-unified-trigger").forEach(function (btn) {
    var item = btn.closest(".atlas-unified-nav-item");
    var menu = document.getElementById(btn.getAttribute("aria-controls"));
    if (!menu) return;
    function closeAll(except) {
      document.querySelectorAll(".atlas-unified-dropdown").forEach(function (d) {
        if (d !== except) d.hidden = true;
      });
      document.querySelectorAll(".atlas-unified-trigger").forEach(function (b) {
        if (!except || b.getAttribute("aria-controls") !== except.id) b.setAttribute("aria-expanded", "false");
      });
    }
    function open() {
      closeAll(menu);
      menu.hidden = false;
      btn.setAttribute("aria-expanded", "true");
    }
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      if (menu.hidden) open();
      else closeAll(null);
    });
    if (item) {
      item.addEventListener("mouseenter", function () {
        if (window.matchMedia("(min-width: 981px)").matches) open();
      });
      item.addEventListener("mouseleave", function () {
        if (window.matchMedia("(min-width: 981px)").matches) closeAll(null);
      });
    }
  });

  document.addEventListener("click", function () {
    document.querySelectorAll(".atlas-unified-dropdown").forEach(function (d) { d.hidden = true; });
    document.querySelectorAll(".atlas-unified-trigger").forEach(function (b) { b.setAttribute("aria-expanded", "false"); });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    setNav(false);
    document.querySelectorAll(".atlas-unified-dropdown").forEach(function (d) { d.hidden = true; });
    document.querySelectorAll(".atlas-unified-trigger").forEach(function (b) { b.setAttribute("aria-expanded", "false"); });
  });

  var back = document.querySelector(".backtop");
  if (back) {
    var onScroll = function () { back.classList.toggle("show", window.scrollY > 700); };
    document.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
    back.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  var bar = document.querySelector(".reading-progress");
  if (bar) {
    var paint = function () {
      var d = document.documentElement;
      var max = Math.max(1, d.scrollHeight - d.clientHeight);
      bar.style.transform = "scaleX(" + (d.scrollTop / max) + ")";
    };
    document.addEventListener("scroll", paint, { passive: true });
    paint();
  }

  function toast(msg) {
    var t = document.querySelector(".toast");
    if (!t) return;
    t.textContent = msg;
    t.classList.add("show");
    setTimeout(function () { t.classList.remove("show"); }, 1600);
  }
  document.querySelectorAll("[data-copy-link]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var text = location.href;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () { toast("Link copied"); }, function () { toast(text); });
      } else toast(text);
    });
  });
  document.querySelectorAll("[data-print-pdf]").forEach(function (btn) {
    btn.addEventListener("click", function () { window.print(); });
  });

  function storedCount(key) {
    try {
      var raw = localStorage.getItem(key);
      if (!raw) return null;
      var data = JSON.parse(raw);
      if (Array.isArray(data)) {
        if (key.indexOf("Defi") >= 0) return { done: data.length, total: 42 };
        if (key.indexOf("LearningPath") >= 0) return { done: data.length, total: 4 };
        return { done: data.length, total: data.length };
      }
      if (data && typeof data === "object") {
        var vals = Object.keys(data);
        return { done: vals.filter(function (k) { return !!data[k]; }).length, total: vals.length };
      }
    } catch (e) {}
    return null;
  }
  var progressEl = document.querySelector("[data-global-progress]");
  if (progressEl) {
    var done = 0;
    var total = 0;
    [storedCount("gbbAtlasProgress"), storedCount("atlasDefiOnchainComplete"), storedCount("atlasLearningPathStages")].forEach(function (part) {
      if (!part || !part.total) return;
      done += part.done;
      total += part.total;
    });
    progressEl.textContent = (total ? Math.round(done / total * 100) : 0) + "%";
  }

  var boxes = Array.prototype.slice.call(document.querySelectorAll("[data-stage-check]"));
  if (boxes.length) {
    var stageKey = "atlasLearningPathStages";
    var saved = [];
    try { saved = JSON.parse(localStorage.getItem(stageKey) || "[]"); } catch (e) { saved = []; }
    boxes.forEach(function (box) {
      box.checked = saved.indexOf(box.id) >= 0;
      box.addEventListener("change", function () {
        var ids = boxes.filter(function (b) { return b.checked; }).map(function (b) { return b.id; });
        try { localStorage.setItem(stageKey, JSON.stringify(ids)); } catch (err) {}
        renderStages();
        if (progressEl) {
          var part = storedCount(stageKey);
          var other = [storedCount("gbbAtlasProgress"), storedCount("atlasDefiOnchainComplete")];
          var d = part ? part.done : 0;
          var t = part ? part.total : 0;
          other.forEach(function (p) { if (p && p.total) { d += p.done; t += p.total; } });
          progressEl.textContent = (t ? Math.round(d / t * 100) : 0) + "%";
        }
      });
    });
    function renderStages() {
      var on = boxes.filter(function (b) { return b.checked; }).length;
      var text = document.querySelector("[data-progress-text]");
      var fill = document.querySelector(".progress-fill");
      var pct = Math.round(on / boxes.length * 100);
      if (text) text.textContent = on + " of " + boxes.length + " stages marked complete · " + pct + "%";
      if (fill) fill.style.width = pct + "%";
    }
    renderStages();
  }

  document.querySelectorAll(".microquiz").forEach(function (quiz) {
    quiz.querySelectorAll("button").forEach(function (btn) {
      btn.addEventListener("click", function () {
        quiz.querySelectorAll("button").forEach(function (b) {
          b.classList.remove("is-correct", "is-wrong");
        });
        var ok = btn.hasAttribute("data-correct");
        btn.classList.add(ok ? "is-correct" : "is-wrong");
        var fb = quiz.querySelector(".micro-feedback");
        if (fb) fb.textContent = btn.dataset.feedback || (ok ? "Correct." : (quiz.dataset.hint || "Review the linked lesson and try again."));
      });
    });
  });

  document.querySelectorAll(".market-lab").forEach(function (lab) {
    var svg = lab.querySelector(".candle-svg");
    var sel = lab.querySelector("[data-lab-scenario]");
    var gridBtn = lab.querySelector("[data-lab-grid]");
    var replayBtn = lab.querySelector("[data-lab-replay]");
    var tip = lab.querySelector(".chart-tooltip");
    if (!svg || !sel) return;
    var n = 48;
    var gridOn = true;
    var timer = null;
    function make(kind) {
      var seed = { range: 17, trend: 29, breakout: 43, volatile: 71 }[kind] || 17;
      var price = 100;
      var out = [];
      function rnd() { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; }
      for (var i = 0; i < 48; i++) {
        var drift = kind === "range" ? (100 - price) * 0.13 + Math.sin(i * 0.7) * 0.25
          : kind === "trend" ? 0.31 + Math.sin(i * 0.45) * 0.16
          : kind === "breakout" ? (i < 30 ? Math.sin(i * 0.65) * 0.12 : (i < 38 ? 0.78 : 0.15))
          : (rnd() - 0.5) * 1.3;
        var o = price;
        var c = o + drift + (rnd() - 0.5) * 0.6;
        var w = 0.25 + rnd() * 0.7;
        out.push({ o: o, h: Math.max(o, c) + w, l: Math.min(o, c) - w, c: c });
        price = c;
      }
      return out;
    }
    function metric(name, value) {
      var el = lab.querySelector('[data-metric="' + name + '"]');
      if (el) el.textContent = value;
    }
    function draw() {
      var data = make(sel.value).slice(0, n);
      var W = 1000, H = 320, L = 16, R = 16, T = 16, B = 16;
      var lo = Math.min.apply(null, data.map(function (d) { return d.l; }));
      var hi = Math.max.apply(null, data.map(function (d) { return d.h; }));
      var pad = (hi - lo) * 0.12 || 1;
      lo -= pad; hi += pad;
      function y(v) { return T + (hi - v) / (hi - lo) * (H - T - B); }
      function x(i) { return L + (i + 0.5) * (W - L - R) / 48; }
      var s = "";
      if (gridOn) {
        for (var g = 1; g <= 6; g++) {
          var gy = y(lo + (hi - lo) * (0.2 + g * 0.08));
          s += '<line x1="' + L + '" y1="' + gy.toFixed(1) + '" x2="' + (W - R) + '" y2="' + gy.toFixed(1) + '" stroke="#62d5ff" stroke-opacity="0.35" stroke-dasharray="5 5"/>';
        }
      }
      data.forEach(function (d, i) {
        var xx = x(i);
        var up = d.c >= d.o;
        var col = up ? "#55e7c1" : "#ff7180";
        var top = Math.min(y(d.o), y(d.c));
        var h = Math.max(2, Math.abs(y(d.o) - y(d.c)));
        s += '<g class="candle" data-i="' + i + '">';
        s += '<line x1="' + xx.toFixed(1) + '" y1="' + y(d.h).toFixed(1) + '" x2="' + xx.toFixed(1) + '" y2="' + y(d.l).toFixed(1) + '" stroke="' + col + '"/>';
        s += '<rect x="' + (xx - 6).toFixed(1) + '" y="' + top.toFixed(1) + '" width="12" height="' + h.toFixed(1) + '" fill="' + col + '" rx="1"/>';
        s += "</g>";
      });
      svg.setAttribute("viewBox", "0 0 " + W + " " + H);
      svg.innerHTML = s;
      var last = data[data.length - 1];
      metric("price", last.c.toFixed(2));
      metric("range", (hi - lo).toFixed(2));
      metric("candles", String(data.length));
      metric("regime", { range: "Two-way range", trend: "Directional", breakout: "Range break", volatile: "High volatility" }[sel.value] || "Illustrative");
      svg._candles = data;
    }
    svg.addEventListener("pointermove", function (e) {
      if (!tip || !svg._candles) return;
      var rect = svg.getBoundingClientRect();
      var idx = Math.max(0, Math.min(svg._candles.length - 1, Math.floor((e.clientX - rect.left) / rect.width * 48)));
      var d = svg._candles[idx];
      if (!d) return;
      tip.textContent = "O " + d.o.toFixed(2) + "  H " + d.h.toFixed(2) + "  L " + d.l.toFixed(2) + "  C " + d.c.toFixed(2);
    });
    sel.addEventListener("change", function () {
      clearInterval(timer);
      n = 48;
      if (replayBtn) replayBtn.disabled = false;
      draw();
    });
    if (gridBtn) gridBtn.addEventListener("click", function () {
      gridOn = !gridOn;
      gridBtn.classList.toggle("active", gridOn);
      gridBtn.setAttribute("aria-pressed", gridOn ? "true" : "false");
      draw();
    });
    if (replayBtn) replayBtn.addEventListener("click", function () {
      clearInterval(timer);
      n = 6;
      draw();
      replayBtn.disabled = true;
      timer = setInterval(function () {
        n += 1;
        draw();
        if (n >= 48) { clearInterval(timer); replayBtn.disabled = false; }
      }, 90);
    });
    draw();
  });

  var notice = document.getElementById("notice-current");
  if (notice) {
    var here = (location.pathname.replace(/\/$/, "") || "/");
    var name = MISSING[here];
    notice.hidden = !name;
    if (name) notice.textContent = "You opened " + here + " — " + name + ".";
  }
})();
