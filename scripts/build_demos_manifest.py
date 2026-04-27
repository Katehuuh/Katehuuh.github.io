#!/usr/bin/env python3
"""Scan demos/ and emit demos/manifest.json so the home page gallery doesn't
have to hit the GitHub Contents API (anonymous limit: 60/hr/IP, easy to blow
through during normal testing). The page falls back to the API only if the
manifest is missing or stale.

Each entry:
  - name:       display key (filename stem for files, dir name for dirs)
  - type:       "file" or "dir"
  - filename:   file's .html name (only for type=file; dirs serve index.html)
  - first_seen: ISO timestamp of the file/dir's earliest commit, used so the
                gallery can order newest-first without per-file commit calls.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEMOS_DIR = ROOT / "demos"
OUT = DEMOS_DIR / "manifest.json"


def first_commit_iso(rel_path: str) -> str:
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
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def main() -> int:
    if not DEMOS_DIR.is_dir():
        print("no demos/ directory")
        return 0

    items: list[dict] = []
    for entry in sorted(DEMOS_DIR.iterdir()):
        if entry.name.startswith(".") or entry.name == "manifest.json":
            continue
        rel = entry.relative_to(ROOT).as_posix()
        if entry.is_dir():
            # Sentinel: drop a `.gallery-exclude` file in a demo folder to
            # keep its index.html at /demos/<name>/ but hide the card.
            if (entry / ".gallery-exclude").exists():
                continue
            if (entry / "index.html").is_file():
                items.append({
                    "name": entry.name,
                    "type": "dir",
                    "first_seen": first_commit_iso(rel),
                })
        elif entry.is_file() and entry.suffix.lower() in (".html", ".htm"):
            items.append({
                "name": entry.stem,
                "type": "file",
                "filename": entry.name,
                "first_seen": first_commit_iso(rel),
            })

    # Newest first commit on the left, oldest on the right.
    items.sort(key=lambda x: x.get("first_seen", ""), reverse=True)

    OUT.write_text(json.dumps({"demos": items}, indent=2) + "\n", encoding="utf-8")
    print(f"demos manifest: {len(items)} entr{'y' if len(items) == 1 else 'ies'} -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
