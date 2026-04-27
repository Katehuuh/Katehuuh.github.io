#!/usr/bin/env python3
"""Auto-crop CatBench raster assets to a consistent square framing.

Samples the four corner pixels for a background colour, finds the bounding
box of pixels that differ from that background, crops with a small padding,
then pads the crop back to a square in the same background. Result: kittens
range from tiny to huge in their original files but render at consistent
size in the grid cells.

Idempotent: a cropped + squared file converges on a stable shape, so this
can run in CI on every push. SVG and GIF files are skipped (vector and
animated, respectively).
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "demos" / "CatBench" / "assets"

CROP_EXTS = {".png", ".jpg", ".jpeg"}
PADDING_PCT = 0.04
DIFF_THRESHOLD = 12   # 0..255, per-channel diff to count as "subject"
MIN_CROP_RATIO = 0.92 # don't crop if the bbox already covers >= 92% of the image


def detect_bg(rgb: Image.Image) -> tuple[int, int, int]:
    w, h = rgb.size
    corners = [rgb.getpixel(p) for p in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1))]
    return tuple(int(sum(c[i] for c in corners) / len(corners)) for i in range(3))


def autocrop(img: Image.Image) -> tuple[Image.Image, tuple[int, int, int]]:
    rgb = img.convert("RGB")
    bg = detect_bg(rgb)
    diff = ImageChops.difference(rgb, Image.new("RGB", rgb.size, bg)).convert("L")
    mask = diff.point(lambda p: 255 if p > DIFF_THRESHOLD else 0)
    bbox = mask.getbbox()
    if not bbox:
        return img, bg

    bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]
    iw, ih = img.size
    if bw / iw >= MIN_CROP_RATIO and bh / ih >= MIN_CROP_RATIO:
        return img, bg

    px = int(bw * PADDING_PCT)
    py = int(bh * PADDING_PCT)
    bbox = (
        max(0, bbox[0] - px),
        max(0, bbox[1] - py),
        min(iw, bbox[2] + px),
        min(ih, bbox[3] + py),
    )
    return img.crop(bbox), bg


def square_pad(img: Image.Image, bg: tuple[int, int, int]) -> Image.Image:
    w, h = img.size
    if w == h:
        return img
    side = max(w, h)
    canvas = Image.new("RGB", (side, side), bg)
    canvas.paste(img.convert("RGB"), ((side - w) // 2, (side - h) // 2))
    return canvas


def process(path: Path) -> bool:
    img = Image.open(path)
    orig_size = img.size
    cropped, bg = autocrop(img)
    squared = square_pad(cropped, bg)
    if squared.size == orig_size:
        return False

    suffix = path.suffix.lower()
    save_kwargs: dict = {}
    if suffix in (".jpg", ".jpeg"):
        save_kwargs = {"quality": 92, "optimize": True}
    elif suffix == ".png":
        save_kwargs = {"optimize": True}
    squared.save(path, **save_kwargs)
    print(f"  cropped {path.name} {orig_size} -> {squared.size}")
    return True


def main() -> int:
    if not ASSETS.is_dir():
        print("no demos/CatBench/assets directory")
        return 0
    n_modified = 0
    n_seen = 0
    for f in sorted(ASSETS.iterdir()):
        if f.suffix.lower() not in CROP_EXTS:
            continue
        n_seen += 1
        try:
            if process(f):
                n_modified += 1
        except Exception as e:
            print(f"  ! {f.name}: {type(e).__name__}: {e}", file=sys.stderr)
    print(f"autocrop: {n_modified}/{n_seen} files modified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
