#!/usr/bin/env python3
"""Scan demos/ and emit demos/manifest.json so the home page gallery doesn't
have to hit the GitHub Contents API (anonymous limit: 60/hr/IP, easy to blow
through during normal testing). The page falls back to the API only if the
manifest is missing or stale.

Each entry:
  - name:     display key (filename stem for files, dir name for dirs)
  - type:     "file" or "dir"
  - filename: file's .html name (only for type=file; dirs serve index.html)

Note: the first-commit-date is intentionally NOT stored here. It's embedded
into each thumbnail JPEG's COM marker by `embed_thumb_dates.py`, so the
home page reads it from the binary it's already fetching for <img>.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEMOS_DIR = ROOT / "demos"
OUT = DEMOS_DIR / "manifest.json"


def first_commit_iso(rel_path: str) -> str:
    """Used only for sort order — newest demos at the top of the manifest.
    Not written into the manifest itself."""
    try:
        result = subprocess.run(
            ["git", "log", "--reverse", "--format=%aI", "--", rel_path],
            capture_output=True, text=True, cwd=ROOT, check=False,
        )
        first = (result.stdout or "").strip().split("\n", 1)[0].strip()
        if first:
            return first
    except Exception:
        pass
    return ""


def main() -> int:
    if not DEMOS_DIR.is_dir():
        print("no demos/ directory")
        return 0

    items: list[tuple[str, dict]] = []  # (sort_key, entry)
    for entry in sorted(DEMOS_DIR.iterdir()):
        if entry.name.startswith(".") or entry.name == "manifest.json":
            continue
        rel = entry.relative_to(ROOT).as_posix()
        if entry.is_dir():
            if (entry / ".gallery-exclude").exists():
                continue
            if (entry / "index.html").is_file():
                items.append((first_commit_iso(rel), {"name": entry.name, "type": "dir"}))
        elif entry.is_file() and entry.suffix.lower() in (".html", ".htm"):
            items.append((first_commit_iso(rel),
                          {"name": entry.stem, "type": "file", "filename": entry.name}))

    items.sort(key=lambda kv: kv[0], reverse=True)
    payload = {"demos": [entry for _, entry in items]}

    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"demos manifest: {len(items)} entr{'y' if len(items) == 1 else 'ies'} -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
