// Course directory: one offline HTML file that maps the whole program.
// Lessons, pictures, worksheets, calculators and the files they live in.
// Usage: node build_directory.js  ->  ../course-hub/directory.html
// Images are embedded, so the file still shows its pictures with no network
// and no sibling assets folder. Open it in any browser.
const fs = require('fs');
const path = require('path');
const os = require('os');
const crypto = require('crypto');
const { execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'course-hub', 'directory.html');
const read = f => fs.readFileSync(path.join(ROOT, f), 'utf8');
const exists = rel => fs.existsSync(path.join(ROOT, rel));
const pad = n => String(n).padStart(2, '0');

const STAGES = [
  { n: '0', name: 'Zero', can: 'Open and secure an account, buy a small amount, set up and back up a wallet, make a first transfer, and make a first practice DeFi transaction.', mods: [0] },
  { n: '1', name: 'Foundations', can: 'Protect a wallet, read a transaction, and swap or provide liquidity on purpose.', mods: [1, 2] },
  { n: '2', name: 'Practitioner', can: 'Borrow against collateral with a buffer, split yield into what is paid for, and map the infrastructure a position depends on.', mods: [3, 4, 5] },
  { n: '3', name: 'Analyst', can: 'Research any protocol and read on-chain data without over-interpreting it.', mods: [6, 7] },
  { n: '4', name: 'Strategist', can: 'Run the strategy library, engineer fixed and hedged yield, and stress-test a portfolio.', mods: [8, 9, 10, 11] },
  { n: '5', name: 'Operator', can: 'Run capital like a bank: balance sheet, credit line, income engine, and automation that does not take the keys.', mods: [12, 13, 14] },
];

// In-browser forms live in the Course Hub. The command name is the matching
// entry in defi_calc.py, for people who have the course files.
const CALCS = [
  { cmd: 'health', hub: true, lesson: '3.2', name: 'Health factor and liquidation price', what: 'Collateral, liquidation threshold and debt, and the price that liquidates the position.' },
  { cmd: 'il', hub: true, lesson: '2.4', name: 'Impermanent loss', what: 'How far a 50/50 pool falls behind simply holding, before fees.' },
  { cmd: 'lp-breakeven', hub: false, lesson: '2.4', name: 'Fee APR to beat holding', what: 'The fee rate a liquidity position needs over a holding period to match holding both tokens.' },
  { cmd: 'loop', hub: true, lesson: '3.4', name: 'Leveraged loop', what: 'Net yield on equity, and the borrow rate that wipes the extra return out.' },
  { cmd: 'lvr', hub: true, lesson: '2.7', name: 'Loss versus rebalancing', what: 'What arbitrage costs a full-range liquidity position, set against fee income.' },
  { cmd: 'pt', hub: true, lesson: '10.1', name: 'Fixed yield from a principal token', what: 'The fixed rate locked in by buying a principal token at a discount and holding to maturity.' },
  { cmd: 'expected', hub: true, lesson: '13.2', name: 'Risk-adjusted yield', what: 'Headline yield minus expected loss and costs.' },
  { cmd: 'income', hub: true, lesson: '13.4', name: 'Income engine payout', what: 'Expected income after losses, and a payout that leaves a buffer. Illustrative only.' },
  { cmd: 'var', hub: true, lesson: '8.7', name: 'One-day value at risk', what: 'A floor for a bad day on a position. Crypto tails are fatter than the model.' },
  { cmd: 'cl', hub: false, lesson: '10.5', name: 'Concentrated liquidity range', what: 'How much tighter a range concentrates a position, and the risk of leaving the range.' },
  { cmd: 'carry', hub: false, lesson: '10.3', name: 'Funding carry', what: 'What a delta-neutral funding position pays at a given 8-hour rate.' },
  { cmd: 'supply', hub: false, lesson: '3.1', name: 'Supply APY', what: 'Lender yield implied by the borrow rate, utilisation and reserve factor.' },
  { cmd: 'apy', hub: false, lesson: '4.1', name: 'APR, APY and gas', what: 'What compounding turns an APR into, and when gas eats the extra compounds.' },
  { cmd: 'airdrop', hub: false, lesson: '4.6', name: 'Airdrop expected value', what: 'Probability times value, minus the costs of chasing it.' },
  { cmd: 'basis', hub: false, lesson: '10.2', name: 'Cash-and-carry basis', what: 'The annualised gap between spot and a future.' },
  { cmd: 'covered-call', hub: false, lesson: '10.4', name: 'Covered call', what: 'Premium income against the upside you give away.' },
  { cmd: 'bank', hub: false, lesson: '12.1', name: 'Balance sheet', what: 'LTV, health factor and how many months the liquid reserve covers.' },
  { cmd: 'perp', hub: false, lesson: '3.5', name: 'Perp liquidation price', what: 'Approximate liquidation price of an isolated perpetual position.' },
  { cmd: 'twr', hub: false, lesson: '8.5', name: 'Time-weighted return', what: 'Return across periods that is not distorted by deposits and withdrawals.' },
  { cmd: 'cdp', hub: false, lesson: '3.7', name: 'CDP mint', what: 'Collateral ratio and stability fee when minting stablecoins against collateral.' },
];

const ORIENTATION = [
  { file: 'welcome.mp4', name: 'Welcome', about: 'A short welcome. Start here if you have just opened the program.' },
  { file: 'welcome-long.mp4', name: 'Welcome tour', about: 'A longer tour of how the course is organised.' },
  { file: 'how-the-program-works.mp4', name: 'How the program works', about: 'The full walkthrough of stages, tools, worksheets and capstones.' },
  { file: 'day1-kit-guide.mp4', name: 'Day-1 Setup Kit', about: 'Walks the printable setup checklist at the end of Module 0.' },
];

function moduleSource(num) {
  const f = fs.readdirSync(path.join(ROOT, 'lessons')).find(x => x.startsWith(`module-${pad(num)}-`));
  let text = read(`lessons/${f}`);
  if (num === 2) {
    const sample = read('02-sample-lesson-amm-math.md').replace(/\n## /g, '\n### ').replace('# Sample Lesson 2.2', '## Lesson 2.2');
    text = text.replace(/Lesson 2\.2 \(AMM mathematics\) is in `\.\.\/02-sample-lesson-amm-math\.md`\.\n/, '');
    const i = text.indexOf('## Lesson 2.3');
    text = text.slice(0, i) + sample + '\n\n' + text.slice(i);
  }
  return text;
}

const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const plain = s => String(s || '')
  .replace(/!\[[^\]]*\]\([^)]*\)/g, '')
  .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
  .replace(/<[^>]+>/g, ' ')
  .replace(/[*_`#>]+/g, '')
  .replace(/\s+/g, ' ')
  .trim();

function sectionText(body, headingRe) {
  const m = body.match(new RegExp('### ' + headingRe + '\\s*\\n+([\\s\\S]*?)(?=\\n### |\\n## |$)'));
  return m ? plain(m[1]) : '';
}

const images = new Map();
function resolveAsset(href) {
  let clean = String(href || '').trim().replace(/^\.\//, '').replace(/^(\.\.\/)+/, '');
  if (clean.startsWith('programs/defi-program/')) clean = clean.slice('programs/defi-program/'.length);
  if (!clean.startsWith('assets/')) return null;
  const abs = path.join(ROOT, clean);
  if (!fs.existsSync(abs)) return null;
  const id = clean.replace(/[^a-zA-Z0-9]+/g, '-').replace(/^-|-$/g, '');
  return { id, abs, rel: clean };
}
function addImage(href, alt, lessonId) {
  const asset = resolveAsset(href);
  if (!asset) return null;
  let rec = images.get(asset.id);
  if (!rec) {
    rec = { ...asset, alt: plain(alt), lessons: [] };
    images.set(asset.id, rec);
  } else if (!rec.alt && alt) rec.alt = plain(alt);
  if (lessonId && !rec.lessons.includes(lessonId)) rec.lessons.push(lessonId);
  return asset.id;
}

const modules = [];
for (let num = 0; num <= 14; num++) {
  const src = moduleSource(num);
  const title = src.match(/^# Module \d+ — (.+)$/m)[1].trim();
  const outcome = (src.match(/^\*Outcome: (.+?)\*$/m) || [, ''])[1];
  const banner = addImage(`assets/modules/module-${pad(num)}.png`, '', null);
  const intro = exists(`video/module-${pad(num)}-intro.mp4`) ? `../video/module-${pad(num)}-intro.mp4` : '';
  const parts = src.split(/^## Lesson (\d+\.\d+) — (.+)$/m);
  const lessons = [];
  for (let i = 1; i < parts.length; i += 3) {
    const lid = parts[i];
    const rawTitle = parts[i + 1].trim();
    const expert = /\*\(expert\)\*/i.test(rawTitle);
    const ltitle = rawTitle.replace(/\s*\*\(.*?\)\*\s*$/, '').replace(/\s+/g, ' ').trim();
    const body = parts[i + 2].split(/\n### Module /)[0].replace(/\n---\s*$/g, '').trim();
    const starter = lid.endsWith('.0');
    let blurb = starter
      ? (sectionText(body, 'The 60-second version') || sectionText(body, 'Objective'))
      : (sectionText(body, 'Objective') || sectionText(body, 'The 60-second version'));
    if (!blurb) blurb = plain(body).slice(0, 360);
    const mastered = starter ? sectionText(body, "You.ve mastered this module when[.…]*") : '';
    let primary = null;
    for (const m of body.matchAll(/!\[([^\]]*)\]\(([^)]+)\)/g)) {
      const id = addImage(m[2], m[1], lid);
      if (!id) continue;
      const isBanner = images.get(id).rel.includes('/modules/');
      if (!primary) primary = id;
      else if (images.get(primary).rel.includes('/modules/') && !isBanner) primary = id;
    }
    if (lid === '8.3' && (!primary || images.get(primary).rel.includes('/modules/'))) {
      const lib = read('03-defi-strategy-mastery.md');
      const im = lib.match(/!\[([^\]]*)\]\(([^)]+)\)/);
      if (im) {
        const id = addImage(im[2], im[1], lid);
        if (id) primary = id;
      }
      if (!/thirty strategies/i.test(blurb)) {
        blurb = 'Name where a strategy’s return comes from, the maths that tests it, how to run it, and how it loses money. Thirty strategies, in seven levels.';
      }
    }
    const vid = `lesson-${lid.split('.')[0].padStart(2, '0')}-${lid.split('.')[1]}`;
    lessons.push({
      id: lid, title: starter ? 'Mastery Starter' : ltitle, starter, expert, blurb, mastered, primary,
      hay: plain(body).slice(0, 3500),
      video: exists(`video/${vid}.mp4`) ? `../video/${vid}.mp4` : '',
    });
  }
  lessons.sort((a, b) => a.id.split('.').map(Number)[1] - b.id.split('.').map(Number)[1]);
  const mastered = (lessons.find(l => l.starter) || {}).mastered || '';
  modules.push({ n: num, title, outcome, banner, intro, mastered, lessons });
}
addImage('assets/diagrams/path-to-mastery.png', 'Six stages from Zero to Operator', null);
const pathImg = resolveAsset('assets/diagrams/path-to-mastery.png').id;

const allLessons = modules.flatMap(m => m.lessons.map(l => ({ ...l, module: m })));
const lessonCount = allLessons.length;
const expertCount = allLessons.filter(l => l.expert).length;
const starterCount = allLessons.filter(l => l.starter).length;

function lessonLink(id, label) {
  return `<a href="index.html#/l/${esc(id)}">${esc(label || 'Lesson ' + id)}</a>`;
}

const wsRaw = read('08-worksheets.md');
const wsRefs = wsRaw.split(/\n(?=## )/).filter(s => s.startsWith('## ')).map(chunk => {
  const title = chunk.split('\n')[0].replace(/^## /, '').trim();
  return {
    id: (title.match(/W\d+/) || ['Worksheet'])[0],
    lesson: (title.match(/Lesson (\d+\.\d+)/) || [, ''])[1],
    mod: (title.match(/Module (\d+)/) || [, ''])[1],
    name: title.replace(/^W\d+\s·\s*/, '').replace(/\s*\(.*$/, '').trim(),
  };
});
function sheetLink(w) {
  return `<a href="#${w.id.toLowerCase()}">${esc(w.id)} ${esc(w.name)}</a>`;
}

function lessonBlock(l) {
  const img = l.primary ? images.get(l.primary) : null;
  const flag = l.starter ? '<span class="flag start">Start here</span>' : l.expert ? '<span class="flag">Expert</span>' : '';
  const videoWord = l.video ? '<span class="hasvid">Video</span>' : '';
  const sheets = wsRefs.filter(w => w.lesson === l.id);
  const find = plain([l.id, l.title, l.blurb, l.hay, l.module.title, l.module.outcome, img ? img.alt : '', sheets.map(w => w.id + ' ' + w.name).join(' '), l.starter ? 'mastery starter' : '', l.expert ? 'expert' : ''].join(' ')).toLowerCase();
  const moreImg = img ? `<img data-img="${esc(img.id)}" alt="${esc(img.alt || l.title)}" width="800">` : '';
  const sheetWord = sheets.length ? `<span class="sheet">${esc(sheets.map(w => w.id).join(' '))}</span>` : '';
  const links = [
    `<a class="go" href="index.html#/l/${esc(l.id)}">Open in Course Hub</a>`,
    l.video ? `<a href="${esc(l.video)}">Video file</a>` : '',
    sheets.map(sheetLink).join(''),
  ].filter(Boolean).join(' · ');
  return `<details class="lesson" id="l-${l.id.replace('.', '-')}" data-kind="${l.starter ? 'starter' : l.expert ? 'expert' : 'lesson'}" data-find="${esc(find)}">
    <summary>
      <span class="lid">${esc(l.id)}</span>
      <span class="ltext"><span class="ltitle">${esc(l.title)}${flag}${videoWord}${sheetWord}</span><span class="ldesc">${esc(l.blurb)}</span></span>
      ${img ? `<img data-img="${esc(img.id)}" alt="" width="140" height="78">` : '<span class="nopic"></span>'}
    </summary>
    <div class="more">${moreImg}<p class="links">${links}</p></div>
  </details>`;
}

function moduleBlock(m) {
  const banner = m.banner ? `<img class="banner" data-img="${esc(m.banner)}" alt="" width="1000">` : '';
  const intro = m.intro ? `<a href="${esc(m.intro)}">Intro video</a>` : '';
  const hub = `<a href="index.html#/m/${m.n}">Open module in Course Hub</a>`;
  const modSheets = wsRefs.filter(w => !w.lesson && w.mod === String(m.n)).map(sheetLink).join('');
  return `<article class="module" id="m-${m.n}">
    ${banner}
    <h3>Module ${m.n} — ${esc(m.title)}</h3>
    <p class="outcome">${esc(m.outcome)}</p>
    ${m.mastered ? `<p class="mastered">You have finished this module when ${esc(m.mastered.replace(/^[.…\s]+/, ''))}</p>` : ''}
    <p class="links">${[hub, intro, modSheets].filter(Boolean).join(' · ')}</p>
    ${m.lessons.map(l => lessonBlock({ ...l, module: m })).join('\n')}
  </article>`;
}

function inline(s) {
  return esc(s)
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
}
function mdBlocks(text) {
  const lines = text.replace(/\r/g, '').split('\n');
  let html = '';
  let i = 0;
  const isSep = cells => cells.every(c => /^:?-+:?$/.test(c));
  while (i < lines.length) {
    if (!lines[i].trim()) { i++; continue; }
    if (lines[i].trim().startsWith('|')) {
      const rows = [];
      while (i < lines.length && lines[i].trim().startsWith('|')) {
        const cells = lines[i].trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(c => c.trim());
        if (!isSep(cells)) rows.push(cells);
        i++;
      }
      if (!rows.length) continue;
      const [head, ...rest] = rows;
      html += '<div class="tablewrap"><table><thead><tr>' + head.map(c => `<th>${inline(c)}</th>`).join('') + '</tr></thead><tbody>'
        + rest.map(r => '<tr>' + r.map(c => `<td>${inline(c) || ' '}</td>`).join('') + '</tr>').join('')
        + '</tbody></table></div>';
    } else if (/^[-*] /.test(lines[i])) {
      const items = [];
      while (i < lines.length && /^[-*] /.test(lines[i])) { items.push(lines[i].replace(/^[-*] /, '')); i++; }
      html += '<ul>' + items.map(it => `<li>${inline(it)}</li>`).join('') + '</ul>';
    } else if (lines[i].startsWith('### ')) {
      html += `<h4>${inline(lines[i].replace(/^### /, ''))}</h4>`;
      i++;
    } else {
      const para = [];
      while (i < lines.length && lines[i].trim() && !lines[i].trim().startsWith('|') && !/^[-*] /.test(lines[i]) && !lines[i].startsWith('#')) {
        para.push(lines[i].trim());
        i++;
      }
      html += `<p>${inline(para.join(' '))}</p>`;
    }
  }
  return html;
}

const wsIntro = plain(wsRaw.split(/^## /m)[0].replace(/^#[^\n]*\n/, ''));
const worksheets = wsRaw.split(/\n(?=## )/).filter(s => s.startsWith('## ')).map(chunk => {
  const lines = chunk.split('\n');
  const title = lines[0].replace(/^## /, '').trim();
  const id = (title.match(/W\d+/) || ['Worksheet'])[0];
  const lesson = (title.match(/Lesson (\d+\.\d+)/) || [, ''])[1];
  const mod = (title.match(/Module (\d+)/) || [, ''])[1];
  const body = lines.slice(1).join('\n').trim();
  const find = plain(title + ' ' + body + ' worksheet ' + id).toLowerCase();
  const where = lesson ? lessonLink(lesson, 'Used in lesson ' + lesson) : mod ? `<a href="index.html#/m/${mod}">Used in module ${mod}</a>` : '';
  return `<article class="worksheet" id="${id.toLowerCase()}" data-find="${esc(find)}">
    <header><h3>${esc(title)}</h3><p class="links">${where}<button type="button" class="copy">Copy worksheet</button></p></header>
    <div class="wsbody">${mdBlocks(body)}</div>
    <pre class="plain" hidden>${esc(chunk.trim())}</pre>
  </article>`;
});

function pictureCard(rec) {
  const used = rec.lessons.map(id => lessonLink(id, id)).join(', ');
  const find = plain((rec.alt || rec.rel) + ' ' + rec.lessons.join(' ') + ' picture diagram chart').toLowerCase();
  return `<figure data-find="${esc(find)}">
    <img data-img="${esc(rec.id)}" alt="${esc(rec.alt || 'Course diagram')}" width="800">
    <figcaption><b>${esc(rec.alt || rec.rel.split('/').pop())}</b>${used ? `<span>Lesson ${used}</span>` : ''}</figcaption>
  </figure>`;
}

const pictureGroups = modules.map(m => {
  const figs = [];
  const seen = new Set();
  for (const l of m.lessons) {
    for (const rec of images.values()) {
      if (!rec.lessons.includes(l.id) || seen.has(rec.id)) continue;
      if (rec.rel.includes('/modules/')) continue;
      seen.add(rec.id);
      figs.push(rec);
    }
  }
  if (!figs.length) return '';
  return `<details class="pics" id="pics-${m.n}">
    <summary>Module ${m.n} — ${esc(m.title)} <span>${figs.length} picture${figs.length === 1 ? '' : 's'}</span></summary>
    <div class="gallery">${figs.map(pictureCard).join('')}</div>
  </details>`;
}).join('\n');

const chartFigs = [...images.values()].filter(r => r.rel.includes('/charts/'));
const chartsBlock = chartFigs.length
  ? `<details class="pics" id="pics-charts"><summary>Charts <span>${chartFigs.length}</span></summary><div class="gallery">${chartFigs.map(pictureCard).join('')}</div></details>`
  : '';

const calcRows = CALCS.map(c => {
  const find = plain(c.cmd + ' ' + c.name + ' ' + c.what + ' calculator lesson ' + c.lesson).toLowerCase();
  const hub = c.hub ? `<a href="index.html#/tools">Open the form</a>` : '<span class="quiet">In the course files</span>';
  return `<div class="calc" data-find="${esc(find)}">
    <h3>${esc(c.name)}</h3>
    <p>${esc(c.what)}</p>
    <p class="links">${lessonLink(c.lesson, 'Lesson ' + c.lesson)} · ${hub}${c.hub ? '' : ` · <code>${esc(c.cmd)}</code>`}</p>
  </div>`;
}).join('\n');

const orientation = ORIENTATION.filter(v => exists('video/' + v.file)).map(v =>
  `<li><a href="../video/${esc(v.file)}">${esc(v.name)}</a> — ${esc(v.about)}</li>`
).join('');

const rail = STAGES.map(s => {
  const mods = s.mods.map(n => {
    const m = modules[n];
    return `<a class="modlink" href="#m-${n}" data-spy="m-${n}">${n} ${esc(m.title)}</a>`;
  }).join('');
  return `<a class="stagelink" href="#stage-${s.n}" data-spy="stage-${s.n}">Stage ${s.n} · ${esc(s.name)}</a>${mods}`;
}).join('');

const stagesHtml = STAGES.map(s => {
  const body = s.mods.map(n => moduleBlock(modules[n])).join('\n');
  return `<section class="stage-block" id="stage-${s.n}">
    <h2>Stage ${s.n} · ${esc(s.name)}</h2>
    <p class="stage-can">${esc(s.can)}</p>
    ${body}
  </section>`;
}).join('\n');

const FILES = [
  ['This directory', 'directory.html', 'The map you are reading. Search, or walk the stages.'],
  ['Course Hub', 'index.html', 'Every lesson with its video, checklist, quiz, and your progress. Saved in this browser only.'],
  ['Day-1 Setup Kit', '../Day-1-Setup-Kit.pdf', 'Printable checklist from Module 0. The written version is Day-1-Setup-Kit.md.'],
  ['Full program book', '../On-Chain-Operator-Program.pdf', 'The same course as one document, with diagrams.'],
  ['Written lessons', '../lessons/', 'One markdown file per module. Lesson 2.2 is also in 02-sample-lesson-amm-math.md. Lesson 8.3 is 03-defi-strategy-mastery.md.'],
  ['Worksheets', '../08-worksheets.md', 'The same 17 templates as the Worksheets section of this page.'],
  ['Topic map', '../09-mastery-map.md', 'Every subject, the lesson that teaches it, and the level: beginner, practitioner, or master.'],
  ['Curriculum', '../01-offer-and-curriculum.md', 'Stages, modules, lesson titles, and what each stage leaves you able to do.'],
  ['Diagrams', '../assets/diagrams/', 'The pictures inside lessons. Also collected in Pictures on this page.'],
  ['Charts', '../assets/charts/', 'The number pictures: health factor, impermanent loss, yield, and the rest.'],
  ['Module banners', '../assets/modules/', 'The plate at the top of each module.'],
  ['Videos', '../video/', 'Lesson films, module intros, welcome, and the program walkthrough. Captions are in video/captions/ and chapters in video/chapters/.'],
  ['Calculator', '../../.claude/skills/defi-strategies/scripts/defi_calc.py', 'The same formulas as the Course Hub forms, plus the rest of the command list.'],
];

const filesHtml = FILES.map(([name, href, about]) => {
  const find = plain(name + ' ' + href + ' ' + about).toLowerCase();
  return `<tr data-find="${esc(find)}"><th><a href="${esc(href)}">${esc(name)}</a></th><td><code>${esc(href.replace(/^\.\.\//, ''))}</code></td><td>${esc(about)}</td></tr>`;
}).join('');

const LOGO = `<svg class="mark" width="36" height="36" viewBox="0 0 200 200" aria-hidden="true">
  <path d="M176 144 L100 188 L24 144 L24 56 L100 12 L176 56 Z" fill="none" stroke="#7dffe0" stroke-width="8"/>
  <circle cx="78" cy="100" r="30" fill="none" stroke="#fff" stroke-width="12"/>
  <circle cx="122" cy="100" r="30" fill="none" stroke="#7eb6ff" stroke-width="12"/>
</svg>`;

const css = `
:root {
  --ink: #07111c;
  --paper: #f3f6f8;
  --text: #14202b;
  --muted: #3e4c59;
  --line: #d3dde6;
  --link: #0a5c48;
  --warn: #9a3412;
  --warnbg: #f8efea;
  --teal: #8ef6d4;
  --mono: "JetBrains Mono", "Cascadia Mono", ui-monospace, monospace;
  --sans: Inter, "Segoe UI", "Helvetica Neue", system-ui, sans-serif;
  color-scheme: light;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
body { margin: 0; background: var(--paper); color: var(--text); font-family: var(--sans); font-size: 17px; line-height: 1.5; }
[hidden] { display: none !important; }
img { max-width: 100%; height: auto; }
a { color: var(--link); text-underline-offset: 2px; }
:focus-visible { outline: 2px solid var(--link); outline-offset: 3px; }
.skip { position: absolute; left: 12px; top: -48px; background: #fff; color: var(--ink); padding: 8px 12px; z-index: 40; }
.skip:focus { top: 8px; }
.top { position: sticky; top: 0; z-index: 20; background: var(--ink); color: #f4f7fa; }
.mast { display: flex; align-items: center; gap: 16px; padding: 12px 22px 8px; }
.brand { display: flex; align-items: center; gap: 10px; color: inherit; text-decoration: none; min-width: 0; }
.brand b { display: block; font-size: 13px; letter-spacing: 0.04em; font-weight: 750; }
.brand b i { font-style: normal; color: var(--teal); }
.brand small { display: block; color: #b7c6d6; font-size: 13px; font-weight: 500; }
.search { margin-left: auto; width: min(440px, 46vw); position: relative; }
.search input { width: 100%; font: inherit; font-size: 15px; color: #fff; background: #122433; border: 1px solid #31485f; border-radius: 4px; padding: 9px 12px; }
.search input::placeholder { color: #8aa0b5; }
.visually-hidden { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); border: 0; }
.jumps { display: flex; gap: 2px; padding: 0 14px; overflow-x: auto; background: var(--ink); }
.jumps a { color: #d5e2ee; text-decoration: none; font-weight: 650; font-size: 14.5px; padding: 10px 12px 12px; border-bottom: 2px solid transparent; white-space: nowrap; }
.jumps a:hover, .jumps a[aria-current="true"] { color: var(--teal); border-bottom-color: var(--teal); }
.top :focus-visible { outline-color: var(--teal); }
.shell { display: grid; grid-template-columns: 248px minmax(0, 1fr); align-items: start; }
.rail { position: sticky; top: 104px; max-height: calc(100vh - 104px); overflow: auto; background: var(--ink); color: #d5e2ee; padding: 16px 10px 48px 14px; }
.rail a { display: block; color: #c5d5e4; text-decoration: none; padding: 5px 8px; font-size: 13.5px; line-height: 1.35; border-left: 2px solid transparent; }
.rail a.stagelink { color: #f4f7fa; font-weight: 700; margin-top: 12px; }
.rail a.modlink { color: #a9bcce; padding-left: 16px; }
.rail a[aria-current="true"] { border-left-color: var(--teal); color: #fff; background: rgba(255,255,255,.06); }
.rail :focus-visible { outline-color: var(--teal); }
.main { padding: 28px 36px 96px; max-width: 980px; }
h1 { font-size: clamp(32px, 4vw, 44px); line-height: 1.12; letter-spacing: -0.03em; font-weight: 720; margin: 0 0 10px; max-width: 18ch; }
h2 { font-size: 28px; letter-spacing: -0.02em; margin: 0 0 8px; }
h3 { font-size: 22px; letter-spacing: -0.02em; margin: 14px 0 6px; }
.lede, .stage-can, .outcome, .mastered { max-width: 66ch; }
.lede { font-size: 18.5px; margin: 0 0 18px; }
.stage-can, .mastered, .quiet { color: var(--muted); }
.mastered { margin-top: 0; }
.path { display: block; width: 100%; background: var(--ink); margin: 8px 0 22px; }
.steps { margin: 0 0 8px; padding-left: 1.2em; max-width: 66ch; }
.steps li { margin: 6px 0; }
.safety { max-width: 68ch; margin: 20px 0 8px; padding: 12px 14px; background: var(--warnbg); border-left: 4px solid var(--warn); color: #3b241c; }
.safety p { margin: 0; }
.vids { max-width: 68ch; }
#count { color: var(--muted); font-variant-numeric: tabular-nums; }
.filters { display: flex; flex-wrap: wrap; gap: 8px; margin: 8px 0 18px; }
.filters button, button.copy { font: inherit; font-size: 14.5px; background: transparent; color: var(--text); border: 1px solid #b7c6d4; padding: 6px 12px; cursor: pointer; }
.filters button[aria-pressed="true"] { background: var(--ink); color: #fff; border-color: var(--ink); }
.stage-block { margin-top: 42px; }
.stage-block > h2 { padding-top: 8px; }
.module { margin: 28px 0 10px; scroll-margin-top: 120px; }
.stage-block, .worksheet, section, .pics { scroll-margin-top: 120px; }
.banner { display: block; width: 100%; background: var(--ink); }
.links { font-size: 15px; }
.links .go { font-weight: 700; }
.lesson { border-top: 1px solid var(--line); scroll-margin-top: 120px; }
.lesson summary { display: grid; grid-template-columns: 3.4rem minmax(0, 1fr) 140px; gap: 8px 14px; align-items: center; padding: 12px 0; cursor: pointer; list-style: none; }
.lesson summary::-webkit-details-marker { display: none; }
.lesson summary:hover .ltitle { text-decoration: underline; text-underline-offset: 2px; }
.lid { font-family: var(--mono); font-size: 13.5px; font-weight: 600; color: var(--link); font-variant-numeric: tabular-nums; }
.ltitle { font-weight: 680; }
.ldesc { display: block; color: var(--muted); font-size: 15px; margin-top: 3px; }
.flag { font-weight: 680; font-size: 14px; margin-left: 8px; color: var(--warn); }
.flag.start { color: var(--link); }
.hasvid, .sheet { margin-left: 8px; color: var(--muted); font-weight: 600; font-size: 14px; }
.sheet { color: var(--link); }
.lesson summary img, .nopic { width: 140px; height: 78px; object-fit: cover; background: var(--ink); display: block; }
.more { padding: 0 0 18px 4.3rem; }
.more img { display: block; width: min(100%, 720px); background: var(--ink); margin-bottom: 10px; }
.more p { max-width: 66ch; margin: 8px 0; }
.worksheet { border-top: 1px solid var(--line); padding: 18px 0 8px; }
.worksheet header { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px 16px; align-items: baseline; }
.worksheet h3 { margin-top: 0; }
.wsbody { max-width: 78ch; }
.tablewrap { overflow-x: auto; margin: 10px 0 16px; }
table { width: 100%; border-collapse: collapse; font-size: 14.5px; }
th, td { text-align: left; vertical-align: top; padding: 8px 10px; border-bottom: 1px solid var(--line); }
th { font-weight: 680; }
code { font-family: var(--mono); font-size: 0.86em; }
.pics { border-top: 1px solid var(--line); padding: 8px 0; }
.pics summary { cursor: pointer; font-weight: 700; font-size: 18px; padding: 10px 0; }
.pics summary span { color: var(--muted); font-weight: 550; font-size: 15px; margin-left: 8px; }
.gallery { display: grid; grid-template-columns: 1fr 1fr; gap: 22px 16px; padding-bottom: 16px; }
.gallery figure { margin: 0; }
.gallery img { display: block; width: 100%; background: var(--ink); }
.gallery figcaption { margin-top: 6px; font-size: 14.5px; }
.gallery figcaption span { display: block; color: var(--muted); }
.calcs { display: grid; gap: 0; }
.calc { border-top: 1px solid var(--line); padding: 14px 0; }
.calc h3 { margin: 0 0 4px; font-size: 18px; }
.calc p { margin: 0 0 6px; max-width: 66ch; }
#files table code { color: var(--muted); }
footer { margin-top: 36px; color: var(--muted); font-size: 14.5px; max-width: 68ch; }
@media (max-width: 860px) {
  .shell { grid-template-columns: 1fr; }
  .rail { position: sticky; top: 96px; max-height: none; display: flex; gap: 0; overflow-x: auto; padding: 0 8px; }
  .rail a { white-space: nowrap; border-left: 0; border-bottom: 2px solid transparent; padding: 10px 12px; }
  .rail a.modlink { display: none; }
  .rail a.stagelink { margin: 0; }
  .main { padding: 22px 16px 72px; }
  .search { width: min(240px, 42vw); }
  .gallery { grid-template-columns: 1fr; }
  .lesson summary { grid-template-columns: 2.8rem minmax(0, 1fr) 92px; gap: 8px; }
  .lesson summary img, .nopic { width: 92px; height: 52px; }
  .more { padding-left: 0; }
}
@media (max-width: 560px) {
  .mast { flex-wrap: wrap; }
  .search { width: 100%; margin-left: 0; }
}
`;

const js = `
const IMG = JSON.parse(document.getElementById('imgdata').textContent);
document.querySelectorAll('[data-img]').forEach(el => { if (IMG[el.dataset.img]) el.src = IMG[el.dataset.img]; });
const q = document.getElementById('q');
const empty = document.getElementById('empty');
const count = document.getElementById('count');
const lessons = [...document.querySelectorAll('.lesson')];
const blocks = [...document.querySelectorAll('[data-find]')];
let mode = 'all';
function words() { return q.value.toLowerCase().trim().split(/\\s+/).filter(Boolean); }
function apply() {
  const w = words();
  const searching = w.length > 0;
  lessons.forEach(el => {
    const kindOk = mode === 'all' || el.dataset.kind === mode;
    const textOk = !searching || w.every(x => el.dataset.find.includes(x));
    el.hidden = !(kindOk && textOk);
  });
  blocks.forEach(el => {
    if (el.classList.contains('lesson')) return;
    const textOk = !searching || w.every(x => el.dataset.find.includes(x));
    el.hidden = !textOk;
    const d = el.closest('details.pics');
    if (d && textOk && searching) { if (!d.open) { d.open = true; d.dataset.searchOpen = '1'; } }
  });
  if (!searching) document.querySelectorAll('details[data-search-open]').forEach(d => { d.open = false; delete d.dataset.searchOpen; });
  document.querySelectorAll('.module').forEach(m => {
    m.hidden = [...m.querySelectorAll('.lesson')].every(l => l.hidden);
  });
  document.querySelectorAll('details.pics').forEach(d => {
    const figs = [...d.querySelectorAll('figure')];
    d.hidden = searching && figs.every(f => f.hidden);
  });
  document.querySelectorAll('.stage-block').forEach(s => {
    s.hidden = [...s.querySelectorAll('.module')].every(m => m.hidden);
  });
  ['worksheets','pictures','calculators','files'].forEach(id => {
    const sec = document.getElementById(id);
    if (!sec) return;
    const rows = [...sec.querySelectorAll('[data-find]')].filter(el => !el.classList.contains('lesson'));
    sec.hidden = searching && rows.length > 0 && rows.every(el => el.hidden);
  });
  const shown = lessons.filter(l => !l.hidden).length;
  const focusResults = searching || mode !== 'all';
  document.getElementById('intro').hidden = focusResults;
  count.textContent = focusResults ? shown + ' of ' + lessons.length + ' lessons' : lessons.length + ' lessons';
  const key = mode + '\\n' + q.value;
  if (apply.last !== undefined && apply.last !== key && focusResults) {
    const target = shown
      ? document.getElementById('lessons')
      : document.querySelector('.worksheet:not([hidden]), #pictures figure:not([hidden]), .calc:not([hidden]), #files tr:not([hidden])');
    if (target) target.scrollIntoView({ block: 'start' });
  }
  apply.last = key;
  const any = shown || ['worksheets','pictures','calculators','files'].some(id => {
    const sec = document.getElementById(id);
    return sec && !sec.hidden && [...sec.querySelectorAll('[data-find]')].some(el => !el.hidden);
  });
  empty.hidden = any || (!searching && mode === 'all');
}
document.querySelectorAll('.filters button').forEach(b => b.addEventListener('click', () => {
  mode = b.dataset.mode;
  document.querySelectorAll('.filters button').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
  apply();
}));
q.addEventListener('input', apply);
document.querySelectorAll('button.copy').forEach(b => b.addEventListener('click', async () => {
  const pre = b.closest('.worksheet').querySelector('pre.plain');
  try {
    await navigator.clipboard.writeText(pre.textContent);
    const old = b.textContent;
    b.textContent = 'Copied';
    setTimeout(() => { b.textContent = old; }, 1600);
  } catch (e) {
    b.textContent = 'Select the worksheet and copy it';
  }
}));
addEventListener('keydown', e => {
  if (e.key === '/' && document.activeElement !== q) { e.preventDefault(); q.focus(); }
});
const spies = [...document.querySelectorAll('[data-spy]')];
const watch = [...document.querySelectorAll('.stage-block, .module')];
if ('IntersectionObserver' in window) {
  const io = new IntersectionObserver(entries => {
    const vis = entries.filter(e => e.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (!vis) return;
    const id = vis.target.id;
    spies.forEach(a => a.setAttribute('aria-current', a.dataset.spy === id ? 'true' : 'false'));
    const stage = vis.target.closest('.stage-block');
    document.querySelectorAll('.jumps a').forEach(a => {
      const onLessons = location.hash.startsWith('#stage-') || location.hash.startsWith('#m-') || location.hash.startsWith('#l-') || !location.hash;
      if (a.getAttribute('href') === '#lessons') a.setAttribute('aria-current', stage && onLessons ? 'true' : 'false');
    });
  }, { rootMargin: '-20% 0px -65% 0px', threshold: [0.1, 0.4] });
  watch.forEach(el => io.observe(el));
}
const openHash = () => {
  const id = location.hash.slice(1);
  const el = id && document.getElementById(id);
  if (el && el.tagName === 'DETAILS') el.open = true;
};
addEventListener('hashchange', openHash);
openHash();
apply();
`;

const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>On-Chain Operator · Course directory</title>
<meta name="description" content="A directory of the On-Chain Operator Program: every stage, module, lesson, picture, worksheet and calculator, and where to find each one. Works offline.">
<link rel="icon" href="../assets/brand/favicon-256.png">
<style>${css}</style>
</head>
<body>
<a class="skip" href="#lessons">Skip to lessons</a>
<div class="top">
  <header class="mast">
    <a class="brand" href="#start">${LOGO}<span><b>ON-CHAIN <i>OPERATOR</i></b><small>Course directory</small></span></a>
    <form class="search" role="search" action="#lessons" onsubmit="return false">
      <label class="visually-hidden" for="q">Search the course</label>
      <input id="q" type="search" placeholder="Search lessons, pictures, worksheets" autocomplete="off" enterkeyhint="search">
    </form>
  </header>
  <nav class="jumps" aria-label="Directory sections">
    <a href="#start">Start</a>
    <a href="#lessons">Lessons</a>
    <a href="#worksheets">Worksheets</a>
    <a href="#pictures">Pictures</a>
    <a href="#calculators">Calculators</a>
    <a href="#files">Where things live</a>
  </nav>
</div>
<div class="shell">
  <nav class="rail" aria-label="Stages and modules">${rail}</nav>
  <main class="main" id="start">
    <div id="intro">
    <h1>Find any part of the course.</h1>
    <p class="lede">Six stages, 15 modules, ${lessonCount} lessons. This page is the map: what each lesson teaches, the picture that goes with it, and where the worksheets, videos and calculators are.</p>
    <img class="path" data-img="${esc(pathImg)}" alt="Six stages in order: Zero, Foundations, Practitioner, Analyst, Strategist, Operator." width="1200">
    <ol class="steps">
      <li>Pick a stage in the list, or search for a topic or a lesson number.</li>
      <li>Read the line. Open the lesson in the Course Hub when you want the video, the checklist and the quiz.</li>
      <li>Copy the matching worksheet into your own notes. Leave every secret out of it.</li>
    </ol>
    <div class="safety">
      <p>Educational content only. Not financial, tax or legal advice. Digital assets are volatile and you can lose some or all of your capital. No results or income are promised. Never enter a seed phrase, private key, API key or password into this directory, the Course Hub, or any worksheet. This program will not ask for them.</p>
    </div>
    <h2>Films to start with</h2>
    <ul class="vids">${orientation}</ul>
    <p class="links"><a href="index.html">Open the Course Hub</a> for the lessons themselves. Progress, ticks and quiz marks stay in that browser.</p>
    </div>

    <section id="lessons">
      <h2>Lessons</h2>
      <p id="count">${lessonCount} lessons</p>
      <div class="filters" role="group" aria-label="Filter lessons">
        <button type="button" data-mode="all" aria-pressed="true">All lessons</button>
        <button type="button" data-mode="starter" aria-pressed="false">Mastery starters (${starterCount})</button>
        <button type="button" data-mode="expert" aria-pressed="false">Expert lessons (${expertCount})</button>
      </div>
      <p id="empty" hidden>Nothing matches that search. Try a lesson number such as 3.2, or a topic such as wallet, health factor, or worksheet.</p>
      ${stagesHtml}
    </section>

    <section id="worksheets">
      <h2>Worksheets</h2>
      <p class="lede">${esc(wsIntro)}</p>
      ${worksheets.join('\n')}
    </section>

    <section id="pictures">
      <h2>Pictures</h2>
      <p class="lede">Every diagram and chart used in a lesson. Open a module to see them. The same pictures sit inside the lesson in the Course Hub.</p>
      ${pictureGroups}
      ${chartsBlock}
    </section>

    <section id="calculators">
      <h2>Calculators</h2>
      <p class="lede">Eight of these are forms in the Course Hub. The rest use the same formulas in the course files. Numbers are for learning. They are not a forecast and not a promise of income.</p>
      <div class="calcs">${calcRows}</div>
    </section>

    <section id="files">
      <h2>Where things live</h2>
      <p class="lede">Open this file from the course folder and these links resolve next to it. If you only downloaded this one file, the pictures on the page are already inside it. The videos and the Course Hub are the other files in the same folder.</p>
      <div class="tablewrap"><table>
        <thead><tr><th>What</th><th>File</th><th>Use it for</th></tr></thead>
        <tbody>${filesHtml}</tbody>
      </table></div>
    </section>

    <footer>
      <p>On-Chain Operator Program. Educational content only. Not financial, tax or legal advice. No results or income are promised. Never type a seed phrase, private key, API key or password into a worksheet or into this page.</p>
    </footer>
  </main>
</div>
<script type="application/json" id="imgdata">__IMG__</script>
<script>${js}</script>
</body>
</html>`;

function jpegDataUri(abs, width) {
  const st = fs.statSync(abs);
  const key = crypto.createHash('sha1').update(`${abs}:${st.mtimeMs}:${width}`).digest('hex');
  const out = path.join(os.tmpdir(), `ocdir-${key}.jpg`);
  if (!fs.existsSync(out)) {
    execFileSync('ffmpeg', ['-y', '-i', abs, '-vf', `scale=${width}:-1`, '-q:v', '6', out], { stdio: 'ignore' });
  }
  return 'data:image/jpeg;base64,' + fs.readFileSync(out).toString('base64');
}

const used = new Set();
for (const m of html.matchAll(/data-img="([^"]+)"/g)) used.add(m[1]);
const payload = {};
let n = 0;
for (const id of used) {
  const rec = images.get(id);
  if (!rec) { console.error('missing image id', id); process.exit(1); }
  const width = rec.rel.includes('/modules/') ? 1000 : rec.rel.includes('path-to-mastery') ? 1400 : 800;
  payload[id] = jpegDataUri(rec.abs, width);
  n++;
  if (n % 20 === 0) process.stdout.write(`encoded ${n}/${used.size}\n`);
}

const missingBlurbs = allLessons.filter(l => !l.blurb);
if (missingBlurbs.length) console.warn('lessons without a description:', missingBlurbs.map(l => l.id).join(', '));
if (lessonCount < 120) {
  console.error('expected about 122 lessons, got', lessonCount);
  process.exit(1);
}
const finalHtml = html.replace('__IMG__', JSON.stringify(payload));
fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, finalHtml);
const noPic = allLessons.filter(l => !l.primary).map(l => l.id);
console.log(`wrote course-hub/directory.html (${(finalHtml.length / 1024 / 1024).toFixed(2)} MB, ${lessonCount} lessons, ${starterCount} starters, ${expertCount} expert, ${used.size} images)`);
if (noPic.length) console.log('lessons with no picture:', noPic.join(', '));
