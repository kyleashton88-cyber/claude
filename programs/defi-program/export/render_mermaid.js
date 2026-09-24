// Render every ```mermaid block in the master file to PNG (mermaid-N.png).
const fs = require('fs');
const { chromium } = require('playwright-core');
const md = fs.readFileSync(process.argv[2], 'utf8');
const blocks = [...md.matchAll(/```mermaid\n([\s\S]*?)```/g)].map(m => m[1]);
(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await browser.newPage({ deviceScaleFactor: 2 });
  await page.setContent('<html><body style="background:#fff;margin:0"><div id="c"></div></body></html>');
  await page.addScriptTag({ path: require.resolve('mermaid/dist/mermaid.min.js') });
  await page.evaluate(() => mermaid.initialize({ startOnLoad: false, theme: 'neutral', fontFamily: 'Arial' }));
  for (let i = 0; i < blocks.length; i++) {
    const svg = await page.evaluate(async ([src, id]) => (await mermaid.render(id, src)).svg, [blocks[i].replace('flowchart LR', 'flowchart TD'), 'm' + i]);
    await page.evaluate(s => { document.getElementById('c').innerHTML = `<div id="w" style="display:inline-block;padding:12px">${s}</div>`; }, svg);
    await (await page.$('#w')).screenshot({ path: require("path").join(__dirname, `mermaid-${i}.png`) });
  }
  console.log(blocks.length, 'diagrams');
  await browser.close();
})();
