// Diagnose which SVG elements pin the crop bbox edges.
// Usage: node scripts/diag_svg_bbox.mjs [file.svg ...]
import { chromium } from 'playwright';
import http from 'node:http';
import { readFile, readdir } from 'node:fs/promises';
import { join, resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const ASSETS = join(ROOT, 'demos', 'CatBench', 'assets');
const PORT = 8650;

async function analyze(page, skipBackdrop) {
  return page.evaluate((skipBackdrop) => {
  const svg = document.querySelector('svg');
  const vb = svg.viewBox.baseVal;
  const items = [];
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
    const x0 = Math.min(...xs), x1 = Math.max(...xs);
    const y0 = Math.min(...ys), y1 = Math.max(...ys);
    return { x: x0, y: y0, width: x1 - x0, height: y1 - y0 };
  };
  const canvasArea = vb.width * vb.height;
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
    const coverW = b.width / vb.width;
    const coverH = b.height / vb.height;
    return coverW >= 0.75 || coverH >= 0.75 || area >= canvasArea * 0.55;
  };
  const label = (el) => {
    const id = el.id || '';
    const tag = (el.tagName || '').toLowerCase();
    const fill = (el.getAttribute('fill') || '').slice(0, 24);
    const op = el.getAttribute('opacity') || '';
    const t = el.getAttribute('transform') || el.parentElement?.getAttribute('transform') || '';
    return { tag, id, fill, op, transform: t.slice(0, 40) };
  };
  const walk = (el, path = 'svg') => {
    for (const c of el.children) {
      const tag = (c.tagName || '').toLowerCase();
      if (skip.has(tag)) continue;
      const p = path + '>' + (c.id || tag);
      if (tag === 'g') { walk(c, p); continue; }
      try {
        const b = bboxRoot(c);
        if (b.width === 0 && b.height === 0) continue;
        const backdrop = skipBackdrop && isBackdrop(c, tag, b);
        if (backdrop) continue;
        items.push({
          ...label(c),
          path: p,
          x: +b.x.toFixed(2), y: +b.y.toFixed(2),
          w: +b.width.toFixed(2), h: +b.height.toFixed(2),
          x2: +(b.x + b.width).toFixed(2), y2: +(b.y + b.height).toFixed(2),
          area: +(b.width * b.height).toFixed(1),
        });
      } catch (_) {}
    }
  };
  walk(svg);
  if (!items.length) return { viewBox: [vb.x, vb.y, vb.width, vb.height], items: [] };
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  for (const it of items) {
    if (it.x < minX) minX = it.x;
    if (it.y < minY) minY = it.y;
    if (it.x2 > maxX) maxX = it.x2;
    if (it.y2 > maxY) maxY = it.y2;
  }
  const tol = 2;
  const pin = (v, target, key) => Math.abs(v - target) <= tol;
  const edgePins = { left: [], top: [], right: [], bottom: [] };
  for (const it of items) {
    if (pin(it.x, minX, 'x')) edgePins.left.push(it);
    if (pin(it.y, minY, 'y')) edgePins.top.push(it);
    if (pin(it.x2, maxX, 'x2')) edgePins.right.push(it);
    if (pin(it.y2, maxY, 'y2')) edgePins.bottom.push(it);
  };
  const w = maxX - minX, h = maxY - minY;
  const side = Math.max(w, h);
  const pad = side * 0.02;
  const crop = {
    minX, minY, maxX, maxY, w: +w.toFixed(2), h: +h.toFixed(2), side: +side.toFixed(2),
    viewBox: [
      +(minX - pad - (side + 2 * pad - (w + 2 * pad)) / 2).toFixed(2),
      +(minY - pad - (side + 2 * pad - (h + 2 * pad)) / 2).toFixed(2),
      +(side + 2 * pad).toFixed(2),
      +(side + 2 * pad).toFixed(2),
    ],
    emptyPct: {
      left: +((minX - vb.x) / vb.width * 100).toFixed(1),
      top: +((minY - vb.y) / vb.height * 100).toFixed(1),
      right: +((vb.x + vb.width - maxX) / vb.width * 100).toFixed(1),
      bottom: +((vb.y + vb.height - maxY) / vb.height * 100).toFixed(1),
    },
  };
  const sortPins = (arr) => arr.sort((a, b) => a.area - b.area).slice(0, 8);
  return {
    viewBox: [vb.x, vb.y, vb.width, vb.height],
    crop,
    edgePins: {
      left: sortPins(edgePins.left),
      top: sortPins(edgePins.top),
      right: sortPins(edgePins.right),
      bottom: sortPins(edgePins.bottom),
    },
    widest: [...items].sort((a, b) => b.w - a.w).slice(0, 5),
    tiniest: [...items].filter(i => i.area < 500).sort((a, b) => a.area - b.area).slice(0, 8),
  };
  }, skipBackdrop);
}

function startServer(files, port) {
  const map = new Map(files.map(f => ['/' + f, join(ASSETS, f)]));
  return new Promise((resolveP, rejectP) => {
    const server = http.createServer(async (req, res) => {
      const file = map.get(decodeURIComponent((req.url || '').split('?')[0]));
      if (!file) { res.statusCode = 404; return res.end(); }
      res.setHeader('Content-Type', 'image/svg+xml');
      res.end(await readFile(file));
    });
    server.on('error', rejectP);
    server.listen(port, () => resolveP(server));
  });
}

const names = process.argv.slice(2);
const files = names.length
  ? names
  : ['Grok-Build-0.1.svg', 'Composer-2.5.svg'];

const server = await startServer(files, PORT);
const browser = await chromium.launch();
const page = await browser.newPage();

for (const name of files) {
  await page.goto(`http://127.0.0.1:${PORT}/${encodeURIComponent(name)}`, { waitUntil: 'load' });
  const withBackdrop = await analyze(page, false);
  const noBackdrop = await analyze(page, true);
  console.log('\n=== ' + name + ' ===');
  console.log('viewBox:', withBackdrop.viewBox);
  console.log('content bbox (no backdrop skip):', withBackdrop.crop);
  console.log('content bbox (backdrop skipped):', noBackdrop.crop);
  console.log('EDGE PINS (backdrop skipped):');
  for (const edge of ['left', 'top', 'right', 'bottom']) {
    console.log(' ', edge.toUpperCase(), JSON.stringify(noBackdrop.edgePins[edge], null, 0));
  }
  console.log('WIDEST elements:', noBackdrop.widest.map(e => `${e.tag}#${e.id} w=${e.w} (${e.path})`));
  console.log('TINIEST elements:', noBackdrop.tiniest.map(e => `${e.tag}#${e.id} area=${e.area} @${e.x},${e.y}`));
}

await browser.close();
server.close();