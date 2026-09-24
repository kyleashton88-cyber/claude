// Render the VSLs, welcome, module intros and lesson videos.
//
// Voice:  build_vo.py (Kokoro, sentence by sentence, measured pauses) -> per-scene
//         clips + sentence timings. Mixed and mastered here: high-pass, de-ess,
//         compression, presence EQ, -16 LUFS. Marketing videos get an ambient
//         music bed that ducks under the voice (sidechain).
// Motion: Chromium renders every frame deterministically via window.setTime(t).
//         Captions, bullet reveals, highlights, counters and callouts are driven
//         by the real sentence timings, so the screen moves with the voice.
// Output: ../video/<id>.mp4, thumbs/<id>.jpg, captions/<id>.vtt, chapters/<id>.txt,
//         SCRIPTS.md (core videos).
// Usage:  node build_video.js                 core videos (VSLs, welcome, module intros)
//         node build_video.js lessons         every lesson video
//         node build_video.js id1,id2         specific videos
//         node build_video.js --thumbs-only   thumbnails only
const fs = require('fs');
const path = require('path');
const { spawn, execFileSync } = require('child_process');
const { chromium } = require('playwright-core');
const { C, FONT, BASE_CSS, icon, logoMark, wordmark, DISCLAIMER } = require('./build_images.js');
const { VIDEOS: CORE } = require('./videos.js');

// Extra specs as JSON under ../video-scripts/** (lessons, hand-written gold scripts).
const SCRIPT_DIR = path.resolve(__dirname, '..', 'video-scripts');
const walk = d => (fs.existsSync(d) ? fs.readdirSync(d, { withFileTypes: true }).flatMap(e => (e.isDirectory() ? walk(path.join(d, e.name)) : e.name.endsWith('.json') ? [path.join(d, e.name)] : [])) : []);
const VIDEOS = [...CORE, ...walk(SCRIPT_DIR).sort().map(f => JSON.parse(fs.readFileSync(f, 'utf8')))];
{ const ids = new Set(); for (const v of VIDEOS) { if (ids.has(v.id)) throw new Error(`duplicate video id ${v.id}`); ids.add(v.id); } }

const FPS = 30;
const LEAD_IN = 0.55, TAIL = 0.75;
const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'video');
const WORK = path.join(__dirname, '.render', 'video');
const FFMPEG = process.env.FFMPEG || execFileSync('python3', ['-c', 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())']).toString().trim();
const VOICE = process.env.VOICE || 'af_heart';
const CHROME = process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

const asset = rel => `file://${path.join(ROOT, rel)}`;
const esc = s => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const fmtTime = (s, ms) => { const h = Math.floor(s / 3600), m = Math.floor(s / 60) % 60, x = s % 60;
  return ms ? `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${x.toFixed(3).padStart(6, '0')}` : `${h ? h + ':' : ''}${h ? String(m).padStart(2, '0') : m}:${String(Math.floor(x)).padStart(2, '0')}`; };

// ------------------------------------------------------------------ text sync
const STOP = new Set('the a an and or of to in on for with your you is are be it its this that at by as from into what how why when not no can will than then them they their our we'.split(' '));
const norm = s => String(s).toLowerCase().replace(/(?:\b[a-z]\.){2,}/g, m => m.replace(/\./g, '')).replace(/[^a-z0-9%$ ]+/g, ' ');
const tokens = s => norm(s).split(/\s+/).filter(w => w.length > 2 && !STOP.has(w));

// Each item's reveal time = start of the first sentence (after the previous
// item's) that shares the most words with it. Unmatched items interpolate.
function syncItems(texts, sents, voStart, voDur, explicit) {
  const n = texts.length;
  let idx = new Array(n).fill(null);
  if (explicit) idx = explicit.map(i => Math.min(i, sents.length - 1));
  else {
    let cur = 0;
    texts.forEach((txt, i) => {
      const tk = new Set(tokens(txt));
      let best = -1, bj = null;
      for (let j = cur; j < sents.length; j++) {
        const sc = tokens(sents[j][2]).filter(w => tk.has(w)).length;
        if (sc > best && sc > 0) { best = sc; bj = j; }
      }
      if (bj !== null) { idx[i] = bj; cur = sents.length - (bj + 1) >= n - i - 1 ? bj + 1 : bj; }
    });
  }
  const t = idx.map(j => (j === null ? null : voStart + Math.max(0, sents[j][0] - 0.12)));
  for (let i = 0; i < n; i++) if (t[i] === null) {
    const prev = i ? t[i - 1] : voStart + 0.1;
    let k = i + 1; while (k < n && t[k] === null) k++;
    const next = k < n ? t[k] : voStart + voDur * 0.8;
    t[i] = prev + (next - prev) * (1 / (k - i + 1)) * (i ? 1 : 0.3);
  }
  for (let i = 1; i < n; i++) t[i] = Math.max(t[i], t[i - 1] + 0.25);
  const out = t.map((a, i) => [a, i < n - 1 ? t[i + 1] : voStart + voDur]);
  return out.map(([a, b]) => [+a.toFixed(3), +b.toFixed(3)]);
}

// Caption cues: written captions aligned to spoken sentences, then split into
// readable chunks; each word carries its own highlight time.
function splitWritten(text) {
  return String(text).replace(/\s+/g, ' ').trim()
    .split(/(?<=[.!?…])\s+(?=[A-Z0-9"'$(])/).filter(Boolean);
}
function captionCues(scene, sents, voStart, maxWords) {
  const written = scene.cap || scene.vo.replace(/\[\[pause [\d.]+\]\]/g, ' ');
  let groups = splitWritten(written);
  if (groups.length > sents.length) {            // merge written sentences to match spoken ones
    const wc = x => x.split(/\s+/).filter(Boolean).length, merged = []; let k = 0;
    sents.forEach(([, , said], i) => {
      if (i === sents.length - 1) { merged.push(groups.slice(k).join(' ')); return; }
      const target = wc(said); let acc = groups[k] || ''; k++;
      while (k < groups.length && groups.length - k > sents.length - i - 1 && Math.abs(wc(acc + ' ' + groups[k]) - target) < Math.abs(wc(acc) - target)) acc += ' ' + groups[k++];
      merged.push(acc);
    });
    groups = merged;
  }
  if (groups.length !== sents.length) {           // proportional re-alignment
    const words = written.replace(/\s+/g, ' ').trim().split(' ');
    const w = sents.map(s => s[1] - s[0]), tot = w.reduce((a, b) => a + b, 0) || 1;
    groups = []; let k = 0;
    sents.forEach((s, i) => { const take = i === sents.length - 1 ? words.length - k : Math.round(words.length * w[i] / tot);
      groups.push(words.slice(k, k + take).join(' ')); k += take; });
  }
  const cues = [];
  sents.forEach(([a, b], i) => {
    const words = (groups[i] || '').split(' ').filter(Boolean);
    if (!words.length) return;
    const nChunks = Math.ceil(words.length / maxWords), per = Math.ceil(words.length / nChunks);
    const total = words.join(' ').length;
    let t = voStart + a; const dur = b - a;
    for (let c = 0; c < nChunks; c++) {
      const cw = words.slice(c * per, (c + 1) * per);
      const len = cw.join(' ').length + (c < nChunks - 1 ? 1 : 0);
      const cd = dur * len / total;
      let wt = t; const wordTimes = cw.map(w => { const x = wt; wt += cd * (w.length + 1) / (len + 1); return +x.toFixed(3); });
      cues.push({ a: +t.toFixed(3), b: +(t + cd).toFixed(3), words: cw, wt: wordTimes });
      t += cd;
    }
  });
  // hold each cue until the next one starts (no flicker in short pauses)
  for (let i = 0; i < cues.length - 1; i++) if (cues[i + 1].a - cues[i].b < 0.6) cues[i].b = cues[i + 1].a;
  return cues;
}

// Numbers in stats animate from 0 with the same formatting.
function counter(str) {
  const m = String(str).match(/^([^\d-]*)(-?[\d,]*\.?\d+)(.*)$/);
  if (!m) return null;
  const dec = (m[2].split('.')[1] || '').length;
  return { pre: m[1], val: parseFloat(m[2].replace(/,/g, '')), dec, comma: m[2].includes(','), post: m[3] };
}

// ------------------------------------------------------------------ scenes
function sceneBody(s, W, H, T) {
  const v = H > W, fs = (a, b) => (v ? b : a);
  const center = `position:absolute;inset:${fs(90, 200)}px 0 ${fs(210, 420)}px 0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center`;
  const item = (i, html, extra = '') => `<div class="it" data-a="${T.items[i][0]}" data-b="${T.items[i][1]}" style="${extra}">${html}</div>`;
  const title = (txt, extra = '') => `<div class="in" data-in="${T.v0}" style="font-size:${fs(70, 76)}px;font-weight:800;letter-spacing:-.02em;line-height:1.08;${extra}">${esc(txt)}</div>`;
  switch (s.type) {
    case 'title': return `<div style="position:absolute;left:${fs(170, 90)}px;right:${fs(170, 90)}px;top:0;bottom:${fs(210, 420)}px;display:flex;flex-direction:column;justify-content:center">
      <div class="in" data-in="${T.v0}" style="display:flex;align-items:center;gap:18px;font-size:${fs(28, 32)}px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:${C.aquaDark}">
        <span class="bar" data-in="${T.v0}" style="display:block;width:70px;height:4px;border-radius:2px;background:${C.aquaDark};transform-origin:left"></span>${esc(s.eyebrow)}</div>
      <div style="display:flex;align-items:flex-end;gap:${fs(50, 30)}px;margin-top:${fs(34, 40)}px">
        ${s.num ? `<div class="pop" data-in="${T.v0 + 0.15}" style="font-size:${fs(260, 200)}px;font-weight:800;line-height:.82;letter-spacing:-.05em;background:linear-gradient(135deg,${C.aquaDark},${C.blueDark});-webkit-background-clip:text;color:transparent">${esc(s.num)}</div>` : ''}
        <div class="in" data-in="${T.v0 + 0.35}" style="font-size:${fs(84, 80)}px;font-weight:800;letter-spacing:-.025em;line-height:1.04;max-width:${fs(1150, 900)}px">${esc(s.title)}</div></div>
      ${s.sub ? `<div class="in" data-in="${T.v0 + 0.8}" style="margin-top:${fs(44, 50)}px;font-size:${fs(38, 42)}px;line-height:1.4;color:rgba(255,255,255,.78);max-width:${fs(1350, 900)}px">${esc(s.sub)}</div>` : ''}
      ${s.src ? `<div class="in" data-in="${T.v0 + 1.1}" style="margin-top:${fs(50, 60)}px;width:${fs(640, 800)}px;border-radius:18px;overflow:hidden;border:1px solid rgba(255,255,255,.14);box-shadow:0 20px 60px rgba(0,0,0,.4)"><img src="${asset(s.src)}" style="display:block;width:100%"></div>` : ''}</div>`;
    case 'strike': return `<div style="${center};gap:${fs(40, 60)}px">
      <div class="in" data-in="${T.v0}" style="position:relative;font-size:${fs(230, 200)}px;font-weight:800;letter-spacing:-.03em">${esc(s.big)}
        <div class="strike" data-in="${T.strike}" style="position:absolute;left:-4%;top:52%;height:${fs(18, 16)}px;width:108%;background:${C.orange};border-radius:9px;transform-origin:left center;transform:scaleX(0)"></div></div>
      <div class="in" data-in="${T.after}" style="font-size:${fs(72, 76)}px;font-weight:800;color:${C.aquaDark};max-width:${fs(1500, 900)}px">${esc(s.after)}</div></div>`;
    case 'statement': return `<div style="${center};padding:0 ${fs(160, 80)}px">
      ${s.kicker ? `<div class="in" data-in="${T.v0}" style="font-size:${fs(28, 32)}px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:${C.aquaDark};margin-bottom:28px">${esc(s.kicker)}</div>` : ''}
      ${s.lines.map((l, i) => `<div class="in" data-in="${(T.lines || [])[i] ?? T.v0 + i * 0.7}" style="font-size:${fs(s.lines.join('').length > 70 ? 76 : 100, 88)}px;font-weight:800;line-height:1.1;letter-spacing:-.02em;${i ? `color:${C.aquaDark}` : ''}">${esc(l)}</div>`).join('')}
      ${s.sub ? `<div class="in" data-in="${T.sub}" style="font-size:${fs(40, 44)}px;color:rgba(255,255,255,.82);margin-top:${fs(40, 50)}px;max-width:${fs(1350, 900)}px;line-height:1.42">${esc(s.sub)}</div>` : ''}</div>`;
    case 'bullets': {
      const n = s.items.length, compact = s.compact || n > 5;
      const size = compact ? (n > 6 ? 34 : 40) : fs(46, 50);
      const mark = s.check === false ? ['rgba(235,104,52,.18)', C.orange, '✕'] : s.numbered ? ['rgba(46,230,166,.16)', C.aquaDark, null] : ['rgba(46,230,166,.16)', C.aquaDark, '✓'];
      return `<div style="position:absolute;left:${fs(190, 90)}px;right:${fs(190, 90)}px;top:${fs(compact ? 130 : 150, 400)}px">
        ${title(s.title)}
        <div style="display:grid;grid-template-columns:${compact && n > 5 && !v ? '1fr 1fr' : '1fr'};gap:${compact ? '20px 56px' : fs('26px', '44px')};margin-top:${compact ? 40 : 46}px">
        ${s.items.map((it, i) => item(i, `<span class="dot" style="flex:none;width:${size * 1.35}px;height:${size * 1.35}px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:${mark[0]};color:${mark[1]};font-weight:800;font-size:${size * 0.72}px">${mark[2] || i + 1}</span><span>${esc(it)}</span>`,
          `display:flex;align-items:center;gap:${size * 0.55}px;font-size:${size}px;line-height:1.25;color:#fff;padding:${compact ? 8 : 12}px 22px;border-radius:18px`)).join('')}</div></div>`;
    }
    case 'pillars': {
      const n = s.items.length;
      return `<div style="position:absolute;left:150px;right:150px;top:140px">
        ${title(s.title, 'text-align:center')}
        <div style="display:grid;grid-template-columns:repeat(${n},1fr);gap:34px;margin-top:64px">
        ${s.items.map((p, i) => item(i, `<div style="width:92px;height:92px;border-radius:24px;display:flex;align-items:center;justify-content:center;background:rgba(46,230,166,.12);border:1px solid rgba(46,230,166,.35)">${icon(p.icon || 'check', 50, C.aquaDark, 1.7)}</div>
          <div style="font-size:${n > 3 ? 38 : 44}px;font-weight:800;margin-top:30px;letter-spacing:-.01em">${esc(p.title)}</div>
          <div style="font-size:${n > 3 ? 27 : 30}px;line-height:1.45;color:rgba(255,255,255,.75);margin-top:16px">${esc(p.text || '')}</div>`,
          'padding:44px 38px;border-radius:28px;background:linear-gradient(180deg,rgba(255,255,255,.07),rgba(255,255,255,.025));border:1px solid rgba(255,255,255,.13);min-height:430px')).join('')}</div></div>`;
    }
    case 'compare': {
      const col = (side, off) => {
        const tone = side.tone === 'bad' ? C.orange : side.tone === 'good' ? C.aquaDark : C.blueDark;
        return `<div class="in" data-in="${T.items[off][0] - 0.2}" style="flex:1;padding:44px 48px;border-radius:28px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.13);border-top:6px solid ${tone}">
          <div style="font-size:30px;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:${tone}">${esc(side.label)}</div>
          ${side.items.map((x, i) => item(off + i, `<span style="color:${tone};font-weight:800;flex:none">${side.tone === 'bad' ? '✕' : side.tone === 'good' ? '✓' : '•'}</span><span>${esc(x)}</span>`,
            'display:flex;gap:20px;font-size:36px;line-height:1.3;margin-top:26px;padding:6px 12px;border-radius:14px')).join('')}</div>`;
      };
      return `<div style="position:absolute;left:150px;right:150px;top:140px">${title(s.title, 'text-align:center')}
        <div style="display:flex;gap:44px;margin-top:56px">${col(s.left, 0)}${col(s.right, s.left.items.length)}</div></div>`;
    }
    case 'steps': return `<div style="position:absolute;left:170px;right:170px;top:130px">
      ${title(s.title)}
      <div style="margin-top:44px;padding:40px 50px;border-radius:26px;background:rgba(3,12,24,.55);border:1px solid rgba(255,255,255,.12)">
      ${s.steps.map((st, i) => item(i, `<span style="flex:none;width:52px;color:${C.aquaDark};font-weight:700">${i + 1}</span><span>${esc(st)}</span>`,
        `display:flex;gap:18px;font-family:'JetBrains Mono',monospace;font-size:${s.steps.length > 5 ? 32 : 37}px;line-height:1.35;padding:10px 16px;border-radius:12px`)).join('')}</div>
      ${s.result ? `<div class="pop" data-in="${T.result}" style="display:inline-block;margin-top:34px;padding:22px 40px;border-radius:18px;background:linear-gradient(90deg,${C.aquaDark},${C.blueDark});color:${C.ink};font-weight:800;font-size:44px">${esc(s.result)}</div>` : ''}</div>`;
    case 'quiz': return `<div style="${center};padding:0 180px">
      <div class="in" data-in="${T.v0}" style="display:flex;align-items:center;gap:22px;font-size:30px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:${C.aquaDark}">Quiz · ${s.n} of ${s.of}</div>
      <div class="in" data-in="${T.v0 + 0.2}" style="font-size:${s.q.length > 90 ? 58 : 70}px;font-weight:800;line-height:1.15;letter-spacing:-.015em;margin-top:34px;max-width:1450px">${esc(s.q)}</div>
      <div style="position:relative;height:250px;margin-top:40px;width:1400px">
        <div class="ring" data-a="${T.think[0]}" data-b="${T.think[1]}" style="position:absolute;left:50%;top:10px;transform:translateX(-50%)">
          <svg width="150" height="150" viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="none" stroke="rgba(255,255,255,.12)" stroke-width="7"/>
          <circle class="arc" cx="50" cy="50" r="44" fill="none" stroke="${C.aquaDark}" stroke-width="7" stroke-linecap="round" pathLength="1" stroke-dasharray="1" transform="rotate(-90 50 50)"/></svg>
          <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:700;color:rgba(255,255,255,.75)">think</div></div>
        <div class="pop" data-in="${T.answer}" style="position:absolute;left:0;right:0;top:0;display:flex;flex-direction:column;align-items:center">
          <div style="padding:30px 48px;border-radius:24px;background:rgba(46,230,166,.12);border:2px solid ${C.aquaDark};font-size:${s.a.length > 110 ? 36 : 42}px;line-height:1.35;max-width:1400px"><b style="color:${C.aquaDark}">Answer · </b>${esc(s.a)}</div></div></div></div>`;
    case 'logo': return `<div style="${center};gap:${fs(34, 50)}px">
      <div class="pop draw" data-in="${T.v0 - 0.3}">${logoMark(fs(400, 560))}</div>
      <div class="in" data-in="${T.v0 + 0.6}" style="font-weight:800;font-size:${fs(64, 70)}px;letter-spacing:.08em">ON-CHAIN <span style="color:${C.aquaDark}">OPERATOR</span></div>
      <div class="in" data-in="${T.v0 + 1.1}" style="font-size:${fs(46, 50)}px;color:rgba(255,255,255,.85);max-width:${fs(1400, 900)}px">${esc(s.tagline)}</div></div>`;
    case 'image': {
      const wide = s.wide ? fs(1560, 1000) : fs(1300, 1000);
      return `<div style="position:absolute;left:0;right:0;top:${fs(96, 330)}px;display:flex;flex-direction:column;align-items:center">
      <div class="in" data-in="${T.v0 - 0.2}" style="font-size:${fs(28, 34)}px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:${C.aquaDark}">${esc(s.eyebrow)}</div>
      <div class="wipe" data-in="${T.v0}" style="position:relative;margin-top:${fs(26, 40)}px;max-width:${wide}px;border-radius:24px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.45);border:1px solid rgba(255,255,255,.16)">
        <img class="kb" src="${asset(s.src)}" style="display:block;max-width:${wide}px;max-height:${fs(670, 1100)}px;width:auto;height:auto" data-zoom='${JSON.stringify(s.zoom ? { ...s.zoom, t: T.zoom } : null)}'>
        ${(s.callouts || []).map((c, i) => `<div class="call" data-in="${T.callouts[i]}" style="position:absolute;left:${c.x * 100}%;top:${c.y * 100}%;transform:translate(-50%,-50%)">
          <div class="pulse" style="width:74px;height:74px;border-radius:50%;border:5px solid ${C.orange};box-shadow:0 0 0 6px rgba(235,104,52,.25)"></div>
          ${c.text ? `<div style="position:absolute;${c.below ? 'top:88px' : 'bottom:88px'};left:50%;transform:translateX(-50%);white-space:nowrap;padding:10px 20px;border-radius:12px;background:${C.orange};color:#fff;font-weight:800;font-size:26px">${esc(c.text)}</div>` : ''}</div>`).join('')}
      </div></div>`;
    }
    case 'stats': return `<div style="${center};${v ? 'flex-direction:column' : 'flex-direction:row'};gap:${fs(90, 70)}px">
      ${s.stats.map(([a, b], i) => { const c = counter(a); return item(i, `<div class="num" data-count='${JSON.stringify(c)}' style="font-size:${fs(170, 200)}px;font-weight:800;line-height:1;color:${i === s.stats.length - 1 && s.lastAccent !== false ? C.orange : '#fff'}">${esc(a)}</div>
        <div style="font-size:${fs(40, 52)}px;color:rgba(255,255,255,.8);margin-top:14px">${esc(b)}</div>`, 'text-align:center'); }).join('')}</div>`;
    case 'cta': return `<div style="${center};gap:${fs(38, 56)}px">
      <div class="pop draw" data-in="${T.v0 - 0.3}">${logoMark(fs(300, 440))}</div>
      <div class="in" data-in="${T.v0 + 0.3}" style="font-weight:800;font-size:${fs(60, 64)}px;letter-spacing:.06em">ON-CHAIN <span style="color:${C.aquaDark}">OPERATOR</span> PROGRAM</div>
      <div class="pop btn" data-in="${T.v0 + 0.8}" style="padding:${fs(28, 34)}px ${fs(70, 80)}px;border-radius:999px;background:linear-gradient(90deg,${C.aquaDark},${C.blueDark});color:${C.ink};font-weight:800;font-size:${fs(46, 54)}px">${esc(s.button)} →</div>
      <div class="in" data-in="${T.v0 + 1.2}" style="font-size:${fs(32, 36)}px;color:rgba(255,255,255,.75)">${esc(s.sub)}</div></div>`;
  }
  throw new Error(`unknown scene type ${s.type}`);
}

// Scene timing plan from sentence marks (seconds relative to the scene start).
function planTimes(s, sents, voStart, voDur) {
  const at = f => +(voStart + voDur * f).toFixed(3);
  const sentAt = (j, fb) => (j != null && sents[j] ? +(voStart + Math.max(0, sents[j][0] - 0.1)).toFixed(3) : fb);
  const T = { v0: voStart + 0.05, items: [] };
  const byText = (re, fb) => { const j = sents.findIndex(x => re.test(x[2])); return j >= 0 ? sentAt(j, fb) : fb; };
  switch (s.type) {
    case 'strike': T.strike = sentAt(s.strikeAt ?? (sents.length > 1 ? 1 : null), at(0.3)); T.after = Math.max(T.strike + 0.5, sentAt(s.afterAt ?? (sents.length > 2 ? 2 : null), at(0.55))); break;
    case 'statement':
      if (s.lineAt) T.lines = s.lineAt.map(j => sentAt(j, T.v0));
      T.sub = s.subAt != null && s.subAt < 1 ? at(s.subAt) : sentAt(s.subAt ?? (sents.length > 1 ? 1 : null), at(0.4)); break;
    case 'bullets': case 'steps': case 'stats': case 'pillars': {
      const texts = s.type === 'stats' ? s.stats.map(x => x.join(' ')) : s.type === 'pillars' ? s.items.map(p => `${p.title} ${p.text || ''}`) : (s.items || s.steps);
      T.items = syncItems(texts, sents, voStart, voDur, s.at);
      if (s.type === 'steps') T.result = s.resultAt != null ? sentAt(s.resultAt, at(0.85)) : Math.max(T.items[T.items.length - 1][0] + 0.8, sentAt(sents.length - 1, at(0.85)));
      break;
    }
    case 'compare': T.items = syncItems([...s.left.items, ...s.right.items], sents, voStart, voDur, s.at); break;
    case 'quiz': { const a = byText(/^(the )?answer/i, at(0.7)); const q = sents.findIndex(x => /^(the )?answer/i.test(x[2]));
      T.answer = a; T.think = [q > 0 ? voStart + sents[q - 1][1] : a - 3, a]; break; }
    case 'image': T.callouts = (s.callouts || []).map((c, i) => sentAt(c.at ?? Math.min(i + 1, sents.length - 1), at(0.3 + i * 0.2)));
      if (s.zoom) T.zoom = sentAt(s.zoom.at ?? Math.min(1, sents.length - 1), at(0.45)); break;
  }
  return T;
}

// ------------------------------------------------------------------ page
function scenePage(video, s, W, H, sc) {
  const v = H > W, minimal = video.chrome === 'minimal';
  return `<!doctype html><html><head><meta charset="utf-8">
  ${[400, 500, 600, 700, 800].map(x => `<link rel="stylesheet" href="${FONT('inter', x)}">`).join('')}
  <link rel="stylesheet" href="${FONT('jetbrains-mono', 500)}"><link rel="stylesheet" href="${FONT('jetbrains-mono', 700)}">
  <style>${BASE_CSS}
    #root { width:${W}px; height:${H}px; color:#fff; position:relative; overflow:hidden; background: radial-gradient(120% 90% at 85% 0%, #1d4a78 0%, ${C.navy} 38%, ${C.ink} 100%); }
    #bg { position:absolute; inset:0; }
    .glow { position:absolute; width:${W * 0.9}px; height:${W * 0.9}px; border-radius:50%; background: radial-gradient(circle, rgba(46,230,166,.10), rgba(46,230,166,0) 62%); pointer-events:none; }
    .vign { position:absolute; inset:0; background: radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(3,10,20,.55) 100%); }
    .cap { position:absolute; left:50%; bottom:${v ? 260 : 96}px; transform:translateX(-50%); max-width:${v ? 960 : 1560}px; text-align:center;
      font-size:${v ? 52 : 42}px; font-weight:700; line-height:1.28; padding:14px 30px 16px; border-radius:16px; background:rgba(4,13,26,.78); color:rgba(255,255,255,.62);
      box-shadow:0 10px 30px rgba(0,0,0,.25); letter-spacing:-.003em; }
    .cap .w.on { color:#fff; } .cap .w.now { color:${C.aquaDark}; }
    .foot2 { position:absolute; left:${v ? 60 : 72}px; right:${v ? 60 : 72}px; bottom:${v ? 80 : 26}px; display:flex; justify-content:space-between; align-items:center; font-size:${v ? 22 : 17}px; color:rgba(255,255,255,.5); }
    .top { position:absolute; left:${v ? 60 : 72}px; right:${v ? 60 : 72}px; top:${v ? 90 : 34}px; display:flex; justify-content:space-between; align-items:center; }
    .chip { display:flex; align-items:center; gap:14px; padding:9px 20px 9px 12px; border-radius:999px; background:rgba(255,255,255,.07); border:1px solid rgba(255,255,255,.12); font-size:21px; font-weight:600; color:rgba(255,255,255,.85); }
    .chip b { color:${C.aquaDark}; font-weight:700; }
    .prog { position:absolute; left:0; top:0; height:5px; background:linear-gradient(90deg,${C.aquaDark},${C.blueDark}); box-shadow:0 0 14px rgba(46,230,166,.6); }
    .progtrack { position:absolute; left:0; right:0; top:0; height:5px; background:rgba(255,255,255,.06); }
    .it { transition:none; }
  </style></head><body>
  <div id="root">
    <canvas id="bg" width="${W}" height="${H}"></canvas><div class="glow" id="glow"></div><div class="vign"></div>
    <div id="scene" style="position:absolute;inset:0">${sceneBody(s, W, H, sc.T)}</div>
    ${minimal ? '' : `<div class="progtrack"></div><div class="prog" id="prog"></div>
    <div class="top"><div class="chip" id="chip">${logoMark(34, { nodes: false })}<span><b>${esc(video.tag || '')}</b>${video.tag ? ' · ' : ''}<span id="chap"></span></span></div></div>`}
    <div class="cap" id="cap"></div>
    <div class="foot2"><div style="transform:scale(${v ? 0.9 : 0.72});transform-origin:left center">${wordmark(16)}</div><span>${v ? '' : DISCLAIMER}</span></div>
  </div>
  <script>
  const DUR = ${sc.dur}, T0 = ${sc.start}, TOTAL = ${sc.total}, CUES = ${JSON.stringify(sc.cues)}, CHAP = ${JSON.stringify(sc.chapter || '')}, VOEND = ${sc.voEnd}, W = ${W}, H = ${H}, NOHI = ${s.highlight === false};
  const ease = x => x <= 0 ? 0 : x >= 1 ? 1 : 1 - Math.pow(1 - x, 3);
  const easeIO = x => x <= 0 ? 0 : x >= 1 ? 1 : x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
  // --- living network background (continuous across scenes: uses global time)
  let seed = ${video.seed || 11}; const rnd = () => (seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296;
  const N = ${v ? 34 : 46}, P = Array.from({ length: N }, () => ({ x: rnd() * W, y: rnd() * H, ax: 30 + rnd() * 70, ay: 30 + rnd() * 70, wx: .05 + rnd() * .12, wy: .05 + rnd() * .12, px: rnd() * 6.3, py: rnd() * 6.3, big: rnd() < .18, teal: rnd() < .14 }));
  const ctx = document.getElementById('bg').getContext('2d');
  function drawBg(g) {
    ctx.clearRect(0, 0, W, H);
    const pts = P.map(p => [p.x + p.ax * Math.sin(g * p.wx + p.px), p.y + p.ay * Math.cos(g * p.wy + p.py)]);
    const R = W * 0.15, edges = [];
    for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) {
      const d = Math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1]);
      if (d < R) { const a = (1 - d / R) * .16; ctx.strokeStyle = 'rgba(127,178,255,' + a + ')'; ctx.lineWidth = 1.1; ctx.beginPath(); ctx.moveTo(pts[i][0], pts[i][1]); ctx.lineTo(pts[j][0], pts[j][1]); ctx.stroke(); edges.push([i, j, a]); }
    }
    // signal pulses travelling along edges (transactions moving through the network)
    edges.forEach(([i, j, a], k) => { if (k % 5) return; const f = (g * .35 + k * .137) % 1; const x = pts[i][0] + (pts[j][0] - pts[i][0]) * f, y = pts[i][1] + (pts[j][1] - pts[i][1]) * f;
      ctx.fillStyle = 'rgba(46,230,166,' + Math.min(.8, a * 5) + ')'; ctx.beginPath(); ctx.arc(x, y, 2.4, 0, 6.3); ctx.fill(); });
    pts.forEach(([x, y], i) => { const p = P[i]; ctx.fillStyle = p.teal ? 'rgba(46,230,166,.55)' : 'rgba(127,178,255,.38)'; ctx.beginPath(); ctx.arc(x, y, p.big ? 3.6 : 2.2, 0, 6.3); ctx.fill(); });
    const gl = document.getElementById('glow'); gl.style.left = (W * .55 + W * .18 * Math.sin(g * .05) - W * .45) + 'px'; gl.style.top = (H * .2 + H * .2 * Math.cos(g * .04) - W * .45) + 'px';
  }
  function draw(el, p) { el.querySelectorAll('circle,path').forEach(c => { if (c.getAttribute('stroke') === 'none' || !c.getAttribute('stroke')) return; c.setAttribute('pathLength', '1'); c.style.strokeDasharray = '1'; c.style.strokeDashoffset = String(1 - p); }); }
  window.setTime = t => {
    const g = T0 + t;
    drawBg(g);
    const inF = ease(t / .4), outF = ease((DUR - t) / .32), fade = Math.min(inF, outF);
    const sc = document.getElementById('scene'); sc.style.opacity = fade; sc.style.transform = 'translateY(' + ((1 - inF) * 18 - (1 - outF) * 14) + 'px)';
    document.querySelectorAll('.in').forEach(el => { const p = ease((t - +el.dataset.in) / .6); el.style.opacity = p; el.style.transform = 'translateY(' + (1 - p) * 34 + 'px)'; });
    document.querySelectorAll('.bar').forEach(el => { el.style.transform = 'scaleX(' + ease((t - +el.dataset.in) / .8) + ')'; });
    document.querySelectorAll('.pop').forEach(el => { const p = ease((t - +el.dataset.in) / .7); el.style.opacity = p; el.style.transform = 'scale(' + (.86 + .14 * p) + ')';
      if (el.classList.contains('draw')) { draw(el, easeIO((t - +el.dataset.in) / 1.6)); const glow = .3 + .12 * Math.sin(t * 2.2); el.style.filter = 'drop-shadow(0 0 ' + (46 * p) + 'px rgba(46,230,166,' + (glow * p) + '))'; }
      if (el.classList.contains('btn')) el.style.boxShadow = '0 0 ' + (30 + 16 * Math.sin(t * 3)) * p + 'px rgba(46,230,166,.45)'; });
    document.querySelectorAll('.strike').forEach(el => { el.style.transform = 'scaleX(' + ease((t - +el.dataset.in) / .45) + ')'; });
    // synced items: reveal, then highlight the one being spoken; all settle when narration ends
    const its = [...document.querySelectorAll('.it')];
    its.forEach(el => { const a = +el.dataset.a, b = +el.dataset.b, p = ease((t - a) / .55);
      const active = t >= a && t < b && t < VOEND && its.length > 1 && !NOHI && !el.querySelector('.num'), anyActive = !NOHI && its.some(e => t >= +e.dataset.a && t < +e.dataset.b && t < VOEND);
      el.style.opacity = p * (active || !anyActive ? 1 : .5); el.style.transform = 'translateX(' + (1 - p) * -30 + 'px)';
      el.style.background = active ? 'rgba(46,230,166,.09)' : 'transparent'; el.style.boxShadow = active ? 'inset 4px 0 0 ${C.aquaDark}' : 'none';
      const num = el.querySelector('.num'); if (num) { const c = JSON.parse(num.dataset.count); if (c) { const q = easeIO((t - a) / 1.3); let x = (c.val * q).toFixed(c.dec); if (c.comma) x = Number(x).toLocaleString('en-US', { minimumFractionDigits: c.dec, maximumFractionDigits: c.dec }); num.textContent = c.pre + x + c.post; } } });
    document.querySelectorAll('.wipe').forEach(el => { const p = easeIO((t - +el.dataset.in) / .9); el.style.clipPath = 'inset(0 ' + (100 - p * 100) + '% 0 0 round 24px)'; });
    document.querySelectorAll('.kb').forEach(el => { const z = JSON.parse(el.dataset.zoom || 'null'); let s = 1 + .045 * t / DUR, ox = 50, oy = 45;
      if (z) { const q = easeIO((t - z.t) / 1.4); s += (z.s - 1) * q; ox = 50 + (z.x * 100 - 50) * q; oy = 45 + (z.y * 100 - 45) * q; }
      el.style.transformOrigin = ox + '% ' + oy + '%'; el.style.transform = 'scale(' + s + ')'; });
    document.querySelectorAll('.call').forEach(el => { const p = ease((t - +el.dataset.in) / .5); el.style.opacity = p; const r = el.querySelector('.pulse'); r.style.transform = 'scale(' + (.6 + .4 * p + .06 * Math.sin((t - +el.dataset.in) * 5)) + ')'; });
    document.querySelectorAll('.ring').forEach(el => { const a = +el.dataset.a, b = +el.dataset.b, p = (t - a) / Math.max(.1, b - a);
      el.style.opacity = t < a - .2 ? 0 : t > b ? Math.max(0, 1 - (t - b) / .3) : 1; el.querySelector('.arc').style.strokeDashoffset = String(Math.min(1, Math.max(0, p))); });
    const prog = document.getElementById('prog'); if (prog) prog.style.width = (g / TOTAL * 100) + '%';
    const chap = document.getElementById('chap'); if (chap) chap.textContent = CHAP;
    const c = CUES.find(x => t >= x.a && t < x.b), cap = document.getElementById('cap');
    if (c) { cap.innerHTML = c.words.map((w, i) => '<span class="w' + (t >= c.wt[i] ? (i === c.words.length - 1 || t < c.wt[i + 1] ? ' on now' : ' on') : '') + '">' + w.replace(/</g, '&lt;') + '</span>').join(' '); cap.style.opacity = Math.min(1, ease((t - c.a) / .12) * 1.0) * outF; }
    else cap.style.opacity = 0;
  };
  </script></body></html>`;
}

// ------------------------------------------------------------------ thumbnail
function thumbPage(video) {
  const th = video.thumbnail || {};
  const t = th.title || video.title.replace(/^[^:]*:\s*/, '');
  const sub = th.subtitle || video.title.split(':')[0];
  return `<!doctype html><html><head><meta charset="utf-8">${[600, 800].map(x => `<link rel="stylesheet" href="${FONT('inter', x)}">`).join('')}
  <style>${BASE_CSS} #root{width:1280px;height:720px}</style></head><body><div id="root" class="dark">
  <div style="position:absolute;right:-60px;top:50%;transform:translateY(-50%);filter:drop-shadow(0 0 60px rgba(46,230,166,.45))">${logoMark(620)}</div>
  <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(11,31,51,.96) 0%,rgba(11,31,51,.82) 50%,rgba(11,31,51,0) 80%)"></div>
  <div style="position:absolute;left:70px;top:70px;right:520px;bottom:70px;display:flex;flex-direction:column;justify-content:center">
    <div style="display:inline-flex;align-self:flex-start;padding:10px 22px;border-radius:999px;background:${C.aquaDark};color:${C.ink};font-weight:800;font-size:26px;letter-spacing:.06em;text-transform:uppercase">${esc(sub)}</div>
    <div style="margin-top:30px;font-weight:800;font-size:${t.length > 26 ? 76 : 96}px;line-height:1.0;letter-spacing:-.035em;color:#fff">${esc(t)}</div>
    <div style="margin-top:34px;width:120px;height:8px;border-radius:4px;background:linear-gradient(90deg,${C.aquaDark},${C.blueDark})"></div></div>
  <div style="position:absolute;left:70px;bottom:40px;transform:scale(.8);transform-origin:left bottom">${wordmark(18)}</div>
  </div></body></html>`;
}

// ------------------------------------------------------------------ audio
function mixAudio(video, dir, scenes, timeline, total) {
  const inputs = scenes.flatMap(s => ['-i', path.join(dir, `${s.id}.wav`)]);
  const n = scenes.length;
  const delays = scenes.map((s, i) => { const d = Math.round((timeline[i].start + LEAD_IN) * 1000); return `[${i}:a]aresample=48000,adelay=${d}|${d}[a${i}]`; }).join(';');
  // Voice mastering: rumble cut, de-ess, gentle compression, presence, air.
  const master = 'highpass=f=75,deesser=i=0.3:m=0.5:f=0.5,acompressor=threshold=0.1:ratio=2.6:attack=6:release=180:makeup=1.8,equalizer=f=220:t=q:w=1:g=-1.5,equalizer=f=3400:t=q:w=1.1:g=2,equalizer=f=11000:t=h:w=0.7:g=1.5,alimiter=limit=0.95';
  let graph = `${delays};${scenes.map((_, i) => `[a${i}]`).join('')}amix=inputs=${n}:normalize=0,apad=whole_dur=${total.toFixed(3)},${master},pan=stereo|c0=c0|c1=c0`;
  const extra = [];
  if (video.music) {
    const bed = path.join(dir, 'music.wav');
    execFileSync('python3', [path.join(__dirname, 'build_vo.py'), 'music', String(total + 1), bed, String(video.seed || 3)], { stdio: 'inherit' });
    extra.push('-i', bed);
    graph += `,asplit=2[vo][key];[${n}:a]aresample=48000,volume=${video.musicLevel || 0.34},atrim=0:${total.toFixed(3)}[mus];[mus][key]sidechaincompress=threshold=0.025:ratio=9:attack=25:release=520[duck];[vo][duck]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[out]`;
  } else graph += ',loudnorm=I=-16:TP=-1.5:LRA=9[out]';
  const audio = path.join(dir, 'mix.m4a');
  execFileSync(FFMPEG, ['-y', '-loglevel', 'error', ...inputs, ...extra, '-filter_complex', graph, '-map', '[out]', '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', audio]);
  return audio;
}

// ------------------------------------------------------------------ render
function writeMeta(video, plan, total) {
  const vtt = ['WEBVTT', ''];
  plan.forEach(p => p.cues.forEach(c => vtt.push(`${fmtTime(p.start + c.a, true)} --> ${fmtTime(p.start + c.b, true)}`, c.words.join(' '), '')));
  const chapters = []; let last = null;
  plan.forEach(p => { if (p.chapter && p.chapter !== last) { chapters.push(`${fmtTime(p.start)} ${p.chapter}`); last = p.chapter; } });
  for (const d of ['captions', 'chapters', 'thumbs']) fs.mkdirSync(path.join(OUT, d), { recursive: true });
  fs.writeFileSync(path.join(OUT, 'captions', `${video.id}.vtt`), vtt.join('\n'));
  if (chapters.length > 1) fs.writeFileSync(path.join(OUT, 'chapters', `${video.id}.txt`), chapters.join('\n') + '\n');
  return chapters;
}

async function thumbnail(video, browser) {
  if (video.size[1] > video.size[0]) return;
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  const f = path.join(WORK, `thumb-${video.id}.html`);
  fs.mkdirSync(WORK, { recursive: true });
  fs.writeFileSync(f, thumbPage(video));
  await page.goto(`file://${f}`); await page.evaluate(() => document.fonts.ready);
  fs.mkdirSync(path.join(OUT, 'thumbs'), { recursive: true });
  await page.screenshot({ path: path.join(OUT, 'thumbs', `${video.id}.jpg`), type: 'jpeg', quality: 88 });
  await page.close();
}

async function render(video, browser) {
  if (process.env.SCENES) { const [x, y] = process.env.SCENES.split('-').map(Number); video = { ...video, id: `${video.id}-test`, scenes: video.scenes.slice(x - 1, y || x) }; }
  const [W, H] = video.size;
  const dir = path.join(WORK, video.id);
  fs.mkdirSync(dir, { recursive: true });
  const scenes = video.scenes.map((s, i) => ({ id: `s${String(i + 1).padStart(2, '0')}`, vo: s.vo, speed: s.speed || video.speed || 0.96 }));
  fs.writeFileSync(path.join(dir, 'scenes.json'), JSON.stringify(scenes));
  execFileSync('python3', [path.join(__dirname, 'build_vo.py'), path.join(dir, 'scenes.json'), dir, VOICE], { stdio: 'inherit' });
  const timings = JSON.parse(fs.readFileSync(path.join(dir, 'timings.json')));

  let start = 0; const timeline = [];
  video.scenes.forEach((s, i) => { const vo = timings[scenes[i].id].dur; const dur = LEAD_IN + vo + TAIL + (s.hold || 0); timeline.push({ start, dur, vo }); start += dur; });
  const total = start;
  if (total > (video.maxMinutes || 25) * 60) throw new Error(`${video.id} is ${(total / 60).toFixed(1)} min, over the ${video.maxMinutes || 25}-minute cap: split it`);

  let chapter = null;
  const plan = video.scenes.map((s, i) => {
    const t = timeline[i], sents = timings[scenes[i].id].sentences;
    if (s.chapter) chapter = s.chapter;
    return { ...t, total, chapter, voEnd: LEAD_IN + t.vo, T: planTimes(s, sents, LEAD_IN, t.vo), cues: captionCues(s, sents, LEAD_IN, H > W ? 5 : 9) };
  });
  const audio = mixAudio(video, dir, scenes, timeline, total);

  const mp4 = path.join(OUT, `${video.id}.mp4`);
  const ff = spawn(FFMPEG, ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-i', audio,
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-tune', 'animation', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-shortest', '-movflags', '+faststart', mp4], { stdio: ['pipe', 'inherit', 'inherit'] });
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  for (let i = 0; i < video.scenes.length; i++) {
    const s = video.scenes[i], p = plan[i];
    const file = path.join(dir, `${scenes[i].id}.html`);
    fs.writeFileSync(file, scenePage(video, s, W, H, p));
    await page.goto(`file://${file}`);
    await page.evaluate(() => document.fonts.ready);
    await page.evaluate(() => Promise.all([...document.images].map(im => im.complete ? 0 : new Promise(r => { im.onload = im.onerror = r; }))));
    const frames = Math.round(p.dur * FPS);
    for (let f = 0; f < frames; f++) {
      await page.evaluate(x => window.setTime(x), f / FPS);
      const buf = await page.screenshot({ type: 'jpeg', quality: 93 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
  }
  ff.stdin.end();
  await new Promise((res, rej) => ff.on('close', code => (code ? rej(new Error(`ffmpeg exit ${code}`)) : res())));
  await page.close();
  const chapters = writeMeta(video, plan, total);
  await thumbnail(video, browser);
  console.log(`wrote video/${video.id}.mp4 (${fmtTime(total)}, ${video.scenes.length} scenes, ${chapters.length} chapters)`);
  return { video, timeline, total };
}

// ------------------------------------------------------------------ SCRIPTS.md
function visual(s) {
  const V = {
    strike: () => `"${s.big}" struck out → "${s.after}"`, statement: () => (s.lines || []).join(' / ') + (s.sub ? ` — ${s.sub}` : ''),
    bullets: () => `${s.title}: ${(s.items || []).join(' · ')}`, logo: () => `Logo draws on + "${s.tagline}"`,
    image: () => `${s.eyebrow}: \`${s.src}\`${s.callouts ? ' + callouts' : ''}${s.zoom ? ' + zoom' : ''}`,
    stats: () => (s.stats || []).map(x => x.join(' ')).join(' · ') + ' (counting up)', cta: () => `Logo + "${s.button}" button · ${s.sub}`,
    title: () => `Title card: ${s.num || ''} ${s.title}`, pillars: () => `${s.title}: ${(s.items || []).map(p => p.title).join(' · ')}`,
    compare: () => `${s.title}: ${s.left.label} (${s.left.items.join(', ')}) vs ${s.right.label} (${s.right.items.join(', ')})`,
    steps: () => `${s.title}: ${(s.steps || []).join(' → ')}${s.result ? ` ⇒ ${s.result}` : ''}`, quiz: () => `Quiz: ${s.q} → ${s.a}`,
  };
  return V[s.type]();
}
function writeScripts(results) {
  let md = `# Video scripts: On-Chain Operator Program

Generated by \`export/build_video.js\` from \`export/videos.js\` (edit the scripts there, then rebuild).

**Voice:** Kokoro TTS, voice \`${VOICE}\`, synthesised sentence by sentence with measured pauses, then mastered
(high-pass, de-ess, compression, presence EQ, −16 LUFS). Marketing videos carry an original ambient music bed
that ducks under the voice. To use a human voice, record the VO column line by line and replace the audio track,
or re-run with \`VOICE=am_michael\` etc.
**Motion:** captions follow the voice word by word; bullets and steps reveal and highlight as they're spoken;
living node-network background, progress bar and chapter tag. Every video also gets \`thumbs/<id>.jpg\`,
\`captions/<id>.vtt\` and \`chapters/<id>.txt\`.

Compliance: no income or return claims, no fake urgency, keys never requested, disclaimer on screen.
`;
  for (const { video, timeline, total } of results.filter(r => r.video.group !== 'lessons')) {
    md += `\n---\n\n## ${video.title}\n\nFile: \`video/${video.id}.mp4\` · ${video.size[0]}×${video.size[1]} · ${fmtTime(total)} · Use: ${video.use}\n\n| # | Time | Visual | Voice-over |\n|---|---|---|---|\n`;
    timeline.forEach((t, i) => { const s = video.scenes[i];
      md += `| ${i + 1} | ${fmtTime(t.start)}–${fmtTime(t.start + t.dur)} | ${visual(s).replace(/\|/g, '/')} | ${(s.cap || s.vo).replace(/\[\[pause [\d.]+\]\]/g, '…').replace(/\|/g, '/')} |\n`; });
  }
  fs.writeFileSync(path.join(OUT, 'SCRIPTS.md'), md);
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const arg = process.argv[2];
  const browser = await chromium.launch({ executablePath: CHROME });
  if (arg === '--scripts-only') {  // rebuild SCRIPTS.md from the last render's narration timings
    const results = VIDEOS.filter(v => v.group !== 'lessons').map(video => {
      const t = JSON.parse(fs.readFileSync(path.join(WORK, video.id, 'timings.json')));
      let start = 0; const timeline = video.scenes.map((s, i) => { const vo = t[`s${String(i + 1).padStart(2, '0')}`].dur, dur = LEAD_IN + vo + TAIL + (s.hold || 0), r = { start, dur, vo }; start += dur; return r; });
      return { video, timeline, total: start };
    });
    writeScripts(results); await browser.close(); console.log('wrote video/SCRIPTS.md'); return;
  }
  if (arg === '--thumbs-only') { for (const v of VIDEOS) await thumbnail(v, browser); await browser.close(); console.log(`${VIDEOS.length} thumbnails`); return; }
  const ids = arg ? new Set(arg.split(',')) : null;
  const results = [];
  for (const v of VIDEOS) {
    const pick = ids ? (ids.has(v.id) || ids.has(v.group)) : v.group !== 'lessons';
    if (pick) results.push(await render(v, browser));
  }
  await browser.close();
  if (!arg) writeScripts(results);
  else console.log('(SCRIPTS.md only regenerates on a full core build)');
})();
