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
const ENTRIES = { 'flow3d': path.join(SRC_DIR, 'flow3d.js') };

function bundlePath(name) { return path.join(OUT_DIR, `webgl-${name}.bundle.js`); }

async function ensure(name) {
  const entry = ENTRIES[name];
  if (!entry) throw new Error(`unknown webgl engine "${name}"`);
  const out = bundlePath(name);
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const srcTime = fs.statSync(entry).mtimeMs;
  const outTime = fs.existsSync(out) ? fs.statSync(out).mtimeMs : 0;
  if (outTime > srcTime) return out;
  await esbuild.build({ entryPoints: [entry], bundle: true, format: 'iife', outfile: out, target: 'chrome120', minify: true, logLevel: 'warning' });
  return out;
}

module.exports = { ensure, bundlePath };
