// Extract the Day-1 Setup Kit (and roadmap/seed images) from Module 0 into
// a standalone printable markdown file, then build_pdf.js renders it.
// Usage: node build_kit.js  -> ../Day-1-Setup-Kit.md
const fs = require('fs');
const path = require('path');
const mod = fs.readFileSync(path.resolve(__dirname, '../lessons/module-00-crypto-from-zero.md'), 'utf8');
const kit = mod.slice(mod.indexOf('## The Day-1 Setup Kit'));
const rules = mod.slice(mod.indexOf('### Explanation — the 10 rules'), mod.indexOf('### Glossary'));
const md = `# Day-1 Setup Kit

*From knowing nothing about crypto to ready for Module 1. Part of the On-Chain Operator Program, Module 0. Educational content only. Not financial advice.*

![Your setup roadmap](assets/diagrams/setup-roadmap.png)

${kit.replace('## The Day-1 Setup Kit', '## The checklist').trim()}

---

## The 10 rules

${rules.replace('### Explanation — the 10 rules', '').trim()}

![Seed phrase: do and don't](assets/diagrams/seed-backup.png)

![Your first transfer](assets/diagrams/first-transfer.png)
`;
fs.writeFileSync(path.resolve(__dirname, '../Day-1-Setup-Kit.md'), md);
console.log('wrote ../Day-1-Setup-Kit.md');
