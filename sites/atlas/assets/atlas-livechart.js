/* Embeddable chart. Binance klines, then CoinGecko OHLC, then /data/samples. */
(function (root) {
  "use strict";
  function sma(values, period) {
    var out = [], sum = 0;
    for (var i = 0; i < values.length; i++) {
      sum += values[i];
      if (i >= period) sum -= values[i - period];
      out.push(i >= period - 1 ? sum / period : null);
    }
    return out;
  }
  function ema(values, period) {
    var k = 2 / (period + 1), out = [], prev = null;
    for (var i = 0; i < values.length; i++) {
      var v = values[i];
      if (v == null || !isFinite(v)) { out.push(null); continue; }
      if (prev == null) {
        if (i < period - 1) { out.push(null); continue; }
        var slice = values.slice(i - period + 1, i + 1), acc = 0, ready = true;
        for (var s = 0; s < slice.length; s++) {
          if (slice[s] == null || !isFinite(slice[s])) { ready = false; break; }
          acc += slice[s];
        }
        if (!ready) { out.push(null); continue; }
        prev = acc / period;
      } else prev = v * k + prev * (1 - k);
      out.push(prev);
    }
    return out;
  }
  function rsi(values, period) {
    var out = [], avgGain = 0, avgLoss = 0;
    for (var i = 0; i < values.length; i++) {
      if (i === 0) { out.push(null); continue; }
      var change = values[i] - values[i - 1];
      var gain = Math.max(change, 0), loss = Math.max(-change, 0);
      if (i < period) { out.push(null); continue; }
      if (i === period) {
        var g = 0, l = 0;
        for (var j = 1; j <= period; j++) {
          var c = values[j] - values[j - 1];
          g += Math.max(c, 0); l += Math.max(-c, 0);
        }
        avgGain = g / period; avgLoss = l / period;
      } else {
        avgGain = (avgGain * (period - 1) + gain) / period;
        avgLoss = (avgLoss * (period - 1) + loss) / period;
      }
      out.push(avgLoss === 0 ? 100 : 100 - 100 / (1 + avgGain / avgLoss));
    }
    return out;
  }
  function macd(values, fast, slow, signal) {
    var fastE = ema(values, fast || 12), slowE = ema(values, slow || 26);
    var line = values.map(function (_, i) {
      return fastE[i] == null || slowE[i] == null ? null : fastE[i] - slowE[i];
    });
    var compact = [], idx = [];
    line.forEach(function (v, i) { if (v != null) { compact.push(v); idx.push(i); } });
    var sig = ema(compact, signal || 9);
    var signalLine = values.map(function () { return null; });
    var hist = values.map(function () { return null; });
    sig.forEach(function (v, k) {
      if (v == null) return;
      signalLine[idx[k]] = v;
      hist[idx[k]] = line[idx[k]] - v;
    });
    return { line: line, signal: signalLine, hist: hist };
  }
  function bollinger(values, period, mult) {
    var p = period || 20, m = mult == null ? 2 : mult, mid = sma(values, p), upper = [], lower = [];
    for (var i = 0; i < values.length; i++) {
      if (mid[i] == null) { upper.push(null); lower.push(null); continue; }
      var slice = values.slice(i - p + 1, i + 1), variance = 0;
      slice.forEach(function (x) { variance += (x - mid[i]) * (x - mid[i]); });
      var sd = Math.sqrt(variance / slice.length);
      upper.push(mid[i] + m * sd); lower.push(mid[i] - m * sd);
    }
    return { mid: mid, upper: upper, lower: lower };
  }
  function atr(candles, period) {
    var p = period || 14;
    var trs = candles.map(function (c, i) {
      if (i === 0) return c.high - c.low;
      var prev = candles[i - 1].close;
      return Math.max(c.high - c.low, Math.abs(c.high - prev), Math.abs(c.low - prev));
    });
    var out = [], prevAtr = null;
    for (var i = 0; i < trs.length; i++) {
      if (i < p - 1) { out.push(null); continue; }
      if (i === p - 1) {
        var sum = 0;
        for (var j = 0; j < p; j++) sum += trs[j];
        prevAtr = sum / p; out.push(prevAtr); continue;
      }
      prevAtr = (prevAtr * (p - 1) + trs[i]) / p;
      out.push(prevAtr);
    }
    return out;
  }
  function vwap(candles) {
    var cumPV = 0, cumV = 0, day = "";
    return candles.map(function (c) {
      var d = new Date(c.time * 1000).toISOString().slice(0, 10);
      if (d !== day) { day = d; cumPV = 0; cumV = 0; }
      var tp = (c.high + c.low + c.close) / 3, vol = Number(c.volume) || 0;
      cumPV += tp * vol; cumV += vol;
      return cumV > 0 ? cumPV / cumV : null;
    });
  }
  function swings(candles, wing) {
    var w = wing || 2, marks = [];
    for (var i = w; i < candles.length - w; i++) {
      var isHigh = true, isLow = true;
      for (var j = i - w; j <= i + w; j++) {
        if (j === i) continue;
        if (candles[j].high >= candles[i].high) isHigh = false;
        if (candles[j].low <= candles[i].low) isLow = false;
      }
      if (isHigh) marks.push({ time: candles[i].time, position: "aboveBar", color: "#52e4ff", shape: "arrowDown", text: "SH" });
      if (isLow) marks.push({ time: candles[i].time, position: "belowBar", color: "#f5bf5d", shape: "arrowUp", text: "SL" });
    }
    return marks;
  }
  root.AtlasMath = { sma: sma, ema: ema, rsi: rsi, macd: macd, bollinger: bollinger, atr: atr, vwap: vwap, swings: swings };
  var COINS = { BTCUSDT: "bitcoin", ETHUSDT: "ethereum", BNBUSDT: "binancecoin", SOLUSDT: "solana", LINKUSDT: "chainlink", SUIUSDT: "sui", LTCUSDT: "litecoin", HBARUSDT: "hedera-hashgraph", XRPUSDT: "ripple" };
  function loadSample(symbol, interval) {
    return fetch("/data/samples/" + symbol + "-" + interval + ".json").then(function (r) {
      if (!r.ok) throw new Error("sample");
      return r.json();
    }).then(function (data) {
      return { candles: data.candles || [], source: "sample", label: "Educational sample" };
    });
  }
  function loadSeries(symbol, tf) {
    var interval = tf || "1h";
    var url = "https://data-api.binance.vision/api/v3/klines?symbol=" + encodeURIComponent(symbol) + "&interval=" + encodeURIComponent(interval) + "&limit=300";
    return fetch(url, { cache: "no-store" }).then(function (r) {
      if (!r.ok) throw new Error("binance");
      return r.json();
    }).then(function (rows) {
      if (!Array.isArray(rows) || !rows.length) throw new Error("empty");
      return {
        candles: rows.map(function (v) {
          return { time: Math.floor(v[0] / 1000), open: +v[1], high: +v[2], low: +v[3], close: +v[4], volume: +v[5] };
        }),
        source: "binance",
        label: "Public market data · educational, may be delayed"
      };
    }).catch(function () {
      var id = COINS[symbol];
      if (!id) return loadSample(symbol, interval);
      var days = interval === "1d" ? 180 : interval === "4h" ? 30 : 1;
      return fetch("https://api.coingecko.com/api/v3/coins/" + id + "/ohlc?vs_currency=usd&days=" + days, { cache: "no-store" })
        .then(function (r) { if (!r.ok) throw new Error("cg"); return r.json(); })
        .then(function (rows) {
          if (!Array.isArray(rows) || rows.length < 5) throw new Error("cg");
          return {
            candles: rows.map(function (v) {
              return { time: Math.floor(v[0] / 1000), open: +v[1], high: +v[2], low: +v[3], close: +v[4], volume: 0 };
            }),
            source: "coingecko",
            label: "CoinGecko OHLC fallback · no volume · educational, may be delayed"
          };
        }).catch(function () { return loadSample(symbol, interval); });
    });
  }
  root.AtlasData = { load: loadSeries, coins: COINS };
  function points(candles, values) {
    var out = [];
    for (var i = 0; i < candles.length; i++) if (values[i] != null && isFinite(values[i])) out.push({ time: candles[i].time, value: values[i] });
    return out;
  }
  function opts(height) {
    return {
      autoSize: true, height: height,
      layout: { background: { color: "#071422" }, textColor: "#9eb6cb" },
      grid: { vertLines: { color: "#123044" }, horzLines: { color: "#123044" } },
      rightPriceScale: { borderColor: "#1a4568" },
      timeScale: { borderColor: "#1a4568", timeVisible: true }
    };
  }
  function mount(el) {
    if (!el || !root.document) return;
    if (el._atlasDestroy) el._atlasDestroy();
    var symbol = el.getAttribute("data-symbol") || "BTCUSDT";
    var tf = el.getAttribute("data-tf") || "1h";
    var overlays = String(el.getAttribute("data-overlays") || "").split(",").map(function (s) { return s.trim(); }).filter(Boolean);
    var pane = el.getAttribute("data-pane") || "";
    var markers = el.getAttribute("data-markers") || "";
    var controls = el.hasAttribute("data-controls");
    var state = { symbol: symbol, tf: tf, overlays: overlays.slice(), pane: pane, markers: markers, pack: null };
    el.classList.add("atlas-chart");
    el.innerHTML = "";
    var bar = document.createElement("div");
    bar.className = "atlas-chart__bar";
    var status = document.createElement("p");
    status.className = "atlas-chart__status";
    status.setAttribute("role", "status");
    status.textContent = "Loading chart…";
    var stage = document.createElement("div");
    stage.className = "atlas-chart__stage";
    var paneEl = document.createElement("div");
    paneEl.className = "atlas-chart__pane";
    paneEl.hidden = true;
    el.append(bar, status, stage, paneEl);
    var names = [["ema20", "EMA 20"], ["sma50", "SMA 50"], ["bb20", "Bollinger"], ["vwap", "VWAP"]];
    if (controls) {
      bar.innerHTML = '<label>Symbol <select data-sym>' + ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"].map(function (s) {
        return "<option" + (s === symbol ? " selected" : "") + ">" + s + "</option>";
      }).join("") + "</select></label>" +
        '<label>Time <select data-tf><option value="1h">1H</option><option value="4h">4H</option><option value="1d">1D</option></select></label>' +
        '<label>Pane <select data-pane><option value="">Price</option><option value="rsi">RSI</option><option value="macd">MACD</option><option value="volume">Volume</option><option value="atr">ATR</option></select></label>' +
        '<div class="atlas-chart__toggles">' + names.map(function (n) {
          var on = state.overlays.indexOf(n[0]) >= 0;
          return '<button type="button" data-ov="' + n[0] + '" aria-pressed="' + on + '">' + n[1] + "</button>";
        }).join("") + "</div>";
      bar.querySelector("[data-tf]").value = tf;
      bar.querySelector("[data-pane]").value = pane;
      bar.querySelector("[data-sym]").addEventListener("change", function (e) { state.symbol = e.target.value; pull(); });
      bar.querySelector("[data-tf]").addEventListener("change", function (e) { state.tf = e.target.value; pull(); });
      bar.querySelector("[data-pane]").addEventListener("change", function (e) { state.pane = e.target.value; paint(); });
      bar.querySelectorAll("[data-ov]").forEach(function (btn) {
        btn.addEventListener("click", function () {
          var key = btn.getAttribute("data-ov");
          var i = state.overlays.indexOf(key);
          if (i >= 0) state.overlays.splice(i, 1); else state.overlays.push(key);
          btn.setAttribute("aria-pressed", state.overlays.indexOf(key) >= 0 ? "true" : "false");
          paint();
        });
      });
    } else bar.innerHTML = "<strong>" + symbol + "</strong> <span>" + tf.toUpperCase() + "</span>";
    var chart = null, candleSeries = null, paneChart = null;
    function destroyCharts() {
      if (chart) chart.remove();
      if (paneChart) paneChart.remove();
      chart = candleSeries = paneChart = null;
      stage.innerHTML = ""; paneEl.innerHTML = "";
    }
    function paint() {
      var pack = state.pack;
      if (!pack || !pack.candles.length || typeof root.LightweightCharts === "undefined") {
        if (typeof root.LightweightCharts === "undefined") status.textContent = "Chart library failed to load from this site.";
        return;
      }
      destroyCharts();
      chart = root.LightweightCharts.createChart(stage, opts(360));
      candleSeries = chart.addCandlestickSeries({ upColor: "#55e7c1", downColor: "#ff7180", borderVisible: false, wickUpColor: "#55e7c1", wickDownColor: "#ff7180" });
      var candles = pack.candles;
      candleSeries.setData(candles.map(function (c) { return { time: c.time, open: c.open, high: c.high, low: c.low, close: c.close }; }));
      var closes = candles.map(function (c) { return c.close; });
      var hasVol = candles.some(function (c) { return c.volume > 0; });
      function line(key, values, color) {
        if (state.overlays.indexOf(key) < 0) return;
        chart.addLineSeries({ color: color, lineWidth: 2, priceLineVisible: false, lastValueVisible: false }).setData(points(candles, values));
      }
      line("ema20", ema(closes, 20), "#52e4ff");
      line("sma50", sma(closes, 50), "#c9a6ff");
      line("ema50", ema(closes, 50), "#f5bf5d");
      if (state.overlays.indexOf("bb20") >= 0) {
        var bb = bollinger(closes, 20, 2);
        chart.addLineSeries({ color: "#9adfff", lineWidth: 1, priceLineVisible: false, lastValueVisible: false }).setData(points(candles, bb.mid));
        chart.addLineSeries({ color: "rgba(82,228,255,.55)", lineWidth: 1, priceLineVisible: false, lastValueVisible: false }).setData(points(candles, bb.upper));
        chart.addLineSeries({ color: "rgba(82,228,255,.55)", lineWidth: 1, priceLineVisible: false, lastValueVisible: false }).setData(points(candles, bb.lower));
      }
      if (state.overlays.indexOf("vwap") >= 0 && hasVol) line("vwap", vwap(candles), "#ffd06f");
      if (state.markers === "swings") candleSeries.setMarkers(swings(candles, 2));
      var note = pack.label;
      if (state.overlays.indexOf("vwap") >= 0 && !hasVol) note += " · VWAP needs volume, so it is hidden on this feed";
      status.textContent = note;
      status.classList.toggle("is-sample", pack.source === "sample");
      if (state.pane) {
        paneEl.hidden = false;
        paneChart = root.LightweightCharts.createChart(paneEl, opts(140));
        if (state.pane === "rsi") paneChart.addLineSeries({ color: "#c9a6ff", lineWidth: 2, priceLineVisible: false }).setData(points(candles, rsi(closes, 14)));
        else if (state.pane === "macd") {
          var m = macd(closes, 12, 26, 9);
          paneChart.addLineSeries({ color: "#52e4ff", lineWidth: 2, priceLineVisible: false }).setData(points(candles, m.line));
          paneChart.addLineSeries({ color: "#f5bf5d", lineWidth: 1, priceLineVisible: false }).setData(points(candles, m.signal));
        } else if (state.pane === "atr") paneChart.addLineSeries({ color: "#ffb4a2", lineWidth: 2, priceLineVisible: false }).setData(points(candles, atr(candles, 14)));
        else if (state.pane === "volume" && hasVol) {
          paneChart.addHistogramSeries({ priceFormat: { type: "volume" }, priceLineVisible: false }).setData(candles.map(function (c) {
            return { time: c.time, value: c.volume, color: c.close >= c.open ? "rgba(85,231,193,.7)" : "rgba(255,113,128,.7)" };
          }));
        } else paneEl.hidden = true;
      }
      chart.timeScale().fitContent();
      if (paneChart) paneChart.timeScale().fitContent();
    }
    function pull() {
      status.textContent = "Loading " + state.symbol + "…";
      loadSeries(state.symbol, state.tf).then(function (pack) {
        state.pack = pack;
        if (!pack.candles.length) throw new Error("empty");
        paint();
      }).catch(function () { status.textContent = "Chart data is unavailable for " + state.symbol + "."; });
    }
    el._atlasDestroy = destroyCharts;
    pull();
  }
  function configure(el, optsIn) {
    if (optsIn.symbol) el.setAttribute("data-symbol", optsIn.symbol);
    if (optsIn.tf) el.setAttribute("data-tf", optsIn.tf);
    if (optsIn.overlays != null) el.setAttribute("data-overlays", optsIn.overlays);
    if (optsIn.pane != null) el.setAttribute("data-pane", optsIn.pane);
    if (optsIn.markers != null) el.setAttribute("data-markers", optsIn.markers);
    el.hidden = false;
    return mount(el);
  }
  root.AtlasLiveChart = { mount: mount, configure: configure };
  function boot() {
    document.querySelectorAll("[data-atlas-chart]").forEach(function (el) { if (!el.hidden) mount(el); });
  }
  if (root.document) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
    else boot();
  }
})(typeof window !== "undefined" ? window : globalThis);
