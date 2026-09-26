// Bundles the Three.js WebGL scene engines (webgl/*.js) into a single classic
// (non-module) script build_video.js can load with <script src="file://...">.
//
// Why bundle at all: three.js has shipped ESM-only since r150 (no browser global
// build), and Chromium refuses to resolve `<script type="module">` imports over
// file:// ("Cross origin requests are only supported for protocol schemes:
// chrome, chrome-extension, ... http, https, ..." — file: isn't in that list).
// A classic script tag doesn't hit that check, so esbuild flattens three.js +
// the scene code into one IIFE ahead of time and build_video.js loads that.
//
// Rebuilt automatically by build_video.js (ensure()) whenever webgl/*.js is newer
// than the cached bundle, so authors never run this by hand.
const fs = require('fs');
const path = require('path');
const esbuild = require('esbuild');

const SRC_DIR = path.join(__dirname, 'webgl');
const OUT_DIR = path.join(__dirname, '.render');
const ENTRIES = { 'flow3d': path.join(SRC_DIR, 'flow3d.js'), 'chart3d': path.join(SRC_DIR, 'chart3d.js') };

function bundlePath(name) { return path.join(OUT_DIR, `webgl-${name}.bundle.js`); }

// Freshness is checked against every file under webgl/ (entries import shared
// helpers from webgl/lib/*.js), not just the one entry file - otherwise editing
// a shared helper without touching the entry would silently keep serving a
// stale bundle.
function newestMtime(dir) {
  let newest = 0;
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    newest = Math.max(newest, e.isDirectory() ? newestMtime(p) : fs.statSync(p).mtimeMs);
  }
  return newest;
}

async function ensure(name) {
  const entry = ENTRIES[name];
  if (!entry) throw new Error(`unknown webgl engine "${name}"`);
  const out = bundlePath(name);
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const srcTime = newestMtime(SRC_DIR);
  const outTime = fs.existsSync(out) ? fs.statSync(out).mtimeMs : 0;
  if (outTime > srcTime) return out;
  await esbuild.build({ entryPoints: [entry], bundle: true, format: 'iife', outfile: out, target: 'chrome120', minify: true, logLevel: 'warning' });
  return out;
}

module.exports = { ensure, bundlePath };
