#!/usr/bin/env python3
"""Auto-crop CatBench raster assets to a 1:1 square around the subject.

Uses edge flood-fill plus row/column margin trimming (drops pale interior
columns/rows that never touch the border, e.g. matplotlib wash rects).
"""
from __future__ import annotations

import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "demos" / "CatBench" / "assets"

CROP_EXTS = {".png", ".jpg", ".jpeg"}
BG_TOLERANCE = 18
EDGE_INK_RATIO = 0.02
PADDING_PCT = 0.02


def detect_bg(rgb: np.ndarray) -> tuple[int, int, int]:
    h, w, _ = rgb.shape
    corners = np.array(
        [rgb[0, 0], rgb[0, w - 1], rgb[h - 1, 0], rgb[h - 1, w - 1]],
        dtype=np.int16,
    )
    return tuple(int(corners[:, i].mean()) for i in range(3))


def near_bg_mask(rgb: np.ndarray, bg: tuple[int, int, int], tol: int) -> np.ndarray:
    return np.abs(rgb.astype(np.int16) - np.array(bg, dtype=np.int16)).max(axis=2) <= tol


def flood_background(near_bg: np.ndarray) -> np.ndarray:
    h, w = near_bg.shape
    visited = np.zeros((h, w), dtype=bool)
    q: deque[tuple[int, int]] = deque()

    for x in range(w):
        for y in (0, h - 1):
            if near_bg[y, x] and not visited[y, x]:
                visited[y, x] = True
                q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if near_bg[y, x] and not visited[y, x]:
                visited[y, x] = True
                q.append((y, x))

    while q:
        y, x = q.popleft()
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx] and near_bg[ny, nx]:
                visited[ny, nx] = True
                q.append((ny, nx))

    return visited


def trim_bbox(near_bg: np.ndarray, edge_ratio: float) -> tuple[int, int, int, int] | None:
    ink = ~near_bg
    rows = np.where(ink.mean(axis=1) > edge_ratio)[0]
    cols = np.where(ink.mean(axis=0) > edge_ratio)[0]
    if rows.size == 0 or cols.size == 0:
        return None
    return int(cols[0]), int(rows[0]), int(cols[-1]) + 1, int(rows[-1]) + 1


def intersect(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])


def pad_bbox(bbox: tuple[int, int, int, int], size: tuple[int, int]) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = bbox
    bw, bh = x1 - x0, y1 - y0
    px, py = int(bw * PADDING_PCT), int(bh * PADDING_PCT)
    iw, ih = size
    return (
        max(0, x0 - px),
        max(0, y0 - py),
        min(iw, x1 + px),
        min(ih, y1 + py),
    )


def subject_bbox(rgb: np.ndarray) -> tuple[int, int, int, int] | None:
    bg = detect_bg(rgb)
    near_bg = near_bg_mask(rgb, bg, BG_TOLERANCE)
    flooded = flood_background(near_bg)
    ys, xs = np.where(~flooded)
    if ys.size == 0:
        return None
    flood_box = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
    trim_box = trim_bbox(near_bg, EDGE_INK_RATIO)
    if trim_box:
        x0, y0, x1, y1 = intersect(flood_box, trim_box)
        if x1 <= x0 or y1 <= y0:
            bbox = flood_box
        else:
            bbox = (x0, y0, x1, y1)
    else:
        bbox = flood_box
    return pad_bbox(bbox, (rgb.shape[1], rgb.shape[0]))


def square_crop(img: Image.Image, bbox: tuple[int, int, int, int]) -> Image.Image:
    x0, y0, x1, y1 = bbox
    bw, bh = x1 - x0, y1 - y0
    cx = (x0 + x1) / 2.0
    cy = (y0 + y1) / 2.0
    side = max(bw, bh)
    left = int(round(cx - side / 2))
    top = int(round(cy - side / 2))
    right = left + side
    bottom = top + side

    iw, ih = img.size
    if left < 0:
        right -= left
        left = 0
    if top < 0:
        bottom -= top
        top = 0
    if right > iw:
        left = max(0, left - (right - iw))
        right = iw
    if bottom > ih:
        top = max(0, top - (bottom - ih))
        bottom = ih

    side = min(right - left, bottom - top)
    return img.crop((left, top, left + side, top + side))


def autocrop(img: Image.Image) -> Image.Image:
    rgb = np.asarray(img.convert("RGB"))
    bbox = subject_bbox(rgb)
    if not bbox:
        return img
    return square_crop(img, bbox)


def process(path: Path) -> bool:
    img = Image.open(path)
    orig_size = img.size
    result = autocrop(img)
    if result.size == orig_size and result.tobytes() == img.convert("RGB").tobytes():
        return False

    suffix = path.suffix.lower()
    save_kwargs: dict = {}
    if suffix in (".jpg", ".jpeg"):
        save_kwargs = {"quality": 92, "optimize": True}
    elif suffix == ".png":
        save_kwargs = {"optimize": True}
    result.save(path, **save_kwargs)
    print(f"  cropped {path.name} {orig_size} -> {result.size}")
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