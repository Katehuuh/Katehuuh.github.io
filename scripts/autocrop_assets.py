#!/usr/bin/env python3
"""Auto-crop CatBench raster assets to a tight 1:1 square around the subject.

Flood-fills background from image edges (corner colour + tolerance), also
treats pale low-saturation pixels as background. Crops to the subject bbox
with no padding, then extracts the smallest centred square. No margin fill.
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
BG_TOLERANCE = 20       # per-channel diff from edge bg colour
PALE_LUMA = 230         # 0-255, pixels brighter than this...
PALE_SAT = 0.14         # ...and less saturated than this count as background


def detect_bg(rgb: np.ndarray) -> tuple[int, int, int]:
    h, w, _ = rgb.shape
    corners = np.array(
        [rgb[0, 0], rgb[0, w - 1], rgb[h - 1, 0], rgb[h - 1, w - 1]],
        dtype=np.int16,
    )
    return tuple(int(corners[:, i].mean()) for i in range(3))


def flood_background(rgb: np.ndarray, bg: tuple[int, int, int], tol: int) -> np.ndarray:
    h, w, _ = rgb.shape
    bg_arr = np.array(bg, dtype=np.int16)
    close = np.abs(rgb.astype(np.int16) - bg_arr).max(axis=2) <= tol
    visited = np.zeros((h, w), dtype=bool)
    q: deque[tuple[int, int]] = deque()

    for x in range(w):
        for y in (0, h - 1):
            if close[y, x] and not visited[y, x]:
                visited[y, x] = True
                q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if close[y, x] and not visited[y, x]:
                visited[y, x] = True
                q.append((y, x))

    while q:
        y, x = q.popleft()
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx] and close[ny, nx]:
                visited[ny, nx] = True
                q.append((ny, nx))

    return visited


def pale_background(rgb: np.ndarray) -> np.ndarray:
    px = rgb.astype(np.float32) / 255.0
    maxc = px.max(axis=2)
    minc = px.min(axis=2)
    sat = np.divide(maxc - minc, maxc, out=np.zeros_like(maxc), where=maxc > 0)
    luma = 0.299 * px[:, :, 0] + 0.587 * px[:, :, 1] + 0.114 * px[:, :, 2]
    return (luma >= PALE_LUMA / 255.0) & (sat <= PALE_SAT)


def subject_bbox(rgb: np.ndarray) -> tuple[int, int, int, int] | None:
    bg = detect_bg(rgb)
    is_bg = flood_background(rgb, bg, BG_TOLERANCE) | pale_background(rgb)
    ys, xs = np.where(~is_bg)
    if ys.size == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


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
    right = left + side
    bottom = top + side
    return img.crop((left, top, right, bottom))


def autocrop(img: Image.Image) -> Image.Image:
    rgb = np.asarray(img.convert("RGB"))
    bbox = subject_bbox(rgb)
    if not bbox:
        return img
    cropped = img.crop(bbox)
    return square_crop(cropped, (0, 0, cropped.size[0], cropped.size[1]))


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