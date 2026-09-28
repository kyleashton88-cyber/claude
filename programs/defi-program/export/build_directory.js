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

// Every command is a form in this file. The formulas match defi_calc.py.
const CALCS = [
  { cmd: 'health', hub: true, lesson: '3.2', name: 'Health factor and liquidation price', what: 'Collateral, liquidation threshold and debt, and the price that liquidates the position.' },
  { cmd: 'il', hub: true, lesson: '2.4', name: 'Impermanent loss', what: 'How far a 50/50 pool falls behind simply holding, before fees.' },
  { cmd: 'lp-breakeven', hub: false, lesson: '2.4', name: 'Fee APR to beat holding', what: 'The fee rate a liquidity position needs over a holding period to match holding both tokens.' },
  { cmd: 'loop', hub: true, lesson: '3.4', name: 'Leveraged loop', what: 'Leverage from a borrow LTV and a number of loops, the net yield on equity, and the borrow rate that wipes the extra return out.' },
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
  .replace(/<\/?[a-zA-Z][^>]*>/g, ' ')
  .replace(/[*_`#>]+/g, '')
  .replace(/\s+/g, ' ')
  .trim();

const readable = s => String(s || '')
  .replace(/!\[[^\]]*\]\([^)]*\)/g, '')
  .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
  .replace(/<\/?[a-zA-Z][^>]*>/g, ' ')
  .replace(/[*`#>]+/g, '')
  .replace(/\s+/g, ' ')
  .trim();
function sectionText(body, headingRe, keepCode) {
  const m = body.match(new RegExp('### ' + headingRe + '\\s*\\n+([\\s\\S]*?)(?=\\n### |\\n## |$)'));
  return m ? (keepCode ? readable(m[1]) : plain(m[1])) : '';
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

function readCaption(vid) {
  const rel = `video/captions/${vid}.vtt`;
  if (!exists(rel)) return null;
  const raw = read(rel);
  const times = [...raw.matchAll(/-->\s+(\d{2}):(\d{2}):(\d{2})\.\d+/g)];
  let secs = 0;
  if (times.length) {
    const t = times[times.length - 1];
    secs = Number(t[1]) * 3600 + Number(t[2]) * 60 + Number(t[3]);
  }
  const text = raw.split('\n')
    .map(line => line.trim())
    .filter(line => line && line !== 'WEBVTT' && !line.includes('-->') && !/^\d+$/.test(line))
    .join(' ')
    .replace(/\s+/g, ' ')
    .trim();
  return { mins: Math.max(1, Math.round(secs / 60)), text };
}
function readChapters(vid) {
  const rel = `video/chapters/${vid}.txt`;
  if (!exists(rel)) return [];
  return read(rel).split('\n').map(line => {
    const m = line.trim().match(/^(\d+:\d+)\s+(.+)$/);
    return m ? { t: m[1], name: m[2] } : null;
  }).filter(Boolean);
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
    const body = parts[i + 2].split(/\n### Module /)[0].split(/\n## (?!#)/)[0].replace(/\n---\s*$/g, '').trim();
    const starter = lid.endsWith('.0');
    let blurb = starter
      ? (sectionText(body, 'The 60-second version') || sectionText(body, 'Objective'))
      : (sectionText(body, 'Objective') || sectionText(body, 'The 60-second version'));
    if (!blurb) blurb = plain(body).slice(0, 360);
    let example = sectionText(body, 'Worked example[^\\n]*', true);
    let exampleKind = example ? 'worked' : '';
    if (!example) {
      example = sectionText(body, 'Explanation[^\\n]*', true) || sectionText(body, 'Your first safe step', true);
      exampleKind = example ? 'from' : '';
    }
    if (example && example.length > 700) {
      const cut = example.slice(0, 700);
      const dot = cut.lastIndexOf('. ');
      example = (dot > 160 ? cut.slice(0, dot + 1) : cut.trim()) + '…';
    }
    if (example && example === blurb) {
      example = '';
      exampleKind = '';
    }
    const mastered = starter ? sectionText(body, "You.ve mastered this module when[.…]*") : '';
    let primary = null;
    for (const m of body.matchAll(/!\[([^\]]*)\]\(([^)]+)\)/g)) {
      const id = addImage(m[2], m[1], lid);
      if (!id) continue;
      const isBanner = images.get(id).rel.includes('/modules/');
      if (!primary) primary = id;
      else if (images.get(primary).rel.includes('/modules/') && !isBanner) primary = id;
    }
    let library = '';
    if (lid === '8.3') {
      library = read('03-defi-strategy-mastery.md');
      for (const im of library.matchAll(/!\[([^\]]*)\]\(([^)]+)\)/g)) {
        const id = addImage(im[2], im[1], lid);
        if (!id) continue;
        const isBanner = images.get(id).rel.includes('/modules/');
        if (!primary || (images.get(primary).rel.includes('/modules/') && !isBanner)) primary = id;
      }
      if (!/thirty strategies/i.test(blurb)) {
        blurb = 'Name where a strategy’s return comes from, the maths that tests it, how to run it, and how it loses money. Thirty strategies, in seven levels.';
      }
    }
    const vid = `lesson-${lid.split('.')[0].padStart(2, '0')}-${lid.split('.')[1]}`;
    const cap = readCaption(vid);
    lessons.push({
      id: lid, title: starter ? 'Mastery Starter' : ltitle, starter, expert, blurb, example, exampleKind, mastered, primary, library, body,
      hay: plain((library || body) + ' ' + (cap ? cap.text : '')),
      video: exists(`video/${vid}.mp4`) ? `../video/${vid}.mp4` : '',
      mins: cap ? cap.mins : 0,
      transcript: cap ? cap.text : '',
      chapters: readChapters(vid),
    });
  }
  lessons.sort((a, b) => a.id.split('.').map(Number)[1] - b.id.split('.').map(Number)[1]);
  const mastered = (lessons.find(l => l.starter) || {}).mastered || '';
  modules.push({ n: num, title, outcome, banner, intro, mastered, lessons });
}
addImage('assets/diagrams/path-to-mastery.png', 'Six stages from Zero to Operator', null);
const pathImg = resolveAsset('assets/diagrams/path-to-mastery.png').id;

let lessonSeq = 0;
const allLessons = [];
modules.forEach(m => m.lessons.forEach(l => {
  l.i = lessonSeq++;
  l.module = m;
  l.stage = STAGES.find(s => s.mods.includes(m.n));
  allLessons.push(l);
}));
allLessons.forEach((l, i) => { l.next = allLessons[i + 1] || null; });
const calcByLesson = {};
CALCS.forEach(c => { (calcByLesson[c.lesson] || (calcByLesson[c.lesson] = [])).push(c); });
const lessonCount = allLessons.length;
const expertCount = allLessons.filter(l => l.expert).length;
const starterCount = allLessons.filter(l => l.starter).length;

function lessonLink(id, label) {
  return `<a href="#l-${String(id).replace('.', '-')}">${esc(label || 'Lesson ' + id)}</a>`;
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
  const videoWord = l.video ? `<span class="hasvid">${l.mins ? l.mins + ' min' : 'Video'}</span>` : '';
  const sheets = wsRefs.filter(w => w.lesson === l.id);
  const find = plain([l.id, l.title, l.blurb, l.hay, l.module.title, l.module.outcome, img ? img.alt : '', sheets.map(w => w.id + ' ' + w.name).join(' '), l.starter ? 'mastery starter' : '', l.expert ? 'expert' : ''].join(' ')).toLowerCase();
  const sheetWord = sheets.length ? `<span class="sheet">${esc(sheets.map(w => w.id).join(' '))}</span>` : '';
  const calcs = calcByLesson[l.id] || [];
  const calcWord = calcs.map(c => `<a class="calclink" href="#lc-${esc(c.cmd)}">${calcs.length > 1 ? esc(c.name) : 'Calculator'}</a>`).join('');
  const read = l.library
    ? `<div class="read library">${foldLibrary(l.library, l.id)}</div>`
    : `<div class="read lessonbody">${mdBlocks(l.body || '', l.id)}</div>`;
  const chapters = l.chapters && l.chapters.length
    ? `<ol class="chapters">${l.chapters.map(c => `<li><span>${esc(c.t)}</span> ${esc(c.name)}</li>`).join('')}</ol>`
    : '';
  const transcript = l.transcript
    ? `<details class="transcript"><summary>Transcript${l.mins ? ' · ' + l.mins + ' min' : ''}</summary><p>${esc(l.transcript)}</p></details>`
    : '';
  const calcHere = calcs.map(c => calcBlock(c, 'in')).join('');
  const links = [
    sheets.map(sheetLink).join(' · '),
    l.video ? `<a class="folderlink" href="${esc(l.video)}">Video file</a>` : '',
    `<a class="folderlink" href="index.html#/l/${esc(l.id)}">Course Hub copy</a>`,
  ].filter(Boolean).join(' · ');
  const place = l.stage ? `Stage ${l.stage.n} · ${l.stage.name} · Module ${l.module.n}` : `Module ${l.module.n}`;
  const next = l.next
    ? `<a href="#l-${l.next.id.replace('.', '-')}">Next: ${esc(l.next.id)} ${esc(l.next.title)}</a>`
    : 'End of the program';
  return `<details class="lesson" id="l-${l.id.replace('.', '-')}" data-kind="${l.starter ? 'starter' : l.expert ? 'expert' : 'lesson'}" data-id="${esc(l.id)}" data-mod="${l.module.n}" data-i="${l.i}" data-title="${esc(plain(l.title).toLowerCase())}" data-blurb="${esc(plain(l.blurb).toLowerCase())}" data-find="${esc(find)}">
    <summary>
      <label class="done"><input type="checkbox" data-done="${esc(l.id)}" aria-label="Mark lesson ${esc(l.id)} done"></label>
      <span class="lid">${esc(l.id)}</span>
      <span class="ltext"><span class="ltitle">${esc(l.title)}${flag}${videoWord}${sheetWord}${calcWord}</span><span class="ldesc">${esc(l.blurb)}</span></span>
      ${img ? `<img data-img="${esc(img.id)}" alt="" width="140" height="78">` : '<span class="nopic"></span>'}
      <span class="snip" hidden></span>
    </summary>
    <div class="more">${read}${chapters}${transcript}${calcHere}<p class="links">${links}</p><p class="nextline"><span>${esc(place)}</span> · ${next}</p></div>
  </details>`;
}

function moduleBlock(m) {
  const banner = m.banner ? `<img class="banner" data-img="${esc(m.banner)}" alt="" width="1000">` : '';
  const intro = m.intro ? `<a class="folderlink" href="${esc(m.intro)}">Intro video</a>` : '';
  const hub = `<a class="folderlink" href="index.html#/m/${m.n}">Course Hub copy</a>`;
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
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[^*])\*([^*]+)\*/g, '$1<em>$2</em>');
}
function isMdBlock(line) {
  const t = line.trim();
  return !t
    || t === '---'
    || t.startsWith('|')
    || t.startsWith('#')
    || t.startsWith('>')
    || t.startsWith('```')
    || t.startsWith('<details>')
    || /^[-*] /.test(t)
    || /^\d+\. /.test(t)
    || /^!\[[^\]]*\]\([^)]+\)$/.test(t);
}
function mdBlocks(text, lessonId) {
  const lines = text.replace(/\r/g, '').split('\n');
  let html = '';
  let i = 0;
  const isSep = cells => cells.every(c => /^:?-+:?$/.test(c));
  const takeContinuation = item => {
    while (i < lines.length && /^\s+\S/.test(lines[i]) && !isMdBlock(lines[i])) {
      item += ' ' + lines[i].trim();
      i++;
    }
    return item;
  };
  while (i < lines.length) {
    const raw = lines[i];
    const trim = raw.trim();
    if (!trim) { i++; continue; }
    if (trim === '---') { html += '<hr>'; i++; continue; }
    if (trim.startsWith('```')) {
      const code = [];
      i++;
      while (i < lines.length && !lines[i].trim().startsWith('```')) { code.push(lines[i]); i++; }
      if (i < lines.length) i++;
      html += `<pre class="code"><code>${esc(code.join('\n'))}</code></pre>`;
      continue;
    }
    if (trim.startsWith('<details>')) {
      const chunk = [];
      while (i < lines.length) {
        chunk.push(lines[i]);
        if (lines[i].includes('</details>')) { i++; break; }
        i++;
      }
      const block = chunk.join('\n');
      const sum = block.match(/<summary>([\s\S]*?)<\/summary>/);
      const rest = block.replace(/<details>\s*<summary>[\s\S]*?<\/summary>/, '').replace(/<\/details>\s*$/, '').trim();
      html += `<details class="quiz"><summary>${inline(sum ? sum[1].trim() : '')}</summary><p>${inline(rest)}</p></details>`;
      continue;
    }
    if (trim.startsWith('|')) {
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
    } else if (/^[-*] /.test(trim) || /^\d+\. /.test(trim)) {
      const ordered = /^\d+\. /.test(trim);
      const re = ordered ? /^\d+\. / : /^[-*] /;
      const items = [];
      while (i < lines.length && re.test(lines[i].trim())) {
        let item = lines[i].trim().replace(re, '');
        i++;
        item = takeContinuation(item);
        items.push(item);
      }
      const tag = ordered ? 'ol' : 'ul';
      html += `<${tag}>` + items.map(it => `<li>${inline(it)}</li>`).join('') + `</${tag}>`;
    } else if (trim.startsWith('>')) {
      const quote = [];
      while (i < lines.length && lines[i].trim().startsWith('>')) {
        quote.push(lines[i].trim().replace(/^>\s?/, ''));
        i++;
      }
      html += `<blockquote><p>${inline(quote.join(' '))}</p></blockquote>`;
    } else if (/^!\[[^\]]*\]\([^)]+\)$/.test(trim)) {
      const img = trim.match(/^!\[([^\]]*)\]\(([^)]+)\)$/);
      const id = addImage(img[2], img[1], lessonId || null);
      if (id) html += `<figure><img data-img="${esc(id)}" alt="${esc(plain(img[1]))}" width="800"><figcaption>${esc(plain(img[1]))}</figcaption></figure>`;
      i++;
    } else if (trim.startsWith('#### ')) {
      html += `<h5>${inline(trim.slice(5))}</h5>`;
      i++;
    } else if (trim.startsWith('### ')) {
      html += `<h4>${inline(trim.slice(4))}</h4>`;
      i++;
    } else if (trim.startsWith('## ')) {
      html += `<h3>${inline(trim.slice(3))}</h3>`;
      i++;
    } else if (trim.startsWith('# ')) {
      html += `<h3>${inline(trim.slice(2))}</h3>`;
      i++;
    } else {
      const para = [];
      while (i < lines.length && lines[i].trim() && !isMdBlock(lines[i])) {
        para.push(lines[i].trim());
        i++;
      }
      html += `<p>${inline(para.join(' '))}</p>`;
    }
  }
  return html;
}

function foldLibrary(md, lessonId) {
  const introAt = md.search(/\n## /);
  const intro = introAt < 0 ? md : md.slice(0, introAt);
  const rest = introAt < 0 ? '' : md.slice(introAt + 1);
  let html = mdBlocks(intro, lessonId);
  for (const part of rest.split(/\n(?=## )/)) {
    const title = part.split('\n')[0].replace(/^## /, '').trim();
    if (/^Part 3\b/.test(title)) {
      const chunks = part.split(/\n(?=### LEVEL )/);
      const lead = chunks[0].replace(/^## [^\n]*\n?/, '');
      let inner = mdBlocks(lead, lessonId);
      for (const chunk of chunks.slice(1)) {
        const heading = chunk.split('\n')[0].replace(/^### /, '').trim();
        const names = [...chunk.matchAll(/^#### (.+)$/gm)].map(m => m[1].trim()).join(' · ');
        const body = chunk.replace(/^### [^\n]*\n?/, '');
        inner += `<details class="level"><summary><b>${esc(heading)}</b><span>${esc(names)}</span></summary>${mdBlocks(body, lessonId)}</details>`;
      }
      html += `<section class="playbook"><h3>${esc(title)}</h3>${inner}</section>`;
    } else {
      const body = part.replace(/^## [^\n]*\n?/, '');
      html += `<details class="level part"><summary>${esc(title)}</summary>${mdBlocks(body, lessonId)}</details>`;
    }
  }
  return html;
}

function fillable(html, id) {
  let n = 0;
  const nid = () => id.toLowerCase() + '-' + (n++);
  const box = () => `<input class="blank" data-ws="${nid()}" aria-label="Your answer">`;
  let out = html.replace(/_{2,}/g, box);
  out = out.replace(/<td>(?:\s|&nbsp;)*<\/td>/g, () => `<td>${box()}</td>`);
  out = out.replace(/<li>\[ \]\s*/g, () => `<li><label class="tick"><input type="checkbox" data-ws="${nid()}"> `);
  out = out.replace(/<li><label class="tick">([\s\S]*?)<\/li>/g, '<li><label class="tick">$1</label></li>');
  out = out.replace(/<thead><tr>([\s\S]*?)<\/tr><\/thead><tbody><\/tbody>/g, (m, head) => {
    const cols = (head.match(/<th[\s>]/g) || []).length || 1;
    const cells = Array.from({ length: cols }, () => `<td>${box()}</td>`).join('');
    return `<thead><tr>${head}</tr></thead><tbody><tr>${cells}</tr></tbody>`;
  });
  return out;
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
    <header><h3>${esc(title)}</h3><p class="links">${where}<button type="button" class="copy">Copy worksheet</button><button type="button" class="print">Print worksheet</button></p></header>
    <div class="wsbody">${fillable(mdBlocks(body), id)}</div>
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

// [key, label, default, unit, kind, select options]
// Unit sits outside the number: $ before it, % or 0–1 after it.
// Fractions stay 0–1. Rates that the lesson writes as percents stay percents.
const FORMS = {
  health: [['qty', 'Collateral quantity', 10, ''], ['price', 'Collateral price', 3000, '$'], ['lt', 'Liquidation threshold', 0.8, '0–1'], ['debt', 'Debt', 12000, '$']],
  il: [['ratio', 'Price ratio, new ÷ entry', 2, '×']],
  'lp-breakeven': [['ratio', 'Price ratio, new ÷ entry', 2, '×'], ['days', 'Days held', 90, ''], ['fee', 'Fee APR', 20, '%']],
  loop: [['ltv', 'Borrow LTV', 0.7, '0–1'], ['loops', 'Loops', 3, ''], ['capy', 'Collateral APY', 3.5, '%'], ['bapy', 'Borrow APY', 2.5, '%']],
  lvr: [['vol', 'Volatility per year', 80, '%'], ['fee', 'Fee APR', 12, '%']],
  pt: [['price', 'PT price of the underlying', 0.95, 'of 1'], ['days', 'Days to maturity', 180, '']],
  expected: [['y', 'Headline yield', 12, '%'], ['p', 'Annual loss probability', 0.05, '0–1'], ['lgd', 'Loss given default', 0.6, '0–1'], ['c', 'Costs', 0.5, '%']],
  income: [['cap', 'Capital', 250000, '$'], ['ry', 'Risk-adjusted yield', 5, '%'], ['payout', 'Payout ratio', 0.7, '0–1']],
  var: [['pos', 'Position', 100000, '$'], ['vol', 'Volatility per year', 70, '%'], ['z', 'Confidence, 1.65 is about 95%', 1.65, '']],
  cl: [['low', 'Range low', 1800, '$'], ['high', 'Range high', 3000, '$']],
  carry: [['rate', 'Funding per 8 hours', 0.01, '%'], ['shortlev', 'Short leverage', 2, '×']],
  supply: [['bapy', 'Borrow APY', 5, '%'], ['util', 'Utilisation', 0.8, '0–1'], ['reserve', 'Reserve factor', 0.1, '0–1']],
  apy: [['apr', 'APR', 12, '%'], ['n', 'Compounds per year', 365, ''], ['pos', 'Position', 10000, '$'], ['gas', 'Gas per compound', 2, '$']],
  airdrop: [['prob', 'Probability', 0.3, '0–1'], ['value', 'Value if it happens', 1500, '$'], ['costs', 'Costs', 200, '$']],
  basis: [['spot', 'Spot price', 3000, '$'], ['future', 'Future price', 3150, '$'], ['days', 'Days to expiry', 90, '']],
  'covered-call': [['spot', 'Spot price', 3000, '$'], ['strike', 'Strike', 3300, '$'], ['premium', 'Premium per period', 1.5, '%'], ['days', 'Days in the period', 7, '']],
  bank: [['coll', 'Collateral', 100000, '$'], ['lt', 'Liquidation threshold', 0.8, '0–1'], ['debt', 'Debt', 20000, '$'], ['bapy', 'Borrow APY', 5, '%'], ['reserve', 'Liquid reserve', 15000, '$'], ['other', 'Other assets', 0, '$'], ['spend', 'Monthly spend', 2000, '$'], ['maxltv', 'Policy max LTV', 30, '%']],
  perp: [['entry', 'Entry price', 3000, '$'], ['lev', 'Leverage', 5, '×'], ['side', 'Side', 'long', '', 'select', ['long', 'short']], ['mmr', 'Maintenance margin', 0.5, '%']],
  twr: [['p1', 'Period 1 return', 4, '%'], ['p2', 'Period 2 return', -2, '%'], ['p3', 'Period 3 return', 3, '%'], ['start', 'Start value', '', '$', 'optional'], ['end', 'End value', '', '$', 'optional'], ['deposits', 'Net deposits', '', '$', 'optional']],
  cdp: [['qty', 'Collateral quantity', 10, ''], ['price', 'Collateral price', 3000, '$'], ['mint', 'Stablecoins to mint', 10000, '$'], ['minr', 'Minimum collateral ratio', 150, '%'], ['fee', 'Stability fee per year', 6, '%']],
};

function fieldControl(f) {
  const [k, lab, def, unit, kind, opts] = f;
  if (kind === 'select') {
    const options = opts.map(o => `<option value="${esc(o)}"${o === def ? ' selected' : ''}>${esc(o)}</option>`).join('');
    return `<label class="field">${esc(lab)}<span class="box"><select data-k="${esc(k)}" data-def="${esc(def)}">${options}</select></span></label>`;
  }
  const opt = kind === 'optional' ? ' data-opt="1"' : '';
  const shown = def === '' || def == null ? '' : (unit === '0–1' ? Number(def).toFixed(2) : String(def));
  const pre = unit === '$' ? '<span class="unit pre">$</span>' : '';
  const suf = unit && unit !== '$' ? `<span class="unit suf">${esc(unit)}</span>` : '';
  return `<label class="field">${esc(lab)}<span class="box">${pre}<input type="number" inputmode="decimal" step="any" data-k="${esc(k)}" data-def="${esc(shown)}" value="${esc(shown)}"${opt}>${suf}</span></label>`;
}

function stageForLesson(id) {
  const n = Number(String(id).split('.')[0]);
  return STAGES.find(s => s.mods.includes(n));
}
function calcBlock(c, place) {
  const find = plain(c.cmd + ' ' + c.name + ' ' + c.what + ' calculator lesson ' + c.lesson).toLowerCase();
  const fields = FORMS[c.cmd];
  if (!fields) throw new Error('missing form for ' + c.cmd);
  const required = fields.filter(f => f[4] !== 'optional');
  const optional = fields.filter(f => f[4] === 'optional');
  const opt = optional.length ? `<p class="optlabel">Optional</p><div class="formgrid">${optional.map(fieldControl).join('')}</div>` : '';
  const prefix = place === 'in' ? 'lc-' : 'c-';
  return `<div class="calc" id="${prefix}${esc(c.cmd)}" data-c="${esc(c.cmd)}" data-name="${esc(c.name.toLowerCase())}" data-find="${esc(find)}">
    <div class="calctop">
      <h3>${esc(c.name)}</h3>
      <p class="calcwhat">${esc(c.what)}</p>
      <p class="exampletag">${lessonLink(c.lesson, 'Lesson ' + c.lesson + ' example')}</p>
      <div class="formgrid">${required.map(fieldControl).join('')}</div>
      ${opt}
      <p class="exrow"><button type="button" class="resetex">Back to the lesson example</button></p>
    </div>
    <div class="out" aria-live="polite"></div>
  </div>`;
}
const calcRows = STAGES.map(s => {
  const items = CALCS.filter(c => stageForLesson(c.lesson) === s).sort((a, b) => {
    const [am, al] = a.lesson.split('.').map(Number);
    const [bm, bl] = b.lesson.split('.').map(Number);
    return am - bm || al - bl || CALCS.indexOf(a) - CALCS.indexOf(b);
  });
  if (!items.length) return '';
  return `<div class="calcgroup"><h3 class="calcstage">Stage ${s.n} · ${esc(s.name)}</h3>${items.map(calcBlock).join('\n')}</div>`;
}).join('\n');

const orientation = ORIENTATION.filter(v => exists('video/' + v.file)).map(v =>
  `<li><a class="folderlink" href="../video/${esc(v.file)}">${esc(v.name)}</a> — ${esc(v.about)}</li>`
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
    <h2>Stage ${s.n} · ${esc(s.name)} <span class="donecount" data-stage-count data-ids="${esc(s.mods.flatMap(n => modules[n].lessons.map(l => l.id)).join(','))}"></span></h2>
    <p class="stage-can">${esc(s.can)}</p>
    ${body}
  </section>`;
}).join('\n');

const FILES = [
  ['This directory', 'directory.html', 'The map you are reading. Search, or walk the stages.'],
  ['Course Hub', 'index.html', 'Every lesson with its video, checklist, quiz, and your progress. Saved in this browser only.'],
  ['Day-1 Setup Kit', '../Day-1-Setup-Kit.pdf', 'Printable checklist from Module 0. The written version is Day-1-Setup-Kit.md.'],
  ['Full program book', '../On-Chain-Operator-Program.pdf', 'The same course as one document, with diagrams.'],
  ['Written lessons', '../lessons/', 'One markdown file per module. Lesson 2.2 is also in 02-sample-lesson-amm-math.md. Lesson 8.3 on this page includes the strategy library from 03-defi-strategy-mastery.md.'],
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
.filters button, button.copy, button.print, button.resetex { font: inherit; font-size: 14.5px; background: transparent; color: var(--text); border: 1px solid #b7c6d4; padding: 6px 12px; cursor: pointer; }
.filters button[aria-pressed="true"] { background: var(--ink); color: #fff; border-color: var(--ink); }
.stage-block { margin-top: 42px; }
.stage-block > h2 { padding-top: 8px; }
.module { margin: 28px 0 10px; scroll-margin-top: 120px; }
.stage-block, .worksheet, section, .pics { scroll-margin-top: 120px; }
.banner { display: block; width: 100%; background: var(--ink); }
.links { font-size: 15px; }
.links .go { font-weight: 700; }
.lesson { border-top: 1px solid var(--line); scroll-margin-top: 120px; }
.lesson summary { display: grid; grid-template-columns: auto 3.4rem minmax(0, 1fr) 140px; gap: 8px 14px; align-items: center; padding: 12px 0; cursor: pointer; list-style: none; }
.lesson summary::-webkit-details-marker { display: none; }
.lesson summary:hover .ltitle { text-decoration: underline; text-underline-offset: 2px; }
.lid { font-family: var(--mono); font-size: 13.5px; font-weight: 600; color: var(--link); font-variant-numeric: tabular-nums; }
.ltitle { font-weight: 680; }
.ldesc { display: block; color: var(--muted); font-size: 15px; margin-top: 3px; }
.flag { font-weight: 680; font-size: 14px; margin-left: 8px; color: var(--warn); }
.flag.start { color: var(--link); }
.hasvid, .sheet, .calclink { margin-left: 8px; font-weight: 680; font-size: 14px; }
.hasvid { color: var(--muted); font-weight: 600; }
.sheet, .calclink { color: var(--link); }
.ltext, .ltitle { min-width: 0; }
.example { max-width: 66ch; }
.hitcalc { display: flex; gap: 12px; align-items: baseline; border-top: 1px solid var(--line); padding: 12px 0; text-decoration: none; }
.hitcalc span { font-family: var(--mono); font-size: 13.5px; font-weight: 600; }
.hitcalc b { color: var(--text); font-weight: 680; }
.lesson summary img, .nopic { width: 140px; height: 78px; object-fit: cover; background: var(--ink); display: block; }
.done { display: flex; align-items: center; }
.done input { width: 1.15rem; height: 1.15rem; margin: 0; accent-color: var(--link); }
.lesson.isdone .lid { color: var(--link); }
.snip { display: none; grid-column: 1 / -1; font-size: 14.5px; font-weight: 450; color: var(--text); }
#hits .lesson .snip { display: block; }
.snip mark { background: #d9f6ec; color: inherit; padding: 0 1px; }
.donecount { font-size: 15px; font-weight: 550; color: var(--muted); margin-left: 10px; }
.more { padding: 0 0 18px 4.6rem; min-width: 0; }
.more img { display: block; width: min(100%, 720px); background: var(--ink); margin-bottom: 10px; }
.more p { max-width: 66ch; margin: 8px 0; }
.read { max-width: 78ch; min-width: 0; }
.read h3 { font-size: 20px; margin: 22px 0 6px; }
.read h4 { font-size: 17px; margin: 18px 0 4px; }
.read h5 { font-size: 16px; margin: 16px 0 4px; }
.read figure { margin: 12px 0 16px; }
.read figcaption { color: var(--muted); font-size: 14px; margin-top: 4px; }
.read pre.code { overflow-x: auto; max-width: 100%; background: var(--ink); color: #e7eef4; padding: 12px 14px; font-size: 13.5px; line-height: 1.45; }
.read pre.code code { color: inherit; }
.read blockquote { margin: 10px 0; padding: 8px 12px; border-left: 4px solid var(--warn); background: var(--warnbg); }
.read blockquote p { margin: 0; max-width: none; }
.read .quiz { margin: 8px 0; border-top: 1px solid var(--line); padding-top: 8px; }
.read .quiz summary { cursor: pointer; font-weight: 650; }
.read .quiz p { margin: 6px 0 0; }
.read ol, .read ul { padding-left: 1.2em; margin: 8px 0; }
.read li { margin: 4px 0; }
.read hr { border: 0; border-top: 1px solid var(--line); margin: 18px 0; }
.level { border-top: 1px solid var(--line); margin: 4px 0; }
.level > summary { cursor: pointer; padding: 8px 0; }
.level > summary b, .level.part > summary { display: block; font-weight: 700; }
.level > summary span { display: block; margin-top: 3px; color: var(--muted); font-weight: 500; font-size: 14.5px; }
.playbook > h3 { margin-top: 8px; }
.chapters { list-style: none; padding: 0; margin: 8px 0 12px; }
.chapters li { margin: 3px 0; }
.chapters span { font-family: var(--mono); color: var(--muted); margin-right: 8px; }
.transcript summary { cursor: pointer; font-weight: 680; }
.transcript p { max-width: 72ch; }
.nextline { font-size: 15px; }
.exrow { margin: 10px 0 0; }
.gloss { border-top: 1px solid var(--line); padding: 12px 0 8px; }
.gloss h3 { font-size: 18px; margin: 0 0 4px; }
.wsbody .blank { font: inherit; font-size: 15px; width: 100%; min-width: 0; border: 0; border-bottom: 1px solid #9aafc0; background: transparent; padding: 2px 0; color: var(--text); }
.wsbody p .blank, .wsbody li .blank { width: 8rem; }
.tick { font-weight: 450; }
.tick input { margin-right: 6px; accent-color: var(--link); }
.worksheet { border-top: 1px solid var(--line); padding: 18px 0 8px; }
.worksheet header { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px 16px; align-items: baseline; }
.worksheet h3 { margin-top: 0; }
.wsbody { max-width: 78ch; }
.tablewrap { overflow-x: auto; max-width: 100%; margin: 10px 0 16px; }
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
.calcstage { margin: 26px 0 0; font-size: 20px; }
.calc { border-top: 1px solid var(--line); padding: 18px 0 8px; scroll-margin-top: 120px; max-width: 760px; }
.calc h3 { margin: 0 0 4px; font-size: 18px; }
.calcwhat { margin: 0 0 8px; max-width: 66ch; color: var(--muted); }
.exampletag { margin: 0 0 8px; font-size: 14.5px; font-weight: 700; }
.optlabel { margin: 2px 0 0; font-size: 13px; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; color: var(--muted); }
.formgrid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 160px), 1fr)); gap: 10px; margin: 8px 0 0; max-width: min(720px, 100%); }
.field { font-size: 13px; font-weight: 650; color: var(--muted); min-width: 0; }
.field .box { display: flex; align-items: stretch; margin-top: 4px; background: #fff; border: 1px solid var(--line); min-width: 0; }
.field .box:focus-within { border-color: var(--link); box-shadow: 0 0 0 1px var(--link); }
.field input, .field select { display: block; width: 100%; min-width: 0; border: 0; margin: 0; font: inherit; font-size: 16px; font-variant-numeric: tabular-nums; padding: 8px 10px; background: transparent; color: var(--text); }
.field .unit { display: flex; align-items: center; padding: 0 10px; color: var(--muted); font-size: 13px; font-weight: 700; white-space: nowrap; background: #f7fafc; }
.field .unit.pre { border-right: 1px solid var(--line); }
.field .unit.suf { border-left: 1px solid var(--line); }
.out { font-size: 15px; line-height: 1.45; background: #fff; border: 1px solid #c9efe4; border-left: 4px solid #12a888; padding: 14px 16px 10px; margin: 14px 0 4px; max-width: 720px; }
.out .result { display: flex; flex-wrap: wrap; align-items: baseline; gap: 8px 12px; margin: 0 0 8px; font-size: 28px; line-height: 1.15; font-weight: 720; letter-spacing: -0.03em; color: var(--ink); font-variant-numeric: tabular-nums; }
.out .mark { font-size: 13px; font-weight: 700; letter-spacing: 0; line-height: 1.3; padding: 3px 8px; }
.out .mark.ok { color: var(--link); background: #e7f6f1; }
.out .mark.warn { color: var(--warn); background: var(--warnbg); }
.out .say { margin: 0 0 10px; max-width: 62ch; font-size: 16px; font-weight: 450; letter-spacing: 0; color: var(--text); }
.out .bits { margin: 0; }
.out .bits div { display: grid; grid-template-columns: minmax(0, 1.3fr) minmax(0, 1fr); gap: 8px 16px; padding: 7px 0; border-top: 1px solid var(--line); }
.out .bits dt { margin: 0; color: var(--muted); font-weight: 600; }
.out .bits dd { margin: 0; font-weight: 680; text-align: right; font-variant-numeric: tabular-nums; overflow-wrap: anywhere; }
.out .bits .warn { color: var(--warn); font-weight: 700; }
.out .plot { margin: 2px 0 12px; }
.out .plot svg { width: 100%; height: auto; display: block; overflow: hidden; }
.out .plot svg text { font-family: Inter, "Segoe UI", "Helvetica Neue", system-ui, sans-serif; }
.out .legend { display: flex; flex-wrap: wrap; gap: 4px 14px; margin: 0; font-size: 12px; font-weight: 650; color: var(--muted); }
.out .legend i { display: inline-block; width: 16px; height: 3px; margin-right: 6px; vertical-align: middle; }
#offline-note { margin-top: 12px; }
#files table code { color: var(--muted); }
footer { margin-top: 36px; color: var(--muted); font-size: 14.5px; max-width: 68ch; }
@media (max-width: 860px) {
  .shell { grid-template-columns: minmax(0, 1fr); }
  .rail, .main { min-width: 0; }
  .rail { position: sticky; top: 96px; max-height: none; display: flex; width: 100%; gap: 0; overflow-x: auto; padding: 0 8px; }
  .rail a { white-space: nowrap; border-left: 0; border-bottom: 2px solid transparent; padding: 10px 12px; }
  .rail a.stagelink { margin: 0; }
  .rail a.modlink { font-size: 13px; }
  .main { padding: 22px 16px 72px; max-width: 100%; }
  .search { width: min(240px, 42vw); }
  .gallery { grid-template-columns: 1fr; }
  .lesson summary { grid-template-columns: auto 2.8rem minmax(0, 1fr) 92px; gap: 8px; }
  .lesson summary img, .nopic { width: 92px; height: 52px; }
  .more { padding-left: 0; }
  .out .result { font-size: 24px; }
}
@media (max-width: 560px) {
  .mast { flex-wrap: wrap; }
  .search { width: 100%; margin-left: 0; }
}
@media print {
  .top, .rail, #intro, #lessons, #glossary, #pictures, #calculators, #files, footer { display: none !important; }
  body.print-one #worksheets .worksheet { display: none !important; }
  body.print-one #worksheets .worksheet.printing { display: block !important; }
  .shell { display: block; }
  .main { max-width: none; padding: 0; }
  button, .filters, #empty, #hits { display: none !important; }
  .wsbody .blank { border-bottom: 1px solid #000; }
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
function parkLessons() {
  document.querySelectorAll('#hits .hitcalc').forEach(n => n.remove());
  const byMod = new Map();
  lessons.forEach(el => {
    const id = el.dataset.mod;
    if (!byMod.has(id)) byMod.set(id, []);
    byMod.get(id).push(el);
  });
  byMod.forEach((els, id) => {
    els.sort((a, b) => Number(a.dataset.i) - Number(b.dataset.i));
    const parent = document.getElementById('m-' + id);
    els.forEach(el => parent.appendChild(el));
  });
}
function lessonScore(el, w) {
  const title = el.dataset.title || '';
  const blurb = el.dataset.blurb || '';
  const hay = el.dataset.find || '';
  if (!w.every(x => hay.includes(x))) return -1;
  let s = 1;
  const id = el.dataset.id || '';
  if (w.length === 1 && (id === w[0] || id.replace('.', '') === w[0])) s += 300;
  if (w.every(x => title.includes(x))) s += 120;
  if (w.every(x => blurb.includes(x))) s += 40;
  return s;
}
function calcScore(el, w) {
  const name = el.dataset.name || '';
  const hay = el.dataset.find || '';
  if (!w.every(x => hay.includes(x))) return -1;
  return w.every(x => name.includes(x)) ? 95 : 8;
}
function apply() {
  const w = words();
  const searching = w.length > 0;
  parkLessons();
  lessons.forEach(el => {
    const kindOk = mode === 'all' || el.dataset.kind === mode;
    const textOk = !searching || w.every(x => el.dataset.find.includes(x));
    el.hidden = !(kindOk && textOk);
  });
  blocks.forEach(el => {
    if (el.classList.contains('lesson') || el.closest('.lesson')) return;
    const textOk = !searching || w.every(x => el.dataset.find.includes(x));
    el.hidden = !textOk;
    const d = el.closest('details.pics');
    if (d && textOk && searching) { if (!d.open) { d.open = true; d.dataset.searchOpen = '1'; } }
  });
  if (!searching) document.querySelectorAll('details[data-search-open]').forEach(d => { d.open = false; delete d.dataset.searchOpen; });
  const hits = document.getElementById('hits');
  if (searching) {
    const items = [];
    lessons.forEach(el => { if (!el.hidden) items.push({ s: lessonScore(el, w), i: Number(el.dataset.i), el }); });
    document.querySelectorAll('#calculators .calc').forEach(el => {
      if (el.hidden) return;
      items.push({ s: calcScore(el, w), i: 1000, calc: el });
    });
    items.sort((a, b) => b.s - a.s || a.i - b.i);
    hits.hidden = items.length === 0;
    items.forEach(item => {
      if (item.el) { hits.appendChild(item.el); return; }
      const a = document.createElement('a');
      a.className = 'hitcalc';
      a.href = '#' + item.calc.id;
      const mark = document.createElement('span');
      mark.textContent = 'Calculator';
      const name = document.createElement('b');
      name.textContent = item.calc.querySelector('h3').textContent;
      a.append(mark, name);
      hits.appendChild(a);
    });
  } else hits.hidden = true;
  lessons.forEach(el => {
    const snip = el.querySelector('.snip');
    if (!snip) return;
    if (searching && !el.hidden) {
      snip.innerHTML = snippet(el, w);
      snip.hidden = !snip.textContent;
    } else {
      snip.hidden = true;
      snip.textContent = '';
    }
  });
  document.querySelectorAll('.module').forEach(m => {
    const rows = [...m.querySelectorAll('.lesson')];
    m.hidden = rows.length === 0 || rows.every(l => l.hidden);
  });
  document.querySelectorAll('details.pics').forEach(d => {
    const figs = [...d.querySelectorAll('figure')];
    d.hidden = searching && figs.every(f => f.hidden);
  });
  document.querySelectorAll('.stage-block').forEach(s => {
    const rows = [...s.querySelectorAll('.module')];
    s.hidden = rows.length === 0 || rows.every(m => m.hidden);
  });
  document.querySelectorAll('.calcgroup').forEach(g => {
    g.hidden = [...g.querySelectorAll('.calc')].every(c => c.hidden);
  });
  ['glossary','worksheets','pictures','calculators','files'].forEach(id => {
    const sec = document.getElementById(id);
    if (!sec) return;
    const rows = [...sec.querySelectorAll('[data-find]')].filter(el => !el.classList.contains('lesson'));
    sec.hidden = searching && rows.length > 0 && rows.every(el => el.hidden);
  });
  const shown = lessons.filter(l => !l.hidden).length;
  const focusResults = searching || mode !== 'all';
  document.getElementById('intro').hidden = focusResults;
  const doneN = document.querySelectorAll('input[data-done]:checked').length;
  count.textContent = (focusResults ? shown + ' of ' + lessons.length + ' lessons' : lessons.length + ' lessons') + (doneN ? ' · ' + doneN + ' done' : '');
  const key = mode + '\\n' + q.value;
  if (apply.last !== undefined && apply.last !== key && focusResults) {
    const target = shown
      ? (searching ? document.getElementById('hits') : document.getElementById('lessons'))
      : document.querySelector('.hitcalc, .worksheet:not([hidden]), #pictures figure:not([hidden]), .calc:not([hidden]), #files tr:not([hidden])');
    if (target) target.scrollIntoView({ block: 'start' });
  }
  apply.last = key;
  const any = shown || ['glossary','worksheets','pictures','calculators','files'].some(id => {
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
function escHtml(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
function snippet(el, w) {
  const box = el.querySelector('.read');
  const text = ((box ? box.textContent : '') + ' ' + (el.querySelector('.ldesc') ? el.querySelector('.ldesc').textContent : '')).replace(/\\s+/g, ' ').trim();
  const bits = text.split(/(?<=[.!?])\\s+/).map(s => s.trim()).filter(s => s.length > 24);
  const lowerBits = bits.map(s => s.toLowerCase());
  let idx = lowerBits.findIndex(s => w.every(x => s.includes(x)));
  if (idx < 0) idx = lowerBits.findIndex(s => w.some(x => s.includes(x)));
  if (idx < 0) return '';
  let hit = bits[idx];
  if (hit.length > 240) hit = hit.slice(0, 240).replace(/\\s+\\S*$/, '') + '…';
  const lower = hit.toLowerCase();
  const spans = [];
  w.forEach(word => {
    let from = 0;
    while (word && from < lower.length) {
      const at = lower.indexOf(word, from);
      if (at < 0) break;
      spans.push([at, at + word.length]);
      from = at + word.length;
    }
  });
  spans.sort((a, b) => a[0] - b[0] || b[1] - a[1]);
  let html = '';
  let i = 0;
  spans.forEach(sp => {
    if (sp[0] < i) return;
    html += escHtml(hit.slice(i, sp[0])) + '<mark>' + escHtml(hit.slice(sp[0], sp[1])) + '</mark>';
    i = sp[1];
  });
  return html + escHtml(hit.slice(i));
}
document.querySelectorAll('a.calclink').forEach(a => a.addEventListener('click', e => {
  e.stopPropagation();
  const lesson = a.closest('details.lesson');
  if (lesson) lesson.open = true;
}));
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
  if (!el) return;
  if (el.tagName === 'DETAILS') el.open = true;
  let parent = el.parentElement;
  while (parent) {
    if (parent.tagName === 'DETAILS') parent.open = true;
    parent = parent.parentElement;
  }
};
const DONEKEY = 'oc-operator-done';
function readDone() { try { return new Set(JSON.parse(localStorage.getItem(DONEKEY) || '[]')); } catch (e) { return new Set(); } }
function paintDone() {
  const done = readDone();
  document.querySelectorAll('input[data-done]').forEach(i => { i.checked = done.has(i.dataset.done); });
  lessons.forEach(el => el.classList.toggle('isdone', done.has(el.dataset.id)));
  document.querySelectorAll('[data-stage-count]').forEach(el => {
    const ids = (el.dataset.ids || '').split(',').filter(Boolean);
    const n = ids.filter(x => done.has(x)).length;
    el.textContent = n ? n + ' of ' + ids.length + ' done' : '';
  });
}
document.querySelectorAll('input[data-done]').forEach(i => {
  const label = i.closest('label');
  if (label) label.addEventListener('click', e => e.stopPropagation());
  i.addEventListener('click', e => e.stopPropagation());
  i.addEventListener('change', () => {
    const done = readDone();
    if (i.checked) done.add(i.dataset.done); else done.delete(i.dataset.done);
    localStorage.setItem(DONEKEY, JSON.stringify([...done]));
    paintDone();
    apply();
  });
});
paintDone();
const WSKEY = 'oc-operator-worksheets';
function readWs() { try { return JSON.parse(localStorage.getItem(WSKEY) || '{}'); } catch (e) { return {}; } }
function saveWs() {
  const data = {};
  document.querySelectorAll('[data-ws]').forEach(el => { data[el.dataset.ws] = el.type === 'checkbox' ? (el.checked ? '1' : '') : el.value; });
  localStorage.setItem(WSKEY, JSON.stringify(data));
}
const savedWs = readWs();
document.querySelectorAll('[data-ws]').forEach(el => {
  if (savedWs[el.dataset.ws]) {
    if (el.type === 'checkbox') el.checked = savedWs[el.dataset.ws] === '1';
    else el.value = savedWs[el.dataset.ws];
  }
  el.addEventListener('input', saveWs);
  el.addEventListener('change', saveWs);
});
document.querySelectorAll('button.print').forEach(b => b.addEventListener('click', () => {
  const sheet = b.closest('.worksheet');
  document.body.classList.add('print-one');
  sheet.classList.add('printing');
  window.print();
  sheet.classList.remove('printing');
  document.body.classList.remove('print-one');
}));
addEventListener('hashchange', openHash);
openHash();
apply();
const money = x => (x < 0 ? '−$' : '$') + Math.abs(x).toLocaleString('en-US', { maximumFractionDigits: 2 });
const pct = (x, d = 2) => (x < 0 ? '−' : '') + Math.abs(x * 100).toFixed(d) + '%';
const pctPts = (n, d = 2) => (n < 0 ? '−' : '') + Math.abs(n).toFixed(d) + '%';
const signed = x => (x < 0 ? '−' : '+') + Math.abs(x).toFixed(1) + '%';
const ilLoss = r => 1 - 2 * Math.sqrt(r) / (1 + r);
const say = msg => '<p class="say">' + msg + '</p>';
const panel = (lead, bits, spoken, status, graph) => {
  const mark = status ? '<span class="mark ' + status.tone + '">' + status.label + '</span>' : '';
  const rows = '<dl class="bits">' + bits.map(b => '<div><dt>' + b[0] + '</dt><dd>' + b[1] + '</dd></div>').join('') + '</dl>';
  return '<p class="result">' + lead + mark + '</p>' + (spoken ? '<p class="say">' + spoken + '</p>' : '') + (graph || '') + rows;
};
const xml = s => String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');
function niceTicks(a, b, count) {
  const span = b - a;
  if (!(span > 0) || !isFinite(span)) return [a];
  const step0 = span / Math.max(1, count);
  const mag = Math.pow(10, Math.floor(Math.log10(step0)));
  const err = step0 / mag;
  const step = (err >= 7.5 ? 10 : err >= 3.5 ? 5 : err >= 1.5 ? 2 : 1) * mag;
  const start = Math.ceil((a - step * 1e-6) / step) * step;
  const ticks = [];
  for (let i = 0; i < 8; i++) {
    const t = Math.round((start + i * step) / step) * step;
    if (t > b + step * 1e-6) break;
    if (t >= a - step * 1e-6) ticks.push(Math.abs(t) < step * 1e-6 ? 0 : t);
  }
  return ticks;
}
function fmtTick(t, unit) {
  const a = Math.abs(t);
  const sign = t < -1e-9 ? '−' : '';
  let body;
  if (unit === '$') {
    if (a >= 1000) {
      const k = a / 1000;
      body = '$' + (k >= 10 || Math.abs(k - Math.round(k)) < 0.05 ? String(Math.round(k)) : k.toFixed(1)) + 'k';
    } else body = '$' + (a >= 100 ? String(Math.round(a)) : String(Math.round(a)));
    return sign + body;
  }
  if (a >= 100) body = a.toFixed(0);
  else if (a >= 10) body = Math.abs(a - Math.round(a)) < 0.05 ? String(Math.round(a)) : a.toFixed(1);
  else if (a >= 1) body = Math.abs(a - Math.round(a)) < 0.05 ? String(Math.round(a)) : a.toFixed(1);
  else body = a.toFixed(2);
  if (unit === '%') body += '%';
  else if (unit === '×') body += '×';
  return sign + body;
}
function samples(x0, x1, n, log) {
  const out = [];
  if (!(x1 > x0) || (log && !(x0 > 0))) return out;
  for (let i = 0; i <= n; i++) {
    const t = i / n;
    out.push(log ? x0 * Math.pow(x1 / x0, t) : x0 + (x1 - x0) * t);
  }
  return out;
}
function fit(vals) {
  const clean = vals.filter(v => isFinite(v));
  let lo = Math.min.apply(null, clean);
  let hi = Math.max.apply(null, clean);
  if (!isFinite(lo) || !isFinite(hi)) { lo = 0; hi = 1; }
  if (!(hi > lo)) { lo -= 1; hi += 1; }
  const pad = (hi - lo) * 0.16;
  return [lo - (lo < 0 ? pad * 0.45 : 0), hi + pad];
}
function figure(label, body, legend, w, h) {
  const key = legend && legend.length
    ? '<p class="legend">' + legend.map(item => '<span><i style="background:' + item.color + '"></i>' + xml(item.name) + '</span>').join('') + '</p>'
    : '';
  return '<figure class="plot" aria-hidden="true"><svg viewBox="0 0 ' + w + ' ' + h + '" focusable="false">' + body + '</svg>' + key + '</figure>';
}
function curve(o) {
  const W = 640, H = 278, L = 56, R = 14, T = 18, B = 36;
  const x0 = o.x0, x1 = o.x1, y0 = o.y0, y1 = o.y1;
  const log = !!o.log;
  const spanX = log ? Math.log(x1 / x0) : (x1 - x0);
  const spanY = y1 - y0 || 1;
  const pw = W - L - R, ph = H - T - B;
  const X = x => L + (log ? Math.log(x / x0) / spanX : (x - x0) / spanX) * pw;
  const Y = y => T + (1 - (y - y0) / spanY) * ph;
  const clampY = y => Math.min(y1, Math.max(y0, y));
  let body = '';
  (o.bands || []).forEach(b => {
    const top = Y(Math.min(y1, Math.max(b.from, b.to)));
    const bot = Y(Math.max(y0, Math.min(b.from, b.to)));
    body += '<rect x="' + L + '" y="' + top.toFixed(1) + '" width="' + pw + '" height="' + Math.max(0, bot - top).toFixed(1) + '" fill="' + b.fill + '"/>';
  });
  (o.vbands || []).forEach(b => {
    const xa = X(Math.min(x1, Math.max(x0, b.from)));
    const xb = X(Math.min(x1, Math.max(x0, b.to)));
    body += '<rect x="' + Math.min(xa, xb).toFixed(1) + '" y="' + T + '" width="' + Math.abs(xb - xa).toFixed(1) + '" height="' + ph + '" fill="' + b.fill + '"/>';
  });
  if (o.zero !== false && y0 < 0 && y1 > 0) {
    body += '<line x1="' + L + '" y1="' + Y(0).toFixed(1) + '" x2="' + (W - R) + '" y2="' + Y(0).toFixed(1) + '" stroke="#d3dde6"/>';
  }
  (o.yticks || niceTicks(y0, y1, 4)).forEach(t => {
    if (t < y0 - 1e-6 || t > y1 + 1e-6) return;
    body += '<line x1="' + L + '" y1="' + Y(t).toFixed(1) + '" x2="' + (W - R) + '" y2="' + Y(t).toFixed(1) + '" stroke="#e6eef3"/>';
    body += '<text x="' + (L - 8) + '" y="' + (Y(t) + 4).toFixed(1) + '" text-anchor="end" font-size="12" fill="#3e4c59">' + xml(fmtTick(t, o.yunit || '')) + '</text>';
  });
  (o.xticks || (log ? [] : niceTicks(x0, x1, 5))).forEach(t => {
    if (t < x0 - 1e-9 || t > x1 + 1e-9) return;
    body += '<text x="' + X(t).toFixed(1) + '" y="' + (H - 12) + '" text-anchor="middle" font-size="12" fill="#3e4c59">' + xml(fmtTick(t, o.xunit || '')) + '</text>';
  });
  (o.series || []).forEach(s => {
    const pts = (s.pts || []).filter(p => isFinite(p[0]) && isFinite(p[1]) && p[0] >= x0 && p[0] <= x1);
    if (pts.length < 2) return;
    const base = s.base != null ? s.base : 0;
    if (s.split) {
      const groups = { up: [], down: [] };
      let cur = [], side = null;
      const flush = () => { if (cur.length > 1 && side) groups[side].push(cur); cur = []; };
      pts.forEach((p, i) => {
        const next = p[1] >= base ? 'up' : 'down';
        if (side && next !== side) {
          const a = pts[i - 1];
          const t = (base - a[1]) / ((p[1] - a[1]) || 1e-9);
          const cross = [a[0] + (p[0] - a[0]) * t, base];
          cur.push(cross);
          flush();
          side = next;
          cur = [cross, p];
        } else {
          side = next;
          cur.push(p);
        }
      });
      flush();
      const paint = (list, color) => list.forEach(poly => {
        let d = '';
        poly.forEach((p, i) => { d += (i ? 'L' : 'M') + X(p[0]).toFixed(1) + ' ' + Y(clampY(p[1])).toFixed(1) + ' '; });
        const yb = Y(clampY(base));
        d += 'L' + X(poly[poly.length - 1][0]).toFixed(1) + ' ' + yb.toFixed(1) + ' L' + X(poly[0][0]).toFixed(1) + ' ' + yb.toFixed(1) + ' Z';
        body += '<path d="' + d + '" fill="' + color + '" fill-opacity="0.16" stroke="none"/>';
      });
      paint(groups.up, '#12a888');
      paint(groups.down, '#9a3412');
    } else if (s.fill) {
      let d = '';
      pts.forEach((p, i) => { d += (i ? 'L' : 'M') + X(p[0]).toFixed(1) + ' ' + Y(clampY(p[1])).toFixed(1) + ' '; });
      const yb = Y(clampY(base));
      d += 'L' + X(pts[pts.length - 1][0]).toFixed(1) + ' ' + yb.toFixed(1) + ' L' + X(pts[0][0]).toFixed(1) + ' ' + yb.toFixed(1) + ' Z';
      body += '<path d="' + d + '" fill="' + s.fill + '" fill-opacity="' + (s.opacity == null ? 0.14 : s.opacity) + '" stroke="none"/>';
    }
    let d = '';
    pts.forEach((p, i) => { d += (i ? 'L' : 'M') + X(p[0]).toFixed(1) + ' ' + Y(clampY(p[1])).toFixed(1) + ' '; });
    body += '<path d="' + d + '" fill="none" stroke="' + (s.color || '#12a888') + '" stroke-width="' + (s.width || 2.5) + '"' + (s.dash ? ' stroke-dasharray="' + s.dash + '"' : '') + ' stroke-linejoin="round" stroke-linecap="round"/>';
  });
  (o.hlines || []).forEach(v => {
    if (v.y < y0 || v.y > y1) return;
    body += '<line x1="' + L + '" y1="' + Y(v.y).toFixed(1) + '" x2="' + (W - R) + '" y2="' + Y(v.y).toFixed(1) + '" stroke="' + (v.color || '#0a5c48') + '" stroke-dasharray="4 4"/>';
    if (v.label) body += '<text x="' + (L + 6) + '" y="' + (Y(v.y) - 6).toFixed(1) + '" font-size="12" fill="' + (v.color || '#0a5c48') + '">' + xml(v.label) + '</text>';
  });
  (o.vlines || []).forEach((v, i) => {
    if (v.x < x0 || v.x > x1) return;
    const x = X(v.x);
    body += '<line x1="' + x.toFixed(1) + '" y1="' + T + '" x2="' + x.toFixed(1) + '" y2="' + (H - B) + '" stroke="' + (v.color || '#9a3412') + '" stroke-dasharray="4 4"/>';
    if (v.label) {
      const anchor = x > W - 130 ? 'end' : 'start';
      body += '<text x="' + (x + (anchor === 'end' ? -6 : 6)).toFixed(1) + '" y="' + (T + 14 + (i % 3) * 15) + '" text-anchor="' + anchor + '" font-size="12" fill="' + (v.color || '#9a3412') + '">' + xml(v.label) + '</text>';
    }
  });
  (o.dots || []).forEach(d => {
    if (!isFinite(d.x) || !isFinite(d.y)) return;
    const cx = X(Math.min(x1, Math.max(x0, d.x)));
    const cy = Y(clampY(d.y));
    body += '<line x1="' + cx.toFixed(1) + '" y1="' + cy.toFixed(1) + '" x2="' + cx.toFixed(1) + '" y2="' + (H - B) + '" stroke="#07111c" stroke-opacity="0.2"/>';
    body += '<circle cx="' + cx.toFixed(1) + '" cy="' + cy.toFixed(1) + '" r="4.5" fill="#07111c"/>';
    body += '<circle cx="' + cx.toFixed(1) + '" cy="' + cy.toFixed(1) + '" r="7.5" fill="none" stroke="#07111c" stroke-width="1.5"/>';
    if (d.label) {
      const left = cx > W * 0.62;
      const above = cy > T + 28;
      body += '<text x="' + (cx + (left ? -12 : 12)).toFixed(1) + '" y="' + (above ? cy - 12 : cy + 18).toFixed(1) + '" text-anchor="' + (left ? 'end' : 'start') + '" font-size="12" font-weight="700" fill="#07111c">' + xml(d.label) + '</text>';
    }
  });
  return figure('', body, o.legend, W, H);
}
function waterfall(o) {
  const W = 640, H = 292, L = 58, R = 12, T = 26, B = 46;
  let run = 0;
  const bars = o.steps.map(s => {
    if (s.total != null) {
      return { name: s.name, lo: Math.min(0, s.total), hi: Math.max(0, s.total), end: s.total, label: s.label, fill: s.fill || (s.total >= 0 ? '#07111c' : '#9a3412') };
    }
    const start = run;
    run += s.delta;
    return { name: s.name, lo: Math.min(start, run), hi: Math.max(start, run), end: run, label: s.label, fill: s.fill || (s.delta >= 0 ? '#12a888' : '#9a3412') };
  });
  const vals = [0];
  bars.forEach(b => { vals.push(b.lo, b.hi); });
  let y0 = Math.min.apply(null, vals);
  let y1 = Math.max.apply(null, vals);
  if (!(y1 > y0)) { y0 -= 1; y1 += 1; }
  const pad = (y1 - y0) * 0.22;
  y0 = y0 < 0 ? y0 - pad * 0.25 : Math.min(0, y0);
  y1 += pad;
  const span = y1 - y0 || 1;
  const Y = y => T + (1 - (y - y0) / span) * (H - T - B);
  const n = Math.max(1, bars.length);
  const gap = 26;
  const bw = (W - L - R - gap * (n - 1)) / n;
  let body = '';
  if (y0 < 0 && y1 > 0) body += '<line x1="' + L + '" y1="' + Y(0).toFixed(1) + '" x2="' + (W - R) + '" y2="' + Y(0).toFixed(1) + '" stroke="#d3dde6"/>';
  niceTicks(y0, y1, 4).forEach(t => {
    if (t < y0 || t > y1) return;
    body += '<text x="' + (L - 8) + '" y="' + (Y(t) + 4).toFixed(1) + '" text-anchor="end" font-size="12" fill="#3e4c59">' + xml(fmtTick(t, o.yunit || '')) + '</text>';
    body += '<line x1="' + L + '" y1="' + Y(t).toFixed(1) + '" x2="' + (W - R) + '" y2="' + Y(t).toFixed(1) + '" stroke="#e6eef3"/>';
  });
  bars.forEach((b, i) => {
    const x = L + i * (bw + gap);
    const y = Y(b.hi);
    const h = Math.max(Y(b.lo) - y, 2);
    if (i < n - 1) {
      body += '<line x1="' + (x + bw).toFixed(1) + '" y1="' + Y(b.end).toFixed(1) + '" x2="' + (x + bw + gap).toFixed(1) + '" y2="' + Y(b.end).toFixed(1) + '" stroke="#9aafc0" stroke-dasharray="3 3"/>';
    }
    body += '<rect x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" width="' + bw.toFixed(1) + '" height="' + h.toFixed(1) + '" fill="' + b.fill + '"/>';
    const below = b.hi <= 0 && b.lo < 0;
    const labelY = below ? Y(b.lo) + 15 : y - 8;
    body += '<text x="' + (x + bw / 2).toFixed(1) + '" y="' + labelY.toFixed(1) + '" text-anchor="middle" font-size="13" font-weight="700" fill="#07111c">' + xml(b.label) + '</text>';
    body += '<text x="' + (x + bw / 2).toFixed(1) + '" y="' + (H - 16) + '" text-anchor="middle" font-size="12" fill="#3e4c59">' + xml(b.name) + '</text>';
  });
  return figure('', body, o.legend, W, H);
}
function columns(o) {
  const W = 640, H = 276, L = 56, R = 16, T = 22, B = 42;
  const vals = [0].concat(o.bars.map(b => b.value), o.line || []);
  if (o.rule) vals.push(o.rule.value);
  const fitted = fit(vals);
  const y0 = fitted[0], y1 = fitted[1], span = y1 - y0 || 1;
  const Y = y => T + (1 - (y - y0) / span) * (H - T - B);
  const n = o.bars.length;
  const slot = (W - L - R) / Math.max(1, n);
  const bw = Math.min(72, slot * 0.5);
  let body = '';
  if (y0 < 0 && y1 > 0) body += '<line x1="' + L + '" y1="' + Y(0).toFixed(1) + '" x2="' + (W - R) + '" y2="' + Y(0).toFixed(1) + '" stroke="#d3dde6"/>';
  niceTicks(y0, y1, 4).forEach(t => {
    if (t < y0 || t > y1) return;
    body += '<line x1="' + L + '" y1="' + Y(t).toFixed(1) + '" x2="' + (W - R) + '" y2="' + Y(t).toFixed(1) + '" stroke="#e6eef3"/>';
    body += '<text x="' + (L - 8) + '" y="' + (Y(t) + 4).toFixed(1) + '" text-anchor="end" font-size="12" fill="#3e4c59">' + xml(fmtTick(t, o.yunit || '')) + '</text>';
  });
  if (o.rule && o.rule.value >= y0 && o.rule.value <= y1) {
    body += '<line x1="' + L + '" y1="' + Y(o.rule.value).toFixed(1) + '" x2="' + (W - R) + '" y2="' + Y(o.rule.value).toFixed(1) + '" stroke="#0a5c48" stroke-dasharray="4 4"/>';
    body += '<text x="' + (L + 6) + '" y="' + (Y(o.rule.value) - 6).toFixed(1) + '" font-size="12" fill="#0a5c48">' + xml(o.rule.label) + '</text>';
  }
  o.bars.forEach((b, i) => {
    const cx = L + slot * (i + 0.5);
    const y = Y(Math.max(b.value, 0));
    const h = Math.max(Math.abs(Y(b.value) - Y(0)), 2);
    body += '<rect x="' + (cx - bw / 2).toFixed(1) + '" y="' + y.toFixed(1) + '" width="' + bw.toFixed(1) + '" height="' + h.toFixed(1) + '" fill="' + (b.value >= 0 ? '#12a888' : '#9a3412') + '"/>';
    const ly = b.value >= 0 ? y - 8 : y + h + 14;
    body += '<text x="' + cx.toFixed(1) + '" y="' + ly.toFixed(1) + '" text-anchor="middle" font-size="12" font-weight="700" fill="#07111c">' + xml(fmtTick(b.value, o.yunit || '')) + '</text>';
    body += '<text x="' + cx.toFixed(1) + '" y="' + (H - 14) + '" text-anchor="middle" font-size="12" fill="#3e4c59">' + xml(b.name) + '</text>';
  });
  if (o.line && o.line.length) {
    let d = '';
    o.line.forEach((y, i) => {
      const cx = L + slot * (i + 0.5);
      d += (i ? 'L' : 'M') + cx.toFixed(1) + ' ' + Y(y).toFixed(1) + ' ';
      body += '<circle cx="' + cx.toFixed(1) + '" cy="' + Y(y).toFixed(1) + '" r="4" fill="#07111c"/>';
    });
    body += '<path d="' + d + '" fill="none" stroke="#07111c" stroke-width="2"/>';
    const last = o.line[o.line.length - 1];
    const cx = L + slot * (o.line.length - 0.5);
    body += '<text x="' + (cx - 8).toFixed(1) + '" y="' + (Y(last) - 10).toFixed(1) + '" text-anchor="end" font-size="12" font-weight="700" fill="#07111c">' + xml(o.lineLabel || fmtTick(last, o.yunit || '')) + '</text>';
  }
  return figure('', body, o.legend, W, H);
}
function meters(o) {
  const W = 640, rowH = 64, H = 8 + o.rows.length * rowH, L = 4, R = 4;
  let body = '';
  o.rows.forEach((row, i) => {
    const y = 8 + i * rowH;
    const x0 = L, w = W - L - R, by = y + 24, bh = 16;
    body += '<text x="' + x0 + '" y="' + (y + 14) + '" font-size="13" font-weight="700" fill="#14202b">' + xml(row.name) + '</text>';
    body += '<text x="' + (x0 + w) + '" y="' + (y + 14) + '" text-anchor="end" font-size="13" font-weight="700" fill="#07111c">' + xml(row.value) + '</text>';
    (row.zones || [{ from: 0, to: 1, fill: '#e7f6f1' }]).forEach(z => {
      const a = x0 + z.from * w, b = x0 + z.to * w;
      body += '<rect x="' + a.toFixed(1) + '" y="' + by + '" width="' + Math.max(0, b - a).toFixed(1) + '" height="' + bh + '" fill="' + z.fill + '"/>';
    });
    body += '<rect x="' + x0 + '" y="' + by + '" width="' + w + '" height="' + bh + '" fill="none" stroke="#d3dde6"/>';
    (row.ticks || []).forEach(t => {
      const x = x0 + Math.min(1, Math.max(0, t.at)) * w;
      body += '<line x1="' + x.toFixed(1) + '" y1="' + (by - 4) + '" x2="' + x.toFixed(1) + '" y2="' + (by + bh + 4) + '" stroke="' + (t.color || '#0a5c48') + '"/>';
      body += '<text x="' + x.toFixed(1) + '" y="' + (by + bh + 16) + '" text-anchor="middle" font-size="11" fill="#3e4c59">' + xml(t.label) + '</text>';
    });
    const nx = x0 + Math.min(1, Math.max(0, row.at)) * w;
    body += '<circle cx="' + nx.toFixed(1) + '" cy="' + (by + bh / 2) + '" r="6.5" fill="#fff" stroke="#07111c" stroke-width="2.5"/>';
  });
  return figure('', body, null, W, H);
}
function lossScale(o) {
  const W = 640, H = 150, L = 56, R = 18, T = 28, B = 32;
  const x1 = o.max > 0 ? o.max : 1;
  const X = x => L + Math.min(1, Math.max(0, x / x1)) * (W - L - R);
  const y = 70;
  let body = '';
  body += '<line x1="' + L + '" y1="' + y + '" x2="' + (W - R) + '" y2="' + y + '" stroke="#d3dde6" stroke-width="8" stroke-linecap="round"/>';
  body += '<line x1="' + L + '" y1="' + y + '" x2="' + X(o.current).toFixed(1) + '" y2="' + y + '" stroke="#9a3412" stroke-width="8" stroke-linecap="round"/>';
  niceTicks(0, x1, 4).forEach(t => {
    body += '<text x="' + X(t).toFixed(1) + '" y="' + (H - 10) + '" text-anchor="middle" font-size="12" fill="#3e4c59">' + xml(fmtTick(t, '$')) + '</text>';
  });
  (o.marks || []).forEach(m => {
    const x = X(m.x);
    const labelY = m.current ? y - 16 : y + 22;
    body += '<line x1="' + x.toFixed(1) + '" y1="' + (y - 16) + '" x2="' + x.toFixed(1) + '" y2="' + (y + 16) + '" stroke="' + (m.current ? '#07111c' : '#3e4c59') + '" stroke-width="' + (m.current ? 2 : 1) + '"/>';
    body += '<text x="' + x.toFixed(1) + '" y="' + labelY + '" text-anchor="middle" font-size="12" font-weight="' + (m.current ? 700 : 500) + '" fill="' + (m.current ? '#07111c' : '#3e4c59') + '">' + xml(m.label) + '</text>';
  });
  return figure('', body, o.legend, W, H);
}
const minusMoney = x => (x < 0 ? '−' : '') + money(Math.abs(x)).replace(/^−/, '');
const pretty = x => { const a = Math.abs(x); return Math.abs(a - Math.round(a)) < 0.05 ? String(Math.round(a)) : a.toFixed(1); };
const RUN = {
  health: v => {
    if (!(v.qty > 0 && v.price > 0 && v.debt > 0)) return say('Quantity, price, and debt must be above zero.');
    if (!(v.lt > 0 && v.lt < 1)) return say('Liquidation threshold must be between 0 and 1.');
    const coll = v.qty * v.price, hf = coll * v.lt / v.debt, liq = v.debt / (v.qty * v.lt);
    const move = (liq / v.price - 1) * 100;
    const under = hf < 2;
    const spoken = hf < 1
      ? 'Health factor is below 1. This position can be liquidated now.'
      : hf < 1.5
        ? 'Health factor is below 1.5. Repay or add collateral.'
        : under
          ? 'Health factor is under 2. The lesson buffer is 2.0.'
          : 'The position liquidates at ' + money(liq) + ', ' + pretty(move) + '% ' + (move < 0 ? 'under' : 'above') + ' the current price.';
    const x0 = liq * 0.55;
    const x1 = Math.max(v.price, liq * 2.4) * 1.2;
    const yHi = Math.max(3.6, Math.min(12, hf * 1.12 + 0.3));
    const hfAt = p => v.qty * p * v.lt / v.debt;
    const graph = curve({
      x0: x0, x1: x1, y0: 0, y1: yHi, xunit: '$', zero: false,
      bands: [
        { from: 0, to: 1, fill: '#f8efea' },
        { from: 1, to: 1.5, fill: '#f8f1e6' },
        { from: 1.5, to: 2, fill: '#f3f6ea' },
        { from: 2, to: yHi, fill: '#e7f6f1' }
      ],
      hlines: [
        { y: 1, label: 'Can liquidate', color: '#9a3412' },
        { y: 1.5, color: '#c2410c' },
        { y: 2, label: 'Lesson buffer', color: '#0a5c48' }
      ],
      vlines: [{ x: liq, label: 'Liquidation ' + money(liq), color: '#9a3412' }],
      series: [{ pts: samples(x0, x1, 72, false).map(p => [p, hfAt(p)]), color: '#07111c', width: 2.5 }],
      dots: [{ x: v.price, y: hf, label: 'Now ' + hf.toFixed(2) }],
      legend: [{ color: '#07111c', name: 'Health factor as price moves' }]
    });
    return panel('Health factor ' + hf.toFixed(2), [
      ['Collateral', money(coll)],
      ['LTV', pct(v.debt / coll, 1)],
      ['Liquidation price', money(liq)],
      ['Distance to liquidation', signed(move)],
      ['Max debt for health factor 1.5', money(coll * v.lt / 1.5)],
      ['Max debt for health factor 2.0', money(coll * v.lt / 2)]
    ], spoken, { tone: under ? 'warn' : 'ok', label: under ? 'Under the lesson buffer' : 'Inside the 2.0 buffer' }, graph);
  },
  il: v => {
    if (!(v.ratio > 0)) return say('Price ratio must be above zero.');
    const loss = ilLoss(v.ratio);
    const moveWord = v.ratio === 2 ? 'double the price' : v.ratio === 0.5 ? 'half the price' : v.ratio + '× the entry price';
    const x0 = Math.min(0.25, v.ratio);
    const x1 = Math.max(4, v.ratio);
    const yAt = r => -ilLoss(r) * 100;
    const ticks = [0.25, 0.5, 1, 2, 3, 4].filter(t => t >= x0 * 0.999 && t <= x1 * 1.001);
    const graph = curve({
      x0: x0, x1: x1, y0: Math.min(yAt(x0), yAt(x1), -8) - 2, y1: 6, log: true, xticks: ticks,
      xunit: '×', yunit: '%',
      hlines: [{ y: 0, label: 'Holding both', color: '#0a5c48' }],
      vlines: [0.5, 2, 3].filter(r => r >= x0 && r <= x1 && Math.abs(Math.log(r / v.ratio)) > 0.08).map(r => ({
        x: r, label: r + '×  ' + pct(ilLoss(r)), color: '#3e4c59'
      })),
      series: [{ pts: samples(x0, x1, 90, true).map(r => [r, yAt(r)]), color: '#9a3412', width: 2.5, fill: '#9a3412', base: 0 }],
      dots: [{ x: v.ratio, y: yAt(v.ratio), label: 'Now ' + (yAt(v.ratio) >= 0 ? '+' : '−') + Math.abs(yAt(v.ratio)).toFixed(2) + '%' }],
      legend: [{ color: '#9a3412', name: 'Behind holding, before fees' }]
    });
    return panel(pct(loss) + ' behind holding', [
      ['Price move', v.ratio + '×, before fees'],
      ['At half the price', pct(ilLoss(0.5)) + ' behind'],
      ['At double the price', pct(ilLoss(2)) + ' behind'],
      ['At triple the price', pct(ilLoss(3)) + ' behind']
    ], 'At ' + moveWord + ', the pool is ' + pct(loss) + ' behind simply holding.', null, graph);
  },
  'lp-breakeven': v => {
    if (!(v.ratio > 0) || !(v.days > 0)) return say('Price ratio and days must be above zero.');
    const loss = ilLoss(v.ratio), need = loss * 365 / v.days, earned = v.fee / 100 * v.days / 365, net = earned - loss;
    const short = net < 0;
    const x0 = Math.min(0.4, v.ratio * 0.7);
    const x1 = Math.max(3.2, v.ratio * 1.35);
    const netAt = r => (v.fee / 100 * v.days / 365 - ilLoss(r)) * 100;
    const pts = samples(x0, x1, 100, true).map(r => [r, netAt(r)]);
    const span = fit(pts.map(p => p[1]).concat([0]));
    const crosses = [];
    for (let i = 1; i < pts.length && crosses.length < 2; i++) {
      const a = pts[i - 1], b = pts[i];
      if ((a[1] < 0 && b[1] >= 0) || (a[1] >= 0 && b[1] < 0)) {
        const t = a[1] / (a[1] - b[1]);
        crosses.push(a[0] * Math.pow(b[0] / a[0], t));
      }
    }
    const graph = curve({
      x0: x0, x1: x1, y0: span[0], y1: span[1], log: true,
      xticks: [0.5, 1, 1.5, 2, 3].filter(t => t >= x0 && t <= x1),
      xunit: '×', yunit: '%',
      vlines: crosses.map(x => ({ x: x, label: 'Even at ' + x.toFixed(2) + '×', color: '#0a5c48' })),
      series: [{ pts: pts, color: '#12a888', width: 2.5, split: true }],
      dots: [{ x: v.ratio, y: netAt(v.ratio), label: 'Now ' + (net >= 0 ? '+' : '−') + Math.abs(net * 100).toFixed(2) + '%' }],
      legend: [{ color: '#12a888', name: 'Fees minus impermanent loss' }]
    });
    return panel('Fee APR of ' + pct(need) + ' to match holding', [
      ['Move', v.ratio + '× over ' + v.days + ' days'],
      ['Impermanent loss', pct(loss)],
      ['Earned at this fee APR', pct(earned)],
      ['Net versus holding', (net >= 0 ? '+' : '') + pct(net)]
    ], 'Over ' + v.days + ' days at ' + v.ratio + '×, fees need a ' + pct(need) + ' APR to match holding. At ' + v.fee + '%, you finish ' + (net >= 0 ? pct(net) + ' ahead' : pct(Math.abs(net)) + ' behind') + '.', { tone: short ? 'warn' : 'ok', label: short ? 'Fees fall short' : 'Fees cover the loss' }, graph);
  },
  loop: v => {
    if (!(v.ltv > 0 && v.ltv < 1)) return say('Borrow LTV must be between 0 and 1.');
    if (!(v.loops >= 0)) return say('Loops must be zero or more.');
    const L = v.ltv, lev = (1 - Math.pow(L, v.loops + 1)) / (1 - L);
    const net = v.capy * lev - v.bapy * (lev - 1);
    const be = lev > 1 ? v.capy * lev / (lev - 1) : Infinity;
    const flat = net <= v.capy;
    const spoken = flat
      ? 'At this borrow rate, leverage does not raise the yield. It only adds liquidation risk.'
      : 'Each $1 of your money controls $' + lev.toFixed(2) + ' of the position, and the extra yield disappears if borrow reaches ' + be.toFixed(2) + '%.';
    const netAt = b => v.capy * lev - b * (lev - 1);
    const x1 = Math.max(8, v.bapy * 1.35, isFinite(be) ? be * 1.28 : 0);
    const ySpan = fit([netAt(0), netAt(x1), v.capy, 0]);
    const vlines = [];
    if (v.capy > 0 && v.capy < x1) vlines.push({ x: v.capy, label: 'Borrow matches yield', color: '#0a5c48' });
    if (isFinite(be) && be > 0 && be < x1) vlines.push({ x: be, label: 'Zero at ' + be.toFixed(2) + '%', color: '#9a3412' });
    const graph = curve({
      x0: 0, x1: x1, y0: ySpan[0], y1: ySpan[1], xunit: '%', yunit: '%',
      hlines: [{ y: v.capy, label: 'Unlevered ' + v.capy.toFixed(2) + '%', color: '#0a5c48' }],
      vlines: vlines,
      series: [{ pts: samples(0, x1, 72, false).map(b => [b, netAt(b)]), color: '#12a888', width: 2.5, split: true }],
      dots: [{ x: Math.min(v.bapy, x1), y: net, label: 'Now ' + pctPts(net) }],
      legend: [{ color: '#12a888', name: 'Net APY on your money' }, { color: '#0a5c48', name: 'Yield with no leverage' }]
    });
    return panel(lev.toFixed(2) + '× leverage', [
      ['Loops', v.loops + ' at LTV ' + L.toFixed(2)],
      ['Maximum if you kept looping', (1 / (1 - L)).toFixed(2) + '×'],
      ['Net APY on equity', pctPts(net)],
      ['Unlevered collateral yield', v.capy.toFixed(2) + '%'],
      ['Borrow rate that wipes the return', be === Infinity ? '—' : be.toFixed(2) + '%']
    ], spoken, flat ? { tone: 'warn', label: 'Leverage adds nothing' } : null, graph);
  },
  lvr: v => {
    if (!(v.vol >= 0)) return say('Volatility must be zero or more.');
    const r = (v.vol / 100) ** 2 / 8, gap = v.fee - r * 100;
    const short = gap < 0;
    const lvrAt = vol => (vol / 100) * (vol / 100) / 8 * 100;
    const x1 = Math.max(120, v.vol * 1.45, 20);
    const beVol = Math.sqrt(Math.max(0, 8 * v.fee / 100)) * 100;
    const yTop = Math.max(lvrAt(x1), v.fee, 1) * 1.12;
    const graph = curve({
      x0: 0, x1: x1, y0: 0, y1: yTop, xunit: '%', yunit: '%', zero: false,
      hlines: [{ y: v.fee, label: 'Fee APR ' + v.fee.toFixed(1) + '%', color: '#0a5c48' }],
      vlines: beVol > 0 && beVol < x1 ? [{ x: beVol, label: 'Fees match at ' + beVol.toFixed(0) + '% vol', color: '#9a3412' }] : [],
      series: [{ pts: samples(0, x1, 72, false).map(vol => [vol, lvrAt(vol)]), color: '#9a3412', width: 2.5, fill: '#9a3412', base: 0 }],
      dots: [{ x: v.vol, y: r * 100, label: 'Now ' + (r * 100).toFixed(2) + '%' }],
      legend: [{ color: '#9a3412', name: 'Lost to rebalancing' }, { color: '#0a5c48', name: 'Fee income' }]
    });
    return panel(pct(r) + ' lost to rebalancing', [
      ['Fee APR', v.fee.toFixed(2) + '%'],
      ['Fees minus LVR', (gap >= 0 ? '+' : '−') + Math.abs(gap).toFixed(2) + '% per year']
    ], 'Arbitrage costs about ' + pct(r) + ' a year. Fees of ' + v.fee.toFixed(2) + '% leave ' + (gap >= 0 ? '+' : '−') + Math.abs(gap).toFixed(2) + '% after that cost.', { tone: short ? 'warn' : 'ok', label: short ? 'Fees fall short' : 'Fees cover the cost' }, graph);
  },
  pt: v => {
    if (!(v.price > 0) || !(v.days > 0)) return say('Price and days must be above zero.');
    if (v.price >= 1) return say('A principal token at or above 1 of the underlying does not lock in a positive fixed yield.');
    const fixed = Math.pow(1 / v.price, 365 / v.days) - 1, simple = (1 / v.price - 1) * 365 / v.days;
    const fixedAt = p => (Math.pow(1 / p, 365 / v.days) - 1) * 100;
    const simpleAt = p => (1 / p - 1) * 365 / v.days * 100;
    let x0 = Math.max(0.5, v.price - 0.14);
    const ceiling = Math.max(fixed * 100, simple * 100, 4) * 2.4;
    while (x0 < v.price - 0.02 && fixedAt(x0) > ceiling) x0 += 0.005;
    const x1 = 0.995;
    const yTop = ceiling;
    const graph = curve({
      x0: x0, x1: x1, y0: 0, y1: yTop, yunit: '%', zero: false,
      xticks: [0.6, 0.7, 0.8, 0.9, 0.95].filter(t => t >= x0 && t <= x1),
      series: [
        { pts: samples(x0, x1, 64, false).map(p => [p, fixedAt(p)]), color: '#12a888', width: 2.5, fill: '#12a888', base: 0 },
        { pts: samples(x0, x1, 64, false).map(p => [p, simpleAt(p)]), color: '#0a5c48', width: 1.75, dash: '5 4' }
      ],
      dots: [{ x: v.price, y: fixed * 100, label: 'Now ' + pct(fixed) }],
      legend: [{ color: '#12a888', name: 'Fixed if held to maturity' }, { color: '#0a5c48', name: 'Simple annualised' }]
    });
    return panel(pct(fixed) + ' fixed if held', [
      ['PT price', v.price + ' of 1'],
      ['Days', String(v.days)],
      ['Simple annualised', pct(simple)],
      ['Yield token cost', (1 - v.price).toFixed(4) + ' per unit']
    ], 'Buying at ' + v.price + ' and holding ' + v.days + ' days locks about ' + pct(fixed) + ' a year if you stay to maturity. The yield token profits only if variable yield beats that.', null, graph);
  },
  expected: v => {
    if (v.p < 0 || v.p > 1 || v.lgd < 0 || v.lgd > 1) return say('Loss probability and loss given default must be between 0 and 1.');
    const h = v.p * v.lgd * 100, net = v.y - h - v.c;
    const graph = waterfall({
      yunit: '%',
      steps: [
        { name: 'Headline', delta: v.y, label: pctPts(v.y) },
        { name: 'Expected loss', delta: -h, label: pctPts(-h) },
        { name: 'Costs', delta: -v.c, label: pctPts(-v.c) },
        { name: 'Left', total: net, label: pctPts(net) }
      ]
    });
    return panel(pctPts(net) + ' after risk', [
      ['Headline yield', v.y.toFixed(2) + '%'],
      ['Expected loss', h.toFixed(2) + '%'],
      ['Loss probability', v.p.toFixed(2)],
      ['Loss given default', v.lgd.toFixed(2)],
      ['Costs', v.c.toFixed(2) + '%']
    ], 'After a ' + pct(v.p, 0) + ' chance of losing ' + pct(v.lgd, 0) + ', and ' + v.c + '% in costs, the ' + v.y + '% headline is ' + pctPts(net) + '.', null, graph);
  },
  income: v => {
    if (!(v.cap > 0)) return say('Capital must be above zero.');
    if (v.payout < 0 || v.payout > 1) return say('Payout ratio must be between 0 and 1.');
    const exp = v.cap * v.ry / 100, pay = exp * v.payout;
    const thin = v.payout > 0.8;
    const held = exp - pay;
    const graph = waterfall({
      yunit: '$',
      steps: [
        { name: 'Expected', delta: exp, label: money(exp) },
        { name: 'Held back', delta: -held, label: minusMoney(-held) },
        { name: 'Paid / year', total: pay, label: money(pay) }
      ],
      legend: [{ color: '#07111c', name: money(pay / 12) + ' a month. Illustrative only.' }]
    });
    return panel(money(pay / 12) + ' per month', [
      ['Expected income', money(exp) + ' per year'],
      ['Risk-adjusted yield', v.ry.toFixed(2) + '%'],
      ['Payout', pct(v.payout, 0) + ', ' + money(pay) + ' per year'],
      ['Retained as a buffer', money(exp - pay)]
    ], 'On ' + money(v.cap) + ' at ' + v.ry + '%, expected income is ' + money(exp) + ' a year. Paying out ' + pct(v.payout, 0) + ' is ' + money(pay / 12) + ' a month, and ' + money(exp - pay) + ' stays back. Illustrative only. No income is promised.', thin ? { tone: 'warn', label: 'Thin buffer' } : null, graph);
  },
  var: v => {
    if (!(v.pos > 0) || !(v.vol >= 0) || !(v.z > 0)) return say('Position and confidence must be above zero. Volatility must be zero or more.');
    const d = v.vol / 100 / Math.sqrt(365), x = v.z * d * v.pos;
    const lossAt = z => z * d * v.pos;
    const marks = [{ z: 1.28, name: '90%' }, { z: 1.65, name: '95%' }, { z: 2.33, name: '99%' }];
    if (!marks.some(m => Math.abs(m.z - v.z) < 0.03)) marks.push({ z: v.z, name: 'This z' });
    const maxLoss = Math.max.apply(null, marks.map(m => lossAt(m.z)).concat([x])) * 1.25;
    const graph = lossScale({
      max: maxLoss,
      current: x,
      marks: marks.map(m => {
        const here = Math.abs(m.z - v.z) < 0.03;
        return { x: lossAt(m.z), label: here ? m.name + '  ' + money(lossAt(m.z)) : m.name, current: here };
      }),
      legend: [{ color: '#9a3412', name: 'Model floor for one day. Crypto tails are fatter.' }]
    });
    return panel(money(x) + ' on a bad day', [
      ['Position', money(v.pos)],
      ['Daily volatility', pct(d)],
      ['Move at this confidence', pct(v.z * d)]
    ], 'On a bad day at this confidence, the model puts the loss near ' + money(x) + '. Crypto tails are fatter than that.', null, graph);
  },
  cl: v => {
    if (!(v.low > 0 && v.low < v.high)) return say('The low price must be above zero and below the high price.');
    const eff = 1 / (1 - Math.pow(v.low / v.high, 0.25));
    const width = v.high / v.low;
    const conc = w => 1 / (1 - Math.pow(1 / w, 0.25));
    const x0 = Math.min(1.2, Math.max(1.04, width * 0.85));
    const x1 = Math.max(4, width * 1.45);
    const yTop = Math.min(conc(x0), Math.max(eff * 1.8, 12)) * 1.05;
    const graph = curve({
      x0: x0, x1: x1, y0: 0, y1: Math.max(yTop, eff * 1.15), xunit: '×', yunit: '×', zero: false,
      series: [{ pts: samples(x0, x1, 72, false).map(w => [w, conc(w)]), color: '#12a888', width: 2.5, fill: '#12a888', base: 0 }],
      dots: [{ x: width, y: eff, label: 'Now ' + eff.toFixed(1) + '×' }],
      legend: [{ color: '#12a888', name: 'Fees and impermanent loss both scale by this, inside the range' }]
    });
    return panel(eff.toFixed(1) + '× versus full range', [
      ['Range', money(v.low) + ' – ' + money(v.high)],
      ['Geometric mid', money(Math.sqrt(v.low * v.high))],
      ['Width', (v.high / v.low).toFixed(2) + '×']
    ], 'A range from ' + money(v.low) + ' to ' + money(v.high) + ' concentrates the position about ' + eff.toFixed(1) + '× versus the full range. Inside the range, fees and impermanent loss both scale by about that. Outside it, fees stop and the position becomes one asset.', null, graph);
  },
  carry: v => {
    if (!(v.shortlev > 0)) return say('Short leverage must be above zero.');
    const apr = v.rate * 3 * 365, capital = 1 + 1 / v.shortlev, on = apr / capital;
    const x1 = Math.max(0.04, Math.abs(v.rate) * 2.4, 0.01);
    const x0 = Math.min(0, v.rate);
    const hedgeAt = rate => rate * 3 * 365;
    const onAt = rate => hedgeAt(rate) / capital;
    const ySpan = fit([0, hedgeAt(x0), hedgeAt(x1), onAt(x0), onAt(x1)]);
    const graph = curve({
      x0: x0, x1: x1, y0: ySpan[0], y1: ySpan[1], xunit: '%', yunit: '%',
      series: [
        { pts: samples(x0, x1, 40, false).map(rate => [rate, hedgeAt(rate)]), color: '#0a5c48', width: 2, dash: '5 4' },
        { pts: samples(x0, x1, 40, false).map(rate => [rate, onAt(rate)]), color: '#12a888', width: 2.5, fill: '#12a888', base: 0 }
      ],
      dots: [{ x: v.rate, y: on, label: 'Now ' + pctPts(on) }],
      legend: [
        { color: '#0a5c48', name: 'APR on the hedge' },
        { color: '#12a888', name: 'APR on the money you post' }
      ]
    });
    return panel(pctPts(on) + ' on your money', [
      ['Funding APR on the hedge', pctPts(apr)],
      ['Capital per $1 hedged', money(capital)],
      ['Short liquidates near', '+' + (100 / v.shortlev).toFixed(0) + '%']
    ], 'Funding of ' + v.rate + '% every 8 hours is ' + pctPts(apr) + ' a year on the hedge, and about ' + pctPts(on) + ' on the money you actually post. Keep a buffer above a ' + (100 / v.shortlev).toFixed(0) + '% move.', null, graph);
  },
  supply: v => {
    if (v.util < 0 || v.util > 1 || v.reserve < 0 || v.reserve > 1) return say('Utilisation and reserve factor must be between 0 and 1.');
    const s = v.bapy * v.util * (1 - v.reserve);
    const idle = v.bapy * (1 - v.util);
    const kept = v.bapy * v.util * v.reserve;
    const graph = waterfall({
      yunit: '%',
      steps: [
        { name: 'Borrow rate', delta: v.bapy, label: pctPts(v.bapy) },
        { name: 'Idle', delta: -idle, label: pctPts(-idle) },
        { name: 'Reserve', delta: -kept, label: pctPts(-kept) },
        { name: 'Lenders', total: s, label: pctPts(s) }
      ]
    });
    return panel(pctPts(s) + ' to lenders', [
      ['Borrow APY', v.bapy + '%'],
      ['Utilisation', v.util.toFixed(2)],
      ['Reserve factor', v.reserve.toFixed(2)],
      ['Kept by the protocol', (v.bapy * v.util * v.reserve).toFixed(2) + '%']
    ], 'Lenders receive ' + pctPts(s) + ': the ' + v.bapy + '% borrow rate times ' + v.util.toFixed(2) + ' utilisation, after a ' + v.reserve.toFixed(2) + ' reserve.', null, graph);
  },
  apy: v => {
    if (!(v.n > 0)) return say('Compounds per year must be above zero.');
    const apy = Math.pow(1 + v.apr / 100 / v.n, v.n) - 1;
    const bits = [['APR', v.apr + '%'], ['Compounds per year', String(v.n)], ['APY before gas', pct(apy)]];
    let heavy = false;
    let spoken = v.apr + '% APR compounded ' + v.n + ' times a year is ' + pct(apy) + ' before gas.';
    if (v.pos > 0 && v.gas > 0) {
      const per = v.pos * v.apr / 100 / v.n;
      bits.push(['Reward per compound', money(per)], ['Gas per compound', money(v.gas)]);
      heavy = per < 10 * v.gas;
      if (heavy) spoken += ' Compound less often. Gas is large next to each reward.';
    }
    const x0 = 1;
    const x1 = Math.max(365, v.n);
    const grossAt = n => (Math.pow(1 + v.apr / 100 / n, n) - 1) * 100;
    const dragAt = n => (v.pos > 0 && v.gas > 0) ? v.gas * n / v.pos * 100 : 0;
    const netAt = n => grossAt(n) - dragAt(n);
    const cont = (Math.exp(v.apr / 100) - 1) * 100;
    const xs = samples(x0, x1, 48, true);
    const ys = xs.map(netAt).concat(xs.map(grossAt), [0, cont]);
    const ySpan = fit(ys);
    const series = [{ pts: xs.map(n => [n, grossAt(n)]), color: '#0a5c48', width: 1.75, dash: '5 4' }];
    const legend = [{ color: '#0a5c48', name: 'APY before gas' }];
    if (v.pos > 0 && v.gas > 0) {
      series.push({ pts: xs.map(n => [n, netAt(n)]), color: '#12a888', width: 2.5, split: true });
      legend.unshift({ color: '#12a888', name: 'After gas' });
    } else {
      series[0] = { pts: xs.map(n => [n, grossAt(n)]), color: '#12a888', width: 2.5, fill: '#12a888', base: 0 };
      legend[0] = { color: '#12a888', name: 'APY before gas' };
    }
    const graph = curve({
      x0: x0, x1: x1, y0: ySpan[0], y1: ySpan[1], log: true,
      xticks: [1, 12, 52, 365].filter(t => t >= x0 && t <= x1),
      yunit: '%',
      hlines: [{ y: cont, label: 'Continuous ' + pctPts(cont), color: '#3e4c59' }],
      series: series,
      dots: v.pos > 0 && v.gas > 0
        ? [
            { x: v.n, y: grossAt(v.n), label: 'Before gas ' + pctPts(grossAt(v.n)) },
            { x: v.n, y: netAt(v.n), label: 'After gas ' + pctPts(netAt(v.n)) }
          ]
        : [{ x: v.n, y: grossAt(v.n), label: 'Now ' + pctPts(apy * 100) }],
      legend: legend
    });
    return panel(pct(apy) + ' before gas', bits, spoken, heavy ? { tone: 'warn', label: 'Compound less often' } : null, graph);
  },
  airdrop: v => {
    if (v.prob < 0 || v.prob > 1) return say('Probability must be between 0 and 1.');
    const ev = v.prob * v.value - v.costs;
    const weighted = v.prob * v.value;
    const missed = v.value - weighted;
    const graph = waterfall({
      yunit: '$',
      steps: [
        { name: 'If it pays', delta: v.value, label: money(v.value) },
        { name: 'Chance misses', delta: -missed, label: minusMoney(-missed) },
        { name: 'Costs', delta: -v.costs, label: minusMoney(-v.costs) },
        { name: 'Expected', total: ev, label: money(ev) }
      ]
    });
    return panel(money(ev) + ' expected', [
      ['Probability', v.prob.toFixed(2)],
      ['Value if it happens', money(v.value)],
      ['Costs', money(v.costs)]
    ], 'A ' + v.prob.toFixed(2) + ' chance of ' + money(v.value) + ', minus ' + money(v.costs) + ' in costs, is worth ' + money(ev) + '.', ev < 0 ? { tone: 'warn', label: 'Worth less than the cost' } : null, graph);
  },
  basis: v => {
    if (!(v.spot > 0) || !(v.future > 0) || !(v.days > 0)) return say('Spot, future, and days must be above zero.');
    const b = v.future / v.spot - 1;
    const x0 = Math.min(14, v.days);
    const x1 = Math.max(365, v.days * 1.15);
    const annAt = days => b * 365 / days * 100;
    const ySpan = fit([0, annAt(x0), annAt(x1), annAt(v.days)]);
    const graph = curve({
      x0: x0, x1: x1, y0: ySpan[0], y1: ySpan[1], yunit: '%',
      xticks: [30, 90, 180, 365].filter(t => t >= x0 && t <= x1),
      hlines: [{ y: b * 100, label: 'Raw basis ' + pct(b), color: '#0a5c48' }],
      series: [{ pts: samples(x0, x1, 64, false).map(days => [days, annAt(days)]), color: '#12a888', width: 2.5, split: true }],
      dots: [{ x: v.days, y: annAt(v.days), label: 'Now ' + pct(b * 365 / v.days) }],
      legend: [{ color: '#12a888', name: 'Annualised basis as expiry lengthens' }]
    });
    return panel(pct(b * 365 / v.days) + ' a year', [
      ['Basis', pct(b)],
      ['Days', String(v.days)],
      ['Spot', money(v.spot)],
      ['Future', money(v.future)]
    ], 'The future is ' + pct(b) + ' ' + (b >= 0 ? 'above' : 'below') + ' spot. Over ' + v.days + ' days that is ' + pct(b * 365 / v.days) + ' a year, if both legs are held to expiry and margin is never called.', null, graph);
  },
  'covered-call': v => {
    if (!(v.spot > 0) || !(v.strike > 0) || !(v.days > 0)) return say('Spot, strike, and days must be above zero.');
    const cap = v.strike / v.spot - 1, ann = v.premium * 365 / v.days, be = v.spot * (1 - v.premium / 100);
    const payAt = price => (Math.min(price, v.strike) - v.spot) / v.spot * 100 + v.premium;
    const x0 = Math.max(0.01, Math.min(be, v.spot) * 0.82);
    const x1 = Math.max(v.strike, v.spot) * 1.18;
    const ySpan = fit([payAt(x0), payAt(v.strike), 0, v.premium]);
    const graph = curve({
      x0: x0, x1: x1, y0: ySpan[0], y1: ySpan[1], xunit: '$', yunit: '%',
      vbands: [{ from: v.strike, to: x1, fill: '#eef3f7' }],
      vlines: [
        { x: be, label: 'Break-even ' + money(be), color: '#9a3412' },
        { x: v.strike, label: 'Strike ' + money(v.strike), color: '#0a5c48' }
      ],
      series: [{ pts: samples(x0, x1, 80, false).map(price => [price, payAt(price)]), color: '#07111c', width: 2.5, split: true }],
      dots: [{ x: v.spot, y: payAt(v.spot), label: 'Spot ' + (v.premium >= 0 ? '+' : '') + v.premium.toFixed(2) + '%' }],
      legend: [{ color: '#07111c', name: 'Gain this period if price expires here' }, { color: '#9aafc0', name: 'Upside stays capped past the strike' }]
    });
    return panel(pctPts(ann, 1) + ' a year if it repeats', [
      ['Premium this period', v.premium + '%'],
      ['Max gain this period', pctPts(v.premium + cap * 100)],
      ['Upside capped at', money(v.strike)],
      ['Break-even price', money(be)]
    ], 'A ' + v.premium + '% premium every ' + v.days + ' days is ' + pctPts(ann, 1) + ' a year if it repeats. The most you can make this period is ' + pctPts(v.premium + cap * 100) + ', and the break-even is ' + money(be) + '. Below that you lose like a holder, minus the premium.', null, graph);
  },
  bank: v => {
    if (!(v.coll > 0)) return say('Collateral must be above zero.');
    if (!(v.lt > 0 && v.lt < 1)) return say('Liquidation threshold must be between 0 and 1.');
    if (v.debt < 0 || v.reserve < 0 || v.spend < 0) return say('Debt, reserve, and spend cannot be negative.');
    const ltv = v.debt / v.coll, hf = v.debt ? v.coll * v.lt / v.debt : Infinity;
    const interest = v.debt * v.bapy / 100 / 12, obligations = v.spend + interest;
    const months = obligations ? v.reserve / obligations : Infinity;
    const equity = v.coll + v.reserve + v.other - v.debt;
    const pass = ok => ok ? 'Pass' : '<span class="warn">Fail</span>';
    const checks = [ltv * 100 <= v.maxltv, hf >= 2, months >= 6];
    const allPass = checks.every(Boolean);
    const ltvPct = ltv * 100;
    const ltvScale = Math.max(v.maxltv, v.lt * 100, ltvPct, 1) * 1.12;
    const hfScale = hf === Infinity ? 4 : Math.max(4, hf) * 1.08;
    const monthScale = months === Infinity ? 12 : Math.max(12, months) * 1.08;
    const graph = meters({
      rows: [
        {
          name: 'Loan to value',
          value: pct(ltv, 1),
          at: ltvPct / ltvScale,
          zones: [
            { from: 0, to: v.maxltv / ltvScale, fill: '#e7f6f1' },
            { from: v.maxltv / ltvScale, to: Math.min(1, v.lt * 100 / ltvScale), fill: '#f8f1e6' },
            { from: Math.min(1, v.lt * 100 / ltvScale), to: 1, fill: '#f8efea' }
          ],
          ticks: [
            { at: v.maxltv / ltvScale, label: 'Policy ' + v.maxltv + '%' },
            { at: v.lt * 100 / ltvScale, label: 'Liquidates ' + Math.round(v.lt * 100) + '%', color: '#9a3412' }
          ]
        },
        {
          name: 'Health factor',
          value: hf === Infinity ? 'No debt' : hf.toFixed(2),
          at: hf === Infinity ? 1 : hf / hfScale,
          zones: [
            { from: 0, to: 1 / hfScale, fill: '#f8efea' },
            { from: 1 / hfScale, to: 2 / hfScale, fill: '#f8f1e6' },
            { from: 2 / hfScale, to: 1, fill: '#e7f6f1' }
          ],
          ticks: [
            { at: 1 / hfScale, label: '1', color: '#9a3412' },
            { at: 2 / hfScale, label: 'Buffer 2', color: '#0a5c48' }
          ]
        },
        {
          name: 'Reserve runway',
          value: months === Infinity ? 'No bills' : months.toFixed(1) + ' months',
          at: months === Infinity ? 1 : months / monthScale,
          zones: [
            { from: 0, to: Math.min(1, 6 / monthScale), fill: '#f8efea' },
            { from: Math.min(1, 6 / monthScale), to: 1, fill: '#e7f6f1' }
          ],
          ticks: [{ at: Math.min(1, 6 / monthScale), label: '6 months', color: '#0a5c48' }]
        }
      ]
    });
    return panel('Equity ' + money(equity), [
      ['Collateral', money(v.coll)],
      ['Reserve', money(v.reserve)],
      ['Other assets', money(v.other)],
      ['Debt', money(v.debt)],
      ['Interest per month', money(interest)],
      ['LTV', pct(ltv, 1)],
      ['Health factor', hf === Infinity ? 'No debt' : hf.toFixed(2)],
      ['Reserve runway', months === Infinity ? 'No monthly obligations' : months.toFixed(1) + ' months'],
      ['LTV at or under ' + v.maxltv + '%', pass(checks[0])],
      ['Health factor at least 2', pass(checks[1])],
      ['Reserve covers 6 months', pass(checks[2])]
    ], 'Equity is ' + money(equity) + '. The loan is ' + pct(ltv, 0) + ' of collateral, health factor is ' + (hf === Infinity ? 'unlimited with no debt' : hf.toFixed(2)) + ', and the reserve covers ' + (months === Infinity ? 'the bills with nothing due' : months.toFixed(1) + ' months') + '.', { tone: allPass ? 'ok' : 'warn', label: allPass ? 'Three checks pass' : 'A check fails' }, graph);
  },
  perp: v => {
    if (!(v.entry > 0) || !(v.lev > 0)) return say('Entry price and leverage must be above zero.');
    if (!(v.mmr >= 0)) return say('Maintenance margin must be zero or more.');
    const move = 1 / v.lev - v.mmr / 100;
    if (!(move > 0)) return say('Maintenance margin uses the whole leverage buffer, so this approximation has no room before liquidation.');
    const liq = v.side === 'short' ? v.entry * (1 + move) : v.entry * (1 - move);
    const dist = (liq / v.entry - 1) * 100;
    const capLev = v.mmr > 0 ? 100 / v.mmr * 0.9 : 25;
    const x0 = Math.min(1.5, v.lev);
    const x1 = Math.min(capLev, Math.max(12, v.lev * 1.45));
    const liqAt = (lev, side) => {
      const m = 1 / lev - v.mmr / 100;
      if (!(m > 0)) return null;
      return side === 'short' ? v.entry * (1 + m) : v.entry * (1 - m);
    };
    const longPts = samples(x0, x1, 48, false).map(lev => [lev, liqAt(lev, 'long')]).filter(p => p[1] != null);
    const shortPts = samples(x0, x1, 48, false).map(lev => [lev, liqAt(lev, 'short')]).filter(p => p[1] != null);
    const ySpan = fit(longPts.map(p => p[1]).concat(shortPts.map(p => p[1]), [v.entry]));
    const graph = curve({
      x0: x0, x1: x1 > x0 ? x1 : x0 + 1, y0: ySpan[0], y1: ySpan[1], xunit: '×', yunit: '$', zero: false,
      hlines: [{ y: v.entry, label: 'Entry ' + money(v.entry), color: '#0a5c48' }],
      series: [
        { pts: longPts, color: v.side === 'long' ? '#9a3412' : '#9aafc0', width: v.side === 'long' ? 2.5 : 1.5, dash: v.side === 'long' ? '' : '4 4' },
        { pts: shortPts, color: v.side === 'short' ? '#9a3412' : '#9aafc0', width: v.side === 'short' ? 2.5 : 1.5, dash: v.side === 'short' ? '' : '4 4' }
      ],
      dots: [{ x: v.lev, y: liq, label: 'Now ' + money(liq) }],
      legend: [{ color: '#9a3412', name: v.side + ' liquidation' }, { color: '#9aafc0', name: 'The other side' }]
    });
    return panel(money(liq) + ' liquidation', [
      ['Side', v.side + ' ' + v.lev + '×'],
      ['Entry', money(v.entry)],
      ['Move to liquidation', signed(dist)],
      ['Maintenance margin', v.mmr + '%'],
      ['Margin per $1,000', money(1000 / v.lev)]
    ], 'A ' + v.lev + '× ' + v.side + ' from ' + money(v.entry) + ' liquidates near ' + money(liq) + ', about ' + pretty(dist) + '% ' + (dist < 0 ? 'under' : 'above') + ' the entry, before fees and funding.', null, graph);
  },
  twr: v => {
    const periods = [v.p1, v.p2, v.p3];
    let growth = 1;
    periods.forEach(r => { growth *= 1 + r / 100; });
    const tw = (growth - 1) * 100;
    const bits = [
      ['Period 1', v.p1 + '%'],
      ['Period 2', v.p2 + '%'],
      ['Period 3', v.p3 + '%']
    ];
    let spoken = 'The three periods compound to ' + pctPts(tw) + '.';
    if (v.start > 0 && v.end != null && v.deposits != null && !Number.isNaN(v.end) && !Number.isNaN(v.deposits)) {
      const simple = (v.end - v.start - v.deposits) / (v.start + v.deposits) * 100;
      bits.push(['Simple gain on capital in', pctPts(simple)]);
      spoken += ' A simple gain on the money put in is ' + pctPts(simple) + ', because deposits change that figure. Time-weighted return follows the periods.';
    }
    const c1 = v.p1;
    const c2 = ((1 + v.p1 / 100) * (1 + v.p2 / 100) - 1) * 100;
    const graph = columns({
      yunit: '%',
      bars: [
        { name: 'Period 1', value: v.p1 },
        { name: 'Period 2', value: v.p2 },
        { name: 'Period 3', value: v.p3 }
      ],
      line: [c1, c2, tw],
      lineLabel: 'Compounded ' + pctPts(tw),
      rule: (v.start > 0 && v.end != null && v.deposits != null && !Number.isNaN(v.end) && !Number.isNaN(v.deposits))
        ? { value: (v.end - v.start - v.deposits) / (v.start + v.deposits) * 100, label: 'Simple gain' }
        : null,
      legend: [{ color: '#12a888', name: 'Each period' }, { color: '#07111c', name: 'Compounded so far' }]
    });
    return panel(pctPts(tw) + ' time-weighted', bits, spoken, null, graph);
  },
  cdp: v => {
    if (!(v.qty > 0 && v.price > 0 && v.mint > 0 && v.minr > 0)) return say('Quantity, price, mint amount, and minimum ratio must be above zero.');
    const coll = v.qty * v.price, maxMint = coll / (v.minr / 100), ratio = coll / v.mint * 100;
    const liq = v.mint * v.minr / 100 / v.qty;
    const under = ratio < v.minr;
    const move = (liq / v.price - 1) * 100;
    const ratioAt = p => v.qty * p / v.mint * 100;
    const x0 = Math.max(0, liq * 0.72);
    const x1 = Math.max(v.price, liq) * 1.35;
    const yTop = Math.max(v.minr * 1.35, ratioAt(v.price) * 1.2, ratio);
    const graph = curve({
      x0: x0, x1: x1, y0: 0, y1: yTop, xunit: '$', yunit: '%', zero: false,
      bands: [
        { from: 0, to: Math.min(v.minr, yTop), fill: '#f8efea' },
        { from: v.minr, to: yTop, fill: '#e7f6f1' }
      ],
      hlines: [{ y: v.minr, label: 'Minimum ' + v.minr.toFixed(0) + '%', color: '#9a3412' }],
      vlines: [{ x: liq, label: 'Liquidation ' + money(liq), color: '#9a3412' }],
      series: [{ pts: samples(Math.max(x0, 0.01), x1, 64, false).map(p => [p, ratioAt(p)]), color: '#07111c', width: 2.5 }],
      dots: [{ x: v.price, y: ratio, label: 'Now ' + ratio.toFixed(0) + '%' }],
      legend: [{ color: '#07111c', name: 'Collateral ratio as price moves' }]
    });
    return panel(ratio.toFixed(0) + '% collateral ratio', [
      ['Collateral', money(coll)],
      ['Minting', money(v.mint)],
      ['Maximum mint', money(maxMint)],
      ['Liquidation price', money(liq)],
      ['Distance', signed(move)],
      ['Stability fee', money(v.mint * v.fee / 100) + ' per year']
    ], v.qty + ' tokens at ' + money(v.price) + ' back ' + money(v.mint) + ' of stablecoins at a ' + ratio.toFixed(0) + '% ratio. The position liquidates near ' + money(liq) + '.', { tone: under ? 'warn' : 'ok', label: under ? 'Under the minimum ratio' : 'Above the minimum' }, graph);
  }
};
document.querySelectorAll('.calc[data-c]').forEach(el => {
  const run = RUN[el.dataset.c];
  const out = el.querySelector('.out');
  if (!run || !out) return;
  const upd = () => {
    const v = {};
    let missing = false;
    el.querySelectorAll('[data-k]').forEach(i => {
      if (i.tagName === 'SELECT') { v[i.dataset.k] = i.value; return; }
      if (i.dataset.opt === '1' && i.value.trim() === '') { v[i.dataset.k] = null; return; }
      const n = parseFloat(i.value);
      if (Number.isNaN(n)) missing = true;
      v[i.dataset.k] = n;
    });
    out.innerHTML = missing ? say('Enter every value.') : run(v);
  };
  el.querySelectorAll('input, select').forEach(i => i.addEventListener('input', upd));
  el.querySelectorAll('select').forEach(i => i.addEventListener('change', upd));
  const reset = el.querySelector('.resetex');
  if (reset) reset.addEventListener('click', () => {
    el.querySelectorAll('[data-k]').forEach(i => { i.value = i.dataset.def || ''; });
    upd();
  });
  upd();
});
if (location.protocol === 'file:' && /On-Chain-Operator-Course-Directory\\.html$/i.test(decodeURIComponent(location.pathname))) {
  const note = document.createElement('p');
  note.id = 'offline-note';
  note.className = 'safety';
  note.textContent = 'This downloaded file is the whole directory. Search, lessons, pictures, worksheets, and the calculators all run here. Video files and the Course Hub are the files next to directory.html in the course folder, so those links stay on this page.';
  document.getElementById('intro').prepend(note);
  document.querySelectorAll('a.folderlink').forEach(a => a.addEventListener('click', e => { e.preventDefault(); note.scrollIntoView({ block: 'nearest' }); }));
}
`;

function parseGlossary(body) {
  const m = String(body || '').match(/### Glossary[^\n]*\n+(\|[\s\S]*?)(?=\n### |\n## |$)/);
  if (!m) return [];
  return m[1].split('\n').map(line => {
    if (!line.trim().startsWith('|')) return null;
    const cells = line.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(c => c.trim());
    if (!cells.length || cells.every(c => /^:?-+:?$/.test(c))) return null;
    return cells;
  }).filter(Boolean).slice(1).map(([word, meaning]) => ({ word, meaning: meaning || '' }));
}
function lessonForTerm(word) {
  const key = word.split('(')[0].split('/')[0].trim().toLowerCase();
  if (key.length < 3) return null;
  return allLessons.find(l => l.id !== '0.8' && ((l.title || '').toLowerCase().includes(key) || (l.blurb || '').toLowerCase().includes(key)))
    || allLessons.find(l => l.id !== '0.8' && (l.hay || '').toLowerCase().includes(key))
    || null;
}
const glossSource = (allLessons.find(l => l.id === '0.8') || {}).body || '';
const glossaryHtml = parseGlossary(glossSource).map(g => {
  const other = lessonForTerm(g.word);
  const links = [lessonLink('0.8', 'Defined in 0.8'), other ? lessonLink(other.id, 'Used in ' + other.id) : ''].filter(Boolean).join(' · ');
  const find = plain(g.word + ' ' + g.meaning + ' glossary').toLowerCase();
  return `<article class="gloss" data-find="${esc(find)}"><h3>${esc(g.word)}</h3><p>${esc(g.meaning)}</p><p class="links">${links}</p></article>`;
}).join('\n');

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
      <input id="q" type="search" placeholder="Search lessons, pictures, worksheets, calculators" autocomplete="off" enterkeyhint="search">
    </form>
  </header>
  <nav class="jumps" aria-label="Directory sections">
    <a href="#start">Start</a>
    <a href="#lessons">Lessons</a>
    <a href="#glossary">Glossary</a>
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
      <li>Open the lesson and read it. Its calculator sits underneath when the lesson has one.</li>
      <li>Mark a lesson done when you finish it. That check stays in this browser.</li>
      <li>Fill in the worksheet on this page, or print it. Leave every secret out of it.</li>
    </ol>
    <div class="safety">
      <p>Educational content only. Not financial, tax or legal advice. Digital assets are volatile and you can lose some or all of your capital. No results or income are promised. Never enter a seed phrase, private key, API key or password into this directory, the Course Hub, or any worksheet. This program will not ask for them.</p>
    </div>
    <h2>Films to start with</h2>
    <ul class="vids">${orientation}</ul>
    <p class="links">The <a href="index.html">Course Hub</a>, in the same folder, has the video, the checklist and the quiz. Progress stays in that browser.</p>
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
      <div id="hits" hidden></div>
      ${stagesHtml}
    </section>

    <section id="glossary">
      <h2>Glossary</h2>
      <p class="lede">The words from lesson 0.8. Each one links back to that lesson, and to another lesson that uses it.</p>
      ${glossaryHtml}
    </section>

    <section id="worksheets">
      <h2>Worksheets</h2>
      <p class="lede">${esc(wsIntro)}</p>
      <p class="quiet">What you type stays in this browser. Print uses the sheet as you filled it in.</p>
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
      <p class="lede">Twenty forms run in this file, grouped by the stage that teaches them. Change a number and the answer updates, and the graph under it redraws. The numbers follow the course formulas. They are for learning, not a forecast, and no income is promised.</p>
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
