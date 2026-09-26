#!/usr/bin/env python3
"""Lint lesson video scripts before rendering.

Checks structure (known scene types, required fields, asset paths, flow edges), teaching
quality (teaching arc, visual variety, cutaways, pacing) and compliance (no income or
safety promises, no key or seed-phrase requests).

Usage:
  python3 lint_video_script.py ../video-scripts/gold/lesson-03-2.json   # one or more files
  python3 lint_video_script.py --all                                    # every script
  python3 lint_video_script.py --all --summary                          # one line per file
Exit code 1 if any ERROR was found. WARN lines are quality advice, not blockers.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WPM = 150  # Kokoro at speed 0.96 with measured pauses lands close to this

REQUIRED = {
    'title': ['title'], 'statement': ['lines'], 'strike': ['big', 'after'], 'bullets': ['title', 'items'],
    'pillars': ['title', 'items'], 'compare': ['title', 'left', 'right'], 'steps': ['title', 'steps'],
    'quiz': ['q', 'a', 'n', 'of'], 'logo': ['tagline'], 'image': ['src'], 'stats': ['stats'],
    'cta': ['button'], 'flow': ['nodes'], 'cutaway': ['shots'],
    # chart/flow3d/chart3d predate this linter (chart shipped without a linter update;
    # flow3d/chart3d are the WebGL scene types - see .claude/skills/webgl-motion-graphics).
    # `kind` defaults to "bars" in build_video.js, so it's not required here either -
    # these are deliberately as loose as `flow`: real per-kind field checks (bars vs
    # segs vs series) aren't cross-checked.
    'chart': [], 'flow3d': ['nodes'], 'chart3d': [],
}
TEXT_SLIDES = {'bullets', 'statement', 'steps', 'pillars'}
VISUALS = {'image', 'flow', 'flow3d', 'cutaway', 'compare', 'stats', 'strike', 'chart', 'chart3d'}
FORBIDDEN = [
    (r'\bguarantee(d|s)?\b(?!.*\bno\b)', 'promise of guaranteed results'),
    (r'\brisk[- ]free\b', '"risk-free"'),
    (r'\b(passive income|get rich|financial freedom in)\b', 'income hype'),
    (r'\byou will (make|earn)\b', 'earnings claim'),
    (r'\b(return|returns|yield|yields|profit|profits|earn|earns|make|makes|pays?)\b.{0,25}\b\d+(\.\d+)?\s?% (a|per|every) (month|week|day)\b', 'periodic return claim'),
    (r'\b(send|share|enter|type|paste) (me |us )?(your )?(seed phrase|private key|recovery phrase)\b', 'asks for keys'),
    (r'\b(zero|no) risk\b', '"no risk"'),
]
# A match inside a warning ("never share your seed phrase", "guaranteed returns are a scam") is fine.
NEGATION = re.compile(r"\b(never|not|no|scam|scams|fake|don't|doesn't|won't|isn't|aren't|red flag|beware|what is it|someone offers|offers you)\b|n't\b", re.I)
ABBR_OK = {'I', 'OK', 'TV', 'US', 'UK', 'AI'}


def sentences(text):
    return [s for s in re.split(r'(?<=[.?!])\s+', re.sub(r'\[\[pause [\d.]+\]\]', ' ', text or '').strip()) if s]


def lint(path):
    out = []
    err = lambda i, m: out.append(('ERROR', i, m))
    warn = lambda i, m: out.append(('WARN', i, m))
    try:
        v = json.loads(Path(path).read_text())
    except Exception as e:  # noqa: BLE001
        return [('ERROR', '-', f'invalid JSON: {e}')], {}
    scenes = v.get('scenes') or []
    for k in ('id', 'title', 'size', 'scenes'):
        if k not in v:
            err('-', f'missing top-level "{k}"')
    words = 0
    for i, s in enumerate(scenes, 1):
        t = s.get('type')
        if t not in REQUIRED:
            err(i, f'unknown scene type "{t}"')
            continue
        for f in REQUIRED[t]:
            if f not in s:
                err(i, f'{t}: missing "{f}"')
        vo = s.get('vo', '')
        if not vo.strip():
            err(i, f'{t}: empty "vo"')
        w = len(vo.split())
        words += w
        if w / WPM * 60 > 75 and t in TEXT_SLIDES:
            warn(i, f'{t}: {w / WPM * 60:.0f}s of voice over one text slide: split it, or cut away to a flow, image or demo')
        for sent in sentences(vo):
            if len(sent.split()) > 32:
                warn(i, f'sentence of {len(sent.split())} words is hard to follow by ear: "{sent[:60]}..."')
        caps = set(re.findall(r'\b[A-Z]{2,}s?\b', vo)) - ABBR_OK
        if caps and not s.get('cap'):
            warn(i, f'abbreviations {sorted(caps)} in "vo": write them as the voice should say them (L.T.V.) and put the on-screen form in "cap"')
        texts = [vo, s.get('cap', '')] + [x for k, x in s.items() if isinstance(x, str) and k not in ('vo', 'cap', 'src')]
        texts += [x if isinstance(x, str) else json.dumps(x) for k in ('items', 'steps', 'lines', 'shots', 'nodes') for x in s.get(k, [])]
        hit = set()
        for sent in (y for x in texts for y in sentences(x)):
            for pat, why in FORBIDDEN:
                m = re.search(pat, sent, re.I)
                if m and why not in hit and not NEGATION.search(sent[:m.start()] + ' ' + sent[m.end():]):
                    hit.add(why)
                    err(i, f'compliance: {why}: "{sent[:80]}"')
        for src in [s.get('src')] + [x.get('src') for x in s.get('shots', [])]:
            if src and not (ROOT / src).exists():
                err(i, f'missing asset {src}')
        if t == 'quiz' and not any(re.match(r'(the )?answer', x, re.I) for x in sentences(vo)):
            err(i, 'quiz: "vo" needs a sentence starting "The answer..." so the timer and reveal sync')
        if t in ('flow', 'flow3d'):
            ids = {n.get('id', str(j)) for j, n in enumerate(s.get('nodes', []))}
            for e in s.get('edges', []):
                if e.get('from') not in ids or e.get('to') not in ids:
                    err(i, f'{t}: edge {e.get("from")}->{e.get("to")} points at an unknown node')
            if len(s.get('nodes', [])) > 6:
                warn(i, f'{t}: more than 6 nodes is hard to read: split into two flows')
        if t == 'cutaway':
            for j, sh in enumerate(s.get('shots', []), 1):
                if not sh.get('box') and not sh.get('zoom'):
                    warn(i, f'cutaway shot {j}: no highlight box: show the viewer where to look')
        if t in ('bullets', 'steps') and len(s.get('items', s.get('steps', []))) > 6:
            warn(i, f'{t}: more than 6 items on one slide')

    types = [s.get('type') for s in scenes]
    mins = words / WPM
    if mins > v.get('maxMinutes', 25):
        err('-', f'about {mins:.1f} min: over the {v.get("maxMinutes", 25)}-minute cap, split into parts')
    if v.get('group') == 'lessons':
        text_share = sum(t in TEXT_SLIDES for t in types) / max(1, len(types))
        run, best = 0, 0
        for a, b in zip(types, types[1:]):
            run = run + 1 if a == b and a in TEXT_SLIDES else 0
            best = max(best, run + 1)
        if text_share > 0.55:
            warn('-', f'{text_share:.0%} of scenes are text slides: add flows, images, cutaways or comparisons')
        if best >= 3:
            warn('-', f'{best} text slides in a row: break the run with a visual')
        if not any(t in VISUALS for t in types):
            warn('-', 'no visual scene at all (flow, image, cutaway, compare, stats)')
        if not any(t in ('steps', 'cutaway') for t in types):
            warn('-', 'no worked example or demo: show it being done (steps or cutaway)')
        if 'quiz' not in types:
            warn('-', 'no retrieval check (quiz)')
        chapters = ' '.join(str(s.get('chapter', '')) for s in scenes).lower()
        if not re.search(r'why|problem|matters|hook', chapters):
            warn('-', 'no hook chapter ("Why it matters"): open with the problem before the content')
        if not re.search(r'recap|summary|wrap', chapters):
            warn('-', 'no recap chapter')
    stats = {'scenes': len(types), 'minutes': round(mins, 1), 'visual': sum(t in VISUALS for t in types),
             'text': sum(t in TEXT_SLIDES for t in types)}
    return out, stats


def main(argv):
    summary = '--summary' in argv
    files = [a for a in argv if not a.startswith('--')]
    if '--all' in argv:
        files = sorted(str(p) for p in (ROOT / 'video-scripts').rglob('*.json'))
    if not files:
        print(__doc__)
        return 2
    n_err = n_warn = 0
    for f in files:
        issues, st = lint(f)
        e = sum(x[0] == 'ERROR' for x in issues)
        w = len(issues) - e
        n_err += e
        n_warn += w
        name = Path(f).name
        if summary:
            print(f'{name:28} {st.get("minutes", 0):5.1f} min  {st.get("scenes", 0):3} scenes  visual {st.get("visual", 0):2}  text {st.get("text", 0):2}  {e} errors  {w} warnings')
        else:
            print(f'\n{name}  ({st.get("minutes", 0)} min, {st.get("scenes", 0)} scenes)')
            for lvl, i, m in issues:
                print(f'  {lvl:5} scene {i}: {m}')
            if not issues:
                print('  clean')
    print(f'\n{len(files)} files · {n_err} errors · {n_warn} warnings')
    return 1 if n_err else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
