// Render square JPEG previews from uploaded .svg files (source SVG never modified).
// Crop/zoom math ignores solid backdrop rects for bbox only; backdrop still paints in output.
//
// Usage: node scripts/render_svg_preview.mjs

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
const OUT_SIZE = 512;

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
        res.setHeader('Content-Type', 'image/svg+xml');
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

const COMPUTE_CROP = `(() => {
  const svg = document.querySelector('svg');
  if (!svg) return null;
  const vb = svg.viewBox && svg.viewBox.baseVal;
  const fullW = (vb && vb.width) || svg.getBBox().width;
  const fullH = (vb && vb.height) || svg.getBBox().height;
  if (!fullW || !fullH) return null;
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  const skip = new Set(['defs', 'metadata', 'title', 'desc', 'style']);
  const pt = svg.createSVGPoint();
  const svgInv = svg.getCTM().inverse();
  const bboxRoot = (el) => {
    const b = el.getBBox();
    const m = el.getCTM().multiply(svgInv);
    if (!m) return b;
    const xs = [], ys = [];
    for (const [x, y] of [[b.x, b.y], [b.x + b.width, b.y], [b.x, b.y + b.height], [b.x + b.width, b.y + b.height]]) {
      pt.x = x; pt.y = y;
      const p = pt.matrixTransform(m);
      xs.push(p.x); ys.push(p.y);
    }
    return { x: Math.min(...xs), y: Math.min(...ys), width: Math.max(...xs) - Math.min(...xs), height: Math.max(...ys) - Math.min(...ys) };
  };
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
  const walk = (el) => {
    for (const c of el.children) {
      const tag = (c.tagName || '').toLowerCase();
      if (skip.has(tag)) continue;
      if (tag === 'g') { walk(c); continue; }
      try {
        const b = bboxRoot(c);
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
  let x = minX, y = minY, w = maxX - minX, h = maxY - minY;
  const pad = Math.max(w, h) * 0.02;
  x -= pad; y -= pad; w += 2 * pad; h += 2 * pad;
  const side = Math.max(w, h);
  x -= (side - w) / 2;
  y -= (side - h) / 2;
  return [x, y, side, side];
})()`;

const APPLY_CROP = (crop, size) => `(() => {
  const svg = document.querySelector('svg');
  if (!svg) return false;
  const c = ${JSON.stringify(crop)};
  svg.setAttribute('viewBox', c[0].toFixed(2) + ' ' + c[1].toFixed(2) + ' ' + c[2].toFixed(2) + ' ' + c[3].toFixed(2));
  svg.setAttribute('width', '${size}');
  svg.setAttribute('height', '${size}');
  svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
  return true;
})()`;

async function main() {
  if (!existsSync(ASSETS)) {
    console.log('no demos/CatBench/assets directory');
    return;
  }
  const files = (await readdir(ASSETS)).filter(f => f.toLowerCase().endsWith('.svg'));
  if (!files.length) {
    console.log('render_svg_preview: 0 files');
    return;
  }

  const server = await startServer(ASSETS, PORT);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: OUT_SIZE, height: OUT_SIZE } });
  let rendered = 0;

  try {
    for (const name of files.sort()) {
      const outName = name.replace(/\.svg$/i, '-svg.jpg');
      const outPath = join(ASSETS, outName);
      const url = `${BASE}/${encodeURIComponent(name)}`;
      await page.goto(url, { waitUntil: 'load' });
      const crop = await page.evaluate(COMPUTE_CROP);
      if (!crop) {
        console.warn(`  skip ${name}: no crop bbox`);
        continue;
      }
      await page.evaluate(APPLY_CROP(crop, OUT_SIZE));
      const buf = await page.locator('svg').screenshot({ type: 'jpeg', quality: 92 });
      await writeFile(outPath, buf);
      console.log(`  preview ${name} -> ${outName}`);
      rendered++;
    }
  } finally {
    await browser.close();
    server.close();
  }
  console.log(`render_svg_preview: ${rendered}/${files.length} previews`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});