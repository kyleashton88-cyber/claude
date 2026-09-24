// Render the VSL and program videos defined in videos.js.
// Narration: Kokoro TTS (build_vo.py). Frames: Chromium, driven frame by
// frame (deterministic). Encode: ffmpeg H.264 + AAC, captions burned in.
// Usage: node build_video.js [videoId]   -> ../video/<id>.mp4 + ../video/SCRIPTS.md
const fs = require('fs');
const path = require('path');
const { spawn, execFileSync } = require('child_process');
const { chromium } = require('playwright-core');
const { C, FONT, BASE_CSS, network, icon, logoMark, wordmark, DISCLAIMER } = require('./build_images.js');
const { VIDEOS: CORE } = require('./videos.js');
// Extra video specs (e.g. lesson videos) as JSON in ../video-scripts/**/*.json, same schema as videos.js.
const SCRIPT_DIR = path.resolve(__dirname, '..', 'video-scripts');
const walk = d => (fs.existsSync(d) ? fs.readdirSync(d, { withFileTypes: true }).flatMap(e => (e.isDirectory() ? walk(path.join(d, e.name)) : e.name.endsWith('.json') ? [path.join(d, e.name)] : [])) : []);
const VIDEOS = [...CORE, ...walk(SCRIPT_DIR).sort().map(f => JSON.parse(fs.readFileSync(f, 'utf8')))];

const FPS = 30;
const LEAD_IN = 0.45, TAIL = 0.6; // seconds of breathing room around each voice line
const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'video');
const WORK = path.join(__dirname, '.render', 'video');
const FFMPEG = process.env.FFMPEG || execFileSync('python3', ['-c', 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())']).toString().trim();
const VOICE = process.env.VOICE || 'af_heart';

const asset = rel => `file://${path.join(ROOT, rel)}`;

// Split narration into caption chunks of ~n words, preferring punctuation breaks.
function captionChunks(text, n) {
  const words = text.split(/\s+/);
  const chunks = []; let cur = [];
  for (const w of words) {
    cur.push(w);
    if (cur.length >= n || (/[.,?!:]$/.test(w) && cur.length >= Math.ceil(n / 2))) { chunks.push(cur.join(' ')); cur = []; }
  }
  if (cur.length) chunks.push(cur.join(' '));
  return chunks;
}

function sceneBody(s, W, H) {
  const v = H > W, fs = (a, b) => (v ? b : a);
  const center = `position:absolute;inset:0 0 ${fs(200, 380)}px 0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center`;
  switch (s.type) {
    case 'strike': return `<div style="${center};gap:${fs(40, 60)}px">
      <div class="in" data-in="0.25" style="position:relative;font-size:${fs(230, 200)}px;font-weight:800;letter-spacing:-.03em">${s.big}
        <div class="strike" data-in="${s.tStrike}" style="position:absolute;left:-4%;top:52%;height:${fs(18, 16)}px;width:108%;background:${C.orange};border-radius:9px;transform-origin:left center;transform:scaleX(0)"></div></div>
      <div class="in" data-in="${s.tAfter}" style="font-size:${fs(72, 76)}px;font-weight:800;color:${C.aquaDark};max-width:${fs(1500, 900)}px">${s.after}</div></div>`;
    case 'statement': return `<div style="${center};padding:0 ${fs(160, 80)}px">
      ${s.lines.map((l, i) => `<div class="in" data-in="${0.3 + i * 0.8}" style="font-size:${fs(104, 92)}px;font-weight:800;line-height:1.1;letter-spacing:-.02em;${i ? `color:${C.aquaDark}` : ''}">${l}</div>`).join('')}
      ${s.sub ? `<div class="in" data-in="${s.tSub}" style="font-size:${fs(40, 44)}px;color:rgba(255,255,255,.8);margin-top:${fs(40, 50)}px;max-width:${fs(1300, 900)}px;line-height:1.4">${s.sub}</div>` : ''}</div>`;
    case 'bullets': if (s.compact || s.items.length > 5) {
      const n = s.items.length, size = n > 6 ? 36 : 42;
      return `<div style="position:absolute;left:200px;right:200px;top:150px">
      <div class="in" data-in="0.2" style="font-size:72px;font-weight:800;letter-spacing:-.015em">${s.title}</div>
      <div style="display:grid;grid-template-columns:${n > 5 ? '1fr 1fr' : '1fr'};gap:22px 50px;margin-top:40px">
      ${s.items.map((it, i) => `<div class="in" data-in="${s.tItems[i]}" style="display:flex;gap:20px;align-items:baseline;font-size:${size}px;color:rgba(255,255,255,.92);line-height:1.25">
        <span style="flex:none;color:${C.aquaDark};font-weight:800;font-size:${size - 4}px">${it.split(' ')[0]}</span><span>${it.split(' ').slice(1).join(' ')}</span></div>`).join('')}</div></div>`;
    }
    return `<div style="position:absolute;left:${fs(200, 90)}px;right:${fs(200, 90)}px;top:${fs(150, 420)}px">
      <div class="in" data-in="0.2" style="font-size:${fs(80, 76)}px;font-weight:800;letter-spacing:-.015em;line-height:1.1">${s.title}</div>
      ${s.items.map((it, i) => `<div class="in" data-in="${s.tItems[i]}" style="display:flex;align-items:center;gap:${fs(28, 26)}px;margin-top:${fs(28, 50)}px;font-size:${fs(48, 52)}px;color:rgba(255,255,255,.92)">
        <span style="flex:none;width:${fs(66, 70)}px;height:${fs(66, 70)}px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:${s.check === false ? 'rgba(235,104,52,.18)' : 'rgba(46,230,166,.16)'};color:${s.check === false ? C.orange : C.aquaDark};font-weight:800;font-size:${fs(36, 38)}px">${s.check === false ? '✕' : '✓'}</span>${it}</div>`).join('')}</div>`;
    case 'logo': return `<div style="${center};gap:${fs(34, 50)}px">
      <div class="pop" data-in="0.15">${logoMark(fs(400, 560))}</div>
      <div class="in" data-in="0.9" style="font-weight:800;font-size:${fs(64, 70)}px;letter-spacing:.08em">ON-CHAIN <span style="color:${C.aquaDark}">OPERATOR</span></div>
      <div class="in" data-in="1.4" style="font-size:${fs(46, 50)}px;color:rgba(255,255,255,.85);max-width:${fs(1400, 900)}px">${s.tagline}</div></div>`;
    case 'image': return `<div style="position:absolute;left:0;right:0;top:${fs(110, 330)}px;display:flex;flex-direction:column;align-items:center">
      <div class="in" data-in="0.15" style="font-size:${fs(30, 34)}px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:${C.aquaDark}">${s.eyebrow}</div>
      <div class="in" data-in="0.3" style="margin-top:${fs(28, 40)}px;width:${fs(1220, 1000)}px;border-radius:24px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.45);border:1px solid rgba(255,255,255,.16)">
        <img class="kb" src="${asset(s.src)}" style="display:block;width:100%;transform-origin:50% 45%"></div></div>`;
    case 'stats': return `<div style="${center};gap:${fs(40, 70)}px">
      ${s.stats.map(([a, b], i) => `<div class="in" data-in="${s.tItems[i]}"><div style="font-size:${fs(170, 200)}px;font-weight:800;line-height:1;color:${i === s.stats.length - 1 ? C.orange : '#fff'}">${a}</div><div style="font-size:${fs(44, 52)}px;color:rgba(255,255,255,.8);margin-top:10px">${b}</div></div>`).join('')}</div>`;
    case 'cta': return `<div style="${center};gap:${fs(38, 56)}px">
      <div class="pop" data-in="0.1">${logoMark(fs(300, 440))}</div>
      <div class="in" data-in="0.6" style="font-weight:800;font-size:${fs(60, 64)}px;letter-spacing:.06em">ON-CHAIN <span style="color:${C.aquaDark}">OPERATOR</span> PROGRAM</div>
      <div class="in" data-in="1.1" style="padding:${fs(28, 34)}px ${fs(70, 80)}px;border-radius:999px;background:linear-gradient(90deg,${C.aquaDark},${C.blueDark});color:${C.ink};font-weight:800;font-size:${fs(46, 54)}px">${s.button} →</div>
      <div class="in" data-in="1.5" style="font-size:${fs(32, 36)}px;color:rgba(255,255,255,.75)">${s.sub}</div></div>`;
  }
  throw new Error(`unknown scene type ${s.type}`);
}

function scenePage(s, W, H, dur, voStart, voDur) {
  const v = H > W;
  const chunks = captionChunks(s.cap || s.vo, v ? 5 : 8);
  const total = chunks.reduce((a, c) => a + c.length, 0);
  let acc = voStart;
  const caps = chunks.map(c => { const st = acc; acc += voDur * c.length / total; return [st, acc, c]; });
  return `<!doctype html><html><head><meta charset="utf-8">
  ${[400, 500, 600, 700, 800].map(x => `<link rel="stylesheet" href="${FONT('inter', x)}">`).join('')}
  <style>${BASE_CSS}
    #root { width:${W}px; height:${H}px; }
    .cap { position:absolute; left:50%; bottom:${v ? 250 : 120}px; transform:translateX(-50%); max-width:${v ? 940 : 1500}px; text-align:center;
      font-size:${v ? 50 : 44}px; font-weight:700; line-height:1.3; padding:14px 30px; border-radius:16px; background:rgba(5,15,28,.72); color:#fff; }
    .foot2 { position:absolute; left:${v ? 60 : 80}px; right:${v ? 60 : 80}px; bottom:${v ? 70 : 34}px; display:flex; justify-content:space-between; align-items:center; font-size:${v ? 22 : 18}px; color:rgba(255,255,255,.55); }
  </style></head><body>
  <div id="root" class="dark">${network(W, H, 40 + s.type.length, v ? 40 : 50, 0.13)}
    <div id="scene" style="position:absolute;inset:0">${sceneBody(s, W, H)}</div>
    <div class="cap" id="cap"></div>
    <div class="foot2"><div style="transform:scale(${v ? 0.9 : 0.75});transform-origin:left center">${wordmark(16)}</div><span>${v ? '' : DISCLAIMER}</span></div>
  </div>
  <script>
    const DUR = ${dur}, CAPS = ${JSON.stringify(caps)};
    const ease = x => x <= 0 ? 0 : x >= 1 ? 1 : 1 - Math.pow(1 - x, 3);
    window.setTime = t => {
      const fade = Math.min(ease(t / 0.35), ease((DUR - t) / 0.3));
      document.getElementById('scene').style.opacity = fade;
      document.querySelectorAll('.in').forEach(el => { const p = ease((t - +el.dataset.in) / 0.55); el.style.opacity = p; el.style.transform = 'translateY(' + (1 - p) * 34 + 'px)'; });
      document.querySelectorAll('.pop').forEach(el => { const p = ease((t - +el.dataset.in) / 0.8); el.style.opacity = p; el.style.transform = 'scale(' + (0.82 + 0.18 * p) + ')'; el.style.filter = 'drop-shadow(0 0 ' + (40 * p) + 'px rgba(46,230,166,' + (0.35 * p) + '))'; });
      document.querySelectorAll('.strike').forEach(el => { el.style.transform = 'scaleX(' + ease((t - +el.dataset.in) / 0.45) + ')'; });
      document.querySelectorAll('.kb').forEach(el => { el.style.transform = 'scale(' + (1 + 0.06 * t / DUR) + ')'; });
      const c = CAPS.find(([a, b]) => t >= a && t < b);
      const cap = document.getElementById('cap');
      cap.textContent = c ? c[2] : ''; cap.style.opacity = c ? Math.min(fade, 1) : 0;
    };
  </script></body></html>`;
}

// Scene-type timing: place reveals at proportional points in the narration.
function planTimes(s, voStart, voDur) {
  const at = f => +(voStart + voDur * f).toFixed(2);
  if (s.type === 'strike') { s.tStrike = at(0.3); s.tAfter = at(0.55); }
  if (s.type === 'statement') s.tSub = at(s.subAt || 0.45);
  if (s.type === 'bullets' || s.type === 'stats') { const n = (s.items || s.stats).length; s.tItems = Array.from({ length: n }, (_, i) => at(0.06 + i * 0.5 / n)); }
}

function writeScripts(results) {
  let md = `# Video scripts: On-Chain Operator Program

Generated by \`export/build_video.js\` from \`export/videos.js\` (edit the scripts there, then rebuild).
Narration: Kokoro TTS, voice \`${VOICE}\` (offline, Apache-2.0 model). To use your own voice,
record the VO lines below and replace the audio track, or re-run with \`VOICE=am_michael\` etc.

Compliance: no income or return claims, no fake urgency, keys never requested, disclaimer on screen.
`;
  for (const { video, timeline, total } of results.filter(r => r.video.group !== 'lessons')) {
    md += `\n---\n\n## ${video.title}\n\nFile: \`video/${video.id}.mp4\` · ${video.size[0]}×${video.size[1]} · ${total.toFixed(1)}s · Use: ${video.use}\n\n| # | Time | Visual | Voice-over |\n|---|---|---|---|\n`;
    timeline.forEach((t, i) => {
      const s = video.scenes[i];
      const visual = { strike: `"${s.big}" struck out → "${s.after}"`, statement: (s.lines || []).join(' / '), bullets: `${s.title}: ${(s.items || []).join(' · ')}`,
        logo: `Logo reveal + "${s.tagline}"`, image: `${s.eyebrow}: \`${s.src}\``, stats: (s.stats || []).map(x => x.join(' ')).join(' · '), cta: `Logo + "${s.button}" button · ${s.sub}` }[s.type];
      md += `| ${i + 1} | ${t.start.toFixed(1)}–${(t.start + t.dur).toFixed(1)}s | ${visual} | ${s.cap || s.vo} |\n`;
    });
  }
  fs.writeFileSync(path.join(OUT, 'SCRIPTS.md'), md);
}

async function render(video, browser) {
  const [W, H] = video.size;
  const dir = path.join(WORK, video.id);
  fs.mkdirSync(dir, { recursive: true });
  const scenes = video.scenes.map((s, i) => ({ id: `s${String(i + 1).padStart(2, '0')}`, vo: s.vo }));
  fs.writeFileSync(path.join(dir, 'scenes.json'), JSON.stringify(scenes));
  execFileSync('python3', [path.join(__dirname, 'build_vo.py'), path.join(dir, 'scenes.json'), dir, VOICE], { stdio: 'inherit' });
  const durs = JSON.parse(fs.readFileSync(path.join(dir, 'durations.json')));

  // Timeline + narration track (silence-padded) built with ffmpeg.
  let start = 0; const timeline = [];
  for (const s of scenes) { const dur = LEAD_IN + durs[s.id] + TAIL; timeline.push({ start, dur, vo: durs[s.id] }); start += dur; }
  const total = start;
  if (total > (video.maxMinutes || 25) * 60) throw new Error(`${video.id} is ${(total / 60).toFixed(1)} min, over the ${video.maxMinutes || 25}-minute cap: split it`);
  const inputs = scenes.flatMap(s => ['-i', path.join(dir, `${s.id}.wav`)]);
  const delays = scenes.map((s, i) => `[${i}:a]adelay=${Math.round((timeline[i].start + LEAD_IN) * 1000)}|${Math.round((timeline[i].start + LEAD_IN) * 1000)}[a${i}]`).join(';');
  const mix = `${delays};${scenes.map((_, i) => `[a${i}]`).join('')}amix=inputs=${scenes.length}:normalize=0,apad=whole_dur=${total.toFixed(3)},loudnorm=I=-16:TP=-1.5[out]`;
  const audio = path.join(dir, 'narration.m4a');
  execFileSync(FFMPEG, ['-y', '-loglevel', 'error', ...inputs, '-filter_complex', mix, '-map', '[out]', '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', audio]);

  const mp4 = path.join(OUT, `${video.id}.mp4`);
  const ff = spawn(FFMPEG, ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-i', audio,
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-shortest', '-movflags', '+faststart', mp4], { stdio: ['pipe', 'inherit', 'inherit'] });
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  for (let i = 0; i < video.scenes.length; i++) {
    const s = video.scenes[i], t = timeline[i];
    planTimes(s, LEAD_IN, t.vo);
    const file = path.join(dir, `${scenes[i].id}.html`);
    fs.writeFileSync(file, scenePage(s, W, H, t.dur, LEAD_IN, t.vo));
    await page.goto(`file://${file}`);
    await page.evaluate(() => document.fonts.ready);
    await page.evaluate(() => Promise.all([...document.images].map(im => im.complete ? 0 : new Promise(r => { im.onload = im.onerror = r; }))));
    const frames = Math.round(t.dur * FPS);
    for (let f = 0; f < frames; f++) {
      await page.evaluate(x => window.setTime(x), f / FPS);
      const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
  }
  ff.stdin.end();
  await new Promise((res, rej) => ff.on('close', code => (code ? rej(new Error(`ffmpeg exit ${code}`)) : res())));
  await page.close();
  console.log(`wrote video/${video.id}.mp4 (${total.toFixed(1)}s)`);
  return { video, timeline, total };
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const only = process.argv[2];
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const results = [];
  // No argument: core videos only (VSLs, welcome, module intros). 'lessons' renders every lesson video.
  for (const v of VIDEOS) {
    const pick = only ? (v.id === only || v.group === only) : v.group !== 'lessons';
    if (pick) results.push(await render(v, browser));
  }
  await browser.close();
  if (!only) writeScripts(results);
  else console.log('(SCRIPTS.md only regenerates on a full build)');
})();
