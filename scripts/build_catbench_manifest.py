#!/usr/bin/env python3
"""Scan CatBench/assets/ and emit CatBench/manifest.json.

Models are sorted by the date their files were first committed: most recent
on the left of the grid, earliest on the right. So a fresh upload jumps to
the leftmost column.


Single drop folder. File kind is determined by extension plus an optional
`-svg` or `-python` suffix on raster filenames:

  <model>.svg                  -> SVG cell, vector
  <model>-svg.{png|jpg|gif}    -> SVG cell, raster (when the model only
                                  produced an image, including animated GIF)
  <model>.py                   -> Python source (auto-rendered if no raster)
  <model>-python.{png|jpg|gif} -> Python output, raster
  <model>.{png|jpg|gif}        -> bare raster, treated as Python output

Filename stem is lowercased, spaces/underscores collapse to dashes.
`GpT-5.5.svg`, `gpt 5.5.py`, `GPT_5.5-python.jpg` all join as model `gpt-5.5`.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATBENCH = ROOT / "demos" / "CatBench"
ASSETS_DIR = CATBENCH / "assets"
RENDER_SCRIPT = ROOT / "scripts" / "render_python.py"

RASTER_EXTS = {".png", ".jpg", ".jpeg", ".gif"}
SVG_RASTER_SUFFIX = "-svg"
PY_RASTER_SUFFIX = "-python"


def normalize(stem: str) -> str:
    return re.sub(r"[_\s]+", "-", stem.strip().lower())


def display_name(stem: str) -> str:
    return re.sub(r"[_\s]+", " ", stem.strip())


def file_first_commit(path: Path) -> str:
    """ISO date of the earliest commit touching this file. Falls back to now
    for uncommitted files so they sort to the leftmost column."""
    rel = path.relative_to(ROOT).as_posix()
    try:
        result = subprocess.run(
            ["git", "log", "--reverse", "--format=%aI", "--", rel],
            capture_output=True, text=True, cwd=ROOT, check=False,
        )
        first = (result.stdout or "").strip().split("\n", 1)[0].strip()
        if first:
            return first
    except Exception:
        pass
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def looks_like_svg(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            head = f.read(1024).lstrip("﻿").lstrip()
    except OSError:
        return False
    return head.startswith("<?xml") or head.startswith("<svg") or head.startswith("<!--")


def scan() -> dict:
    models: dict[str, dict] = {}
    if not ASSETS_DIR.is_dir():
        return models

    # display_name candidates per key: higher priority wins. .py is the
    # cleanest source of a model name, so it always beats raster suffixes
    # whose stems are lowercased on the user's side.
    PRI_PY = 4
    PRI_RASTER = 3   # bare or -python or -svg raster files
    PRI_SVG_FILE = 2
    name_pri: dict[str, int] = {}

    def propose(key: str, priority: int, stem: str) -> None:
        if key not in name_pri or priority > name_pri[key]:
            name_pri[key] = priority
            models[key]["display_name"] = display_name(stem)

    if not ASSETS_DIR.is_dir():
        return models

    for f in sorted(ASSETS_DIR.iterdir()):
        ext = f.suffix.lower()
        stem = f.stem

        if ext == ".svg":
            key = normalize(stem)
            models.setdefault(key, {"display_name": ""})
            if looks_like_svg(f):
                models[key]["svg"] = f"assets/{f.name}"
                models[key].pop("svg_error", None)
            elif "svg" not in models[key]:
                models[key]["svg_error"] = "file is not valid SVG markup"
                print(f"  ! svg invalid: {f.name}", file=sys.stderr)
            propose(key, PRI_SVG_FILE, stem)

        elif ext == ".py":
            key = normalize(stem)
            models.setdefault(key, {"display_name": ""})
            models[key]["python_source"] = f"assets/{f.name}"
            propose(key, PRI_PY, stem)

        elif ext in RASTER_EXTS:
            stem_norm = normalize(stem)
            if stem_norm.endswith(SVG_RASTER_SUFFIX):
                base_norm = stem_norm[: -len(SVG_RASTER_SUFFIX)]
                models.setdefault(base_norm, {"display_name": ""})
                if "svg" not in models[base_norm]:
                    models[base_norm]["svg"] = f"assets/{f.name}"
                base_stem = re.sub(r"-svg$", "", stem, flags=re.IGNORECASE)
                propose(base_norm, PRI_RASTER, base_stem)
            elif stem_norm.endswith(PY_RASTER_SUFFIX):
                base_norm = stem_norm[: -len(PY_RASTER_SUFFIX)]
                models.setdefault(base_norm, {"display_name": ""})
                if "python_render" not in models[base_norm]:
                    models[base_norm]["python_render"] = f"assets/{f.name}"
                base_stem = re.sub(r"-python$", "", stem, flags=re.IGNORECASE)
                propose(base_norm, PRI_RASTER, base_stem)
            else:
                key = normalize(stem)
                models.setdefault(key, {"display_name": ""})
                if "python_render" not in models[key]:
                    models[key]["python_render"] = f"assets/{f.name}"
                propose(key, PRI_RASTER, stem)

    return models


def render_missing(models: dict) -> None:
    for key, m in models.items():
        if "python_source" not in m or "python_render" in m:
            continue
        src = CATBENCH / m["python_source"]
        # Auto-render output: <stem>-python.jpg in the same folder
        out = src.with_name(f"{src.stem}-python.jpg")
        cmd = [sys.executable, str(RENDER_SCRIPT), str(src), str(out)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0 and out.exists():
            m["python_render"] = f"assets/{out.name}"
        else:
            err = (result.stderr or result.stdout or "").strip()
            m["python_error"] = err.splitlines()[-1] if err else f"render exit {result.returncode}"
            print(f"  ! render failed for {key}: {m['python_error']}", file=sys.stderr)


def annotate_first_seen(models: dict) -> None:
    """Take the earliest first-commit date across each model's files."""
    for key, m in models.items():
        candidates: list[str] = []
        for field in ("svg", "python_source", "python_render"):
            if field in m:
                p = CATBENCH / m[field]
                if p.exists():
                    candidates.append(file_first_commit(p))
        m["_first_seen"] = min(candidates) if candidates else datetime.now(timezone.utc).isoformat(timespec="seconds")


def main() -> int:
    models = scan()
    render_missing(models)
    annotate_first_seen(models)

    # Sort: newest first commit on the left, oldest on the right.
    ordered = sorted(models.items(), key=lambda kv: kv[1].get("_first_seen", ""), reverse=True)
    manifest = {
        "models": dict(ordered),
        "prompts": {
            "svg": "Create a detailed SVG image of a cute kitten.",
            "python": "Write a Python script that draws a cute kitten using matplotlib.",
        },
    }

    out_path = CATBENCH / "manifest.json"
    out_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"manifest: {len(models)} models -> {out_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
