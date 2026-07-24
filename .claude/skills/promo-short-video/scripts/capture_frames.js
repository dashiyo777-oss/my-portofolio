#!/usr/bin/env node
/*
 * Deterministic frame exporter for the promo-short engine.
 * Opens <url> (which must define window.renderAt(ms) and window.TOTAL), then
 * screenshots one JPEG per frame at <fps> by driving renderAt — no live recording,
 * so timing is exact and there is zero startup/white pre-roll.
 *
 * Usage: node capture_frames.js <url> <outDir> [fps=30] [chromePath]
 * Requires: playwright-core (npm i playwright-core --no-save)
 */
const { chromium } = require('playwright-core');
const fs = require('fs');

const [,, url, outDir, fpsArg, chromeArg] = process.argv;
if (!url || !outDir) { console.error('usage: node capture_frames.js <url> <outDir> [fps] [chromePath]'); process.exit(1); }
const FPS = parseInt(fpsArg || '30', 10);

function findChrome() {
  if (chromeArg) return chromeArg;
  const base = '/opt/pw-browsers';
  try {
    const dir = fs.readdirSync(base).find(d => d.startsWith('chromium-') && !d.includes('headless'));
    if (dir) return `${base}/${dir}/chrome-linux/chrome`;
  } catch (e) {}
  return undefined; // let playwright resolve its default
}

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const exe = findChrome();
  const b = await chromium.launch({
    executablePath: exe,
    args: ['--no-sandbox', '--force-color-profile=srgb', '--disable-gpu'],
  });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto(url, { waitUntil: 'domcontentloaded' });
  await p.waitForFunction('window.renderAt && window.TOTAL');
  const total = await p.evaluate('window.TOTAL');
  const N = Math.round(total / 1000 * FPS);
  const t0 = Date.now();
  for (let i = 0; i < N; i++) {
    // set the virtual clock, then wait one animation frame so the paint flushes
    await p.evaluate(ms => { window.renderAt(ms); return new Promise(r => requestAnimationFrame(() => r())); }, i * (1000 / FPS));
    await p.screenshot({ path: `${outDir}/f${String(i + 1).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 92 });
    if (i % 150 === 0) console.error(`  frame ${i + 1}/${N}  ${((Date.now() - t0) / 1000).toFixed(1)}s`);
  }
  // print total ms on stdout so the caller can compute duration
  console.log(JSON.stringify({ frames: N, totalMs: total, fps: FPS }));
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
