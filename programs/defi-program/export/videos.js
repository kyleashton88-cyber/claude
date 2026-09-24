// Video scripts: the single source of truth for narration, captions and
// visuals. build_video.js renders them; it also writes ../video/SCRIPTS.md.
//
// Scene types: title, statement, strike, image, bullets, pillars, compare,
// steps, stats, quiz, logo, cta. `vo` is spoken (abbreviations spelled for
// the voice, "[[pause 3]]" for a timed pause); `cap` is the written caption.
// Reveals and highlights sync to the sentence that mentions each item.
// Rules: no income or return claims, no urgency tricks, keys never requested.

const VIDEOS = [
  {
    id: 'vsl-main',
    title: 'VSL: main (sales page & store listing)',
    size: [1920, 1080], chrome: 'minimal', music: true, speed: 0.98, seed: 5,
    thumbnail: { title: 'From zero to your own on-chain bank', subtitle: 'On-Chain Operator Program' },
    use: 'Whop store listing video, sales page hero, application page.',
    scenes: [
      { type: 'strike', big: '12% APY', after: 'What am I being paid to risk?',
        vo: 'Most people enter DeFi through a number. Twelve percent A.P.Y. Operators start with a different question. What am I being paid to risk?',
        cap: 'Most people enter DeFi through a number. 12% APY. Operators start with a different question. What am I being paid to risk?' },
      { type: 'statement', lines: ['And how do I get out?'], sub: "If you can't explain the exit, you don't understand the position yet.",
        vo: "And how do I get out? Because if you can't explain the exit, you don't understand the position yet." },
      { type: 'bullets', title: 'Why most people get hurt in DeFi', check: false,
        items: ['Setup mistakes that can’t be undone', 'Yields nobody can explain', 'Borrowing with no buffer', 'No plan for the way out'],
        vo: "Here's why most people get hurt. Setup mistakes that can't be undone: the wrong network, a leaked seed phrase, one bad approval. Yields nobody can explain, until the subsidy stops. Borrowing with no buffer, so one sharp move liquidates them. And no plan for the way out." },
      { type: 'statement', kicker: 'On-chain', lines: ["There's no help desk."], sub: 'No chargebacks. No margin calls. No one to phone. The only protection is the process you follow before you act.',
        vo: "On-chain, there's no help desk. No chargebacks. No margin calls. No one to phone. The only protection you have is the process you follow before you act." },
      { type: 'logo', tagline: 'From zero to your own on-chain bank.',
        vo: "That process is what the On-Chain Operator Program teaches. It takes you from zero, never having owned crypto, to running your capital with the discipline of your own on-chain bank." },
      { type: 'image', src: 'assets/store/gallery-01-path-to-mastery.png', eyebrow: 'The path', wide: true,
        vo: "It's built as a path, in six stages, and you do them in order. Stage zero sets everything up safely, step by step, with a printable Day-One Setup Kit. Then foundations and safety, swaps and liquidity. Then lending, yield and infrastructure risk.",
        cap: "It's built as a path, in six stages, and you do them in order. Stage 0 sets everything up safely, step by step, with a printable Day-1 Setup Kit. Then foundations and safety, swaps and liquidity. Then lending, yield and infrastructure risk." },
      { type: 'image', src: 'assets/store/gallery-05-research-loop.png', eyebrow: 'Stage 3 · Analyst', wide: true,
        vo: "In stage three, you learn to research any protocol with a six-step loop, and to read on-chain data without fooling yourself. You finish with a real due-diligence file.",
        cap: "In Stage 3, you learn to research any protocol with a 6-step loop, and to read on-chain data without fooling yourself. You finish with a real due-diligence file." },
      { type: 'image', src: 'assets/store/gallery-04-strategy-levels.png', eyebrow: 'Stage 4 · Strategist', wide: true,
        vo: "Stage four is the strategy library. Thirty playbooks in seven levels, from simple lending to fixed-rate yield, basis trades, options and hedged positions. Every one comes with its maths, its kill rules, and exactly how it loses money.",
        cap: "Stage 4 is the strategy library. 30 playbooks in 7 levels, from simple lending to fixed-rate yield, basis trades, options and hedged positions. Every one comes with its maths, its kill rules, and exactly how it loses money." },
      { type: 'image', src: 'assets/store/gallery-03-own-bank.png', eyebrow: 'Stage 5 · Operator', wide: true,
        vo: "And in stage five, you operate as your own bank. A balance sheet. Multisig custody. A credit line against your own assets. A liquidity ladder, so you're never a forced seller.",
        cap: "And in Stage 5, you operate as your own bank. A balance sheet. Multisig custody. A credit line against your own assets. A liquidity ladder, so you're never a forced seller." },
      { type: 'image', src: 'assets/charts/income-waterfall.png', eyebrow: 'The income engine', wide: true,
        vo: "Then the income engine. It measures what you expect to earn after expected losses, and it pays out less than that. Never from principal. No projections, no promises. Just honest arithmetic." },
      { type: 'compare', title: 'What makes it different',
        left: { label: 'Typical crypto course', tone: 'bad', items: ['Signals and hot tips', 'Chases the highest APY', 'Risk in the small print'] },
        right: { label: 'Operator Program', tone: 'good', items: ['A process you can repeat', 'Asks what the yield pays for', 'Risk first, with kill rules'] },
        vo: "Here's what makes it different. A typical crypto course sells signals and hot tips. This program gives you a process you can repeat. Others chase the highest A.P.Y. Here, you ask what the yield is paying you for. And where others hide risk in the small print, we put risk first, with written kill rules.",
        cap: "Here's what makes it different. A typical crypto course sells signals and hot tips. This program gives you a process you can repeat. Others chase the highest APY. Here, you ask what the yield is paying you for. And where others hide risk in the small print, we put risk first, with written kill rules." },
      { type: 'stats', stats: [['15', 'modules'], ['107', 'lessons + 15 starters'], ['30', 'strategy playbooks']], lastAccent: false,
        vo: "Fifteen modules. A hundred and seven lessons, plus a beginner starter at the top of every module. Thirty strategy playbooks.",
        cap: "15 modules. 107 lessons, plus a beginner starter at the top of every module. 30 strategy playbooks." },
      { type: 'pillars', title: "What's included",
        items: [{ icon: 'video', title: 'Narrated video lessons', text: 'Every lesson, with worked examples on screen' },
                { icon: 'chart', title: 'Calculators & worksheets', text: '20 calculators, 17 worksheet templates' },
                { icon: 'target', title: 'Capstones', text: 'Analyst and operator, with rubrics' },
                { icon: 'users', title: 'Live tier', text: 'Group sessions and reviews, on application' }],
        vo: "Every lesson comes with a narrated video lesson, with the worked examples on screen. You get calculators and worksheets for every decision. Two capstones, analyst and operator, marked against a rubric. And for those who want it, a live tier, with group sessions and reviews, on application." },
      { type: 'bullets', title: "What you won't get", check: false, items: ['Signals to copy', 'Promised or projected returns', 'Anyone asking for your keys'],
        vo: "What you won't get: signals to copy, promised or projected returns, or anyone asking for your keys. You keep custody, always." },
      { type: 'statement', kicker: 'Risk reversal', lines: ['14-day conditional refund'], sub: "Full refund within 14 days if you've completed no more than 10% of the lessons and haven't used a capstone or live session.",
        vo: "And you're covered by a fourteen-day conditional refund. If it isn't right for you, and you've completed no more than ten percent of the lessons, with no capstone or live session used, you get a full refund.",
        cap: "And you're covered by a 14-day conditional refund. If it isn't right for you, and you've completed no more than 10% of the lessons, with no capstone or live session used, you get a full refund." },
      { type: 'bullets', title: 'How to join', numbered: true, items: ['Apply: a short form', 'A 30-minute fit call', 'Your enrolment link'],
        vo: "Joining takes three steps. Apply with a short form. Then a thirty-minute fit call, where we'll tell you honestly if it isn't a fit. If it is, you'll get your enrolment link.",
        cap: "Joining takes three steps. Apply with a short form. Then a 30-minute fit call, where we'll tell you honestly if it isn't a fit. If it is, you'll get your enrolment link." },
      { type: 'cta', button: 'Apply to join', sub: 'Application-only · Course and Live tiers · Educational content only',
        vo: "The On-Chain Operator Program. From zero, to your own on-chain bank. Apply below." },
    ],
  },
  {
    id: 'vsl-short-vertical',
    title: 'VSL: 30-second vertical cut (ads, Reels, Shorts, TikTok)',
    size: [1080, 1920], chrome: 'minimal', music: true, speed: 1.0, seed: 8,
    use: 'Paid social and organic short-form. Upload as 9:16.',
    scenes: [
      { type: 'strike', big: '12% APY', after: 'Paid to risk what?',
        vo: 'Twelve percent A.P.Y. Sounds great. But what are you actually being paid to risk?',
        cap: '12% APY. Sounds great. But what are you actually being paid to risk?' },
      { type: 'statement', lines: ["On-chain, there's", 'no help desk.'], sub: 'No chargebacks. No margin calls.',
        vo: "On-chain, there's no help desk. No chargebacks. No margin calls. Just the process you follow." },
      { type: 'logo', tagline: 'From zero to your own on-chain bank.',
        vo: 'The On-Chain Operator Program takes you from zero to running your crypto with the discipline of a bank.' },
      { type: 'stats', stats: [['107', 'lessons'], ['30', 'strategy playbooks'], ['0', 'promised returns']],
        vo: 'A hundred and seven lessons. Thirty strategy playbooks. And zero promised returns. Just a process.',
        cap: '107 lessons. 30 strategy playbooks. And zero promised returns. Just a process.' },
      { type: 'cta', button: 'Apply to join', sub: 'Application-only · Not financial advice',
        vo: 'Apply to join, at the link.' },
    ],
  },
  {
    id: 'welcome',
    title: 'Welcome video (inside the program, top of Start here)',
    size: [1920, 1080], music: true, musicLevel: 0.26, tag: 'Welcome', seed: 21,
    thumbnail: { title: 'Welcome, operator', subtitle: 'Start here' },
    use: 'First thing a new member sees after purchase.',
    scenes: [
      { type: 'logo', chapter: 'Welcome', tagline: 'Welcome, operator.',
        vo: "Welcome to the On-Chain Operator Program. I'm glad you're here. In the next minute, I'll show you exactly how to get the most from it." },
      { type: 'image', chapter: 'How it works', src: 'assets/diagrams/path-to-mastery.png', eyebrow: 'Six stages, in order', wide: true,
        vo: "The program runs in six stages, and each one builds on the last. So do them in order. Stage zero gets you set up safely. Stage five has you running your own on-chain bank. Everything in between is the path from one to the other.",
        cap: "The program runs in six stages, and each one builds on the last. So do them in order. Stage 0 gets you set up safely. Stage 5 has you running your own on-chain bank. Everything in between is the path from one to the other." },
      { type: 'pillars', chapter: 'How it works', title: 'How to work every lesson',
        items: [{ icon: 'video', title: 'Watch', text: 'The video walks the idea and the numbers' },
                { icon: 'check', title: 'Do', text: 'The checklist, with a small test amount' },
                { icon: 'target', title: 'Check', text: 'Three quiz questions before moving on' }],
        vo: "Every lesson works the same way. Watch the video. It walks through the idea and the numbers on screen. Then do the checklist, for real, with a small test amount. Then check yourself with three quiz questions before you move on. The checklist is where the learning sticks." },
      { type: 'statement', chapter: 'How it works', kicker: 'New to a topic?', lines: ['Start with the', 'Mastery Starter.'], sub: 'Every module opens with one. Ten minutes from zero to ready.',
        vo: "New to a topic? Every module opens with a Mastery Starter. It takes about ten minutes, and gets you from zero to ready for that module." },
      { type: 'image', chapter: 'Your first day', src: 'assets/diagrams/setup-roadmap.png', eyebrow: 'Your first day', wide: true,
        vo: "Today, open Module Zero, and print the Day-One Setup Kit. Work through it in order. Use only an amount you can afford to lose while you learn. There's no rush.",
        cap: "Today, open Module 0, and print the Day-1 Setup Kit. Work through it in order. Use only an amount you can afford to lose while you learn. There's no rush." },
      { type: 'statement', chapter: 'The one rule', kicker: 'One rule, forever', lines: ['Never share your', 'seed phrase.'], sub: 'Nobody from this program will ever ask for it, or for your keys.',
        vo: "And one rule, forever. Never share your seed phrase. Nobody from this program will ever ask for it, or for your keys. Anyone who does is a scammer." },
      { type: 'cta', chapter: 'Begin', button: 'Open Module 0', sub: 'Educational content only · Not financial advice',
        vo: "That's it. Open Module Zero, and let's begin.", cap: "That's it. Open Module 0, and let's begin." },
    ],
  },
];

// Module intro videos (one per module), generated from the curriculum so they
// never drift from it. Spoken numbers are spelled out for the voice.
const fs = require('fs');
const path = require('path');
const NUM = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen'];
const clean = s => s.replace(/Mastery Starter:.*$/, 'Mastery Starter').replace(/\*|`/g, '').replace(/\s+—\s+sample lesson/i, '').replace(/,\s*full content in.*$/, '').replace(/\s*\(.*?\)\s*$/, '').trim();
const say = x => x.replace(/APY/g, 'A.P.Y.').replace(/\bLPs\b/g, 'L.P.s').replace(/\bLP\b/g, 'L.P.').replace(/\bL2s?\b/g, 'layer twos').replace(/PT\/YT/g, 'P.T. and Y.T.').replace(/\bMEV\b/g, 'M.E.V.').replace(/\bIL\b/g, 'impermanent loss').replace(/&/g, 'and');
const STAGE_OF = [0, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 4, 5, 5, 5];
const STAGE = ['Zero', 'Foundations', 'Practitioner', 'Analyst', 'Strategist', 'Operator'];
function moduleIntros() {
  const md = fs.readFileSync(path.resolve(__dirname, '../01-offer-and-curriculum.md'), 'utf8');
  const out = [];
  for (const m of md.matchAll(/### Module (\d+) — (.+?) \*\((\d+) lessons?[^)]*\)\*\n(?:Outcome: (.+)\n)?([\s\S]*?)(?=\n### |\n## |$)/g)) {
    const [, n, title, count, outcome = '', rest] = m;
    const rows = [...rest.matchAll(/^\| (\d+\.\d+) \| (.+?) \|/gm)].map(r => [r[1], clean(r[2])]).filter(r => !r[1].startsWith('Mastery Starter'));
    const lessons = rows.map(([id, t]) => `${id} ${t}`);
    const nn = String(n).padStart(2, '0'), st = STAGE_OF[+n];
    const goal = outcome.charAt(0).toUpperCase() + outcome.slice(1).replace(/\.$/, '') + '.';
    const first = rows[0] ? rows[0][1] : '';
    out.push({
      id: `module-${nn}-intro`, title: `Module ${n} intro: ${title}`, size: [1920, 1080], use: `Top of Module ${n} in the Whop course.`, group: 'modules',
      music: true, musicLevel: 0.24, tag: `Module ${n}`, seed: 30 + +n,
      thumbnail: { title, subtitle: `Module ${n}` },
      scenes: [
        { type: 'title', chapter: 'Intro', eyebrow: `Stage ${st} · ${STAGE[st]}`, num: String(n), title, src: `assets/modules/module-${nn}.png`,
          vo: `Module ${NUM[+n]}. ${say(title)}. Part of stage ${NUM[st].toLowerCase()}, ${STAGE[st]}.`, cap: `Module ${n}. ${title}. Part of Stage ${st}, ${STAGE[st]}.` },
        { type: 'statement', chapter: 'The goal', kicker: 'By the end of this module', lines: ['You will be able to…'], sub: goal,
          vo: `By the end of this module, you'll be able to ${say(outcome.replace(/\.$/, '')).replace(/^./, c => c.toLowerCase())}. That's the standard. Every lesson moves you toward it.`,
          cap: `By the end of this module, you'll be able to ${outcome.replace(/\.$/, '').replace(/^./, c => c.toLowerCase())}. That's the standard. Every lesson moves you toward it.` },
        { type: 'bullets', chapter: 'The lessons', title: `${rows.length} lessons`, items: lessons, compact: true, highlight: false,
          vo: `There are ${NUM[rows.length] ? NUM[rows.length].toLowerCase() : rows.length} lessons, starting with ${say(first)}. Each one ends with a checklist to do for real, and a three-question quiz.`,
          cap: `There are ${rows.length} lessons, starting with ${first}. Each one ends with a checklist to do for real, and a three-question quiz.` },
        { type: 'pillars', chapter: 'How to use it', title: 'How to work this module',
          items: [{ icon: 'compass', title: `Starter ${n}.0`, text: 'New to the topic? Ten minutes, zero to ready' },
                  { icon: 'book', title: 'Lessons in order', text: 'Each builds on the one before' },
                  { icon: 'check', title: 'Checklists for real', text: 'Small test amounts, every time' }],
          vo: `If the topic is new to you, start with Mastery Starter ${NUM[+n].toLowerCase()} point zero. It takes about ten minutes. Then take the lessons in order, because each one builds on the one before. And do the checklists for real, with small test amounts, every time.`,
          cap: `If the topic is new to you, start with Mastery Starter ${n}.0. It takes about ten minutes. Then take the lessons in order, because each one builds on the one before. And do the checklists for real, with small test amounts, every time.` },
        { type: 'cta', chapter: 'Begin', button: `Start lesson ${n}.0`, sub: 'Educational content only · Not financial advice',
          vo: `Let's begin, with lesson ${NUM[+n].toLowerCase()} point zero.`, cap: `Let's begin, with lesson ${n}.0.` },
      ],
    });
  }
  return out;
}
VIDEOS.push(...moduleIntros());

module.exports = { VIDEOS };
