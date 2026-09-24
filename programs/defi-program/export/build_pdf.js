// Render a program markdown file to a designed, print-ready PDF with Chromium.
// Lessons get header bands; Objective / Worked example / Checklist / Quiz and
// every Mastery Starter section become styled callouts; full-bleed brand cover.
// Usage: node build_pdf.js <file.md> <out.pdf>   (PDF_SUBTITLE="…" for the cover)
const fs = require('fs');
const path = require('path');
const { marked } = require('marked');
const { chromium } = require('playwright-core');
const { C, FONT, logoMark, network } = require('./build_images.js');

const [src, out] = process.argv.slice(2);
let md = fs.readFileSync(src, 'utf8');
md = md.replace(/<details>\s*<summary>([\s\S]*?)<\/summary>\s*([\s\S]*?)<\/details>/g,
  (_, q, a) => `<div class="qa"><p class="q">${marked.parseInline(q.trim())}</p><p class="a"><b>Answer</b> ${marked.parseInline(a.trim())}</p></div>\n`);
md = md.replace(/\*Generated [^\n]*\n/, '');

let n = 0;
const renderer = new marked.Renderer();
const baseCode = renderer.code.bind(renderer);
renderer.code = (tok) => {
  if (tok.lang === 'mermaid') {
    const f = path.join(__dirname, `mermaid-${n++}.png`);
    if (fs.existsSync(f)) return `<p class="fig"><img src="data:image/png;base64,${fs.readFileSync(f).toString('base64')}"></p>`;
  }
  return baseCode(tok);
};
renderer.image = ({ href, text }) => {
  const file = path.resolve(path.dirname(src), href);
  const banner = /assets\/modules\//.test(href);
  return `<figure class="${banner ? 'banner' : 'figure'}"><img alt="${text}" src="data:image/png;base64,${fs.readFileSync(file).toString('base64')}">${banner || !text ? '' : `<figcaption>${text}</figcaption>`}</figure>`;
};
let body = marked.parse(md, { renderer, gfm: true });
body = body.replace(/<li><input checked="" disabled="" type="checkbox">/g, '<li class="task done">')
  .replace(/<li><input disabled="" type="checkbox">/g, '<li class="task">')
  .replace(/<p>(<figure[\s\S]*?<\/figure>)<\/p>/g, '$1');

// ---- structure: lesson bands + callouts -------------------------------------
const KINDS = [
  [/^objective/i, 'obj', 'Objective'], [/^explanation/i, 'plain', 'Explanation'], [/^worked example/i, 'ex', 'Worked example'],
  [/^checklist/i, 'check', 'Checklist'], [/^quiz/i, 'quiz', 'Quiz'], [/^the 60-second/i, 'sixty', 'The 60-second version'],
  [/^words you/i, 'words', 'Words you’ll need'], [/^before you start/i, 'safe', 'Before you start'], [/^your first safe step/i, 'step', 'Your first safe step'],
  [/^the mastery ladder/i, 'ladder', 'The mastery ladder'], [/^you.ve mastered/i, 'mastered', 'You’ve mastered this module when…'],
  [/^(how it loses|kill rules|risks?\b|what can go wrong)/i, 'risk', null], [/^(common mistakes|mistakes)/i, 'risk', null],
];
const strip = h => h.replace(/<[^>]+>/g, '').replace(/&#39;/g, "'").replace(/&quot;/g, '"').replace(/&amp;/g, '&').trim();
const parts = body.split(/(?=<h[1-3][\s>])/);
body = parts.map(ch => {
  const h3 = ch.match(/^<h3[^>]*>([\s\S]*?)<\/h3>/);
  if (h3) {
    const text = strip(h3[1]);
    const k = KINDS.find(([re]) => re.test(text));
    if (!k || k[1] === 'plain') return ch;
    return `<section class="box ${k[1]}"><div class="tag">${k[2] || text}</div>${ch.slice(h3[0].length)}</section>`;
  }
  const h2 = ch.match(/^<h2[^>]*>([\s\S]*?)<\/h2>/);
  if (h2) {
    const m = strip(h2[1]).match(/^(?:Sample )?Lesson (\d+\.\d+)\s*[—:-]\s*(.+?)(?:\s*\((ch\.[^)]*|[^)]*)\))?$/);
    if (m) {
      const starter = /mastery starter/i.test(m[2]);
      return `<div class="band${starter ? ' starter' : ''}"><div class="n">${m[1]}</div><div class="t"><div class="k">${starter ? 'Mastery Starter · start here' : 'Lesson'}</div>${starter ? 'Mastery Starter' : m[2]}</div></div>${ch.slice(h2[0].length)}`;
    }
  }
  const h1 = ch.match(/^<h1[^>]*>([\s\S]*?)<\/h1>/);
  if (h1) {
    const m = strip(h1[1]).match(/^Module (\d+) — (.+)$/);
    if (m && /<figure class="banner">/.test(ch)) return `<h1 class="modh">Module ${m[1]} — ${m[2]}</h1>${ch.slice(h1[0].length)}`;  // the banner is the heading
    if (m) return `<div class="modhead"><div class="k">Module ${m[1]}</div><h1>${m[2]}</h1></div>${ch.slice(h1[0].length)}`;
  }
  return ch;
}).join('');

const b64 = f => fs.readFileSync(path.resolve(__dirname, f)).toString('base64');
const date = new Date().toISOString().slice(0, 10);
const subtitle = process.env.PDF_SUBTITLE || 'From zero to your own on-chain bank';
const html = `<!doctype html><html><head><meta charset="utf-8">
${[400, 500, 600, 700, 800].map(x => `<link rel="stylesheet" href="${FONT('inter', x)}">`).join('')}
<link rel="stylesheet" href="${FONT('jetbrains-mono', 500)}">
<style>
  @page { size: A4; margin: 18mm 17mm 20mm; }
  :root { --ink:${C.ink}; --navy:${C.navy}; --brand:${C.brand}; --blue:${C.blue}; --orange:${C.orange}; --teal:#14a874; --line:${C.line}; --panel:${C.panel}; }
  body { font-family: Inter, sans-serif; font-size: 10pt; line-height: 1.55; color: #1d232b; -webkit-print-color-adjust: exact; }
  p { margin: 5px 0 8px; }
  strong { color: var(--ink); font-weight: 700; }
  h1 { color: var(--ink); font-size: 22pt; font-weight: 800; letter-spacing: -.02em; line-height: 1.15; break-before: page; margin: 0 0 10px; padding-bottom: 8px; border-bottom: 3px solid var(--brand); }
  .modhead { break-before: page; background: linear-gradient(120deg, var(--ink), var(--navy) 60%, #1d4a78); color: #fff; border-radius: 14px; padding: 18px 22px 16px; margin-bottom: 12px; }
  h1.modh { position: absolute; left: -9999px; font-size: 1px; border: 0; margin: 0; padding: 0; }
  h1.modh + figure.banner { break-before: page; margin-top: 0; }
  .modhead h1 { break-before: auto; color: #fff; border: 0; margin: 2px 0 0; padding: 0; font-size: 24pt; }
  .modhead .k, .band .k { font-size: 8pt; font-weight: 700; letter-spacing: .18em; text-transform: uppercase; color: #2ee6a6; }
  h2 { color: var(--brand); font-size: 14.5pt; font-weight: 800; letter-spacing: -.01em; margin: 20px 0 6px; break-after: avoid; }
  h3 { font-size: 11.5pt; font-weight: 700; color: var(--ink); margin: 14px 0 4px; break-after: avoid; }
  h4 { font-size: 10.5pt; margin: 10px 0 2px; break-after: avoid; }
  .band { display: flex; align-items: stretch; gap: 0; margin: 22px 0 10px; border-radius: 12px; overflow: hidden; break-after: avoid; break-inside: avoid; box-shadow: 0 1px 0 var(--line); }
  .band .n { background: var(--brand); color: #fff; font-weight: 800; font-size: 20pt; letter-spacing: -.03em; padding: 10px 16px; display: flex; align-items: center; min-width: 22mm; justify-content: center; }
  .band .t { background: var(--panel); flex: 1; padding: 9px 16px; font-size: 14pt; font-weight: 800; color: var(--ink); line-height: 1.2; letter-spacing: -.01em; }
  .band .t .k { color: var(--blue); margin-bottom: 3px; }
  .band.starter .n { background: linear-gradient(135deg, #14a874, var(--blue)); }
  .band.starter .t { background: #eaf7f1; }
  .box { position: relative; border-radius: 10px; padding: 20px 14px 8px; margin: 16px 0 12px; break-inside: avoid; background: var(--panel); border: 1px solid var(--line); }
  .box .tag { position: absolute; top: -9px; left: 12px; font-size: 7.5pt; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; padding: 3px 9px; border-radius: 999px; color: #fff; background: var(--brand); }
  .box.obj { background: #eef4fb; border-color: #cfe0f3; border-left: 5px solid var(--blue); font-weight: 600; font-size: 10.5pt; color: var(--ink); }
  .box.obj .tag { background: var(--blue); }
  .box.ex { background: #fbfaf6; border-color: #e7e2d3; border-left: 5px solid var(--ink); }
  .box.ex .tag { background: var(--ink); }
  .box.check { background: #eefaf4; border-color: #c4ebd8; border-left: 5px solid var(--teal); }
  .box.check .tag { background: var(--teal); }
  .box.quiz { background: #fff5ef; border-color: #f6d6c5; border-left: 5px solid var(--orange); break-inside: auto; }
  .box.quiz .tag { background: var(--orange); }
  .box.sixty { background: linear-gradient(120deg, var(--ink), var(--navy)); color: #fff; border: 0; font-size: 11pt; }
  .box.sixty .tag { background: #2ee6a6; color: var(--ink); } .box.sixty strong { color: #2ee6a6; }
  .box.words .tag { background: var(--blue); }
  .box.safe, .box.step { background: #eefaf4; border-color: #c4ebd8; } .box.safe .tag, .box.step .tag { background: var(--teal); }
  .box.ladder { background: #fff; } .box.mastered { background: #eef4fb; border-left: 5px solid var(--brand); font-weight: 600; }
  .box.risk { background: #fff5ef; border-color: #f6d6c5; border-left: 5px solid var(--orange); } .box.risk .tag { background: var(--orange); }
  .box > :last-child { margin-bottom: 6px; }
  table { border-collapse: separate; border-spacing: 0; width: 100%; margin: 8px 0 12px; font-size: 9pt; break-inside: auto; border: 1px solid var(--line); border-radius: 8px; overflow: hidden; background: #fff; }
  th { background: var(--ink); color: #fff; text-align: left; font-weight: 700; font-size: 8.5pt; letter-spacing: .02em; }
  th, td { border-bottom: 1px solid var(--line); padding: 5px 8px; vertical-align: top; }
  tr:last-child td { border-bottom: 0; }
  tr:nth-child(even) td { background: #f7f9fb; }
  tr { break-inside: avoid; }
  code { font-family: 'JetBrains Mono', monospace; background: #e9eef4; padding: 0 4px; border-radius: 4px; font-size: 8.3pt; color: var(--ink); }
  pre { background: var(--ink); color: #d7e3f0; padding: 10px 12px; border-radius: 8px; white-space: pre-wrap; font-size: 8pt; break-inside: avoid; }
  pre code { background: none; padding: 0; color: inherit; }
  blockquote { border-left: 4px solid var(--brand); background: var(--panel); margin: 10px 0; padding: 6px 14px; border-radius: 0 8px 8px 0; color: #34404d; }
  blockquote p { margin: 4px 0; }
  ul, ol { padding-left: 20px; } li { margin: 3px 0; } li::marker { color: var(--blue); }
  li.task { list-style: none; margin-left: -20px; padding-left: 24px; position: relative; }
  li.task::before { content: ''; position: absolute; left: 2px; top: 3px; width: 11px; height: 11px; border: 1.6px solid var(--teal); border-radius: 3px; background: #fff; }
  li.task.done::before { background: var(--teal); }
  .qa { break-inside: avoid; margin: 8px 0 10px; padding-bottom: 8px; border-bottom: 1px dashed #efc9b4; } .qa:last-child { border-bottom: 0; }
  .qa p { margin: 2px 0; } .qa .q { font-weight: 700; color: var(--ink); } .qa .a b { color: var(--orange); font-size: 8pt; letter-spacing: .1em; text-transform: uppercase; margin-right: 4px; }
  figure { margin: 12px 0 14px; break-inside: avoid; }
  figure.figure img { display: block; width: 100%; border-radius: 8px; border: 1px solid var(--line); }
  figure.banner img { display: block; width: 100%; border-radius: 12px; }
  figcaption { font-size: 8.5pt; color: #6b7480; margin-top: 5px; text-align: center; font-style: italic; }
  .fig { text-align: center; } .fig img { width: 240px; }
  hr { border: 0; height: 0; margin: 14px 0; }
  a { color: var(--blue); text-decoration: none; }
  em { color: #4a5563; }
  .cover { position: relative; width: 210mm; height: 296.5mm; overflow: hidden; color: #fff; background: radial-gradient(120% 90% at 85% 0%, #1d4a78 0%, ${C.navy} 38%, ${C.ink} 100%); break-after: page; }
  .cover .bg { position: absolute; inset: 0; width: 100%; height: 100%; }
  .cover .inner { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 0 22mm; }
  .cover .t1 { font-weight: 800; font-size: 34pt; letter-spacing: .1em; margin-top: 10mm; }
  .cover .t2 { font-weight: 800; font-size: 20pt; letter-spacing: .38em; margin-top: 2mm; color: #2ee6a6; }
  .cover .t3 { font-weight: 600; font-size: 9pt; letter-spacing: .6em; margin-top: 4mm; color: rgba(255,255,255,.6); }
  .cover .sub { margin-top: 16mm; font-size: 15pt; font-weight: 600; color: #fff; }
  .cover .rule { width: 26mm; height: 2.5px; border-radius: 2px; background: linear-gradient(90deg,#2ee6a6,#3987e5); margin: 8mm auto; }
  .cover .meta { font-size: 9pt; color: rgba(255,255,255,.65); line-height: 1.8; }
  .cover .disc { position: absolute; left: 0; right: 0; bottom: 14mm; font-size: 8pt; color: rgba(255,255,255,.5); text-align: center; }
</style></head><body>
COVER_SPLIT<div class="cover">${network(794, 1123, 11, 34, 0.2)}
  <div class="inner">${logoMark(300)}
    <div class="t1">ON-CHAIN</div><div class="t2">OPERATOR</div><div class="t3">PROGRAM</div>
    <div class="sub">${subtitle}</div><div class="rule"></div>
    <div class="meta">Edition ${date}</div></div>
  <div class="disc">Educational content only · Not financial advice · No results are guaranteed</div></div><!--/cover-->
${body}</body></html>`;

(async () => {
  const work = path.join(__dirname, '.render');
  fs.mkdirSync(work, { recursive: true });
  const [headHtml, rest] = html.split('COVER_SPLIT');
  const cut = rest.indexOf('<!--/cover-->');
  const coverHtml = headHtml + rest.slice(0, cut) + '</body></html>';
  const bodyHtml = headHtml + rest.slice(cut);
  const coverFile = path.join(work, `pdf-${path.basename(out, '.pdf')}-cover.html`);
  const file = path.join(work, `pdf-${path.basename(out, '.pdf')}.html`);
  fs.writeFileSync(coverFile, coverHtml.replace('@page { size: A4; margin: 18mm 17mm 20mm; }', '@page { size: A4; margin: 0; }'));
  fs.writeFileSync(file, bodyHtml);
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await browser.newPage();
  await page.goto(`file://${coverFile}`, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const coverPdf = path.join(work, 'cover.pdf'), bodyPdf = path.join(work, 'body.pdf');
  await page.pdf({ path: coverPdf, format: 'A4', printBackground: true, preferCSSPageSize: true });
  await page.goto(`file://${file}`, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({
    path: bodyPdf, format: 'A4', printBackground: true, displayHeaderFooter: true, preferCSSPageSize: true,
    headerTemplate: '<span></span>',
    footerTemplate: `<div style="font-family:Inter,Arial,sans-serif;font-size:7.5px;color:#8a8f98;width:100%;padding:0 17mm;display:flex;justify-content:space-between"><span>On-Chain Operator Program${process.env.PDF_SUBTITLE ? ' · ' + process.env.PDF_SUBTITLE : ''}</span><span>Educational content only · Not financial advice</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`,
  });
  await browser.close();
  // Full-bleed cover (no footer) + numbered body, merged with PyMuPDF.
  require('child_process').execFileSync('python3', ['-c', 'import sys,pymupdf;a=pymupdf.open(sys.argv[1]);a.insert_pdf(pymupdf.open(sys.argv[2]));a.save(sys.argv[3],garbage=3,deflate=True)', coverPdf, bodyPdf, out]);
  console.log('wrote', out);
})();
