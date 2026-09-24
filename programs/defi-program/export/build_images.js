// Render every On-Chain Operator Program image (store listing, module banners,
// diagrams, charts) to PNG at 2x with Chromium.
// Usage: node build_images.js            -> writes ../assets/**.png
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');

const OUT = path.resolve(__dirname, '..', 'assets');
const RENDER = path.join(__dirname, '.render');
const FONT = (pkg, w) => `file://${require.resolve(`@fontsource/${pkg}/${w}.css`)}`;

// Brand tokens. Chart series: blue, orange (validated pair); aqua only on dark.
const C = {
  ink: '#0B1F33', navy: '#12355B', brand: '#1F4E79', blue: '#2a78d6', blueDark: '#3987e5',
  orange: '#eb6834', aqua: '#1baf7a', aquaDark: '#2ee6a6', yellow: '#eda100',
  surface: '#FCFCFB', panel: '#F3F6F9', line: '#D9E1EA', text: '#0b0b0b', text2: '#52514e', muted: '#8a8f98',
};
const DISCLAIMER = 'Educational content only · Not financial advice · No results are guaranteed';

// ---------- shared pieces ----------
function lcg(seed) { let s = seed; return () => (s = (s * 1664525 + 1013904223) % 4294967296) / 4294967296; }

// Faint node-network motif for dark backgrounds.
function network(w, h, seed = 7, n = 38, opacity = 0.16) {
  const r = lcg(seed);
  const pts = Array.from({ length: n }, () => [r() * w, r() * h]);
  let lines = '';
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
    const d = Math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1]);
    if (d < w * 0.14) lines += `<line x1="${pts[i][0]}" y1="${pts[i][1]}" x2="${pts[j][0]}" y2="${pts[j][1]}" stroke="#7fb2ff" stroke-width="1" opacity="${(1 - d / (w * 0.14)) * opacity}"/>`;
  }
  const dots = pts.map(([x, y], i) => `<circle cx="${x}" cy="${y}" r="${i % 5 ? 2.2 : 3.6}" fill="${i % 7 ? '#7fb2ff' : C.aquaDark}" opacity="${opacity * 2.2}"/>`).join('');
  return `<svg class="bg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">${lines}${dots}</svg>`;
}

// Line icons, 24x24 viewBox, stroke = currentColor.
const ICON = {
  shield: '<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
  swap: '<path d="M4 8h13l-3-3"/><path d="M20 16H7l3 3"/>',
  bank: '<path d="M3 10l9-6 9 6"/><path d="M5 10v8M10 10v8M14 10v8M19 10v8M3 20h18"/>',
  sprout: '<path d="M12 21v-9"/><path d="M12 12c0-4 3-7 8-7 0 5-3 7-8 7z"/><path d="M12 14c0-3-2.5-5.5-7-5.5 0 4 2.5 5.5 7 5.5z"/>',
  layers: '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
  search: '<circle cx="10.5" cy="10.5" r="6"/><path d="M15 15l5 5"/>',
  chart: '<path d="M4 20V4"/><path d="M4 20h16"/><path d="M7 15l4-4 3 3 5-6"/>',
  cog: '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/>',
  grid: '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/>',
  lock: '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 018 0v4"/>',
  wallet: '<rect x="3" y="6" width="18" height="14" rx="2"/><path d="M3 10h18"/><circle cx="16.5" cy="15" r="1.2"/>',
  flame: '<path d="M12 21c-4 0-6-2.7-6-6 0-4 4-6 4-11 3 2 8 5.5 8 11 0 3.3-2 6-6 6z"/>',
  exit: '<path d="M14 4h5v16h-5"/><path d="M10 8l-4 4 4 4"/><path d="M6 12h10"/>',
  users: '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14c3 0 5.5 2 5.5 5"/>',
  video: '<rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10l5-3v10l-5-3"/>',
  book: '<path d="M4 5a2 2 0 012-2h13v16H6a2 2 0 00-2 2z"/><path d="M4 21V5"/>',
  check: '<path d="M5 12l4 4 10-10"/>',
};
const icon = (name, size = 24, color = 'currentColor', sw = 1.8) =>
  `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round">${ICON[name]}</svg>`;

const MODULES = [
  { n: 1, t: 'Foundations & Safety', o: 'Set up and use a wallet safely. Know what can go irreversibly wrong.', i: 'shield', l: 6 },
  { n: 2, t: 'Trading On-Chain', o: 'Swap and provide liquidity deliberately: price impact, IL, MEV.', i: 'swap', l: 5 },
  { n: 3, t: 'Lending & Leverage', o: 'Borrow against collateral with a buffer and a written defence plan.', i: 'bank', l: 4 },
  { n: 4, t: 'Yield', o: 'Split any APY into organic vs subsidised, and name the risk being paid for.', i: 'sprout', l: 6 },
  { n: 5, t: 'Infrastructure Risk', o: 'Map every bridge, oracle, L2 and contract a position depends on.', i: 'layers', l: 5 },
  { n: 6, t: 'Protocol Research', o: 'Complete a full due-diligence file on a real protocol.', i: 'search', l: 4 },
  { n: 7, t: 'On-Chain Analytics', o: 'Read on-chain data without over-interpreting it.', i: 'chart', l: 8 },
  { n: 8, t: 'The DeFi Operating System', o: 'Portfolio plan with risk buckets, limits and an emergency plan.', i: 'cog', l: 4 },
  { n: 9, t: 'DeFi vs Grid Bots', o: 'Choose the right tool for the market, and run both as one system.', i: 'grid', l: 3 },
];

const BASE_CSS = `
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: Inter, sans-serif; -webkit-font-smoothing: antialiased; }
  .mono { font-family: 'JetBrains Mono', monospace; }
  .dark { background: radial-gradient(120% 90% at 85% 0%, #1d4a78 0%, ${C.navy} 38%, ${C.ink} 100%); color: #fff; position: relative; overflow: hidden; }
  .light { background: ${C.surface}; color: ${C.text}; position: relative; overflow: hidden; }
  .bg { position: absolute; inset: 0; }
  .eyebrow { font-weight: 700; letter-spacing: .18em; text-transform: uppercase; }
  .foot { position: absolute; left: 0; right: 0; bottom: 0; font-size: 15px; color: rgba(255,255,255,.55); padding: 22px 72px; display: flex; justify-content: space-between; }
  .light .foot { color: ${C.muted}; }
`;

function page(w, h, cls, inner) {
  return `<!doctype html><html><head><meta charset="utf-8">
  ${[400, 500, 600, 700, 800].map(x => `<link rel="stylesheet" href="${FONT('inter', x)}">`).join('')}
  <link rel="stylesheet" href="${FONT('jetbrains-mono', 500)}">
  <style>${BASE_CSS} #root { width: ${w}px; height: ${h}px; }</style></head>
  <body><div id="root" class="${cls}">${inner}</div></body></html>`;
}

const brandMark = (size = 40) => `
  <svg width="${size}" height="${size}" viewBox="0 0 40 40">
    <rect x="1" y="1" width="38" height="38" rx="10" fill="none" stroke="${C.aquaDark}" stroke-width="2"/>
    <circle cx="13" cy="20" r="5" fill="none" stroke="#fff" stroke-width="2.4"/>
    <circle cx="27" cy="20" r="5" fill="none" stroke="#fff" stroke-width="2.4"/>
    <path d="M18 20h4" stroke="${C.aquaDark}" stroke-width="2.4"/>
  </svg>`;
const wordmark = (s = 22) => `<div style="display:flex;align-items:center;gap:14px">${brandMark(s * 1.8)}
  <div style="font-weight:700;font-size:${s}px;letter-spacing:.02em">On-Chain Operator Program</div></div>`;

// ---------- store assets (dark) ----------
function storeIcon() {
  const w = 1024;
  return page(w, w, 'dark', `${network(w, w, 11, 30, 0.22)}
  <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:40px">
    <svg width="560" height="360" viewBox="0 0 280 180">
      <circle cx="90" cy="90" r="62" fill="none" stroke="#fff" stroke-width="14"/>
      <circle cx="190" cy="90" r="62" fill="none" stroke="#fff" stroke-width="14"/>
      <path d="M140 46v88" stroke="${C.aquaDark}" stroke-width="14" stroke-linecap="round"/>
      <circle cx="140" cy="90" r="10" fill="${C.aquaDark}"/>
    </svg>
    <div class="eyebrow" style="font-size:54px;color:#fff;letter-spacing:.3em">ON-CHAIN</div>
    <div class="eyebrow" style="font-size:34px;color:${C.aquaDark};letter-spacing:.42em;margin-top:-26px">OPERATOR</div>
  </div>`);
}

function storeBanner() {
  const w = 1920, h = 1080;
  const stats = [['9', 'modules'], ['45', 'lessons'], ['16', 'strategy playbooks'], ['1', 'capstone']];
  return page(w, h, 'dark', `${network(w, h, 3, 60)}
  <div style="position:absolute;left:120px;top:110px">${wordmark(26)}</div>
  <div style="position:absolute;left:120px;top:300px;width:1180px">
    <div class="eyebrow" style="color:${C.aquaDark};font-size:24px">The risk-first DeFi operating system</div>
    <div style="font-size:112px;font-weight:800;line-height:1.02;margin-top:26px;letter-spacing:-.02em">Research. Size.<br>Exit. <span style="color:${C.aquaDark}">On-chain.</span></div>
    <div style="font-size:34px;line-height:1.4;color:rgba(255,255,255,.82);margin-top:34px;width:1000px">Learn to research any protocol, know exactly where yield comes from, and never sign a position you can't unwind.</div>
  </div>
  <div style="position:absolute;left:120px;bottom:120px;display:flex;gap:26px">
    ${stats.map(([a, b]) => `<div style="padding:22px 34px;border:1px solid rgba(255,255,255,.18);border-radius:18px;background:rgba(255,255,255,.05)">
      <div style="font-size:52px;font-weight:800">${a}</div><div style="font-size:22px;color:rgba(255,255,255,.7)">${b}</div></div>`).join('')}
  </div>
  ${heroVisual(1360, 250)}
  <div class="foot" style="padding:22px 120px"><span>${DISCLAIMER}</span><span>Live tier available</span></div>`);
}

// Stylised concentrated-liquidity range visual used on the banner.
function heroVisual(x, y) {
  const W = 460, H = 560, r = lcg(21);
  let p = 300, pts = [];
  for (let i = 0; i <= 60; i++) { p += (r() - 0.5) * 34 + (300 - p) * 0.08; pts.push([i * W / 60, p]); }
  const d = pts.map(([a, b], i) => `${i ? 'L' : 'M'}${a.toFixed(1)},${b.toFixed(1)}`).join('');
  const levels = Array.from({ length: 11 }, (_, i) => 150 + i * 30);
  return `<svg style="position:absolute;left:${x}px;top:${y}px" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
    <rect x="0" y="150" width="${W}" height="300" rx="14" fill="${C.aquaDark}" opacity=".10" stroke="${C.aquaDark}" stroke-opacity=".5"/>
    ${levels.map(yy => `<line x1="0" x2="${W}" y1="${yy}" y2="${yy}" stroke="#fff" stroke-opacity=".12" stroke-dasharray="4 6"/>`).join('')}
    <path d="${d}" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/>
    <circle cx="${pts[60][0]}" cy="${pts[60][1]}" r="9" fill="${C.aquaDark}"/>
    <text x="0" y="132" fill="rgba(255,255,255,.7)" font-size="20" font-family="Inter">Operating range</text>
    <text x="0" y="492" fill="rgba(255,255,255,.7)" font-size="20" font-family="Inter">Invalidation defined before entry</text>
  </svg>`;
}

function galleryShell(eyebrow, title, body, seed) {
  const w = 1920, h = 1080;
  return page(w, h, 'dark', `${network(w, h, seed, 44, 0.12)}
  <div style="position:absolute;left:110px;top:90px;right:110px">
    <div style="display:flex;justify-content:space-between;align-items:center">${wordmark(20)}
      <div class="eyebrow" style="color:${C.aquaDark};font-size:20px">${eyebrow}</div></div>
    <div style="font-size:66px;font-weight:800;margin-top:54px;letter-spacing:-.015em">${title}</div>
  </div>
  <div style="position:absolute;left:110px;right:110px;top:330px;bottom:110px">${body}</div>
  <div class="foot" style="padding:22px 110px"><span>${DISCLAIMER}</span></div>`);
}

function galleryCurriculum() {
  const cards = MODULES.map(m => `<div style="border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.05);border-radius:20px;padding:26px 28px;display:flex;gap:22px;align-items:flex-start">
    <div style="flex:none;width:62px;height:62px;border-radius:16px;background:rgba(46,230,166,.14);display:flex;align-items:center;justify-content:center;color:${C.aquaDark}">${icon(m.i, 34)}</div>
    <div><div style="font-size:17px;color:rgba(255,255,255,.6);font-weight:600">MODULE ${m.n} · ${m.l} LESSONS</div>
    <div style="font-size:29px;font-weight:700;margin-top:6px">${m.t}</div>
    <div style="font-size:19px;color:rgba(255,255,255,.72);margin-top:8px;line-height:1.35">${m.o}</div></div></div>`).join('');
  return galleryShell('Curriculum', '9 modules · 45 lessons · 1 capstone',
    `<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:24px">${cards}</div>`, 5);
}

function galleryLoop() { return galleryShell('Method', 'The 6-step research loop', loopSvg(true), 9); }
function galleryLevels() { return galleryShell('Strategy library', '16 strategies, 5 levels, risk first', levelsHtml(true), 13); }
function galleryGridLp() { return galleryShell('Module 9', 'A DeFi LP is an on-chain grid bot', gridLpSvg(true), 17); }

function galleryIncluded() {
  const col = (title, sub, items, accent) => `<div style="flex:1;border:1px solid ${accent ? C.aquaDark : 'rgba(255,255,255,.16)'};background:rgba(255,255,255,${accent ? '.08' : '.04'});border-radius:24px;padding:44px 48px">
    <div class="eyebrow" style="color:${accent ? C.aquaDark : 'rgba(255,255,255,.65)'};font-size:20px">${sub}</div>
    <div style="font-size:48px;font-weight:800;margin:10px 0 28px">${title}</div>
    ${items.map(([ic, t]) => `<div style="display:flex;gap:20px;align-items:center;margin:26px 0;font-size:32px;color:rgba(255,255,255,.92)"><span style="color:${C.aquaDark}">${icon(ic, 36)}</span>${t}</div>`).join('')}
  </div>`;
  return galleryShell('What\'s included', 'Two ways to join', `<div style="display:flex;gap:36px;height:100%">
    ${col('Course', 'Self-paced', [['book', '9 modules, 45 lessons'], ['check', 'Checklists & quizzes every lesson'], ['search', 'Due-diligence & pre-launch worksheets'], ['chart', 'Strategy calculator'], ['lock', 'Capstone project']], false)}
    ${col('Live', 'Course + coaching', [['check', 'Everything in Course'], ['video', 'Live group sessions'], ['users', 'Capstone & portfolio reviews'], ['search', 'Protocol research Q&A'], ['shield', 'Risk-plan feedback']], true)}
  </div>`, 19);
}

// ---------- module banners ----------
function moduleBanner(m) {
  const w = 1600, h = 500;
  return page(w, h, 'dark', `${network(w, h, 30 + m.n, 34, 0.14)}
  <div style="position:absolute;left:80px;top:0;bottom:0;display:flex;align-items:center;gap:40px">
    <div style="width:330px;flex:none;font-size:230px;font-weight:800;line-height:1;color:transparent;-webkit-text-stroke:3px rgba(255,255,255,.35)">${String(m.n).padStart(2, '0')}</div>
    <div style="width:880px">
      <div class="eyebrow" style="color:${C.aquaDark};font-size:22px">Module ${m.n} · ${m.l} lessons</div>
      <div style="font-size:66px;font-weight:800;margin-top:12px;letter-spacing:-.015em;white-space:nowrap">${m.t}</div>
      <div style="font-size:28px;color:rgba(255,255,255,.8);margin-top:18px;line-height:1.35">${m.o}</div>
    </div>
  </div>
  <div style="position:absolute;right:90px;top:50%;transform:translateY(-50%);width:170px;height:170px;border-radius:40px;background:rgba(46,230,166,.12);border:1px solid rgba(46,230,166,.4);display:flex;align-items:center;justify-content:center;color:${C.aquaDark}">${icon(m.i, 96, 'currentColor', 1.5)}</div>
  <div style="position:absolute;left:80px;bottom:34px;font-size:18px;color:rgba(255,255,255,.55)">On-Chain Operator Program</div>`);
}

// ---------- diagrams (light for documents; some reused dark in gallery) ----------
function lightShell(w, h, title, sub, body) {
  return page(w, h, 'light', `
  <div style="position:absolute;left:64px;top:52px;right:64px">
    <div style="font-size:40px;font-weight:800;color:${C.ink};letter-spacing:-.01em">${title}</div>
    ${sub ? `<div style="font-size:22px;color:${C.text2};margin-top:10px">${sub}</div>` : ''}
  </div>
  <div style="position:absolute;left:64px;right:64px;top:${sub ? 170 : 130}px;bottom:70px">${body}</div>
  <div class="foot" style="padding:18px 64px;font-size:14px"><span>On-Chain Operator Program</span><span>${DISCLAIMER}</span></div>`);
}

function loopSvg(dark) {
  const steps = [['Mechanism', 'What the contracts actually do'], ['Cash flow', 'Real fees vs emissions'], ['Dependencies', 'Oracles, bridges, admin keys'],
    ['Solvency', 'Collateral, liquidations, bad debt'], ['Evidence', 'Explorers, audits, governance'], ['Exit', 'The exact unwind, planned before entry']];
  const fg = dark ? '#fff' : C.ink, sub = dark ? 'rgba(255,255,255,.72)' : C.text2;
  const acc = dark ? C.aquaDark : C.blue, card = dark ? 'rgba(255,255,255,.06)' : '#fff', stroke = dark ? 'rgba(255,255,255,.2)' : C.line;
  const arrow = `<svg width="44" height="30" viewBox="0 0 44 30" style="flex:none"><path d="M4 15H34" stroke="${acc}" stroke-width="3"/><path d="M28 7L38 15L28 23" fill="none" stroke="${acc}" stroke-width="3"/></svg>`;
  const cards = steps.map(([t, s], i) => `<div style="flex:1;min-width:0;height:230px;border-radius:20px;background:${card};border:1.5px solid ${i === 5 ? acc : stroke};padding:26px 22px">
      <div style="width:52px;height:52px;border-radius:50%;background:${acc};color:${dark ? C.ink : '#fff'};font-size:26px;font-weight:800;display:flex;align-items:center;justify-content:center">${i + 1}</div>
      <div style="font-size:28px;font-weight:700;color:${fg};margin-top:20px">${t}</div>
      <div style="font-size:20px;color:${sub};margin-top:8px;line-height:1.35">${s}</div></div>`).join(arrow);
  return `<div style="display:flex;flex-direction:column;justify-content:center;height:100%">
    <div style="display:flex;align-items:center">${cards}</div>
    <svg width="100%" height="110" viewBox="0 0 1672 110" preserveAspectRatio="none" style="margin-top:6px">
      <path d="M1540 6 V60 H130 V14" fill="none" stroke="${acc}" stroke-width="3" stroke-dasharray="10 9"/>
      <path d="M121 22 L130 6 L139 22" fill="none" stroke="${acc}" stroke-width="3"/></svg>
    <div style="text-align:center;margin-top:-34px;font-size:24px;font-weight:700;color:${fg}">Repeat for every protocol · log it in the due-diligence tracker · no capital moves until step 6 is written</div>
  </div>`;
}

function levelsHtml(dark) {
  const L = [['1', 'Core', 'Stable lending · Staking & LSTs · Collateral borrowing'], ['2', 'Liquidity', '50/50 LP · Concentrated LP · Stable-stable LP'],
    ['3', 'Yield', 'Vaults · Incentive farming · Airdrops & points'], ['4', 'Advanced', 'Leveraged loops · LST loops · Funding carry · LP hedge'],
    ['5', 'Treasury & research', 'Cash management · Accumulation & growth screens']];
  const fg = dark ? '#fff' : C.ink, sub = dark ? 'rgba(255,255,255,.75)' : C.text2;
  return `<div style="display:flex;flex-direction:column;gap:18px;height:100%;justify-content:center">
    ${L.map(([n, t, s], i) => `<div style="display:flex;align-items:center;gap:30px;margin-left:${i * 70}px;padding:20px 30px;border-radius:18px;
      background:${dark ? `rgba(46,230,166,${0.05 + i * 0.03})` : '#fff'};border:1px solid ${dark ? 'rgba(46,230,166,.35)' : C.line}">
      <div style="font-size:54px;font-weight:800;width:60px;color:${dark ? C.aquaDark : C.blue}">${n}</div>
      <div style="font-size:32px;font-weight:700;width:360px;color:${fg}">${t}</div>
      <div style="font-size:24px;color:${sub}">${s}</div></div>`).join('')}
    <div style="font-size:22px;color:${sub};margin-top:8px">Graduate a level only when the one below is routine. Leverage and carry come last.</div>
  </div>`;
}

function gridLpSvg(dark) {
  const W = 1700, H = 620, top = 80, bot = 560, lo = 2700, hi = 3300;
  const y = p => bot - (p - lo) / (hi - lo) * (bot - top);
  const fg = dark ? '#fff' : C.ink, sub = dark ? 'rgba(255,255,255,.72)' : C.text2, grid = dark ? 'rgba(255,255,255,.14)' : C.line;
  const buy = dark ? C.blueDark : C.blue, sell = C.orange;
  const panel = (x0, title, inner) => `<g transform="translate(${x0},0)"><text x="0" y="30" font-size="28" font-weight="700" fill="${fg}" font-family="Inter">${title}</text>${inner}</g>`;
  let gridLines = '';
  for (let p = lo; p <= hi; p += 30) gridLines += `<line x1="90" x2="520" y1="${y(p)}" y2="${y(p)}" stroke="${p < 3000 ? buy : p > 3000 ? sell : fg}" stroke-width="${p === 3000 ? 3 : 2}" stroke-opacity="${p === 3000 ? 1 : 0.75}"/>`;
  const axis = [2700, 2850, 3000, 3150, 3300].map(p => `<text x="80" y="${y(p) + 7}" text-anchor="end" font-size="20" fill="${sub}" font-family="Inter">$${p.toLocaleString()}</text>`).join('');
  const gridPanel = `${axis}${gridLines}
    <text x="540" y="${y(2835) + 8}" font-size="22" fill="${fg}" font-family="Inter" font-weight="700">avg buy ≈ $2,835</text>
    <text x="540" y="${y(3165) + 8}" font-size="22" fill="${fg}" font-family="Inter" font-weight="700">avg sell ≈ $3,165</text>
    <text x="540" y="${y(3000) + 8}" font-size="20" fill="${sub}" font-family="Inter">price now $3,000</text>`;
  const lpPanel = `${axis}
    <defs><linearGradient id="lpg${dark ? 'd' : 'l'}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${sell}" stop-opacity=".55"/><stop offset=".5" stop-color="${fg}" stop-opacity=".06"/><stop offset="1" stop-color="${buy}" stop-opacity=".55"/></linearGradient></defs>
    <rect x="90" y="${y(hi)}" width="430" height="${y(lo) - y(hi)}" rx="12" fill="url(#lpg${dark ? 'd' : 'l'})" stroke="${grid}"/>
    <line x1="90" x2="520" y1="${y(3000)}" y2="${y(3000)}" stroke="${fg}" stroke-width="3"/>
    <text x="540" y="${y(2846) + 8}" font-size="22" fill="${fg}" font-family="Inter" font-weight="700">avg buy ≈ $2,846</text>
    <text x="540" y="${y(3146) + 8}" font-size="22" fill="${fg}" font-family="Inter" font-weight="700">avg sell ≈ $3,146</text>
    <text x="540" y="${y(3000) + 8}" font-size="20" fill="${sub}" font-family="Inter">continuous in range</text>`;
  return `<svg width="100%" height="100%" viewBox="0 0 ${W} ${H}">
    ${panel(0, 'Grid bot · 20 levels, $30 apart', gridPanel)}
    ${panel(880, 'Concentrated LP · same range', lpPanel)}
    <text x="0" y="${H - 4}" font-size="20" fill="${sub}" font-family="Inter">Blue = buys as price falls · Orange = sells as price rises · Range $2,700–$3,300, ETH at $3,000. Illustrative.</text>
  </svg>`;
}

function flowBoxes(items, dark = false, opts = {}) {
  // Vertical or horizontal chain of boxes with arrows.
  const { dir = 'row', w = 300, h = 150, gap = 70, loop = false } = opts;
  const acc = C.blue;
  const boxes = items.map(([t, s, ic], i) => `<div style="flex:none;width:${w}px;height:${h}px;border-radius:18px;background:#fff;border:1.5px solid ${C.line};padding:22px 24px;box-shadow:0 2px 0 rgba(15,40,70,.04)">
      <div style="display:flex;align-items:center;gap:12px;color:${acc}">${ic ? icon(ic, 30) : ''}<div style="font-size:30px;font-weight:700;color:${C.ink}">${t}</div></div>
      <div style="font-size:23px;color:${C.text2};margin-top:14px;line-height:1.4">${s}</div></div>`);
  const arrow = dir === 'row'
    ? `<svg width="${gap}" height="30" viewBox="0 0 ${gap} 30"><path d="M4 15H${gap - 10}" stroke="${acc}" stroke-width="3"/><path d="M${gap - 16} 7L${gap - 6} 15L${gap - 16} 23" fill="none" stroke="${acc}" stroke-width="3"/></svg>`
    : `<svg width="30" height="${gap}" viewBox="0 0 30 ${gap}"><path d="M15 4V${gap - 10}" stroke="${acc}" stroke-width="3"/><path d="M7 ${gap - 16}L15 ${gap - 6}L23 ${gap - 16}" fill="none" stroke="${acc}" stroke-width="3"/></svg>`;
  return `<div style="display:flex;flex-direction:${dir};align-items:center;justify-content:center;height:100%">${boxes.join(arrow)}</div>`;
}

function diagramLiquidation() {
  const W = 1700, H = 560;
  const n = [['Collateral price falls', 'ETH drops'], ['Health factor drops', 'toward 1.0'], ['Liquidation', 'Collateral seized, plus a penalty'], ['Forced selling', 'Seized collateral hits the market']];
  const P = [[330, 120], [1370, 120], [1370, 420], [330, 420]];
  const nodes = n.map(([t, s], i) => `<g transform="translate(${P[i][0] - 250},${P[i][1] - 70})"><rect width="500" height="140" rx="20" fill="#fff" stroke="${i === 2 ? C.orange : C.line}" stroke-width="${i === 2 ? 3 : 1.5}"/>
    <text x="30" y="60" font-size="30" font-weight="700" fill="${C.ink}" font-family="Inter">${t}</text><text x="30" y="100" font-size="21" fill="${C.text2}" font-family="Inter">${s}</text></g>`).join('');
  const seg = (a, b) => `<path d="M${a[0]},${a[1]} L${b[0]},${b[1]}" stroke="${C.blue}" stroke-width="4" marker-end="url(#al)"/>`;
  return lightShell(1800, 900, 'The liquidation cascade', 'Why buffers matter: one leveraged position can feed a market-wide loop',
    `<svg width="100%" height="100%" viewBox="0 0 ${W} ${H}"><defs><marker id="al" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0L10,5L0,10z" fill="${C.blue}"/></marker></defs>
    ${seg([585, 120], [1110, 120])}${seg([1370, 195], [1370, 340])}${seg([1115, 420], [590, 420])}${seg([330, 345], [330, 200])}${nodes}
    <g transform="translate(700,215)"><rect width="300" height="110" rx="16" fill="${C.panel}"/><text x="150" y="50" text-anchor="middle" font-size="24" font-weight="800" fill="${C.ink}" font-family="Inter">Defence</text>
    <text x="150" y="84" text-anchor="middle" font-size="19" fill="${C.text2}" font-family="Inter">HF ≥ 2 · act at 1.5</text></g></svg>`);
}

function diagramWallets() {
  const cols = [['Vault', 'lock', 'Long-term holdings', 'Almost never signs · no DeFi approvals', 'Hardware or multisig'],
    ['Operator', 'wallet', 'Active DeFi positions', 'Verified protocols only', 'Hardware'],
    ['Burner', 'flame', 'Small amounts for anything new', 'Experiments, mints, airdrops', 'Hot wallet']];
  const body = `<div style="display:flex;gap:40px;height:100%;align-items:stretch">${cols.map(([t, ic, a, b, c], i) => `
    <div style="flex:1;background:#fff;border:1.5px solid ${C.line};border-radius:22px;padding:38px 36px;position:relative">
      <div style="width:72px;height:72px;border-radius:18px;background:${C.panel};display:flex;align-items:center;justify-content:center;color:${C.blue}">${icon(ic, 40)}</div>
      <div style="font-size:40px;font-weight:800;margin-top:24px;color:${C.ink}">${t}</div>
      <div style="font-size:24px;color:${C.text};margin-top:14px;font-weight:600">${a}</div>
      <div style="font-size:21px;color:${C.text2};margin-top:10px;line-height:1.4">${b}</div>
      <div style="position:absolute;left:36px;bottom:32px;font-size:19px;color:${C.blue};font-weight:700">${c}</div>
      
    </div>`).join('')}</div>`;
  return lightShell(1800, 720, 'The 3-wallet setup', 'Funds move down only as needed; profits are swept back up. A drained burner costs only the burner.', body);
}

function diagramProfitSources() {
  const S = [['Service fees', 'Swap fees to LPs', 'swap'], ['Interest', 'Lending to borrowers', 'bank'], ['Security rewards', 'Staking', 'shield'],
    ['Structural carry', 'Funding, basis', 'chart'], ['Incentives', 'Emissions, points (only real once sold)', 'sprout']];
  const body = `<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:24px;height:100%">${S.map(([t, s, ic], i) => `
    <div style="background:#fff;border:1.5px solid ${i === 4 ? C.orange : C.line};border-radius:20px;padding:32px 26px;display:flex;flex-direction:column">
      <div style="font-size:60px;font-weight:800;color:${i === 4 ? C.orange : C.blue}">${i + 1}</div>
      <div style="color:${C.blue};margin:14px 0">${icon(ic, 40)}</div>
      <div style="font-size:28px;font-weight:700;color:${C.ink}">${t}</div>
      <div style="font-size:20px;color:${C.text2};margin-top:10px;line-height:1.4">${s}</div></div>`).join('')}</div>`;
  return lightShell(1800, 640, 'Where DeFi returns come from', 'Every strategy is a mix of these five. Price going up is not a strategy.', body);
}

function diagramLadder() {
  const P = [['Elite Intel Community', '$67/mo', 'Daily intel · entry point'], ['Grid Bot Builder', '$997', 'Automated range income'],
    ['Grid Bot Elite', '$2,497', 'Institutional + coaching'], ['On-Chain Operator Program', 'from $15,000', 'Course · Live tier above']];
  const body = `<div style="display:flex;align-items:flex-end;gap:26px;height:100%">${P.map(([t, p, s], i) => `
    <div style="flex:1;height:${40 + i * 20}%;background:${i === 3 ? C.brand : '#fff'};color:${i === 3 ? '#fff' : C.ink};border:1.5px solid ${i === 3 ? C.brand : C.line};border-radius:20px 20px 8px 8px;padding:28px;display:flex;flex-direction:column;justify-content:flex-end">
      <div style="font-size:24px;font-weight:700">${t}</div><div style="font-size:40px;font-weight:800;margin-top:8px">${p}</div>
      <div style="font-size:19px;opacity:.75;margin-top:6px">${s}</div></div>`).join('')}</div>`;
  return lightShell(1800, 820, 'Product ladder', 'The program sits at the top; Module 9 cross-sells back into Grid Bot Builder.', body);
}

function diagramFunnel() {
  return lightShell(1800, 700, 'High-ticket sales path', 'Cold traffic never goes straight to a $15,000 checkout',
    flowBoxes([['Traffic', 'Ads · email · GBB cross-sell', 'users'], ['Application', 'Capital, experience, goals · scored', 'book'],
      ['Call', 'vip-defi-consult Calendly', 'video'], ['Checkout', 'Per-buyer link with UTM tracking', 'lock'], ['Onboarding', 'Module 1 + wallet setup', 'check']],
      false, { w: 296, h: 250, gap: 48 }) +
    `<div style="position:absolute;left:0;right:0;bottom:-10px;text-align:center;font-size:23px;color:${C.text2}">Not qualified at application → nurture sequence + Elite Intel Community trial</div>`);
}

function diagramAmmFlow() {
  return lightShell(1800, 640, 'How a constant-product swap is priced', 'x · y = k stays constant; the bigger the trade relative to reserves, the worse the price',
    flowBoxes([['Reserves', 'x ETH · y USDC · k = x·y'], ['Trader adds Δx', 'New x′ = x + Δx'], ['Pool solves y′', 'y′ = k ÷ x′'],
      ['Trader receives', 'Δy = y − y′'], ['Price impact', 'Larger Δx vs reserves = worse fill']], false, { w: 296, h: 230, gap: 48 }));
}

// ---------- charts (light, static print; single series unless stated) ----------
function axisFrame(W, H, m, xTicks, yTicks, xs, ys, xLabel, yLabel, fmtX, fmtY) {
  const g = yTicks.map(v => `<line x1="${m.l}" x2="${W - m.r}" y1="${ys(v)}" y2="${ys(v)}" stroke="${v === 0 ? '#9aa3ad' : '#E6EAF0'}" stroke-width="${v === 0 ? 1.5 : 1}"/>
    <text x="${m.l - 14}" y="${ys(v) + 7}" text-anchor="end" font-size="20" fill="${C.text2}" font-family="Inter">${fmtY(v)}</text>`).join('');
  const x = xTicks.map(v => `<text x="${xs(v)}" y="${H - m.b + 34}" text-anchor="middle" font-size="20" fill="${C.text2}" font-family="Inter">${fmtX(v)}</text>`).join('');
  return `${g}${x}<text x="${(m.l + W - m.r) / 2}" y="${H - 8}" text-anchor="middle" font-size="20" fill="${C.text2}" font-family="Inter">${xLabel}</text>
    <text transform="translate(22,${(m.t + H - m.b) / 2}) rotate(-90)" text-anchor="middle" font-size="20" fill="${C.text2}" font-family="Inter">${yLabel}</text>`;
}
const dot = (x, y, col = C.blue) => `<circle cx="${x}" cy="${y}" r="7" fill="${col}" stroke="${C.surface}" stroke-width="2.5"/>`;
const label = (x, y, t, anchor = 'start', w = 700) => `<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="21" font-weight="${w}" fill="${C.text}" font-family="Inter">${t}</text>`;

function chartIL() {
  const W = 1672, H = 600, m = { l: 100, r: 40, t: 20, b: 70 };
  const lx = v => Math.log(v), x0 = lx(0.2), x1 = lx(5);
  const xs = v => m.l + (lx(v) - x0) / (x1 - x0) * (W - m.l - m.r);
  const ys = v => m.t + (-v) / 30 * (H - m.t - m.b);
  const il = r => (2 * Math.sqrt(r) / (1 + r) - 1) * 100;
  let d = '';
  for (let i = 0; i <= 300; i++) { const r = Math.exp(x0 + (x1 - x0) * i / 300); d += `${i ? 'L' : 'M'}${xs(r).toFixed(1)},${ys(il(r)).toFixed(1)}`; }
  // [ratio, anchor, dx, dy]: labels sit on the empty side of the curve.
  const pts = [[0.5, 'end', -16, -16], [1.5, 'start', 16, -22], [2, 'start', 16, -14], [3, 'start', 16, -14], [5, 'end', -18, 34]];
  const marks = pts.map(([r, a, dx, dy]) => `${dot(xs(r), ys(il(r)))}${label(xs(r) + dx, ys(il(r)) + dy, `${r}× → ${il(r).toFixed(1)}%`, a)}`).join('');
  return lightShell(1800, 820, 'Impermanent loss vs simply holding', '50/50 constant-product pool, before fees. Same loss for the same ratio up or down (0.5× = 2×).',
    `<svg width="100%" height="100%" viewBox="0 0 ${W} ${H}">
    ${axisFrame(W, H, m, [0.2, 0.5, 1, 2, 3, 5], [0, -5, -10, -15, -20, -25, -30], xs, ys, 'Price change (new ÷ entry, log scale)', 'Loss vs holding', v => `${v}×`, v => `${v}%`)}
    <path d="${d}" fill="none" stroke="${C.blue}" stroke-width="3" stroke-linejoin="round"/>${marks}</svg>`);
}

function chartAMM() {
  const W = 1672, H = 600, m = { l: 130, r: 40, t: 20, b: 70 }, k = 30e6;
  const X0 = 80, X1 = 140, Y0 = 200000, Y1 = 400000;
  const xs = v => m.l + (v - X0) / (X1 - X0) * (W - m.l - m.r), ys = v => m.t + (Y1 - v) / (Y1 - Y0) * (H - m.t - m.b);
  let d = '';
  for (let x = X0; x <= X1; x += 0.5) d += `${x === X0 ? 'M' : 'L'}${xs(x).toFixed(1)},${ys(k / x).toFixed(1)}`;
  const A = [100, 300000], B = [110, k / 110];
  const tan = x => 300000 - 3000 * (x - 100);
  return lightShell(1800, 820, 'The x · y = k curve: why size costs you', 'Pool of 100 ETH / 300,000 USDC. Swapping in 10 ETH returns ≈ 27,273 USDC, not 30,000.',
    `<svg width="100%" height="100%" viewBox="0 0 ${W} ${H}">
    ${axisFrame(W, H, m, [80, 90, 100, 110, 120, 130, 140], [200000, 250000, 300000, 350000, 400000], xs, ys, 'ETH in pool (x)', 'USDC in pool (y)', v => v, v => `${v / 1000}k`)}
    <path d="M${xs(85)},${ys(tan(85))} L${xs(118)},${ys(tan(118))}" stroke="${C.muted}" stroke-width="2" stroke-dasharray="8 7"/>
    <path d="${d}" fill="none" stroke="${C.blue}" stroke-width="3"/>
    <path d="M${xs(A[0])},${ys(A[1])} H${xs(B[0])}" stroke="${C.orange}" stroke-width="3"/>
    <path d="M${xs(B[0])},${ys(A[1])} V${ys(B[1])}" stroke="${C.orange}" stroke-width="3"/>
    ${dot(xs(A[0]), ys(A[1]))}${dot(xs(B[0]), ys(B[1]), C.orange)}
    ${label(xs(A[0]) - 16, ys(A[1]) + 34, 'A', 'end', 800)}${label(xs(B[0]) - 16, ys(B[1]) + 34, 'B', 'end', 800)}
    ${label(xs(139), ys(385000), 'A · Before: spot price 3,000 USDC/ETH (dashed slope)', 'end')}
    ${label(xs(105), ys(A[1]) - 16, '+10 ETH in', 'middle', 600)}
    ${label(xs(B[0]) + 18, ys((A[1] + B[1]) / 2) + 8, '−27,273 USDC out', 'start', 600)}
    ${label(xs(82), ys(212000), 'B · After: effective price 2,727 USDC/ETH (−9.1% vs spot)')}
    </svg>`);
}

function chartLoop() {
  const W = 1672, H = 600, m = { l: 100, r: 40, t: 20, b: 70 };
  const xs = v => m.l + v / 8 * (W - m.l - m.r), ys = v => m.t + (12 - v) / 18 * (H - m.t - m.b);
  const net = b => 10.5 - 2 * b;
  return lightShell(1800, 820, 'Leveraged loop: the spread is everything', '3× loop on 3.5% collateral yield. Net APY on equity = 3.5% × 3 − borrow rate × 2.',
    `<svg width="100%" height="100%" viewBox="0 0 ${W} ${H}">
    <rect x="${xs(5.25)}" y="${ys(0)}" width="${xs(8) - xs(5.25)}" height="${ys(-6) - ys(0)}" fill="#E6EAF0" opacity=".7"/>
    ${axisFrame(W, H, m, [0, 1, 2, 3, 4, 5, 6, 7, 8], [-6, -3, 0, 3, 6, 9, 12], xs, ys, 'Borrow rate (%)', 'Net APY on equity (%)', v => `${v}%`, v => `${v}%`)}
    <path d="M${xs(0)},${ys(3.5)} H${xs(8)}" stroke="${C.orange}" stroke-width="2.5" stroke-dasharray="10 8"/>
    <path d="M${xs(0)},${ys(net(0))} L${xs(8)},${ys(net(8))}" stroke="${C.blue}" stroke-width="3"/>
    ${dot(xs(2.5), ys(net(2.5)))}${label(xs(2.5) + 16, ys(net(2.5)) - 12, '2.5% borrow → 5.5% net')}
    ${dot(xs(3.5), ys(3.5), C.orange)}${label(xs(3.5) + 16, ys(3.5) - 14, 'Above 3.5%: leverage adds nothing')}
    ${dot(xs(5.25), ys(0))}${label(xs(5.25) + 16, ys(0) - 14, '5.25%: return wiped out')}
    ${label(xs(8) - 14, ys(3.5) + 30, 'Unlevered 3.5% (dashed)', 'end', 600)}
    ${label(xs(5.45), ys(-4.6), 'Losing money', 'start', 600)}
    </svg>`);
}

// ---------- registry ----------
const ASSETS = [
  ['store/icon-1024.png', 1024, 1024, storeIcon],
  ['store/banner-1920x1080.png', 1920, 1080, storeBanner],
  ['store/gallery-01-curriculum.png', 1920, 1080, galleryCurriculum],
  ['store/gallery-02-research-loop.png', 1920, 1080, galleryLoop],
  ['store/gallery-03-strategy-levels.png', 1920, 1080, galleryLevels],
  ['store/gallery-04-grid-vs-lp.png', 1920, 1080, galleryGridLp],
  ['store/gallery-05-whats-included.png', 1920, 1080, galleryIncluded],
  ...MODULES.map(m => [`modules/module-${String(m.n).padStart(2, '0')}.png`, 1600, 500, () => moduleBanner(m)]),
  ['diagrams/research-loop.png', 1800, 640, () => lightShell(1800, 640, 'The 6-step research loop', 'Run every protocol through it before any capital moves', loopSvg(false))],
  ['diagrams/strategy-levels.png', 1800, 860, () => lightShell(1800, 860, 'The strategy library', '16 strategies in 5 levels', levelsHtml(false))],
  ['diagrams/grid-vs-lp.png', 1800, 860, () => lightShell(1800, 860, 'Grid bot vs concentrated LP', 'Same range, almost the same inventory path', gridLpSvg(false))],
  ['diagrams/liquidation-cascade.png', 1800, 900, diagramLiquidation],
  ['diagrams/three-wallets.png', 1800, 720, diagramWallets],
  ['diagrams/profit-sources.png', 1800, 640, diagramProfitSources],
  ['diagrams/product-ladder.png', 1800, 820, diagramLadder],
  ['diagrams/sales-funnel.png', 1800, 700, diagramFunnel],
  ['diagrams/amm-swap-flow.png', 1800, 640, diagramAmmFlow],
  ['charts/impermanent-loss.png', 1800, 820, chartIL],
  ['charts/amm-curve.png', 1800, 820, chartAMM],
  ['charts/loop-spread.png', 1800, 820, chartLoop],
];

(async () => {
  fs.mkdirSync(RENDER, { recursive: true });
  const only = process.argv[2];
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  // Store uploads at exact pixel size; document images at 2x for print sharpness.
  const pages = { 1: await browser.newPage({ deviceScaleFactor: 1 }), 2: await browser.newPage({ deviceScaleFactor: 2 }) };
  for (const [rel, w, h, fn] of ASSETS) {
    if (only && !rel.includes(only)) continue;
    const page = pages[rel.startsWith('store/') ? 1 : 2];
    const file = path.join(RENDER, rel.replace(/\//g, '_') + '.html');
    fs.writeFileSync(file, fn());
    await page.setViewportSize({ width: w, height: h });
    await page.goto(`file://${file}`);
    await page.evaluate(() => document.fonts.ready);
    const out = path.join(OUT, rel);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    await (await page.$('#root')).screenshot({ path: out });
    console.log('wrote', path.relative(path.dirname(OUT), out));
  }
  await browser.close();
})();
