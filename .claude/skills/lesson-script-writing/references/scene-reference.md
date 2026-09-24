# Scene reference (build_video.js)

Every video is a JSON file in `programs/defi-program/video-scripts/` (lessons) or an
entry in `export/videos.js` (VSLs, welcome, module intros).

## Video fields

| Field | Meaning |
|---|---|
| `id` | File name of the output, e.g. `lesson-03-2` → `video/lesson-03-2.mp4` |
| `title` | "Lesson 3.2: LTV, liquidation threshold & health factor" |
| `size` | `[1920, 1080]` (landscape) or `[1080, 1920]` (vertical) |
| `group` | `"lessons"` for lesson videos |
| `tag` | Chip text top-left, e.g. `"Lesson 3.2"` |
| `maxMinutes` | Hard cap, default 25; render fails above it |
| `gold` | `true` for hand-finished scripts |
| `use` | Where it's used, teach plan notes, "facts last checked: YYYY-MM-DD" |
| `thumbnail` | `{ "title": "Never get liquidated", "subtitle": "Lesson 3.2" }` |
| `speed` | Voice speed, default 0.96 |
| `music`, `musicLevel` | Ambient bed (marketing videos only) |
| `chrome` | `"minimal"` hides progress bar and chip |

## Fields on every scene

| Field | Meaning |
|---|---|
| `type` | One of the types below |
| `chapter` | Chapter name (drives the chip and the chapter list). Use: Intro, Why it matters, How it works, the concept names, Do it, Worked example, Quiz, Your turn, Recap |
| `vo` | What the voice says. Spell abbreviations as spoken (L.T.V., E.T.H.). `[[pause 2]]` inserts a pause in seconds |
| `cap` | On-screen caption text if it differs from `vo` (e.g. "LTV" instead of "L.T.V.") |
| `hold` | Extra seconds to hold the scene after the voice ends |
| `at` | Optional list of sentence indexes (0-based) at which each item appears, overriding automatic sync |

Items, steps, pillars, flow nodes and cutaway shots are synced automatically: each
appears at the sentence that shares the most words with it. Name the thing on screen
in the sentence that introduces it, and sync takes care of itself.

## Teacher-view scenes

**title** `eyebrow`, `num`, `title`, `sub`, optional `src` (image under the title).

**statement** `kicker`, `lines` (1 to 3 short lines; line 2+ in aqua), `sub`. Timing: `lineAt`, `subAt`.

**strike** `big` (the myth, struck through on sentence 2), `after` (the truth). Timing: `strikeAt`, `afterAt`.

**bullets** `title`, `items` (at most 6), `numbered`, `check: false` (✕ marks for don'ts), `compact`.

**pillars** `title`, `items: [{ icon, title, text }]` (3 or 4). Icons: shield swap bank sprout layers search chart cog grid lock wallet flame exit users video book check compass target umbrella vault coins bot.

**compare** `title`, `left: { label, tone, items }`, `right: { label, tone, items }`. `tone`: `bad` (orange ✕), `good` (aqua ✓), or omit.

**steps** `title`, `steps` (monospace, numbered; good for arithmetic and procedures), `result` (pops in at the end), `resultAt`.

**stats** `stats: [["$1.2B", "lost to bridge hacks"], ...]` counting up; last one orange unless `lastAccent: false`.

**quiz** `n`, `of`, `q`, `a`. The `vo` must be: the question, `[[pause 4]]`, then a sentence starting "The answer...". A thinking timer fills during the pause.

**cta** `button`, `sub`. **logo** `tagline`.

## Cutaway scenes

**image** A full-width image with a wipe reveal and a slow push-in.
```json
{ "type": "image", "eyebrow": "Health factor in practice", "src": "assets/diagrams/hf-curve.png", "wide": true,
  "callouts": [ { "x": 0.62, "y": 0.4, "text": "Liquidation", "at": 2 } ],
  "zoom": { "s": 1.5, "x": 0.62, "y": 0.4, "at": 2 } }
```

**flow** An animated mechanism: nodes appear as they're named, arrows draw into them, and a token travels along the arrow into the node being spoken about. 3 to 6 nodes.
```json
{ "type": "flow", "chapter": "How it works", "title": "What happens when you borrow",
  "layout": "row",
  "nodes": [
    { "id": "w", "label": "Your wallet", "sub": "deposits ETH", "icon": "wallet" },
    { "id": "p", "label": "Lending pool", "sub": "holds collateral", "icon": "bank" },
    { "id": "o", "label": "Price oracle", "sub": "values it every block", "icon": "chart" },
    { "id": "l", "label": "Liquidator", "sub": "sells if HF < 1", "icon": "bot", "tone": "bad" } ],
  "edges": [
    { "from": "w", "to": "p", "label": "collateral" },
    { "from": "p", "to": "o", "label": "price check" },
    { "from": "o", "to": "l", "label": "HF below 1", "tone": "bad", "dashed": true } ],
  "vo": "Start with your wallet, which deposits E.T.H. as collateral. The lending pool holds that collateral. Every block, a price oracle values it. And if your health factor drops below one, a liquidator sells it, at a penalty." }
```
- `layout`: `row` (default landscape), `column` (default vertical), `cycle` (loops, e.g. a grid bot's buy/sell cycle), or give each node `x`, `y` (0 to 1) for a custom layout.
- `edges` default to a chain in node order. `bend` (px) curves an edge; use it for return arrows in a cycle.
- `tone: "bad"` on nodes or edges for the failure path.

**cutaway** Real screenshots in a browser frame, one per step: crossfade, highlight box with the rest dimmed, push-in towards the box, "Step N" caption.
```json
{ "type": "cutaway", "chapter": "Do it", "label": "On screen: your lending position", "url": "app.example.org",
  "shots": [
    { "src": "assets/demos/lending-position/01.png", "caption": "Find your health factor", "box": [0.62, 0.18, 0.2, 0.08] },
    { "src": "assets/demos/lending-position/02.png", "caption": "Read the liquidation price", "box": [0.62, 0.3, 0.2, 0.08], "push": 1.5,
      "blur": [[0.8, 0.02, 0.18, 0.05]] } ] }
```
- `box` and `blur` are `[x, y, w, h]` as fractions of the screenshot. `capture_demo.js` writes them for you.
- `push` sets the zoom into the box (default 1.35); `zoom: { s, x, y }` overrides it.
- Screenshots should be 16:9 (the capture tool uses 1600×900).
