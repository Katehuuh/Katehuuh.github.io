// Square-crop CatBench .svg files server-side (replaces client-side attachSvgAutoCrop).
// Uses Playwright + Chromium getBBox, same logic as the old index.html crop.
//
// Usage: node scripts/autocrop_svg.mjs

import { chromium } from 'playwright';
import { readFile, readdir, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { join, resolve, dirname, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import http from 'node:http';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const ASSETS = join(ROOT, 'demos', 'CatBench', 'assets');
const PORT = 8643;
const BASE = `http://localhost:${PORT}`;

const MIME = { svg: 'image/svg+xml' };

function startServer(rootDir, port) {
  return new Promise((resolveP, rejectP) => {
    const server = http.createServer(async (req, res) => {
      try {
        let pth = decodeURIComponent((req.url || '/').split('?')[0]);
        if (pth.startsWith('/')) pth = pth.slice(1);
        const file = resolve(rootDir, pth);
        if (!file.startsWith(rootDir + sep) && file !== rootDir) {
          res.statusCode = 403;
          return res.end('forbidden');
        }
        const data = await readFile(file);
        res.setHeader('Content-Type', MIME.svg);
        res.setHeader('Cache-Control', 'no-store');
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

const CROP_SCRIPT = `(() => {
  const svg = document.querySelector('svg');
  if (!svg) return null;
  const vb = svg.viewBox && svg.viewBox.baseVal;
  const fullW = (vb && vb.width) || svg.getBBox().width;
  const fullH = (vb && vb.height) || svg.getBBox().height;
  if (!fullW || !fullH) return null;
  if (!svg.getAttribute('width') && !svg.getAttribute('height')
      && Math.abs(fullW - fullH) < 0.5) return null;
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  const skip = new Set(['defs', 'metadata', 'title', 'desc', 'style']);
  const isBackdrop = (tag, b) => tag === 'rect'
    && b.width >= fullW * 0.95 && b.height >= fullH * 0.95;
  const walk = (el) => {
    for (const c of el.children) {
      const tag = (c.tagName || '').toLowerCase();
      if (skip.has(tag)) continue;
      if (tag === 'g') { walk(c); continue; }
      try {
        const b = c.getBBox();
        if (b.width === 0 && b.height === 0) continue;
        if (isBackdrop(tag, b)) continue;
        if (b.x < minX) minX = b.x;
        if (b.y < minY) minY = b.y;
        if (b.x + b.width > maxX) maxX = b.x + b.width;
        if (b.y + b.height > maxY) maxY = b.y + b.height;
      } catch (_) {}
    }
  };
  walk(svg);
  if (!isFinite(minX)) return null;
  let x = minX, y = minY, w = maxX - minX, h = maxY - minY;
  const pad = Math.max(w, h) * 0.02;
  x -= pad; y -= pad; w += 2 * pad; h += 2 * pad;
  const side = Math.max(w, h);
  x -= (side - w) / 2;
  y -= (side - h) / 2;
  svg.setAttribute('viewBox', x.toFixed(2) + ' ' + y.toFixed(2) + ' ' + side.toFixed(2) + ' ' + side.toFixed(2));
  svg.removeAttribute('width');
  svg.removeAttribute('height');
  svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
  const pre = document.querySelector('svg')?.ownerDocument?.xmlVersion
    ? '<?xml version="1.0" encoding="UTF-8"?>\\n' : '';
  return pre + new XMLSerializer().serializeToString(svg);
})()`;

async function main() {
  if (!existsSync(ASSETS)) {
    console.log('no demos/CatBench/assets directory');
    return;
  }
  const files = (await readdir(ASSETS)).filter(f => f.toLowerCase().endsWith('.svg'));
  if (!files.length) {
    console.log('autocrop_svg: 0 files');
    return;
  }

  const server = await startServer(ASSETS, PORT);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  let modified = 0;

  try {
    for (const name of files.sort()) {
      const path = join(ASSETS, name);
      const before = await readFile(path, 'utf8');
      const url = `${BASE}/${encodeURIComponent(name)}`;
      await page.goto(url, { waitUntil: 'load' });
      const out = await page.evaluate(CROP_SCRIPT);
      if (!out || out === before) continue;
      await writeFile(path, out, 'utf8');
      console.log(`  cropped ${name}`);
      modified++;
    }
  } finally {
    await browser.close();
    server.close();
  }
  console.log(`autocrop_svg: ${modified}/${files.length} files modified`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});