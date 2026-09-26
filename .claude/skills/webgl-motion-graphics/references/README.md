# Reference imagery

Real screenshots from our own `flow3d`/`chart3d` renders — not third-party
scraped design assets. This container's network policy blocks direct browser
access to design-inspiration sites (Dribbble, Awwwards, CodePen, threejs.org
all refused the CONNECT); `WebSearch`/`WebFetch` still work (they're
server-side, not subject to this container's egress policy) and were used to
research technique names and trade-offs (fresnel/rim-glow shells instead of a
bloom pass, particle-morph chart treatments) — see the citations in the
skill's `SKILL.md`. The actual images below are what a viewer will really see
on screen, generated the same way a production render would, which is more
useful as a reference than a mood board of someone else's unrelated work.

Every shot below came from a real gold lesson script (nodes/edges/bars/segs
unmodified, only `type` flipped to the 3D variant) rendered through the
unmodified `sceneBody()`/`scenePage()` code path, at a late timepoint so
everything is fully revealed. Several of these renders caught real bugs before
they shipped — noted below, not scrubbed from the record, because the next
scene type built on this engine will hit the same class of issue if it
doesn't know to check for it.

## flow3d

- **flow3d-3node-row.jpg** — 3-node row layout, no tone overrides (lesson
  00-1, "A trade, the bank way"). The baseline case: clean facets, one edge
  token in flight, labels sitting clear below each node.
- **flow3d-7node-wide.jpg** — 7-node row layout (lesson 01-2, "Create to
  finality, seven stops"). Stress test for node count. **Caught and fixed:**
  at this density, fixed-width `nowrap` labels overlapped their neighbors
  illegibly; labels now wrap within a width tied to `nw` (which itself
  shrinks as flowLayout packs more nodes into the same stage). Still tight —
  recommend the flat `flow` scene instead of `flow3d` past ~6 nodes; it has
  more label room to work with (see "When not to use flow3d" in SKILL.md).
- **flow3d-cycle-6node.jpg** — 6-node `cycle` layout (lesson 00-0, "Module 0,
  recapped as one loop"). **Caught and fixed:** camera framing computed from
  the node bounding box alone left no slack for the camera's sway motion or a
  node's per-node z-jitter, and the rightmost node's label clipped off the
  right edge. Fixed by widening `frameFromPoints`' margins in `lib/core.js`
  and shrinking the z-jitter amplitude.
- **flow3d-failure-tone.jpg** — a 4-node failure-path flow with `tone: "bad"`
  on the first node (lesson 01-2, "One stuck nonce, three transactions
  waiting"). Shows the amber/orange vs. blue tone contrast and the active-node
  highlight (brighter emissive + glow) together.
- **flow3d-portrait.jpg** — 3-node `column` layout at 1080×1920 (lesson 01-0,
  "A 2-of-3 multisig"). **Caught and fixed twice:** the title overlapped the
  first node, and the last node's label sat under the caption strip. Both are
  the same root cause — flowLayout() reserves specific pixel margins (top for
  the title, bottom for the caption) in its 2D coordinate space, and fitting
  the 3D camera tightly to the node bounding box undoes that reserve. Fixed by
  giving portrait layouts extra vertical framing margin in `lib/core.js`
  (`marginY: H > W ? 6.4 : 4.6`). If a portrait scene's title still runs to 3
  lines, check a real render before shipping — this margin was tuned against
  one real case, not proven for every title length.

## chart3d

- **chart3d-bars.jpg** — 4-bar cost breakdown, one `tone: "bad"` total
  (lesson 00-0, "Where your $100 goes"). **First version caught and fixed:**
  bars were originally drawn as thin `THREE.Line` beams, which most browsers
  clamp to 1px regardless of the `linewidth` material property — it read as
  "a dot floating on a thread," not a bar chart. Rebuilt as solid emissive
  cylinders (`CylinderGeometry` scaled on Y, geometry pre-translated so it
  grows from its base) with a fatter additive "aura" cylinder around it. The
  same fix applies to any future beam/bar-shaped WebGL element — reach for a
  thin mesh, never a thin line, if it needs to read as having width.
- **chart3d-donut.jpg** — 3-segment donut with a center total (lesson 00-0,
  "An example $100 learning budget"). Same thin-line problem existed here
  too (a bare colored circle, barely visible) — fixed with a `TubeGeometry`
  arc rebuilt each frame from the currently-revealed fraction.
- **chart3d-donut-alt.jpg** — 6-segment donut, all warm/attack tones (lesson
  01-6, "Roughly how these attacks break down"). Stress test for segment
  count and same-family colors; legend remains legible even when adjacent
  slice colors are close.

## What isn't pictured

- `chart3d`'s `line` kind (trend lines, gas-price-over-time charts) doesn't
  exist yet — `chart3d` only implements `bars` and `donut`. A lesson scene
  with `kind: "line"` must stay on the flat `chart` scene.
- A shader-based full-screen ambient background (as opposed to the depth
  particle field both engines already have) hasn't been built. See
  "What's left" in `SKILL.md`.
