// Screenshot every demos/<name>/index.html and every entry in data.json with
// a `screenshot_from` field. Outputs to assets/thumbs/<name>.png.
//
// Local targets are served over a tiny HTTP server on localhost so pages
// using fetch() or XHR for same-origin assets work. The file:// origin would
// block those requests in headless Chromium.
//
// Usage: node scripts/screenshot_thumbs.mjs

import { chromium } from 'playwright';
import { readFile, readdir, stat, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { join, resolve, dirname, sep, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import http from 'node:http';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const THUMBS_DIR = join(ROOT, 'assets', 'thumbs');
const DEMOS_DIR = join(ROOT, 'demos');
const DATA_JSON = join(ROOT, 'data.json');
const PORT = 8642;
const BASE_URL = `http://localhost:${PORT}`;

const VIEWPORT = { width: 1280, height: 720 };
const NAV_TIMEOUT_MS = 30_000;
const SETTLE_MS = 2000;

const MIME = {
  html: 'text/html', css: 'text/css', js: 'text/javascript', mjs: 'text/javascript',
  json: 'application/json', png: 'image/png', svg: 'image/svg+xml',
  jpg: 'image/jpeg', jpeg: 'image/jpeg', gif: 'image/gif', webp: 'image/webp',
  woff: 'font/woff', woff2: 'font/woff2', txt: 'text/plain', md: 'text/markdown',
  ico: 'image/x-icon',
};

function mimeFor(file) {
  const dot = file.lastIndexOf('.');
  const ext = dot < 0 ? '' : file.slice(dot + 1).toLowerCase();
  return MIME[ext] || 'application/octet-stream';
}

async function ensureDir(p) {
  if (!existsSync(p)) await mkdir(p, { recursive: true });
}

function startStaticServer(rootDir, port) {
  return new Promise((resolveP, rejectP) => {
    const server = http.createServer(async (req, res) => {
      try {
        let pth = decodeURIComponent((req.url || '/').split('?')[0]);
        if (pth.endsWith('/')) pth += 'index.html';
        if (pth.startsWith('/')) pth = pth.slice(1);
        const file = resolve(rootDir, pth);
        if (!file.startsWith(rootDir + sep) && file !== rootDir) {
          res.statusCode = 403; return res.end('forbidden');
        }
        const data = await readFile(file);
        res.setHeader('Content-Type', mimeFor(file));
        res.setHeader('Cache-Control', 'no-store');
        res.end(data);
      } catch {
        res.statusCode = 404; res.end('not found');
      }
    });
    server.on('error', rejectP);
    server.listen(port, () => resolveP(server));
  });
}

function resolveTargetUrl(spec) {
  if (/^https?:\/\//i.test(spec)) return spec;
  return `${BASE_URL}/${spec.replace(/^\/+/, '')}`;
}

async function listDemos() {
  if (!existsSync(DEMOS_DIR)) return [];
  const out = [];
  for (const entry of await readdir(DEMOS_DIR)) {
    if (entry.startsWith('.')) continue;
    const full = join(DEMOS_DIR, entry);
    const st = await stat(full);
    if (st.isDirectory()) {
      // Sentinel: skip demos whose folder contains `.gallery-exclude`. They
      // still serve at /demos/<name>/, just no card and no auto thumbnail.
      if (existsSync(join(full, '.gallery-exclude'))) continue;
      if (existsSync(join(full, 'index.html'))) {
        out.push({
          name: entry,
          url: `${BASE_URL}/demos/${entry}/`,
          source: relative(ROOT, full).replace(/\\/g, '/'),
        });
      }
    } else if (st.isFile() && /\.html?$/i.test(entry)) {
      const name = entry.replace(/\.html?$/i, '');
      out.push({
        name,
        url: `${BASE_URL}/demos/${entry}`,
        source: `demos/${entry}`,
      });
    }
  }
  return out;
}

async function readDataJsonTargets() {
  if (!existsSync(DATA_JSON)) return [];
  const data = JSON.parse(await readFile(DATA_JSON, 'utf-8'));
  return (data.projects || [])
    .filter(p => p.screenshot_from)
    .map(p => {
      const isUrl = /^https?:\/\//i.test(p.screenshot_from);
      return {
        name: p.name,
        url: resolveTargetUrl(p.screenshot_from),
        // For URL targets there's no local source to compare against;
        // proxy via data.json's last commit time so the thumb is regenerated
        // when (and only when) the URL is changed/added.
        source: isUrl ? 'data.json' : p.screenshot_from,
      };
    });
}

function gitLastCommitISO(path) {
  try {
    const out = execFileSync('git', ['log', '-1', '--format=%aI', '--', path],
      { cwd: ROOT, encoding: 'utf-8', stdio: ['ignore', 'pipe', 'ignore'] });
    return out.trim() || null;
  } catch {
    return null;
  }
}

// Skip the screenshot if the existing thumb was committed AT OR AFTER the
// source's last change. This stops Playwright pixel jitter from producing
// a "new" thumb on every CI run when nothing meaningful changed.
function shouldSkipShot(target) {
  // Look at whichever thumb extension already exists (jpg is current default,
  // legacy .png entries are still respected).
  const candidates = ['jpg', 'jpeg', 'webp', 'png'];
  let thumbRel = null;
  for (const ext of candidates) {
    const rel = `assets/thumbs/${target.name}.${ext}`;
    if (existsSync(join(ROOT, rel))) { thumbRel = rel; break; }
  }
  if (!thumbRel) return false;
  const thumbT = gitLastCommitISO(thumbRel);
  if (!thumbT) return false;
  const srcT = target.source ? gitLastCommitISO(target.source) : null;
  if (!srcT) return false;
  return new Date(thumbT) >= new Date(srcT);
}

async function shoot(page, name, url) {
  const out = join(THUMBS_DIR, `${name}.jpg`);
  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: NAV_TIMEOUT_MS });
  } catch (e) {
    console.warn(`  ! ${name}: networkidle timeout, falling back to load`);
    try {
      await page.goto(url, { waitUntil: 'load', timeout: NAV_TIMEOUT_MS });
    } catch (e2) {
      console.error(`  X ${name}: failed to load ${url}: ${e2.message}`);
      return false;
    }
  }
  await page.waitForTimeout(SETTLE_MS);
  // JPG ~50% the size of PNG for these screenshots; quality 80 is plenty.
  // Heavy demos (transformers.js, LLM init) saturate the runner CPU; the default
  // 30s screenshot timeout isn't enough on GH-hosted runners. Bump to 90s and
  // retry once with the load-state path if the first capture still hangs.
  try {
    await page.screenshot({ path: out, fullPage: false, type: 'jpeg', quality: 80, timeout: 90_000 });
  } catch (e) {
    console.warn(`  ! ${name}: screenshot timeout, retrying once: ${e.message}`);
    await page.waitForTimeout(2000);
    await page.screenshot({ path: out, fullPage: false, type: 'jpeg', quality: 80, timeout: 90_000 });
  }
  console.log(`  - ${name} -> ${out}`);
  return true;
}

(async () => {
  await ensureDir(THUMBS_DIR);

  const fromData = await readDataJsonTargets();
  const local = await listDemos();
  const seen = new Set(fromData.map(t => t.name));
  const localFiltered = local.filter(p => !seen.has(p.name));
  const allTargets = [...localFiltered, ...fromData];

  // Filter out unchanged targets so CI doesn't churn fresh-byte thumbnails
  // every run on demos that haven't actually been touched.
  const targets = [];
  let skipped = 0;
  for (const t of allTargets) {
    if (shouldSkipShot(t)) {
      skipped++;
    } else {
      targets.push(t);
    }
  }

  if (targets.length === 0) {
    console.log(`nothing to screenshot (${skipped} target(s) up to date)`);
    return;
  }

  console.log(`screenshotting ${targets.length} target(s); ${skipped} skipped (unchanged source)`);

  const server = await startStaticServer(ROOT, PORT);
  console.log(`local static server: ${BASE_URL}`);

  const browser = await chromium.launch();
  // Match the site's dark aesthetic: pages that listen to prefers-color-scheme
  // (e.g. the AMOLED editor, Infinite Craft) render in dark mode for the thumb.
  const ctx = await browser.newContext({
    viewport: VIEWPORT,
    deviceScaleFactor: 1,
    colorScheme: 'dark',
  });
  ctx.on('page', p => p.on('dialog', d => d.dismiss().catch(() => {})));
  const page = await ctx.newPage();
  page.on('dialog', d => d.dismiss().catch(() => {}));

  let ok = 0;
  for (const t of targets) {
    if (await shoot(page, t.name, t.url)) ok++;
  }

  await browser.close();
  await new Promise(r => server.close(r));
  console.log(`done: ${ok}/${targets.length} (+${skipped} skipped)`);
})().catch(err => {
  console.error(err);
  process.exit(1);
});
