// Shared building blocks for every WebGL scene engine (flow3d, chart3d, ...):
// deterministic RNG/easing, the brand tone palette, a cheap fresnel "holo" glow
// shell (the well-known Stemkoski glow-shader technique - a second, slightly
// larger mesh with additive blending, not a postprocessing bloom pass, which
// measured 5x too slow with MeshPhysicalMaterial transmission and wasn't
// re-tried as a full-screen pass for the same reason), an ambient depth-particle
// field, and bbox-derived camera framing. Each scene engine is bundled as its
// own separate IIFE (see build_webgl_engine.js), so this file is duplicated
// into each bundle rather than shared at runtime - that's fine, a lesson scene
// only ever loads one bundle at a time.
import * as THREE from 'three';

export function lcg(seed) { let s = seed >>> 0 || 1; return () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296; }
export const ease = x => x <= 0 ? 0 : x >= 1 ? 1 : 1 - Math.pow(1 - x, 3);
export const easeIO = x => x <= 0 ? 0 : x >= 1 ? 1 : x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
export const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
export const TONE = { good: 0x2ee6a6, bad: 0xeb6834, warn: 0xeda100, muted: 0x7fb2ff, default: 0x3987e5 };
export const toneColor = t => TONE[t] || TONE.default;

// One radial-gradient sprite texture, reused (not rebuilt) by every glow sprite
// (edge tokens, chart callouts, particle motes) in a scene.
let _glowTex = null;
export function glowTexture() {
  if (_glowTex) return _glowTex;
  const c = document.createElement('canvas'); c.width = c.height = 64;
  const ctx = c.getContext('2d');
  const g = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
  g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(0.4, 'rgba(255,255,255,.7)'); g.addColorStop(1, 'rgba(255,255,255,0)');
  ctx.fillStyle = g; ctx.fillRect(0, 0, 64, 64);
  _glowTex = new THREE.CanvasTexture(c);
  return _glowTex;
}

// Fresnel rim-glow shell: a second copy of a mesh's geometry, scaled up
// slightly, additive-blended, rendered back-face so the glow reads as a halo
// around the silhouette rather than a bright patch on top of it. One extra
// draw call per node, same triangle count as the base geometry - much cheaper
// than a full-screen bloom pass and doesn't touch the PBR material's own
// shader internals (which would be fragile to hand-patch across three.js
// versions), so it composes safely with any base material.
const RIM_VERT = `
  varying vec3 vNormal;
  varying vec3 vViewDir;
  void main() {
    vNormal = normalize(normalMatrix * normal);
    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
    vViewDir = normalize(-mvPosition.xyz);
    gl_Position = projectionMatrix * mvPosition;
  }`;
const RIM_FRAG = `
  uniform vec3 glowColor;
  uniform float power;
  uniform float intensity;
  varying vec3 vNormal;
  varying vec3 vViewDir;
  void main() {
    float rim = pow(1.0 - max(dot(vNormal, vViewDir), 0.0), power);
    gl_FragColor = vec4(glowColor * intensity, rim * intensity);
  }`;
export function rimGlowMaterial(color, { power = 2.4, intensity = 1.0 } = {}) {
  return new THREE.ShaderMaterial({
    uniforms: { glowColor: { value: new THREE.Color(color) }, power: { value: power }, intensity: { value: intensity } },
    vertexShader: RIM_VERT, fragmentShader: RIM_FRAG,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.BackSide,
  });
}

// A translucent glass-ish base + a wireframe overlay (the facet-edge tracery
// that actually reads as "hologram" - a flat-shaded low-poly fill alone just
// looks like a solid gem) + a fresnel rim-glow shell for the ambient halo, as
// one Object3D. The base carries real PBR lighting (from the scene's point
// lights) so it isn't just a flat silhouette.
export function holoMesh(geometry, color, { opacity = 0.32, emissiveIntensity = 0.5, wireOpacity = 0.5, rimPower = 2.4, rimIntensity = 0.85, rimScale = 1.08 } = {}) {
  const group = new THREE.Group();
  const base = new THREE.Mesh(geometry, new THREE.MeshStandardMaterial({
    color, transparent: true, opacity, roughness: 0.25, metalness: 0.15, emissive: color, emissiveIntensity, depthWrite: false,
  }));
  group.add(base);
  const wire = new THREE.Mesh(geometry, new THREE.MeshBasicMaterial({ color: 0xffffff, wireframe: true, transparent: true, opacity: wireOpacity, depthWrite: false }));
  wire.scale.setScalar(1.012);
  group.add(wire);
  const rim = new THREE.Mesh(geometry, rimGlowMaterial(color, { power: rimPower, intensity: rimIntensity }));
  rim.scale.setScalar(rimScale);
  group.add(rim);
  group.userData = { base, wire, rim };
  return group;
}

// Ambient depth-particle field: replaces the flat scene's 2D "living network"
// canvas background for a WebGL scene. Deterministic per `seed` so re-renders
// (and QA contact sheets) are pixel-stable frame to frame.
export function ambientParticles(scene, seed, { count = 140, spread = [34, 20, 26], color = 0x7fb2ff, size = 0.055, opacity = 0.5 } = {}) {
  const rnd = lcg(seed);
  const pos = new Float32Array(count * 3);
  for (let i = 0; i < count; i++) {
    pos[i * 3] = (rnd() - 0.5) * spread[0]; pos[i * 3 + 1] = (rnd() - 0.5) * spread[1]; pos[i * 3 + 2] = (rnd() - 0.5) * spread[2] - 4;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  const mat = new THREE.PointsMaterial({ color, size, transparent: true, opacity, sizeAttenuation: true, blending: THREE.AdditiveBlending, depthWrite: false });
  const points = new THREE.Points(geo, mat);
  scene.add(points);
  return points;
}

// Camera distance derived from the actual spread of `points` (THREE.Vector3[])
// rather than a magic number, so framing holds regardless of node/bar count or
// layout (row, column, cycle, a chart's bar row, a donut's ring).
export function frameFromPoints(points, W, H, { vFovDeg = 42, marginX = 2.2, marginY = 3.0, minDist = 9, slack = 1.22 } = {}) {
  const bbox = new THREE.Box3();
  points.forEach(p => bbox.expandByPoint(p));
  const size = bbox.getSize(new THREE.Vector3()), centroid = bbox.getCenter(new THREE.Vector3());
  const vFov = vFovDeg * Math.PI / 180;
  const halfW = size.x / 2 + marginX, halfH = size.y / 2 + marginY;
  const dist = Math.max(minDist, Math.max(halfH / Math.tan(vFov / 2), halfW / (Math.tan(vFov / 2) * (W / H))) * slack);
  return { centroid, dist, vFovDeg };
}

// Three distinct, equally bounded camera choreographies - never a full orbit,
// which (with content roughly in a plane) can swing pieces out of frame; see
// flow3d.js's camera-framing note for how this was found empirically. Picking
// between them (see pickCameraMove) is what keeps every lesson's WebGL scenes
// from reading as the exact same shot repeated - see the SKILL.md's "give each
// lesson a distinct treatment" guidance.
// Small integers (this codebase's scene seeds are mostly 1-30-ish) need a real
// mix before a modulo pick, or nearby seeds collapse onto the same variant -
// plain `seed % n` or a bit-shift both do that for the seed range actually in
// use. `mixSeed` gives each `salt` its own decorrelated hash of `seed`.
function mixSeed(seed, salt) { let x = ((seed || 0) + salt) >>> 0; x = Math.imul(x ^ (x >>> 16), 2246822507); x = Math.imul(x ^ (x >>> 13), 3266489909); return (x ^ (x >>> 16)) >>> 0; }

export const CAMERA_MOVES = ['sway', 'rise', 'push'];
export function pickCameraMove(seed) { return CAMERA_MOVES[mixSeed(seed, 0x9e3779b1) % CAMERA_MOVES.length]; }

export function moveCamera(camera, centroid, dist, t, move, { activeDolly = 0, duration = 10 } = {}) {
  const d = dist - activeDolly, prog = clamp(t / duration, 0, 1);
  if (move === 'rise') {
    // a slow vertical arc, camera rising then settling - reads as "revealing" the scene
    const sway = Math.sin(t * 0.1) * 0.14;
    const riseY = centroid.y - d * 0.16 + Math.sin(prog * Math.PI * 0.5) * d * 0.32;
    camera.position.set(centroid.x + Math.sin(sway) * d, riseY, centroid.z + Math.cos(sway) * d);
  } else if (move === 'push') {
    // a slow documentary push-in, tightening the frame as the scene proceeds
    const pushD = d * (1 - 0.14 * prog), sway = Math.sin(t * 0.08) * 0.1;
    camera.position.set(centroid.x + Math.sin(sway) * pushD, centroid.y + d * 0.08, centroid.z + Math.cos(sway) * pushD);
  } else {
    // 'sway' (default): a gentle isometric side-to-side drift
    const sway = Math.sin(t * 0.13) * 0.16, tilt = Math.sin(t * 0.09) * 0.05;
    camera.position.set(centroid.x + Math.sin(sway) * d, centroid.y + Math.sin(tilt) * d * 0.35 + d * 0.06, centroid.z + Math.cos(sway) * d);
  }
  camera.lookAt(centroid);
  camera.updateMatrixWorld(true); // callers project() label positions with THIS frame's camera, not last frame's
}

// A handful of distinct node silhouettes, auto-picked from the scene's seed
// by default so different lessons don't render identical crystal shapes -
// override per scene with an explicit `shape` field if a lesson wants a
// specific one (see SKILL.md).
export const NODE_SHAPES = ['icosahedron', 'octahedron', 'dodecahedron'];
export function pickNodeShape(seed) { return NODE_SHAPES[mixSeed(seed, 0x85ebca6b) % NODE_SHAPES.length]; }
export function makeNodeGeometry(shape) {
  switch (shape) {
    case 'octahedron': return new THREE.OctahedronGeometry(1, 0);
    case 'dodecahedron': return new THREE.DodecahedronGeometry(1, 0);
    default: return new THREE.IcosahedronGeometry(1, 0);
  }
}

// Same counting-up number format as the flat scene's `.ccount`/`.num` handlers
// in scenePage()'s shared script - `c` is the server-parsed {pre,val,dec,comma,post}
// from build_video.js's counter(), `q` is an eased 0..1 progress.
export function formatCounter(c, q) {
  if (!c) return '';
  let x = (c.val * q).toFixed(c.dec);
  if (c.comma) x = Number(x).toLocaleString('en-US', { minimumFractionDigits: c.dec, maximumFractionDigits: c.dec });
  return c.pre + x + c.post;
}

export function project(v3, camera, W, H) {
  const p = v3.clone().project(camera);
  return { x: (p.x * 0.5 + 0.5) * W, y: (-p.y * 0.5 + 0.5) * H };
}
