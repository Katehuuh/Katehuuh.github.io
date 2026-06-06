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
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  const skip = new Set(['defs', 'metadata', 'title', 'desc', 'style']);
  const canvasArea = fullW * fullH;
  const solidFill = (el) => {
    const fill = (el.getAttribute('fill') || '').trim();
    return fill && fill !== 'none' && !fill.startsWith('url(');
  };
  const isPerfectRect = (el, tag, b) => {
    if (tag !== 'rect') return false;
    const rx = parseFloat(el.getAttribute('rx') || '0');
    const ry = parseFloat(el.getAttribute('ry') || el.getAttribute('rx') || '0');
    if (rx > 0.5 || ry > 0.5) return false;
    const rw = parseFloat(el.getAttribute('width') || '0');
    const rh = parseFloat(el.getAttribute('height') || '0');
    if (!rw || !rh) return false;
    return Math.abs(b.width - rw) <= 1.5 && Math.abs(b.height - rh) <= 1.5;
  };
  const isBackdrop = (el, tag, b) => {
    if (!isPerfectRect(el, tag, b) || !solidFill(el)) return false;
    const opacity = parseFloat(el.getAttribute('opacity') || el.getAttribute('fill-opacity') || '1');
    if (opacity < 0.92) return false;
    const area = b.width * b.height;
    if (area < canvasArea * 0.4) return false;
    const coverW = b.width / fullW;
    const coverH = b.height / fullH;
    return coverW >= 0.75 || coverH >= 0.75 || area >= canvasArea * 0.55;
  };
  const removeBackdrops = (el) => {
    for (let i = el.children.length - 1; i >= 0; i--) {
      const c = el.children[i];
      const tag = (c.tagName || '').toLowerCase();
      if (skip.has(tag)) continue;
      if (tag === 'g') { removeBackdrops(c); continue; }
      try {
        const b = c.getBBox();
        if (isBackdrop(c, tag, b)) c.remove();
      } catch (_) {}
    }
  };
  const walk = (el) => {
    for (const c of el.children) {
      const tag = (c.tagName || '').toLowerCase();
      if (skip.has(tag)) continue;
      if (tag === 'g') { walk(c); continue; }
      try {
        const b = c.getBBox();
        if (b.width === 0 && b.height === 0) continue;
        if (isBackdrop(c, tag, b)) continue;
        if (b.x < minX) minX = b.x;
        if (b.y < minY) minY = b.y;
        if (b.x + b.width > maxX) maxX = b.x + b.width;
        if (b.y + b.height > maxY) maxY = b.y + b.height;
      } catch (_) {}
    }
  };
  walk(svg);
  if (!isFinite(minX)) return null;
  removeBackdrops(svg);
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