import { chromium } from 'playwright';
import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { resolve, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const CATBENCH = join(ROOT, 'demos', 'CatBench');
const PORT = 8777;

const server = await new Promise((res, rej) => {
  const s = http.createServer(async (req, res) => {
    let p = decodeURIComponent((req.url || '/').split('?')[0]);
    if (p === '/') p = '/index.html';
    const file = resolve(CATBENCH, '.' + p);
    const data = await readFile(file);
    const ext = file.split('.').pop()?.toLowerCase();
    res.setHeader('Content-Type', ({ html: 'text/html', json: 'application/json', svg: 'image/svg+xml', jpg: 'image/jpeg' })[ext] || 'application/octet-stream');
    res.end(data);
  });
  s.on('error', rej);
  s.listen(PORT, () => res(s));
});

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
await page.goto(`http://127.0.0.1:${PORT}/`, { waitUntil: 'networkidle' });
await page.waitForSelector('[data-path="assets/Grok-Build-0.1.svg"]');
const grok = page.locator('[data-path="assets/Grok-Build-0.1.svg"]');
const comp = page.locator('[data-path="assets/Composer-2.5.svg"]');
const grokBox = await grok.boundingBox();
const compBox = await comp.boundingBox();
const grokImg = await grok.locator('img').boundingBox();
const compImg = await comp.locator('img').boundingBox();
const grokOffset = grokImg.x - grokBox.x;
const compOffset = compImg.x - compBox.x;
console.log('grok img left offset in cell:', Math.round(grokOffset), 'px');
console.log('composer img left offset in cell:', Math.round(compOffset), 'px');
if (Math.abs(grokOffset - compOffset) > 12) {
  console.error('FAIL: grok still shifted vs composer');
  process.exit(1);
}
console.log('PASS: grok alignment matches composer');
await browser.close();
server.close();