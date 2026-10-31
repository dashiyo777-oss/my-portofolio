// capture_png.js <baseUrl> <outDir> <layer1,layer2,...>
// Screenshots each ?layer=NAME of the overlay page as a transparent 1080x1920 PNG.
const { chromium } = require('playwright-core');
const fs = require('fs');
function findChrome() {
  const base = '/opt/pw-browsers';
  try {
    const dir = fs.readdirSync(base).find(d => d.startsWith('chromium-') && !d.includes('headless'));
    if (dir) return `${base}/${dir}/chrome-linux/chrome`;
  } catch (e) {}
  return undefined;
}
(async () => {
  const [baseUrl, outDir, layersCsv] = process.argv.slice(2);
  const layers = layersCsv.split(',').map(s => s.trim()).filter(Boolean);
  const b = await chromium.launch({ executablePath: findChrome(), args: ['--no-sandbox', '--force-color-profile=srgb', '--disable-gpu'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  for (const layer of layers) {
    await p.goto(`${baseUrl}?layer=${layer}`, { waitUntil: 'networkidle' });
    await p.evaluate(async () => { if (document.fonts && document.fonts.ready) await document.fonts.ready; });
    await p.waitForTimeout(350);
    const out = `${outDir}/${layer}.png`;
    await p.screenshot({ path: out, type: 'png', omitBackground: true });
    console.log('wrote', out);
  }
  await b.close();
})();
