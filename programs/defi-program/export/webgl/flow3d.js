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
import * as THREE from 'three';

function lcg(seed) { let s = seed >>> 0 || 1; return () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296; }
const ease = x => x <= 0 ? 0 : x >= 1 ? 1 : 1 - Math.pow(1 - x, 3);
const easeIO = x => x <= 0 ? 0 : x >= 1 ? 1 : x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
const TONE = { good: 0x2ee6a6, bad: 0xeb6834, default: 0x3987e5 };

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
  const rim = new THREE.PointLight(0x3987e5, 2.2, 60); rim.position.set(-7, -4, 8); scene.add(rim);

  // --- ambient depth particles (replaces the flat 2D "living network" canvas for this scene) ---
  const PN = 140;
  const pPos = new Float32Array(PN * 3);
  for (let i = 0; i < PN; i++) {
    pPos[i * 3] = (rnd() - 0.5) * 34; pPos[i * 3 + 1] = (rnd() - 0.5) * 20; pPos[i * 3 + 2] = (rnd() - 0.5) * 26 - 4;
  }
  const pGeo = new THREE.BufferGeometry();
  pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3));
  const pMat = new THREE.PointsMaterial({ color: 0x7fb2ff, size: 0.055, transparent: true, opacity: 0.5, sizeAttenuation: true, blending: THREE.AdditiveBlending, depthWrite: false });
  const particles = new THREE.Points(pGeo, pMat);
  scene.add(particles);

  // --- layout: reuse the server-computed 2D stage positions (px,py from flowLayout), placed on a depth plane ---
  const aspect = H / W, PW = 24, PH = PW * aspect;
  const nodes3 = DATA.nodes.map((n, i) => {
    const x = (n.px / W - 0.5) * PW, y = -(n.py / H - 0.5) * PH;
    const z = Math.sin(i * 2.399963) * 2.4; // golden-angle spread: deterministic, no clustering
    const r = clamp((n.nw || 260) / W * 7.5, 0.62, 1.15);
    return { ...n, i, base: new THREE.Vector3(x, y, z), r, phase: rnd() * 6.28 };
  });
  const byId = Object.fromEntries(nodes3.map(n => [n.id, n]));

  // --- camera framing: derive distance from the actual node spread (not a magic
  // number), so a 2-node compare and a 7-node cycle both stay fully in frame ---
  const bbox = new THREE.Box3();
  nodes3.forEach(n => bbox.expandByPoint(n.base));
  const bboxSize = bbox.getSize(new THREE.Vector3()), centroid = bbox.getCenter(new THREE.Vector3());
  const vFov = 42 * Math.PI / 180;
  const halfW = bboxSize.x / 2 + 2.2, halfH = bboxSize.y / 2 + 3.0; // +margin for node radius + labels hanging below
  const camDist = Math.max(9, Math.max(halfH / Math.tan(vFov / 2), halfW / (Math.tan(vFov / 2) * (W / H))) * 1.22);

  const nodeGeo = new THREE.IcosahedronGeometry(1, 0);
  const meshes = nodes3.map(n => {
    const color = TONE[n.tone] || TONE.default;
    const mat = new THREE.MeshStandardMaterial({
      color, transparent: true, opacity: 0.42, roughness: 0.25, metalness: 0.15,
      emissive: color, emissiveIntensity: 0.55, depthWrite: false,
    });
    const m = new THREE.Mesh(nodeGeo, mat);
    m.scale.setScalar(n.r);
    m.position.copy(n.base);
    const wire = new THREE.Mesh(nodeGeo, new THREE.MeshBasicMaterial({ color: 0xffffff, wireframe: true, transparent: true, opacity: 0.22, depthWrite: false }));
    wire.scale.setScalar(1.015);
    m.add(wire);
    scene.add(m);
    return m;
  });

  // --- edges: a bright core + soft additive halo, both rebuilt from current node positions each frame ---
  const edges3 = DATA.edges.map(e => {
    const color = TONE[e.tone] || 0x7fb2ff;
    const core = new THREE.Line(new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(new Float32Array(6), 3)),
      new THREE.LineBasicMaterial({ color, transparent: true, opacity: 0 }));
    const halo = new THREE.Line(new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(new Float32Array(6), 3)),
      new THREE.LineBasicMaterial({ color, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false, linewidth: 3 }));
    scene.add(core, halo);
    const tokTex = glowTexture();
    const tok = new THREE.Sprite(new THREE.SpriteMaterial({ map: tokTex, color, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false }));
    tok.scale.setScalar(1.1);
    scene.add(tok);
    return { ...e, core, halo, tok, a: byId[e.from], b: byId[e.to] };
  });

  function glowTexture() {
    const c = document.createElement('canvas'); c.width = c.height = 64;
    const ctx = c.getContext('2d');
    const g = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
    g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(0.4, 'rgba(255,255,255,.7)'); g.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.fillStyle = g; ctx.fillRect(0, 0, 64, 64);
    return new THREE.CanvasTexture(c);
  }

  // --- HTML label overlay (crisp text; WebGL only carries the geometry/lighting) ---
  // The 3D mesh itself is the node's "icon" now, so the overlay only carries text —
  // anchored by its top-center so it hangs below the sphere instead of sitting on it.
  function labelHtml(n) {
    const size = clamp((n.nw || 260) * 0.135, 26, 46);
    return `<div style="display:flex;flex-direction:column;align-items:center;text-align:center;gap:4px;transform:translate(-50%,0)">
      <div style="font-size:${size}px;font-weight:800;line-height:1.15;white-space:nowrap;text-shadow:0 2px 14px rgba(0,0,0,.85),0 0 24px rgba(0,0,0,.6)">${n.label || ''}</div>
      ${n.sub ? `<div style="font-size:${size * 0.66}px;line-height:1.25;color:rgba(255,255,255,.78);white-space:nowrap;text-shadow:0 2px 10px rgba(0,0,0,.85)">${n.sub}</div>` : ''}</div>`;
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

  const proj = new THREE.Vector3();
  function project(v3) {
    proj.copy(v3).project(camera);
    return { x: (proj.x * 0.5 + 0.5) * W, y: (-proj.y * 0.5 + 0.5) * H };
  }

  const lookTarget = centroid.clone();

  window.__hooks = window.__hooks || [];
  window.__hooks.push(t => {
    // Camera: a bounded, isometric-feeling sway around the whole node group's
    // centroid (never a full orbit — with nodes roughly in a line, anything wider
    // than a gentle sway pushes the end nodes out of frame) plus a small dolly-in
    // that tracks whichever node is being narrated, without re-aiming the shot.
    const activeIdx = nodes3.findIndex((_, i) => { const [a, b] = DATA.itemsT[i] || [1e9, -1]; return t >= a && t < b; });
    const sway = Math.sin(t * 0.13) * 0.16, tilt = Math.sin(t * 0.09) * 0.05;
    const dollyIn = activeIdx >= 0 ? camDist * 0.055 : 0;
    const d = camDist - dollyIn;
    camera.position.set(centroid.x + Math.sin(sway) * d, centroid.y + Math.sin(tilt) * d * 0.35 + d * 0.06, centroid.z + Math.cos(sway) * d);
    camera.lookAt(lookTarget);
    camera.updateMatrixWorld(true); // labels below project() with THIS frame's camera, not last frame's

    particles.rotation.y = t * 0.015;

    nodes3.forEach((n, i) => {
      const [a, b] = DATA.itemsT[i] || [0, 1e9];
      const inP = ease((t - a) / 0.6);
      const active = t >= a && t < b;
      const bob = Math.sin(t * 0.7 + n.phase) * 0.22;
      const m = meshes[i];
      m.position.set(n.base.x, n.base.y + bob, n.base.z);
      m.scale.setScalar(n.r * (0.6 + 0.4 * inP) * (active ? 1 + 0.04 * Math.sin(t * 3) : 1));
      m.rotation.y = t * 0.25 + i; m.rotation.x = t * 0.12;
      m.material.emissiveIntensity = active ? 0.95 : 0.5;
      m.material.opacity = 0.42 * inP;

      const el = labelEls[i];
      const below = m.position.clone(); below.y -= m.scale.x * 1.45; // anchor labels under the sphere, not on top of it
      const s = project(below);
      el.style.opacity = String(inP * (active || activeIdx < 0 ? 1 : 0.55));
      el.style.transform = `translate(${s.x.toFixed(1)}px, ${s.y.toFixed(1)}px) translateY(${(1 - inP) * 22}px)`;
    });

    edges3.forEach((e, k) => {
      const [a, b] = DATA.edgesT[k] || [0, 1e9];
      const p = easeIO((t - a) / 0.7);
      const A = meshes[e.a.i].position, B = meshes[e.b.i].position;
      const pos = new Float32Array([A.x, A.y, A.z, B.x, B.y, B.z]);
      e.core.geometry.attributes.position.array.set(pos); e.core.geometry.attributes.position.needsUpdate = true;
      e.halo.geometry.attributes.position.array.set(pos); e.halo.geometry.attributes.position.needsUpdate = true;
      e.core.material.opacity = 0.85 * p; e.halo.material.opacity = 0.35 * p;

      if (t > a + 0.4 && t < b) {
        const f = ((t - a - 0.4) / 1.3) % 1, fe = easeIO(f);
        e.tok.position.lerpVectors(meshes[e.a.i].position, meshes[e.b.i].position, fe);
        e.tok.material.opacity = f < 0.1 ? f * 10 : f > 0.9 ? (1 - f) * 10 : 1;
      } else e.tok.material.opacity = 0;

      const lbl = edgeLabelEls[k];
      if (lbl) {
        const mid = new THREE.Vector3().lerpVectors(meshes[e.a.i].position, meshes[e.b.i].position, 0.5);
        const s = project(mid);
        lbl.style.opacity = String(ease((t - a - 0.4) / 0.5));
        lbl.style.transform = `translate(${s.x.toFixed(1)}px, ${s.y.toFixed(1)}px)`;
      }
    });

    renderer.render(scene, camera);
  });
}

const DATA = window.__WEBGL_SCENE;
if (DATA) run(DATA);
