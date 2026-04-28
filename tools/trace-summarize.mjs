#!/usr/bin/env node
// Standalone Node CLI version of the trace summarizer.
// Mirrors the aggregator + markdown builder from
// demos/[TOOL]-Debug-Drowser-Perf-Trace.html — same noise filter, same
// init/steady split, same wrapper exclusion, same percentile maths,
// same markdown layout with ASCII bars.
//
// Usage:
//   node tools/trace-summarize.mjs trace.json > report.md
//   cat trace.json | node tools/trace-summarize.mjs > report.md
//   node tools/trace-summarize.mjs trace.json --top 80 --long-ms 30
//
// Why a separate file: GH Pages can't run server-side, so a literal
// `curl <URL>` against the browser tool just returns the HTML.
// This CLI gives an agent the same pipe-friendly behaviour locally —
// pure Node, zero deps, no build step.
//
// Drift caveat: the aggregator logic lives in two places (worker + this
// file). If a bug is found, fix BOTH. A future de-dup step would
// inject this source into the HTML at build time.

import { readFileSync } from 'node:fs';

// ─── Constants (mirror the worker) ────────────────────────────────────
const USE_ONLY_COMPLETE_EVENTS = true;
const JS_EVENT_NAMES = new Set([
  'FunctionCall', 'EvaluateScript', 'V8.Execute', 'v8.run', 'CompileCode', 'JSEvaluate',
]);
const RENDER_EVENTS = new Set([
  'AnimationFrame', 'AnimationFrame::Start', 'AnimationFrame::Fire', 'AnimationFrame::Process',
  'Layout', 'RecalculateStyles', 'RecalculateStyle', 'Paint', 'RasterTask',
  'CompositeLayers', 'UpdateLayerTree', 'HitTest', 'ParseHTML',
  'BeginMainThreadFrame', 'BeginMainFrame', 'Commit', 'ActivateLayerTree',
]);
const WRAPPER_NAMES = new Set([
  'RunTask', 'RunMicrotasks', 'v8.callFunction', 'FireAnimationFrame',
  'v8::Debugger::AsyncTaskRun', 'v8::Debugger::AsyncTaskScheduled',
]);
const NOISE_URL_RE = /^chrome-extension:\/\/|userscript\.html|^https?:\/\/[^/]*\.wbsm\.ai\/|^https?:\/\/websim\.com\/assets\//i;
const INIT_FALLBACK_US = 1500 * 1000;
const PERCENTILE_SAMPLE_CAP = 1000;

// ─── Args ─────────────────────────────────────────────────────────────
function parseArgs(argv) {
  const args = { file: null, topN: 50, longTaskMs: 50, onlyMain: true };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--top') args.topN = +argv[++i];
    else if (a === '--long-ms') args.longTaskMs = +argv[++i];
    else if (a === '--all-threads') args.onlyMain = false;
    else if (a === '-h' || a === '--help') {
      console.error([
        'Usage: trace-summarize.mjs [trace.json] [--top N] [--long-ms N] [--all-threads]',
        '       cat trace.json | trace-summarize.mjs',
        '',
        'Options:',
        '  --top N        Top N items per section (default 50)',
        '  --long-ms N    Long task threshold in ms (default 50)',
        '  --all-threads  Include non-main threads (default: main only)',
      ].join('\n'));
      process.exit(0);
    } else if (!a.startsWith('-') && !args.file) args.file = a;
  }
  return args;
}

async function readInput(file) {
  if (file && file !== '-') return readFileSync(file, 'utf-8');
  // stdin
  return new Promise((resolve, reject) => {
    let buf = '';
    process.stdin.setEncoding('utf-8');
    process.stdin.on('data', chunk => buf += chunk);
    process.stdin.on('end', () => resolve(buf));
    process.stdin.on('error', reject);
  });
}

// ─── Aggregator ───────────────────────────────────────────────────────
function get(obj, path) {
  const parts = path.split('.');
  let cur = obj;
  for (const p of parts) {
    if (cur == null) return undefined;
    cur = cur[p];
  }
  return cur;
}

function extractMetadata(events) {
  const threadNames = new Map();
  const processNames = new Map();
  let minTs = Number.POSITIVE_INFINITY;
  let maxTs = 0;
  for (const ev of events) {
    if (ev.ph === 'X' && ev.ts != null) {
      minTs = Math.min(minTs, ev.ts);
      const endTs = ev.dur != null ? ev.ts + ev.dur : ev.ts;
      maxTs = Math.max(maxTs, endTs);
    }
    if (ev.ph === 'M' && ev.name === 'thread_name' && ev.args && ev.args.name) {
      threadNames.set(ev.pid + ':' + ev.tid, ev.args.name);
    }
    if (ev.ph === 'M' && ev.name === 'process_name' && ev.args && ev.args.name) {
      processNames.set(ev.pid, ev.args.name);
    }
  }
  let main = null;
  for (const [key, name] of threadNames.entries()) {
    if (/CrRendererMain|RendererMain/i.test(name)) {
      const [pid, tid] = key.split(':').map(Number);
      main = { pid, tid, name }; break;
    }
  }
  if (!main) {
    const totals = new Map();
    for (const ev of events) {
      if (USE_ONLY_COMPLETE_EVENTS && ev.ph !== 'X') continue;
      if (!String(ev.cat || '').includes('devtools.timeline')) continue;
      const key = ev.pid + ':' + ev.tid;
      totals.set(key, (totals.get(key) || 0) + (ev.dur || 0));
    }
    let bestKey = null, bestVal = -1;
    for (const [k, v] of totals.entries()) if (v > bestVal) { bestVal = v; bestKey = k; }
    if (bestKey) {
      const [pid, tid] = bestKey.split(':').map(Number);
      main = { pid, tid, name: threadNames.get(bestKey) || 'Main (?)' };
    }
  }
  const mainProcName = main ? (processNames.get(main.pid) || '') : '';
  return {
    threadNames, processNames,
    mainThread: main, processName: mainProcName,
    totalWindowUs: Math.max(0, maxTs - (isFinite(minTs) ? minTs : 0)),
    traceMinUs: isFinite(minTs) ? minTs : 0,
  };
}

function addToMap(map, key, dur, isInit) {
  let cur = map.get(key);
  if (!cur) {
    cur = { total: 0, count: 0, initTotal: 0, initCount: 0, steadyTotal: 0, steadyCount: 0, durs: [] };
    map.set(key, cur);
  }
  cur.total += dur;
  cur.count += 1;
  if (isInit) { cur.initTotal += dur; cur.initCount += 1; }
  else { cur.steadyTotal += dur; cur.steadyCount += 1; }
  if (cur.durs.length < PERCENTILE_SAMPLE_CAP) cur.durs.push(dur);
}

function percentile(durs, q) {
  if (!durs || durs.length === 0) return 0;
  const sorted = durs.slice().sort((a, b) => a - b);
  const idx = Math.min(sorted.length - 1, Math.floor(sorted.length * q));
  return sorted[idx];
}

function isLongTaskName(name) {
  return /Task|ProcessTask|EventDispatch|MessageLoop/i.test(name);
}

function aggregate(events, opts) {
  const { mainPid, mainTid, onlyMain, longTaskThresholdUs, topN } = opts;
  let traceMinUs = Number.POSITIVE_INFINITY;
  for (const ev of events) {
    if (ev.ph === 'X' && ev.ts != null) traceMinUs = Math.min(traceMinUs, ev.ts);
  }
  if (!isFinite(traceMinUs)) traceMinUs = 0;
  let initEndAbsUs = traceMinUs + INIT_FALLBACK_US;
  for (const ev of events) {
    if (ev.name === 'FireAnimationFrame' && ev.ph === 'X' &&
        (mainPid == null || (ev.pid === mainPid && ev.tid === mainTid))) {
      initEndAbsUs = ev.ts; break;
    }
  }

  const totalsByEvent = new Map();
  const totalsRendering = new Map();
  const totalsJS = new Map();
  const totalsJSNoise = new Map();
  const totalsThree = new Map();
  const longTasks = [];
  let eventsParsed = 0, totalMainDurUs = 0;
  let noiseDropTotalUs = 0, noiseDropCount = 0;

  for (const ev of events) {
    eventsParsed++;
    if (USE_ONLY_COMPLETE_EVENTS && ev.ph !== 'X') continue;
    const isMain = (ev.pid === mainPid && ev.tid === mainTid);
    if (onlyMain && !isMain) continue;

    const dur = ev.dur || 0;
    const ts = ev.ts || 0;
    const isInit = ts < initEndAbsUs;

    if (isMain) totalMainDurUs += dur;
    addToMap(totalsByEvent, ev.name, dur, isInit);

    if (RENDER_EVENTS.has(ev.name)) addToMap(totalsRendering, ev.name, dur, isInit);

    if (!WRAPPER_NAMES.has(ev.name) && isLongTaskName(ev.name) && dur >= longTaskThresholdUs) {
      longTasks.push({ name: ev.name, startUs: ts, durUs: dur, isInit, pid: ev.pid, tid: ev.tid });
    }

    const url = get(ev, 'args.data.url') || get(ev, 'args.beginData.url') || '';
    const fn = get(ev, 'args.data.functionName') || get(ev, 'args.beginData.functionName') || '';
    const line = get(ev, 'args.data.lineNumber') ?? get(ev, 'args.beginData.lineNumber');
    const col = get(ev, 'args.data.columnNumber') ?? get(ev, 'args.beginData.columnNumber');
    const loc = (line != null) ? (':' + line + (col != null ? ':' + col : '')) : '';
    const hasJsName = JS_EVENT_NAMES.has(ev.name);
    const jsKey = hasJsName || url || fn
      ? [fn || '', url || '', ev.name].filter(Boolean).join(' @ ') + (loc || '')
      : null;

    if (jsKey) {
      const isNoise = NOISE_URL_RE.test(url) || NOISE_URL_RE.test(jsKey);
      if (isNoise) {
        noiseDropTotalUs += dur; noiseDropCount += 1;
        addToMap(totalsJSNoise, jsKey, dur, isInit);
      } else {
        addToMap(totalsJS, jsKey, dur, isInit);
      }
    }

    if ((url && /three(\.module)?\.js|threejs/i.test(url)) || /three/i.test(fn)) {
      const key = [fn || ev.name, url || ''].filter(Boolean).join(' @ ') + (loc || '');
      addToMap(totalsThree, key, dur, isInit);
    }
  }

  const finishItem = ([name, v]) => ({
    name,
    totalUs: v.total, count: v.count,
    initTotalUs: v.initTotal, initCount: v.initCount,
    steadyTotalUs: v.steadyTotal, steadyCount: v.steadyCount,
    medianUs: percentile(v.durs, 0.5), p95Us: percentile(v.durs, 0.95), p99Us: percentile(v.durs, 0.99),
    isWrapper: WRAPPER_NAMES.has(name),
  });
  const finishJs = ([key, v]) => ({
    key,
    totalUs: v.total, count: v.count,
    initTotalUs: v.initTotal, initCount: v.initCount,
    steadyTotalUs: v.steadyTotal, steadyCount: v.steadyCount,
    medianUs: percentile(v.durs, 0.5), p95Us: percentile(v.durs, 0.95), p99Us: percentile(v.durs, 0.99),
  });
  const sortDesc = (a, b) => b.totalUs - a.totalUs;

  const allEvents = Array.from(totalsByEvent.entries()).map(finishItem).sort(sortDesc);
  const topEvents = allEvents.filter(e => !e.isWrapper).slice(0, topN);
  const wrappers = allEvents.filter(e => e.isWrapper).slice(0, 10);
  const rendering = Array.from(totalsRendering.entries()).map(finishItem).sort(sortDesc).slice(0, topN);
  const topJs = Array.from(totalsJS.entries()).map(finishJs).sort(sortDesc).slice(0, topN);
  const topJsNoise = Array.from(totalsJSNoise.entries()).map(finishJs).sort(sortDesc).slice(0, 10);
  const three = Array.from(totalsThree.entries()).map(finishJs).sort(sortDesc).slice(0, topN);

  longTasks.sort((a, b) => b.durUs - a.durUs);
  return {
    eventsParsed, initEndAbsUs, traceMinUs,
    topEvents, wrappers, rendering, topJs, topJsNoise, three,
    longTasks: longTasks.slice(0, topN),
    totalMainDurUs, noiseDropTotalUs, noiseDropCount,
  };
}

function buildOutput(agg, meta) {
  return {
    meta: {
      eventsParsed: agg.eventsParsed,
      mainThread: meta.mainThread,
      processName: meta.processName,
      totalWindowUs: meta.totalWindowUs,
      totalMainDurUs: agg.totalMainDurUs,
      traceMinUs: agg.traceMinUs,
      initEndAbsUs: agg.initEndAbsUs,
      initWindowUs: Math.max(0, agg.initEndAbsUs - agg.traceMinUs),
      steadyWindowUs: Math.max(0, meta.totalWindowUs - (agg.initEndAbsUs - agg.traceMinUs)),
      noiseDropTotalUs: agg.noiseDropTotalUs,
      noiseDropCount: agg.noiseDropCount,
    },
    topEvents: agg.topEvents, wrappers: agg.wrappers, rendering: agg.rendering,
    topJs: agg.topJs, topJsNoise: agg.topJsNoise, three: agg.three,
    longTasks: agg.longTasks,
  };
}

// ─── Markdown builder ─────────────────────────────────────────────────
function bar(value, max, width = 22) {
  if (max <= 0) return ' '.repeat(width);
  const filled = Math.max(0, Math.min(width, Math.round((value / max) * width)));
  return '█'.repeat(filled) + '░'.repeat(width - filled);
}

function buildMarkdown(r, fileMeta) {
  const fmt = us => (us / 1000).toFixed(2);
  const tStart = (r.meta && r.meta.traceMinUs) || 0;
  const out = [];
  out.push('# Trace summary');
  out.push('');
  out.push('- **File**: `' + (fileMeta.name || '?') + '` (' + (fileMeta.sizeMB || 0).toFixed(1) + ' MB)');
  out.push('- **Thread**: ' + (r.meta.mainThread && r.meta.mainThread.name || '?') +
           ' (pid ' + (r.meta.mainThread && r.meta.mainThread.pid) +
           ', tid ' + (r.meta.mainThread && r.meta.mainThread.tid) + ')');
  out.push('- **Window**: ' + fmt(r.meta.totalWindowUs) + ' ms total | init ' +
           fmt(r.meta.initWindowUs || 0) + ' ms | steady ' + fmt(r.meta.steadyWindowUs || 0) + ' ms');
  out.push('- **Main thread time**: ' + fmt(r.meta.totalMainDurUs) + ' ms');
  out.push('- **Events**: ' + r.meta.eventsParsed.toLocaleString() +
           (r.meta.noiseDropCount ? ' (' + r.meta.noiseDropCount + ' noise events / ' +
            fmt(r.meta.noiseDropTotalUs) + ' ms filtered: chrome-extension, userscript, host-CDN)' : ''));
  out.push('');

  if (r.topJs && r.topJs.length) {
    const max = r.topJs[0].totalUs || 1;
    out.push('## Top JavaScript (page code, noise-filtered)');
    out.push('```');
    for (const i of r.topJs) {
      const trimmed = i.key.length > 44 ? i.key.slice(0, 41) + '...' : i.key;
      const meanS = fmt(i.totalUs / Math.max(1, i.count));
      const phase = (i.steadyCount > 0)
        ? `init=${fmt(i.initTotalUs || 0)}/x${i.initCount || 0}, steady=${fmt(i.steadyTotalUs || 0)}/x${i.steadyCount || 0}`
        : `init-only x${i.initCount || 0}`;
      out.push(trimmed.padEnd(44) + ' [' + bar(i.totalUs, max) + '] ' + fmt(i.totalUs) + ' ms x' + i.count +
               ' | mean=' + meanS + ' med=' + fmt(i.medianUs || 0) + ' p95=' + fmt(i.p95Us || 0) + ' | ' + phase);
    }
    out.push('```');
    out.push('');
  }

  if (r.longTasks && r.longTasks.length) {
    out.push('## Long tasks (above threshold)');
    out.push('```');
    for (const t of r.longTasks) {
      out.push('[' + (t.isInit ? 'INIT  ' : 'STEADY') + '] ' + t.name.padEnd(28) +
               ' dur=' + fmt(t.durUs) + ' ms at t+' + fmt((t.startUs || 0) - tStart) + ' ms');
    }
    out.push('```');
    out.push('');
  }

  if (r.rendering && r.rendering.length) {
    const max = r.rendering[0].totalUs || 1;
    out.push('## Rendering / Layout');
    out.push('```');
    for (const i of r.rendering) {
      out.push(i.name.padEnd(22) + ' [' + bar(i.totalUs, max) + '] ' + fmt(i.totalUs) + ' ms x' + i.count);
    }
    out.push('```');
    out.push('');
  }

  if (r.topEvents && r.topEvents.length) {
    const max = r.topEvents[0].totalUs || 1;
    out.push('## Top events (wrappers excluded)');
    out.push('```');
    for (const i of r.topEvents.slice(0, 18)) {
      out.push(i.name.padEnd(34) + ' [' + bar(i.totalUs, max) + '] ' + fmt(i.totalUs) + ' ms x' + i.count);
    }
    out.push('```');
    out.push('');
  }

  if (r.wrappers && r.wrappers.length) {
    out.push('## Wrappers (do NOT rank — their dur is the sum of children)');
    out.push('```');
    for (const i of r.wrappers) {
      out.push(i.name.padEnd(28) + ' ' + fmt(i.totalUs) + ' ms x' + i.count);
    }
    out.push('```');
    out.push('');
  }

  if (r.three && r.three.length) {
    out.push('## Three.js hotspots');
    out.push('```');
    for (const i of r.three) {
      const trimmed = i.key.length > 60 ? i.key.slice(0, 57) + '...' : i.key;
      out.push(trimmed.padEnd(60) + ' ' + fmt(i.totalUs) + ' ms x' + i.count);
    }
    out.push('```');
    out.push('');
  }

  if (r.topJsNoise && r.topJsNoise.length) {
    out.push('## Filtered noise (chrome-extension, userscript, host-CDN/analytics)');
    out.push('```');
    for (const i of r.topJsNoise.slice(0, 8)) {
      const trimmed = i.key.length > 70 ? i.key.slice(0, 67) + '...' : i.key;
      out.push(trimmed + ' | ' + fmt(i.totalUs) + ' ms x' + i.count);
    }
    out.push('```');
    out.push('');
  }

  return out.join('\n');
}

// ─── Main ─────────────────────────────────────────────────────────────
async function main() {
  const args = parseArgs(process.argv);
  const text = await readInput(args.file);
  const sizeBytes = Buffer.byteLength(text, 'utf-8');
  const obj = JSON.parse(text);
  const traceEvents = Array.isArray(obj) ? obj : (obj.traceEvents || obj.events || []);
  if (!Array.isArray(traceEvents)) throw new Error('Unrecognized trace JSON format');

  const meta = extractMetadata(traceEvents);
  const res = aggregate(traceEvents, {
    mainPid: meta.mainThread && meta.mainThread.pid,
    mainTid: meta.mainThread && meta.mainThread.tid,
    onlyMain: args.onlyMain,
    longTaskThresholdUs: args.longTaskMs * 1000,
    topN: Math.min(100, Math.max(5, args.topN)),
  });

  const output = buildOutput(res, meta);
  const md = buildMarkdown(output, {
    name: args.file ? args.file.split(/[\\/]/).pop() : 'stdin',
    sizeMB: sizeBytes / 1024 / 1024,
  });
  process.stdout.write(md);
}

main().catch(e => { console.error('Error:', e.message); process.exit(1); });
