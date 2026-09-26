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
  link: '<path d="M10 14a4 4 0 005.7 0l3-3a4 4 0 00-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 00-5.7 0l-3 3a4 4 0 005.7 5.7l1-1"/>',
  eye: '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
  key: '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M15 8l2 2"/>',
  clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
  code: '<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/>',
  globe: '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.8 3 2.8 15 0 18M12 3c-2.8 3-2.8 15 0 18"/>',
  alert: '<path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18v.5"/>',
  bell: '<path d="M6 16V11a6 6 0 0112 0v5l2 2H4z"/><path d="M10 20a2 2 0 004 0"/>',
  doc: '<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4M9 12h7M9 16h7"/>',
  scale: '<path d="M12 4v16M5 20h14M4 8h16"/><path d="M4 8l-2 6h4zM20 8l-2 6h4z"/>',
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

function chartHF() {
  // 10 ETH collateral, liquidation threshold 0.80. HF = price × 10 × 0.8 ÷ debt.
  const W = 1672, H = 600, m = { l: 100, r: 40, t: 20, b: 70 };
  const xs = v => m.l + (v - 1000) / 3500 * (W - m.l - m.r), ys = v => m.t + (3 - v) / 3 * (H - m.t - m.b);
  const hf = (p, debt) => p * 8 / debt;
  const line = debt => { let d = ''; for (let p = 1000; p <= 4500; p += 25) { const h = Math.min(3, hf(p, debt)); d += `${p === 1000 ? 'M' : 'L'}${xs(p).toFixed(1)},${ys(h).toFixed(1)}`; } return d; };
  const band = (a, b, col) => `<rect x="${m.l}" y="${ys(b)}" width="${W - m.l - m.r}" height="${ys(a) - ys(b)}" fill="${col}"/>`;
  return lightShell(1800, 820, 'Health factor as the price of ETH moves', '10 ETH collateral, liquidation threshold 0.80. Blue: $12,000 debt. Orange: $16,000 debt. Below 1.0 the position can be liquidated.',
    `<svg width="100%" height="100%" viewBox="0 0 ${W} ${H}">
    ${band(0, 1, 'rgba(235,104,52,.10)')}${band(1, 1.5, 'rgba(237,161,0,.08)')}
    ${axisFrame(W, H, m, [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500], [0, 0.5, 1, 1.5, 2, 2.5, 3], xs, ys, 'ETH price (USD)', 'Health factor', v => `$${v.toLocaleString('en-US')}`, v => v.toFixed(1))}
    <path d="M${m.l},${ys(1)} H${W - m.r}" stroke="${C.orange}" stroke-width="2" stroke-dasharray="9 7"/>
    <path d="M${xs(3000)},${m.t} V${H - m.b}" stroke="#9aa3ad" stroke-width="1.5" stroke-dasharray="4 6"/>
    <path d="${line(12000)}" fill="none" stroke="${C.blue}" stroke-width="3.5"/>
    <path d="${line(16000)}" fill="none" stroke="${C.orange}" stroke-width="3.5"/>
    ${dot(xs(3000), ys(2))}${label(xs(3000) + 16, ys(2) + 34, 'Today: HF 2.0')}
    ${dot(xs(3000), ys(1.5), C.orange)}${label(xs(3000) + 16, ys(1.5) + 32, 'HF 1.5')}
    ${dot(xs(1500), ys(1))}${label(xs(1500) - 14, ys(1) - 18, 'Liquidation $1,500 (−50%)', 'end')}
    ${dot(xs(2000), ys(1), C.orange)}${label(xs(2000) + 14, ys(1) + 36, 'Liquidation $2,000 (−33%)')}
    ${label(xs(4450), ys(0.5), 'Liquidatable (HF below 1.0)', 'end', 600)}${label(xs(4450), ys(1.25), 'Danger zone (HF 1.0–1.5)', 'end', 600)}
    ${label(xs(3000) + 8, m.t + 26, 'Price today $3,000', 'start', 600)}
    </svg>`);
}

// ---------- lesson images: layout templates + one data row per image ----------
// Every image goes through lightShell (title, logo footer, DISCLAIMER). Blue = neutral,
// orange = the risk or failure side. Copy is illustrative; it never promises returns.
const noteBar = note => note ? `<div style="position:absolute;left:0;right:0;bottom:0;text-align:center;font-size:23px;color:${C.text2};font-weight:500">${note}</div>` : '';
const withNote = (inner, note) => `<div style="position:absolute;inset:0 0 ${note ? 60 : 0}px 0">${inner}</div>${noteBar(note)}`;
function tplFlow(r) {
  const n = r.steps.length, gap = n > 4 ? 48 : 64, w = Math.floor((1672 - gap * (n - 1)) / n);
  return lightShell(1800, r.h || 640, r.title, r.sub, withNote(flowBoxes(r.steps, false, { w, h: 250, gap }), r.note));
}
function tplCols(r) {
  const n = r.cols.length;
  const cards = r.cols.map(c => {
    const col = c.tone === 'risk' ? C.orange : c.tone === 'good' ? C.brand : C.blue;
    return `<div style="flex:1;background:#fff;border:1.5px solid ${c.tone ? col : C.line};border-top:6px solid ${col};border-radius:20px;padding:30px 32px">
      <div style="display:flex;align-items:center;gap:16px"><div style="width:62px;height:62px;border-radius:16px;background:${C.panel};color:${col};display:flex;align-items:center;justify-content:center;flex:none">${icon(c.ic || 'check', 34)}</div>
      <div style="font-size:${n > 3 ? 28 : 32}px;font-weight:800;color:${C.ink};line-height:1.15">${c.t}</div></div>
      <div style="margin-top:22px;display:flex;flex-direction:column;gap:14px">${c.lines.map(l => `<div style="display:flex;gap:12px;font-size:${n > 3 ? 21 : 23}px;line-height:1.4;color:${C.text}"><span style="flex:none;width:9px;height:9px;border-radius:50%;background:${col};margin-top:12px"></span><span>${l}</span></div>`).join('')}</div></div>`;
  }).join('');
  return lightShell(1800, r.h || 760, r.title, r.sub, withNote(`<div style="display:flex;gap:30px;height:100%;align-items:stretch">${cards}</div>`, r.note));
}
function tplTiles(r) {
  const n = r.tiles.length;
  const tiles = r.tiles.map(([t, s, ic], i) => `<div style="background:#fff;border:1.5px solid ${C.line};border-radius:20px;padding:30px 28px">
    <div style="width:64px;height:64px;border-radius:16px;background:${C.panel};color:${C.blue};display:flex;align-items:center;justify-content:center">${icon(ic, 36)}</div>
    <div style="font-size:30px;font-weight:800;color:${C.ink};margin-top:22px">${t}</div>
    <div style="font-size:22px;color:${C.text2};margin-top:10px;line-height:1.4">${s}</div></div>`).join('');
  return lightShell(1800, r.h || 640, r.title, r.sub, withNote(`<div style="display:grid;grid-template-columns:repeat(${n},1fr);gap:26px;height:100%">${tiles}</div>`, r.note));
}
function tplRank(r) {
  const n = r.rows.length;
  const rows = r.rows.map(([t, s], i) => { const f = i / (n - 1);
    return `<div style="display:flex;align-items:center;gap:24px;background:#fff;border:1.5px solid ${C.line};border-radius:14px;padding:12px 24px">
      <div style="font-size:26px;font-weight:800;color:${f > .6 ? C.orange : C.blue};width:34px">${i + 1}</div>
      <div style="width:380px;font-size:26px;font-weight:700;color:${C.ink}">${t}</div><div style="flex:1;font-size:21px;color:${C.text2}">${s}</div>
      <div style="width:260px;height:12px;border-radius:6px;background:${C.panel}"><div style="height:100%;width:${100 - f * 85}%;border-radius:6px;background:${f > .6 ? C.orange : C.blue}"></div></div></div>`; }).join('');
  return lightShell(1800, 820, r.title, r.sub, withNote(`<div style="display:flex;flex-direction:column;justify-content:space-between;height:100%">
    <div style="display:flex;justify-content:space-between;font-size:18px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:${C.text2}"><span>More durable</span><span>More fragile ↓</span></div>${rows}</div>`, r.note));
}
function tplBars(r) { // stacked bars in HTML: [label, [[part, value, 'blue'|'orange'], ...]]
  const max = Math.max(...r.bars.map(b => b[1].reduce((a, p) => a + p[1], 0)));
  const bars = r.bars.map(([label, parts]) => { const tot = parts.reduce((a, p) => a + p[1], 0);
    return `<div style="display:flex;align-items:center;gap:26px"><div style="width:230px;font-size:26px;font-weight:700;color:${C.ink}">${label}</div>
      <div style="flex:1;display:flex;height:84px">${parts.map(([p, v, c]) => `<div style="width:${v / max * 88}%;background:${c === 'orange' ? C.orange : C.blue};color:#fff;font-size:21px;font-weight:700;display:flex;align-items:center;justify-content:center;border-right:3px solid #fff">${v / max * 88 >= 12 ? `${p} ${v}%` : ''}</div>`).join('')}
      <div style="padding-left:18px;align-self:center"><div style="font-size:30px;font-weight:800;color:${C.ink}">${tot}%</div><div style="font-size:18px;color:${C.text2};white-space:nowrap">${parts.map(([p, v]) => `${p} ${v}%`).join(' + ')}</div></div></div></div>`; }).join('');
  return lightShell(1800, 640, r.title, r.sub, withNote(`<div style="display:flex;flex-direction:column;justify-content:center;gap:40px;height:100%">${bars}</div>`, r.note));
}
function tplTable(r) {
  const body = `<table style="width:100%;border-collapse:separate;border-spacing:0;font-size:23px;background:#fff;border:1.5px solid ${C.line};border-radius:16px;overflow:hidden">
    <tr>${r.head.map(h => `<th style="text-align:left;padding:18px 22px;background:${C.ink};color:#fff;font-size:19px;letter-spacing:.06em;text-transform:uppercase">${h}</th>`).join('')}</tr>
    ${r.rows.map(row => `<tr>${row.map((c, j) => `<td style="padding:18px 22px;border-top:1px solid ${C.line};color:${j === 2 ? (c === 'High' ? C.orange : C.blue) : C.text};font-weight:${j === 0 || j === 2 ? 700 : 400}">${c}</td>`).join('')}</tr>`).join('')}</table>`;
  return lightShell(1800, 700, r.title, r.sub, withNote(body, r.note));
}
function diagramPoolDepth() {
  const W = 1672, H = 470, m = { l: 110, r: 40, t: 20, b: 70 };
  const xs = v => m.l + v / 20 * (W - m.l - m.r), ys = v => m.t + (20 - v) / 20 * (H - m.t - m.b);
  const imp = s => s / (100 + s) * 100; // % price impact for a trade of s% of the pool's reserve (x·y=k)
  let d = ''; for (let s = 0; s <= 20; s += 0.25) d += `${s ? 'L' : 'M'}${xs(s).toFixed(1)},${ys(imp(s)).toFixed(1)}`;
  return lightShell(1800, 760, 'Can this pool take your trade', 'Depth vs your size: price impact in a constant-product pool, before fees',
    `<svg width="100%" height="100%" viewBox="0 0 ${W} ${H}">${axisFrame(W, H, m, [0, 5, 10, 15, 20], [0, 5, 10, 15, 20], xs, ys, 'Your trade as % of the pool reserve', 'Price impact', v => `${v}%`, v => `${v}%`)}
    <path d="${d}" fill="none" stroke="${C.blue}" stroke-width="3.5"/>
    ${dot(xs(1), ys(imp(1)))}${label(xs(1.9), ys(0.25), '1% of the pool → ≈1.0% impact')}
    ${dot(xs(10), ys(imp(10)), C.orange)}${label(xs(10) + 16, ys(imp(10)) + 34, '10% of the pool → ≈9.1% impact')}</svg>`);
}
function chartVarDrawdown() {
  const W = 1672, H = 600, m = { l: 120, r: 40, t: 20, b: 70 };
  const xs = v => m.l + (v - 20) / 100 * (W - m.l - m.r), ys = v => m.t + (14000 - v) / 14000 * (H - m.t - m.b);
  const vaR = (vol, z) => z * vol / 100 / Math.sqrt(365) * 100000;
  const line = z => { let d = ''; for (let v = 20; v <= 120; v += 1) d += `${v === 20 ? 'M' : 'L'}${xs(v).toFixed(1)},${ys(vaR(v, z)).toFixed(1)}`; return d; };
  return lightShell(1800, 820, 'Quantitative risk', 'Size from the number: 1-day value at risk on a $100,000 position. Assumes normal returns, and crypto tails are fatter, so treat it as a floor.',
    `<svg width="100%" height="100%" viewBox="0 0 ${W} ${H}">${axisFrame(W, H, m, [20, 40, 60, 80, 100, 120], [0, 2000, 4000, 6000, 8000, 10000, 12000, 14000], xs, ys, 'Annualised volatility (%)', '1-day VaR', v => `${v}%`, v => `$${(v / 1000).toFixed(0)}k`)}
    <path d="${line(1.65)}" fill="none" stroke="${C.blue}" stroke-width="3.5"/><path d="${line(2.33)}" fill="none" stroke="${C.orange}" stroke-width="3.5"/>
    ${dot(xs(70), ys(vaR(70, 1.65)))}${label(xs(70) + 16, ys(vaR(70, 1.65)) + 32, '70% vol, 95%: ≈$6,040')}
    ${dot(xs(70), ys(vaR(70, 2.33)), C.orange)}${label(xs(70) - 16, ys(vaR(70, 2.33)) - 16, '70% vol, 99%: ≈$8,530', 'end')}
    ${label(xs(118), ys(vaR(118, 1.65)) + 34, 'Blue: 95% (z = 1.65)', 'end', 600)}${label(xs(118), ys(vaR(118, 2.33)) - 18, 'Orange: 99% (z = 2.33)', 'end', 600)}</svg>`);
}
function chartExpectedYield() {
  const W = 1672, H = 600, m = { l: 110, r: 40, t: 40, b: 70 };
  const P = [['Stablecoin lending', 5, 0.02, 0.5], ['Blue-chip LP farm', 18, 0.10, 0.6], ['New high-APY farm', 40, 0.30, 0.9]];
  const ys = v => m.t + (45 - v) / 45 * (H - m.t - m.b), bw = 260, gap = (W - m.l - m.r - bw * 3) / 4;
  const bars = P.map(([n, y, p, lgd], i) => { const loss = p * lgd * 100, x = m.l + gap + i * (bw + gap), e = y - loss;
    return `<rect x="${x}" y="${ys(e)}" width="${bw}" height="${ys(0) - ys(e)}" fill="${C.blue}"/><rect x="${x}" y="${ys(y)}" width="${bw}" height="${ys(e) - ys(y)}" fill="${C.orange}"/>
      <text x="${x + bw / 2}" y="${ys(y) - 14}" text-anchor="middle" font-size="22" font-weight="800" fill="${C.text}" font-family="Inter">${y}% headline</text>
      ${e > 3 ? `<text x="${x + bw / 2}" y="${ys(e) + 32}" text-anchor="middle" font-size="22" font-weight="800" fill="#fff" font-family="Inter">${e.toFixed(1)}% expected</text>` : ''}
      <text x="${x + bw / 2}" y="${H - m.b + 32}" text-anchor="middle" font-size="20" fill="${C.text2}" font-family="Inter">${n}</text>
      <text x="${x + bw / 2}" y="${H - m.b + 56}" text-anchor="middle" font-size="17" fill="${C.text2}" font-family="Inter">loss ${p} × ${lgd} = ${loss.toFixed(1)}%</text>`; }).join('');
  const grid = [0, 10, 20, 30, 40].map(v => `<line x1="${m.l}" x2="${W - m.r}" y1="${ys(v)}" y2="${ys(v)}" stroke="${v ? '#E6EAF0' : '#9aa3ad'}"/><text x="${m.l - 14}" y="${ys(v) + 7}" text-anchor="end" font-size="20" fill="${C.text2}" font-family="Inter">${v}%</text>`).join('');
  return lightShell(1800, 820, 'Expected yield', 'Headline APY − expected loss (annual loss probability × loss given default) = expected yield. Blue: expected yield. Orange: expected loss. Illustrative inputs.',
    `<svg width="100%" height="100%" viewBox="0 0 ${W} ${H + 20}">${grid}${bars}</svg>`);
}

const LESSON_IMAGES = [
  // Module 0
  { file: 'ledgers-vs-blockchain', lesson: '0.1', kind: 'cols', title: 'Ledgers vs a blockchain', sub: 'Same record, different trust', note: 'On a blockchain there is no undo.',
    cols: [{ t: 'A bank’s private ledger', ic: 'bank', lines: ['One copy, kept by the bank', 'The bank can correct or reverse entries', 'You trust the bank'] },
      { t: 'A shared blockchain', ic: 'layers', tone: 'risk', lines: ['Thousands of computers keep the same copy', 'Old entries can’t be quietly changed', 'No undo: a mistake is final'] }] },
  { file: 'exchange-lockdown', lesson: '0.2', kind: 'flow', title: 'Lock the exchange down first', sub: 'Before any deposit', note: 'Do all four before the first deposit.',
    steps: [['Account', 'Unique email and a password manager', 'users'], ['2FA', 'Authenticator app, not SMS', 'lock'], ['Whitelist', 'Withdrawals only to your own addresses', 'shield'], ['Anti-phishing', 'A code shown in every real email', 'check']] },
  { file: 'first-buy-costs', lesson: '0.3', kind: 'flow', title: 'What a first buy actually costs', sub: 'Headline price is not the fill', note: 'Compare offers by what you receive, not the quoted price.',
    steps: [['Price', 'What the chart shows', 'chart'], ['− Spread', 'Gap between buy and sell', 'swap'], ['− Fee', 'Trading or “convenience” fee', 'coins'], ['− Network', 'Withdrawal or gas cost', 'layers'], ['= Received', 'What lands in your wallet', 'wallet']] },
  { file: 'custody-split', lesson: '0.4', kind: 'cols', title: 'Who holds the keys', sub: 'Exchange account vs your wallet', note: 'Your keys, your coins, and your responsibility. Never share a seed phrase.',
    cols: [{ t: 'Exchange account', ic: 'bank', lines: ['The exchange holds the keys', 'Belongs here: buying, selling, cashing out', 'Risk: freezes, hacks, insolvency'] },
      { t: 'Your wallet', ic: 'wallet', lines: ['You hold the keys (the seed phrase)', 'Belongs here: holding and using DeFi', 'Risk: lose the seed, lose the funds'] }] },
  { file: 'practice-mode-first', lesson: '0.7', kind: 'flow', title: 'Practice mode first', sub: 'Test net, then a tiny real amount',
    steps: [['Test network', 'Free test tokens with no value', 'compass'], ['Connect', 'Only from a bookmarked site', 'link'], ['Read it', 'What, to whom, how much', 'eye'], ['Tiny real amount', 'Last, after the test works', 'coins']] },
  { file: 'security-baseline', lesson: '0.8', kind: 'tiles', title: 'Security baseline', sub: 'The habits that prevent most losses',
    tiles: [['Hardware wallet', 'Keys never touch the internet', 'lock'], ['Unique passwords', 'A password manager plus 2FA everywhere', 'key'], ['Never share keys', 'Real support never asks for a seed phrase', 'shield'], ['Bookmark apps', 'Never follow links to wallets or DeFi apps', 'book']] },
  // Module 1
  { file: 'defi-stack', lesson: '1.1', kind: 'flow', title: 'The DeFi stack', sub: 'Yield is payment for a risk', note: 'Every yield pays for a risk. Name it before you deposit.',
    steps: [['Chain', 'Settles every transaction', 'layers'], ['Wallet', 'Holds your keys and signs', 'wallet'], ['App', 'Smart contracts: swap, lend, stake', 'grid'], ['Position', 'What you hold and what it risks', 'target']] },
  { file: 'tx-lifecycle', lesson: '1.2', kind: 'flow', title: 'A transaction’s life', sub: 'Sign to finality', note: 'Gas is paid whether the transaction succeeds or fails.',
    steps: [['Sign', 'Your wallet signs it', 'key'], ['Mempool', 'Waiting, publicly visible', 'clock'], ['Block', 'A validator includes it', 'layers'], ['Finality', 'Now irreversible', 'check']] },
  { file: 'approval-anatomy', lesson: '1.4', kind: 'cols', title: 'Anatomy of an approval', sub: 'Read it before you sign', note: 'An approval outlives the trade. Revoke the ones you no longer use.',
    cols: [{ t: 'Token', ic: 'coins', lines: ['Which asset the app may move'] }, { t: 'Spender', ic: 'eye', lines: ['The contract that can move it', 'Check it on the explorer'] },
      { t: 'Amount', ic: 'target', tone: 'risk', lines: ['Infinite: no limit, until revoked', 'Exact: only this trade', 'Exact is the default'] }] },
  { file: 'stablecoin-designs', lesson: '1.5', kind: 'cols', title: 'How stablecoins are built', sub: 'And how each design breaks',
    cols: [{ t: 'Fiat-backed', ic: 'bank', lines: ['Cash and T-bills held by an issuer', 'Breaks if: reserves are frozen or missing'] },
      { t: 'Crypto-backed', ic: 'vault', lines: ['Over-collateralised on-chain', 'Breaks if: collateral falls faster than liquidations'] },
      { t: 'Algorithmic', ic: 'cog', tone: 'risk', lines: ['Held up by incentives and a sister token', 'Breaks if: confidence goes and it spirals'] }] },
  { file: 'scam-patterns', lesson: '1.6', kind: 'tiles', title: 'Common attacks', sub: 'Recognise them before they cost you', note: 'Nobody legitimate will ever ask for your seed phrase or keys.',
    tiles: [['Fake sites', 'Look-alike URLs and sponsored ads', 'globe'], ['Drainers', 'One signature that grants everything', 'flame'], ['Fake support', '“Support” DMs asking for your seed', 'users'], ['Poisoned addresses', 'Look-alike addresses in your history', 'alert']] },
  { file: 'simulate-before-sign', lesson: '1.7', kind: 'flow', title: 'Simulate before you sign', sub: 'Know what the call does',
    steps: [['Wallet preview', 'What the wallet says will happen', 'wallet'], ['Simulator', 'Run it without sending', 'search'], ['Decoded calls', 'Function, token, amount, spender', 'code'], ['Sign or reject', 'Only if all three agree', 'check']] },
  { file: 'privacy-physical', lesson: '1.8', kind: 'cols', title: 'Privacy and physical security', sub: 'Address ≠ identity, until you connect the two',
    cols: [{ t: 'Public address', ic: 'globe', lines: ['Every balance and trade is public', 'Anyone can follow the funds'] },
      { t: 'Your identity', ic: 'users', lines: ['Exchanges link it to your address', 'Don’t post addresses or balances'] },
      { t: 'Home and devices', ic: 'lock', tone: 'risk', lines: ['Seed backups out of sight', 'A separate device for signing', 'Tell no one what you hold'] }] },
  // Module 2
  { file: 'dex-vs-aggregator', lesson: '2.1', kind: 'cols', title: 'DEX vs aggregator', sub: 'Compare net received, not the quote',
    cols: [{ t: 'Direct pool', ic: 'swap', lines: ['One pool, one price curve', 'Simple, but size moves the price'] },
      { t: 'Aggregator', ic: 'grid', lines: ['Routes across many pools', 'Often a better fill, plus its own contract risk'] },
      { t: 'Compare this', ic: 'target', tone: 'good', lines: ['Net received after fees and gas', 'Not the headline quote'] }] },
  { file: 'lp-position', lesson: '2.3', kind: 'flow', title: 'Providing liquidity', sub: 'Fees vs inventory change', note: 'Result = fees earned − impermanent loss, compared with just holding.',
    steps: [['Deposit both', 'Equal value of each asset', 'coins'], ['Pool share', 'A receipt for your slice', 'layers'], ['Earn fees', 'From every swap through the pool', 'sprout'], ['The bag changes', 'You end up holding more of the loser', 'alert']] },
  { file: 'mev-sandwich', lesson: '2.5', kind: 'flow', title: 'A sandwich', sub: 'Your swap in the middle', note: 'Loose slippage is the open door. Keep it tight and use a protected RPC.',
    steps: [['Attacker buys', 'Front-runs you and pushes the price up', 'flame'], ['Your swap', 'Fills at the worse price', 'swap'], ['Attacker sells', 'Keeps the difference', 'flame']] },
  { file: 'order-types', lesson: '2.6', kind: 'cols', title: 'Order types', sub: 'Better than a plain swap',
    cols: [{ t: 'Market', ic: 'swap', lines: ['Fills now at the current price', 'Safer when: small size, deep pool'] }, { t: 'Limit', ic: 'target', lines: ['Fills only at your price or better', 'Safer when: you can wait'] },
      { t: 'TWAP', ic: 'clock', lines: ['Splits a large order over time', 'Safer when: size is large vs the pool'] }, { t: 'Intent', ic: 'users', lines: ['You sign the outcome; solvers compete', 'Safer when: MEV is a concern'] }] },
  // Module 3
  { file: 'lending-pool-flow', lesson: '3.1', kind: 'flow', title: 'How a lending pool works', sub: 'Rates jump when utilisation is high', note: 'Near 100% utilisation, lenders may not be able to withdraw.',
    steps: [['Suppliers', 'Deposit assets, earn interest', 'coins'], ['Pool', 'Utilisation = borrowed ÷ supplied', 'bank'], ['Borrowers', 'Post collateral, pay interest', 'wallet']] },
  { file: 'perp-anatomy', lesson: '3.5', kind: 'cols', title: 'Perpetual futures', sub: 'Margin, funding, liquidation',
    cols: [{ t: 'Position', ic: 'chart', lines: ['Long or short, no expiry', 'Margin backs the position'] }, { t: 'Funding', ic: 'swap', lines: ['Longs and shorts pay each other', 'Keeps the perp near spot'] },
      { t: 'Liquidation', ic: 'alert', tone: 'risk', lines: ['Margin falls below maintenance', 'At 20× leverage, a move of under 5% can wipe out the margin'] }] },
  { file: 'cdp-mint', lesson: '3.7', kind: 'flow', title: 'Minting your own dollars', sub: 'A CDP, managed like a bank', note: 'Keep the collateral ratio well above the minimum, like any loan.',
    steps: [['Lock collateral', 'An approved asset such as ETH', 'vault'], ['Mint', 'Stablecoins up to the ratio', 'coins'], ['Use it', 'Spend, lend or hold', 'wallet'], ['Repay + fee', 'Plus the stability fee; collateral unlocks', 'exit']] },
  // Module 4
  { file: 'base-vs-emissions', lesson: '4.1', kind: 'bars', title: 'Base yield vs emissions', sub: 'Split the APY (illustrative pools)', note: 'Emissions are paid in a token that can fall. Fees are the part that lasts.',
    bars: [['Pool A', [['Fees', 4, 'blue'], ['Emissions', 16, 'orange']]], ['Pool B', [['Fees', 8, 'blue'], ['Emissions', 1, 'orange']]]] },
  { file: 'native-staking', lesson: '4.2', kind: 'flow', title: 'Native staking', sub: 'What the yield is paying for', note: 'The yield pays for locking capital and taking validator risk.',
    steps: [['Stake', 'Deposit to the protocol', 'lock'], ['Validator', 'Secures the chain, earns rewards', 'shield'], ['Exit queue', 'Unstaking takes time', 'clock'], ['Slashing', 'A penalty for validator faults', 'alert']] },
  { file: 'lst-accrual', lesson: '4.3', kind: 'flow', title: 'Liquid staking tokens', sub: 'Accrual vs depeg',
    steps: [['ETH', 'Staked through a provider', 'coins'], ['LST', 'A token for your staked ETH', 'layers'], ['Accrues', 'Rewards build into its value', 'sprout'], ['Depeg risk', 'It can trade below the ETH behind it', 'alert']] },
  { file: 'restaking-layers', lesson: '4.4', kind: 'flow', title: 'Restaking adds layers', sub: 'Extra yield, extra slashing', note: 'Each layer adds yield and adds another way to lose it.',
    steps: [['Stake', 'Base staking yield', 'lock'], ['Restake', 'Reuse the same stake', 'layers'], ['Extra services', 'Extra rewards', 'sprout'], ['Extra slashing', 'Each service can penalise you', 'alert']] },
  { file: 'vault-vs-diy', lesson: '4.5', kind: 'cols', title: 'Vault vs doing it yourself', sub: 'Fees for automation', note: 'Pay for automation when its fees cost less than your gas and time.',
    cols: [{ t: 'Vault', ic: 'bot', lines: ['Automates harvesting and rebalancing', 'Charges management or performance fees', 'Adds the vault’s own contract risk'] },
      { t: 'Do it yourself', ic: 'users', lines: ['The same steps by hand', 'Gas every time you act', 'Your time and your mistakes'] }] },
  { file: 'points-opportunity-cost', lesson: '4.6', kind: 'cols', title: 'Points are a bet', sub: 'Include the costs', note: 'Value = probability × airdrop size − costs. Size it as a bet.',
    cols: [{ t: 'What you pay', ic: 'lock', tone: 'risk', lines: ['Capital locked, yield given up', 'Gas and bridge costs', 'Protocol risk while you wait'] },
      { t: 'What you might get', ic: 'sprout', lines: ['An airdrop of unknown size', 'Possibly nothing at all'] }] },
  { file: 'yield-bearing-stables', lesson: '4.7', kind: 'cols', title: 'Yield-bearing stablecoins', sub: 'Different machines, different risk',
    cols: [{ t: 'Idle stablecoin', ic: 'coins', lines: ['No yield', 'Risk: issuer and peg'] }, { t: 'Savings-rate stable', ic: 'bank', lines: ['Yield from protocol lending', 'Risk: adds the protocol’s loans and contracts'] },
      { t: 'RWA-backed stable', ic: 'vault', tone: 'risk', lines: ['Yield from off-chain T-bills', 'Risk: adds custodian, legal wrapper, redemption'] }] },
  { file: 'rwa-trust', lesson: '4.8', kind: 'flow', title: 'Tokenized real-world assets', sub: 'What you actually own', note: 'You own a claim on the issuer, not the asset itself.',
    steps: [['Token', 'What you hold on-chain', 'coins'], ['Issuer', 'Promises redemption', 'bank'], ['Custodian', 'Holds the real asset', 'vault'], ['Real asset', 'T-bills, credit, property', 'doc']] },
  // Module 5
  { file: 'bridge-trust', lesson: '5.1', kind: 'cols', title: 'Bridge trust models', sub: 'Size exposure to the model',
    cols: [{ t: 'Custodial / multisig', ic: 'users', tone: 'risk', lines: ['You trust a small set of signers', 'Keys compromised: funds gone'] },
      { t: 'Light-client', ic: 'shield', lines: ['You trust the chains’ own consensus', 'Strongest, slower and rarer'] },
      { t: 'Optimistic', ic: 'clock', lines: ['You trust at least one honest watcher', 'Withdrawals wait out a challenge window'] }] },
  { file: 'l2-exit', lesson: '5.2', kind: 'flow', title: 'How an L2 settles', sub: 'And how you exit',
    steps: [['You', 'Transact on the L2', 'wallet'], ['Sequencer', 'Orders the transactions', 'cog'], ['L1 settlement', 'Batches posted to Ethereum', 'layers'], ['Forced exit', 'Withdraw via L1 if the sequencer fails', 'exit']] },
  { file: 'oracle-twap', lesson: '5.3', kind: 'cols', title: 'Oracles and TWAPs', sub: 'Which price secures the position',
    cols: [{ t: 'Spot print', ic: 'chart', tone: 'risk', lines: ['One price at one moment', 'A thin pool can be pushed for a block'] },
      { t: 'TWAP', ic: 'clock', lines: ['Averaged over a time window', 'Costly to manipulate, lags fast moves'] },
      { t: 'Ask', ic: 'search', lines: ['Which price secures this position?', 'Where does it come from?'] }] },
  { file: 'proxy-admin-keys', lesson: '5.4', kind: 'flow', title: 'Proxies and admin keys', sub: 'Code can change after you deposit', note: 'Check the timelock and who holds the admin key before you deposit.',
    steps: [['You call', 'The proxy address', 'wallet'], ['Proxy', 'Holds your funds and state', 'layers'], ['Logic', 'The implementation, replaceable', 'code'], ['Admin', 'Can upgrade the logic', 'key']] },
  { file: 'audit-coverage', lesson: '5.5', kind: 'cols', title: 'What an audit covers', sub: 'And what it never proved',
    cols: [{ t: 'An audit checked', ic: 'check', lines: ['One specific code version', 'Known classes of bugs', 'The scope written in the report'] },
      { t: 'It never proved', ic: 'alert', tone: 'risk', lines: ['Later upgrades', 'Economic and oracle attacks', 'Admin-key misuse', 'That the code is safe'] }] },
  { file: 'ecosystem-map', lesson: '5.6', kind: 'tiles', title: 'Beyond Ethereum', sub: 'Different chains, different trust', note: 'Know which chain, and which trust assumption, you rely on.',
    tiles: [['Ethereum', 'The base layer with the deepest DeFi', 'layers'], ['L2s', 'Cheaper; settle to Ethereum with added trust', 'grid'], ['Solana', 'A fast single chain with its own validators', 'swap'], ['Bitcoin wrappers', 'BTC used elsewhere via a custodian or bridge', 'link']] },
  { file: 'cross-chain-gas', lesson: '5.7', kind: 'flow', title: 'Operating across chains', sub: 'Don’t get stranded without gas', note: 'Bring a little native gas token before, or with, the bridge.',
    steps: [['Bridge', 'Assets move across', 'link'], ['Arrive', 'Funds on the destination', 'wallet'], ['Gas tank', 'Native token for fees', 'flame'], ['Stranded?', 'No gas, no transactions', 'alert']] },
  { file: 'read-verified-code', lesson: '5.8', kind: 'flow', title: 'Read the verified code', sub: 'Check the claim',
    steps: [['Explorer', 'Open the contract', 'search'], ['Code tab', 'The verified source', 'code'], ['Function', 'Find the one you’ll call', 'target'], ['The claim', 'Does the code match the docs?', 'check']] },
  // Module 6
  { file: 'token-supply-unlocks', lesson: '6.2', kind: 'cols', title: 'Supply, unlocks, FDV', sub: 'Does success reach the token',
    cols: [{ t: 'Circulating vs FDV', ic: 'coins', lines: ['Circulating: tradable today', 'FDV: price × every token that will exist'] },
      { t: 'Unlock cliff', ic: 'clock', tone: 'risk', lines: ['Large unlocks add supply', 'Check the schedule before you buy'] },
      { t: 'Value capture', ic: 'target', lines: ['Does protocol success reach the token?', 'Fees, buybacks, or nothing'] }] },
  { file: 'dao-control', lesson: '6.3', kind: 'flow', title: 'Who controls the protocol', sub: 'Governance risk before it hits you', note: 'Short timelocks and powerful admins are governance risk.',
    steps: [['Token vote', 'Holders propose and vote', 'users'], ['Timelock', 'A delay before changes run', 'clock'], ['Admin / multisig', 'Executes; may hold emergency powers', 'key']] },
  { file: 'thesis-invalidation', lesson: '6.4', kind: 'flow', title: 'Thesis and kill conditions', sub: 'Written before capital moves', note: 'All three fit on one page.',
    steps: [['Thesis', 'Why this position, in one line', 'doc'], ['Monitors', 'What you’ll watch', 'eye'], ['Invalidation', 'What makes you exit', 'exit']] },
  { file: 'failure-patterns', lesson: '6.5', kind: 'tiles', title: 'How DeFi failures rhyme', sub: 'Patterns, not headlines',
    tiles: [['Oracle', 'A manipulated or stale price', 'chart'], ['Upgrade', 'A bad or malicious code change', 'code'], ['Bank run', 'Everyone exits at once', 'users'], ['Incentive death', 'Emissions stop, liquidity leaves', 'sprout']] },
  { file: 've-bribe-flow', lesson: '6.6', kind: 'flow', title: 'Vote-escrow and bribes', sub: 'Lock, votes, gauges',
    steps: [['Lock', 'Tokens locked for voting power', 'lock'], ['Votes', 've-holders vote on gauges', 'users'], ['Bribes', 'Protocols pay for votes', 'coins'], ['Gauges', 'Emissions go to the winning pools', 'sprout']] },
  { file: 'protocol-multiples', lesson: '6.7', kind: 'flow', title: 'Protocol economics', sub: 'Fees to multiples, no narrative', note: 'Compare multiples across protocols using real data only.',
    steps: [['Fees', 'Paid by users', 'coins'], ['Revenue', 'The protocol’s share', 'bank'], ['Earnings', 'Revenue − incentives − costs', 'chart'], ['Multiple', 'Value ÷ earnings', 'target']] },
  // Module 7
  { file: 'onchain-misreads', lesson: '7.1', kind: 'cols', title: 'Classic on-chain misreads', sub: 'Volume, users, TVL', note: 'Every metric needs its caveat.',
    cols: [{ t: 'Volume', ic: 'swap', lines: ['Can be wash-traded', 'Check: unique traders, fees paid'] }, { t: 'Users', ic: 'users', lines: ['Addresses are not people', 'Check: sybil and airdrop farming'] },
      { t: 'TVL', ic: 'vault', lines: ['Counts looped and subsidised capital', 'Check: organic fees'] }] },
  { file: 'explorer-anatomy', lesson: '7.2', kind: 'tiles', title: 'A transaction on the explorer', sub: 'You do not need the app UI',
    tiles: [['Tx hash', 'The receipt ID', 'doc'], ['From / to', 'Who signed, which contract', 'users'], ['Logs', 'Events: transfers, swaps', 'book'], ['Internal calls', 'What the contract did next', 'code']] },
  { file: 'exchange-flows', lesson: '7.3', kind: 'cols', title: 'Exchange inflows and outflows', sub: 'Read them with caveats',
    cols: [{ t: 'Inflows', ic: 'exit', lines: ['Coins moving to exchanges', 'Often read as: selling ahead', 'Caveat: also collateral and market makers'] },
      { t: 'Outflows', ic: 'wallet', lines: ['Coins leaving exchanges', 'Often read as: holding', 'Caveat: also internal reshuffles'] }] },
  { file: 'entity-clusters', lesson: '7.4', kind: 'cols', title: 'Whales vs clusters', sub: 'Do not copy blindly', note: 'Don’t copy a wallet you can’t identify.',
    cols: [{ t: 'One whale', ic: 'wallet', lines: ['A single large address', 'Motive unknown: hedge, OTC deal, error'] },
      { t: 'Exchange cluster', ic: 'grid', tone: 'risk', lines: ['Many addresses, one entity', 'Looks like whales; it’s customer flow'] }] },
  { file: 'holder-metrics', lesson: '7.5', kind: 'tiles', title: 'Holder metrics as context', sub: 'Not a trade signal', note: 'Context, not a signal.',
    tiles: [['MVRV', 'Market value vs realised value', 'chart'], ['SOPR', 'Are coins being spent at a profit?', 'coins'], ['HODL waves', 'Supply grouped by age', 'layers']] },
  { file: 'real-usage', lesson: '7.6', kind: 'cols', title: 'Real network usage', sub: 'Beyond transaction counts',
    cols: [{ t: 'Transaction count', ic: 'swap', tone: 'risk', lines: ['Cheap to inflate', 'Bots and spam count too'] }, { t: 'Fees paid', ic: 'coins', lines: ['Users paying to use it', 'Hard to fake at scale'] },
      { t: 'Active addresses that matter', ic: 'users', lines: ['Addresses moving real value', 'Dust and sybils filtered out'] }] },
  { file: 'pool-depth', lesson: '7.7', kind: 'custom', fn: diagramPoolDepth, w: 1800, h: 760, title: 'Can this pool take your trade' },
  { file: 'funding-oi', lesson: '7.8', kind: 'tiles', title: 'Derivatives positioning', sub: 'Funding, OI, liquidations', note: 'Positioning is context for risk, not a prediction.',
    tiles: [['Funding', 'Positive: longs pay shorts', 'swap'], ['Open interest', 'Total open positions', 'layers'], ['Liquidation levels', 'Where forced selling clusters', 'alert']] },
  { file: 'query-your-own', lesson: '7.9', kind: 'flow', title: 'Query the chain yourself', sub: 'Don’t depend on one dashboard',
    steps: [['Question', 'One precise question', 'search'], ['RPC / SQL / subgraph', 'Pull the raw data', 'code'], ['Table', 'An answer you can check', 'grid']] },
  // Module 8
  { file: 'risk-buckets', lesson: '8.1', kind: 'cols', title: 'Portfolio risk buckets', sub: 'Caps so one failure cannot sink you', note: 'Each bucket has a written cap, and so does each position inside it.',
    cols: [{ t: 'Core', ic: 'shield', lines: ['Most of the capital', 'Simple, well-tested positions'] }, { t: 'Satellite', ic: 'target', lines: ['A moderate share', 'Strategies you have tested'] },
      { t: 'Speculative', ic: 'flame', tone: 'risk', lines: ['A small, capped share', 'Money you can afford to lose entirely'] }] },
  { file: 'risk-register', lesson: '8.2', kind: 'table', title: 'The risk register', sub: 'Score it, name the response (illustrative rows)',
    head: ['Position', 'Risks', 'Score', 'Written response'],
    rows: [['Stablecoin lending', 'Depeg, contract bug', 'Low', 'Peg alert; exit rule written'], ['ETH/USDC LP', 'Impermanent loss, MEV', 'Medium', 'Weekly range review; fee vs LVR check'], ['Leveraged loop', 'Liquidation, borrow-rate spike', 'High', 'Health-factor alert; repay amount pre-computed']] },
  { file: 'deploy-monitor-respond', lesson: '8.4', kind: 'flow', title: 'The operating playbook', sub: 'Same four phases every time',
    steps: [['Deploy', 'Small first, then size up', 'target'], ['Monitor', 'Alerts on the risks you named', 'eye'], ['Respond', 'Pre-written actions', 'alert'], ['Review', 'What happened, what changes', 'doc']] },
  { file: 'twr-vs-deposits', lesson: '8.5', kind: 'cols', title: 'Honest performance', sub: 'Strip out deposits',
    cols: [{ t: 'Headline P&L', ic: 'chart', tone: 'risk', lines: ['Balance now − balance then', 'Deposits look like profit'] },
      { t: 'Time-weighted return', ic: 'clock', lines: ['Chains each period’s return', 'Deposits and withdrawals stripped out'] }] },
  { file: 'discipline-rules', lesson: '8.6', kind: 'cols', title: 'Impulse vs a written rule', sub: 'Psychology that turns strategy into losses',
    cols: [{ t: 'Impulse', ic: 'flame', tone: 'risk', lines: ['“It’s pumping, add more”', '“It’ll come back”', '“Just this once, more leverage”'] },
      { t: 'Written rule', ic: 'doc', lines: ['Size set before entry', 'Exit at the invalidation', 'Leverage cap written in the policy'] }] },
  { file: 'var-drawdown', dir: 'charts', lesson: '8.7', kind: 'custom', fn: chartVarDrawdown, w: 1800, h: 820, title: 'Quantitative risk' },
  // Module 9
  { file: 'when-each-wins', lesson: '9.2', kind: 'cols', title: 'When each one wins', sub: 'Grid, LP, both, or neither', note: 'Match the tool to the market regime.',
    cols: [{ t: 'Range-bound', ic: 'grid', lines: ['Grid bot or concentrated LP', 'Both earn from oscillation'] },
      { t: 'Strong trend', ic: 'chart', tone: 'risk', lines: ['Neither, or much smaller', 'Both sell into strength and buy into weakness'] },
      { t: 'Choppy, thin volume', ic: 'clock', lines: ['A grid with wider spacing', 'LP fees may not cover the losses'] }] },
  { file: 'combined-system', lesson: '9.3', kind: 'cols', title: 'One system, two sleeves', sub: 'Shared risk cap',
    cols: [{ t: 'Exchange grid sleeve', ic: 'grid', lines: ['Grid bots on an exchange', 'Risk: exchange custody'] }, { t: 'On-chain sleeve', ic: 'layers', lines: ['LPs and lending in DeFi', 'Risk: contracts and oracles'] },
      { t: 'One risk cap', ic: 'shield', tone: 'good', lines: ['One exposure limit across both', 'One kill rule for the whole book'] }] },
  // Module 10
  { file: 'cash-and-carry', lesson: '10.2', kind: 'flow', title: 'Cash-and-carry', sub: 'Capture the basis, not a price view', note: 'Locked only if both legs are held to expiry and margin is never called.',
    steps: [['Buy spot', 'Hold the asset', 'coins'], ['Short future', 'Same size, fixed expiry', 'chart'], ['Basis', 'Future − spot, fixed at entry', 'target'], ['Expiry', 'Prices converge', 'check']] },
  { file: 'funding-carry', lesson: '10.3', kind: 'flow', title: 'Funding carry', sub: 'Sizing, venue limits, exit', note: 'The risks are the venue and a funding flip. Size to venue limits.',
    steps: [['Hold spot', 'Long the asset', 'coins'], ['Short perp', 'Same size, opposite side', 'swap'], ['Collect funding', 'While longs pay shorts', 'sprout'], ['Exit', 'Funding flips or a limit is hit', 'exit']] },
  { file: 'covered-call-put', lesson: '10.4', kind: 'cols', title: 'Options income', sub: 'Premium in, upside capped',
    cols: [{ t: 'Covered call', ic: 'coins', lines: ['Hold the asset, sell a call', 'Premium in', 'Upside capped at the strike'] },
      { t: 'Cash-secured put', ic: 'bank', lines: ['Hold cash, sell a put', 'Premium in', 'You may buy the asset at the strike after a fall'] }] },
  { file: 'cl-range-rebalance', lesson: '10.5', kind: 'cols', title: 'Concentrated liquidity', sub: 'Can fees pay for the rebalance',
    cols: [{ t: 'Narrow range', ic: 'target', lines: ['Bigger fee share while in range', 'Frequent rebalances, more cost'] }, { t: 'Wide range', ic: 'grid', lines: ['Smaller fee share', 'Rarely rebalances'] },
      { t: 'The test', ic: 'check', tone: 'good', lines: ['Fees earned > rebalance cost + impermanent loss'] }] },
  { file: 'points-as-option', lesson: '10.6', kind: 'cols', title: 'Points are an option', sub: 'Size from the known yield',
    cols: [{ t: 'Known yield', ic: 'coins', lines: ['The yield you can measure', 'Size the position on this alone'] },
      { t: 'Unknown points', ic: 'sprout', tone: 'risk', lines: ['A free option if it pays', 'Never the reason for the size'] }] },
  { file: 'perp-lp-vault', lesson: '10.7', kind: 'flow', title: 'You are the house', sub: 'Perp LP vault', note: 'The house can lose: big trader wins are vault losses.',
    steps: [['Traders', 'Open perp positions', 'users'], ['Trader P&L', 'Traders win or lose', 'chart'], ['Your vault', 'The other side, plus fees', 'vault'], ['Risk', 'Traders win big, vault loses', 'alert']] },
  { file: 'peg-arb', lesson: '10.9', kind: 'cols', title: 'Peg and redemption', sub: 'When retail can take part',
    cols: [{ t: 'Mint / redeem', ic: 'bank', lines: ['At $1 with the issuer', 'Often limited to approved parties'] }, { t: 'Secondary market', ic: 'swap', lines: ['Trades at $0.99 or $1.01', 'Open to everyone'] },
      { t: 'Arbitrage', ic: 'target', tone: 'good', lines: ['Buy below, redeem at $1', 'Only where you can redeem'] }] },
  // Module 11
  { file: 'hedge-perp-option', lesson: '11.1', kind: 'cols', title: 'Hedging price', sub: 'Perp vs put, cost of each',
    cols: [{ t: 'Perp short', ic: 'swap', lines: ['Offsets price moves one for one', 'Cost: funding and margin risk'] },
      { t: 'Put option', ic: 'umbrella', lines: ['Pays below the strike', 'Cost: the premium, paid up front'] }] },
  { file: 'cover-what-pays', lesson: '11.2', kind: 'cols', title: 'On-chain cover', sub: 'What it pays and what it excludes', note: 'Read the wording: a payout needs a claim that matches it.',
    cols: [{ t: 'Depeg cover', ic: 'coins', lines: ['Pays: a covered stablecoin below its threshold for the set period', 'Excludes: brief dips, other assets'] },
      { t: 'Protocol cover', ic: 'shield', lines: ['Pays: covered exploit losses', 'Excludes: market losses, your own errors'] },
      { t: 'Contract cover', ic: 'code', lines: ['Pays: bugs in named contracts', 'Excludes: phishing, key compromise'] }] },
  { file: 'liq-buffer-alerts', lesson: '11.3', kind: 'flow', title: 'Liquidation protection', sub: 'Buffer, alerts, pre-computed repay',
    steps: [['Buffer', 'Health factor well above 1', 'shield'], ['Alerts', 'A warning long before trouble', 'bell'], ['Repay ready', 'Amount computed, funds on hand', 'exit']] },
  { file: 'stress-grid', lesson: '11.4', kind: 'cols', title: 'Stress-test the book', sub: 'Fix it before the market does',
    cols: [{ t: '−30% price', ic: 'chart', tone: 'risk', lines: ['Breaks: leveraged loops, tight LP ranges', 'Fix: less leverage, a wider buffer'] },
      { t: 'Stablecoin depeg', ic: 'coins', tone: 'risk', lines: ['Breaks: stable LPs, “safe” yield', 'Fix: spread across issuers'] },
      { t: 'Protocol exploit', ic: 'alert', tone: 'risk', lines: ['Breaks: everything in that protocol', 'Fix: a per-protocol cap'] }] },
  { file: 'incident-60min', lesson: '11.5', kind: 'flow', title: 'The first 60 minutes', sub: 'Exploit, depeg, or compromised wallet',
    steps: [['0–5 min', 'Stop. Sign nothing new', 'alert'], ['5–20 min', 'Size the exposure', 'target'], ['20–40 min', 'Move keys and funds to safety', 'key'], ['40–60 min', 'Public facts only; record everything', 'doc']] },
  // Module 12
  { file: 'personal-balance-sheet', lesson: '12.1', kind: 'cols', title: 'Your on-chain balance sheet', sub: 'Equity, LTV, runway',
    cols: [{ t: 'Assets', ic: 'coins', lines: ['Wallet balances', 'DeFi positions at market value'] }, { t: 'Liabilities', ic: 'bank', tone: 'risk', lines: ['Loans outstanding', 'Accrued interest'] },
      { t: 'The numbers', ic: 'chart', tone: 'good', lines: ['Equity = assets − liabilities', 'LTV = debt ÷ collateral', 'Runway = liquid assets ÷ monthly spend'] }] },
  { file: 'credit-policy', lesson: '12.3', kind: 'flow', title: 'The credit line', sub: 'Liquidity without selling', note: 'The written limits come first: max LTV, minimum health factor, repayment plan.',
    steps: [['Collateral', 'Assets you won’t sell', 'vault'], ['Borrow', 'Within written limits', 'bank'], ['Use', 'Liquidity without selling', 'wallet'], ['Repay', 'On the plan, not on hope', 'exit']] },
  { file: 'lender-side', lesson: '12.5', kind: 'flow', title: 'Being the lender', sub: 'Supply, price, pull',
    steps: [['Choose', 'Collateral and oracle you accept', 'search'], ['Price', 'Rate vs what can go wrong', 'scale'], ['Supply', 'Sized within your cap', 'coins'], ['Pull', 'On utilisation spikes or weak collateral', 'exit']] },
  { file: 'books-succession', lesson: '12.6', kind: 'tiles', title: 'Books and succession', sub: 'A stranger could follow this',
    tiles: [['Ledger', 'Every position and transaction', 'book'], ['Locations', 'Where keys and backups are kept', 'lock'], ['Recovery', 'Who can recover if you can’t', 'users'], ['Instructions', 'Clear enough for a stranger', 'doc']] },
  { file: 'tax-records', lesson: '12.7', kind: 'cols', title: 'Records for tax and legal', sub: 'Not tax advice', note: 'Not tax or legal advice. Consult a qualified professional where you live.',
    cols: [{ t: 'Log for every transaction', ic: 'doc', lines: ['Date, asset, amount', 'Value in your currency', 'Fees paid', 'Transaction hash'] },
      { t: 'Keep', ic: 'book', lines: ['Exchange statements', 'Wallet exports', 'Your own ledger'] }] },
  // Module 13
  { file: 'durability-rank', lesson: '13.1', kind: 'rank', title: 'Income by durability', sub: 'Not by headline APY',
    rows: [['Staking rewards', 'Paid for securing the chain'], ['Lending interest', 'Paid by borrowers'], ['Trading fees', 'Paid by traders; varies with volume'], ['Funding / basis carry', 'Real, but flips and gets crowded'], ['Emissions', 'Newly printed tokens; fade over time'], ['Points', 'Unknown; may be worth nothing']] },
  { file: 'expected-yield', dir: 'charts', lesson: '13.2', kind: 'custom', fn: chartExpectedYield, w: 1800, h: 820, title: 'Expected yield' },
  { file: 'payout-policy', lesson: '13.4', kind: 'flow', title: 'The payout policy', sub: 'What you may take out', note: 'Never pay out from principal.',
    steps: [['Expected income', 'After expected losses', 'chart'], ['Buffer', 'Part stays in the book', 'vault'], ['Payout', 'What you may take out', 'wallet'], ['Cut rules', 'Income falls or drawdown: pay less', 'alert']] },
  { file: 'annual-review', lesson: '13.5', kind: 'flow', title: 'Annual review', sub: 'Grow it like a bank', note: 'Slowly, and on evidence.',
    steps: [['Compound', 'Reinvest what you retain', 'sprout'], ['Scale', 'Grow only what worked', 'chart'], ['Review', 'Yearly: policies, limits, results', 'doc']] },
  // Module 14
  { file: 'alert-stack', lesson: '14.1', kind: 'flow', title: 'Monitoring', sub: 'Hear about it before it costs money',
    steps: [['Positions', 'Health factor, peg, ranges', 'target'], ['Watchers', 'Bots and dashboards read the chain', 'eye'], ['Phone', 'Alerts that wake you', 'bell']] },
  { file: 'least-permission-bot', lesson: '14.2', kind: 'cols', title: 'Automate with least permission', sub: 'No key handover',
    cols: [{ t: 'Keeper / agent', ic: 'bot', lines: ['Does one job', 'Can’t withdraw to new addresses'] }, { t: 'Permission box', ic: 'lock', tone: 'good', lines: ['Named functions only', 'Spending caps', 'Revocable at any time'] },
      { t: 'Never', ic: 'key', tone: 'risk', lines: ['Hand over a seed phrase or key', 'Grant unlimited approvals'] }] },
  { file: 'change-control', lesson: '14.3', kind: 'flow', title: 'Change control', sub: 'No single-point mistakes',
    steps: [['Propose', 'Write the change down', 'doc'], ['Review', 'A second person checks it', 'eye'], ['Multi-sign', 'More than one key approves', 'key'], ['Execute', 'Then verify it worked', 'check']] },
  { file: 'capstone-pack', lesson: '14.4', kind: 'tiles', title: 'Capstone pack', sub: 'What you submit', note: 'No keys, seed phrases or account access anywhere in the pack.',
    tiles: [['Balance sheet', 'Assets, liabilities, equity, LTV', 'doc'], ['Policies', 'Custody, credit, liquidity, payout', 'book'], ['Monitors', 'Alerts mapped to actions', 'bell'], ['Stress test', 'Five scenarios, each one fixed', 'chart']] },
  { file: 'readonly-tools', lesson: '14.5', kind: 'tiles', title: 'Read-only tools', sub: 'No signing', note: 'Read-only tools can’t move funds.',
    tiles: [['Read contract', 'The explorer’s read functions', 'search'], ['Query', 'SQL or a subgraph', 'code'], ['Small script', 'Read-only RPC calls', 'bot']] },
  { file: 'searcher-keeper', lesson: '14.6', kind: 'flow', title: 'Searchers and keepers', sub: 'Why competing is hard', note: 'Competing means racing professionals on speed and capital.',
    steps: [['Mempool', 'Pending transactions', 'clock'], ['Searcher', 'Finds profitable orderings', 'search'], ['Keeper', 'Runs liquidations and upkeep', 'bot'], ['Builder', 'Picks the highest bid', 'layers']] },
];
const renderLessonImage = r => ({ flow: tplFlow, cols: tplCols, tiles: tplTiles, rank: tplRank, bars: tplBars, table: tplTable }[r.kind] || r.fn)(r);
const lessonAsset = r => [`${r.dir || 'diagrams'}/${r.file}.png`, r.w || 1800, r.h || ({ flow: 640, cols: 760, tiles: 640, rank: 820, bars: 640, table: 700 }[r.kind]), () => renderLessonImage(r)];

// ---------- Module 0 story illustrations (beginner analogies, drawn accurately) ----------
function storyChain() {
  const blocks = [['1,001', ['Ana → Ben · 0.10', 'Cai → Dee · 2.00'], '3e9a…', '7c41…'], ['1,002', ['Ben → Eli · 0.05', 'Fay → Ana · 1.20'], '7c41…', 'b2d8…'],
    ['1,003', ['Dee → Gus · 0.30', 'Eli → Cai · 0.75'], 'b2d8…', '51fa…'], ['1,004', ['Gus → Fay · 0.02', 'Ana → Hal · 4.00'], '51fa…', '9e07…']];
  const card = ([n, tx, prev, seal], i) => `<div style="flex:1;background:#fff;border:1.5px solid ${C.line};border-radius:18px;padding:22px 22px 18px">
    <div style="font-size:15px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:${C.blue}">Block</div>
    <div style="font-size:34px;font-weight:800;color:${C.ink}">#${n}</div>
    <div style="margin:14px 0;padding:12px 14px;border-radius:12px;background:${C.panel};font-family:'JetBrains Mono',monospace;font-size:19px;line-height:1.7;color:${C.text}">${tx.join('<br>')}</div>
    <div style="font-size:17px;color:${C.text2}">Previous seal: <b style="font-family:'JetBrains Mono',monospace;color:${i ? C.blue : C.text2}">${prev}</b></div>
    <div style="font-size:17px;color:${C.text2};margin-top:4px">This block's seal: <b style="font-family:'JetBrains Mono',monospace;color:${C.ink}">${seal}</b></div></div>`;
  const link = `<div style="flex:none;width:54px;display:flex;align-items:center;justify-content:center;color:${C.blue}">${icon('link', 38)}</div>`;
  return lightShell(1800, 560, 'A blockchain is a chain of sealed pages', 'Each page (block) records transactions and carries the seal of the page before it',
    `<div style="position:absolute;inset:0 0 60px 0;display:flex;align-items:stretch">${blocks.map(card).join(link)}</div>
    <div style="position:absolute;left:0;right:0;bottom:0;text-align:center;font-size:23px;color:${C.text2}">Change one old entry and its seal changes, so every page after it stops matching. That's why history can't be quietly edited.</div>`);
}
function storyCopies() {
  const W = 1672, H = 470, cx = W / 2, cy = H / 2 - 10, n = 12;
  const nodes = Array.from({ length: n }, (_, i) => { const a = -Math.PI / 2 + i * 2 * Math.PI / n; return [cx + 560 * Math.cos(a), cy + 190 * Math.sin(a), i === 4]; });
  const svg = `<svg width="100%" height="100%" viewBox="0 0 ${W} ${H}">
    ${nodes.map(([x, y, bad]) => `<line x1="${cx}" y1="${cy}" x2="${x}" y2="${y}" stroke="${bad ? C.orange : '#c9d6e4'}" stroke-width="2" ${bad ? 'stroke-dasharray="8 7"' : ''}/>`).join('')}
    <rect x="${cx - 120}" y="${cy - 70}" width="240" height="140" rx="18" fill="${C.brand}"/>
    <text x="${cx}" y="${cy - 12}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="30" fill="#fff">The ledger</text>
    <text x="${cx}" y="${cy + 26}" text-anchor="middle" font-family="Inter" font-size="20" fill="rgba(255,255,255,.8)">one shared record</text>
    ${nodes.map(([x, y, bad]) => `<g transform="translate(${x - 70},${y - 38})"><rect width="140" height="76" rx="14" fill="#fff" stroke="${bad ? C.orange : C.line}" stroke-width="2"/>
      <text x="70" y="32" text-anchor="middle" font-family="Inter" font-weight="700" font-size="18" fill="${bad ? C.orange : C.ink}">${bad ? 'Edited copy' : 'Copy'}</text>
      <text x="70" y="56" text-anchor="middle" font-family="Inter" font-size="16" fill="${bad ? C.orange : C.text2}">${bad ? '✕ rejected' : '✓ matches'}</text></g>`).join('')}
  </svg>`;
  return lightShell(1800, 760, 'Thousands of copies, all in agreement', 'Computers around the world keep the same ledger and check every new entry',
    `<div style="position:absolute;inset:0 0 60px 0">${svg}</div><div style="position:absolute;left:0;right:0;bottom:0;text-align:center;font-size:23px;color:${C.text2}">A copy that doesn't match everyone else's is simply ignored. No single company is in charge, and no one can undo a payment.</div>`);
}
function storySeedWords() {
  const words = ['orbit', 'velvet', 'canyon', 'ladder', 'pilot', 'harvest', 'maple', 'anchor', 'silent', 'ribbon', 'tunnel', 'frost'];
  const chips = words.map((w, i) => `<div style="display:flex;align-items:center;gap:14px;background:#fff;border:1.5px solid ${C.line};border-radius:14px;padding:16px 20px">
    <span style="font-size:18px;font-weight:700;color:${C.blue};width:28px">${i + 1}</span><span style="font-family:'JetBrains Mono',monospace;font-size:28px;color:${C.ink}">${w}</span></div>`).join('');
  return lightShell(1800, 760, 'A seed phrase: 12 words that are your wallet', 'Whoever has these words, in this order, controls every coin in the wallet',
    `<div style="position:absolute;inset:0;display:flex;gap:44px">
      <div style="flex:1.5;position:relative;display:grid;grid-template-columns:repeat(3,1fr);gap:16px;align-content:start">${chips}
        <div style="grid-column:1/-1;justify-self:center;margin-top:26px;transform:rotate(-3deg);padding:10px 30px;border:5px solid ${C.orange};border-radius:14px;color:${C.orange};font-weight:800;font-size:40px;letter-spacing:.08em">EXAMPLE WORDS · NEVER USE THESE</div></div>
      <div style="flex:1;display:flex;flex-direction:column;gap:16px;font-size:23px;color:${C.text}">
        ${[['check', 'Usually 12 or 24 words, from a standard list of 2,048'], ['doc', 'Written on paper or stamped in metal, in order'], ['wallet', 'Restores your wallet on any device, anywhere'], ['alert', 'Never typed, photographed, stored online or shared']].map(([ic, t], i) => `<div style="display:flex;gap:14px;align-items:flex-start;padding:16px 18px;border-radius:14px;background:${i === 3 ? '#fff5ef' : C.panel};border:1.5px solid ${i === 3 ? C.orange : C.line}"><span style="color:${i === 3 ? C.orange : C.blue};flex:none">${icon(ic, 28)}</span><span>${t}</span></div>`).join('')}
      </div></div>`);
}
function storyRoads() {
  const roads = [['Ethereum mainnet', 'The original road: highest security, higher fees', 'layers'], ['Layer 2 “A”', 'A faster, cheaper road built on top of Ethereum', 'swap'], ['Layer 2 “B”', 'Another cheaper road, separate from A', 'swap']];
  const rows = roads.map(([t, s, ic], i) => `<div style="display:flex;align-items:center;gap:24px">
    <div style="width:330px;flex:none;display:flex;align-items:center;gap:14px"><span style="color:${C.blue}">${icon(ic, 32)}</span><div><div style="font-size:26px;font-weight:800;color:${C.ink}">${t}</div><div style="font-size:18px;color:${C.text2}">${s}</div></div></div>
    <div style="flex:1;position:relative;height:66px;border-radius:14px;background:repeating-linear-gradient(90deg,#dfe7f0 0 40px,#eef3f8 40px 80px);border:1.5px solid ${C.line}">
      <div style="position:absolute;left:${[8, 38, 64][i]}%;top:50%;transform:translateY(-50%);display:flex;align-items:center;gap:10px;padding:8px 16px;border-radius:10px;background:${i === 2 ? C.orange : C.blue};color:#fff;font-weight:700;font-size:19px">${icon('coins', 22, '#fff')} ${i === 2 ? 'Sent on the wrong road' : 'Your parcel'}</div>
      <div style="position:absolute;right:14px;top:50%;transform:translateY(-50%);display:flex;align-items:center;gap:8px;font-size:18px;font-weight:700;color:${C.ink}">${icon('wallet', 26, C.brand)} Your address</div></div></div>`).join('');
  return lightShell(1800, 760, 'Networks are separate roads', 'The same address can exist on many roads, but a parcel only travels on the road it was sent on',
    `<div style="position:absolute;inset:0 0 70px 0;display:flex;flex-direction:column;justify-content:center;gap:34px">${rows}</div>
    <div style="position:absolute;left:0;right:0;bottom:0;text-align:center;font-size:23px;color:${C.text2}">Always pick a network that both the sender and your wallet support, and send a small test first. Sending on an unsupported road can mean the money is very hard, or impossible, to get back.</div>`);
}
function storyJourney() {
  const stops = [['0.0', 'Mastery Starter', 'compass'], ['0.1', 'Ledgers & blockchains', 'book'], ['0.2', 'Open & secure an exchange', 'bank'], ['0.3', 'Your first buy', 'coins'],
    ['0.4', 'Who holds the keys', 'key'], ['0.5', 'Wallet & backup', 'wallet'], ['0.6', 'Networks & first transfer', 'swap'], ['0.7', 'First DeFi steps', 'grid'], ['0.8', 'Security baseline', 'shield']];
  const W = 1672, H = 520, pts = stops.map((_, i) => [80 + i * (W - 160) / (stops.length - 1), i % 2 ? 150 : 330]);
  let d = `M${pts[0][0]},${pts[0][1]}`; for (let i = 1; i < pts.length; i++) { const [x0, y0] = pts[i - 1], [x1, y1] = pts[i]; d += ` C${x0 + 80},${y0} ${x1 - 80},${y1} ${x1},${y1}`; }
  const svg = `<svg width="100%" height="100%" viewBox="0 0 ${W} ${H}"><path d="${d}" fill="none" stroke="#c9d6e4" stroke-width="10" stroke-linecap="round" stroke-dasharray="2 18"/>
    ${pts.map(([x, y], i) => `<g transform="translate(${x},${y})"><circle r="42" fill="${i === 0 ? C.aqua : i === stops.length - 1 ? C.brand : '#fff'}" stroke="${i === 0 ? C.aqua : C.brand}" stroke-width="4"/>
      <g transform="translate(-16,-16)" color="${i === 0 || i === stops.length - 1 ? '#fff' : C.blue}">${icon(stops[i][2], 32)}</g>
      <text y="${i % 2 ? -62 : 78}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="22" fill="${C.blue}">${stops[i][0]}</text>
      <text y="${i % 2 ? -88 : 104}" text-anchor="middle" font-family="Inter" font-weight="700" font-size="19" fill="${C.ink}">${stops[i][1]}</text></g>`).join('')}</svg>`;
  return lightShell(1800, 760, 'Your journey through Module 0', 'Nine stops, in order: from knowing nothing to set up safely',
    `<div style="position:absolute;inset:0 0 60px 0">${svg}</div><div style="position:absolute;left:0;right:0;bottom:0;text-align:center;font-size:23px;color:${C.text2}">It ends with the Day-1 Setup Kit ticked off, and you ready for Module 1: Foundations & Safety.</div>`);
}
function storyBlockExplorer() {
  const chrome = `<div style="height:46px;display:flex;align-items:center;gap:10px;padding:0 20px;background:#eef2f6;border-bottom:1px solid ${C.line}">
    <span style="width:13px;height:13px;border-radius:50%;background:#ff5f57"></span><span style="width:13px;height:13px;border-radius:50%;background:#febc2e"></span><span style="width:13px;height:13px;border-radius:50%;background:#28c840"></span>
    <span style="margin-left:14px;flex:1;padding:6px 16px;border-radius:8px;background:#fff;border:1px solid ${C.line};font-size:16px;color:${C.text2};font-family:'JetBrains Mono',monospace">a block explorer (illustrative)</span></div>`;
  const rows = [['0x71C7…976F', '0x3aB1…44E2', '0.10 ETH', 'Confirmed'], ['0x9e02…1bCa', '0x71C7…976F', '2.00 ETH', 'Confirmed'], ['0x44E2…3aB1', '0x8f10…c02d', '0.05 ETH', 'Confirmed']];
  const table = `<div style="border:1px solid ${C.line};border-radius:14px;overflow:hidden">
    <div style="display:grid;grid-template-columns:1.3fr 1.3fr 1fr 1fr;background:${C.panel};padding:14px 20px;font-size:16px;font-weight:700;color:${C.text2}"><span>From</span><span>To</span><span>Value</span><span>Status</span></div>
    ${rows.map(([f, t, v, st]) => `<div style="display:grid;grid-template-columns:1.3fr 1.3fr 1fr 1fr;padding:16px 20px;border-top:1px solid ${C.line};font-family:'JetBrains Mono',monospace;font-size:18px;align-items:center">
      <span style="color:${C.blue}">${f}</span><span style="color:${C.blue}">${t}</span><span style="font-weight:700">${v}</span>
      <span style="display:inline-flex;align-items:center;gap:8px;color:${C.aqua};font-weight:700">${icon('check', 18, C.aqua)} ${st}</span></div>`).join('')}
  </div>`;
  const body = `<div style="border-radius:18px;overflow:hidden;border:1px solid ${C.line};box-shadow:0 20px 50px rgba(20,30,50,.12)">${chrome}
    <div style="padding:26px 28px;background:#fff">
      <div style="display:flex;align-items:baseline;gap:16px;margin-bottom:18px">
        <span style="font-size:15px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:${C.blue}">Block</span>
        <span style="font-size:32px;font-weight:800;color:${C.ink}">#19,204,551</span>
        <span style="font-size:16px;color:${C.text2}">· 3 transactions · sealed 12 seconds ago</span></div>
      ${table}</div></div>`;
  return lightShell(1800, 700, 'What a block explorer shows', 'Anyone can look up any block or transaction, for free',
    `${body}<div style="position:absolute;left:0;right:0;bottom:-6px;text-align:center;font-size:22px;color:${C.text2}">A block explorer just reads the public ledger. It can show you a transaction; it can never undo one.</div>`);
}
function storyTimeline() {
  const stops = [['2008', 'The idea', 'Satoshi Nakamoto publishes the Bitcoin white paper: money with no bank in the middle.'],
    ['2009', 'Bitcoin launches', 'The first block is mined. The first working blockchain, and the first cryptocurrency, BTC.'],
    ['2015', 'Ethereum launches', 'A blockchain that also runs small programs — smart contracts — not just payments.'],
    ['2020s', 'DeFi grows up', 'Lending, trading and stablecoins run by those programs, at real scale.']];
  const W = 1700, seg = W / stops.length;
  const row = stops.map(([y, t, s], i) => `<div style="flex:1;min-width:0;position:relative;padding:0 18px">
    <div style="width:22px;height:22px;border-radius:50%;background:${i === stops.length - 1 ? C.aqua : C.brand};margin:0 0 18px;box-shadow:0 0 0 6px ${C.panel}"></div>
    <div style="font-size:30px;font-weight:800;color:${C.blue}">${y}</div>
    <div style="font-size:22px;font-weight:700;color:${C.ink};margin-top:4px">${t}</div>
    <div style="font-size:17px;color:${C.text2};margin-top:8px;line-height:1.4">${s}</div></div>`).join('');
  return lightShell(1800, 640, 'A short, real timeline', 'Bitcoin, then Ethereum, then DeFi built on top',
    `<div style="position:relative;padding-top:8px">
      <div style="position:absolute;left:18px;right:18px;top:19px;height:3px;background:${C.line}"></div>
      <div style="display:flex">${row}</div></div>`);
}
function storyWalletSend() {
  const chrome = `<div style="height:46px;display:flex;align-items:center;gap:10px;padding:0 20px;background:#eef2f6;border-bottom:1px solid ${C.line}">
    <span style="width:13px;height:13px;border-radius:50%;background:#ff5f57"></span><span style="width:13px;height:13px;border-radius:50%;background:#febc2e"></span><span style="width:13px;height:13px;border-radius:50%;background:#28c840"></span>
    <span style="margin-left:14px;flex:1;padding:6px 16px;border-radius:8px;background:#fff;border:1px solid ${C.line};font-size:16px;color:${C.text2};font-family:'JetBrains Mono',monospace">a wallet's send screen (illustrative)</span></div>`;
  const field = (label, value, mono) => `<div style="margin-bottom:20px"><div style="font-size:15px;font-weight:700;color:${C.text2};margin-bottom:8px">${label}</div>
    <div style="padding:16px 18px;border-radius:12px;background:${C.panel};border:1px solid ${C.line};font-size:${mono ? 22 : 26}px;font-weight:${mono ? 500 : 700};color:${C.ink}${mono ? ";font-family:'JetBrains Mono',monospace" : ''}">${value}</div></div>`;
  const body = `<div style="max-width:820px;margin:0 auto;border-radius:18px;overflow:hidden;border:1px solid ${C.line};box-shadow:0 20px 50px rgba(20,30,50,.12)">${chrome}
    <div style="padding:30px 34px;background:#fff">
      ${field('Send to', "0x3aB1…44E2 (Bob's address)", true)}
      ${field('Amount', '0.10 ETH')}
      ${field('Network fee (gas)', '≈ $1.10', false)}
      <div style="display:flex;justify-content:center;margin-top:10px"><div style="padding:16px 60px;border-radius:14px;background:${C.brand};color:#fff;font-weight:800;font-size:24px">Sign & Send</div></div>
    </div></div>`;
  return lightShell(1800, 800, "Alice's wallet, right before she sends", "She signs an instruction. She never hands over a file, or her keys.",
    `${body}<div style="margin-top:34px;text-align:center;font-size:22px;color:${C.text2}">The wallet asks her to sign; her private key does the signing. Bob never sees it.</div>`);
}
function storyAddressPoisoning() {
  const seg = (t, hi) => `<span style="${hi ? `background:${C.orange};color:#fff;padding:2px 4px;border-radius:6px` : `color:${C.text}`}">${t}</span>`;
  const row = (label, parts, tone) => `<div style="margin-bottom:26px">
    <div style="font-size:17px;font-weight:700;color:${C.text2};margin-bottom:10px">${label}</div>
    <div style="padding:20px 26px;border-radius:14px;background:${C.panel};border:2px solid ${tone === 'bad' ? C.orange : C.line};font-family:'JetBrains Mono',monospace;font-size:32px;letter-spacing:.01em">${parts}</div></div>`;
  const good = seg('0x7a3F') + seg('9c21');
  const bad = seg('0x7a3F') + seg('e0b4…d189', true) + seg('9c21');
  const body = `<div style="max-width:1000px;margin:0 auto">
    ${row('Your usual address (saved in your address book)', good, 'good')}
    ${row('What showed up in your history today', bad, 'bad')}
    <div style="display:flex;align-items:center;gap:14px;padding:16px 20px;border-radius:12px;background:#fff5ef;border:1.5px solid ${C.orange}">
      ${icon('alert', 26, C.orange)}<span style="font-size:19px;color:${C.text}">Same first 4 and last 4 characters. A completely different address in the middle.</span></div>
  </div>`;
  return lightShell(1800, 560, 'Address poisoning, character by character', 'Never copy an address from your history — only from your saved address book',
    body);
}
const STORY_IMAGES = [
  { file: 'story-address-poisoning', w: 1800, h: 560, fn: storyAddressPoisoning },
  { file: 'story-block-explorer', w: 1800, h: 700, fn: storyBlockExplorer },
  { file: 'story-btc-eth-timeline', w: 1800, h: 640, fn: storyTimeline },
  { file: 'story-wallet-send', w: 1800, h: 800, fn: storyWalletSend },

  { file: 'story-chain-of-blocks', w: 1800, h: 560, fn: storyChain },
  { file: 'story-many-copies', w: 1800, h: 760, fn: storyCopies },
  { file: 'story-seed-words', w: 1800, h: 760, fn: storySeedWords },
  { file: 'story-networks-roads', w: 1800, h: 760, fn: storyRoads },
  { file: 'story-module0-journey', w: 1800, h: 760, fn: storyJourney },
  { file: 'story-why-crypto', kind: 'tiles', h: 540, title: 'What crypto makes possible', sub: 'And the responsibility that comes with it', note: 'The same things that make it powerful make mistakes permanent. That is why we start with safety.',
    tiles: [['Send worldwide', 'To anyone, any time, in minutes', 'globe'], ['Hold it yourself', 'No bank needed to keep it', 'wallet'], ['Programmable money', 'Apps that lend, trade and pay by code', 'code'], ['Open rules', 'Anyone can check the record', 'eye']] },
  { file: 'story-mailbox-and-key', kind: 'cols', h: 560, title: 'Your address is a mailbox. Your key opens it.', sub: 'Three things, three different jobs',
    cols: [{ t: 'Address = your mailbox slot', ic: 'globe', lines: ['Share it freely', 'Anyone can send you coins through it', 'Looks like 0x71C7…976F'] },
      { t: 'Private key = the only key', ic: 'key', tone: 'risk', lines: ['Opens the box and signs for you', 'Whoever has it can empty the box', 'Never share it with anyone'] },
      { t: 'Seed phrase = the master recipe', ic: 'doc', tone: 'risk', lines: ['12 or 24 words that recreate every key', 'Your backup if a device is lost', 'Paper or metal, never online'] }] },
  { file: 'story-gas-stamp', kind: 'flow', h: 540, title: 'Gas is the postage stamp', sub: 'Every transaction pays a small fee to the network that delivers it', note: 'Busy roads cost more. The stamp is paid even if the letter comes back undelivered.',
    steps: [['Your letter', 'The transaction you sign', 'doc'], ['The stamp', 'Gas: a small fee in the network’s coin', 'flame'], ['Post office', 'Validators check and order it', 'shield'], ['Delivered', 'Added to a block, final', 'check']] },
  { file: 'story-stablecoin-voucher', kind: 'flow', h: 540, title: 'A stablecoin is a digital dollar voucher', sub: 'Built to stay worth $1, like a voucher backed by cash in a vault', note: 'It’s only as good as the reserves and the issuer behind it. It can still fail.',
    steps: [['$1 in reserve', 'Held by the issuer', 'bank'], ['1 token', 'Issued on the blockchain', 'coins'], ['Moves 24/7', 'Send it like any crypto', 'swap'], ['Redeem', 'Swap back for $1', 'exit']] },
  { file: 'story-vending-machine', kind: 'flow', h: 540, title: 'A smart contract is a vending machine', sub: 'DeFi apps are programs with fixed rules, and no cashier', note: 'It does exactly what its code says. If you press the wrong button, there’s no one to refund you.',
    steps: [['Insert', 'You send coins to it', 'coins'], ['Rules run', 'Code decides what happens', 'code'], ['Output', 'You get the result instantly', 'check'], ['No cashier', 'No refunds, no exceptions', 'alert']] },
  { file: 'story-flight-simulator', kind: 'flow', h: 540, title: 'Practise like a pilot', sub: 'Pilots train in a simulator before they fly passengers', note: 'The test network is your simulator: free, fake money, real buttons.',
    steps: [['Simulator', 'Test network, free test coins', 'compass'], ['Short hop', 'A tiny real amount', 'coins'], ['Check it', 'Did it do what you expected?', 'search'], ['Fly', 'Normal use, same habits', 'check']] },
  { file: 'story-what-can-go-wrong', kind: 'tiles', h: 540, title: 'What goes wrong for beginners', sub: 'Almost every loss starts with one of these four', note: 'Module 0 exists to close all four doors before you move real money.',
    tiles: [['Lost seed phrase', 'No backup, no recovery', 'doc'], ['Wrong network', 'Coins sent on the wrong road', 'swap'], ['Fake sites & support', 'Someone tricks you into signing', 'users'], ['Rushing', 'Urgency and FOMO beat good habits', 'clock']] },
  { file: 'story-bank-vs-you', kind: 'cols', h: 560, title: 'The bank model vs the crypto model', sub: 'Same money idea, different person in charge',
    cols: [{ t: 'Your bank', ic: 'bank', lines: ['Keeps the record for you', 'Can reverse a payment', 'Helps if you forget a password', 'Can freeze your account'] },
      { t: 'Crypto, in your own wallet', ic: 'wallet', tone: 'good', lines: ['The network keeps the record', 'No one can reverse a payment', 'No one can reset your password', 'No one can freeze it but you'] }] },
];
const storyAsset = r => [`diagrams/${r.file}.png`, r.w || 1800, r.h || ({ flow: 640, cols: 760, tiles: 640 }[r.kind]), () => (r.fn ? r.fn() : renderLessonImage(r))];

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
  ['charts/health-factor.png', 1800, 820, chartHF],
  ['diagrams/mev-supply-chain.png', 1800, 700, diagramMEV],
  ...LESSON_IMAGES.map(lessonAsset),
  ...STORY_IMAGES.map(storyAsset),
];

module.exports = { C, FONT, BASE_CSS, network, icon, logoMark, wordmark, lockupStacked, DISCLAIMER, LESSON_IMAGES };

if (require.main === module) (async () => {
  fs.mkdirSync(RENDER, { recursive: true });
  const only = process.argv.slice(2); // one or more name filters; none = everything
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  // Store uploads at exact pixel size; document images at 2x for print sharpness.
  const pages = { 1: await browser.newPage({ deviceScaleFactor: 1 }), 2: await browser.newPage({ deviceScaleFactor: 2 }) };
  for (const [rel, w, h, fn] of ASSETS) {
    if (only.length && !only.some(o => rel.includes(o))) continue;
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
