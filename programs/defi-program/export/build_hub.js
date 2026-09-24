// Build the interactive Course Hub: one self-contained HTML file with every
// lesson, sidebar navigation by stage and module, search, progress tracking,
// persistent checklists, self-marked quizzes, in-browser calculators, and the
// lesson videos (with captions and chapters) wherever they've been rendered.
// Usage: node build_hub.js   -> ../course-hub/index.html
// Open it from the repo (it loads ../assets and ../video by relative path), or
// upload the course-hub/, assets/ and video/ folders together to any static host.
const fs = require('fs');
const path = require('path');
const { marked } = require('marked');
const { C, logoMark } = require('./build_images.js');

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'course-hub');
const read = f => fs.readFileSync(path.join(ROOT, f), 'utf8');
const STAGES = [
  ['0', 'Zero', [0]], ['1', 'Foundations', [1, 2]], ['2', 'Practitioner', [3, 4, 5]],
  ['3', 'Analyst', [6, 7]], ['4', 'Strategist', [8, 9, 10, 11]], ['5', 'Operator', [12, 13, 14]],
];
const ICONS = { 0: 'compass', 1: 'shield', 2: 'swap', 3: 'bank', 4: 'sprout', 5: 'layers', 6: 'search', 7: 'chart', 8: 'cog', 9: 'grid', 10: 'target', 11: 'umbrella', 12: 'vault', 13: 'coins', 14: 'bot' };

// ---- markdown -> lesson HTML ------------------------------------------------
const KINDS = [
  [/^objective/i, 'obj', 'Objective'], [/^worked example/i, 'ex', 'Worked example'], [/^checklist/i, 'check', 'Checklist'],
  [/^quiz/i, 'quiz', 'Quiz'], [/^the 60-second/i, 'sixty', 'The 60-second version'], [/^words you/i, 'words', 'Words you’ll need'],
  [/^before you start/i, 'safe', 'Before you start'], [/^your first safe step/i, 'step', 'Your first safe step'],
  [/^the mastery ladder/i, 'ladder', 'The mastery ladder'], [/^you.ve mastered/i, 'mastered', 'You’ve mastered this module when…'],
];
const strip = h => h.replace(/<[^>]+>/g, '').replace(/&#39;/g, "'").replace(/&quot;/g, '"').replace(/&amp;/g, '&').trim();
function lessonHtml(md, lid) {
  let qn = 0, cn = 0;
  md = md.replace(/<details>\s*<summary>([\s\S]*?)<\/summary>\s*([\s\S]*?)<\/details>/g, (_, q, a) => {
    const k = `${lid}:q${qn++}`;
    return `<div class="qq" data-k="${k}"><div class="qtext">${marked.parseInline(q.trim().replace(/^\d+\.\s*/, ''))}</div>
      <button class="reveal">Reveal answer</button><div class="ans" hidden><div>${marked.parseInline(a.trim())}</div>
      <div class="grade"><span>How did you do?</span><button data-g="1">✓ I got it</button><button data-g="0">✗ I missed it</button></div></div></div>\n`;
  });
  const renderer = new marked.Renderer();
  renderer.image = ({ href, text }) => `<figure><img loading="lazy" alt="${text}" src="${href.replace(/^(\.\.\/)?assets\//, '../assets/')}">${text && !/assets\/modules\//.test(href) ? `<figcaption>${text}</figcaption>` : ''}</figure>`;
  let html = marked.parse(md, { renderer, gfm: true })
    .replace(/<li><input (checked="" )?disabled="" type="checkbox">\s*/g, () => `<li class="task"><label><input type="checkbox" data-k="${lid}:c${cn++}"><span>`)
    .replace(/<p>(<figure[\s\S]*?<\/figure>)<\/p>/g, '$1');
  html = html.replace(/(<li class="task"><label>[\s\S]*?)(<\/li>)/g, '$1</span></label>$2');
  return html.split(/(?=<h3[\s>])/).map(ch => {
    const h3 = ch.match(/^<h3[^>]*>([\s\S]*?)<\/h3>/);
    if (!h3) return ch;
    const k = KINDS.find(([re]) => re.test(strip(h3[1])));
    return k ? `<section class="box ${k[1]}"><div class="tag">${k[2]}</div>${ch.slice(h3[0].length)}</section>` : ch;
  }).join('');
}
const plainText = md => md.replace(/<[^>]+>/g, ' ').replace(/!\[[^\]]*\]\([^)]*\)/g, '').replace(/\[([^\]]+)\]\([^)]*\)/g, '$1').replace(/[*`#|>_-]+/g, ' ').replace(/\s+/g, ' ').trim();

// ---- collect modules and lessons ---------------------------------------------
function moduleSource(num) {
  const f = fs.readdirSync(path.join(ROOT, 'lessons')).find(x => x.startsWith(`module-${String(num).padStart(2, '0')}-`));
  let text = read(`lessons/${f}`);
  if (num === 2) {
    const sample = read('02-sample-lesson-amm-math.md').replace(/\n## /g, '\n### ').replace('# Sample Lesson 2.2', '## Lesson 2.2');
    text = text.replace(/Lesson 2\.2 \(AMM mathematics\) is in `\.\.\/02-sample-lesson-amm-math\.md`\.\n/, '');
    const i = text.indexOf('## Lesson 2.3');
    text = text.slice(0, i) + sample + '\n\n' + text.slice(i);
  }
  if (num === 8) {  // the stub 8.3 in the module file points to the full library: inline it
    const lib = read('03-defi-strategy-mastery.md').replace(/^# .*$/m, '').replace(/\n## /g, '\n### ').replace(/\n### (?=\d)/g, '\n#### ');
    text = text.replace(/## Lesson 8\.3 — [^\n]*\n[\s\S]*?(?=\n## Lesson 8\.4)/, `## Lesson 8.3 — The strategy library\n${lib}\n`);
  }
  return text;
}
const exists = rel => fs.existsSync(path.join(ROOT, rel));
function videoFor(id) {
  if (!exists(`video/${id}.mp4`)) return null;
  const ch = exists(`video/chapters/${id}.txt`) ? read(`video/chapters/${id}.txt`).trim().split('\n').map(l => { const [t, ...r] = l.split(' '); const s = t.split(':').reverse().reduce((a, x, i) => a + +x * 60 ** i, 0); return [s, t, r.join(' ')]; }) : [];
  return { src: `../video/${id}.mp4`, poster: exists(`video/thumbs/${id}.jpg`) ? `../video/thumbs/${id}.jpg` : '', vtt: exists(`video/captions/${id}.vtt`) ? `../video/captions/${id}.vtt` : '', chapters: ch };
}
const modules = [];
for (let num = 0; num <= 14; num++) {
  const src = moduleSource(num);
  const title = src.match(/^# Module \d+ — (.+)$/m)[1].trim();
  const outcome = (src.match(/^\*Outcome: (.+?)\*$/m) || [, ''])[1];
  const parts = src.split(/^## Lesson (\d+\.\d+) — (.+)$/m);
  const lessons = [];
  for (let i = 1; i < parts.length; i += 3) {
    const lid = parts[i], ltitle = parts[i + 1].replace(/\s*\*\(.*?\)\*\s*$/, '').trim();
    const body = parts[i + 2].split(/\n### Module /)[0].replace(/\n---\s*$/g, '').trim();
    const vid = `lesson-${lid.split('.')[0].padStart(2, '0')}-${lid.split('.')[1]}`;
    const script = exists(`video-scripts/gold/${vid}.json`) ? `video-scripts/gold/${vid}.json` : exists(`video-scripts/lessons/${vid}.json`) ? `video-scripts/lessons/${vid}.json` : null;
    lessons.push({ id: lid, title: /mastery starter/i.test(ltitle) ? 'Mastery Starter' : ltitle, starter: lid.endsWith('.0'), html: lessonHtml(body, lid), text: plainText(body).slice(0, 6000), video: videoFor(vid), script });
  }
  lessons.sort((a, b) => a.id.split('.').map(Number)[1] - b.id.split('.').map(Number)[1]);
  modules.push({ n: num, title, outcome, icon: ICONS[num], banner: `../assets/modules/module-${String(num).padStart(2, '0')}.png`, intro: videoFor(`module-${String(num).padStart(2, '0')}-intro`), lessons });
}
const welcome = videoFor('welcome');
const totalLessons = modules.reduce((a, m) => a + m.lessons.filter(l => !l.starter).length, 0);

// ---- page -------------------------------------------------------------------
const ICON = require('./build_images.js').icon;
const iconSvgs = Object.fromEntries(Object.values(ICONS).concat(['check', 'search', 'video', 'book', 'chart', 'target']).map(n => [n, ICON(n, 20)]));
const DATA = { stages: STAGES, modules, welcome, totalLessons, icons: iconSvgs };

const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>On-Chain Operator · Course Hub</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<link rel="icon" href="../assets/brand/favicon-256.png">
<style>
:root { --bg:#FCFCFB; --panel:#F3F6F9; --card:#ffffff; --line:#D9E1EA; --text:#141a21; --text2:#52606d; --muted:#8a8f98; --brand:${C.brand}; --ink:${C.ink};
  --accent:${C.blue}; --accent2:#14a874; --warn:${C.orange}; --side:#0B1F33; --sidetext:#dbe6f2; --glow:rgba(42,120,214,.12); color-scheme: light; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg:#0a1726; --panel:#0f2135; --card:#11263d; --line:#1f3a57; --text:#e8eef5; --text2:#a9b8c8; --muted:#7d8da0;
  --accent:#4d9bf0; --accent2:#2ee6a6; --warn:#ff8a57; --side:#071220; --glow:rgba(46,230,166,.10); color-scheme: dark; } }
:root[data-theme="dark"] { --bg:#0a1726; --panel:#0f2135; --card:#11263d; --line:#1f3a57; --text:#e8eef5; --text2:#a9b8c8; --muted:#7d8da0;
  --accent:#4d9bf0; --accent2:#2ee6a6; --warn:#ff8a57; --side:#071220; --glow:rgba(46,230,166,.10); color-scheme: dark; }
* { box-sizing: border-box; }
html, body { margin: 0; background: var(--bg); color: var(--text); font-family: Inter, system-ui, -apple-system, "Segoe UI", sans-serif; -webkit-font-smoothing: antialiased; }
a { color: var(--accent); }
button { font: inherit; cursor: pointer; }
.app { display: grid; grid-template-columns: 318px 1fr; min-height: 100vh; }
aside { position: sticky; top: 0; height: 100vh; overflow-y: auto; background: var(--side); color: var(--sidetext); padding: 18px 14px 40px; }
.brand { display: flex; gap: 10px; align-items: center; padding: 4px 6px 14px; text-decoration: none; color: #fff; }
.brand b { display: block; font-weight: 800; letter-spacing: .06em; font-size: 14px; } .brand b span { color: #2ee6a6; }
.brand small { display: block; font-size: 10px; letter-spacing: .38em; color: rgba(255,255,255,.55); margin-top: 3px; }
.search { position: relative; margin: 6px 4px 14px; }
.search input { width: 100%; padding: 10px 12px 10px 36px; border-radius: 10px; border: 1px solid rgba(255,255,255,.14); background: rgba(255,255,255,.06); color: #fff; font: inherit; font-size: 14px; }
.search svg { position: absolute; left: 11px; top: 11px; color: rgba(255,255,255,.5); }
.overall { margin: 0 6px 16px; font-size: 12px; color: rgba(255,255,255,.7); }
.bar { height: 6px; border-radius: 4px; background: rgba(255,255,255,.1); overflow: hidden; margin-top: 6px; }
.bar i { display: block; height: 100%; background: linear-gradient(90deg,#2ee6a6,#3987e5); border-radius: 4px; transition: width .3s; }
.nav-top a { display: flex; gap: 10px; align-items: center; padding: 8px 10px; border-radius: 8px; color: var(--sidetext); text-decoration: none; font-size: 14px; font-weight: 600; }
.nav-top a:hover, .nav-top a.on { background: rgba(255,255,255,.08); }
.stage { margin-top: 14px; }
.stage > .sh { font-size: 10.5px; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; color: #2ee6a6; padding: 6px 10px; display: flex; justify-content: space-between; }
details.mod { border-radius: 8px; }
details.mod > summary { list-style: none; display: flex; gap: 10px; align-items: center; padding: 8px 10px; border-radius: 8px; cursor: pointer; font-size: 13.5px; font-weight: 600; color: #fff; }
details.mod > summary::-webkit-details-marker { display: none; }
details.mod > summary:hover { background: rgba(255,255,255,.06); }
details.mod > summary .ic { color: #7fb2ff; flex: none; display: flex; }
details.mod > summary .pc { margin-left: auto; font-size: 11px; color: rgba(255,255,255,.5); font-weight: 500; }
.lessons a { display: flex; gap: 8px; padding: 6px 10px 6px 40px; font-size: 13px; color: rgba(219,230,242,.78); text-decoration: none; border-radius: 6px; line-height: 1.35; }
.lessons a:hover { background: rgba(255,255,255,.05); color: #fff; }
.lessons a.on { background: rgba(46,230,166,.12); color: #fff; box-shadow: inset 3px 0 0 #2ee6a6; }
.lessons a .id { flex: none; width: 30px; color: rgba(255,255,255,.45); font-variant-numeric: tabular-nums; }
.lessons a.done .id::after { content: ' ✓'; color: #2ee6a6; }
main { min-width: 0; }
.topbar { position: sticky; top: 0; z-index: 5; display: flex; align-items: center; gap: 12px; padding: 12px 28px; background: color-mix(in srgb, var(--bg) 88%, transparent); backdrop-filter: blur(8px); border-bottom: 1px solid var(--line); }
.crumbs { font-size: 13px; color: var(--text2); flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.icon-btn { border: 1px solid var(--line); background: var(--card); color: var(--text); border-radius: 9px; padding: 7px 11px; font-size: 13px; }
.menu-btn { display: none; }
.content { max-width: 880px; margin: 0 auto; padding: 30px 28px 90px; }
.hero { border-radius: 20px; padding: 34px 34px 30px; color: #fff; background: radial-gradient(120% 90% at 85% 0%, #1d4a78 0%, ${C.navy} 38%, ${C.ink} 100%); position: relative; overflow: hidden; }
.hero h1 { margin: 12px 0 6px; font-size: 34px; letter-spacing: -.02em; line-height: 1.1; }
.hero p { color: rgba(255,255,255,.8); margin: 0; font-size: 16px; }
.hero .cta { display: inline-flex; margin-top: 20px; padding: 12px 22px; border-radius: 999px; background: linear-gradient(90deg,#2ee6a6,#3987e5); color: ${C.ink}; font-weight: 800; text-decoration: none; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 14px; margin-top: 18px; }
.card { background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 16px 18px; text-decoration: none; color: var(--text); display: block; transition: transform .15s, box-shadow .15s; }
.card:hover { transform: translateY(-2px); box-shadow: 0 10px 30px var(--glow); }
.card .k { font-size: 11px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--accent); }
.card h3 { margin: 6px 0 6px; font-size: 17px; }
.card p { margin: 0; color: var(--text2); font-size: 13.5px; line-height: 1.45; }
h2.sec { font-size: 22px; margin: 34px 0 4px; letter-spacing: -.01em; }
.lesson-head { display: flex; gap: 18px; align-items: stretch; margin-bottom: 18px; }
.lesson-head .n { flex: none; min-width: 84px; border-radius: 14px; background: var(--brand); color: #fff; font-weight: 800; font-size: 30px; display: flex; align-items: center; justify-content: center; letter-spacing: -.03em; }
.lesson-head.starter .n { background: linear-gradient(135deg,#14a874,#2a78d6); }
.lesson-head .k { font-size: 11px; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; color: var(--accent); }
.lesson-head h1 { margin: 4px 0 0; font-size: 30px; letter-spacing: -.02em; line-height: 1.15; }
.video { margin: 8px 0 20px; border-radius: 14px; overflow: hidden; background: #000; border: 1px solid var(--line); }
.video video { display: block; width: 100%; aspect-ratio: 16/9; background: #000; }
.chapters { display: flex; flex-wrap: wrap; gap: 6px; padding: 10px 12px; background: var(--panel); }
.chapters button { border: 1px solid var(--line); background: var(--card); color: var(--text2); border-radius: 999px; padding: 4px 10px; font-size: 12px; }
.chapters button b { color: var(--accent); font-weight: 600; margin-right: 4px; font-variant-numeric: tabular-nums; }
.novideo { display: flex; gap: 14px; align-items: center; padding: 14px 16px; border-radius: 14px; border: 1px dashed var(--line); background: var(--panel); color: var(--text2); font-size: 13.5px; margin: 8px 0 20px; }
article { font-size: 16px; line-height: 1.7; }
article h3 { font-size: 19px; margin: 28px 0 6px; }
article p { margin: 8px 0 12px; }
article figure { margin: 18px 0; } article figure img { width: 100%; border-radius: 12px; border: 1px solid var(--line); background: #fff; }
article figcaption { font-size: 13px; color: var(--muted); text-align: center; margin-top: 6px; }
article table { width: 100%; border-collapse: separate; border-spacing: 0; font-size: 14px; border: 1px solid var(--line); border-radius: 10px; overflow: hidden; margin: 12px 0 16px; display: block; overflow-x: auto; }
article th { background: var(--ink); color: #fff; text-align: left; padding: 8px 10px; font-size: 13px; }
article td { padding: 8px 10px; border-top: 1px solid var(--line); vertical-align: top; background: var(--card); }
article code { font-family: "JetBrains Mono", ui-monospace, monospace; font-size: .86em; background: var(--panel); border: 1px solid var(--line); padding: 1px 5px; border-radius: 5px; }
article pre { background: var(--ink); color: #d7e3f0; padding: 14px; border-radius: 10px; overflow-x: auto; } article pre code { background: none; border: 0; color: inherit; }
article blockquote { margin: 14px 0; padding: 8px 16px; border-left: 4px solid var(--accent); background: var(--panel); border-radius: 0 10px 10px 0; }
.box { position: relative; border-radius: 14px; padding: 24px 20px 10px; margin: 26px 0 18px; background: var(--panel); border: 1px solid var(--line); }
.box .tag { position: absolute; top: -11px; left: 16px; font-size: 11px; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; padding: 4px 11px; border-radius: 999px; color: #fff; background: var(--brand); }
.box.obj { border-left: 5px solid var(--accent); font-weight: 600; } .box.obj .tag { background: var(--accent); }
.box.ex { border-left: 5px solid var(--ink); } .box.ex .tag { background: var(--ink); }
:root[data-theme="dark"] .box.ex .tag { background: #3a5877; }
.box.check { border-left: 5px solid var(--accent2); } .box.check .tag { background: #14a874; }
.box.quiz { border-left: 5px solid var(--warn); } .box.quiz .tag { background: var(--warn); }
.box.sixty { background: linear-gradient(120deg, ${C.ink}, ${C.navy}); color: #fff; border: 0; } .box.sixty .tag { background: #2ee6a6; color: ${C.ink}; } .box.sixty strong { color: #2ee6a6; }
.box.safe, .box.step { border-left: 5px solid var(--accent2); } .box.safe .tag, .box.step .tag { background: #14a874; }
.box.mastered { border-left: 5px solid var(--brand); font-weight: 600; }
li.task { list-style: none; margin-left: -22px; }
li.task label { display: flex; gap: 10px; align-items: flex-start; cursor: pointer; padding: 3px 0; }
li.task input { width: 18px; height: 18px; margin-top: 4px; accent-color: #14a874; flex: none; }
li.task input:checked + span { color: var(--muted); text-decoration: line-through; }
.qq { padding: 12px 0 14px; border-bottom: 1px dashed var(--line); } .qq:last-child { border-bottom: 0; }
.qtext { font-weight: 700; }
.reveal { margin-top: 8px; border: 1px solid var(--warn); color: var(--warn); background: transparent; border-radius: 999px; padding: 5px 14px; font-size: 13px; font-weight: 600; }
.ans { margin-top: 10px; padding: 10px 14px; border-radius: 10px; background: var(--card); border: 1px solid var(--line); }
.grade { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-top: 8px; font-size: 13px; color: var(--text2); }
.grade button { border: 1px solid var(--line); background: var(--panel); color: var(--text); border-radius: 999px; padding: 4px 12px; font-size: 13px; }
.grade button.sel[data-g="1"] { background: #14a874; color: #fff; border-color: #14a874; } .grade button.sel[data-g="0"] { background: var(--warn); color: #fff; border-color: var(--warn); }
.done-row { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; justify-content: space-between; margin-top: 34px; padding: 18px 20px; border-radius: 14px; background: var(--panel); border: 1px solid var(--line); }
.btn { border: 0; border-radius: 999px; padding: 11px 20px; font-weight: 700; font-size: 14px; background: var(--brand); color: #fff; text-decoration: none; display: inline-flex; gap: 8px; align-items: center; }
.btn.good { background: #14a874; } .btn.ghost { background: transparent; color: var(--text); border: 1px solid var(--line); }
.pager { display: flex; justify-content: space-between; gap: 12px; margin-top: 16px; }
.pager a { flex: 1; padding: 14px 16px; border-radius: 12px; border: 1px solid var(--line); text-decoration: none; color: var(--text); background: var(--card); font-size: 14px; }
.pager a small { display: block; color: var(--muted); font-size: 12px; margin-bottom: 2px; } .pager a.next { text-align: right; }
.results a { display: block; padding: 12px 14px; border-radius: 10px; border: 1px solid var(--line); margin: 8px 0; text-decoration: none; color: var(--text); background: var(--card); }
.results a small { color: var(--muted); display: block; margin-top: 3px; font-size: 13px; } mark { background: rgba(46,230,166,.35); color: inherit; border-radius: 3px; }
.calc { background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 18px 20px; margin: 16px 0; }
.calc h3 { margin: 0 0 4px; font-size: 18px; } .calc p.d { margin: 0 0 12px; color: var(--text2); font-size: 14px; }
.calc .f { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px; }
.calc label { font-size: 12px; color: var(--text2); font-weight: 600; display: block; }
.calc input { width: 100%; margin-top: 4px; padding: 8px 10px; border-radius: 8px; border: 1px solid var(--line); background: var(--bg); color: var(--text); font: inherit; font-size: 15px; }
.calc .out { margin-top: 12px; padding: 12px 14px; border-radius: 10px; background: var(--panel); font-family: "JetBrains Mono", ui-monospace, monospace; font-size: 13.5px; line-height: 1.7; white-space: pre-wrap; }
.calc .out .warn { color: var(--warn); font-weight: 700; }
.disc { margin-top: 40px; font-size: 12px; color: var(--muted); text-align: center; }
.mod-banner { width: 100%; border-radius: 16px; display: block; }
@media (max-width: 900px) { .app { grid-template-columns: 1fr; } aside { position: fixed; z-index: 20; left: 0; top: 0; width: 86vw; max-width: 340px; transform: translateX(-100%); transition: transform .2s; box-shadow: 0 0 40px rgba(0,0,0,.4); }
  body.nav-open aside { transform: none; } .menu-btn { display: inline-block; } .content { padding: 22px 16px 80px; } .topbar { padding: 10px 16px; } .hero { padding: 24px 20px; } .hero h1 { font-size: 26px; } .lesson-head h1 { font-size: 23px; } .lesson-head .n { min-width: 64px; font-size: 22px; } }
</style></head><body>
<div class="app">
<aside>
  <a class="brand" href="#/">${logoMark(40, { nodes: false })}<div><b>ON-CHAIN <span>OPERATOR</span></b><small>COURSE HUB</small></div></a>
  <div class="search">${ICON('search', 16)}<input id="q" type="search" placeholder="Search lessons  ( / )" autocomplete="off"></div>
  <div class="overall"><span id="ovtxt"></span><div class="bar"><i id="ovbar"></i></div></div>
  <nav class="nav-top"><a href="#/" data-r="home">${ICON('compass', 18)} Start here</a><a href="#/tools" data-r="tools">${ICON('chart', 18)} Calculators</a></nav>
  <nav id="tree"></nav>
</aside>
<main>
  <div class="topbar"><button class="icon-btn menu-btn" id="menu" aria-label="Menu">☰</button><div class="crumbs" id="crumbs"></div>
    <button class="icon-btn" id="theme" title="Toggle theme">◐ Theme</button></div>
  <div class="content" id="view"></div>
</main></div>
<script id="data" type="application/json">${JSON.stringify(DATA).replace(/</g, '\\u003c')}</script>
<script>
const D = JSON.parse(document.getElementById('data').textContent);
const $ = s => document.querySelector(s), esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
// ---- state (per browser; wrapped because storage can be unavailable)
const KEY = 'oop-hub-v1';
let S = { done: {}, checks: {}, quiz: {}, last: null };
try { S = Object.assign(S, JSON.parse(localStorage.getItem(KEY) || '{}')); } catch (e) {}
const save = () => { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} };
try { const t = localStorage.getItem('oop-theme'); if (t) document.documentElement.dataset.theme = t; } catch (e) {}
$('#theme').onclick = () => { const cur = document.documentElement.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  const nx = cur === 'dark' ? 'light' : 'dark'; document.documentElement.dataset.theme = nx; try { localStorage.setItem('oop-theme', nx); } catch (e) {} };
$('#menu').onclick = () => document.body.classList.toggle('nav-open');
// ---- index
const ALL = []; D.modules.forEach(m => m.lessons.forEach(l => ALL.push({ ...l, m })));
const byId = Object.fromEntries(ALL.map(l => [l.id, l]));
const stageOf = n => D.stages.find(s => s[2].includes(n));
const countable = ALL.filter(l => !l.starter);
function progress() {
  const d = countable.filter(l => S.done[l.id]).length;
  $('#ovtxt').textContent = d + ' of ' + countable.length + ' lessons complete';
  $('#ovbar').style.width = (d / countable.length * 100) + '%';
}
function tree(active) {
  $('#tree').innerHTML = D.stages.map(([n, name, mods]) => {
    const ls = ALL.filter(l => mods.includes(l.m.n) && !l.starter), d = ls.filter(l => S.done[l.id]).length;
    return '<div class="stage"><div class="sh"><span>Stage ' + n + ' · ' + name + '</span><span>' + d + '/' + ls.length + '</span></div>' + mods.map(mn => {
      const m = D.modules[mn], open = active && active.m.n === mn;
      const md = m.lessons.filter(l => !l.starter && S.done[l.id]).length, mt = m.lessons.filter(l => !l.starter).length;
      return '<details class="mod"' + (open ? ' open' : '') + '><summary><span class="ic">' + D.icons[m.icon] + '</span>' + mn + '. ' + esc(m.title) + '<span class="pc">' + md + '/' + mt + '</span></summary><div class="lessons">' +
        '<a href="#/m/' + mn + '">' + '<span class="id">•</span>Module overview</a>' +
        m.lessons.map(l => '<a href="#/l/' + l.id + '" class="' + (S.done[l.id] ? 'done ' : '') + (active && active.id === l.id ? 'on' : '') + '"><span class="id">' + l.id + '</span>' + esc(l.title) + '</a>').join('') + '</div></details>';
    }).join('') + '</div>';
  }).join('');
  progress();
}
function videoBlock(v, label) {
  if (!v) return '';
  return '<div class="video"><video controls preload="metadata" playsinline ' + (v.poster ? 'poster="' + v.poster + '"' : '') + ' src="' + v.src + '">' + (v.vtt ? '<track kind="captions" srclang="en" label="English" src="' + v.vtt + '">' : '') + '</video>' +
    (v.chapters.length ? '<div class="chapters">' + v.chapters.map(c => '<button data-t="' + c[0] + '"><b>' + c[1] + '</b>' + esc(c[2]) + '</button>').join('') + '</div>' : '') + '</div>';
}
function wireVideo() { document.querySelectorAll('.chapters button').forEach(b => b.onclick = () => { const v = b.closest('.video').querySelector('video'); v.currentTime = +b.dataset.t; v.play(); }); }
// ---- views
function home() {
  const next = S.last && byId[S.last] ? byId[S.last] : ALL[0];
  $('#crumbs').textContent = 'Start here';
  return '<div class="hero">' + ${JSON.stringify(logoMark(64, { nodes: false }))} + '<h1>From zero to your own on-chain bank.</h1><p>Six stages · 15 modules · ' + D.totalLessons + ' lessons, each module opening with a Mastery Starter.</p>' +
    '<a class="cta" href="#/l/' + next.id + '">' + (S.last ? 'Continue: Lesson ' + next.id : 'Begin with Lesson ' + next.id) + ' →</a></div>' +
    (D.welcome ? '<h2 class="sec">Welcome</h2>' + videoBlock(D.welcome) : '') +
    '<h2 class="sec">How every lesson works</h2><div class="grid">' +
    [['1 · Watch', 'The narrated video walks through the idea and the numbers on screen.'], ['2 · Do', 'Tick the checklist for real, with a small test amount. Your ticks are saved in this browser.'], ['3 · Check', 'Answer the quiz, reveal the answer, and mark yourself honestly.']].map(([a, b]) => '<div class="card"><h3>' + a + '</h3><p>' + b + '</p></div>').join('') + '</div>' +
    D.stages.map(([n, name, mods]) => '<h2 class="sec">Stage ' + n + ' · ' + name + '</h2><div class="grid">' + mods.map(mn => { const m = D.modules[mn], mt = m.lessons.filter(l => !l.starter), d = mt.filter(l => S.done[l.id]).length;
      return '<a class="card" href="#/m/' + mn + '"><div class="k">Module ' + mn + '</div><h3>' + esc(m.title) + '</h3><p>' + esc(m.outcome) + '</p><div class="bar" style="background:var(--panel)"><i style="width:' + (d / mt.length * 100) + '%"></i></div></a>'; }).join('') + '</div>').join('') +
    '<p class="disc">Educational content only · Not financial advice · No results are guaranteed · We will never ask for your seed phrase or keys.</p>';
}
function modView(mn) {
  const m = D.modules[mn]; $('#crumbs').textContent = 'Stage ' + stageOf(mn)[0] + ' · Module ' + mn + ' · ' + m.title;
  return '<img class="mod-banner" src="' + m.banner + '" alt="Module ' + mn + '">' + (m.intro ? '<h2 class="sec">Module intro</h2>' + videoBlock(m.intro) : '') +
    '<h2 class="sec">Outcome</h2><p>' + esc(m.outcome) + '</p><h2 class="sec">Lessons</h2><div class="grid">' +
    m.lessons.map(l => '<a class="card" href="#/l/' + l.id + '"><div class="k">' + (l.starter ? 'Start here' : 'Lesson ' + l.id) + (S.done[l.id] ? ' · ✓ done' : '') + '</div><h3>' + esc(l.title) + '</h3></a>').join('') + '</div>';
}
function lessonView(id) {
  const l = byId[id]; if (!l) return home();
  S.last = id; save();
  const i = ALL.indexOf(l), prev = ALL[i - 1], next = ALL[i + 1];
  $('#crumbs').textContent = 'Stage ' + stageOf(l.m.n)[0] + ' · Module ' + l.m.n + ' · ' + l.m.title + ' · ' + (l.starter ? 'Mastery Starter' : 'Lesson ' + l.id);
  return '<div class="lesson-head' + (l.starter ? ' starter' : '') + '"><div class="n">' + l.id + '</div><div><div class="k">' + (l.starter ? 'Mastery Starter · start here' : 'Module ' + l.m.n + ' · ' + esc(l.m.title)) + '</div><h1>' + esc(l.title) + '</h1></div></div>' +
    (l.video ? videoBlock(l.video) : l.script ? '<div class="novideo">' + D.icons.video + '<div>The narrated video for this lesson is scripted (<code>' + l.script + '</code>) and renders with <code>node build_video.js ' + l.script.split('/').pop().replace('.json', '') + '</code>.</div></div>' : '') +
    '<article>' + l.html + '</article>' +
    '<div class="done-row"><div><b>' + (S.done[id] ? 'Lesson complete ✓' : 'Finished the checklist and quiz?') + '</b></div><button class="btn ' + (S.done[id] ? 'ghost' : 'good') + '" id="mark">' + (S.done[id] ? 'Mark as not done' : 'Mark lesson complete') + '</button></div>' +
    '<div class="pager">' + (prev ? '<a href="#/l/' + prev.id + '"><small>← Previous</small>' + prev.id + ' ' + esc(prev.title) + '</a>' : '<span></span>') + (next ? '<a class="next" href="#/l/' + next.id + '"><small>Next →</small>' + next.id + ' ' + esc(next.title) + '</a>' : '') + '</div>' +
    '<p class="disc">Educational content only · Not financial advice · No results are guaranteed.</p>';
}
function wireLesson(id) {
  document.querySelectorAll('li.task input').forEach(cb => { cb.checked = !!S.checks[cb.dataset.k]; cb.onchange = () => { S.checks[cb.dataset.k] = cb.checked; save(); }; });
  document.querySelectorAll('.qq').forEach(q => { const k = q.dataset.k, a = q.querySelector('.ans'), r = q.querySelector('.reveal');
    const paint = () => q.querySelectorAll('.grade button').forEach(b => b.classList.toggle('sel', String(S.quiz[k]) === b.dataset.g));
    if (S.quiz[k] !== undefined) { a.hidden = false; r.hidden = true; }
    r.onclick = () => { a.hidden = false; r.hidden = true; };
    q.querySelectorAll('.grade button').forEach(b => b.onclick = () => { S.quiz[k] = +b.dataset.g; save(); paint(); }); paint(); });
  const mk = $('#mark'); if (mk) mk.onclick = () => { S.done[id] = !S.done[id]; save(); route(); };
}
function searchView(term) {
  $('#crumbs').textContent = 'Search';
  const t = term.toLowerCase().trim(); if (!t) return home();
  const words = t.split(/\\s+/);
  const hits = ALL.map(l => { const hay = (l.title + ' ' + l.text).toLowerCase(); const score = words.reduce((a, w) => a + (hay.includes(w) ? 1 + (l.title.toLowerCase().includes(w) ? 3 : 0) : -99), 0); return [score, l]; })
    .filter(x => x[0] > 0).sort((a, b) => b[0] - a[0]).slice(0, 40);
  const hl = s => esc(s).replace(new RegExp('(' + words.map(w => w.replace(/[.*+?^\${}()|[\\]\\\\]/g, '\\\\$&')).join('|') + ')', 'gi'), '<mark>$1</mark>');
  return '<h1 style="margin-top:0">Search: “' + esc(term) + '”</h1><p style="color:var(--text2)">' + hits.length + ' lesson' + (hits.length === 1 ? '' : 's') + '</p><div class="results">' +
    hits.map(([, l]) => { const i = l.text.toLowerCase().indexOf(words[0]); const snip = l.text.slice(Math.max(0, i - 70), i + 150);
      return '<a href="#/l/' + l.id + '"><b>' + l.id + ' · ' + hl(l.title) + '</b><small>Module ' + l.m.n + ' · …' + hl(snip) + '…</small></a>'; }).join('') + '</div>';
}
// ---- calculators (same formulas as defi_calc.py)
const money = x => (x < 0 ? '−$' : '$') + Math.abs(x).toLocaleString('en-US', { maximumFractionDigits: 2 });
const pct = (x, d = 2) => (x * 100).toFixed(d) + '%';
const CALCS = [
  { id: 'health', t: 'Health factor & liquidation price', d: 'Before any borrow. Lesson 3.2.', f: [['qty', 'Collateral quantity', 10], ['price', 'Collateral price ($)', 3000], ['lt', 'Liquidation threshold', 0.8], ['debt', 'Debt ($)', 12000]],
    run: v => { const coll = v.qty * v.price, hf = coll * v.lt / v.debt, liq = v.debt / (v.qty * v.lt);
      return 'Collateral ' + money(coll) + ' · LTV ' + pct(v.debt / coll, 1) + '\\nHealth factor ' + hf.toFixed(2) + ' · liquidation price ' + money(liq) + ' (' + ((liq / v.price - 1) * 100).toFixed(1) + '% from now)\\nMax debt for HF 1.5: ' + money(coll * v.lt / 1.5) + ' · for HF 2.0: ' + money(coll * v.lt / 2) + (hf < 1.5 ? '\\n<span class="warn">Warning: HF below 1.5. Repay or add collateral.</span>' : ''); } },
  { id: 'il', t: 'Impermanent loss', d: '50/50 constant-product pool, before fees. Lesson 2.3.', f: [['ratio', 'Price ratio (new ÷ entry)', 2], ['days', 'Days held', 90], ['fee', 'Fee APR (%)', 20]],
    run: v => { const il = 1 - 2 * Math.sqrt(v.ratio) / (1 + v.ratio), need = il * 365 / v.days, earned = v.fee / 100 * v.days / 365;
      return v.ratio + '× move → impermanent loss ' + pct(il) + '\\nFee APR needed over ' + v.days + ' days just to match holding: ' + pct(need) + '\\nAt ' + v.fee + '% fee APR you earn ' + pct(earned) + ' → net vs holding ' + (earned - il >= 0 ? '+' : '') + pct(earned - il); } },
  { id: 'loop', t: 'Leveraged loop', d: 'Net yield on equity and the break-even borrow rate. Lesson 3.4.', f: [['lev', 'Leverage (×)', 3], ['capy', 'Collateral APY (%)', 3.5], ['bapy', 'Borrow APY (%)', 2.5]],
    run: v => { const net = v.capy * v.lev - v.bapy * (v.lev - 1), be = v.lev > 1 ? v.capy * v.lev / (v.lev - 1) : Infinity;
      return 'Net APY on equity ' + net.toFixed(2) + '% (unlevered ' + v.capy.toFixed(2) + '%)\\nBorrow rate that wipes out the return: ' + be.toFixed(2) + '%' + (net <= v.capy ? '\\n<span class="warn">Leverage adds nothing at this spread, only liquidation risk.</span>' : ''); } },
  { id: 'lvr', t: 'Loss-versus-rebalancing', d: 'What arbitrage costs a full-range LP. Lesson 2.7.', f: [['vol', 'Volatility (%/yr)', 80], ['fee', 'Fee APR (%)', 12]],
    run: v => { const r = (v.vol / 100) ** 2 / 8; return 'LVR ≈ ' + pct(r) + ' of pool value per year\\nFees minus LVR ≈ ' + (v.fee - r * 100 >= 0 ? '+' : '') + (v.fee - r * 100).toFixed(2) + '%/yr'; } },
  { id: 'pt', t: 'Fixed yield from a principal token (PT)', d: 'Lesson 10.1.', f: [['price', 'PT price (of underlying)', 0.95], ['days', 'Days to maturity', 180]],
    run: v => { const fixed = (1 / v.price) ** (365 / v.days) - 1, simple = (1 / v.price - 1) * 365 / v.days; return 'Fixed APY if held to maturity: ' + pct(fixed) + ' (simple ' + pct(simple) + ')\\nYT profits only if realised variable yield beats ≈ ' + pct(fixed) + ' over the period'; } },
  { id: 'expected', t: 'Risk-adjusted yield', d: 'Headline yield minus expected loss and costs. Lesson 13.1.', f: [['y', 'Headline yield (%)', 12], ['p', 'Annual loss probability', 0.05], ['lgd', 'Loss given default (0–1)', 0.6], ['c', 'Costs (%)', 0.5]],
    run: v => { const h = v.p * v.lgd * 100, net = v.y - h - v.c; return 'Headline ' + v.y + '% − expected loss ' + h.toFixed(2) + '% − costs ' + v.c + '% = ' + net.toFixed(2) + '% risk-adjusted'; } },
  { id: 'income', t: 'Income engine payout', d: 'Pay out less than you expect to earn. Module 13.', f: [['cap', 'Capital ($)', 250000], ['ry', 'Risk-adjusted yield (%)', 5], ['payout', 'Payout ratio (0–1)', 0.7]],
    run: v => { const exp = v.cap * v.ry / 100, pay = exp * v.payout; return 'Expected income ' + money(exp) + '/yr\\nPay out ' + pct(v.payout, 0) + ' = ' + money(pay) + '/yr (' + money(pay / 12) + '/month)\\nRetain ' + money(exp - pay) + ' as a loss buffer' + (v.payout > 0.8 ? '\\n<span class="warn">Payout above 80% of expected income leaves little buffer.</span>' : '') + '\\nIllustrative only. No income is promised.'; } },
  { id: 'var', t: 'One-day value at risk', d: 'A floor, not a ceiling: crypto tails are fatter. Lesson 11.5.', f: [['pos', 'Position ($)', 100000], ['vol', 'Volatility (%/yr)', 70], ['z', 'Confidence z (1.65 = 95%)', 1.65]],
    run: v => { const d = v.vol / 100 / Math.sqrt(365), x = v.z * d * v.pos; return 'Daily volatility ' + pct(d) + '\\n1-day VaR ≈ ' + money(x) + ' on ' + money(v.pos) + ' (' + pct(v.z * d) + ')'; } },
];
function toolsView() {
  $('#crumbs').textContent = 'Calculators';
  return '<h1 style="margin-top:0">Calculators</h1><p style="color:var(--text2)">The same formulas as the program’s <code>defi_calc.py</code>. Every number you act on should be computed, not guessed. Illustrative only; not financial advice.</p>' +
    CALCS.map(c => '<div class="calc" data-c="' + c.id + '"><h3>' + c.t + '</h3><p class="d">' + c.d + '</p><div class="f">' + c.f.map(([k, lab, def]) => '<label>' + lab + '<input type="number" step="any" data-k="' + k + '" value="' + def + '"></label>').join('') + '</div><div class="out"></div></div>').join('');
}
function wireTools() { document.querySelectorAll('.calc').forEach(el => { const c = CALCS.find(x => x.id === el.dataset.c);
  const upd = () => { const v = {}; el.querySelectorAll('input').forEach(i => v[i.dataset.k] = parseFloat(i.value)); el.querySelector('.out').innerHTML = Object.values(v).some(isNaN) ? 'Enter every value.' : c.run(v); };
  el.querySelectorAll('input').forEach(i => i.oninput = upd); upd(); }); }
// ---- router
function route() {
  const h = location.hash.replace(/^#\\/?/, ''), [kind, arg] = h.split('/');
  let html, active = null;
  if (kind === 'l') { active = byId[decodeURIComponent(arg)]; html = lessonView(decodeURIComponent(arg)); }
  else if (kind === 'm') html = modView(+arg);
  else if (kind === 'tools') html = toolsView();
  else if (kind === 's') html = searchView(decodeURIComponent(arg || ''));
  else html = home();
  $('#view').innerHTML = html; tree(active);
  document.querySelectorAll('.nav-top a').forEach(a => a.classList.toggle('on', (a.dataset.r === 'tools' && kind === 'tools') || (a.dataset.r === 'home' && !kind)));
  if (kind === 'l') wireLesson(decodeURIComponent(arg)); if (kind === 'tools') wireTools(); wireVideo();
  document.body.classList.remove('nav-open'); if (kind !== 's') window.scrollTo(0, 0);
  const on = document.querySelector('.lessons a.on'); if (on) on.scrollIntoView({ block: 'nearest' });
}
let st; $('#q').oninput = e => { clearTimeout(st); st = setTimeout(() => { location.hash = e.target.value.trim() ? '#/s/' + encodeURIComponent(e.target.value) : '#/'; }, 180); };
addEventListener('keydown', e => {
  if (e.target.matches('input, textarea')) return;
  if (e.key === '/') { e.preventDefault(); $('#q').focus(); }
  const m = location.hash.match(/^#\\/l\\/(.+)$/); if (!m) return; const i = ALL.findIndex(l => l.id === decodeURIComponent(m[1]));
  if (e.key === 'ArrowRight' && ALL[i + 1]) location.hash = '#/l/' + ALL[i + 1].id;
  if (e.key === 'ArrowLeft' && ALL[i - 1]) location.hash = '#/l/' + ALL[i - 1].id;
});
addEventListener('hashchange', route); route();
</script></body></html>`;

fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, 'index.html'), html);
const vids = modules.reduce((a, m) => a + m.lessons.filter(l => l.video).length, 0);
console.log(`wrote course-hub/index.html (${(html.length / 1024).toFixed(0)} KB, ${modules.reduce((a, m) => a + m.lessons.length, 0)} lessons, ${vids} with video)`);
