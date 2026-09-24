// Capture a screen demo as a sequence of screenshots for a `cutaway` scene.
//
// Usage:  node capture_demo.js ../demos/<id>.json
// Input:  a demo spec (see ../demos/README.md):
//   { "id": "aave-health-factor", "url": "https://app.example.org", "viewport": [1600, 900],
//     "steps": [ { "goto": "https://..." }, { "click": "text=Borrow" }, { "type": ["#amount", "100"] },
//                { "wait": 1200 }, { "scroll": 600 }, { "hover": "css=.health" },
//                { "shot": "01", "caption": "Open the market", "highlight": "css=.health", "blur": ["css=.address"] } ] }
// Output: ../assets/demos/<id>/<shot>.png, plus ../demos/<id>.scene.json: a ready-to-paste
//         `cutaway` scene with normalised highlight boxes and blur boxes for every shot.
//
// Safety: never types into password fields or anything that looks like a seed phrase box,
// and refuses spec text that looks like a private key or a 12/24-word mnemonic.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');

const ROOT = path.resolve(__dirname, '..');
const CHROME = process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
// A 64-hex private key, or a string that is nothing but 12-24 short lowercase words (a mnemonic).
const looksSecret = s => { const x = String(s).trim(), w = x.split(/\s+/);
  return /\b(0x)?[0-9a-f]{64}\b/i.test(x) || ([12, 15, 18, 21, 24].includes(w.length) && w.every(y => /^[a-z]{3,8}$/.test(y))); };
const strings = o => (typeof o === 'string' ? [o] : o && typeof o === 'object' ? Object.values(o).flatMap(strings) : []);

(async () => {
  const specFile = process.argv[2];
  if (!specFile) { console.error('usage: node capture_demo.js ../demos/<id>.json'); process.exit(1); }
  const spec = JSON.parse(fs.readFileSync(specFile, 'utf8'));
  if (strings(spec).some(looksSecret)) throw new Error('spec contains something that looks like a private key or seed phrase: remove it');
  const [W, H] = spec.viewport || [1600, 900];
  const outDir = path.join(ROOT, 'assets', 'demos', spec.id);
  fs.mkdirSync(outDir, { recursive: true });

  const browser = await chromium.launch({ executablePath: CHROME });
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  const resolve = u => (u.startsWith('file:') && !u.startsWith('file://') ? `file://${path.resolve(path.dirname(specFile), u.slice(5))}` : u);
  if (spec.url) await page.goto(resolve(spec.url), { waitUntil: 'networkidle' });

  const box = async sel => {
    const b = await page.locator(sel).first().boundingBox();
    if (!b) throw new Error(`no visible element for ${sel}`);
    const pad = 8;
    const x = Math.max(0, (b.x - pad) / W), y = Math.max(0, (b.y - pad) / H);
    const w = Math.min(1 - x, (b.width + pad * 2) / W), h = Math.min(1 - y, (b.height + pad * 2) / H);
    return [x, y, w, h].map(v => +v.toFixed(4));
  };

  const shots = [];
  for (const st of spec.steps) {
    if (st.goto) await page.goto(resolve(st.goto), { waitUntil: 'networkidle' });
    if (st.click) await page.locator(st.click).first().click();
    if (st.hover) await page.locator(st.hover).first().hover();
    if (st.type) {
      const [sel, text] = st.type, loc = page.locator(sel).first();
      const attrs = await loc.evaluate(el => `${el.type || ''} ${el.name || ''} ${el.id || ''} ${el.placeholder || ''}`.toLowerCase());
      if (/password|seed|mnemonic|private|secret|recovery/.test(attrs) || looksSecret(text)) throw new Error(`refusing to type into ${sel}: looks like a secret field`);
      await loc.fill(String(text));
    }
    if (st.scroll) await page.mouse.wheel(0, st.scroll);
    if (st.wait) await page.waitForTimeout(st.wait);
    if (st.shot) {
      await page.waitForTimeout(st.settle ?? 400);
      const file = path.join(outDir, `${st.shot}.png`);
      await page.screenshot({ path: file });
      const shot = { src: path.relative(ROOT, file), caption: st.caption || '' };
      if (st.highlight) shot.box = await box(st.highlight);
      if (st.blur) {
        shot.blur = [];
        for (const sel of st.blur) { const n = await page.locator(sel).count(); if (!n) { console.warn(`blur: nothing matches ${sel} (skipped)`); continue; }
          for (let i = 0; i < n; i++) { const b = await page.locator(sel).nth(i).boundingBox(); if (b) shot.blur.push([b.x / W, b.y / H, b.width / W, b.height / H].map(v => +v.toFixed(4))); } }
      }
      if (st.push) shot.push = st.push;
      shots.push(shot);
      console.log(`shot ${st.shot}${shot.box ? ' box ' + shot.box.join(',') : ''}`);
    }
  }
  await browser.close();
  const scene = { type: 'cutaway', chapter: spec.chapter || 'Do it', label: spec.label || 'On screen', url: spec.showUrl || '', shots,
    vo: spec.vo || shots.map(s => `${s.caption}.`).join(' ') };
  const out = path.join(path.dirname(specFile), `${spec.id}.scene.json`);
  fs.writeFileSync(out, JSON.stringify(scene, null, 2));
  console.log(`wrote ${shots.length} shots to assets/demos/${spec.id}/ and ${path.relative(ROOT, out)}`);
})().catch(e => { console.error(e.message); process.exit(1); });
