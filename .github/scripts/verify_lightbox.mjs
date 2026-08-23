// Verify CatBench lightbox renders SVG previews (object) and raster (img).
import { chromium } from 'playwright';
import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const CATBENCH = resolve(ROOT, 'demos', 'CatBench');
const PORT = 8765;

function startServer(rootDir, port) {
  return new Promise((resolveP, rejectP) => {
    const server = http.createServer(async (req, res) => {
      try {
        let pth = decodeURIComponent((req.url || '/').split('?')[0]);
        if (pth === '/') pth = '/index.html';
        const file = resolve(rootDir, '.' + pth);
        const data = await readFile(file);
        const ext = file.split('.').pop()?.toLowerCase();
        const types = {
          html: 'text/html', json: 'application/json', svg: 'image/svg+xml',
          jpg: 'image/jpeg', js: 'text/javascript', css: 'text/css',
        };
        res.setHeader('Content-Type', types[ext] || 'application/octet-stream');
        res.end(data);
      } catch {
        res.statusCode = 404;
        res.end('not found');
      }
    });
    server.on('error', rejectP);
    server.listen(port, () => resolveP(server));
  });
}

async function main() {
  const server = await startServer(CATBENCH, PORT);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  try {
    await page.goto(`http://127.0.0.1:${PORT}/`, { waitUntil: 'networkidle' });
    await page.waitForSelector('.catbench-grid .cell[data-kind="svg"]', { timeout: 10000 });
    const svgCell = page.locator('.catbench-grid .cell[data-kind="svg"]').first();
    await svgCell.click();
    await page.waitForSelector('.lightbox:not([hidden])', { timeout: 5000 });
    const objectBox = await page.locator('.lightbox-body object').boundingBox();
    const imgCount = await page.locator('.lightbox-body img').count();
    if (!objectBox || objectBox.width < 100 || objectBox.height < 100) {
      console.error('FAIL: lightbox object missing or too small', objectBox, 'imgCount', imgCount);
      process.exit(1);
    }
    await page.keyboard.press('Escape');
    const pyCell = page.locator('.catbench-grid .cell[data-kind="image"]').first();
    await pyCell.click();
    await page.waitForSelector('.lightbox:not([hidden]) .lightbox-body img', { timeout: 5000 });
    const imgBox = await page.locator('.lightbox-body img').boundingBox();
    if (!imgBox || imgBox.width < 50 || imgBox.height < 50) {
      console.error('FAIL: lightbox raster img missing or too small', imgBox);
      process.exit(1);
    }
    console.log('PASS: svg object', Math.round(objectBox.width), 'x', Math.round(objectBox.height));
    console.log('PASS: python img', Math.round(imgBox.width), 'x', Math.round(imgBox.height));
  } finally {
    await browser.close();
    server.close();
  }
}

main().catch(err => { console.error(err); process.exit(1); });