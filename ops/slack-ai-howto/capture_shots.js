const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright-core");

const ROOT = __dirname;
const HTML = path.join(ROOT, "ui", "slack-howto.html");
const OUT = path.join(ROOT, "shots");
const CHROME =
  process.env.CHROMIUM_PATH ||
  "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";
const SHOTS = ["S02", "S03", "S04", "S05", "S06", "S07", "S08", "S08b"];
const NAMES = {
  S02: "S02_sidebar.png",
  S03: "S03_channel.png",
  S04: "S04_mention.png",
  S05: "S05_draft.png",
  S06: "S06_sent.png",
  S07: "S07_thread.png",
  S08: "S08_reply.png",
  S08b: "S08b_followup.png",
};

(async () => {
  const browser = await chromium.launch({
    executablePath: CHROME,
    headless: true,
    args: ["--no-sandbox", "--disable-gpu"],
  });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto("file://" + HTML);
  for (const id of SHOTS) {
    await page.evaluate((shot) => window.renderShot(shot), id);
    await page.waitForTimeout(50);
    const file = path.join(OUT, NAMES[id]);
    await page.screenshot({ path: file });
    console.log("wrote", file);
  }
  await browser.close();
})();
