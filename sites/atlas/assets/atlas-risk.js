(function (root) {
  function num(v) { var n = Number(v); return isFinite(n) ? n : NaN; }
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
  root.AtlasRisk = { sizePosition: sizePosition };
  function boot() {
    var form = document.querySelector("[data-risk-calc]");
    if (!form) return;
    function money(n) { return n.toLocaleString(undefined, { maximumFractionDigits: 2 }); }
    function read() {
      var result = sizePosition({
        account: form.account.value, riskPct: form.riskPct.value, entry: form.entry.value, stop: form.stop.value,
        feeBps: form.feeBps.value, slipBps: form.slipBps.value, leverage: form.leverage.value, mode: form.mode.value
      });
      var warn = document.getElementById("riskWarning");
      if (result.error) { warn.textContent = result.error; return; }
      document.getElementById("riskQty").textContent = result.qty.toLocaleString(undefined, { maximumFractionDigits: 6 });
      document.getElementById("riskNotional").textContent = money(result.notional);
      document.getElementById("riskCash").textContent = money(result.riskCash);
      document.getElementById("riskDistance").textContent = result.distancePct.toFixed(2) + "%";
      document.getElementById("riskFriction").textContent = money(result.friction);
      document.getElementById("riskLoss").textContent = money(result.lossAtStop);
      document.getElementById("riskImplied").textContent = result.impliedLeverage.toFixed(2) + "×";
      warn.textContent = "Hypothetical " + result.side + " model. Fees and slippage are applied on the way in and the way out. This is not an order." + (result.warning ? " " + result.warning : "");
    }
    form.addEventListener("input", read);
    read();
  }
  if (root.document) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
    else boot();
  }
})(typeof window !== "undefined" ? window : globalThis);
