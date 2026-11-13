#!/usr/bin/env python3
"""Build the Atlas course file, the text, and the image manifest.

Run from anywhere:
    python3 dist/atlas/build_atlas.py

If a PNG exists in dist/atlas/images/ under the manifest file name, it is
inlined in place of the labelled diagram.
"""
from __future__ import annotations

import base64
import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from lib_diagrams import DIAGRAMS  # noqa: E402
from lib_lessons import LEVELS, flat_lessons, lesson_index  # noqa: E402

ROOT = HERE.parents[1]
GLOSSARY_PATH = ROOT / "sites" / "atlas" / "data" / "glossary.json"
IMAGES = HERE / "images"
OUT_HTML = HERE / "atlas.html"
OUT_MD = HERE / "ATLAS_CONTENT.md"
OUT_JSON = HERE / "IMAGE_MANIFEST.json"
OUT_MAN_MD = HERE / "IMAGE_MANIFEST.md"

CATEGORY_LESSON = {
    "grid": "grid-what",
    "market-structure": "market-structure",
    "technical-analysis": "support-resistance",
    "risk": "risk-basics",
    "security": "wallets",
    "execution": "order-types",
    "derivatives": "options-basics",
    "crypto": "markets",
    "defi": "wallets",
    "on-chain": "wallets",
    "research": "journaling",
    "macro": "markets",
    "portfolio": "building-a-system",
    "psychology": "psychology",
    "automation": "grid-how",
}


def e(text: str) -> str:
    return html.escape(str(text), quote=True)


def lesson_for_term(term: dict) -> str:
    anchor = term["anchor"]
    category = term["category"]
    if category == "grid":
        if any(word in anchor for word in ("risk", "inventory", "liquidat")):
            return "grid-risk"
        if "count" in anchor or "spac" in anchor or "arithmetic" in anchor or "geometric" in anchor:
            return "grid-range"
        if any(word in anchor for word in ("cycle", "profit", "fee")):
            return "grid-how"
        return "grid-what"
    if category == "derivatives":
        if "fund" in anchor:
            return "funding"
        if "basis" in anchor or "perpetual" in anchor or "futures" in anchor:
            return "perpetuals"
        if "call" in anchor or "put" in anchor:
            return "calls-puts"
        if any(word in anchor for word in ("delta", "gamma", "theta", "vega", "greek")):
            return "greeks"
        return "options-basics"
    if category == "risk":
        if "journal" in anchor or "expect" in anchor:
            return "journaling"
        if "leverage" in anchor or "liquidat" in anchor or "margin" in anchor:
            return "leverage-multiples"
        return "risk-basics"
    return CATEGORY_LESSON.get(category, "markets")


def figure(file_name: str) -> str:
    meta = DIAGRAMS[file_name]
    png = IMAGES / file_name
    if png.exists():
        blob = base64.b64encode(png.read_bytes()).decode("ascii")
        visual = (
            f'<img alt="{e(meta["alt"])}" width="1600" height="900" '
            f'src="data:image/png;base64,{blob}">'
        )
    else:
        visual = meta["svg"]
    return (
        f'<figure data-image="{e(file_name)}">{visual}'
        f"<figcaption>{e(meta['alt'])}</figcaption></figure>"
    )


def lesson_html(level, module, lesson, nxt) -> str:
    parts = [
        f'<p class="crumb">{e(level["title"])} / {e(module["title"])}</p>',
        f'<p class="learn"><strong>What you\'ll learn: </strong>{e(lesson["learn"])}</p>',
        f'<h1>{e(lesson["title"])}</h1>',
    ]
    for paragraph in lesson["paragraphs"]:
        parts.append(f"<p>{e(paragraph)}</p>")
    parts.append("<h2>Example</h2><ul>")
    for line in lesson["example"]:
        parts.append(f"<li>{e(line)}</li>")
    parts.append("</ul>")
    for image in lesson["images"]:
        parts.append(figure(image))
    parts.append("<h2>Recap</h2><ul>")
    for line in lesson["recap"]:
        parts.append(f"<li>{e(line)}</li>")
    parts.append("</ul>")
    if nxt:
        parts.append(
            f'<p class="next"><a href="#/lesson/{nxt["id"]}">Next lesson: {e(nxt["title"])}</a></p>'
        )
    else:
        parts.append('<p class="next"><a href="#/glossary">Next: Glossary</a></p>')
    return "".join(parts)


def module_html(level, module) -> str:
    items = []
    for lesson in module["lessons"]:
        items.append(
            f'<li><a href="#/lesson/{lesson["id"]}"><strong>{e(lesson["title"])}</strong>'
            f'<span>{e(lesson["learn"])}</span></a></li>'
        )
    return (
        f'<p class="crumb">{e(level["title"])}</p>'
        f'<h1>{e(module["title"])}</h1>'
        f'<p>{e(module["blurb"])}</p>'
        f'<ol class="index">{"".join(items)}</ol>'
        f'<p class="next"><a href="#/lesson/{module["lessons"][0]["id"]}">Next lesson: {e(module["lessons"][0]["title"])}</a></p>'
    )


def level_html(level) -> str:
    blocks = []
    for module in level["modules"]:
        links = "".join(
            f'<li><a href="#/lesson/{lesson["id"]}">{e(lesson["title"])}</a></li>'
            for lesson in module["lessons"]
        )
        blocks.append(
            f'<section><h2><a href="#/module/{module["id"]}">{e(module["title"])}</a></h2>'
            f'<p>{e(module["blurb"])}</p><ol>{links}</ol></section>'
        )
    return f'<h1>{e(level["title"])}</h1><p>{e(level["blurb"])}</p>' + "".join(blocks)


def start_html(first_lessons) -> str:
    items = []
    for number, lesson in enumerate(first_lessons, start=1):
        items.append(
            f'<li><a href="#/lesson/{lesson["id"]}"><strong>{number}. {e(lesson["title"])}</strong>'
            f'<span>{e(lesson["learn"])}</span></a></li>'
        )
    return (
        "<h1>Atlas</h1>"
        "<p>Atlas is a directory for learning how markets work, how to read structure, how grid bots behave, "
        "and how leverage and later contracts change the risk.</p>"
        "<p>Educational content only, not financial advice.</p>"
        "<p>If you are new, follow the list below from the top. Each lesson says what you will learn, "
        "shows a labelled picture, walks through made-up numbers, and ends with the next lesson. "
        "Use the glossary when a word is new. Use the tools when you want to change a number and see the arithmetic.</p>"
        + figure("atlas-start-01.png")
        + '<h2>Start here</h2><ol class="index">'
        + "".join(items)
        + "</ol><p>After those lessons, open Intermediate. Grid bots sit in that level, after the structure lessons.</p>"
        + f'<p class="next"><a href="#/lesson/{first_lessons[0]["id"]}">Next lesson: {e(first_lessons[0]["title"])}</a></p>'
    )


def glossary_html(terms, titles) -> str:
    grouped: dict[str, list] = {}
    for term in terms:
        letter = term["term"][0].upper()
        if not letter.isalpha():
            letter = "#"
        grouped.setdefault(letter, []).append(term)
    letters = "".join(
        f'<a href="#/glossary/letter-{letter}">{letter}</a>' for letter in sorted(grouped)
    )
    blocks = []
    for letter in sorted(grouped):
        rows = []
        for term in grouped[letter]:
            target = lesson_for_term(term)
            title = titles[target]
            rows.append(
                f'<article class="term" id="{e(term["anchor"])}">'
                f'<h2>{e(term["term"])}</h2>'
                f'<p>{e(term["one_liner"])}</p>'
                f'<p><a href="#/lesson/{target}">Lesson: {e(title)}</a></p>'
                f"</article>"
            )
        blocks.append(f'<h2 id="letter-{letter}">{letter}</h2>' + "".join(rows))
    return (
        "<h1>Glossary</h1>"
        "<p>Each line is a plain definition. The link under it is the lesson that uses the idea.</p>"
        f'<nav class="letters" aria-label="Letters">{letters}</nav>'
        + "".join(blocks)
    )


def tools_html() -> str:
    return """
<h1>Tools</h1>
<p>These three calculators use the numbers you type. They do not send orders and they do not read a live price. Educational content only, not financial advice.</p>
<h2 id="tool-size">Position size</h2>
<p>Cash at risk divided by the distance from entry to stop. This belongs to the position sizing lesson.</p>
<p><a href="#/lesson/position-size">Lesson: Position sizing</a></p>
<form class="calc" data-calc="size">
<div class="fields">
<label>Mode <select name="mode"><option value="spot">Spot</option><option value="futures">Futures</option></select></label>
<label>Account <input name="account" type="number" min="0" step="1" value="10000"></label>
<label>Risk percent <input name="riskPct" type="number" min="0" step="0.1" value="1"></label>
<label>Entry <input name="entry" type="number" min="0" step="any" value="100"></label>
<label>Stop <input name="stop" type="number" min="0" step="any" value="95"></label>
<label>Fee, basis points <input name="feeBps" type="number" min="0" step="1" value="10"></label>
<label>Slippage, basis points <input name="slipBps" type="number" min="0" step="1" value="5"></label>
<label>Leverage cap <input name="leverage" type="number" min="0" step="0.1" value="2"></label>
</div>
<div class="results">
<div><span>Quantity</span><strong data-out="qty"></strong></div>
<div><span>Notional</span><strong data-out="notional"></strong></div>
<div><span>Cash at risk</span><strong data-out="cash"></strong></div>
<div><span>Stop distance</span><strong data-out="distance"></strong></div>
<div><span>Fee and slippage</span><strong data-out="friction"></strong></div>
<div><span>Loss if stopped</span><strong data-out="loss"></strong></div>
<div><span>Implied multiple</span><strong data-out="implied"></strong></div>
</div>
<p class="note" data-note></p>
</form>
<h2 id="tool-liq">Liquidation price</h2>
<p>A teaching model for an isolated position. Long result is entry times (1 minus 1 divided by leverage, plus the maintenance rate). Short result flips the middle sign. A live venue can use a harsher schedule.</p>
<p><a href="#/lesson/liquidation">Lesson: Liquidation</a></p>
<form class="calc" data-calc="liq">
<div class="fields">
<label>Side <select name="side"><option value="long">Long</option><option value="short">Short</option></select></label>
<label>Entry <input name="entry" type="number" min="0" step="any" value="100"></label>
<label>Leverage <input name="leverage" type="number" min="1" step="0.1" value="10"></label>
<label>Maintenance rate, percent <input name="mmr" type="number" min="0" step="0.1" value="0.5"></label>
</div>
<div class="results"><div><span>Example liquidation</span><strong data-out="liq"></strong></div></div>
<p class="note" data-note></p>
</form>
<h2 id="tool-grid">Grid profit per gap</h2>
<p>Arithmetic step is the box width divided by the number of gaps. The round-trip fee is estimated at the midpoint. If the step is smaller than that fee, the gap does not pay for itself in this model.</p>
<p><a href="#/lesson/grid-range">Lesson: Range and grid count</a></p>
<form class="calc" data-calc="grid">
<div class="fields">
<label>Lower price <input name="lower" type="number" min="0" step="any" value="90"></label>
<label>Upper price <input name="upper" type="number" min="0" step="any" value="110"></label>
<label>Gaps <input name="gaps" type="number" min="1" step="1" value="10"></label>
<label>Fee, basis points each side <input name="feeBps" type="number" min="0" step="1" value="10"></label>
</div>
<div class="results">
<div><span>Step</span><strong data-out="step"></strong></div>
<div><span>Round-trip fee at mid</span><strong data-out="fee"></strong></div>
<div><span>Step after that fee</span><strong data-out="net"></strong></div>
</div>
<p class="note" data-note></p>
</form>
"""


CSS = """
:root {
  --bg: #071422;
  --panel: #10283a;
  --text: #e8f4fc;
  --muted: #c5d7e6;
  --line: #3d6484;
  --cyan: #8fe7ff;
  --teach: #b6f3d4;
  --amber: #ffe7a3;
  --ink: #1a1204;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: Segoe UI, Helvetica, Arial, sans-serif;
  font-size: 1.05rem;
  line-height: 1.6;
}
a { color: var(--cyan); }
:focus-visible { outline: 3px solid var(--amber); outline-offset: 3px; }
.skip {
  position: absolute; left: 0; top: 0; width: 1px; height: 1px; overflow: hidden;
  background: var(--amber); color: var(--ink); font-weight: 700;
}
.skip:focus { width: auto; height: auto; padding: 0.6rem 0.8rem; z-index: 5; }
header {
  position: sticky; top: 0; background: #071422; border-bottom: 1px solid var(--line); z-index: 2;
}
.bar { display: flex; flex-wrap: wrap; gap: 0.4rem 0.8rem; align-items: center; padding: 0.7rem 1rem; }
.brand { color: var(--text); text-decoration: none; font-weight: 750; margin-right: 0.4rem; }
.bar nav { display: flex; flex-wrap: wrap; gap: 0.35rem 0.7rem; }
.bar a { text-decoration: none; }
.bar a[aria-current="page"] { color: var(--teach); }
.layout { display: grid; grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr)); }
main { padding: 1.1rem 1.1rem 3rem; max-width: 52rem; }
.learn, p, li { max-width: 68ch; }
.learn { background: #10283a; border-left: 4px solid var(--teach); padding: 0.75rem 0.9rem; }
h1 { font-size: clamp(2rem, 4vw, 3rem); line-height: 1.1; margin: 0.4rem 0 0.8rem; max-width: 20ch; }
h2 { font-size: 1.4rem; margin: 1.4rem 0 0.4rem; }
.crumb { color: var(--muted); margin-bottom: 0.2rem; }
figure { margin: 1rem 0; max-width: 100%; }
figure svg, figure img { width: 100%; height: auto; display: block; border-radius: 12px; }
figcaption { color: var(--muted); margin-top: 0.4rem; }
ol.index { list-style: none; padding: 0; }
ol.index a, .index a { display: flex; flex-direction: column; padding: 0.7rem 0; border-bottom: 1px solid var(--line); text-decoration: none; color: var(--text); }
ol.index strong { color: var(--cyan); font-size: 1.15rem; }
.fields { display: grid; grid-template-columns: repeat(auto-fit, minmax(11rem, 1fr)); gap: 0.7rem; }
label { display: flex; flex-direction: column; gap: 0.25rem; font-weight: 650; }
input, select {
  font: inherit; color: var(--text); background: #0c1c2a; border: 1px solid var(--line);
  border-radius: 10px; min-height: 44px; padding: 0.4rem 0.6rem;
}
.results { display: grid; grid-template-columns: repeat(auto-fit, minmax(9rem, 1fr)); gap: 0.6rem; margin: 0.8rem 0; }
.results div { background: var(--panel); border: 1px solid var(--line); border-radius: 10px; padding: 0.55rem 0.7rem; }
.results span { display: block; color: var(--muted); font-size: 0.9rem; }
.results strong { font-variant-numeric: tabular-nums; }
.note { color: var(--amber); }
.next { border-top: 1px solid var(--line); padding-top: 0.8rem; font-size: 1.15rem; }
.term { border-top: 1px solid var(--line); padding: 0.75rem 0; }
.term h2 { font-size: 1.2rem; margin: 0; }
.letters { display: flex; flex-wrap: wrap; gap: 0.35rem; }
.letters a { min-width: 2.2rem; min-height: 2.4rem; display: inline-flex; align-items: center; justify-content: center; border: 1px solid var(--line); border-radius: 8px; text-decoration: none; color: var(--text); }
footer { border-top: 1px solid var(--line); padding: 1rem; color: var(--muted); }
"""

JS = r"""
(function () {
  var views = window.ATLAS_VIEWS;
  var main = document.getElementById("main");
  function num(v) { var n = Number(v); return isFinite(n) ? n : NaN; }
  function money(n) { return n.toLocaleString(undefined, { maximumFractionDigits: 2 }); }
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
    var warning = "";
    if (input.mode === "spot" && implied > 1.001) warning = "The notional is larger than the account. On spot, that means the position needs more cash than the account figure, or the stop is very close.";
    if (input.mode === "futures" && isFinite(leverage) && leverage > 0 && implied > leverage + 0.001) warning = "The size implies about " + implied.toFixed(2) + " times, above the leverage cap you entered.";
    return { qty: qty, notional: notional, riskCash: riskCash, distancePct: distance / entry * 100, friction: friction, lossAtStop: riskCash + friction, impliedLeverage: implied, warning: warning };
  }
  function liquidation(input) {
    var entry = num(input.entry), leverage = num(input.leverage), mmr = num(input.mmr);
    if (!(entry > 0) || !(leverage > 1) || !(mmr >= 0)) return { error: "Enter an entry, leverage above 1, and a maintenance rate." };
    var m = mmr / 100;
    var price = input.side === "short"
      ? entry * (1 + 1 / leverage - m)
      : entry * (1 - 1 / leverage + m);
    if (!(price > 0)) return { error: "This example model produced a price at or below zero. Raise the maintenance rate or lower the leverage." };
    return { price: price };
  }
  function gridStep(input) {
    var lower = num(input.lower), upper = num(input.upper), gaps = num(input.gaps), feeBps = num(input.feeBps);
    if (!(lower > 0) || !(upper > lower) || !(gaps >= 1)) return { error: "Enter a lower price, a higher upper price, and at least one gap." };
    if (!isFinite(feeBps) || feeBps < 0) feeBps = 0;
    gaps = Math.round(gaps);
    var step = (upper - lower) / gaps;
    var mid = (upper + lower) / 2;
    var fee = mid * 2 * (feeBps / 10000);
    return { step: step, fee: fee, net: step - fee };
  }
  function readForm(form) {
    var data = {};
    Array.prototype.forEach.call(form.elements, function (el) {
      if (el.name) data[el.name] = el.value;
    });
    return data;
  }
  function bind(root) {
    root.querySelectorAll("form.calc").forEach(function (form) {
      var run = function () {
        var note = form.querySelector("[data-note]");
        var data = readForm(form);
        var kind = form.getAttribute("data-calc");
        if (kind === "size") {
          var result = sizePosition(data);
          if (result.error) { note.textContent = result.error; return; }
          form.querySelector('[data-out="qty"]').textContent = result.qty.toLocaleString(undefined, { maximumFractionDigits: 6 });
          form.querySelector('[data-out="notional"]').textContent = money(result.notional);
          form.querySelector('[data-out="cash"]').textContent = money(result.riskCash);
          form.querySelector('[data-out="distance"]').textContent = result.distancePct.toFixed(2) + "%";
          form.querySelector('[data-out="friction"]').textContent = money(result.friction);
          form.querySelector('[data-out="loss"]').textContent = money(result.lossAtStop);
          form.querySelector('[data-out="implied"]').textContent = result.impliedLeverage.toFixed(2) + " times";
          note.textContent = "Example only. Fees and slippage are counted on the way in and the way out. This is not an order." + (result.warning ? " " + result.warning : "");
        } else if (kind === "liq") {
          var liq = liquidation(data);
          if (liq.error) { note.textContent = liq.error; return; }
          form.querySelector('[data-out="liq"]').textContent = liq.price.toFixed(4);
          note.textContent = "Example model for an isolated position. It is not a venue schedule.";
        } else {
          var grid = gridStep(data);
          if (grid.error) { note.textContent = grid.error; return; }
          form.querySelector('[data-out="step"]').textContent = grid.step.toFixed(4);
          form.querySelector('[data-out="fee"]').textContent = grid.fee.toFixed(4);
          form.querySelector('[data-out="net"]').textContent = grid.net.toFixed(4);
          note.textContent = grid.net <= 0
            ? "Example only. The step is smaller than the round-trip fee at the midpoint, so this gap does not pay for itself in the model."
            : "Example only. The step is larger than the round-trip fee at the midpoint. Spread and slippage are not in the fee box.";
        }
      };
      form.addEventListener("input", run);
      run();
    });
  }
  var booted = false;
  function render() {
    var raw = location.hash.replace(/^#/, "");
    if (!raw || raw === "/") raw = "/start";
    if (raw.charAt(0) === "/") raw = raw.slice(1);
    var parts = raw.split("/").filter(Boolean);
    var key = parts.join("/");
    var anchor = "";
    if (!views[key] && parts.length > 1) {
      key = parts.slice(0, -1).join("/");
      anchor = parts[parts.length - 1];
    }
    if (!views[key]) key = "start";
    main.innerHTML = views[key];
    document.title = (main.querySelector("h1") ? main.querySelector("h1").textContent : "Atlas") + " - Atlas";
    bind(main);
    document.querySelectorAll(".bar a").forEach(function (link) {
      var href = (link.getAttribute("href") || "").replace("#/", "");
      if (href === key || (href && key.indexOf(href + "/") === 0)) link.setAttribute("aria-current", "page");
      else link.removeAttribute("aria-current");
    });
    var target = anchor && document.getElementById(anchor);
    if (booted) {
      var focusNode = target || main.querySelector("h1");
      if (focusNode) {
        if (!focusNode.hasAttribute("tabindex")) focusNode.setAttribute("tabindex", "-1");
        focusNode.focus();
      }
    }
    if (target) target.scrollIntoView();
    else if (booted) window.scrollTo(0, 0);
    booted = true;
  }
  window.addEventListener("hashchange", render);
  render();
  window.atlasSelfTest = function () {
    var failures = [];
    var a = sizePosition({ account: 10000, riskPct: 1, entry: 100, stop: 95, feeBps: 10, slipBps: 5, leverage: 2, mode: "spot" });
    if (Math.abs(a.qty - 20) > 1e-9) failures.push("qty");
    if (Math.abs(a.riskCash - 100) > 1e-9) failures.push("cash");
    if (Math.abs(a.friction - 6) > 1e-6) failures.push("friction");
    var b = liquidation({ entry: 100, leverage: 10, mmr: 0.5, side: "long" });
    if (Math.abs(b.price - 90.5) > 1e-9) failures.push("liq");
    var c = gridStep({ lower: 90, upper: 110, gaps: 10, feeBps: 10 });
    if (Math.abs(c.step - 2) > 1e-9) failures.push("step");
    return { ok: failures.length === 0, failures: failures };
  };
})();
"""


def markdown() -> str:
    index = lesson_index()
    titles = {lesson["id"]: lesson["title"] for _, _, lesson in flat_lessons()}
    lines = [
        "# Atlas",
        "",
        "Atlas is a directory for learning how markets work, how to read structure, how grid bots behave, and how leverage and later contracts change the risk.",
        "",
        "Educational content only, not financial advice.",
        "",
        "If you are new, read Start here from the top. Each lesson says what you will learn, shows a labelled picture, walks through made-up numbers, and names the next lesson. The glossary is one plain line per word. The tools redo the arithmetic when you change a number.",
        "",
        "## Start here",
        "",
        "Follow the beginner lessons in order. Then open Intermediate.",
        "",
    ]
    number = 1
    for level, module, lesson in flat_lessons():
        if level["id"] != "beginner":
            continue
        lines.append(f"{number}. {lesson['title']} ({module['title']}). {lesson['learn'].rstrip('.')}.")
        number += 1
    lines.append("")
    for level in LEVELS:
        lines.append(f"## {level['title']}")
        lines.append("")
        lines.append(level["blurb"])
        lines.append("")
        for module in level["modules"]:
            lines.append(f"### {module['title']}")
            lines.append("")
            lines.append(module["blurb"])
            lines.append("")
            flat = flat_lessons()
            ids = [item[2]["id"] for item in flat]
            for lesson in module["lessons"]:
                nxt = None
                position = ids.index(lesson["id"])
                if position + 1 < len(ids):
                    nxt = titles[ids[position + 1]]
                lines.append(f"#### {lesson['title']}")
                lines.append("")
                lines.append(f"What you'll learn: {lesson['learn']}")
                lines.append("")
                for paragraph in lesson["paragraphs"]:
                    lines.append(paragraph)
                    lines.append("")
                lines.append("Example.")
                lines.append("")
                for line in lesson["example"]:
                    lines.append(f"- {line}")
                lines.append("")
                for image in lesson["images"]:
                    meta = DIAGRAMS[image]
                    lines.append(f"Picture `{image}`. {meta['alt']}")
                    lines.append("")
                lines.append("Recap.")
                lines.append("")
                for line in lesson["recap"]:
                    lines.append(f"- {line}")
                lines.append("")
                if nxt:
                    lines.append(f"Next lesson: {nxt}.")
                else:
                    lines.append("Next: Glossary.")
                lines.append("")
    lines.append("## Tools")
    lines.append("")
    lines.append("Position size. Cash at risk divided by the distance from entry to stop. Lesson: Position sizing.")
    lines.append("")
    lines.append("Liquidation price. A teaching model. Long result is entry times (1 minus 1 divided by leverage, plus the maintenance rate). Short result flips the middle sign. Lesson: Liquidation.")
    lines.append("")
    lines.append("Grid profit per gap. Box width divided by the number of gaps, compared with a round-trip fee at the midpoint. Lesson: Range and grid count.")
    lines.append("")
    lines.append("## Glossary")
    lines.append("")
    lines.append("One plain line for each word, then the lesson that uses it.")
    lines.append("")
    terms = json.loads(GLOSSARY_PATH.read_text(encoding="utf-8"))
    current = ""
    for term in sorted(terms, key=lambda item: item["term"].lower()):
        letter = term["term"][0].upper()
        if letter != current:
            current = letter
            lines.append(f"### {letter}")
            lines.append("")
        target = titles[lesson_for_term(term)]
        lines.append(f"**{term['term']}.** {term['one_liner']} Lesson: {target}.")
        lines.append("")
    return "\n".join(lines)


def manifest_rows():
    titles = {lesson["id"]: lesson["title"] for _, _, lesson in flat_lessons()}
    module_of = {}
    level_of = {}
    for level, module, lesson in flat_lessons():
        module_of[lesson["id"]] = module["title"]
        level_of[lesson["id"]] = level["title"]
    rows = []
    for file_name, meta in DIAGRAMS.items():
        lesson_id = meta["lesson"]
        if lesson_id == "start":
            level_name, module_name, lesson_name = "Start here", "Start here", "Start here"
        else:
            level_name = level_of[lesson_id]
            module_name = module_of[lesson_id]
            lesson_name = titles[lesson_id]
        rows.append(
            {
                "file": file_name,
                "width": meta["width"],
                "height": meta["height"],
                "level": level_name,
                "module": module_name,
                "lesson": lesson_name,
                "alt": meta["alt"],
                "prompt": meta["prompt"],
            }
        )
    return rows


def manifest_md(rows) -> str:
    lines = [
        "# Atlas image slots",
        "",
        "The delivered page draws each slot as a labelled diagram. Drop a PNG with the file name below into `dist/atlas/images/` and run `python3 dist/atlas/build_atlas.py` to inline that PNG instead.",
        "",
        "Style for a later illustration: navy background, cyan lines, pale labels, an amber EXAMPLE badge when numbers appear, 2 to 5 labels, one idea, no people, no faces, no logos, no exchange names.",
        "",
    ]
    for row in rows:
        lines.append(f"## {row['file']}")
        lines.append("")
        lines.append(f"- Size: {row['width']}x{row['height']}")
        lines.append(f"- Level: {row['level']}")
        lines.append(f"- Module: {row['module']}")
        lines.append(f"- Lesson: {row['lesson']}")
        lines.append(f"- Alt text: {row['alt']}")
        lines.append(f"- Prompt: {row['prompt']}")
        lines.append("")
    return "\n".join(lines)


def check(paths: list[Path]) -> None:
    banned = [
        chr(64),
        "a" + "bn",
        "p" + "ty",
        "market " + "pros",
        "cr" + "own",
        "ky" + "le",
        "ste" + "wart",
    ]
    phrases = [
        "kind " + "regards",
        "best " + "regards",
        "yours " + "sinc" + "erely",
        "sinc" + "erely",
        "sign-" + "off",
    ]
    for path in paths:
        text = path.read_text(encoding="utf-8").lower()
        for token in banned + phrases:
            if token in text:
                raise SystemExit(f"Banned string {token!r} in {path}")


def main() -> None:
    index = lesson_index()
    missing = []
    for _, _, lesson in flat_lessons():
        for image in lesson["images"]:
            if image not in DIAGRAMS:
                missing.append(image)
            elif DIAGRAMS[image]["lesson"] != lesson["id"]:
                raise SystemExit(f"{image} is filed under {DIAGRAMS[image]['lesson']} but used by {lesson['id']}")
    if "atlas-start-01.png" not in DIAGRAMS:
        missing.append("atlas-start-01.png")
    if missing:
        raise SystemExit("Missing diagrams: " + ", ".join(missing))
    terms = json.loads(GLOSSARY_PATH.read_text(encoding="utf-8"))
    if len(terms) != 435:
        raise SystemExit(f"Expected 435 glossary terms, found {len(terms)}")
    titles = {lesson["id"]: lesson["title"] for _, _, lesson in flat_lessons()}
    for term in terms:
        target = lesson_for_term(term)
        if target not in titles:
            raise SystemExit(f"No lesson for {term['term']} -> {target}")

    flat = [lesson for _, _, lesson in flat_lessons()]
    views = {"start": start_html([lesson for level, _, lesson in flat_lessons() if level["id"] == "beginner"])}
    for level in LEVELS:
        views[f"level/{level['id']}"] = level_html(level)
        for module in level["modules"]:
            views[f"module/{module['id']}"] = module_html(level, module)
    for position, lesson in enumerate(flat):
        level, module, _ = index[lesson["id"]]
        nxt = flat[position + 1] if position + 1 < len(flat) else None
        views[f"lesson/{lesson['id']}"] = lesson_html(level, module, lesson, nxt)
    views["glossary"] = glossary_html(sorted(terms, key=lambda item: item["term"].lower()), titles)
    views["tools"] = tools_html()

    payload = json.dumps(views, ensure_ascii=True, separators=(",", ":")).replace("<", "\\u003c")
    nav = [
        '<a class="brand" href="#/start">Atlas</a>',
        '<nav aria-label="Levels">',
        '<a href="#/start">Start here</a>',
    ]
    for level in LEVELS:
        nav.append(f'<a href="#/level/{level["id"]}">{e(level["title"])}</a>')
    nav.append('<a href="#/glossary">Glossary</a><a href="#/tools">Tools</a></nav>')
    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Atlas</title>
<meta name="description" content="A trading directory from first principles through grid bots, leverage, futures, options, and a written system.">
<style>
{CSS}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header><div class="bar">{''.join(nav)}</div></header>
<main id="main"></main>
<footer><p>Educational content only, not financial advice.</p></footer>
<script>window.ATLAS_VIEWS = {payload};</script>
<script>
{JS}
</script>
</body>
</html>
"""
    rows = manifest_rows()
    OUT_JSON.write_text(json.dumps(rows, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    OUT_MAN_MD.write_text(manifest_md(rows), encoding="utf-8")
    OUT_MD.write_text(markdown(), encoding="utf-8")
    OUT_HTML.write_text(document, encoding="utf-8")
    check([OUT_HTML, OUT_MD, OUT_JSON, OUT_MAN_MD, Path(__file__), HERE / "lib_lessons.py", HERE / "lib_diagrams.py"])
    lesson_count = len(flat)
    print(f"levels {len(LEVELS)}")
    print(f"modules {sum(len(level['modules']) for level in LEVELS)}")
    print(f"lessons {lesson_count}")
    print(f"glossary {len(terms)}")
    print(f"images {len(rows)}")
    print(f"html {OUT_HTML.stat().st_size}")
    print(f"md {OUT_MD.stat().st_size}")
    print(f"manifest {OUT_JSON.stat().st_size}")


if __name__ == "__main__":
    main()
