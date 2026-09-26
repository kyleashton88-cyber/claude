// Three.js scene engine for the `chart3d` scene type: the WebGL counterpart of
// the flat `chart` scene's `bars` and `donut` kinds (no `line` yet - see
// .claude/skills/webgl-motion-graphics/SKILL.md). Bars are glowing vertical
// energy beams with a drifting particle stream instead of flat rounded
// rectangles; a donut is a glowing particle-flecked arc that fills segment by
// segment instead of an SVG stroke-dasharray circle. Same counter/reveal
// timing (T.items) as the flat version, same window.__hooks per-frame
// contract as flow3d.js.
//
// Contract with build_video.js (see sceneBody()'s `chart3d` case):
//   window.__WEBGL_SCENE = {
//     kind: 'bars' | 'donut', W, H, seed, itemsT: [[a,b], ...],
//     bars: [{ label, text, tone, value, base, count }],  max,       // kind:'bars'
//     segs: [{ label, text, tone, f, st, count }], center, centerSub, // kind:'donut'
//   }
import * as THREE from 'three';
import { lcg, ease, easeIO, clamp, toneColor, glowTexture, ambientParticles, frameFromPoints, moveCamera, pickCameraMove, project, formatCounter } from './lib/core.js';

function mount(W, H) {
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
  const key = new THREE.PointLight(0x2ee6a6, 3, 60); key.position.set(6, 6, 12); scene.add(key);
  const rimLight = new THREE.PointLight(0x3987e5, 2, 60); rimLight.position.set(-7, -4, 8); scene.add(rimLight);
  return { renderer, scene, camera, labels };
}

// A solid glowing column: a bright emissive core cylinder + a fatter, very
// transparent additive "aura" cylinder around it - real mesh volume, not a
// thin WebGL line (most browsers clamp line width to 1px regardless of the
// `linewidth` material property, which made an earlier line-based version of
// this read as a bare thread with a dot on top rather than a bar). Both grow
// from a shared base y via scale.y, geometry pre-translated so y=0 is the
// bottom face - the 3D analogue of the flat scene's `scaleY(0..1)` bar.
const BAR_GEO = new THREE.CylinderGeometry(1, 1, 1, 14, 1, true);
BAR_GEO.translate(0, 0.5, 0);
function makeColumn(scene, color, radius) {
  const core = new THREE.Mesh(BAR_GEO, new THREE.MeshStandardMaterial({
    color, transparent: true, opacity: 0.88, roughness: 0.3, metalness: 0.1, emissive: color, emissiveIntensity: 0.7, side: THREE.DoubleSide, depthWrite: false,
  }));
  core.scale.x = core.scale.z = radius;
  const halo = new THREE.Mesh(BAR_GEO, new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.22, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide }));
  halo.scale.x = halo.scale.z = radius * 2.1;
  scene.add(core, halo);
  return {
    core, halo,
    setHeight(baseY, h) {
      core.position.y = halo.position.y = baseY;
      core.scale.y = halo.scale.y = Math.max(0.001, h);
    },
  };
}

function labelDiv(container, html) {
  const el = document.createElement('div');
  el.style.cssText = 'position:absolute;left:0;top:0;opacity:0;will-change:transform,opacity';
  el.innerHTML = html;
  container.appendChild(el);
  return el;
}

function runBars(DATA) {
  const { W, H } = DATA;
  const { renderer, scene, camera, labels } = mount(W, H);
  const rnd = lcg(DATA.seed || 7);
  const n = DATA.bars.length, maxH = 6.4, spacing = clamp(3.6 - n * 0.12, 1.9, 3.6);

  const bars = DATA.bars.map((b, i) => {
    const x = (i - (n - 1) / 2) * spacing;
    const z = (i % 2 ? 1 : -1) * 0.5; // mild depth stagger, not a flat coplanar row
    const targetH = clamp(b.value / DATA.max, 0, 1) * maxH;
    const baseH = clamp((b.base || 0) / DATA.max, 0, 1) * maxH;
    return { ...b, i, x, z, targetH, baseH, color: toneColor(b.tone) };
  });

  const { centroid, dist: camDist } = frameFromPoints(
    bars.flatMap(b => [new THREE.Vector3(b.x, 0, b.z), new THREE.Vector3(b.x, maxH, b.z)]), W, H, { marginX: 2.4, marginY: 2.6 });

  // Measure the actual projected gap between neighboring bars' label anchors
  // (using the same moveCamera/project the render hook uses) so long labels
  // (e.g. "Passkey + hardware key") wrap instead of overflowing sideways into
  // the next bar's label - a fixed nowrap here read fine with short labels but
  // clipped a neighbor's sub-label once real lesson copy ran longer.
  moveCamera(camera, centroid, camDist, 0, DATA.cameraMove || pickCameraMove(DATA.seed), { duration: DATA.dur });
  const anchorX = bars.map(b => project(new THREE.Vector3(b.x, -0.35, b.z), camera, W, H).x);
  const gaps = anchorX.slice(1).map((x, i) => Math.abs(x - anchorX[i]));
  const maxLabelW = Math.max(150, (gaps.length ? Math.min(...gaps) : W * 0.6) * 0.92);

  // ground plinth: a faint line under the whole row
  const plinthGeo = new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(
    new Float32Array([bars[0].x - spacing * 0.6, 0, 0, bars[n - 1].x + spacing * 0.6, 0, 0]), 3));
  scene.add(new THREE.Line(plinthGeo, new THREE.LineBasicMaterial({ color: 0x2a4a6a, transparent: true, opacity: 0.6 })));

  const barRadius = clamp(spacing * 0.24, 0.28, 0.5);
  const columns = bars.map(b => makeColumn(scene, b.color, barRadius));
  const caps = bars.map(b => { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTexture(), color: b.color, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false })); s.scale.setScalar(barRadius * 2.6); scene.add(s); return s; });

  // one shared particle stream for every bar's column (fewer draw calls than
  // one system per bar); each particle loops upward within its own bar's height.
  const PPB = 14, total = n * PPB;
  const streamGeo = new THREE.BufferGeometry();
  const streamPos = new Float32Array(total * 3);
  const streamMeta = bars.flatMap((b, i) => Array.from({ length: PPB }, () => ({ bar: i, phase: rnd(), speed: 0.35 + rnd() * 0.25 })));
  streamGeo.setAttribute('position', new THREE.BufferAttribute(streamPos, 3));
  const streamMat = new THREE.PointsMaterial({ size: 0.09, transparent: true, opacity: 0.8, sizeAttenuation: true, vertexColors: true, blending: THREE.AdditiveBlending, depthWrite: false });
  const streamColors = new Float32Array(total * 3);
  streamGeo.setAttribute('color', new THREE.BufferAttribute(streamColors, 3));
  const stream = new THREE.Points(streamGeo, streamMat);
  scene.add(stream);
  const tmpColor = new THREE.Color();

  const particles = ambientParticles(scene, DATA.seed || 7, { count: 110 });

  const labelEls = bars.map(b => labelDiv(labels, `<div style="text-align:center;max-width:${maxLabelW}px;transform:translate(-50%,0)">
    <div style="font-size:29px;font-weight:700;line-height:1.2;text-shadow:0 2px 12px rgba(0,0,0,.85)">${b.label}</div>
    ${b.text ? `<div style="font-size:22px;font-weight:500;color:rgba(255,255,255,.66);line-height:1.25;text-shadow:0 2px 10px rgba(0,0,0,.85)">${b.text}</div>` : ''}</div>`));
  const countEls = bars.map(b => labelDiv(labels, `<div style="font-size:36px;font-weight:800;white-space:nowrap;transform:translate(-50%,-100%);text-shadow:0 2px 12px rgba(0,0,0,.85)"></div>`));

  window.__hooks = window.__hooks || [];
  window.__hooks.push(t => {
    const activeIdx = bars.findIndex((_, i) => { const [a, b] = DATA.itemsT[i] || [1e9, -1]; return t >= a && t < b; });
    moveCamera(camera, centroid, camDist, t, DATA.cameraMove || pickCameraMove(DATA.seed), { activeDolly: activeIdx >= 0 ? camDist * 0.05 : 0, duration: DATA.dur });
    particles.rotation.y = t * 0.012;

    bars.forEach((b, i) => {
      const [a, bnd] = DATA.itemsT[i] || [0, 1e9];
      const p = easeIO((t - a) / 0.9), active = t >= a && t < bnd;
      const h = b.baseH + (b.targetH - b.baseH) * p;
      const col = columns[i];
      col.setHeight(b.baseH, Math.max(0.02, h - b.baseH));
      col.core.position.x = col.halo.position.x = b.x; col.core.position.z = col.halo.position.z = b.z;
      const glow = active ? 1 : 0.62;
      col.core.material.emissiveIntensity = (active ? 1.0 : 0.55) * glow;
      col.core.material.opacity = 0.88 * (p > 0 ? 1 : 0);
      col.halo.material.opacity = 0.22 * glow * (p > 0 ? 1 : 0);
      const B = new THREE.Vector3(b.x, h, b.z);
      caps[i].position.copy(B);
      caps[i].material.opacity = p > 0.02 ? (active ? 0.95 : 0.6) : 0;
      caps[i].scale.setScalar(barRadius * (active ? 2.9 + 0.2 * Math.sin(t * 3) : 2.3));

      const lp = project(new THREE.Vector3(b.x, -0.35, b.z), camera, W, H);
      const le = labelEls[i]; le.style.opacity = String(ease((t - a) / 0.5) * (0.55 + 0.45 * (active || activeIdx < 0 ? 1 : 0))); le.style.transform = `translate(${lp.x.toFixed(1)}px, ${lp.y.toFixed(1)}px)`;
      const cp = project(new THREE.Vector3(b.x, h + 0.55, b.z), camera, W, H);
      // A bar at (or near) max height projects its counter close to the top of
      // the frame, where the scene's own title/sub header sits (a flat 2D
      // overlay the camera framing above doesn't know about) - clamp so the
      // counter never floats up into it, found on a "Rung 3" bar at 100% height.
      cp.y = Math.max(cp.y, 250);
      const ce = countEls[i]; ce.style.opacity = String(ease((t - a) / 0.4)); ce.style.transform = `translate(${cp.x.toFixed(1)}px, ${cp.y.toFixed(1)}px)`;
      ce.style.color = active ? `#${b.color.toString(16).padStart(6, '0')}` : '#fff';
      ce.firstChild.textContent = formatCounter(b.count, easeIO((t - a) / 1.1));
    });

    for (let k = 0; k < total; k++) {
      const m = streamMeta[k], b = bars[m.bar];
      const [a] = DATA.itemsT[m.bar] || [0];
      const h = Math.max(0.15, b.baseH + (b.targetH - b.baseH) * clamp((t - a) / 0.9, 0, 1));
      const y = h * (((t * m.speed + m.phase) % 1));
      streamPos[k * 3] = b.x + (m.phase - 0.5) * 0.3; streamPos[k * 3 + 1] = y; streamPos[k * 3 + 2] = b.z + (m.phase - 0.5) * 0.3;
      tmpColor.setHex(b.color); const fade = t >= a ? 1 : 0;
      streamColors[k * 3] = tmpColor.r * fade; streamColors[k * 3 + 1] = tmpColor.g * fade; streamColors[k * 3 + 2] = tmpColor.b * fade;
    }
    streamGeo.attributes.position.needsUpdate = true; streamGeo.attributes.color.needsUpdate = true;

    renderer.render(scene, camera);
  });
}

function runDonut(DATA) {
  const { W, H } = DATA;
  const { renderer, scene, camera, labels } = mount(W, H);
  const R = 3.6, TUBE = 0.42;
  const points3 = [new THREE.Vector3(-R, R, 0), new THREE.Vector3(R, -R, 0)]; // bbox stand-in for a ring
  const { centroid, dist: camDist } = frameFromPoints(points3, W, H, { marginX: 2.6, marginY: 2.6 });

  const segs = DATA.segs.map(g => ({ ...g, color: toneColor(g.tone) }));
  const TUBE_R = 0.34;
  function arcPoints(from, to, n) {
    const pts = [];
    for (let i = 0; i <= n; i++) { const a = -Math.PI / 2 + (from + (to - from) * i / n) * Math.PI * 2;
      pts.push(new THREE.Vector3(Math.cos(a) * R, Math.sin(a) * R, 0)); }
    return pts;
  }
  // Each segment is a solid glowing tube built fresh each frame from the arc
  // currently revealed (a thin THREE.Line here rendered as a near-invisible
  // 1px hairline in most browsers, which clamp line width regardless of the
  // `linewidth` material property - the same fix as the bar columns below).
  // Segment count is small (a handful of donut slices), so rebuilding the tube
  // geometry per frame stays inside the measured render budget.
  const arcs = segs.map(g => {
    const mesh = new THREE.Mesh(new THREE.BufferGeometry(), new THREE.MeshStandardMaterial({
      color: g.color, transparent: true, opacity: 0.9, roughness: 0.3, metalness: 0.1, emissive: g.color, emissiveIntensity: 0.6, depthWrite: false,
    }));
    mesh.visible = false;
    scene.add(mesh);
    return { mesh };
  });
  const trackGeo = new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(new Float32Array(arcPoints(0, 1, 96).flatMap(v => [v.x, v.y, v.z])), 3));
  scene.add(new THREE.Line(trackGeo, new THREE.LineBasicMaterial({ color: 0x2a4a6a, transparent: true, opacity: 0.5 })));

  const particles = ambientParticles(scene, DATA.seed || 7, { count: 110 });

  const centerEl = DATA.center ? labelDiv(labels, `<div style="text-align:center;transform:translate(-50%,-50%)">
    <div style="font-size:60px;font-weight:800;text-shadow:0 2px 14px rgba(0,0,0,.85)">${DATA.center}</div>
    ${DATA.centerSub ? `<div style="font-size:22px;color:rgba(255,255,255,.7);text-shadow:0 2px 10px rgba(0,0,0,.85)">${DATA.centerSub}</div>` : ''}</div>`) : null;
  const legendEl = document.createElement('div');
  legendEl.style.cssText = `position:absolute;right:190px;top:50%;transform:translateY(-50%);display:flex;flex-direction:column;gap:16px;pointer-events:none`;
  labels.appendChild(legendEl);
  const legendRows = segs.map(g => {
    const row = document.createElement('div');
    row.style.cssText = 'display:flex;align-items:center;gap:20px;opacity:0;padding:12px 20px;border-radius:14px;transition:none';
    row.innerHTML = `<span style="flex:none;width:24px;height:24px;border-radius:7px;background:#${g.color.toString(16).padStart(6, '0')}"></span>
      <span style="flex:1;font-size:30px;font-weight:700;white-space:nowrap">${g.label}${g.text ? `<span style="display:block;font-size:21px;font-weight:500;color:rgba(255,255,255,.66)">${g.text}</span>` : ''}</span>
      <span class="v" style="font-size:34px;font-weight:800;color:#${g.color.toString(16).padStart(6, '0')};white-space:nowrap"></span>`;
    legendEl.appendChild(row);
    return row;
  });

  window.__hooks = window.__hooks || [];
  window.__hooks.push(t => {
    const activeIdx = segs.findIndex((_, i) => { const [a, b] = DATA.itemsT[i] || [1e9, -1]; return t >= a && t < b; });
    moveCamera(camera, centroid, camDist, t, DATA.cameraMove || pickCameraMove(DATA.seed), { activeDolly: activeIdx >= 0 ? camDist * 0.05 : 0, duration: DATA.dur });
    particles.rotation.y = t * 0.012;

    segs.forEach((g, i) => {
      const [a, b] = DATA.itemsT[i] || [0, 1e9];
      const p = easeIO((t - a) / 0.9), active = t >= a && t < b;
      const cur = g.f * p;
      const mesh = arcs[i].mesh;
      if (cur > 0.002) {
        const n = Math.max(2, Math.round(56 * cur));
        const curve = new THREE.CatmullRomCurve3(arcPoints(g.st, g.st + cur, n));
        mesh.geometry.dispose();
        mesh.geometry = new THREE.TubeGeometry(curve, n, TUBE_R, 8, false);
        mesh.material.opacity = active ? 0.95 : 0.72;
        mesh.material.emissiveIntensity = active ? 0.95 : 0.5;
        mesh.visible = true;
      } else mesh.visible = false;

      const row = legendRows[i];
      row.style.opacity = String(ease((t - a) / 0.5));
      row.style.background = active ? 'rgba(255,255,255,.06)' : 'transparent';
      row.querySelector('.v').textContent = formatCounter(g.count, easeIO((t - a) / 1.1));
    });

    if (centerEl) { const s = project(new THREE.Vector3(0, 0, 0), camera, W, H); centerEl.style.opacity = '1'; centerEl.style.transform = `translate(${s.x.toFixed(1)}px, ${s.y.toFixed(1)}px)`; }

    renderer.render(scene, camera);
  });
}

const DATA = window.__WEBGL_SCENE;
if (DATA) (DATA.kind === 'donut' ? runDonut : runBars)(DATA);
