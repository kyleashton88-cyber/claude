// Three.js scene engine for the `flow3d` scene type: floating holographic nodes,
// glowing directional edges with a travelling signal, an ambient depth-particle
// field, and a slow narration-aware camera drift — the WebGL counterpart of the
// flat `flow` scene, driven by the exact same per-scene timing data (T.items /
// T.edges) build_video.js already computes for the CSS/SVG version.
//
// Contract with build_video.js (see sceneBody()'s `flow3d` case):
//   window.__WEBGL_SCENE = {
//     W, H,                                  // stage size in px
//     seed,                                  // deterministic RNG seed for particles/depth
//     nodes: [{ id, label, sub, tone, px, py, nw }],
//     edges: [{ from, to, label, tone }],
//     itemsT: [[a,b], ...],                   // per node, same order as nodes
//     edgesT: [[a,b], ...],                   // per edge
//   }
// This file is bundled (esbuild, IIFE) by build_webgl_engine.js and loaded with a
// plain <script src="file://...">, so it never needs ES module resolution over
// file:// (which Chromium refuses for `type="module"`). It contributes its
// per-frame update through `window.__hooks` — a tiny, additive extension point in
// scenePage()'s shared setTime() — rather than owning window.setTime itself, so
// every existing scene type (and the shared caption/progress-bar/chip chrome) is
// completely unaffected.
//
// Shared node/particle/camera/glow building blocks live in webgl/lib/core.js so
// chart3d (and any future WebGL scene) doesn't re-implement them - see that
// file's header and .claude/skills/webgl-motion-graphics/SKILL.md for the
// design rationale (why fresnel rim-glow instead of bloom or `transmission`,
// why the camera never fully orbits, why labels are HTML not WebGL text).
import * as THREE from 'three';
import { lcg, ease, easeIO, clamp, toneColor, glowTexture, holoMesh, ambientParticles, frameFromPoints, moveCamera, pickCameraMove, pickNodeShape, makeNodeGeometry, project } from './lib/core.js';

function run(DATA) {
  const { W, H } = DATA;
  const rnd = lcg(DATA.seed || 7);

  const root = document.createElement('div');
  root.style.cssText = 'position:absolute;inset:0';
  const canvas = document.createElement('canvas');
  root.appendChild(canvas);
  const labels = document.createElement('div');
  labels.style.cssText = 'position:absolute;inset:0;pointer-events:none';
  root.appendChild(labels);
  document.getElementById('gl3d-mount').appendChild(root);

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, alpha: false });
  renderer.setSize(W, H);
  renderer.setPixelRatio(1);
  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x0b1f33, 0.018);
  const camera = new THREE.PerspectiveCamera(42, W / H, 0.1, 100);

  scene.add(new THREE.AmbientLight(0x223344, 1.3));
  const key = new THREE.PointLight(0x2ee6a6, 3.2, 60); key.position.set(6, 6, 12); scene.add(key);
  const rimLight = new THREE.PointLight(0x3987e5, 2.2, 60); rimLight.position.set(-7, -4, 8); scene.add(rimLight);

  const particles = ambientParticles(scene, DATA.seed || 7);

  // --- layout: reuse the server-computed 2D stage positions (px,py from flowLayout), placed on a depth plane ---
  const aspect = H / W, PW = 24, PH = PW * aspect;
  const nodes3 = DATA.nodes.map((n, i) => {
    const x = (n.px / W - 0.5) * PW, y = -(n.py / H - 0.5) * PH;
    const z = Math.sin(i * 2.399963) * 1.3; // golden-angle spread: deterministic, no clustering
    const r = clamp((n.nw || 260) / W * 7.5, 0.62, 1.15);
    return { ...n, i, base: new THREE.Vector3(x, y, z), r, phase: rnd() * 6.28 };
  });
  const byId = Object.fromEntries(nodes3.map(n => [n.id, n]));

  // Camera framing derived from the actual node spread, so a 2-node compare and
  // a 7-node cycle both stay fully in frame (margins account for node radius +
  // labels hanging below).
  // Extra margin beyond the node radius/labels: the camera sways off-axis
  // (see moveCamera), and a node's z-jitter can put it further toward the
  // frame edge from a swayed angle than its raw x,y bbox alone suggests -
  // caught by a 6-node cycle layout clipping its rightmost node's label.
  // Portrait needs more still: flowLayout() reserves a much taller bottom
  // margin in portrait (460px vs 220px) for the caption strip, and fitting
  // the node bbox tightly to the 3D frame edge-to-edge undoes that reserve -
  // caught by a portrait column layout's last label sitting under the caption.
  const { centroid, dist: camDist } = frameFromPoints(nodes3.map(n => n.base), W, H, { marginX: 3.1, marginY: H > W ? 6.4 : 4.6 });

  const nodeGeo = makeNodeGeometry(DATA.shape || pickNodeShape(DATA.seed));
  const groups = nodes3.map(n => {
    const g = holoMesh(nodeGeo, toneColor(n.tone));
    g.scale.setScalar(n.r);
    g.position.copy(n.base);
    scene.add(g);
    return g;
  });

  // --- edges: a bright core + soft additive halo, both rebuilt from current node positions each frame ---
  const edges3 = DATA.edges.map(e => {
    const color = toneColor(e.tone);
    const core = new THREE.Line(new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(new Float32Array(6), 3)),
      new THREE.LineBasicMaterial({ color, transparent: true, opacity: 0 }));
    const halo = new THREE.Line(new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(new Float32Array(6), 3)),
      new THREE.LineBasicMaterial({ color, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false, linewidth: 3 }));
    scene.add(core, halo);
    const tok = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTexture(), color, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false }));
    tok.scale.setScalar(1.1);
    scene.add(tok);
    return { ...e, core, halo, tok, a: byId[e.from], b: byId[e.to] };
  });

  // --- HTML label overlay (crisp text; WebGL only carries the geometry/lighting) ---
  // The 3D mesh itself is the node's "icon" now, so the overlay only carries text —
  // anchored by its top-center so it hangs below the sphere instead of sitting on it.
  // `nw` already shrinks as flowLayout() packs more nodes into the same stage
  // width, so a width cap tied to it (rather than nowrap) keeps a 7-node flow's
  // labels from overlapping their neighbors - they wrap to two lines instead.
  function labelHtml(n) {
    const size = clamp((n.nw || 260) * 0.135, 26, 46), maxW = Math.max(120, (n.nw || 260) * 1.35);
    return `<div style="display:flex;flex-direction:column;align-items:center;text-align:center;gap:4px;max-width:${maxW}px;transform:translate(-50%,0)">
      <div style="font-size:${size}px;font-weight:800;line-height:1.15;text-shadow:0 2px 14px rgba(0,0,0,.85),0 0 24px rgba(0,0,0,.6)">${n.label || ''}</div>
      ${n.sub ? `<div style="font-size:${size * 0.66}px;line-height:1.25;color:rgba(255,255,255,.78);text-shadow:0 2px 10px rgba(0,0,0,.85)">${n.sub}</div>` : ''}</div>`;
  }
  const labelEls = nodes3.map(n => {
    const el = document.createElement('div');
    el.style.cssText = 'position:absolute;left:0;top:0;opacity:0;will-change:transform,opacity';
    el.innerHTML = labelHtml(n);
    labels.appendChild(el);
    return el;
  });
  const edgeLabelEls = edges3.map(e => {
    if (!e.label) return null;
    const el = document.createElement('div');
    el.style.cssText = `position:absolute;left:0;top:0;opacity:0;font-size:24px;font-weight:700;color:rgba(255,255,255,.85);
      text-shadow:0 2px 10px rgba(0,0,0,.7);white-space:nowrap;transform:translate(-50%,-50%)`;
    el.textContent = e.label;
    labels.appendChild(el);
    return el;
  });

  window.__hooks = window.__hooks || [];
  window.__hooks.push(t => {
    // Camera: a bounded, isometric-feeling sway around the whole node group's
    // centroid (never a full orbit — with nodes roughly in a line, anything wider
    // than a gentle sway pushes the end nodes out of frame) plus a small dolly-in
    // that tracks whichever node is being narrated, without re-aiming the shot.
    const activeIdx = nodes3.findIndex((_, i) => { const [a, b] = DATA.itemsT[i] || [1e9, -1]; return t >= a && t < b; });
    moveCamera(camera, centroid, camDist, t, DATA.cameraMove || pickCameraMove(DATA.seed), { activeDolly: activeIdx >= 0 ? camDist * 0.055 : 0, duration: DATA.dur });

    particles.rotation.y = t * 0.015;

    nodes3.forEach((n, i) => {
      const [a, b] = DATA.itemsT[i] || [0, 1e9];
      const inP = ease((t - a) / 0.6);
      const active = t >= a && t < b;
      const bob = Math.sin(t * 0.7 + n.phase) * 0.22;
      const g = groups[i];
      g.position.set(n.base.x, n.base.y + bob, n.base.z);
      g.scale.setScalar(n.r * (0.6 + 0.4 * inP) * (active ? 1 + 0.04 * Math.sin(t * 3) : 1));
      g.rotation.y = t * 0.25 + i; g.rotation.x = t * 0.12;
      g.userData.base.material.emissiveIntensity = active ? 0.95 : 0.5;
      g.userData.base.material.opacity = 0.4 * inP;
      g.userData.rim.material.uniforms.intensity.value = (active ? 1.2 : 0.32) * inP;

      const el = labelEls[i];
      const below = g.position.clone(); below.y -= g.scale.x * 1.45; // anchor labels under the sphere, not on top of it
      const s = project(below, camera, W, H);
      el.style.opacity = String(inP * (active || activeIdx < 0 ? 1 : 0.55));
      el.style.transform = `translate(${s.x.toFixed(1)}px, ${s.y.toFixed(1)}px) translateY(${(1 - inP) * 22}px)`;
    });

    edges3.forEach((e, k) => {
      const [a, b] = DATA.edgesT[k] || [0, 1e9];
      const p = easeIO((t - a) / 0.7);
      const A = groups[e.a.i].position, B = groups[e.b.i].position;
      const pos = new Float32Array([A.x, A.y, A.z, B.x, B.y, B.z]);
      e.core.geometry.attributes.position.array.set(pos); e.core.geometry.attributes.position.needsUpdate = true;
      e.halo.geometry.attributes.position.array.set(pos); e.halo.geometry.attributes.position.needsUpdate = true;
      e.core.material.opacity = 0.85 * p; e.halo.material.opacity = 0.35 * p;

      if (t > a + 0.4 && t < b) {
        const f = ((t - a - 0.4) / 1.3) % 1, fe = easeIO(f);
        e.tok.position.lerpVectors(groups[e.a.i].position, groups[e.b.i].position, fe);
        e.tok.material.opacity = f < 0.1 ? f * 10 : f > 0.9 ? (1 - f) * 10 : 1;
      } else e.tok.material.opacity = 0;

      const lbl = edgeLabelEls[k];
      if (lbl) {
        const mid = new THREE.Vector3().lerpVectors(groups[e.a.i].position, groups[e.b.i].position, 0.5);
        const s = project(mid, camera, W, H);
        lbl.style.opacity = String(ease((t - a - 0.4) / 0.5));
        lbl.style.transform = `translate(${s.x.toFixed(1)}px, ${s.y.toFixed(1)}px)`;
      }
    });

    renderer.render(scene, camera);
  });
}

const DATA = window.__WEBGL_SCENE;
if (DATA) run(DATA);
