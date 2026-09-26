---
name: webgl-motion-graphics
description: Design and build real WebGL/Three.js scene types for the On-Chain Operator Program's lesson video renderer - floating holographic 3D nodes, glowing particle-stream bar/donut charts, and the shared engine (glow material, camera framing, ambient particles, shape/camera variety) they're built from. Use when asked for a "3D", "cinematic", "WebGL" or "holographic" treatment of a flow or chart scene, when extending `flow3d`/`chart3d`, or when a lesson's WebGL scene renders wrong (thin/invisible lines, clipped nodes, overlapping labels).
---

# WebGL Motion Graphics

`flow3d` and `chart3d` are real WebGL scene types (Three.js, rendered in headless
Chromium via SwiftShader) that sit **alongside** the flat CSS/SVG `flow` and
`chart` scenes documented in `animated-flows` — not a replacement for them.
Author a scene exactly as you would for `flow`/`chart` (same `nodes`/`edges` or
`bars`/`segs` JSON) and just change `"type"` to `"flow3d"` or `"chart3d"`. Spec:
`.claude/skills/lesson-script-writing/references/scene-reference.md`.

Read `references/README.md` before touching the engine code — it walks
through eight real screenshots (`references/screenshots/*.jpg`) and the bugs
each one caught (thin WebGL lines reading as invisible threads, camera framing
clipping a node, labels overlapping at high node counts, a title/caption
colliding with a node in portrait). Those are exactly the failure modes a new
scene type built on this engine will hit again if it skips straight to code.

## Why this exists, and its real cost

A CSS-only motion pass (kinetic word reveal, ambient drift — see
`build_video.js` git history) was a bounded, safe stopgap. This is the real
thing: a genuine 3D renderer, not a CSS trick. That means it has genuine
WebGL costs, measured on real lesson scenes, not guessed:

- **Render time:** existing flat scenes already cost ~70-90ms/frame in this
  container (2D canvas background + DOM/SVG compositing + the Playwright
  screenshot IPC round-trip). `flow3d` costs ~100-115ms/frame (~3-3.4x
  realtime); `chart3d` costs ~90-120ms/frame (~2.7-3.3x realtime, kind- and
  node-count-dependent). Both are workable for a handful of scenes per lesson
  and would meaningfully slow a render if every scene switched to them.
- **File size**, at the production encode settings (libx264, crf 19, preset
  medium, tune animation): `flow3d` runs **~1.5-2x** the flat `flow` scene's
  KB/s (the wireframe facets + fresnel glow halo don't compress as well as
  flat color fields) — negligible for one or two scenes inside a lesson's
  ~95MB cap, but re-check final file size if used more broadly. `chart3d` is
  actually **smaller** than the flat `chart` scene (~0.7-0.8x) — mostly
  smooth-shaded solid geometry against near-black compresses efficiently.
- **What's expensive and must be avoided:** `MeshPhysicalMaterial`'s
  `transmission` (real-time glass refraction) measured **5x** slower than a
  transmission-free material in isolation (367ms/frame vs. 71ms/frame at
  1920×1080) — a full off-screen render-target pass per transmissive object,
  per frame. Never turn it on for a per-frame-rendered scene like this one.
  Antialiasing costs a real but survivable ~15-20ms/frame; both engines leave
  it off and rely on JPEG/h264's own softening plus the fresnel glow shell.

Before adding a third engine or a shader background, read "What's left"
below — the render-time and file-size ceiling is closer than it looks once
several WebGL scenes land in the same lesson.

## The shared engine (`export/webgl/`)

- **`lib/core.js`** — deterministic RNG (`lcg`), easing (`ease`/`easeIO`),
  the brand tone palette (`toneColor`), a shared glow sprite texture
  (`glowTexture`, built once and reused, not once per sprite), the
  fresnel/rim-glow material (`rimGlowMaterial`, `holoMesh`), the ambient
  depth-particle field (`ambientParticles`), bbox-derived camera framing
  (`frameFromPoints`), the three camera choreographies (`moveCamera`,
  `pickCameraMove`), the node-shape variants (`makeNodeGeometry`,
  `pickNodeShape`), and the counting-number formatter (`formatCounter`).
  Every new WebGL scene type should import from here, not reimplement it.
- **`flow3d.js`** — the 3D flow engine (nodes, edges, travelling signal).
- **`chart3d.js`** — the 3D chart engine (`runBars`, `runDonut`).
- **`build_webgl_engine.js`** (in `export/`) — bundles each engine (esbuild,
  IIFE) into `.render/webgl-<name>.bundle.js`, loaded by a classic
  `<script src="file://...">` tag. Rebuilt automatically the first time a
  video actually uses that engine, and re-bundled whenever anything under
  `webgl/` is newer than the cached bundle — you never run this by hand.

**Why bundle at all:** three.js has shipped ESM-only (no browser global
build) since r150, and Chromium refuses to resolve `<script type="module">`
imports over `file://` ("Cross origin requests are only supported for
protocol schemes: chrome, chrome-extension, ... http, https, ..." — `file:`
isn't in that list). A classic script tag doesn't hit that check.

**Why HTML labels, not WebGL text:** every label (node name, bar value,
donut legend) is a plain absolutely-positioned `<div>`, projected onto the
node's current 3D position each frame via `project()` — not text rendered
inside the WebGL canvas. Text-in-WebGL is blurrier, more expensive, and
harder to keep crisp after JPEG/h264 compression than the browser's own text
renderer. This is why every scene's HTML also needs the `#gl3d-mount` div
`sceneBody()` creates and the tiny `window.__hooks` extension point in
`scenePage()`'s shared script (`(window.__hooks || []).forEach(fn => fn(t))`
at the end of `window.setTime`) — each WebGL engine pushes its per-frame
update there instead of owning `window.setTime` itself, so the shared
caption/progress-bar/chip/kinetic-title chrome keeps working untouched.

## Give every lesson a distinct cinematic treatment

Per direction from this skill's own build: a lesson's WebGL scenes should not
read as the same shot copy-pasted from the last lesson. Both engines pick a
**node shape** (`icosahedron` / `octahedron` / `dodecahedron`) and a **camera
move** (`sway` — gentle side-to-side drift; `rise` — a slow vertical reveal;
`push` — a documentary push-in) automatically from the scene's `seed` field,
via a real hash (`mixSeed` in `lib/core.js` — a plain modulo or bit-shift
collapses this codebase's small seed values like 1-30 onto the same variant,
which is why one exists). Different lessons using different seeds get
different treatments for free; a lesson author never has to think about it.

Override explicitly when a specific look matters more than variety: set
`shape: "octahedron"` or `cameraMove: "push"` directly on a `flow3d` scene
(chart3d takes `cameraMove` only — its bars/donut don't have a swappable node
shape). Don't hand-pick a shape/move for every scene "for variety" — that's
what the seed-based defaults already do; only override when the flat
default genuinely doesn't fit (e.g. a `push` move for a scene about
narrowing down to one conclusion).

## When to reach for flow3d / chart3d, and when not to

- **Good fit:** a mechanism you want to visually anchor a lesson around — a
  handful of scenes per lesson (one, maybe two), not a wholesale swap of
  every `flow`/`chart` scene. Node counts of 2-6 for `flow3d`; any segment
  count for `chart3d`'s donut, though the legend gets tight past ~6.
- **Stay flat (`flow`/`chart`) when:**
  - A flow needs **7+ nodes** — `flow3d`'s labels start crowding even with
    the wrap fix (see `flow3d-7node-wide.jpg`); the flat scene has more label
    room because it isn't fighting 3D perspective placement too.
  - The chart is a **`line`** kind (trend over time, gas price, price
    charts) — `chart3d` doesn't implement it yet.
  - The lesson is portrait and the title runs long — re-check a real render;
    the portrait framing margin (`marginY: H > W ? 6.4 : 4.6` in
    `flow3d.js`) was tuned against one real 3-line title, not proven for
    every case.
  - You're not confident the render-time/file-size budget above still holds
    for this lesson's total scene count — measure, don't assume.

## Extending this system

Adding a third engine (or a shader ambient background — see "What's left"):
build it the same way `chart3d.js` was built on top of what `flow3d.js`
already had:
1. Import shared pieces from `lib/core.js` first; only write new lib code
   for something genuinely new (and put it in `lib/core.js`, not duplicated
   per-engine).
2. Register it in `build_webgl_engine.js`'s `ENTRIES` map.
3. Add a `case '<name>':` to `sceneBody()` (build the data payload + mount
   div + `<script>` tags) and to `planTimes()` (reuse the flat scene's timing
   case if the JSON shape matches — `case 'flow': case '<name>':` etc.).
4. Test with the same methodology used to build this skill: render a real
   gold lesson scene (not synthetic data) through the unmodified
   `sceneBody()`/`scenePage()`/`planTimes()` code path, screenshot several
   timepoints (early reveal, mid, fully-settled), and encode a real clip at
   production ffmpeg settings to measure the actual KB/s delta. A bench
   harness pattern for this (copy `build_video.js`, add
   `module.exports = {...}` before its `require.main === module` guard so
   its internals are callable without triggering the full render pipeline)
   isn't checked into the repo — it's disposable scaffolding, not a shipped
   test suite.
5. Update `references/README.md` with what the new screenshots caught.
6. Document the new scene type in `export/VIDEO_PRODUCTION_TEAM_PROMPT.md`
   the same way `flow3d` is documented there.

## What's left before any of this is a default

- `chart3d`'s `line` kind doesn't exist.
- No shader-based full-screen ambient background exists — both engines use
  a particle field (`ambientParticles`), not a fragment-shader backdrop.
  Prototype and measure it the same way this skill's own build measured
  everything else before adding it.
- The `flow3d`/`chart3d` visual "language" (glass + wireframe + fresnel
  glow) hasn't been extended to any other flat scene type (`pillars`,
  `compare`, `stats`, `steps`) — those all still render as flat CSS cards.
  If asked to do that, treat each as its own prototype-and-measure pass, not
  a mechanical reskin.
- Neither engine has been validated against a real Kokoro-narrated render
  end to end (this skill's own build used fabricated sentence timings — no
  TTS model was available in that session) — the timing *mechanism*
  (`T.items`/`T.edges`, shared with the flat scenes) is unchanged and
  already production-proven, but do one real narrated render before treating
  this as fully closed out.
