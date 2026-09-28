/* On-Chain Operator calculator.
   Same relationships as defi_calc.py. Educational modelling only.
   Rates are inputs. Outputs are not forecasts. */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.OcoCalc = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  function num(v, fallback) {
    const n = typeof v === "number" ? v : parseFloat(v);
    return Number.isFinite(n) ? n : fallback;
  }

  function il(r) {
    return (2 * Math.sqrt(r)) / (1 + r) - 1;
  }

  function money(n, digits) {
    const d = digits == null ? (Math.abs(n) >= 1000 ? 0 : 2) : digits;
    const sign = n < 0 ? "−" : "";
    return sign + "$" + Math.abs(n).toLocaleString("en-US", {
      minimumFractionDigits: d,
      maximumFractionDigits: d
    });
  }

  function pct(n, digits) {
    const d = digits == null ? 2 : digits;
    const sign = n < 0 ? "−" : "";
    return sign + Math.abs(n).toFixed(d) + "%";
  }

  function signedPct(n, digits) {
    const d = digits == null ? 2 : digits;
    if (n < 0) return "−" + Math.abs(n).toFixed(d) + "%";
    return "+" + n.toFixed(d) + "%";
  }

  function multiple(n, digits) {
    return n.toFixed(digits == null ? 2 : digits) + "×";
  }

  function zone(status, label) {
    return { status: status, label: label };
  }

  function result(partial) {
    return Object.assign({
      status: "watch",
      zone: "Watch this",
      verdict: "",
      figure: "",
      figureLabel: "",
      metrics: [],
      formula: "",
      use: "",
      read: "",
      chart: null,
      table: null,
      numbers: {},
      error: ""
    }, partial);
  }

  function linspace(a, b, n) {
    const out = [];
    const steps = Math.max(2, n);
    for (let i = 0; i < steps; i++) out.push(a + (b - a) * i / (steps - 1));
    return out;
  }

  function series(points) {
    return points.map(function (p) { return { x: p[0], y: p[1] }; });
  }

  const tools = [
    {
      id: "il",
      name: "Impermanent loss",
      group: "Pools",
      blurb: "The gap between a 50/50 pool and simply holding both assets after the price moves.",
      fields: [
        { key: "ratio", label: "Price now ÷ price when you entered", value: 2, min: 0.05, max: 10, step: 0.01 }
      ],
      compute: function (v) {
        const r = num(v.ratio, 2);
        if (!(r > 0)) return result({ status: "bad", zone: "Outside the safe zone", error: "The price ratio has to be above zero.", verdict: "Enter a price ratio above zero." });
        const loss = il(r) * 100;
        const abs = Math.abs(loss);
        const status = abs < 1 ? "good" : abs < 5 ? "watch" : "bad";
        const xs = linspace(0.25, 5, 80);
        return result({
          status: status,
          zone: status === "good" ? "In the safe zone" : status === "watch" ? "Watch this" : "Outside the safe zone",
          verdict: "A " + multiple(r, 2) + " price leaves this pool " + pct(abs) + " behind holding both assets.",
          figure: pct(loss),
          figureLabel: "versus holding",
          formula: "Gap = 2 × √(price ratio) ÷ (1 + price ratio) − 1",
          use: "Type how far the price has moved since you added liquidity. 2 means the price doubled. 0.5 means it halved.",
          read: "The curve is always at or below zero. Near 1× the gap is small. Past about 2×, or below 0.5×, the gap is large enough that fees have real work to do. A move up and the same move down cost the same.",
          metrics: [
            { label: "Price ratio", value: multiple(r, 2) },
            { label: "Gap versus holding", value: pct(loss) }
          ],
          chart: {
            kind: "line",
            xLabel: "Price ratio",
            yLabel: "Gap versus holding",
            yUnit: "percent",
            series: [{ name: "Gap versus holding", points: series(xs.map(function (x) { return [x, il(x) * 100]; })) }],
            guides: [{ y: -1, label: "1% gap", tone: "good" }, { y: -5, label: "5% gap", tone: "bad" }],
            marker: { x: Math.min(5, Math.max(0.25, r)), y: loss, label: multiple(r, 2) }
          },
          numbers: { il: il(r) }
        });
      }
    },
    {
      id: "lp",
      name: "Fee break-even",
      group: "Pools",
      blurb: "The fee rate a pool must pay before it beats holding, for a given move and a given stay.",
      fields: [
        { key: "ratio", label: "Price now ÷ price when you entered", value: 1.5, min: 0.05, max: 10, step: 0.01 },
        { key: "days", label: "Days you plan to stay", value: 30, min: 1, max: 365, step: 1 },
        { key: "feeApr", label: "Fee APR the pool is paying", value: 20, min: 0, max: 500, step: 0.1, unit: "%" }
      ],
      compute: function (v) {
        const r = num(v.ratio, 1.5);
        const days = num(v.days, 30);
        const fee = num(v.feeApr, 20);
        if (!(r > 0) || !(days > 0)) return result({ status: "bad", zone: "Outside the safe zone", error: "Price ratio and days both have to be above zero.", verdict: "Enter a price ratio and a stay above zero." });
        const loss = -il(r);
        const need = loss * 365 / days * 100;
        const earned = fee / 100 * days / 365;
        const net = (earned - loss) * 100;
        const status = net >= 0 ? "good" : net > -1 ? "watch" : "bad";
        const xs = linspace(0, Math.max(need * 1.6, fee * 1.4, 10), 60);
        return result({
          status: status,
          zone: status === "good" ? "In the safe zone" : status === "watch" ? "Watch this" : "Outside the safe zone",
          verdict: net >= 0
            ? "Fees cover the " + pct(loss * 100) + " gap, with " + signedPct(net) + " left over versus holding."
            : "Fees fall " + pct(Math.abs(net)) + " short of the " + pct(loss * 100) + " gap versus holding.",
          figure: pct(need),
          figureLabel: "fee APR needed",
          formula: "Fee APR needed = gap versus holding × 365 ÷ days you stay",
          use: "Use this after impermanent loss, once you know the move and how long you intend to leave the position open. Type the fee APR you can see on the pool, not a hoped-for rate.",
          read: "The marker sits on your fee APR. Left of the zero line, holding still wins. On or right of zero, fees have paid the gap for this stay. A shorter stay demands a higher APR for the same price move.",
          metrics: [
            { label: "Gap to earn back", value: pct(loss * 100) },
            { label: "Fees earned over the stay", value: pct(earned * 100) },
            { label: "Net versus holding", value: signedPct(net) }
          ],
          chart: {
            kind: "line",
            xLabel: "Fee APR",
            yLabel: "Net versus holding",
            yUnit: "percent",
            xUnit: "percent",
            series: [{
              name: "Net versus holding",
              points: series(xs.map(function (x) {
                return [x, (x / 100 * days / 365 - loss) * 100];
              }))
            }],
            guides: [{ y: 0, label: "Matches holding", tone: "good" }],
            marker: { x: fee, y: net, label: pct(fee, 1) }
          },
          numbers: { need: need, net: net, loss: loss }
        });
      }
    },
    {
      id: "cl",
      name: "Concentrated range",
      group: "Pools",
      blurb: "How much harder your capital works inside a price range, and what happens when price leaves it.",
      fields: [
        { key: "low", label: "Lower price of the range", value: 1800, min: 0.0001, max: 1000000, step: 1 },
        { key: "high", label: "Upper price of the range", value: 3200, min: 0.0001, max: 1000000, step: 1 }
      ],
      compute: function (v) {
        const low = num(v.low, 1800);
        const high = num(v.high, 3200);
        if (!(low > 0 && high > low)) return result({ status: "bad", zone: "Outside the safe zone", error: "The upper price has to sit above the lower price, and both above zero.", verdict: "Set a range with the upper price above the lower price." });
        const eff = 1 / (1 - Math.pow(low / high, 0.25));
        const mid = Math.sqrt(low * high);
        const width = high / low;
        const status = eff < 2 ? "watch" : eff <= 12 ? "good" : "bad";
        const xs = linspace(1.35, 6, 70);
        return result({
          status: status,
          zone: status === "good" ? "In the safe zone" : status === "watch" ? "Watch this" : "Outside the safe zone",
          verdict: status === "bad"
            ? "This range is about " + multiple(eff, 1) + " as concentrated as a full-range pool, which means price will leave it often."
            : status === "watch"
              ? "This range is only " + multiple(eff, 1) + " as concentrated as a full-range pool, so the extra fee is modest."
              : "Inside " + money(low, 0) + " to " + money(high, 0) + " your capital works about " + multiple(eff, 1) + " a full-range position.",
          figure: multiple(eff, 1),
          figureLabel: "capital at work versus full range",
          formula: "Efficiency ≈ 1 ÷ (1 − (lower ÷ upper) ^ 0.25)",
          use: "Type the lower and upper prices of the range you would actually set. The geometric middle is the price the range is built around.",
          read: "Fees and the impermanent-loss gap both scale by roughly this multiple, and only while price stays inside. Outside the band you earn no fees and the position becomes one asset. A multiple under 2× is a wide range. Past about 12× the range is tight enough to sit idle a lot.",
          metrics: [
            { label: "Geometric middle", value: money(mid, mid >= 100 ? 0 : 2) },
            { label: "Width", value: multiple(width, 2) },
            { label: "Out of range", value: "No fees, one asset" }
          ],
          chart: {
            kind: "line",
            xLabel: "Upper ÷ lower",
            yLabel: "Capital at work",
            yUnit: "multiple",
            series: [{
              name: "Capital at work",
              points: series(xs.map(function (w) {
                return [w, 1 / (1 - Math.pow(1 / w, 0.25))];
              }))
            }],
            guides: [{ y: 2, label: "2×", tone: "watch" }, { y: 12, label: "12×", tone: "bad" }],
            marker: { x: Math.min(6, Math.max(1.35, width)), y: eff, label: multiple(width, 2) }
          },
          numbers: { eff: eff, mid: mid, width: width }
        });
      }
    },
    {
      id: "lvr",
      name: "Loss versus rebalancing",
      group: "Pools",
      blurb: "The steady drag volatility puts on a full-range pool, set next to the fees it collects.",
      fields: [
        { key: "vol", label: "Annualised volatility", value: 80, min: 1, max: 300, step: 1, unit: "%" },
        { key: "feeApr", label: "Fee APR, if you know it", value: 25, min: 0, max: 500, step: 0.1, unit: "%" }
      ],
      compute: function (v) {
        const vol = num(v.vol, 80);
        const fee = num(v.feeApr, 0);
        if (!(vol > 0)) return result({ status: "bad", zone: "Outside the safe zone", error: "Volatility has to be above zero.", verdict: "Enter a volatility above zero." });
        const rate = (vol / 100) ** 2 / 8 * 100;
        const net = fee - rate;
        const status = net > 1 ? "good" : net >= 0 ? "watch" : "bad";
        const xs = linspace(10, 150, 60);
        return result({
          status: status,
          zone: status === "good" ? "In the safe zone" : status === "watch" ? "Watch this" : "Outside the safe zone",
          verdict: net >= 0
            ? "Fees outpace the rebalancing drag by " + signedPct(net) + " a year on this model."
            : "The rebalancing drag is " + pct(Math.abs(net)) + " a year ahead of the fees.",
          figure: pct(rate),
          figureLabel: "of pool value per year",
          formula: "Drag ≈ volatility² ÷ 8, for a full-range constant-product pool",
          use: "Type the annualised volatility of the pair and the fee APR the pool is paying now. This is the full-range case, before concentration.",
          read: "The drag rises with the square of volatility. If the fee line sits above the drag, the pool is being paid for the rebalancing. If it sits below, you are paying to provide liquidity. Concentration raises both fees and this drag while you stay in range.",
          metrics: [
            { label: "Rebalancing drag", value: pct(rate) + " / year" },
            { label: "Fee APR", value: pct(fee) },
            { label: "Fees minus drag", value: signedPct(net) + " / year" }
          ],
          chart: {
            kind: "line",
            xLabel: "Annualised volatility",
            yLabel: "Percent per year",
            yUnit: "percent",
            xUnit: "percent",
            series: [
              { name: "Rebalancing drag", points: series(xs.map(function (x) { return [x, (x / 100) ** 2 / 8 * 100]; })) },
              { name: "Your fee APR", points: series(xs.map(function (x) { return [x, fee]; })), dashed: true }
            ],
            guides: [],
            marker: { x: Math.min(150, Math.max(10, vol)), y: rate, label: pct(vol, 0) }
          },
          numbers: { rate: rate, net: net }
        });
      }
    },
    {
      id: "health",
      name: "Health factor",
      group: "Borrowing",
      blurb: "How far a collateralised loan sits from liquidation, and the price that closes it.",
      fields: [
        { key: "qty", label: "Collateral units", value: 10, min: 0.0001, max: 1000000, step: 0.01 },
        { key: "price", label: "Collateral price", value: 3000, min: 0.0001, max: 10000000, step: 1, unit: "$" },
        { key: "lt", label: "Liquidation threshold", value: 0.8, min: 0.05, max: 0.99, step: 0.01 },
        { key: "debt", label: "Debt value", value: 10000, min: 1, max: 100000000, step: 1, unit: "$" }
      ],
      compute: function (v) {
        const qty = num(v.qty, 10);
        const price = num(v.price, 3000);
        const lt = num(v.lt, 0.8);
        const debt = num(v.debt, 10000);
        if (!(qty > 0 && price > 0 && lt > 0 && lt < 1 && debt > 0)) {
          return result({ status: "bad", zone: "Outside the safe zone", error: "Units, price, and debt must be above zero. The liquidation threshold sits between 0 and 1.", verdict: "Check the collateral, the threshold, and the debt." });
        }
        const coll = qty * price;
        const hf = coll * lt / debt;
        const liq = debt / (qty * lt);
        const dist = (liq / price - 1) * 100;
        const status = hf >= 2 ? "good" : hf >= 1.5 ? "watch" : "bad";
        const lo = Math.min(liq * 0.7, price * 0.4);
        const hi = Math.max(price * 1.3, liq * 1.4);
        const xs = linspace(Math.max(lo, 0.01), hi, 80);
        return result({
          status: status,
          zone: status === "good" ? "In the safe zone" : status === "watch" ? "Watch this" : "Outside the safe zone",
          verdict: status === "bad"
            ? "Health factor " + hf.toFixed(2) + " is under 1.5. Repay or add collateral before the price reaches " + money(liq) + "."
            : "Health factor " + hf.toFixed(2) + ". Liquidation is " + pct(Math.abs(dist), 1) + " " + (dist < 0 ? "under" : "over") + " the current price, at " + money(liq) + ".",
          figure: hf.toFixed(2),
          figureLabel: "health factor",
          formula: "Health factor = collateral × liquidation threshold ÷ debt",
          use: "Type the units you posted, today’s price, the protocol’s liquidation threshold as a decimal (0.80, not 80), and the debt in dollars.",
          read: "Under 1.0 the position can be liquidated. The working floor in this program is 1.5, and 2.0 leaves room for a sharp move. The graph shows health factor against price. Your marker should sit above the 2.0 line with the liquidation price well to the left.",
          metrics: [
            { label: "Collateral", value: money(coll) },
            { label: "Loan to value", value: pct(debt / coll * 100, 1) },
            { label: "Liquidation price", value: money(liq, liq >= 100 ? 0 : 2) },
            { label: "Max debt at 2.0", value: money(coll * lt / 2) }
          ],
          chart: {
            kind: "line",
            xLabel: "Collateral price",
            yLabel: "Health factor",
            yUnit: "number",
            xUnit: "money",
            series: [{ name: "Health factor", points: series(xs.map(function (x) { return [x, qty * x * lt / debt]; })) }],
            guides: [{ y: 1, label: "Liquidation", tone: "bad" }, { y: 1.5, label: "1.5 floor", tone: "watch" }, { y: 2, label: "2.0 floor", tone: "good" }],
            marker: { x: price, y: hf, label: money(price, 0) }
          },
          numbers: { hf: hf, liq: liq, coll: coll }
        });
      }
    },
    {
      id: "loop",
      name: "Lending loop",
      group: "Borrowing",
      blurb: "What repeated borrow-and-supply does to leverage, and the borrow rate that wipes the spread out.",
      fields: [
        { key: "ltv", label: "Borrow amount each loop, as a share of collateral", value: 0.75, min: 0.05, max: 0.95, step: 0.01 },
        { key: "loops", label: "Loops", value: 3, min: 0, max: 20, step: 1 },
        { key: "collateralApy", label: "Collateral APY", value: 5, min: 0, max: 200, step: 0.1, unit: "%" },
        { key: "borrowApy", label: "Borrow APY", value: 3, min: 0, max: 200, step: 0.1, unit: "%" }
      ],
      compute: function (v) {
        const L = num(v.ltv, 0.75);
        const loops = Math.round(num(v.loops, 3));
        const cApy = num(v.collateralApy, 5);
        const bApy = num(v.borrowApy, 3);
        if (!(L > 0 && L < 1) || loops < 0) return result({ status: "bad", zone: "Outside the safe zone", error: "Each loop’s borrow share has to sit between 0 and 1.", verdict: "Set the borrow share between 0 and 1." });
        const lev = (1 - Math.pow(L, loops + 1)) / (1 - L);
        const net = cApy * lev - bApy * (lev - 1);
        const breakeven = lev > 1 ? cApy * lev / (lev - 1) : Infinity;
        const status = net <= 0 ? "bad" : net <= cApy + 0.05 ? "watch" : "good";
        const hi = Math.max(breakeven * 1.3, bApy * 1.5, cApy * 2, 5);
        const xs = linspace(0, hi, 70);
        return result({
          status: status,
          zone: status === "good" ? "In the safe zone" : status === "watch" ? "Watch this" : "Outside the safe zone",
          verdict: net <= cApy + 0.05
            ? "At " + multiple(lev) + " leverage the net is " + pct(net) + ". The spread is not paying you to loop."
            : multiple(lev) + " leverage turns " + pct(cApy) + " collateral yield into " + pct(net) + " on your equity, until borrow reaches " + pct(breakeven) + ".",
          figure: pct(net),
          figureLabel: "net APY on equity",
          formula: "Leverage = (1 − LTV^(loops+1)) ÷ (1 − LTV). Net = collateral APY × leverage − borrow APY × (leverage − 1)",
          use: "Type the loan-to-value you borrow on each pass, how many passes you will actually do, and the two live rates.",
          read: "Leverage helps only while collateral yield beats the borrow rate. The graph crosses zero at the borrow rate that erases the return. Above that line you pay for the privilege of being levered. Looping also stacks liquidation risk, which this APY does not show. Check health factor beside it.",
          metrics: [
            { label: "Leverage", value: multiple(lev) },
            { label: "Ceiling if you kept looping", value: multiple(1 / (1 - L)) },
            { label: "Borrow rate that wipes it out", value: Number.isFinite(breakeven) ? pct(breakeven) : "—" },
            { label: "Unlevered yield", value: pct(cApy) }
          ],
          chart: {
            kind: "line",
            xLabel: "Borrow APY",
            yLabel: "Net APY on equity",
            yUnit: "percent",
            xUnit: "percent",
            series: [{ name: "Net APY on equity", points: series(xs.map(function (x) { return [x, cApy * lev - x * (lev - 1)]; })) }],
            guides: [{ y: 0, label: "Wiped out", tone: "bad" }, { y: cApy, label: "Unlevered", tone: "watch" }],
            marker: { x: bApy, y: net, label: pct(bApy, 1) }
          },
          numbers: { lev: lev, net: net, breakeven: breakeven }
        });
      }
    },
    {
      id: "supply",
      name: "Supply rate",
      group: "Borrowing",
      blurb: "The lend rate implied by what borrowers pay, after utilisation and the reserve.",
      fields: [
        { key: "borrowApy", label: "Borrow APY", value: 8, min: 0, max: 200, step: 0.1, unit: "%" },
        { key: "utilisation", label: "Utilisation", value: 0.7, min: 0, max: 1, step: 0.01 },
        { key: "reserve", label: "Reserve factor", value: 0.1, min: 0, max: 0.95, step: 0.01 }
      ],
      compute: function (v) {
        const borrow = num(v.borrowApy, 8);
        const u = num(v.utilisation, 0.7);
        const rf = num(v.reserve, 0.1);
        if (!(u >= 0 && u <= 1 && rf >= 0 && rf < 1 && borrow >= 0)) {
          return result({ status: "bad", zone: "Outside the safe zone", error: "Utilisation and the reserve factor sit between 0 and 1.", verdict: "Utilisation and the reserve factor sit between 0 and 1." });
        }
        const s = borrow * u * (1 - rf);
        const status = u >= 0.95 ? "bad" : u >= 0.85 ? "watch" : "good";
        const xs = linspace(0, 1, 50);
        return result({
          status: status,
          zone: status === "good" ? "In the safe zone" : status === "watch" ? "Watch this" : "Outside the safe zone",
          verdict: status === "bad"
            ? "Utilisation is " + pct(u * 100, 0) + ". Supply APY is " + pct(s) + ", and borrow rates can jump from here."
            : "Supply APY is about " + pct(s) + " while " + pct(u * 100, 0) + " of deposits are borrowed.",
          figure: pct(s),
          figureLabel: "supply APY",
          formula: "Supply APY ≈ borrow APY × utilisation × (1 − reserve factor)",
          use: "Read borrow APY, utilisation, and the reserve factor from the lending market. Utilisation is a decimal: 0.70, not 70.",
          read: "Lenders are paid from borrower interest, after the protocol keeps the reserve. The rate climbs with utilisation, and so does the chance that liquidity dries up when you want to withdraw. Past about 85% utilised, treat the rate as unstable.",
          metrics: [
            { label: "Borrow APY", value: pct(borrow) },
            { label: "Share that reaches lenders", value: pct((1 - rf) * 100, 0) },
            { label: "Utilisation", value: pct(u * 100, 0) }
          ],
          chart: {
            kind: "line",
            xLabel: "Utilisation",
            yLabel: "Supply APY",
            yUnit: "percent",
            xUnit: "share",
            series: [{ name: "Supply APY", points: series(xs.map(function (x) { return [x, borrow * x * (1 - rf)]; })) }],
            guides: [{ x: 0.85, label: "85% utilised", tone: "watch" }],
            marker: { x: u, y: s, label: pct(u * 100, 0) }
          },
          numbers: { supply: s }
        });
      }
    },
    {
      id: "cdp",
      name: "CDP mint",
      group: "Borrowing",
      blurb: "How many stablecoins a collateral position can mint, and the price that breaks the minimum ratio.",
      fields: [
        { key: "qty", label: "Collateral units", value: 10, min: 0.0001, max: 1000000, step: 0.01 },
        { key: "price", label: "Collateral price", value: 3000, min: 0.0001, max: 10000000, step: 1, unit: "$" },
        { key: "mint", label: "Amount you would mint", value: 8000, min: 0, max: 100000000, step: 1, unit: "$" },
        { key: "minRatio", label: "Minimum collateral ratio", value: 150, min: 101, max: 1000, step: 1, unit: "%" },
        { key: "fee", label: "Stability fee per year", value: 2, min: 0, max: 50, step: 0.1, unit: "%" }
      ],
      compute: function (v) {
        const qty = num(v.qty, 10);
        const price = num(v.price, 3000);
        const mint = num(v.mint, 8000);
        const minRatio = num(v.minRatio, 150);
        const fee = num(v.fee, 2);
        if (!(qty > 0 && price > 0 && minRatio > 100)) return result({ status: "bad", zone: "Outside the safe zone", error: "Collateral has to be above zero and the minimum ratio above 100%.", verdict: "Check the collateral and the minimum ratio." });
        const coll = qty * price;
        const maxMint = coll / (minRatio / 100);
        const ratio = mint > 0 ? coll / mint * 100 : Infinity;
        const liq = mint > 0 ? mint * minRatio / 100 / qty : 0;
        const feeYr = mint * fee / 100;
        const status = mint <= 0 ? "watch" : ratio < minRatio ? "bad" : ratio < minRatio * 1.25 ? "watch" : "good";
        const xs = linspace(Math.max(maxMint * 0.25, 1), maxMint * 1.15, 50);
        return result({
          status: status,
          zone: status === "good" ? "In the safe zone" : status === "watch" ? "Watch this" : "Outside the safe zone",
          verdict: mint <= 0
            ? "This collateral can mint up to " + money(maxMint, 0) + " at a " + pct(minRatio, 0) + " minimum ratio."
            : ratio < minRatio
              ? "A " + pct(ratio, 0) + " ratio is under the " + pct(minRatio, 0) + " minimum. The position would already be open to liquidation."
              : "Minting " + money(mint, 0) + " leaves a " + pct(ratio, 0) + " ratio. Liquidation price is " + money(liq) + ".",
          figure: mint > 0 ? pct(ratio, 0) : money(maxMint, 0),
          figureLabel: mint > 0 ? "collateral ratio" : "maximum mint",
          formula: "Maximum mint = collateral ÷ (minimum ratio). Liquidation price = mint × minimum ratio ÷ collateral units",
          use: "Type the collateral, the amount you want to mint, and the vault’s minimum ratio. 150 means 150%, not 1.50.",
          read: "Stay above the minimum with room. The graph falls as you mint more. Crossing the minimum line means a small price drop can liquidate you. The stability fee is a real annual cost on the minted amount.",
          metrics: [
            { label: "Collateral value", value: money(coll, 0) },
            { label: "Maximum mint", value: money(maxMint, 0) },
            { label: "Liquidation price", value: mint > 0 ? money(liq) : "—" },
            { label: "Stability fee", value: money(feeYr, 0) + " / year" }
          ],
          chart: {
            kind: "line",
            xLabel: "Amount minted",
            yLabel: "Collateral ratio",
            yUnit: "percent",
            xUnit: "money",
            series: [{
              name: "Collateral ratio",
              points: series(xs.filter(function (x) { return x > maxMint * 0.02; }).map(function (x) {
                return [x, coll / x * 100];
              }))
            }],
            guides: [{ y: minRatio, label: "Minimum " + pct(minRatio, 0), tone: "bad" }],
            marker: { x: Math.min(maxMint * 1.15, Math.max(mint, maxMint * 0.25)), y: mint > 0 ? ratio : minRatio * 2, label: money(mint, 0) }
          },
          numbers: { maxMint: maxMint, ratio: ratio, liq: liq, feeYr: feeYr }
        });
      }
    },
    {
      id: "perp",
      name: "Perp liquidation",
      group: "Borrowing",
      blurb: "The approximate price that liquidates an isolated perpetual, before fees and funding.",
      fields: [
        { key: "entry", label: "Entry price", value: 3000, min: 0.0001, max: 10000000, step: 1, unit: "$" },
        { key: "leverage", label: "Leverage", value: 5, min: 1.1, max: 100, step: 0.1 },
        { key: "side", label: "Side", value: "long", type: "select", options: [{ value: "long", label: "Long" }, { value: "short", label: "Short" }] },
        { key: "mmr", label: "Maintenance margin", value: 0.5, min: 0, max: 20, step: 0.1, unit: "%" }
      ],
      compute: function (v) {
        const entry = num(v.entry, 3000);
        const lev = num(v.leverage, 5);
        const side = v.side === "short" ? "short" : "long";
        const mmr = num(v.mmr, 0.5);
        if (!(entry > 0 && lev > 1)) return result({ status: "bad", zone: "Outside the safe zone", error: "Entry price has to be above zero and leverage above 1.", verdict: "Set an entry price and leverage above 1." });
        const move = 1 / lev - mmr / 100;
        if (!(move > 0)) return result({ status: "bad", zone: "Outside the safe zone", error: "Maintenance margin is too high for this leverage. The position would have no room.", verdict: "Lower the maintenance margin or the leverage." });
        const liq = side === "long" ? entry * (1 - move) : entry * (1 + move);
        const dist = Math.abs(liq / entry - 1) * 100;
        const status = dist >= 20 ? "good" : dist >= 10 ? "watch" : "bad";
        const xs = linspace(1.5, Math.max(20, lev), 50);
        return result({
          status: status,
          zone: status === "good" ? "In the safe zone" : status === "watch" ? "Watch this" : "Outside the safe zone",
          verdict: "A " + side + " at " + multiple(lev, 1) + " liquidates near " + money(liq) + ", about " + pct(dist, 1) + " from entry, before fees and funding.",
          figure: money(liq),
          figureLabel: "approximate liquidation price",
          formula: "Room = 1 ÷ leverage − maintenance margin. Liquidation sits that far through the entry price.",
          use: "Type the entry, the leverage, whether you are long or short, and the venue’s maintenance margin in percent.",
          read: "This is the isolated-margin sketch. Cross margin, fees, and funding move the real price. A liquidation within 10% of entry is a small adverse move. Past 20% away you have more room, and you have posted less of the position as margin only if leverage is low. Margin per $1,000 of position is $1,000 ÷ leverage.",
          metrics: [
            { label: "Distance from entry", value: pct(dist, 1) },
            { label: "Margin per $1,000", value: money(1000 / lev) },
            { label: "Side", value: side === "long" ? "Long" : "Short" }
          ],
          chart: {
            kind: "line",
            xLabel: "Leverage",
            yLabel: "Liquidation price",
            yUnit: "money",
            series: [{
              name: "Liquidation price",
              points: series(xs.map(function (x) {
                const m = 1 / x - mmr / 100;
                const y = m <= 0 ? null : (side === "long" ? entry * (1 - m) : entry * (1 + m));
                return [x, y];
              }).filter(function (p) { return p[1] != null; }))
            }],
            guides: [{ y: entry, label: "Entry", tone: "watch" }],
            marker: { x: lev, y: liq, label: multiple(lev, 1) }
          },
          numbers: { liq: liq, dist: dist }
        });
      }
    },
    {
      id: "carry",
      name: "Funding carry",
      group: "Yield",
      blurb: "What an 8-hour funding rate pays on a hedged position, and what the short leg can survive.",
      fields: [
        { key: "rate8h", label: "Funding each 8 hours", value: 0.01, min: -1, max: 1, step: 0.001, unit: "%" },
        { key: "shortLev", label: "Leverage on the short", value: 2, min: 1, max: 20, step: 0.1 }
      ],
      compute: function (v) {
        const rate = num(v.rate8h, 0.01);
        const lev = num(v.shortLev, 1);
        if (!(lev >= 1)) return result({ status: "bad", zone: "Outside the safe zone", error: "Short leverage has to be at least 1.", verdict: "Set short leverage to at least 1." });
        const apr = rate * 3 * 365;
        const capital = 1 + 1 / lev;
        const onCapital = apr / capital;
        const liqMove = 100 / lev;
        const status = onCapital <= 0 ? "bad" : liqMove < 25 ? "watch" : "good";
        const xs = linspace(-0.03, 0.05, 70);
        return result({
          status: status,
          zone: status === "good" ? "In the safe zone" : status === "watch" ? "Watch this" : "Outside the safe zone",
          verdict: onCapital <= 0
            ? "You would pay funding. The carry on capital is " + signedPct(onCapital) + "."
            : pct(rate, 3) + " each 8 hours is about " + pct(onCapital) + " a year on the capital this hedge ties up. The short liquidates near a " + pct(liqMove, 0) + " rally.",
          figure: pct(onCapital),
          figureLabel: "on capital tied up",
          formula: "APR on the hedge ≈ funding per 8h × 3 × 365. On capital, divide by (1 + 1 ÷ short leverage).",
          use: "Type the live funding rate for one 8-hour window, in percent, and the leverage on the short perp. 0.01 means 0.01%, not 1%.",
          read: "Positive funding pays the short. Negative funding means the hedge costs you. The APR assumes the rate stays put, which it will not. The short leg still liquidates on a rally of about 100 ÷ leverage, before maintenance margin, so a tighter short needs a larger buffer.",
          metrics: [
            { label: "APR on the hedged size", value: pct(apr) },
            { label: "Capital per $1 hedged", value: money(capital) },
            { label: "Short liquidation move", value: "+" + pct(liqMove, 0) }
          ],
          chart: {
            kind: "line",
            xLabel: "Funding each 8 hours",
            yLabel: "Return on capital",
            yUnit: "percent",
            xUnit: "percent",
            series: [{ name: "Return on capital", points: series(xs.map(function (x) { return [x, x * 3 * 365 / capital]; })) }],
            guides: [{ y: 0, label: "You pay funding", tone: "bad" }],
            marker: { x: rate, y: onCapital, label: pct(rate, 3) }
          },
          numbers: { apr: apr, onCapital: onCapital, capital: capital }
        });
      }
    },
    {
      id: "basis",
      name: "Cash and carry",
      group: "Yield",
      blurb: "The annualised gap between a future and the spot price, if both legs are held to expiry.",
      fields: [
        { key: "spot", label: "Spot price", value: 100, min: 0.0001, max: 10000000, step: 0.01, unit: "$" },
        { key: "future", label: "Future price", value: 102, min: 0.0001, max: 10000000, step: 0.01, unit: "$" },
        { key: "days", label: "Days to expiry", value: 30, min: 1, max: 365, step: 1 }
      ],
      compute: function (v) {
        const spot = num(v.spot, 100);
        const future = num(v.future, 102);
        const days = num(v.days, 30);
        if (!(spot > 0 && future > 0 && days > 0)) return result({ status: "bad", zone: "Outside the safe zone", error: "Spot, future, and days all have to be above zero.", verdict: "Enter a spot, a future, and days to expiry." });
        const b = future / spot - 1;
        const ann = b * 365 / days * 100;
        const status = b > 0.002 ? "good" : b >= 0 ? "watch" : "bad";
        const xs = linspace(7, Math.max(180, days), 50);
        return result({
          status: status,
          zone: status === "good" ? "In the safe zone" : status === "watch" ? "Watch this" : "Outside the safe zone",
          verdict: b >= 0
            ? "The future is " + pct(b * 100) + " over spot, about " + pct(ann) + " a year if you hold both legs to expiry."
            : "The future is " + pct(Math.abs(b * 100)) + " under spot. Cash and carry does not pay in backwardation.",
          figure: pct(ann),
          figureLabel: "annualised basis",
          formula: "Basis = future ÷ spot − 1. Annualised = basis × 365 ÷ days.",
          use: "Type the spot, the dated future, and the days left until that future expires.",
          read: "The locked reading exists only if you hold both legs to expiry and the short is never margin-called. A shorter expiry makes the same price gap look like a higher annual rate. The graph shows that roll-down. A future under spot is a cost, not a carry.",
          metrics: [
            { label: "Basis over the term", value: signedPct(b * 100) },
            { label: "Days", value: String(Math.round(days)) },
            { label: "Locked only if", value: "Held to expiry, margin intact" }
          ],
          chart: {
            kind: "line",
            xLabel: "Days to expiry",
            yLabel: "Annualised basis",
            yUnit: "percent",
            series: [{ name: "Annualised basis", points: series(xs.map(function (d) { return [d, b * 365 / d * 100]; })) }],
            guides: [{ y: 0, label: "No carry", tone: "bad" }],
            marker: { x: days, y: ann, label: Math.round(days) + "d" }
          },
          numbers: { basis: b, ann: ann }
        });
      }
    },
    {
      id: "covered",
      name: "Covered call",
      group: "Yield",
      blurb: "Premium in, upside capped at the strike, and the price where the premium is used up.",
      fields: [
        { key: "spot", label: "Spot price", value: 100, min: 0.0001, max: 10000000, step: 0.01, unit: "$" },
        { key: "strike", label: "Strike", value: 110, min: 0.0001, max: 10000000, step: 0.01, unit: "$" },
        { key: "premium", label: "Premium this period", value: 2, min: 0, max: 50, step: 0.1, unit: "%" },
        { key: "days", label: "Days in the period", value: 7, min: 1, max: 365, step: 1 }
      ],
      compute: function (v) {
        const spot = num(v.spot, 100);
        const strike = num(v.strike, 110);
        const premium = num(v.premium, 2);
        const days = num(v.days, 7);
        if (!(spot > 0 && strike > 0 && days > 0 && premium >= 0)) return result({ status: "bad", zone: "Outside the safe zone", error: "Spot, strike, and days have to be above zero.", verdict: "Enter a spot, a strike, and a period length." });
        const cap = (strike / spot - 1) * 100;
        const maxGain = premium + cap;
        const be = spot * (1 - premium / 100);
        const ann = premium * 365 / days;
        const status = strike <= spot ? "watch" : premium <= 0 ? "watch" : "good";
        const lo = spot * 0.7;
        const hi = Math.max(strike, spot) * 1.25;
        const xs = linspace(lo, hi, 80);
        function pnl(price) {
          const intrinsicCap = Math.min(price, strike);
          return premium + (intrinsicCap / spot - 1) * 100;
        }
        return result({
          status: status,
          zone: status === "good" ? "In the safe zone" : "Watch this",
          verdict: "You collect " + pct(premium) + " this period and give away gains above " + money(strike) + ". The most you can make is " + signedPct(maxGain) + ". You are behind holding once price falls through " + money(be) + ".",
          figure: pct(ann, 1),
          figureLabel: "if this premium repeated all year",
          formula: "Max gain = premium + (strike ÷ spot − 1). Break-even = spot × (1 − premium).",
          use: "Type spot, the strike you would sell, the premium as a percent of spot, and the length of the option period.",
          read: "The flat top of the graph is the cap. Above the strike you stop gaining. Below the break-even you lose like a holder, reduced by the premium you already took. The annualised figure assumes you sell the same premium every period. You will not. A strike at or under spot is already capping you.",
          metrics: [
            { label: "Max gain this period", value: signedPct(maxGain) },
            { label: "Break-even price", value: money(be) },
            { label: "Upside you give away", value: cap > 0 ? "Above " + money(strike) : "Already capped" }
          ],
          chart: {
            kind: "line",
            xLabel: "Price at expiry",
            yLabel: "Gain this period",
            yUnit: "percent",
            xUnit: "money",
            series: [
              { name: "Covered call", points: series(xs.map(function (x) { return [x, pnl(x)]; })) },
              { name: "Holding the asset", points: series(xs.map(function (x) { return [x, (x / spot - 1) * 100]; })), dashed: true }
            ],
            guides: [{ y: 0, label: "Break-even", tone: "watch" }],
            marker: { x: spot, y: pnl(spot), label: "Spot" }
          },
          numbers: { maxGain: maxGain, be: be, ann: ann }
        });
      }
    },
    {
      id: "pt",
      name: "Principal token",
      group: "Yield",
      blurb: "The fixed yield if you buy the principal token and hold it to maturity.",
      fields: [
        { key: "price", label: "Price, in units of the underlying", value: 0.95, min: 0.01, max: 1.5, step: 0.001 },
        { key: "days", label: "Days to maturity", value: 90, min: 1, max: 3650, step: 1 }
      ],
      compute: function (v) {
        const price = num(v.price, 0.95);
        const days = num(v.days, 90);
        if (!(price > 0 && days > 0)) return result({ status: "bad", zone: "Outside the safe zone", error: "Price and days have to be above zero.", verdict: "Enter a price and days to maturity." });
        const fixed = (Math.pow(1 / price, 365 / days) - 1) * 100;
        const simple = (1 / price - 1) * 365 / days * 100;
        const status = price >= 1 ? "bad" : price > 0.99 ? "watch" : "good";
        const xs = linspace(0.88, 1.02, 50);
        return result({
          status: status,
          zone: status === "good" ? "In the safe zone" : status === "watch" ? "Watch this" : "Outside the safe zone",
          verdict: price >= 1
            ? "At " + price.toFixed(3) + " of the underlying there is no fixed yield left. You would pay par or more."
            : "Held to maturity, " + price.toFixed(3) + " of the underlying fixes about " + pct(fixed) + ". The yield token has to beat that to have been the better side.",
          figure: pct(fixed),
          figureLabel: "fixed if held to maturity",
          formula: "Fixed APY = (1 ÷ price) ^ (365 ÷ days) − 1",
          use: "Type the principal-token price as a fraction of the underlying. 0.95 means you pay 0.95 and receive 1 at maturity. Then type the days left.",
          read: "This yield is fixed only if you hold to maturity and the issuer pays. Selling early depends on the market price. The yield token costs about 1 − price, and it profits only if realised variable yield, plus any points you are willing to count separately, beats this fixed rate over the same days.",
          metrics: [
            { label: "Simple annualised", value: pct(simple) },
            { label: "Yield-token cost", value: (1 - price).toFixed(4) + " per unit" },
            { label: "Days", value: String(Math.round(days)) }
          ],
          chart: {
            kind: "line",
            xLabel: "Price of the principal token",
            yLabel: "Fixed APY",
            yUnit: "percent",
            series: [{
              name: "Fixed APY",
              points: series(xs.filter(function (x) { return x > 0 && x < 1.2; }).map(function (x) {
                return [x, (Math.pow(1 / x, 365 / days) - 1) * 100];
              }))
            }],
            guides: [{ y: 0, label: "No fixed yield", tone: "bad" }],
            marker: { x: price, y: fixed, label: price.toFixed(3) }
          },
          numbers: { fixed: fixed, simple: simple }
        });
      }
    },
    {
      id: "apy",
      name: "APR to APY",
      group: "Yield",
      blurb: "What compounding does to a stated APR, and whether gas is eating the extra compounds.",
      fields: [
        { key: "apr", label: "Stated APR", value: 12, min: 0, max: 500, step: 0.1, unit: "%" },
        { key: "n", label: "Compounds per year", value: 12, min: 1, max: 8760, step: 1 },
        { key: "position", label: "Position size", value: 10000, min: 0, max: 100000000, step: 1, unit: "$" },
        { key: "gas", label: "Gas each compound", value: 2, min: 0, max: 10000, step: 0.1, unit: "$" }
      ],
      compute: function (v) {
        const apr = num(v.apr, 12);
        const n = Math.max(1, Math.round(num(v.n, 12)));
        const position = num(v.position, 0);
        const gas = num(v.gas, 0);
        const apy = (Math.pow(1 + apr / 100 / n, n) - 1) * 100;
        const per = position > 0 ? position * apr / 100 / n : 0;
        const drag = position > 0 ? gas * n / position * 100 : 0;
        const worth = !(position > 0 && gas > 0) || per >= 10 * gas;
        const status = position > 0 && gas > 0 && !worth ? "bad" : drag > apy * 0.25 && position > 0 ? "watch" : "good";
        const xs = [1, 2, 4, 12, 52, 365].filter(function (x) { return x <= Math.max(n, 12) * 2 || x <= 365; });
        const uniq = [];
        [1, 2, 4, 12, 52, 365].forEach(function (x) { if (uniq.indexOf(x) < 0) uniq.push(x); });
        if (uniq.indexOf(n) < 0) uniq.push(n);
        uniq.sort(function (a, b) { return a - b; });
        return result({
          status: status,
          zone: status === "good" ? "In the safe zone" : status === "watch" ? "Watch this" : "Outside the safe zone",
          verdict: position > 0 && gas > 0
            ? pct(apr) + " compounded " + n + " times is " + pct(apy) + " before gas. Each compound earns " + money(per) + " and costs " + money(gas) + (worth ? "." : ". Compound less often.")
            : pct(apr) + " compounded " + n + " times a year is " + pct(apy) + " before gas.",
          figure: pct(apy),
          figureLabel: "APY before gas",
          formula: "APY = (1 + APR ÷ compounds) ^ compounds − 1",
          use: "Type the stated APR and how many times a year you would compound. Add position size and gas when you want to know if the extra transactions are worth sending.",
          read: "Compounding lifts APY, and the lift flattens quickly. Gas is a drag of gas × compounds ÷ position. A reward under about ten times the gas is a sign to compound less often. The dashed line is APY after that gas drag.",
          metrics: [
            { label: "Reward each compound", value: position > 0 ? money(per) : "Add a position" },
            { label: "Gas drag", value: position > 0 ? pct(drag) + " / year" : "—" },
            { label: "Worth compounding", value: position > 0 && gas > 0 ? (worth ? "Yes, reward covers 10× gas" : "No, compound less often") : "Add gas to check" }
          ],
          chart: {
            kind: "line",
            xLabel: "Compounds per year",
            yLabel: "APY",
            yUnit: "percent",
            series: [
              { name: "APY before gas", points: series(uniq.map(function (x) { return [x, (Math.pow(1 + apr / 100 / x, x) - 1) * 100]; })) },
              { name: "After gas", points: position > 0 ? series(uniq.map(function (x) { return [x, (Math.pow(1 + apr / 100 / x, x) - 1) * 100 - gas * x / position * 100]; })) : [], dashed: true }
            ],
            guides: [],
            marker: { x: n, y: apy, label: String(n) }
          },
          numbers: { apy: apy, per: per, drag: drag }
        });
      }
    },
    {
      id: "expected",
      name: "Risk-adjusted yield",
      group: "The book",
      blurb: "Headline yield after a loss you might actually take, and after costs.",
      fields: [
        { key: "yieldApy", label: "Headline APY", value: 12, min: -50, max: 500, step: 0.1, unit: "%" },
        { key: "lossProb", label: "Chance of a loss this year", value: 0.05, min: 0, max: 1, step: 0.01 },
        { key: "lgd", label: "Share lost if it happens", value: 0.4, min: 0, max: 1, step: 0.01 },
        { key: "costs", label: "Costs per year", value: 1, min: 0, max: 50, step: 0.1, unit: "%" }
      ],
      compute: function (v) {
        const y = num(v.yieldApy, 12);
        const p = num(v.lossProb, 0.05);
        const lgd = num(v.lgd, 1);
        const costs = num(v.costs, 0);
        if (!(p >= 0 && p <= 1 && lgd >= 0 && lgd <= 1)) return result({ status: "bad", zone: "Outside the safe zone", error: "The chance of loss and the share lost both sit between 0 and 1.", verdict: "Enter the chance of loss and the share lost as decimals between 0 and 1." });
        const haircut = p * lgd * 100;
        const net = y - haircut - costs;
        const status = net <= 0 ? "bad" : haircut > Math.max(y, 0) / 2 ? "watch" : "good";
        return result({
          status: status,
          zone: status === "good" ? "In the safe zone" : status === "watch" ? "Watch this" : "Outside the safe zone",
          verdict: "After a " + pct(haircut) + " expected loss and " + pct(costs) + " of costs, " + pct(y) + " headline becomes " + pct(net) + ".",
          figure: pct(net),
          figureLabel: "risk-adjusted",
          formula: "Risk-adjusted = headline − (chance of loss × share lost) − costs",
          use: "Type the advertised yield, your own estimate of how likely a real loss is this year, how much of the position that loss would take, and your costs. Decimals: 0.05 is a 5% chance.",
          read: "The bars take the headline apart. Expected loss is not a forecast of this year. It is the average hit if you repeated the bet. When that hit is more than half the headline, or the result is at or below zero, the yield is mostly payment for a risk you may not want.",
          metrics: [
            { label: "Headline", value: pct(y) },
            { label: "Expected loss", value: pct(haircut) },
            { label: "Costs", value: pct(costs) }
          ],
          chart: {
            kind: "bar",
            yLabel: "Percent",
            bars: [
              { label: "Headline", value: y, tone: "neutral" },
              { label: "Expected loss", value: -haircut, tone: "bad" },
              { label: "Costs", value: -costs, tone: "watch" },
              { label: "Left", value: net, tone: net > 0 ? "good" : "bad" }
            ]
          },
          numbers: { haircut: haircut, net: net }
        });
      }
    },
    {
      id: "income",
      name: "Income plan",
      group: "The book",
      blurb: "Risk-adjusted income across positions, then a payout that leaves a loss buffer.",
      fields: [
        { key: "payout", label: "Share of expected income you pay out", value: 0.7, min: 0, max: 1, step: 0.05 },
        {
          key: "positions",
          type: "positions",
          value: [
            { name: "Stables", amount: 100000, yield: 8, lossProb: 0.01, lgd: 1 },
            { name: "ETH pool", amount: 50000, yield: 20, lossProb: 0.15, lgd: 0.5 }
          ]
        }
      ],
      compute: function (v) {
        const payout = num(v.payout, 0.7);
        const rowsIn = Array.isArray(v.positions) ? v.positions : [];
        if (!(payout >= 0 && payout <= 1)) return result({ status: "bad", zone: "Outside the safe zone", error: "The payout share sits between 0 and 1.", verdict: "Set the payout share between 0 and 1." });
        let total = 0;
        let exp = 0;
        const tableRows = [];
        const bars = [];
        rowsIn.forEach(function (row) {
          const name = String(row.name || "Position").slice(0, 32);
          const amt = num(row.amount, 0);
          const y = num(row.yield, 0);
          const p = num(row.lossProb, 0);
          const lgd = num(row.lgd, 1);
          if (!(amt > 0)) return;
          const net = y - p * lgd * 100;
          const inc = amt * net / 100;
          total += amt;
          exp += inc;
          tableRows.push([name, money(amt, 0), pct(y), pct(p * lgd * 100), pct(net), money(inc, 0)]);
          bars.push({ label: name, value: inc, tone: inc >= 0 ? "good" : "bad" });
        });
        if (!(total > 0)) return result({ status: "bad", zone: "Outside the safe zone", error: "Add at least one position with an amount above zero.", verdict: "Add a position with an amount above zero." });
        const blended = exp / total * 100;
        const paid = exp * payout;
        const buffer = exp - paid;
        const status = exp <= 0 ? "bad" : buffer <= 0 ? "watch" : "good";
        bars.push({ label: "Paid out", value: paid, tone: "neutral" });
        bars.push({ label: "Buffer", value: buffer, tone: buffer > 0 ? "good" : "bad" });
        return result({
          status: status,
          zone: status === "good" ? "In the safe zone" : status === "watch" ? "Watch this" : "Outside the safe zone",
          verdict: "Expected income is " + money(exp, 0) + " a year, " + pct(blended) + " on " + money(total, 0) + ". Paying out " + pct(payout * 100, 0) + " is " + money(paid, 0) + " a year, " + money(paid / 12, 0) + " a month, and keeps " + money(buffer, 0) + " as a buffer.",
          figure: money(paid / 12, 0),
          figureLabel: "a month if you pay that share",
          formula: "Each position: income = amount × (yield − chance of loss × share lost). Payout = total income × the share you take.",
          use: "Add each position you would actually hold. Yield, chance of loss, and share lost are your estimates. The payout share is the part of expected income you intend to spend. 0.70 spends 70% and keeps 30%.",
          read: "Income here is already net of the expected loss. The buffer is what you do not spend, so a loss does not force you to sell. A plan that pays out everything, or whose expected income is at or below zero, has no shock absorber.",
          metrics: [
            { label: "Capital", value: money(total, 0) },
            { label: "Blended risk-adjusted yield", value: pct(blended) },
            { label: "Expected income", value: money(exp, 0) + " / year" },
            { label: "Left as buffer", value: money(buffer, 0) + " / year" }
          ],
          table: {
            headers: ["Position", "Amount", "Yield", "Expected loss", "Net", "Income / year"],
            rows: tableRows
          },
          chart: { kind: "bar", yLabel: "Dollars a year", bars: bars },
          numbers: { total: total, exp: exp, blended: blended, paid: paid, buffer: buffer }
        });
      }
    },
    {
      id: "bank",
      name: "Balance sheet",
      group: "The book",
      blurb: "Equity, loan to value, health factor, and how many months the reserve covers.",
      fields: [
        { key: "collateral", label: "Collateral", value: 200000, min: 0, max: 100000000, step: 100, unit: "$" },
        { key: "debt", label: "Debt", value: 40000, min: 0, max: 100000000, step: 100, unit: "$" },
        { key: "lt", label: "Liquidation threshold", value: 0.8, min: 0.05, max: 0.99, step: 0.01 },
        { key: "borrowApy", label: "Borrow APY", value: 8, min: 0, max: 100, step: 0.1, unit: "%" },
        { key: "reserve", label: "Stablecoin reserve", value: 40000, min: 0, max: 100000000, step: 100, unit: "$" },
        { key: "other", label: "Other assets", value: 80000, min: 0, max: 100000000, step: 100, unit: "$" },
        { key: "spend", label: "Monthly spending", value: 5000, min: 0, max: 1000000, step: 50, unit: "$" },
        { key: "maxLtv", label: "Your maximum loan to value", value: 30, min: 1, max: 90, step: 1, unit: "%" }
      ],
      compute: function (v) {
        const coll = num(v.collateral, 0);
        const debt = num(v.debt, 0);
        const lt = num(v.lt, 0.8);
        const borrow = num(v.borrowApy, 0);
        const reserve = num(v.reserve, 0);
        const other = num(v.other, 0);
        const spend = num(v.spend, 0);
        const maxLtv = num(v.maxLtv, 30);
        if (!(lt > 0 && lt < 1)) return result({ status: "bad", zone: "Outside the safe zone", error: "The liquidation threshold sits between 0 and 1.", verdict: "Set the liquidation threshold between 0 and 1." });
        const ltv = coll > 0 ? debt / coll * 100 : (debt > 0 ? Infinity : 0);
        const hf = debt > 0 ? coll * lt / debt : Infinity;
        const interest = debt * borrow / 100 / 12;
        const obligations = spend + interest;
        const months = obligations > 0 ? reserve / obligations : Infinity;
        const equity = coll + reserve + other - debt;
        const checks = [
          { label: "Loan to value within your maximum", ok: ltv <= maxLtv },
          { label: "Health factor at least 2", ok: hf >= 2 },
          { label: "Reserve covers 6 months", ok: months >= 6 }
        ];
        const fails = checks.filter(function (c) { return !c.ok; }).length;
        const status = fails === 0 ? "good" : (hf < 1.5 || months < 3) ? "bad" : "watch";
        return result({
          status: status,
          zone: status === "good" ? "In the safe zone" : status === "watch" ? "Watch this" : "Outside the safe zone",
          verdict: "Equity is " + money(equity, 0) + ". The reserve covers " + (Number.isFinite(months) ? months.toFixed(1) : "more than") + " months of spending and interest. " + (fails === 0 ? "All three book rules pass." : fails + " of the three book rules fail."),
          figure: Number.isFinite(months) ? months.toFixed(1) : "—",
          figureLabel: "months of reserve",
          formula: "Equity = assets − debt. Health factor = collateral × liquidation threshold ÷ debt. Months = reserve ÷ (spending + monthly interest).",
          use: "Type the balance sheet you actually have. The maximum loan to value is your rule, in percent. 30 means 30%. The liquidation threshold is the protocol’s decimal.",
          read: "Three rules sit under the numbers. Loan to value at or under your maximum. Health factor at or above 2. Reserve covering at least six months of spending plus interest. Missing one is a watch. A health factor under 1.5, or a reserve under three months, is the point to change the book before adding a new position.",
          metrics: [
            { label: "Equity", value: money(equity, 0) },
            { label: "Loan to value", value: Number.isFinite(ltv) ? pct(ltv, 1) : "No collateral" },
            { label: "Health factor", value: Number.isFinite(hf) ? hf.toFixed(2) : "No debt" },
            { label: "Interest", value: money(interest, 0) + " / month" }
          ],
          checks: checks,
          chart: {
            kind: "bar",
            yLabel: "Dollars",
            bars: [
              { label: "Collateral", value: coll, tone: "neutral" },
              { label: "Reserve", value: reserve, tone: "good" },
              { label: "Other", value: other, tone: "neutral" },
              { label: "Debt", value: -debt, tone: "bad" },
              { label: "Equity", value: equity, tone: equity >= 0 ? "good" : "bad" }
            ]
          },
          numbers: { equity: equity, ltv: ltv, hf: hf, months: months, interest: interest }
        });
      }
    },
    {
      id: "twr",
      name: "Time-weighted return",
      group: "The book",
      blurb: "The return of the decisions, with deposits and withdrawals taken out of the story.",
      fields: [
        { key: "start", label: "Value at the start", value: 10000, min: 0, max: 100000000, step: 1, unit: "$" },
        { key: "end", label: "Value at the end", value: 11200, min: 0, max: 100000000, step: 1, unit: "$" },
        { key: "deposits", label: "Net deposits over the stretch", value: 500, min: -100000000, max: 100000000, step: 1, unit: "$" },
        { key: "periods", type: "periods", value: [5, -2, 4] }
      ],
      compute: function (v) {
        const periods = (Array.isArray(v.periods) ? v.periods : []).map(function (p) { return num(p, 0); });
        if (!periods.length) return result({ status: "bad", zone: "Outside the safe zone", error: "Add at least one period return.", verdict: "Add the return for each stretch between cash flows." });
        let growth = 1;
        const path = [{ x: 0, y: 1 }];
        periods.forEach(function (r, i) {
          growth *= 1 + r / 100;
          path.push({ x: i + 1, y: growth });
        });
        const twr = (growth - 1) * 100;
        const start = num(v.start, NaN);
        const end = num(v.end, NaN);
        const dep = num(v.deposits, NaN);
        let simple = null;
        if (Number.isFinite(start) && Number.isFinite(end) && Number.isFinite(dep) && (start + dep) !== 0) {
          simple = (end - start - dep) / (start + dep) * 100;
        }
        const status = twr > 0.5 ? "good" : twr >= 0 ? "watch" : "bad";
        return result({
          status: status,
          zone: status === "good" ? "In the safe zone" : status === "watch" ? "Watch this" : "Outside the safe zone",
          verdict: "Linking these periods gives " + signedPct(twr) + "." + (simple == null ? "" : " A simple look at money in and money out says " + signedPct(simple) + ", and deposits are what bend that number."),
          figure: signedPct(twr),
          figureLabel: "time-weighted return",
          formula: "Time-weighted return = (1 + first) × (1 + next) × … − 1",
          use: "Split the track record at every deposit and withdrawal. Type each stretch’s own percent return. The start, end, and net deposits are only there to show how a simple gain differs.",
          read: "The line is $1 growing through your decisions. A deposit should not look like skill, and a withdrawal should not look like a loss. When the simple gain and the time-weighted return disagree, believe the time-weighted one for the strategy and the simple one for the cash.",
          metrics: [
            { label: "Periods", value: String(periods.length) },
            { label: "Simple gain on cash in", value: simple == null ? "Add start, end, and deposits" : signedPct(simple) },
            { label: "Ending value of $1", value: "$" + growth.toFixed(3) }
          ],
          chart: {
            kind: "line",
            xLabel: "Period",
            yLabel: "Growth of $1",
            yUnit: "number",
            series: [{ name: "Growth of $1", points: path }],
            guides: [{ y: 1, label: "Started", tone: "watch" }],
            marker: { x: periods.length, y: growth, label: signedPct(twr) }
          },
          numbers: { twr: twr, simple: simple, growth: growth }
        });
      }
    },
    {
      id: "airdrop",
      name: "Airdrop value",
      group: "The book",
      blurb: "Expected value of a drop after the chance it never arrives and the costs of chasing it.",
      fields: [
        { key: "probability", label: "Chance you receive it", value: 0.2, min: 0, max: 1, step: 0.01 },
        { key: "value", label: "Value if you do", value: 500, min: 0, max: 10000000, step: 1, unit: "$" },
        { key: "costs", label: "Costs to chase it", value: 40, min: 0, max: 1000000, step: 1, unit: "$" }
      ],
      compute: function (v) {
        const p = num(v.probability, 0);
        const value = num(v.value, 0);
        const costs = num(v.costs, 0);
        if (!(p >= 0 && p <= 1)) return result({ status: "bad", zone: "Outside the safe zone", error: "The chance sits between 0 and 1.", verdict: "Enter the chance as a decimal between 0 and 1." });
        const ev = p * value - costs;
        const status = ev > costs * 0.25 && ev > 0 ? "good" : ev > 0 ? "watch" : "bad";
        const xs = linspace(0, 1, 21);
        return result({
          status: status,
          zone: status === "good" ? "In the safe zone" : status === "watch" ? "Watch this" : "Outside the safe zone",
          verdict: ev > 0
            ? "Expected value is " + money(ev) + ". You are paying " + money(costs) + " to chase a " + pct(p * 100, 0) + " chance of " + money(value) + "."
            : "Expected value is " + money(ev) + ". The costs are ahead of the chance-weighted payout.",
          figure: money(ev),
          figureLabel: "expected value",
          formula: "Expected value = chance × value if it pays − costs",
          use: "Type your honest chance, the value you would actually receive if it pays, and every cost: gas, bridges, and the time you could have used elsewhere, in dollars.",
          read: "Above zero, the bet is worth more than it costs on these inputs. A thin margin over costs is still a watch, because the chance is a guess. The line shows how the expected value moves if you were more or less sure.",
          metrics: [
            { label: "Chance-weighted payout", value: money(p * value) },
            { label: "Costs", value: money(costs) },
            { label: "Chance", value: pct(p * 100, 0) }
          ],
          chart: {
            kind: "line",
            xLabel: "Chance it pays",
            yLabel: "Expected value",
            yUnit: "money",
            xUnit: "share",
            series: [{ name: "Expected value", points: series(xs.map(function (x) { return [x, x * value - costs]; })) }],
            guides: [{ y: 0, label: "Costs win", tone: "bad" }],
            marker: { x: p, y: ev, label: pct(p * 100, 0) }
          },
          numbers: { ev: ev }
        });
      }
    },
    {
      id: "var",
      name: "Value at risk",
      group: "The book",
      blurb: "A one-day loss estimate from volatility. Crypto tails are fatter, so treat it as a floor.",
      fields: [
        { key: "position", label: "Position size", value: 50000, min: 1, max: 100000000, step: 100, unit: "$" },
        { key: "vol", label: "Annualised volatility", value: 80, min: 1, max: 400, step: 1, unit: "%" },
        { key: "z", label: "Confidence", value: "1.65", type: "select", options: [{ value: "1.65", label: "95% of days (z = 1.65)" }, { value: "2.33", label: "99% of days (z = 2.33)" }] }
      ],
      compute: function (v) {
        const position = num(v.position, 50000);
        const vol = num(v.vol, 80);
        const z = num(v.z, 1.65);
        if (!(position > 0 && vol > 0 && z > 0)) return result({ status: "bad", zone: "Outside the safe zone", error: "Position, volatility, and the confidence level have to be above zero.", verdict: "Enter a position and a volatility above zero." });
        const daily = vol / 100 / Math.sqrt(365);
        const loss = z * daily * position;
        const share = z * daily * 100;
        const status = share >= 10 ? "bad" : share >= 5 ? "watch" : "good";
        const xs = linspace(10, Math.max(150, vol), 40);
        return result({
          status: status,
          zone: status === "good" ? "In the safe zone" : status === "watch" ? "Watch this" : "Outside the safe zone",
          verdict: "On a normal-returns model, about 1 day in " + (z > 2 ? "100" : "20") + " loses at least " + money(loss, 0) + ", which is " + pct(share) + " of the position. Real crypto days run past that.",
          figure: money(loss, 0),
          figureLabel: "one-day floor",
          formula: "One-day move ≈ confidence × annual volatility ÷ √365. Loss ≈ that move × position.",
          use: "Type the position in dollars and the annualised volatility you believe. Pick 95% for a day that should be rare, or 99% for a day that should be very rare, on a normal model.",
          read: "The number is a floor, not a worst case. The model assumes a tidy bell curve. Crypto has fatter tails, so size the book for a loss beyond the line. A one-day floor above 10% of the position is a large swing for money you cannot leave alone.",
          metrics: [
            { label: "Daily volatility", value: pct(daily * 100) },
            { label: "Share of the position", value: pct(share) },
            { label: "Read it as", value: "A floor, not a cap" }
          ],
          chart: {
            kind: "line",
            xLabel: "Annualised volatility",
            yLabel: "One-day loss",
            yUnit: "money",
            xUnit: "percent",
            series: [{ name: "One-day floor", points: series(xs.map(function (x) { return [x, z * (x / 100) / Math.sqrt(365) * position]; })) }],
            guides: [{ y: position * 0.1, label: "10% of position", tone: "bad" }],
            marker: { x: vol, y: loss, label: pct(vol, 0) }
          },
          numbers: { loss: loss, daily: daily * 100, share: share }
        });
      }
    }
  ];

  function toolById(id) {
    for (let i = 0; i < tools.length; i++) if (tools[i].id === id) return tools[i];
    return null;
  }

  function defaults(tool) {
    const v = {};
    tool.fields.forEach(function (f) {
      v[f.key] = f.type === "positions" || f.type === "periods" ? JSON.parse(JSON.stringify(f.value)) : f.value;
    });
    return v;
  }

  function run(id, values) {
    const tool = toolById(id);
    if (!tool) return result({ status: "bad", error: "Unknown calculator.", verdict: "That calculator is not in this set." });
    try {
      return tool.compute(values || defaults(tool));
    } catch (err) {
      return result({ status: "bad", zone: "Outside the safe zone", error: "Those inputs cannot be calculated.", verdict: "Those inputs cannot be calculated." });
    }
  }

  return {
    tools: tools,
    toolById: toolById,
    defaults: defaults,
    run: run,
    il: il
  };
});
