#!/usr/bin/env python3
"""Scan demos/ and emit demos/manifest.json so the home page gallery doesn't
have to hit the GitHub Contents API (anonymous limit: 60/hr/IP, easy to blow
through during normal testing). The page falls back to the API only if the
manifest is missing or stale.

Each entry:
  - name:        display key (filename stem for files, dir name for dirs)
  - type:        "file" or "dir"
  - filename:    file's .html name (only for type=file; dirs serve index.html)
  - description: extracted from the demo's <meta name="description"> if present

Note: the first-commit-date is intentionally NOT stored here. It's embedded
into each thumbnail JPEG's COM marker by `embed_thumb_dates.py`, so the
home page reads it from the binary it's already fetching for <img>.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from git_helpers import first_commit_iso

ROOT = Path(__file__).resolve().parent.parent
DEMOS_DIR = ROOT / "demos"
OUT = DEMOS_DIR / "manifest.json"

# Conservative <meta name="description"> matcher: only the first 8 KB of the
# file (descriptions live in <head>) and tolerant of single/double quotes and
# attribute order variants. Returns None if not found.
_META_RE = re.compile(
    r"""<meta\s+[^>]*name\s*=\s*['"]description['"][^>]*content\s*=\s*['"]([^'"]+)['"]""",
    re.IGNORECASE,
)
_META_RE_REVERSED = re.compile(
    r"""<meta\s+[^>]*content\s*=\s*['"]([^'"]+)['"][^>]*name\s*=\s*['"]description['"]""",
    re.IGNORECASE,
)


def extract_description(html_path: Path) -> str | None:
    try:
        head = html_path.read_text(encoding="utf-8", errors="ignore")[:8192]
    except OSError:
        return None
    m = _META_RE.search(head) or _META_RE_REVERSED.search(head)
    return m.group(1).strip() if m else None


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
            index = entry / "index.html"
            if index.is_file():
                e: dict = {"name": entry.name, "type": "dir"}
                desc = extract_description(index)
                if desc:
                    e["description"] = desc
                items.append((first_commit_iso(rel, ROOT) or "", e))
        elif entry.is_file() and entry.suffix.lower() in (".html", ".htm"):
            e = {"name": entry.stem, "type": "file", "filename": entry.name}
            desc = extract_description(entry)
            if desc:
                e["description"] = desc
            items.append((first_commit_iso(rel, ROOT) or "", e))

    items.sort(key=lambda kv: kv[0], reverse=True)
    payload = {"demos": [entry for _, entry in items]}

    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"demos manifest: {len(items)} entr{'y' if len(items) == 1 else 'ies'} -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
