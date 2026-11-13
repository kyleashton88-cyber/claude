(function () {
  var root = document.querySelector("[data-orderbook]");
  if (!root) return;
  var symbolSel = root.querySelector("[data-book-symbol]");
  var status = root.querySelector("[data-book-status]");
  var spread = root.querySelector("[data-book-spread]");
  var bids = root.querySelector("[data-book-bids]");
  var asks = root.querySelector("[data-book-asks]");
  function row(price, qty, cls) {
    var li = document.createElement("li");
    li.innerHTML = '<span class="' + cls + '">' + price + "</span><span>" + qty + "</span>";
    return li;
  }
  function paint(book, label) {
    bids.innerHTML = ""; asks.innerHTML = "";
    (book.bids || []).slice(0, 10).forEach(function (level) { bids.appendChild(row(level[0], level[1], "bid")); });
    (book.asks || []).slice(0, 10).forEach(function (level) { asks.appendChild(row(level[0], level[1], "ask")); });
    var bestBid = Number(book.bids && book.bids[0] && book.bids[0][0]);
    var bestAsk = Number(book.asks && book.asks[0] && book.asks[0][0]);
    if (bestBid > 0 && bestAsk > 0) {
      var diff = bestAsk - bestBid, mid = (bestAsk + bestBid) / 2;
      spread.textContent = diff.toLocaleString(undefined, { maximumFractionDigits: 4 }) + " (" + (diff / mid * 10000).toFixed(2) + " bps)";
    } else spread.textContent = "—";
    status.textContent = label;
    status.classList.toggle("is-sample", label.indexOf("Educational sample") === 0);
  }
  function sample(symbol) {
    var mid = symbol.indexOf("BTC") === 0 ? 64000 : symbol.indexOf("ETH") === 0 ? 3200 : 150;
    var b = [], a = [];
    for (var i = 0; i < 10; i++) {
      b.push([(mid - (i + 1) * mid * 0.00015).toFixed(2), (2 + i * 0.3).toFixed(3)]);
      a.push([(mid + (i + 1) * mid * 0.00015).toFixed(2), (1.6 + i * 0.25).toFixed(3)]);
    }
    return { bids: b, asks: a };
  }
  function load() {
    var symbol = symbolSel.value;
    status.textContent = "Loading public depth…";
    fetch("https://data-api.binance.vision/api/v3/depth?symbol=" + encodeURIComponent(symbol) + "&limit=20", { cache: "no-store" })
      .then(function (r) { if (!r.ok) throw new Error("depth"); return r.json(); })
      .then(function (book) { paint(book, "Public depth · educational, may be delayed"); })
      .catch(function () { paint(sample(symbol), "Educational sample"); });
  }
  symbolSel.addEventListener("change", load);
  load();
})();
