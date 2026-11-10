/* Market pages describe a live educational chart. This restores that chart
   from public klines. It does not invent prices when the feed is down, and
   it does not label trades. */
(function () {
  var root = document.querySelector("[data-market-page]");
  if (!root) return;
  var symbol = root.dataset.symbol;
  var decimals = Number(root.dataset.decimals || 2);
  var tf = "1h";
  var show = { ema20: true, ema50: false, volume: true, rsi: false };
  var candles = [];
  var chart, candleSeries, ema20Series, ema50Series, volumeSeries, rsiChart, rsiSeries;

  function text(id, value) {
    var el = document.getElementById(id);
    if (el) el.textContent = value;
  }
  function money(n) {
    if (!Number.isFinite(n)) return "—";
    return n.toLocaleString(undefined, { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
  }

  function ema(values, period) {
    var k = 2 / (period + 1);
    var out = [];
    var prev = null;
    values.forEach(function (v, i) {
      if (i < period - 1) { out.push(null); return; }
      if (prev == null) {
        var slice = values.slice(0, period);
        prev = slice.reduce(function (a, b) { return a + b; }, 0) / period;
      } else prev = v * k + prev * (1 - k);
      out.push(prev);
    });
    return out;
  }
  function rsi(values, period) {
    var out = [];
    var gains = 0;
    var losses = 0;
    for (var i = 0; i < values.length; i++) {
      if (i === 0) { out.push(null); continue; }
      var change = values[i] - values[i - 1];
      if (i <= period) {
        if (i < period) { gains += Math.max(change, 0); losses += Math.max(-change, 0); out.push(null); continue; }
        gains = (gains + Math.max(change, 0)) / period;
        losses = (losses + Math.max(-change, 0)) / period;
      } else {
        gains = (gains * (period - 1) + Math.max(change, 0)) / period;
        losses = (losses * (period - 1) + Math.max(-change, 0)) / period;
      }
      var rs = losses === 0 ? 100 : gains / losses;
      out.push(100 - 100 / (1 + rs));
    }
    return out;
  }

  function ensureCharts() {
    if (chart || typeof LightweightCharts === "undefined") return;
    var main = document.getElementById("atlasChart");
    var rsiEl = document.getElementById("rsiChart");
    if (!main) return;
    chart = LightweightCharts.createChart(main, {
      autoSize: true,
      layout: { background: { color: "#071422" }, textColor: "#9eb6cb" },
      grid: { vertLines: { color: "#123044" }, horzLines: { color: "#123044" } },
      rightPriceScale: { borderColor: "#1a4568" },
      timeScale: { borderColor: "#1a4568", timeVisible: true }
    });
    candleSeries = chart.addCandlestickSeries({
      upColor: "#55e7c1", downColor: "#ff7180", borderVisible: false,
      wickUpColor: "#55e7c1", wickDownColor: "#ff7180"
    });
    ema20Series = chart.addLineSeries({ color: "#52e4ff", lineWidth: 2, priceLineVisible: false, lastValueVisible: false });
    ema50Series = chart.addLineSeries({ color: "#f5bf5d", lineWidth: 2, priceLineVisible: false, lastValueVisible: false });
    volumeSeries = chart.addHistogramSeries({
      priceFormat: { type: "volume" },
      priceScaleId: "vol",
      priceLineVisible: false,
      lastValueVisible: false
    });
    chart.priceScale("vol").applyOptions({ scaleMargins: { top: 0.8, bottom: 0 } });
    if (rsiEl) {
      rsiChart = LightweightCharts.createChart(rsiEl, {
        autoSize: true,
        layout: { background: { color: "#071422" }, textColor: "#9eb6cb" },
        grid: { vertLines: { color: "#123044" }, horzLines: { color: "#123044" } },
        rightPriceScale: { borderColor: "#1a4568" },
        timeScale: { visible: false }
      });
      rsiSeries = rsiChart.addLineSeries({ color: "#c9a6ff", lineWidth: 2, priceLineVisible: false });
    }
    chart.subscribeCrosshairMove(function (param) {
      var tip = document.getElementById("chartTooltip");
      if (!tip) return;
      if (!param.time || !param.seriesData || !candleSeries) { tip.textContent = ""; return; }
      var bar = param.seriesData.get(candleSeries);
      if (!bar) { tip.textContent = ""; return; }
      tip.textContent = "O " + money(bar.open) + "  H " + money(bar.high) + "  L " + money(bar.low) + "  C " + money(bar.close);
    });
  }

  function paint() {
    if (!candles.length) return;
    ensureCharts();
    if (!chart) return;
    candleSeries.setData(candles.map(function (c) {
      return { time: c.time, open: c.open, high: c.high, low: c.low, close: c.close };
    }));
    var closes = candles.map(function (c) { return c.close; });
    function lineData(series, values) {
      series.applyOptions({ visible: true });
      series.setData(candles.map(function (c, i) {
        return values[i] == null ? null : { time: c.time, value: values[i] };
      }).filter(Boolean));
    }
    if (show.ema20) lineData(ema20Series, ema(closes, 20));
    else ema20Series.applyOptions({ visible: false });
    if (show.ema50) lineData(ema50Series, ema(closes, 50));
    else ema50Series.applyOptions({ visible: false });
    volumeSeries.applyOptions({ visible: show.volume });
    if (show.volume) {
      volumeSeries.setData(candles.map(function (c) {
        return { time: c.time, value: c.volume, color: c.close >= c.open ? "rgba(85,231,193,.45)" : "rgba(255,113,128,.45)" };
      }));
    }
    var rsiValues = rsi(closes, 14);
    var lastRsi = null;
    for (var i = rsiValues.length - 1; i >= 0; i--) if (rsiValues[i] != null) { lastRsi = rsiValues[i]; break; }
    text("statRSI", lastRsi == null ? "—" : lastRsi.toFixed(1));
    var wrap = document.getElementById("rsiWrap");
    if (wrap) wrap.classList.toggle("is-on", show.rsi);
    if (rsiSeries) {
      rsiSeries.setData(show.rsi ? candles.map(function (c, idx) {
        return rsiValues[idx] == null ? null : { time: c.time, value: rsiValues[idx] };
      }).filter(Boolean) : []);
    }
    var ema20 = ema(closes, 20);
    var lastEma = null;
    for (var j = ema20.length - 1; j >= 0; j--) if (ema20[j] != null) { lastEma = ema20[j]; break; }
    var last = candles[candles.length - 1];
    text("statTrend", lastEma == null ? "—" : (last.close >= lastEma ? "Close above EMA 20" : "Close below EMA 20"));
    if (rsiChart) rsiChart.timeScale().fitContent();
    chart.timeScale().fitContent();
  }

  function unavailable(message) {
    text("marketStatus", message);
    var main = document.getElementById("atlasChart");
    if (main && !candles.length) {
      main.innerHTML = "<p style=\"padding:18px;color:#9eb6cb\">Live candlesticks are unavailable from this browser. No sample prices are shown.</p>";
    }
  }

  function loadCandles() {
    text("marketStatus", "CONNECTING TO LIVE DATA…");
    fetch("https://data-api.binance.vision/api/v3/klines?symbol=" + encodeURIComponent(symbol) + "&interval=" + tf + "&limit=300", { cache: "no-store" })
      .then(function (r) { if (!r.ok) throw new Error("klines"); return r.json(); })
      .then(function (rows) {
        candles = rows.map(function (v) {
          return { time: Math.floor(v[0] / 1000), open: +v[1], high: +v[2], low: +v[3], close: +v[4], volume: +v[5] };
        });
        paint();
        text("marketStatus", "LIVE · BINANCE · educational data, may be delayed");
      })
      .catch(function () { unavailable("Live feed unavailable. Chart data is not shown."); });
  }

  function loadTicker() {
    fetch("https://data-api.binance.vision/api/v3/ticker/24hr?symbol=" + encodeURIComponent(symbol), { cache: "no-store" })
      .then(function (r) { if (!r.ok) throw new Error("ticker"); return r.json(); })
      .then(function (t) {
        var last = +t.lastPrice;
        var ch = +t.priceChangePercent;
        text("marketPrice", money(last));
        var change = document.getElementById("marketChange");
        if (change) {
          change.textContent = (ch >= 0 ? "+" : "") + ch.toFixed(2) + "%";
          change.className = "market-change " + (ch >= 0 ? "up" : "down");
        }
        text("statHigh", money(+t.highPrice));
        text("statLow", money(+t.lowPrice));
        var qv = +t.quoteVolume;
        text("statVolume", Number.isFinite(qv) ? qv.toLocaleString(undefined, { maximumFractionDigits: 0 }) : "—");
        var high = +t.highPrice, low = +t.lowPrice;
        text("statRange", last ? ((high - low) / last * 100).toFixed(2) + "%" : "—");
      })
      .catch(function () {
        text("marketPrice", "—");
        text("marketStatus", document.getElementById("marketStatus").textContent || "Live price unavailable");
      });
  }

  function loadEvents() {
    var box = document.getElementById("marketEvents");
    if (!box) return;
    box.innerHTML = "<p>Headlines are not bundled with this page. Event flags are omitted rather than invented. <a href=\"/macro-lab\">Open Macro &amp; Intermarket →</a></p>";
  }

  document.querySelectorAll("[data-tf]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      tf = btn.dataset.tf;
      document.querySelectorAll("[data-tf]").forEach(function (b) {
        var on = b === btn;
        b.classList.toggle("active", on);
        b.setAttribute("aria-pressed", on ? "true" : "false");
      });
      loadCandles();
    });
  });
  document.querySelectorAll("[data-overlay]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var key = btn.dataset.overlay;
      show[key] = !show[key];
      btn.setAttribute("aria-pressed", show[key] ? "true" : "false");
      btn.classList.toggle("active", show[key]);
      paint();
    });
  });

  loadCandles();
  loadTicker();
  loadEvents();
})();
