// Render the master markdown file to a print-styled PDF with Chromium.
// Usage: node build_pdf.js <master.md> <out.pdf>
const fs = require('fs');
const path = require('path');
const { marked } = require('marked');
const { chromium } = require('playwright-core');

const [src, out] = process.argv.slice(2);
let md = fs.readFileSync(src, 'utf8');
md = md.replace(/<details>\s*<summary>([\s\S]*?)<\/summary>\s*([\s\S]*?)<\/details>/g,
  (_, q, a) => `<div class="qa"><p class="q">Q: ${marked.parseInline(q.trim())}</p><p class="a"><em>Answer:</em> ${marked.parseInline(a.trim())}</p></div>\n`);
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
  return `<img class="figure" alt="${text}" src="data:image/png;base64,${fs.readFileSync(file).toString('base64')}">`;
};
let body = marked.parse(md, { renderer, gfm: true });
body = body.replace(/<li><input checked="" disabled="" type="checkbox">/g, '<li class="task">☑')
  .replace(/<li><input disabled="" type="checkbox">/g, '<li class="task">☐');

const date = new Date().toISOString().slice(0, 10);
const html = `<!doctype html><html><head><meta charset="utf-8"><style>
  @page { size: A4; margin: 20mm 18mm 22mm; }
  body { font-family: Calibri, Carlito, "Liberation Sans", Arial, sans-serif; font-size: 10.5pt; line-height: 1.45; color: #222; }
  h1 { color: #1F4E79; font-size: 20pt; border-bottom: 2px solid #1F4E79; padding-bottom: 4px; break-before: page; margin-top: 0; }
  .cover + h1 { break-before: page; }
  h2 { color: #1F4E79; font-size: 14pt; margin-top: 22px; break-after: avoid; }
  h3 { font-size: 12pt; margin-top: 16px; break-after: avoid; }
  table { border-collapse: collapse; width: 100%; margin: 8px 0 12px; font-size: 9.5pt; break-inside: auto; }
  th { background: #1F4E79; color: #fff; text-align: left; }
  th, td { border: 1px solid #BFC9D4; padding: 4px 6px; vertical-align: top; }
  tr:nth-child(even) td { background: #F3F6F9; }
  tr { break-inside: avoid; }
  code { font-family: Consolas, "Liberation Mono", monospace; background: #EEF2F6; padding: 0 3px; font-size: 9pt; }
  pre { background: #EEF2F6; padding: 8px 10px; white-space: pre-wrap; font-size: 8.5pt; break-inside: avoid; }
  pre code { background: none; padding: 0; }
  blockquote { border-left: 4px solid #1F4E79; background: #F3F6F9; margin: 10px 0; padding: 6px 12px; }
  blockquote p { margin: 4px 0; }
  ul, ol { padding-left: 22px; } li { margin: 2px 0; }
  li.task { list-style: none; margin-left: -16px; }
  .qa { break-inside: avoid; margin: 6px 0 10px; } .qa p { margin: 2px 0; } .q { font-weight: bold; }
  img.figure { display: block; width: 100%; margin: 10px 0 14px; border-radius: 6px; break-inside: avoid; }
  .fig { text-align: center; } .fig img { width: 240px; }
  hr { display: none; }
  a { color: #0563C1; text-decoration: none; }
  .cover { height: 245mm; display: flex; flex-direction: column; justify-content: center; text-align: center; }
  .cover .t { font-size: 30pt; font-weight: bold; color: #1F4E79; }
  .cover .s { font-size: 14pt; color: #404040; margin: 12px 0 40px; }
  .cover .d { color: #707070; }
</style></head><body>
<div class="cover"><img src="data:image/png;base64,${fs.readFileSync(path.resolve(__dirname, '../assets/store/banner-1920x1080.png')).toString('base64')}" style="width:100%;border-radius:10px;margin-bottom:48px">
<div class="t">On-Chain Operator Program</div>
<div class="s">Master File — Offer, Curriculum, Setup, Funnel &amp; Course Content</div>
<div class="d">Draft · ${date}</div>
<div class="d"><em>Educational content only. Not financial advice. No results are guaranteed.</em></div></div>
${body}</body></html>`;

(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'load' });
  await page.pdf({
    path: out, format: 'A4', printBackground: true, displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-size:8px;color:#808080;width:100%;text-align:center">On-Chain Operator Program · <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    margin: { top: '20mm', bottom: '22mm', left: '18mm', right: '18mm' },
  });
  await browser.close();
  console.log('wrote', out);
})();
