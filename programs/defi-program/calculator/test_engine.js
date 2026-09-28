#!/usr/bin/env node
"use strict";

const calc = require("./engine.js");
const assert = require("assert");

function close(actual, expected, tol, label) {
  const ok = Math.abs(actual - expected) <= tol;
  if (!ok) {
    console.error("FAIL", label, "got", actual, "expected", expected);
    process.exitCode = 1;
  }
}

function run(id) {
  const tool = calc.toolById(id);
  return calc.run(id, calc.defaults(tool));
}

const il = run("il");
close(il.numbers.il * 100, -5.72, 0.02, "il 2x");
assert.strictEqual(il.status, "bad");

const half = calc.run("il", { ratio: 0.5 });
close(half.numbers.il * 100, -5.72, 0.02, "il 0.5x mirrors 2x");

const quiet = calc.run("il", { ratio: 1.25 });
close(quiet.numbers.il * 100, -0.62, 0.02, "il 1.25x");
assert.strictEqual(quiet.status, "good");

const lp = run("lp");
close(lp.numbers.need, 24.58, 0.05, "lp fee needed");
close(lp.numbers.net, -0.38, 0.05, "lp net");
assert.strictEqual(lp.status, "watch");

const covered = calc.run("lp", { ratio: 1.5, days: 30, feeApr: 40 });
assert.ok(covered.numbers.net > 0, "higher fee covers the gap");
assert.strictEqual(covered.status, "good");

const cl = run("cl");
close(cl.numbers.eff, 7.5, 0.15, "cl efficiency");
close(cl.numbers.mid, 2400, 0.1, "cl mid");
assert.strictEqual(cl.status, "good");
assert.ok(calc.run("cl", { low: 3200, high: 1800 }).error);

const lvr = run("lvr");
close(lvr.numbers.rate, 8, 0.01, "lvr 80 vol");
close(lvr.numbers.net, 17, 0.01, "lvr net");
assert.strictEqual(lvr.status, "good");
assert.strictEqual(calc.run("lvr", { vol: 80, feeApr: 4 }).status, "bad");

const health = run("health");
close(health.numbers.hf, 2.4, 0.01, "hf");
close(health.numbers.liq, 1250, 0.01, "liq price");
assert.strictEqual(health.status, "good");
assert.strictEqual(calc.run("health", { qty: 10, price: 3000, lt: 0.8, debt: 20000 }).status, "bad");

const loop = run("loop");
close(loop.numbers.lev, 2.73, 0.02, "loop lev");
close(loop.numbers.net, 8.47, 0.02, "loop net");
close(loop.numbers.breakeven, 7.88, 0.05, "loop breakeven");
assert.strictEqual(loop.status, "good");
assert.strictEqual(calc.run("loop", { ltv: 0.75, loops: 3, collateralApy: 5, borrowApy: 9 }).status, "bad");

const supply = run("supply");
close(supply.numbers.supply, 5.04, 0.01, "supply");
assert.strictEqual(supply.status, "good");
assert.strictEqual(calc.run("supply", { borrowApy: 8, utilisation: 0.97, reserve: 0.1 }).status, "bad");

const cdp = run("cdp");
close(cdp.numbers.maxMint, 20000, 0.1, "cdp max");
close(cdp.numbers.ratio, 375, 0.1, "cdp ratio");
close(cdp.numbers.liq, 1200, 0.1, "cdp liq");
close(cdp.numbers.feeYr, 160, 0.1, "cdp fee");
assert.strictEqual(cdp.status, "good");

const perp = run("perp");
close(perp.numbers.liq, 2415, 0.6, "perp liq");
close(perp.numbers.dist, 19.5, 0.15, "perp dist");
assert.strictEqual(perp.status, "watch");
const short = calc.run("perp", { entry: 3000, leverage: 5, side: "short", mmr: 0.5 });
assert.ok(short.numbers.liq > 3000, "short liquidates above entry");

const carry = run("carry");
close(carry.numbers.apr, 10.95, 0.02, "carry apr");
close(carry.numbers.onCapital, 7.3, 0.05, "carry on capital");
assert.strictEqual(carry.status, "good");
assert.strictEqual(calc.run("carry", { rate8h: -0.01, shortLev: 2 }).status, "bad");

const basis = run("basis");
close(basis.numbers.basis * 100, 2, 0.01, "basis");
close(basis.numbers.ann, 24.33, 0.05, "basis ann");
assert.strictEqual(basis.status, "good");
assert.strictEqual(calc.run("basis", { spot: 100, future: 99, days: 30 }).status, "bad");

const call = run("covered");
close(call.numbers.maxGain, 12, 0.02, "covered max");
close(call.numbers.be, 98, 0.01, "covered be");
close(call.numbers.ann, 104.3, 0.15, "covered ann");

const pt = run("pt");
close(pt.numbers.fixed, 23.12, 0.05, "pt fixed");
close(pt.numbers.simple, 21.35, 0.05, "pt simple");
assert.strictEqual(pt.status, "good");
assert.strictEqual(calc.run("pt", { price: 1.02, days: 90 }).status, "bad");

const apy = run("apy");
close(apy.numbers.apy, 12.68, 0.03, "apy");
close(apy.numbers.per, 100, 0.01, "apy reward");
assert.strictEqual(apy.status, "good");
assert.strictEqual(calc.run("apy", { apr: 12, n: 365, position: 1000, gas: 15 }).status, "bad");

const expected = run("expected");
close(expected.numbers.haircut, 2, 0.01, "expected haircut");
close(expected.numbers.net, 9, 0.01, "expected net");
assert.strictEqual(expected.status, "good");

const income = run("income");
close(income.numbers.total, 150000, 0.1, "income capital");
close(income.numbers.exp, 13250, 0.5, "income");
close(income.numbers.blended, 8.83, 0.03, "income blend");
close(income.numbers.paid, 9275, 0.5, "income payout");
close(income.numbers.buffer, 3975, 0.5, "income buffer");
assert.strictEqual(income.status, "good");

const bank = run("bank");
close(bank.numbers.equity, 280000, 0.1, "equity");
close(bank.numbers.ltv, 20, 0.05, "ltv");
close(bank.numbers.hf, 4, 0.01, "bank hf");
close(bank.numbers.months, 7.6, 0.05, "runway");
assert.strictEqual(bank.status, "good");
assert.ok(bank.checks.every(function (c) { return c.ok; }));

const twr = run("twr");
close(twr.numbers.twr, 7.02, 0.03, "twr");
close(twr.numbers.simple, 6.67, 0.05, "simple");
assert.strictEqual(twr.status, "good");

const drop = run("airdrop");
close(drop.numbers.ev, 60, 0.01, "airdrop ev");
assert.strictEqual(drop.status, "good");
assert.strictEqual(calc.run("airdrop", { probability: 0.1, value: 100, costs: 40 }).status, "bad");

const risk = run("var");
close(risk.numbers.daily, 4.19, 0.03, "daily vol");
close(risk.numbers.loss, 3455, 5, "var dollars");
close(risk.numbers.share, 6.91, 0.05, "var share");
assert.strictEqual(risk.status, "watch");

assert.strictEqual(calc.tools.length, 20);

if (process.exitCode) {
  console.error("Calculator checks failed");
} else {
  console.log("20 calculators match the lesson figures.");
}
