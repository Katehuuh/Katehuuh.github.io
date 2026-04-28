#!/usr/bin/env python3
"""Embed each demo's first-commit-date into its thumbnail JPEG via the
JPEG COM marker (0xFFFE). Runs after screenshot_thumbs.mjs.

The home page reads this binary tag to display creation dates without
hitting the GitHub commits API at runtime — the thumbnail fetch the
browser already makes for <img> doubles as the date source.

JPEG segment format after SOI: FF <marker> <2-byte big-endian length> <payload>.
COM marker is one of the few that's free-form text; we just inject one.
"""
from __future__ import annotations

import sys
from pathlib import Path

from git_helpers import first_commit_iso

ROOT = Path(__file__).resolve().parent.parent
THUMBS = ROOT / "assets" / "thumbs"
DEMOS = ROOT / "demos"

SOI = b"\xff\xd8"
COM_MARKER = 0xFE
SOS_MARKER = 0xDA
# JPEG markers that occupy 2 bytes total (no length field): SOI/EOI, RST0-RST7, TEM.
# DRI (0xDD) is length-prefixed (payload = 4 bytes) — do NOT add it here.
STANDALONE = {0xD0, 0xD1, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8, 0xD9, 0x01}


def strip_existing_coms(data: bytes) -> bytes:
    """Walk JPEG segments and drop any pre-existing COM marker so re-runs
    don't compound them. Stops at SOS (entropy-coded payload follows)."""
    if not data.startswith(SOI):
        return data
    out = bytearray(data[:2])
    i = 2
    while i + 1 < len(data):
        if data[i] != 0xFF:
            out += data[i:]; break
        marker = data[i + 1]
        if marker == SOS_MARKER:
            out += data[i:]; break
        if marker in STANDALONE:
            out += data[i:i + 2]; i += 2; continue
        if i + 3 >= len(data):
            out += data[i:]; break
        seg_len = (data[i + 2] << 8) | data[i + 3]
        if marker == COM_MARKER:
            i += 2 + seg_len
            continue
        out += data[i:i + 2 + seg_len]
        i += 2 + seg_len
    return bytes(out)


def embed_jpeg_comment(path: Path, text: str) -> bool:
    data = path.read_bytes()
    if not data.startswith(SOI):
        return False
    payload = text.encode("utf-8")
    if len(payload) > 65533:
        return False
    cleaned = strip_existing_coms(data)
    marker = b"\xff\xfe" + (len(payload) + 2).to_bytes(2, "big") + payload
    path.write_bytes(cleaned[:2] + marker + cleaned[2:])
    return True


def find_demo_html(thumb_stem: str) -> Path | None:
    flat = DEMOS / f"{thumb_stem}.html"
    if flat.is_file():
        return flat
    folder = DEMOS / thumb_stem / "index.html"
    if folder.is_file():
        return folder
    return None


def main() -> int:
    if not THUMBS.is_dir():
        print("no thumbs directory")
        return 0
    count, skipped = 0, []
    for jpg in sorted(THUMBS.glob("*.jpg")):
        demo = find_demo_html(jpg.stem)
        if not demo:
            skipped.append((jpg.name, "no matching demo HTML"))
            continue
        rel = demo.relative_to(ROOT).as_posix()
        date = first_commit_iso(rel, ROOT)
        if not date:
            skipped.append((jpg.name, "no git history"))
            continue
        if embed_jpeg_comment(jpg, date):
            count += 1
        else:
            skipped.append((jpg.name, "not a JPEG / payload too large"))
    print(f"embedded dates into {count} thumbnails")
    for name, reason in skipped:
        print(f"  skipped {name}: {reason}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
