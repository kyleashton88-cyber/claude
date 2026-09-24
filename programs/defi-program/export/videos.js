// Video scripts: the single source of truth for narration, captions and
// visuals. build_video.js renders them; it also writes ../video/SCRIPTS.md.
//
// Scene types: logo, statement, strike, image, bullets, stats, cta.
// Rules: no income or return claims, no urgency tricks, keys never requested.

const VIDEOS = [
  {
    id: 'vsl-main',
    title: 'VSL: main (sales page & store listing)',
    size: [1920, 1080],
    use: 'Whop store listing video, sales page hero, application page.',
    scenes: [
      { type: 'strike', big: '12% APY', after: 'What am I being paid to risk?',
        vo: 'Most people enter DeFi through a number. An A.P.Y. Operators start with a different question. What am I being paid to risk?',
        cap: 'Most people enter DeFi through a number. An APY. Operators start with a different question. What am I being paid to risk?' },
      { type: 'statement', lines: ['And how do I get out?'], sub: 'If you can\'t explain the unwind, you don\'t understand the position.',
        vo: 'And how do I get out? If you can\'t explain the exit, you don\'t understand the position yet.' },
      { type: 'bullets', title: 'Without a process, DeFi is a maze', items: ['Wallets, seed phrases and networks', 'Approvals you can\'t read', 'Yields you can\'t explain', 'Mistakes that can\'t be undone'],
        vo: 'Without a process, DeFi is a maze. Wallets, networks, approvals, and yields nobody can explain. And on-chain, a mistake can\'t be undone.' },
      { type: 'logo', tagline: 'From zero to your own on-chain bank.',
        vo: 'The On-Chain Operator Program takes you from zero, never having owned crypto, to running your capital like your own on-chain bank.' },
      { type: 'image', src: 'assets/store/gallery-01-path-to-mastery.png', eyebrow: 'The path',
        vo: 'Six stages. Fifteen modules. A hundred and seven lessons, each module opening with a beginner starter. You start by setting everything up safely, step by step, with a Day-One Setup Kit.',
        cap: '6 stages. 15 modules. 107 lessons, each module opening with a beginner starter. You start by setting everything up safely, step by step, with a Day-1 Setup Kit.' },
      { type: 'image', src: 'assets/store/gallery-04-strategy-levels.png', eyebrow: 'Strategy library',
        vo: 'Then you learn to research any protocol, and work through thirty strategy playbooks. Each one with its maths, its exit rules, and exactly how it loses money.',
        cap: 'Then you learn to research any protocol, and work through 30 strategy playbooks. Each one with its maths, its exit rules, and exactly how it loses money.' },
      { type: 'image', src: 'assets/store/gallery-03-own-bank.png', eyebrow: 'Stage five',
        vo: 'Finally, you build your own bank. A balance sheet. Multisig custody. A credit line against your assets. A liquidity ladder.' },
      { type: 'image', src: 'assets/charts/income-waterfall.png', eyebrow: 'The income engine',
        vo: 'And an income engine that measures what you expect to earn after expected losses, and pays out less than that. Never from principal.' },
      { type: 'bullets', title: 'What you won\'t get', items: ['Signals to copy', 'Guaranteed returns', 'Anyone asking for your keys'], check: false,
        vo: 'What you won\'t get: signals to copy, guaranteed returns, or anyone asking for your keys. Just a process you can explain, position by position.' },
      { type: 'cta', button: 'Apply to join', sub: 'Application-only · Course and Live tiers',
        vo: 'The On-Chain Operator Program is application-only. Apply today, and we\'ll see if it\'s the right fit for you.' },
    ],
  },
  {
    id: 'vsl-short-vertical',
    title: 'VSL: 30-second vertical cut (ads, Reels, Shorts, TikTok)',
    size: [1080, 1920],
    use: 'Paid social and organic short-form. Upload as 9:16.',
    scenes: [
      { type: 'strike', big: '12% APY', after: 'Paid to risk what?',
        vo: 'Twelve percent A.P.Y. The real question is: what are you being paid to risk?',
        cap: '12% APY. The real question is: what are you being paid to risk?' },
      { type: 'logo', tagline: 'From zero to your own on-chain bank.',
        vo: 'The On-Chain Operator Program takes you from zero to running your crypto like your own bank.' },
      { type: 'stats', stats: [['107', 'lessons'], ['30', 'strategy playbooks'], ['0', 'guaranteed returns']],
        vo: 'A hundred and seven lessons. Thirty strategy playbooks. And zero promises. Just a process.',
        cap: '107 lessons. 30 strategy playbooks. And zero promises. Just a process.' },
      { type: 'cta', button: 'Apply to join', sub: 'Application-only',
        vo: 'Apply to join the On-Chain Operator Program.' },
    ],
  },
  {
    id: 'welcome',
    title: 'Welcome video (inside the program, top of Module 0)',
    size: [1920, 1080],
    use: 'First thing a new member sees after purchase.',
    scenes: [
      { type: 'logo', tagline: 'Welcome, operator.',
        vo: 'Welcome to the On-Chain Operator Program. Here\'s how to get the most from it.' },
      { type: 'image', src: 'assets/diagrams/path-to-mastery.png', eyebrow: 'How it works', light: true,
        vo: 'The program runs in six stages. Do them in order. Each stage unlocks the next, from your first wallet to running your own on-chain bank.' },
      { type: 'bullets', title: 'Every lesson, the same shape', items: ['Objective', 'Explanation', 'Worked example', 'Checklist', 'Three-question quiz'],
        vo: 'Every lesson has the same shape. An objective, an explanation, a worked example, a checklist, and a short quiz. Do the checklist. That\'s where the learning sticks.' },
      { type: 'image', src: 'assets/diagrams/setup-roadmap.png', eyebrow: 'Start here', light: true,
        vo: 'Start with Module Zero and the Day-One Setup Kit. Use a small amount you can afford to lose while you learn.',
        cap: 'Start with Module 0 and the Day-1 Setup Kit. Use a small amount you can afford to lose while you learn.' },
      { type: 'statement', lines: ['One rule, forever:', 'never share your seed phrase.'], sub: 'Nobody from this program will ever ask for it.',
        vo: 'And one rule, forever. Never share your seed phrase. Nobody from this program, or anywhere else, will ever ask for it.' },
      { type: 'cta', button: 'Open Module 0', sub: 'Educational content only · Not financial advice',
        vo: 'Open Module Zero, and let\'s begin.', cap: 'Open Module 0, and let\'s begin.' },
    ],
  },
];

// Module intro videos (one per module), generated from the curriculum so they
// never drift from it. Spoken numbers are spelled out for the voice.
const fs = require('fs');
const path = require('path');
const NUM = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen'];
const clean = s => s.replace(/Mastery Starter:.*$/, 'Mastery Starter').replace(/\*|`/g, '').replace(/\s+—\s+sample lesson/i, '').replace(/,\s*full content in.*$/, '').replace(/\s*\(.*?\)\s*$/, '').trim();
function moduleIntros() {
  const md = fs.readFileSync(path.resolve(__dirname, '../01-offer-and-curriculum.md'), 'utf8');
  const out = [];
  for (const m of md.matchAll(/### Module (\d+) — (.+?) \*\((\d+) lessons?[^)]*\)\*\n(?:Outcome: (.+)\n)?([\s\S]*?)(?=\n### |\n## |$)/g)) {
    const [, n, title, count, outcome = '', rest] = m;
    const lessons = [...rest.matchAll(/^\| (\d+\.\d+) \| (.+?) \|/gm)].map(r => `${r[1]} ${clean(r[2])}`);
    const nn = String(n).padStart(2, '0');
    const say = x => x.replace(/APY/g, 'A.P.Y.').replace(/\bLP\b/g, 'L.P.').replace(/\bL2s?\b/g, 'layer twos').replace(/PT\/YT/g, 'P.T. and Y.T.');
    out.push({
      id: `module-${nn}-intro`, title: `Module ${n} intro: ${title}`, size: [1920, 1080], use: `Top of Module ${n} in the Whop course.`, group: 'modules',
      scenes: [
        { type: 'image', src: `assets/modules/module-${nn}.png`, eyebrow: `Module ${n}`,
          vo: `Module ${NUM[+n]}. ${say(title)}.`, cap: `Module ${n}. ${title}.` },
        { type: 'statement', lines: ['The goal'], sub: outcome.charAt(0).toUpperCase() + outcome.slice(1).replace(/\.$/, '') + '.',
          vo: `The goal: ${say(outcome)}`, cap: `The goal: ${outcome}` },
        { type: 'bullets', title: `Mastery Starter + ${count} lessons`, items: lessons, compact: true,
          vo: `${NUM[+count] || count} lessons, and a Mastery Starter if you're new to the topic. Each lesson ends with a checklist and a short quiz.`,
          cap: `${count} lessons, plus a Mastery Starter if you're new to the topic. Each lesson ends with a checklist and a short quiz.` },
        { type: 'cta', button: `Start lesson ${n}.1`, sub: 'Educational content only · Not financial advice',
          vo: `Start with lesson ${NUM[+n]} point one.`, cap: `Start with lesson ${n}.1.` },
      ],
    });
  }
  return out;
}
VIDEOS.push(...moduleIntros());

module.exports = { VIDEOS };
