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
  compass: '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
  target: '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
  umbrella: '<path d="M3 12a9 9 0 0118 0z"/><path d="M12 12v7a2 2 0 01-4 0"/>',
  vault: '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="12" cy="12" r="4"/><path d="M12 8v1.5M12 14.5V16M8 12h1.5M14.5 12H16M6 20v1.5M18 20v1.5"/>',
  coins: '<ellipse cx="9" cy="7" rx="6" ry="2.5"/><path d="M3 7v4c0 1.4 2.7 2.5 6 2.5s6-1.1 6-2.5V7"/><path d="M9 16.5c-3.3 0-6-1.1-6-2.5"/><path d="M3 11v5c0 1.4 2.7 2.5 6 2.5 1 0 2-.1 2.8-.3"/><circle cx="17" cy="16" r="4.5"/>',
  bot: '<rect x="4" y="8" width="16" height="12" rx="3"/><path d="M12 4v4"/><circle cx="12" cy="3.5" r="1"/><circle cx="9" cy="13.5" r="1.3"/><circle cx="15" cy="13.5" r="1.3"/><path d="M9.5 17h5"/>',
};
const icon = (name, size = 24, color = 'currentColor', sw = 1.8) =>
  `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round">${ICON[name]}</svg>`;

const MODULES = [
  { n: 0, t: 'Crypto From Zero', o: 'From never owning crypto to a secured wallet, a first transfer and a first DeFi step.', i: 'compass', l: 8 },
  { n: 1, t: 'Foundations & Safety', o: 'Set up and use a wallet safely. Know what can go irreversibly wrong.', i: 'shield', l: 9 },
  { n: 2, t: 'Trading On-Chain', o: 'Swap and provide liquidity deliberately: price impact, IL, MEV.', i: 'swap', l: 8 },
  { n: 3, t: 'Lending & Leverage', o: 'Borrow against collateral with a buffer and a written defence plan.', i: 'bank', l: 7 },
  { n: 4, t: 'Yield', o: 'Split any APY into organic vs subsidised, and name the risk being paid for.', i: 'sprout', l: 8 },
  { n: 5, t: 'Infrastructure Risk', o: 'Map every bridge, oracle, L2 and contract a position depends on.', i: 'layers', l: 8 },
  { n: 6, t: 'Protocol Research', o: 'Complete a full due-diligence file on a real protocol.', i: 'search', l: 7 },
  { n: 7, t: 'On-Chain Analytics', o: 'Read on-chain data without over-interpreting it.', i: 'chart', l: 9 },
  { n: 8, t: 'The DeFi Operating System', o: 'Portfolio plan with risk buckets, limits and an emergency plan.', i: 'cog', l: 7 },
  { n: 9, t: 'DeFi vs Grid Bots', o: 'Choose the right tool for the market, and run both as one system.', i: 'grid', l: 3 },
  { n: 10, t: 'Advanced Yield Engineering', o: 'Fixed, hedged and structured yield, and exactly what each is short.', i: 'target', l: 9 },
  { n: 11, t: 'Hedging & Risk Engineering', o: 'Hedge unwanted risk, stress-test the book, run an incident plan.', i: 'umbrella', l: 5 },
  { n: 12, t: 'Operate as Your Own Bank', o: 'Balance sheet, custody, credit line, liquidity ladder, records.', i: 'vault', l: 8 },
  { n: 13, t: 'The Income Engine', o: 'Risk-adjusted income and a payout policy you can sustain.', i: 'coins', l: 5 },
  { n: 14, t: 'Automation & Mastery', o: 'Monitor, automate safely, and complete the operator capstone.', i: 'bot', l: 6 },
];
const STAGES = [
  ['0', 'Zero', [0], 'Open an account, buy, set up a wallet, first transfer'],
  ['1', 'Foundations', [1, 2], 'Protect a wallet, swap and LP deliberately'],
  ['2', 'Practitioner', [3, 4, 5], 'Borrow, earn yield, map infrastructure risk'],
  ['3', 'Analyst', [6, 7], 'Research any protocol, read on-chain data'],
  ['4', 'Strategist', [8, 9, 10, 11], '30 strategies, fixed & hedged yield, stress tests'],
  ['5', 'Operator', [12, 13, 14], 'Run your own on-chain bank and income engine'],
];

const BASE_CSS = `
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: Inter, sans-serif; -webkit-font-smoothing: antialiased; }
  .mono { font-family: 'JetBrains Mono', monospace; }
  .dark { background: radial-gradient(120% 90% at 85% 0%, #1d4a78 0%, ${C.navy} 38%, ${C.ink} 100%); color: #fff; position: relative; overflow: hidden; }
  .transparent { background: transparent; position: relative; overflow: hidden; }
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

// ---------- logo system ----------
// Mark: two interlocked chain rings (over-under) inside a hexagonal block,
// with node dots on the vertices. Works on dark (white + teal) and light (navy + blue).
let logoId = 0;
function logoMark(size, { dark = true, nodes = true } = {}) {
  const id = `lg${logoId++}`;
  const ringA = dark ? '#ffffff' : C.ink;
  const hex = [0, 1, 2, 3, 4, 5].map(i => { const a = Math.PI / 6 + i * Math.PI / 3; return [100 + 88 * Math.cos(a), 100 + 88 * Math.sin(a)]; });
  const hexPath = hex.map(([x, y], i) => `${i ? 'L' : 'M'}${x.toFixed(2)},${y.toFixed(2)}`).join('') + 'Z';
  return `<svg width="${size}" height="${size}" viewBox="0 0 200 200">
    <defs>
      <linearGradient id="${id}g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${dark ? C.aquaDark : '#14a874'}"/><stop offset="1" stop-color="${dark ? C.blueDark : C.blue}"/></linearGradient>
      <clipPath id="${id}c"><rect x="86" y="58" width="28" height="30"/></clipPath>
      ${dark ? `<filter id="${id}f" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6"/></filter>` : ''}
    </defs>
    ${dark ? `<path d="${hexPath}" fill="none" stroke="url(#${id}g)" stroke-width="10" opacity=".45" filter="url(#${id}f)"/>` : ''}
    <path d="${hexPath}" fill="${dark ? 'rgba(255,255,255,.03)' : 'none'}" stroke="url(#${id}g)" stroke-width="7" stroke-linejoin="round"/>
    ${nodes ? hex.map(([x, y], i) => `<circle cx="${x.toFixed(2)}" cy="${y.toFixed(2)}" r="${i % 2 ? 6 : 8.5}" fill="${i % 2 ? (dark ? C.ink : C.surface) : `url(#${id}g)`}" stroke="url(#${id}g)" stroke-width="4"/>`).join('') : ''}
    <circle cx="78" cy="100" r="33" fill="none" stroke="${ringA}" stroke-width="13"/>
    <circle cx="122" cy="100" r="33" fill="none" stroke="url(#${id}g)" stroke-width="13"/>
    <circle cx="78" cy="100" r="33" fill="none" stroke="${ringA}" stroke-width="13" clip-path="url(#${id}c)"/>
  </svg>`;
}
const brandMark = (size = 40, dark = true) => logoMark(size, { dark, nodes: size >= 60 });
function wordmark(s = 22, dark = true) {
  return `<div style="display:flex;align-items:center;gap:${s * 0.6}px">${logoMark(s * 3, { dark, nodes: s >= 26 })}
    <div style="line-height:1"><div style="font-weight:800;font-size:${s}px;letter-spacing:.06em;color:${dark ? '#fff' : C.ink}">ON-CHAIN <span style="color:${dark ? C.aquaDark : C.blue}">OPERATOR</span></div>
    <div style="font-weight:600;font-size:${s * 0.5}px;letter-spacing:.42em;margin-top:${s * 0.3}px;color:${dark ? 'rgba(255,255,255,.6)' : C.text2}">PROGRAM</div></div></div>`;
}
function lockupStacked(scale = 1, dark = true) {
  return `<div style="display:flex;flex-direction:column;align-items:center">${logoMark(540 * scale, { dark })}
    <div style="font-weight:800;font-size:${86 * scale}px;letter-spacing:.14em;margin-top:${6 * scale}px;color:${dark ? '#fff' : C.ink}">ON-CHAIN</div>
    <div style="font-weight:800;font-size:${60 * scale}px;letter-spacing:.34em;margin-top:${6 * scale}px;background:linear-gradient(90deg,${C.aquaDark},${C.blueDark});-webkit-background-clip:text;color:transparent">OPERATOR</div>
    <div style="font-weight:600;font-size:${22 * scale}px;letter-spacing:.6em;margin-top:${18 * scale}px;color:${dark ? 'rgba(255,255,255,.6)' : C.text2}">PROGRAM</div></div>`;
}
function brandAsset(kind) {
  if (kind === 'icon') return page(1024, 1024, 'dark', `${network(1024, 1024, 11, 30, 0.2)}
    <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center">${lockupStacked(1)}</div>`);
  if (kind === 'mark-dark') return page(1024, 1024, 'dark', `${network(1024, 1024, 4, 26, 0.18)}
    <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center">${logoMark(760)}</div>`);
  if (kind === 'mark-transparent-light') return page(1024, 1024, 'transparent', `<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center">${logoMark(900, { dark: false })}</div>`);
  if (kind === 'mark-transparent') return page(1024, 1024, 'transparent', `<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center">${logoMark(900)}</div>`);
  if (kind === 'horizontal-dark') return page(1800, 520, 'dark', `${network(1800, 520, 6, 30, 0.14)}
    <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center">${wordmark(84)}</div>`);
  if (kind === 'horizontal-light') return page(1800, 520, 'light', `<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center">${wordmark(84, false)}</div>`);
  if (kind === 'favicon') return page(256, 256, 'dark', `<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center">${logoMark(230, { nodes: false })}</div>`);
  if (kind === 'guide') return page(1920, 1080, 'dark', `${network(1920, 1080, 8, 40, 0.1)}
    <div style="position:absolute;left:110px;top:90px;display:flex;justify-content:space-between;right:110px;align-items:center">${wordmark(20)}<div class="eyebrow" style="color:${C.aquaDark};font-size:20px">Brand guide</div></div>
    <div style="position:absolute;left:110px;top:220px;width:760px;height:700px;border-radius:28px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.14);display:flex;align-items:center;justify-content:center">${lockupStacked(0.95)}</div>
    <div style="position:absolute;left:920px;top:220px;right:110px;height:330px;border-radius:28px;background:${C.surface};display:flex;align-items:center;justify-content:center">${wordmark(52, false)}</div>
    <div style="position:absolute;left:920px;top:590px;right:110px;display:flex;gap:18px">
      ${[['Ink', C.ink], ['Navy', C.navy], ['Brand', C.brand], ['Teal', C.aquaDark], ['Blue', C.blue], ['Orange', C.orange]].map(([n, c]) => `<div style="flex:1"><div style="height:120px;border-radius:16px;background:${c};border:1px solid rgba(255,255,255,.2)"></div><div style="font-size:20px;margin-top:10px;font-weight:700">${n}</div><div class="mono" style="font-size:16px;color:rgba(255,255,255,.65)">${c}</div></div>`).join('')}
    </div>
    <div style="position:absolute;left:920px;top:830px;right:110px;display:flex;gap:40px;align-items:flex-end">
      <div><div style="font-size:64px;font-weight:800">Aa</div><div style="font-size:18px;color:rgba(255,255,255,.65)">Inter · 400–800</div></div>
      <div><div class="mono" style="font-size:44px">x·y=k</div><div style="font-size:18px;color:rgba(255,255,255,.65)">JetBrains Mono · figures & formulas</div></div>
      <div style="font-size:18px;color:rgba(255,255,255,.65);max-width:420px;line-height:1.4">Mark: two interlocked rings (a chain) inside a block. Keep clear space of one ring's width. Never recolour the rings or stretch the mark.</div>
    </div>`);
}

// ---------- store assets (dark) ----------
function storeIcon() { return brandAsset('icon'); }

function storeBanner() {
  const w = 1920, h = 1080;
  const stats = [['15', 'modules'], ['107', 'lessons'], ['30', 'strategy playbooks'], ['2', 'capstones']];
  return page(w, h, 'dark', `${network(w, h, 3, 60)}
  <div style="position:absolute;right:110px;top:200px">${logoMark(600)}</div>
  <div style="position:absolute;left:120px;top:100px">${wordmark(30)}</div>
  <div style="position:absolute;left:120px;top:330px;width:1150px">
    <div class="eyebrow" style="color:${C.aquaDark};font-size:24px">Zero to operator · the risk-first DeFi program</div>
    <div style="font-size:104px;font-weight:800;line-height:1.02;margin-top:26px;letter-spacing:-.02em">From zero to your<br>own <span style="color:${C.aquaDark}">on-chain bank.</span></div>
    <div style="font-size:32px;line-height:1.42;color:rgba(255,255,255,.82);margin-top:34px;width:1020px">DeFi from first principles to professional strategies. Build a risk-adjusted income engine and run your capital like a bank, with written policy for every position.</div>
  </div>
  <div style="position:absolute;left:120px;bottom:110px;display:flex;gap:26px">
    ${stats.map(([a, b]) => `<div style="padding:22px 34px;border:1px solid rgba(255,255,255,.18);border-radius:18px;background:rgba(255,255,255,.05)">
      <div style="font-size:52px;font-weight:800">${a}</div><div style="font-size:22px;color:rgba(255,255,255,.7)">${b}</div></div>`).join('')}
  </div>
  <div class="foot" style="padding:22px 120px"><span>${DISCLAIMER}</span><span>Course · Live tier</span></div>`);
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
  const cards = MODULES.map(m => `<div style="border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.05);border-radius:18px;padding:22px 22px">
    <div style="display:flex;align-items:center;gap:14px"><div style="flex:none;width:50px;height:50px;border-radius:14px;background:rgba(46,230,166,.14);display:flex;align-items:center;justify-content:center;color:${C.aquaDark}">${icon(m.i, 28)}</div>
    <div style="font-size:15px;color:rgba(255,255,255,.6);font-weight:700;letter-spacing:.06em">MODULE ${m.n} · ${m.l} LESSONS</div></div>
    <div style="font-size:25px;font-weight:700;margin-top:14px;line-height:1.2">${m.t}</div></div>`).join('');
  return galleryShell('Curriculum', '15 modules · 107 lessons · 2 capstones',
    `<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:20px">${cards}</div>`, 5);
}

function pathHtml(dark) {
  const fg = dark ? '#fff' : C.ink, sub = dark ? 'rgba(255,255,255,.72)' : C.text2, acc = dark ? C.aquaDark : C.blue;
  return `<div style="display:flex;align-items:flex-end;gap:18px;height:100%">
    ${STAGES.map(([n, name, mods, can], i) => `<div style="flex:1;height:${34 + i * 13}%;border-radius:20px 20px 8px 8px;padding:24px 22px;display:flex;flex-direction:column;justify-content:flex-end;
      background:${dark ? `rgba(46,230,166,${0.05 + i * 0.035})` : (i === 5 ? C.brand : '#fff')};border:1.5px solid ${dark ? 'rgba(46,230,166,.35)' : (i === 5 ? C.brand : C.line)};color:${!dark && i === 5 ? '#fff' : fg}">
      <div style="font-size:18px;font-weight:700;letter-spacing:.12em;color:${!dark && i === 5 ? 'rgba(255,255,255,.75)' : acc}">STAGE ${n}</div>
      <div style="font-size:32px;font-weight:800;margin-top:6px">${name}</div>
      <div style="font-size:18px;margin-top:8px;opacity:.85">Modules ${mods.length > 1 ? `${mods[0]}–${mods[mods.length - 1]}` : mods[0]}</div>
      <div style="font-size:19px;margin-top:10px;line-height:1.35;color:${!dark && i === 5 ? 'rgba(255,255,255,.85)' : sub}">${can}</div></div>`).join('')}
  </div>`;
}
function galleryPath() { return galleryShell('The path', 'From knowing nothing to operating your own bank', pathHtml(true), 23); }

function ownBankHtml(dark) {
  const fg = dark ? '#fff' : C.ink, sub = dark ? 'rgba(255,255,255,.75)' : C.text2, acc = dark ? C.aquaDark : C.blue;
  const card = dark ? 'rgba(255,255,255,.06)' : '#fff', line = dark ? 'rgba(255,255,255,.18)' : C.line;
  const pillars = [['vault', 'Custody', 'Multisig vault, limits, allowlists'], ['bank', 'Credit line', 'Borrow against assets under policy'],
    ['coins', 'Lending desk', 'Supply, curate, price credit risk'], ['layers', 'Treasury', 'Liquidity ladder T0–T3']];
  return `<div style="display:flex;flex-direction:column;height:100%;gap:18px">
    <div style="height:26%;clip-path:polygon(50% 0,100% 100%,0 100%);background:${dark ? 'rgba(46,230,166,.16)' : C.brand};display:flex;align-items:flex-end;justify-content:center;padding-bottom:18px">
      <div style="text-align:center;color:${dark ? '#fff' : '#fff'}"><div style="font-size:34px;font-weight:800">Your on-chain bank</div><div style="font-size:20px;opacity:.85">Income engine · payout policy</div></div></div>
    <div style="flex:1;display:flex;gap:22px">
      ${pillars.map(([ic, tt, s]) => `<div style="flex:1;border-radius:16px;background:${card};border:1.5px solid ${line};padding:26px 24px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
        <div style="color:${acc}">${icon(ic, 46)}</div><div style="font-size:30px;font-weight:800;margin-top:14px;color:${fg}">${tt}</div>
        <div style="font-size:20px;margin-top:8px;color:${sub};line-height:1.35">${s}</div></div>`).join('')}
    </div>
    <div style="height:13%;border-radius:12px;background:${dark ? 'rgba(255,255,255,.08)' : C.panel};border:1.5px solid ${line};display:flex;align-items:center;justify-content:center;gap:12px;font-size:24px;font-weight:700;color:${fg}">
      <span style="color:${acc}">${icon('book', 30)}</span>Books · records · succession</div>
  </div>`;
}
function galleryOwnBank() { return galleryShell('Stage 5 · Operator', 'Operate as your own bank', ownBankHtml(true), 29); }

function galleryLoop() { return galleryShell('Method', 'The 6-step research loop', loopSvg(true), 9); }
function galleryLevels() { return galleryShell('Strategy library', '30 strategies, 7 levels, risk first', levelsHtml(true), 13); }
function galleryGridLp() { return galleryShell('Module 9', 'A DeFi LP is an on-chain grid bot', gridLpSvg(true), 17); }

function galleryIncluded() {
  const col = (title, sub, items, accent) => `<div style="flex:1;border:1px solid ${accent ? C.aquaDark : 'rgba(255,255,255,.16)'};background:rgba(255,255,255,${accent ? '.08' : '.04'});border-radius:24px;padding:44px 48px">
    <div class="eyebrow" style="color:${accent ? C.aquaDark : 'rgba(255,255,255,.65)'};font-size:20px">${sub}</div>
    <div style="font-size:48px;font-weight:800;margin:10px 0 28px">${title}</div>
    ${items.map(([ic, t]) => `<div style="display:flex;gap:20px;align-items:center;margin:26px 0;font-size:32px;color:rgba(255,255,255,.92)"><span style="color:${C.aquaDark}">${icon(ic, 36)}</span>${t}</div>`).join('')}
  </div>`;
  return galleryShell('What\'s included', 'Two ways to join', `<div style="display:flex;gap:36px;height:100%">
    ${col('Course', 'Self-paced', [['book', '15 modules, 107 lessons, zero to operator'], ['target', '30 strategy playbooks'], ['search', 'Due-diligence & bank-policy worksheets'], ['chart', 'Strategy, income & bank calculators'], ['lock', 'Analyst + operator capstones']], false)}
    ${col('Live', 'Course + coaching', [['check', 'Everything in Course'], ['video', 'Live group sessions'], ['users', 'Capstone & portfolio reviews'], ['vault', 'Own-bank policy review'], ['coins', 'Income-engine & payout review']], true)}
  </div>`, 19);
}

// ---------- module banners ----------
function moduleBanner(m) {
  const w = 1600, h = 500;
  return page(w, h, 'dark', `${network(w, h, 30 + m.n, 34, 0.14)}
  <div style="position:absolute;left:80px;top:0;bottom:0;display:flex;align-items:center;gap:40px">
    <div style="width:340px;flex:none;font-size:${m.n > 9 ? 200 : 230}px;letter-spacing:-.04em;font-weight:800;line-height:1;color:transparent;-webkit-text-stroke:3px rgba(255,255,255,.35)">${String(m.n).padStart(2, '0')}</div>
    <div style="width:820px">
      <div class="eyebrow" style="color:${C.aquaDark};font-size:22px">Module ${m.n} · ${m.l} lessons</div>
      <div style="font-size:${m.t.length > 22 ? 54 : 66}px;font-weight:800;margin-top:12px;letter-spacing:-.015em;white-space:nowrap">${m.t}</div>
      <div style="font-size:28px;color:rgba(255,255,255,.8);margin-top:18px;line-height:1.35">${m.o}</div>
    </div>
  </div>
  <div style="position:absolute;right:90px;top:50%;transform:translateY(-50%);width:170px;height:170px;border-radius:40px;background:rgba(46,230,166,.12);border:1px solid rgba(46,230,166,.4);display:flex;align-items:center;justify-content:center;color:${C.aquaDark}">${icon(m.i, 96, 'currentColor', 1.5)}</div>
  <div style="position:absolute;left:80px;bottom:26px;transform:scale(.9);transform-origin:left bottom">${wordmark(14)}</div>`);
}

// ---------- diagrams (light for documents; some reused dark in gallery) ----------
function lightShell(w, h, title, sub, body) {
  return page(w, h, 'light', `
  <div style="position:absolute;left:64px;top:52px;right:64px">
    <div style="font-size:40px;font-weight:800;color:${C.ink};letter-spacing:-.01em">${title}</div>
    ${sub ? `<div style="font-size:22px;color:${C.text2};margin-top:10px">${sub}</div>` : ''}
  </div>
  <div style="position:absolute;left:64px;right:64px;top:${sub ? 170 : 130}px;bottom:70px">${body}</div>
  <div class="foot" style="padding:14px 64px;font-size:14px;align-items:center"><span style="display:flex;align-items:center;gap:10px">${logoMark(30, { dark: false, nodes: false })}On-Chain Operator Program</span><span>${DISCLAIMER}</span></div>`);
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
    ['5', 'Treasury & research', 'Cash management · Accumulation & growth screens'],
    ['6', 'Professional', 'PT/YT fixed rate · Basis · Options · Credit lines · Lending vaults · Hedged restaking'],
    ['7', 'Expert', 'CDP minting · Bribe markets · Perp vaults · Peg arbitrage · Rates positioning']];
  const fg = dark ? '#fff' : C.ink, sub = dark ? 'rgba(255,255,255,.75)' : C.text2;
  return `<div style="display:flex;flex-direction:column;gap:10px;height:100%;justify-content:center">
    ${L.map(([n, t, s], i) => `<div style="display:flex;align-items:center;gap:30px;margin-left:${i * 48}px;padding:8px 30px;border-radius:18px;
      background:${dark ? `rgba(46,230,166,${0.05 + i * 0.03})` : '#fff'};border:1px solid ${dark ? 'rgba(46,230,166,.35)' : C.line}">
      <div style="font-size:46px;font-weight:800;width:60px;color:${dark ? C.aquaDark : C.blue}">${n}</div>
      <div style="font-size:32px;font-weight:700;width:360px;color:${fg}">${t}</div>
      <div style="font-size:22px;color:${sub};white-space:nowrap">${s}</div></div>`).join('')}
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

function diagramCustody() {
  const tiers = [['vault', 'Vault', 'Most of your equity', ['2-of-3 multisig, keys in separate places', 'No DeFi approvals', 'Outflows allowlisted + timelocked']],
    ['wallet', 'Operating', 'Active positions', ['Hardware wallet or limited smart account', 'Verified protocols only', 'Daily spending limit']],
    ['flame', 'Hot', 'Small float', ['Anything new or experimental', 'Refilled on schedule', 'A drain costs only the float']]];
  const body = `<div style="display:flex;flex-direction:column;gap:0;height:100%;justify-content:center">
    ${tiers.map(([ic, t2, h2, rules], i) => `
      <div style="display:flex;align-items:center;gap:28px;background:#fff;border:1.5px solid ${i === 0 ? C.brand : C.line};border-radius:18px;padding:22px 30px;margin:0 ${i * 90}px">
        <div style="width:70px;height:70px;border-radius:18px;background:${i === 0 ? C.brand : C.panel};color:${i === 0 ? '#fff' : C.blue};display:flex;align-items:center;justify-content:center;flex:none">${icon(ic, 38)}</div>
        <div style="width:260px;flex:none"><div style="font-size:32px;font-weight:800;color:${C.ink}">${t2}</div><div style="font-size:20px;color:${C.text2}">${h2}</div></div>
        <div style="display:flex;gap:26px;font-size:20px;color:${C.text}">${rules.map(r => `<div style="display:flex;gap:8px;align-items:center"><span style="color:${C.blue}">${icon('check', 22)}</span>${r}</div>`).join('')}</div>
      </div>
      ${i < 2 ? `<div style="display:flex;justify-content:space-between;padding:10px ${i * 90 + 120}px;font-size:18px;color:${C.text2}"><span>↓ funds move down only as needed</span><span>profits swept back up ↑</span></div>` : ''}`).join('')}
  </div>`;
  return lightShell(1800, 820, 'Custody architecture', 'No single lost device, stolen key or bad signature can drain the bank', body);
}

function diagramLadder2() {
  const T = [['T0', 'Instant', 'Seconds', 'Stablecoins in the operating wallet', '1 month · $5,000', 58],
    ['T1', 'Same day', 'Hours', 'Blue-chip lending, split across 2 protocols', '5 months · $25,000', 72],
    ['T2', 'Term', 'Scheduled', 'PTs maturing when money is needed', 'Next 6–12 months of plans', 86],
    ['T3', 'Growth', 'Days–weeks', 'Strategy positions, LPs, staking', 'The rest, within caps', 100]];
  const body = `<div style="display:flex;flex-direction:column;gap:18px;height:100%;justify-content:center">
    ${T.map(([k, n, acc, what, size, w], i) => `<div style="display:flex;align-items:center;gap:26px">
      <div style="width:90px;font-size:40px;font-weight:800;color:${C.blue}">${k}</div>
      <div style="width:${w}%;background:${i === 0 ? C.brand : '#fff'};color:${i === 0 ? '#fff' : C.ink};border:1.5px solid ${i === 0 ? C.brand : C.line};border-radius:14px;padding:18px 26px;display:flex;gap:30px;align-items:center">
        <div style="width:170px;flex:none"><div style="font-size:26px;font-weight:800">${n}</div><div style="font-size:18px;opacity:.75">${acc}</div></div>
        <div style="font-size:21px;flex:1">${what}</div><div style="font-size:20px;font-weight:700;white-space:nowrap">${size}</div></div></div>`).join('')}
    <div style="font-size:20px;color:${C.text2};margin-left:116px">Refill downward on a schedule. Never fund a T0 need by selling T3 in a bad market. Example: $5,000/month spending.</div>
  </div>`;
  return lightShell(1800, 760, 'The liquidity ladder', 'Match the timing of your assets to the timing of what you owe', body);
}

function chartPT() {
  const W = 1672, H = 600, m = { l: 110, r: 40, t: 20, b: 70 }, r = 0.0863, T = 180;
  const xs = v => m.l + v / T * (W - m.l - m.r), ys = v => m.t + (1.01 - v) / 0.06 * (H - m.t - m.b);
  const pt = d => Math.pow(1 + r, -(T - d) / 365);
  let d = '';
  for (let x = 0; x <= T; x += 1) d += `${x ? 'L' : 'M'}${xs(x).toFixed(1)},${ys(pt(x)).toFixed(1)}`;
  return lightShell(1800, 820, 'Principal tokens pull to par', 'PT bought at 0.96 with 180 days left redeems at 1.00: an 8.63% fixed APY if held to maturity.',
    `<svg width="100%" height="100%" viewBox="0 0 ${W} ${H}">
    ${axisFrame(W, H, m, [0, 30, 60, 90, 120, 150, 180], [0.95, 0.96, 0.97, 0.98, 0.99, 1.0], xs, ys, 'Days since purchase', 'PT price (in underlying)', v => v, v => v.toFixed(2))}
    <path d="M${xs(0)},${ys(1)} H${xs(T)}" stroke="${C.orange}" stroke-width="2.5" stroke-dasharray="10 8"/>
    <path d="${d}" fill="none" stroke="${C.blue}" stroke-width="3"/>
    ${dot(xs(0), ys(pt(0)))}${label(xs(0) + 16, ys(pt(0)) + 34, 'Buy at 0.96')}
    ${dot(xs(T), ys(1), C.orange)}${label(xs(T) - 16, ys(1) - 18, 'Redeem 1:1 at maturity', 'end')}
    ${label(xs(90) + 16, ys(pt(90)) + 36, `Day 90 ≈ ${pt(90).toFixed(3)} (if the implied rate holds)`, 'start', 600)}
    ${label(xs(4), ys(1) - 16, 'Underlying = 1.00 (dashed)', 'start', 600)}
    </svg>`);
}

function chartIncome() {
  const W = 1672, H = 600, m = { l: 120, r: 40, t: 30, b: 70 };
  const steps = [['Headline yield', 26800, 'total'], ['Expected losses', -3500, 'minus'], ['Expected income', 23300, 'total'], ['Retained buffer (30%)', -6990, 'minus'], ['Sustainable payout', 16310, 'total']];
  const ys = v => m.t + (30000 - v) / 30000 * (H - m.t - m.b);
  const bw = 200, gap = (W - m.l - m.r - bw * steps.length) / (steps.length - 1);
  let level = 0, bars = '';
  steps.forEach(([name, v, kind], i) => {
    const x = m.l + i * (bw + gap);
    const top = kind === 'total' ? v : level, bottom = kind === 'total' ? 0 : level + v;
    if (kind === 'total') level = v; else level = level + v;
    const col = kind === 'total' ? C.blue : C.orange;
    bars += `<rect x="${x}" y="${ys(top)}" width="${bw}" height="${ys(bottom) - ys(top)}" rx="4" fill="${col}"/>
      <text x="${x + bw / 2}" y="${ys(top) - 14}" text-anchor="middle" font-size="24" font-weight="800" fill="${C.text}" font-family="Inter">${v < 0 ? '−' : ''}$${Math.abs(v).toLocaleString()}</text>
      <text x="${x + bw / 2}" y="${H - m.b + 34}" text-anchor="middle" font-size="19" fill="${C.text2}" font-family="Inter">${name}</text>`;
    if (i < steps.length - 1) bars += `<line x1="${x + bw}" x2="${x + bw + gap}" y1="${ys(level)}" y2="${ys(level)}" stroke="#9aa3ad" stroke-dasharray="5 5"/>`;
  });
  const grid = [0, 10000, 20000, 30000].map(v => `<line x1="${m.l}" x2="${W - m.r}" y1="${ys(v)}" y2="${ys(v)}" stroke="${v ? '#E6EAF0' : '#9aa3ad'}"/><text x="${m.l - 14}" y="${ys(v) + 7}" text-anchor="end" font-size="20" fill="${C.text2}" font-family="Inter">$${v / 1000}k</text>`).join('');
  return lightShell(1800, 820, 'From headline yield to a sustainable payout', 'Illustrative $500,000 income portfolio (Module 13). Loss rates are assumptions; income is not guaranteed.',
    `<svg width="100%" height="100%" viewBox="0 0 ${W} ${H}">${grid}${bars}</svg>`);
}

function diagramSetupRoadmap() {
  const S = [['users', 'Accounts', 'Password manager, secure email, 2FA'], ['bank', 'Exchange', 'Open, KYC, lock it down'], ['coins', 'First buy', 'A little ETH + USDC, cheapest route'],
    ['wallet', 'Wallet', 'Official install, seed on paper, restore test'], ['swap', 'First transfer', 'Right network, test amount first'], ['target', 'Practice DeFi', 'Testnet, then a tiny real swap'],
    ['shield', 'Security baseline', '10 rules, bookmarks, hardware wallet']];
  const body = `<div style="display:flex;align-items:stretch;gap:0;height:100%">${S.map(([ic, t2, s], i) => `
    <div style="flex:1;display:flex;flex-direction:column;align-items:center;text-align:center;position:relative">
      <div style="width:96px;height:96px;border-radius:50%;background:${i === 6 ? C.brand : '#fff'};border:2px solid ${i === 6 ? C.brand : C.blue};color:${i === 6 ? '#fff' : C.blue};display:flex;align-items:center;justify-content:center;z-index:2">${icon(ic, 44)}</div>
      ${i < 6 ? `<div style="position:absolute;top:47px;left:calc(50% + 48px);right:calc(-50% + 48px);height:3px;background:${C.blue};opacity:.5"></div>` : ''}
      <div style="font-size:18px;font-weight:700;color:${C.blue};margin-top:18px;letter-spacing:.1em">STEP ${i + 1}</div>
      <div style="font-size:28px;font-weight:800;color:${C.ink};margin-top:6px">${t2}</div>
      <div style="font-size:20px;color:${C.text2};margin-top:8px;line-height:1.35;padding:0 10px">${s}</div></div>`).join('')}</div>
    <div style="position:absolute;left:0;right:0;bottom:-6px;text-align:center;font-size:21px;color:${C.text2}">Do it in order, with a small learning amount. Allow 2–3 hours over a few days. Checklist: the Day-1 Setup Kit.</div>`;
  return lightShell(1800, 640, 'Your setup roadmap', 'From zero to ready for Module 1, in seven steps', body);
}

function diagramFirstTransfer() {
  return lightShell(1800, 700, 'Your first transfer: exchange → your wallet', 'The network must match on both sides. Send a small test first.',
    flowBoxes([['Copy address', 'Wallet copy button: never type it', 'wallet'], ['Choose network', 'One your wallet supports, e.g. an L2', 'layers'],
      ['Check address', 'First and last 6 characters, ideally all', 'search'], ['Send a test', '$10 first, wait until it arrives', 'check'],
      ['Send the rest', 'Then allowlist the address', 'lock']], false, { w: 296, h: 250, gap: 48 }) +
    `<div style="position:absolute;left:0;right:0;bottom:-10px;text-align:center;font-size:22px;color:${C.text2}">Keep a little ETH on that network for gas, or you can't move anything.</div>`);
}

function diagramSeedBackup() {
  const col = (good, title, items) => `<div style="flex:1;background:#fff;border:2px solid ${good ? C.blue : C.orange};border-radius:22px;padding:34px 40px">
    <div style="display:flex;align-items:center;gap:14px;color:${good ? C.blue : C.orange}">${icon(good ? 'check' : 'flame', 40)}<div style="font-size:38px;font-weight:800;color:${C.ink}">${title}</div></div>
    ${items.map(x => `<div style="font-size:25px;color:${C.text};margin-top:20px;display:flex;gap:14px;align-items:flex-start"><span style="color:${good ? C.blue : C.orange};font-weight:800">${good ? '✓' : '✕'}</span><span>${x}</span></div>`).join('')}</div>`;
  return lightShell(1800, 640, 'Your seed phrase: do and don\'t', 'The 12–24 words are the wallet. Whoever has them has everything.',
    `<div style="display:flex;gap:40px;height:100%">
      ${col(true, 'Do', ['Write it on paper or stamp it in metal, in order', 'Store it privately, safe from fire and water', 'Keep a second copy elsewhere for larger amounts', 'Test a restore before depositing', 'Use a hardware wallet once the amount matters'])}
      ${col(false, 'Never', ['Type it into any website or form', 'Photograph it or keep it in notes, email or cloud', 'Share it with anyone: no real support will ask', 'Use a phrase that came pre-printed or from someone else', 'Store it next to written instructions on how to use it'])}
    </div>`);
}

function chartLVR() {
  const W = 1672, H = 600, m = { l: 100, r: 40, t: 20, b: 70 };
  const xs = v => m.l + (v - 20) / 100 * (W - m.l - m.r), ys = v => m.t + (20 - v) / 20 * (H - m.t - m.b);
  const lvr = s => s * s / 800; // percent/yr for vol in percent
  let d = '';
  for (let s = 20; s <= 120; s += 1) d += `${s === 20 ? 'M' : 'L'}${xs(s).toFixed(1)},${ys(lvr(s)).toFixed(1)}`;
  return lightShell(1800, 820, 'Loss-versus-rebalancing: what arbitrage costs LPs', 'Full-range x·y=k pool: LVR ≈ σ²/8 of pool value per year. Fees must beat this line.',
    `<svg width="100%" height="100%" viewBox="0 0 ${W} ${H}">
    ${axisFrame(W, H, m, [20, 40, 60, 80, 100, 120], [0, 5, 10, 15, 20], xs, ys, 'Annualised volatility of the pair (%)', 'Cost to LPs (% of pool / yr)', v => `${v}%`, v => `${v}%`)}
    <path d="M${xs(20)},${ys(12)} H${xs(120)}" stroke="${C.orange}" stroke-width="2.5" stroke-dasharray="10 8"/>
    <path d="${d}" fill="none" stroke="${C.blue}" stroke-width="3"/>
    ${dot(xs(80), ys(lvr(80)))}${label(xs(80) - 16, ys(lvr(80)) - 16, '80% vol → 8% LVR', 'end')}
    ${dot(xs(110), ys(lvr(110)))}${label(xs(110) - 16, ys(lvr(110)) - 18, '110% vol → 15.1% LVR', 'end')}
    ${label(xs(22), ys(12) - 14, 'Example fee APR 12% (dashed)', 'start', 600)}
    ${label(xs(24), ys(6.5), 'Below the dashed line: fees beat LVR', 'start', 600)}
    </svg>`);
}

function diagramMEV() {
  return lightShell(1800, 700, 'The MEV supply chain', 'Where your transaction goes, and who can profit from its ordering',
    flowBoxes([['You / wallet', 'Public mempool or private RPC', 'wallet'], ['Searchers', 'Arbitrage, liquidations, backruns, sandwiches', 'search'],
      ['Builders', 'Assemble the most valuable block', 'layers'], ['Relays', 'Pass blocks to validators', 'swap'], ['Proposer', 'Validator picks the highest-paying block', 'shield']],
      false, { w: 296, h: 250, gap: 48 }) +
    `<div style="position:absolute;left:0;right:0;bottom:-10px;text-align:center;font-size:22px;color:${C.text2}">Protect yourself: private/protected RPCs, intent systems, tight slippage, and MEV rebates where offered.</div>`);
}

// ---------- registry ----------
const ASSETS = [
  ['brand/logo-icon-1024.png', 1024, 1024, () => brandAsset('icon')],
  ['brand/logo-mark-dark-1024.png', 1024, 1024, () => brandAsset('mark-dark')],
  ['brand/logo-mark-transparent-dark-1024.png', 1024, 1024, () => brandAsset('mark-transparent')],
  ['brand/logo-mark-transparent-light-1024.png', 1024, 1024, () => brandAsset('mark-transparent-light')],
  ['brand/logo-horizontal-dark.png', 1800, 520, () => brandAsset('horizontal-dark')],
  ['brand/logo-horizontal-light.png', 1800, 520, () => brandAsset('horizontal-light')],
  ['brand/favicon-256.png', 256, 256, () => brandAsset('favicon')],
  ['brand/brand-guide.png', 1920, 1080, () => brandAsset('guide')],
  ['store/icon-1024.png', 1024, 1024, storeIcon],
  ['store/banner-1920x1080.png', 1920, 1080, storeBanner],
  ['store/gallery-01-path-to-mastery.png', 1920, 1080, galleryPath],
  ['store/gallery-02-curriculum.png', 1920, 1080, galleryCurriculum],
  ['store/gallery-03-own-bank.png', 1920, 1080, galleryOwnBank],
  ['store/gallery-04-strategy-levels.png', 1920, 1080, galleryLevels],
  ['store/gallery-05-research-loop.png', 1920, 1080, galleryLoop],
  ['store/gallery-06-grid-vs-lp.png', 1920, 1080, galleryGridLp],
  ['store/gallery-07-whats-included.png', 1920, 1080, galleryIncluded],
  ...MODULES.map(m => [`modules/module-${String(m.n).padStart(2, '0')}.png`, 1600, 500, () => moduleBanner(m)]),
  ['diagrams/setup-roadmap.png', 1800, 640, diagramSetupRoadmap],
  ['diagrams/first-transfer.png', 1800, 700, diagramFirstTransfer],
  ['diagrams/seed-backup.png', 1800, 640, diagramSeedBackup],
  ['diagrams/path-to-mastery.png', 1800, 820, () => lightShell(1800, 820, 'The path to mastery', 'Six stages from knowing nothing to operating your own on-chain bank', pathHtml(false))],
  ['diagrams/own-bank.png', 1800, 900, () => lightShell(1800, 900, 'Operate as your own bank', 'Four pillars on a base of records, under one income policy', ownBankHtml(false))],
  ['diagrams/custody-architecture.png', 1800, 820, diagramCustody],
  ['diagrams/liquidity-ladder.png', 1800, 760, diagramLadder2],
  ['diagrams/research-loop.png', 1800, 640, () => lightShell(1800, 640, 'The 6-step research loop', 'Run every protocol through it before any capital moves', loopSvg(false))],
  ['diagrams/strategy-levels.png', 1800, 900, () => lightShell(1800, 900, 'The strategy library', '30 strategies in 7 levels', levelsHtml(false))],
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
  ['charts/pt-convergence.png', 1800, 820, chartPT],
  ['charts/income-waterfall.png', 1800, 820, chartIncome],
  ['charts/lvr.png', 1800, 820, chartLVR],
  ['diagrams/mev-supply-chain.png', 1800, 700, diagramMEV],
];

module.exports = { C, FONT, BASE_CSS, network, icon, logoMark, wordmark, lockupStacked, DISCLAIMER };

if (require.main === module) (async () => {
  fs.mkdirSync(RENDER, { recursive: true });
  const only = process.argv[2];
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  // Store uploads at exact pixel size; document images at 2x for print sharpness.
  const pages = { 1: await browser.newPage({ deviceScaleFactor: 1 }), 2: await browser.newPage({ deviceScaleFactor: 2 }) };
  for (const [rel, w, h, fn] of ASSETS) {
    if (only && !rel.includes(only)) continue;
    const page = pages[rel.startsWith('store/') || rel.startsWith('brand/') ? 1 : 2];
    const file = path.join(RENDER, rel.replace(/\//g, '_') + '.html');
    fs.writeFileSync(file, fn());
    await page.setViewportSize({ width: w, height: h });
    await page.goto(`file://${file}`);
    await page.evaluate(() => document.fonts.ready);
    const out = path.join(OUT, rel);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    await (await page.$('#root')).screenshot({ path: out, omitBackground: rel.includes('transparent') });
    console.log('wrote', path.relative(path.dirname(OUT), out));
  }
  await browser.close();
})();
