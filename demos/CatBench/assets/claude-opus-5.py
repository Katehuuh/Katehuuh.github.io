#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A cute kitten, drawn with matplotlib.

Everything is built from Bezier outlines, gradient fills and soft shadows --
no images, no fonts, no data files. Run it and it writes ``kitten.png``.

Design notes
------------
* All geometry is authored on a 512 x 512 "canvas" with y pointing DOWN
  (the way one sketches on paper). ``path`` converts to matplotlib's y-up
  data space while parsing, so the numbers below read like a drawing, and
  ``mirror=True`` reflects a shape about the centre line for symmetry.
* ``grad`` paints a real gradient by rendering a small RGBA ramp with
  ``imshow`` and clipping it to a patch -- matplotlib has no native
  gradient fill, and flat colours make fur look like plastic.
* ``soft_blob`` stands in for a Gaussian blur (drop shadow, blush,
  ambient occlusion) using a smoothstep radial alpha ramp.
"""

import math

import numpy as np
import matplotlib

matplotlib.use("Agg")  # headless rendering

import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Ellipse, Circle
from matplotlib.colors import to_rgb

# --------------------------------------------------------------------------
# canvas
# --------------------------------------------------------------------------
SIZE = 512.0          # design units
FIG_IN = 6.4          # figure edge, inches
U = 72.0 * FIG_IN / SIZE      # points per design unit -> 1:1 line widths
K = 0.5523                    # circle-from-Bezier magic number


# --------------------------------------------------------------------------
# a very small SVG-ish path parser (M, L, C, Z -- absolute only)
# --------------------------------------------------------------------------
def _tokens(d):
    """Split a path string into command letters and numbers."""
    out, buf = [], ""
    for ch in d:
        if ch in "MLCZ":
            if buf:
                out.append(buf)
                buf = ""
            out.append(ch)
        elif ch in " ,\t\n":
            if buf:
                out.append(buf)
                buf = ""
        else:
            buf += ch
    if buf:
        out.append(buf)
    return out


def path(d, mirror=False):
    """Build a matplotlib Path from a path string, flipping y (and x)."""
    toks = _tokens(d)
    verts, codes = [], []
    i, cmd = 0, None
    while i < len(toks):
        t = toks[i]
        if t in "MLCZ":
            cmd = t
            i += 1
            if cmd == "Z":
                verts.append((0.0, 0.0))
                codes.append(Path.CLOSEPOLY)
                cmd = None
                continue
        if cmd is None:
            i += 1
            continue
        if cmd in "ML":
            verts.append((float(toks[i]), float(toks[i + 1])))
            codes.append(Path.MOVETO if cmd == "M" else Path.LINETO)
            i += 2
            if cmd == "M":                       # repeats after M are lines
                cmd = "L"
        else:                                    # cubic
            for k in range(3):
                verts.append((float(toks[i + 2 * k]), float(toks[i + 2 * k + 1])))
                codes.append(Path.CURVE4)
            i += 6
    pts = np.asarray(verts, dtype=float)
    if mirror:
        pts[:, 0] = SIZE - pts[:, 0]
    pts[:, 1] = SIZE - pts[:, 1]                 # y down -> y up
    return Path(pts, codes)


def epath(cx, cy, rx, ry):
    """An ellipse as a four-cubic path string, in design space."""
    return ("M {} {} C {} {} {} {} {} {} C {} {} {} {} {} {} "
            "C {} {} {} {} {} {} C {} {} {} {} {} {} Z").format(
        cx, cy - ry,
        cx + rx * K, cy - ry, cx + rx, cy - ry * K, cx + rx, cy,
        cx + rx, cy + ry * K, cx + rx * K, cy + ry, cx, cy + ry,
        cx - rx * K, cy + ry, cx - rx, cy + ry * K, cx - rx, cy,
        cx - rx, cy - ry * K, cx - rx * K, cy - ry, cx, cy - ry)


def P(x, y):
    """A single design-space point in matplotlib data space."""
    return (x, SIZE - y)


# --------------------------------------------------------------------------
# figure
# --------------------------------------------------------------------------
fig = plt.figure(figsize=(FIG_IN, FIG_IN), dpi=150)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, SIZE)
ax.set_ylim(0, SIZE)
ax.set_aspect("equal")
ax.axis("off")


# --------------------------------------------------------------------------
# painting helpers
# --------------------------------------------------------------------------
def ramp(stops, t):
    """Interpolate (position, '#rrggbb', alpha) stops over t -> RGBA array."""
    pos = np.array([s[0] for s in stops], dtype=float)
    cols = np.array([to_rgb(s[1]) for s in stops], dtype=float)
    alp = np.array([s[2] for s in stops], dtype=float)
    out = np.empty(t.shape + (4,), dtype=float)
    for c in range(3):
        out[..., c] = np.interp(t, pos, cols[:, c])
    out[..., 3] = np.interp(t, pos, alp)
    return out


def shape(p, color, z, alpha=1.0, clip=None):
    """Flat-filled patch."""
    pt = PathPatch(p, facecolor=color, edgecolor="none", alpha=alpha,
                   zorder=z, antialiased=True)
    ax.add_patch(pt)
    if clip is not None:
        pt.set_clip_path(clip)
    return pt


def outline(p, color, w, z, alpha=1.0, clip=None):
    """Stroked (unfilled) patch, round caps and joins."""
    pt = PathPatch(p, facecolor="none", edgecolor=color, lw=w * U,
                   capstyle="round", joinstyle="round", alpha=alpha, zorder=z)
    ax.add_patch(pt)
    if clip is not None:
        pt.set_clip_path(clip)
    return pt


def grad(p, stops, z, kind="radial", cx=0.5, cy=0.5, r=0.75,
         ang=90.0, clip=None, res=300):
    """
    Fill a path with a gradient.

    Coordinates follow the drawing: fractions of the shape's bounding box
    with (0, 0) at its TOP-left.  kind='radial' spreads the stops from
    (cx, cy) out to radius r; kind='linear' runs along ang degrees, where
    90 means top -> bottom.
    """
    holder = PathPatch(p, facecolor="none", edgecolor="none", zorder=z)
    ax.add_patch(holder)
    bb = p.get_extents()
    X, Y = np.meshgrid(np.linspace(0.0, 1.0, res), np.linspace(0.0, 1.0, res))
    if kind == "radial":
        t = np.sqrt(((X - cx) / r) ** 2 + ((Y - cy) / r) ** 2)
    else:
        a = math.radians(ang)
        t = X * math.cos(a) + Y * math.sin(a)
        t = (t - t.min()) / max(t.max() - t.min(), 1e-9)
    im = ax.imshow(ramp(stops, np.clip(t, 0.0, 1.0)),
                   extent=(bb.x0, bb.x1, bb.y0, bb.y1), origin="upper",
                   zorder=z, aspect="auto", interpolation="bilinear")
    im.set_clip_path(clip if clip is not None else holder)
    return holder


def soft_blob(cx, cy, rx, ry, color, alpha, z, hardness=0.62, res=170):
    """A blurred ellipse -- shadows, blush, ambient occlusion."""
    ext = 1.5
    g = np.linspace(-ext, ext, res)
    X, Y = np.meshgrid(g, g)
    d = np.sqrt(X ** 2 + Y ** 2)
    t = np.clip((1.15 - d) / (1.15 - hardness), 0.0, 1.0)
    rgba = np.zeros(X.shape + (4,))
    rgba[..., :3] = to_rgb(color)
    rgba[..., 3] = alpha * t * t * (3.0 - 2.0 * t)      # smoothstep falloff
    x, y = P(cx, cy)
    ax.imshow(rgba, extent=(x - rx * ext, x + rx * ext,
                            y - ry * ext, y + ry * ext),
              origin="lower", zorder=z, aspect="auto",
              interpolation="bilinear")


def ell(cx, cy, rx, ry, color, z, alpha=1.0, rot=0.0, clip=None):
    """Ellipse in design space (rot in degrees, positive = clockwise)."""
    e = Ellipse(P(cx, cy), 2 * rx, 2 * ry, angle=-rot, facecolor=color,
                edgecolor="none", alpha=alpha, zorder=z)
    ax.add_patch(e)
    if clip is not None:
        e.set_clip_path(clip)
    return e


def dot(cx, cy, r, color, z, alpha=1.0, clip=None):
    c = Circle(P(cx, cy), r, facecolor=color, edgecolor="none",
               alpha=alpha, zorder=z)
    ax.add_patch(c)
    if clip is not None:
        c.set_clip_path(clip)
    return c


def strokes(dlist, color, w, z, alpha=1.0, clip=None, mirror_too=False):
    for d in dlist:
        outline(path(d), color, w, z, alpha, clip)
        if mirror_too:
            outline(path(d, mirror=True), color, w, z, alpha, clip)


# --------------------------------------------------------------------------
# geometry
# --------------------------------------------------------------------------
HEAD = ("M 256 114 C 325 114 380 168 380 234 C 380 292 344 336 296 348 "
        "C 283 352 270 354 256 354 C 242 354 229 352 216 348 "
        "C 168 336 132 292 132 234 C 132 168 187 114 256 114 Z")
HEAD_RIM = ("M 256 110 C 327 110 384 166 384 234 C 384 294 347 339 297 352 "
            "C 284 356 270 358 256 358 C 242 358 228 356 215 352 "
            "C 165 339 128 294 128 234 C 128 166 185 110 256 110 Z")
BODY = ("M 256 288 C 196 290 158 330 146 386 C 136 434 156 476 204 480 "
        "L 308 480 C 356 476 376 434 366 386 C 354 330 316 288 256 288 Z")
BODY_RIM = ("M 256 284 C 194 286 154 328 142 384 C 132 434 152 480 204 484 "
            "L 308 484 C 360 480 380 434 370 384 C 358 328 318 284 256 284 Z")
TAIL = ("M 330 392 C 408 392 460 424 464 464 C 466 488 440 500 414 494 "
        "C 396 490 392 476 402 472 C 416 466 422 456 418 442 "
        "C 408 424 370 416 330 434 Z")
TAIL_IN = ("M 332 394 C 407 394 457 425 461 464 C 463 486 439 497 414 491 "
           "C 398 488 395 476 403 472 C 418 465 425 455 420 440 "
           "C 409 421 370 414 332 432 Z")
CHEST = ("M 258 316 C 240 314 230 324 214 330 C 192 338 180 362 180 392 "
         "C 180 438 212 470 256 470 C 300 470 332 438 332 392 "
         "C 332 362 320 338 298 330 C 282 324 274 314 258 316 Z")
EAR_RIM = ("M 158 188 C 146 138 150 92 164 62 C 170 50 184 52 190 64 "
           "C 210 100 238 126 264 142 C 232 166 194 182 158 188 Z")
EAR = ("M 161 186 C 150 138 154 94 166 66 C 172 54 183 56 188 67 "
       "C 208 102 235 127 259 142 C 230 164 194 179 161 186 Z")
EAR_PINK = ("M 174 176 C 166 138 168 106 178 84 C 182 74 190 76 194 88 "
            "C 210 116 230 134 248 144 C 224 160 198 170 174 176 Z")
EAR_PINK2 = ("M 180 168 C 174 138 176 112 183 94 C 186 87 191 88 194 97 "
             "C 206 120 222 135 236 144 C 216 156 198 164 180 168 Z")
EAR_TUFTS = [
    "M 186 168 C 194 160 202 152 208 142 C 210 152 204 164 194 172 Z",
    "M 200 160 C 208 152 216 145 222 138 C 224 147 217 157 208 164 Z",
    "M 214 152 C 222 146 229 140 234 134 C 236 142 229 151 221 157 Z",
]
NOSE_RIM = ("M 235 296 C 239 289 273 289 277 296 C 281 304 269 316 258 320 "
            "C 257 321 255 321 254 320 C 243 316 231 304 235 296 Z")
NOSE = ("M 237 297 C 241 291 271 291 275 297 C 278 304 268 314 257 318 "
        "C 256 319 255 319 254 318 C 243 314 234 304 237 297 Z")
COLLAR = "M 182 336 C 202 380 310 380 330 336"
SPARK = ("M 0 -15 C 2 -5 5 -2 15 0 C 5 2 2 5 0 15 "
         "C -2 5 -5 2 -15 0 C -5 -2 -2 -5 0 -15 Z")

# fur clumps that peek out from behind the head
CHEEK_FLUFF = [
    "M 140 282 C 126 288 116 297 112 308 C 124 310 140 308 156 302 Z",
    "M 156 312 C 142 320 132 331 129 343 C 142 342 158 336 174 328 Z",
    "M 180 338 C 168 348 160 360 158 372 C 170 368 184 359 198 348 Z",
]
CROWN_FLUFF = [
    "M 246 120 C 241 105 245 89 254 81 C 254 95 258 108 264 118 Z",
    "M 268 118 C 271 107 278 97 287 91 C 282 101 279 110 279 119 Z",
]

# palette
FUR_RIM = "#CF8340"
FUR_LIGHT = [(0.00, "#FFE3BA", 1.0), (0.40, "#FBC98E", 1.0),
             (0.76, "#F0AC68", 1.0), (1.00, "#DC9250", 1.0)]
STRIPE = "#CE7F39"
CREAM = "#FFF8EA"


# --------------------------------------------------------------------------
# 1. background
# --------------------------------------------------------------------------
_res = 420
_X, _Y = np.meshgrid(np.linspace(0.0, 1.0, _res), np.linspace(0.0, 1.0, _res))
_t = 0.44 * _X + 0.56 * _Y
ax.imshow(ramp([(0.00, "#F5FBF8", 1.0),
                (0.45, "#E4F3EC", 1.0),
                (1.00, "#C7E5DB", 1.0)], _t),
          extent=(0, SIZE, 0, SIZE), origin="upper", zorder=0,
          aspect="auto", interpolation="bilinear")

soft_blob(256, 268, 240, 240, "#FFF7E4", 0.85, z=0.5, hardness=0.05)

for _cx, _cy, _r, _a in [(74, 118, 36, .34), (440, 148, 23, .30),
                         (56, 330, 17, .26), (470, 252, 13, .30),
                         (104, 72, 11, .28)]:
    dot(_cx, _cy, _r, "#FFFFFF", z=0.7, alpha=_a)

for _cx, _cy, _s, _a in [(90, 206, 1.00, .85), (412, 88, 1.15, .80),
                         (474, 340, 0.70, .75), (58, 412, 0.62, .70),
                         (148, 54, 0.55, .70)]:
    _p = path(SPARK)
    _v = _p.vertices.copy()
    _v[:, 0] = _v[:, 0] * _s + _cx
    _v[:, 1] = (_v[:, 1] - SIZE) * _s + (SIZE - _cy)
    shape(Path(_v, _p.codes), "#FFD98F", z=0.8, alpha=_a)


def paw_print(cx, cy, s, rot, alpha):
    """A small decorative paw print."""
    a = math.radians(rot)
    ca, sa = math.cos(a), math.sin(a)

    def put(dx, dy, rx, ry):
        x, y = P(cx + s * (dx * ca - dy * sa), cy + s * (dx * sa + dy * ca))
        ax.add_patch(Ellipse((x, y), 2 * rx * s, 2 * ry * s, angle=-rot,
                             facecolor="#FFFFFF", edgecolor="none",
                             alpha=alpha, zorder=0.8))

    put(0, 9, 16, 12.5)
    for tx, ty in [(-14, -8), (-4.6, -14.5), (5.8, -14.5), (15, -7)]:
        put(tx, ty, 6, 6)


paw_print(68, 464, 0.62, -18, 0.42)
paw_print(460, 420, 0.50, 16, 0.42)

# --------------------------------------------------------------------------
# 2. ground shadow
# --------------------------------------------------------------------------
soft_blob(272, 490, 172, 22, "#2E6B58", 0.20, z=1.0, hardness=0.55)
soft_blob(252, 482, 112, 16, "#2E6B58", 0.18, z=1.0, hardness=0.55)

# --------------------------------------------------------------------------
# 3. tail (behind the body)
# --------------------------------------------------------------------------
tail_clip = shape(path(TAIL), FUR_RIM, z=2.0)
grad(path(TAIL_IN), [(0.00, "#F9C78D", 1.0),
                     (0.60, "#EFAC69", 1.0),
                     (1.00, "#DC9250", 1.0)],
     z=2.1, kind="linear", ang=51.0)
strokes(["M 368 380 L 374 448", "M 406 452 L 456 404", "M 436 474 L 490 484"],
        STRIPE, 17, z=2.2, alpha=0.72, clip=tail_clip)
ell(406, 486, 24, 13, "#FFF4E2", z=2.3, alpha=0.5, clip=tail_clip)

# --------------------------------------------------------------------------
# 4. body
# --------------------------------------------------------------------------
shape(path(BODY_RIM), FUR_RIM, z=3.0)
body_clip = grad(path(BODY), [(0.00, "#FCD29F", 1.0),
                              (0.52, "#F3B87A", 1.0),
                              (1.00, "#D68C4B", 1.0)],
                 z=3.1, kind="radial", cx=0.40, cy=0.20, r=0.92)

strokes(["M 124 352 C 152 362 178 364 198 358",
         "M 126 396 C 154 408 180 410 200 402",
         "M 136 440 C 162 452 186 454 204 448"],
        STRIPE, 13, z=3.2, alpha=0.68, clip=body_clip, mirror_too=True)

grad(path(BODY), [(0.00, "#A96A2C", 0.00),
                  (0.62, "#A96A2C", 0.06),
                  (1.00, "#8E5320", 0.32)],
     z=3.3, kind="linear", ang=90.0, clip=body_clip)

strokes(["M 150 336 C 160 344 164 354 160 366",
         "M 142 412 C 152 420 156 430 152 442"],
        "#C8813C", 2.6, z=3.35, alpha=0.28, clip=body_clip, mirror_too=True)

# --------------------------------------------------------------------------
# 5. chest fluff
# --------------------------------------------------------------------------
chest_clip = grad(path(CHEST), [(0.00, "#FFFDF8", 1.0),
                                (0.60, "#FDF2DF", 1.0),
                                (1.00, "#F5E1C2", 1.0)],
                  z=4.0, kind="radial", cx=0.50, cy=0.26, r=0.85)
strokes(["M 214 348 C 220 366 220 386 214 404",
         "M 234 340 C 240 360 240 382 234 402",
         "M 256 424 C 244 434 232 440 220 442"],
        "#EBD3AC", 3.0, z=4.1, alpha=0.75, clip=chest_clip, mirror_too=True)
soft_blob(256, 338, 104, 34, "#9A6428", 0.17, z=4.2, hardness=0.5)

# --------------------------------------------------------------------------
# 6. collar and bell (tucked behind the chin)
# --------------------------------------------------------------------------
outline(path(COLLAR), "#2C7E8C", 22, z=5.0)
outline(path(COLLAR), "#4FB4BB", 18, z=5.1)
outline(path("M 196 352 C 214 378 298 378 316 352"), "#9BE3DE", 3.5,
        z=5.2, alpha=0.55)
shape(path("M 249 366 L 263 366 L 263 378 L 249 378 Z"), "#E8B93C", z=5.2)
dot(256, 390, 17, "#B98322", z=5.3)
grad(path(epath(256, 389, 15.5, 15.5)),
     [(0.00, "#FFF3B8", 1.0), (0.45, "#F8D46A", 1.0),
      (0.82, "#E0A82F", 1.0), (1.00, "#B57F1B", 1.0)],
     z=5.4, kind="radial", cx=0.34, cy=0.28, r=0.80)
outline(path("M 241 391 C 250 396 262 396 271 391"), "#B07C1C", 2.6,
        z=5.5, alpha=0.9)
outline(path("M 256 392 L 256 402"), "#8E6114", 4, z=5.5)
dot(256, 399, 3.6, "#8E6114", z=5.5)
ell(249, 382, 5, 3.4, "#FFFBE4", z=5.6, alpha=0.85, rot=-28)

# --------------------------------------------------------------------------
# 7. front paws
# --------------------------------------------------------------------------
soft_blob(256, 436, 96, 24, "#C08A4A", 0.16, z=6.0, hardness=0.5)
for _px in (202, 310):
    ell(_px, 454, 47, 27, "#DFC098", z=6.1)
    grad(path(epath(_px, 452, 45, 25.5)),
         [(0.0, "#FFFCF4", 1.0), (1.0, "#F2DFBF", 1.0)],
         z=6.2, kind="radial", cx=0.40, cy=0.30, r=0.85)
strokes(["M 187 437 C 185 447 185 458 188 468",
         "M 216 437 C 218 447 218 458 215 468",
         "M 295 437 C 293 447 293 458 296 468",
         "M 324 437 C 326 447 326 458 323 468"],
        "#E0C297", 3.4, z=6.3, alpha=0.95)
ell(190, 443, 18, 8, "#FFFFFF", z=6.4, alpha=0.45, rot=-8)
ell(298, 443, 18, 8, "#FFFFFF", z=6.4, alpha=0.45, rot=-8)

# --------------------------------------------------------------------------
# 8. ears (drawn before the head, so their bases stay hidden)
# --------------------------------------------------------------------------
for _mir in (False, True):
    shape(path(EAR_RIM, mirror=_mir), FUR_RIM, z=7.0)
    grad(path(EAR, mirror=_mir), FUR_LIGHT,
         z=7.1, kind="radial", cx=0.40, cy=0.30, r=0.95)
    grad(path(EAR_PINK, mirror=_mir), [(0.00, "#FBBEC0", 1.0),
                                       (0.55, "#F19DA6", 1.0),
                                       (1.00, "#DC7C8C", 1.0)],
         z=7.2, kind="radial", cx=0.45, cy=0.72, r=0.80)
    shape(path(EAR_PINK2, mirror=_mir), "#F7C7C6", z=7.3, alpha=0.45)
    for _d in EAR_TUFTS:
        shape(path(_d, mirror=_mir), "#FFF3E2", z=7.4, alpha=0.85)

# --------------------------------------------------------------------------
# 9. head
# --------------------------------------------------------------------------
for _d in CHEEK_FLUFF:
    shape(path(_d), "#DE9450", z=8.0)
    shape(path(_d, mirror=True), "#DE9450", z=8.0)
for _d in CROWN_FLUFF:
    shape(path(_d), "#DE9450", z=8.0)

shape(path(HEAD_RIM), FUR_RIM, z=8.1)
head_clip = grad(path(HEAD), FUR_LIGHT,
                 z=8.2, kind="radial", cx=0.35, cy=0.26, r=0.88)

# a slightly deeper tone across the crown
shape(path("M 108 204 C 142 188 168 200 196 192 C 220 185 238 198 256 194 "
           "C 276 189 294 200 316 192 C 342 183 372 194 404 206 "
           "L 404 92 L 108 92 Z"), "#E39A52", z=8.3, alpha=0.40,
      clip=head_clip)
ell(194, 170, 78, 46, "#FFFFFF", z=8.35, alpha=0.20, rot=-22, clip=head_clip)

# pale muzzle field, fading out into the fur
grad(path(epath(256, 322, 106, 68)),
     [(0.00, "#FFF9EC", 1.00), (0.62, "#FFF5E2", 0.92),
      (1.00, "#FFF2DA", 0.00)],
     z=8.4, kind="radial", cx=0.5, cy=0.5, r=0.5, clip=head_clip)
soft_blob(256, 372, 118, 42, "#C07C36", 0.20, z=8.45, hardness=0.45)

# tabby markings: the classic forehead "M", then cheek bars
for _d, _w in [("M 256 126 C 253 144 253 162 256 178", 12),
               ("M 220 130 C 214 150 213 168 218 188", 10.5),
               ("M 292 130 C 298 150 299 168 294 188", 10.5),
               ("M 186 146 C 178 166 176 182 182 200", 9.5),
               ("M 326 146 C 334 166 336 182 330 200", 9.5),
               ("M 156 174 C 147 190 144 204 148 218", 8.5),
               ("M 356 174 C 365 190 368 204 364 218", 8.5)]:
    outline(path(_d), STRIPE, _w, z=8.5, alpha=0.62, clip=head_clip)
for _d, _w in [("M 152 258 C 136 264 122 273 112 286", 9),
               ("M 162 290 C 145 298 132 309 126 322", 8)]:
    outline(path(_d), STRIPE, _w, z=8.5, alpha=0.55, clip=head_clip)
    outline(path(_d, mirror=True), STRIPE, _w, z=8.5, alpha=0.55,
            clip=head_clip)

soft_blob(170, 298, 30, 18, "#F2887F", 0.30, z=8.6, hardness=0.40)
soft_blob(342, 298, 30, 18, "#F2887F", 0.30, z=8.6, hardness=0.40)

strokes(["M 136 236 C 145 244 147 254 143 266",
         "M 144 206 C 153 212 156 222 152 234",
         "M 202 126 C 210 132 212 140 208 150",
         "M 172 318 C 182 324 186 332 184 342"],
        "#C8813C", 2.6, z=8.7, alpha=0.30, clip=head_clip, mirror_too=True)

# --------------------------------------------------------------------------
# 10. face
# --------------------------------------------------------------------------
IRIS = [(0.00, "#F6E39A", 1.0), (0.24, "#C3DE7C", 1.0), (0.52, "#6FC272", 1.0),
        (0.80, "#2F9A62", 1.0), (1.00, "#166046", 1.0)]
LID_SHADE = [(0.00, "#10251B", 0.50), (0.38, "#10251B", 0.06),
             (0.72, "#FFFFFF", 0.05), (1.00, "#EAFFC9", 0.22)]


def eye(cx, cy):
    """One big kitten eye: rim, iris, slit pupil and three highlights."""
    soft_blob(cx, cy, 50, 54, "#D89252", 0.28, z=9.0, hardness=0.45)
    ell(cx, cy, 44, 48, "#3B2718", z=9.1)                      # dark rim
    iris = path(epath(cx, cy, 39.5, 43.5))
    holder = grad(iris, IRIS, z=9.2, kind="radial", cx=0.5, cy=0.42, r=0.72)
    grad(iris, LID_SHADE, z=9.3, kind="linear", ang=90.0, clip=holder)
    grad(path(epath(cx, cy - 2, 15.5, 31)),                    # pupil
         [(0.0, "#2A2016", 1.0), (0.6, "#140F0A", 1.0), (1.0, "#0A0705", 1.0)],
         z=9.4, kind="radial", cx=0.45, cy=0.35, r=0.80)
    ell(cx - 13, cy - 21, 13.5, 12.5, "#FFFFFF", z=9.5, alpha=0.95)
    dot(cx + 12, cy + 25, 7, "#FFFFFF", z=9.5, alpha=0.60)
    dot(cx + 6, cy - 34, 4.2, "#FFFFFF", z=9.5, alpha=0.85)
    lid = "M {} {} C {} {} {} {} {} {}".format(
        cx - 32, cy - 29, cx - 20, cy - 46, cx + 20, cy - 46, cx + 32, cy - 29)
    outline(path(lid), "#2E1D11", 4.5, z=9.6, alpha=0.5)


eye(200, 248)
eye(312, 248)

# whisker pads and chin
ell(224, 326, 39, 27, CREAM, z=9.7, alpha=0.95)
ell(288, 326, 39, 27, CREAM, z=9.7, alpha=0.95)
ell(256, 344, 26, 14, "#FFF9EE", z=9.7, alpha=0.90)

# nose
shape(path(NOSE_RIM), "#C97A85", z=9.8)
grad(path(NOSE), [(0.00, "#FBB5B8", 1.0), (0.55, "#F2939C", 1.0),
                  (1.00, "#DC717F", 1.0)],
     z=9.85, kind="linear", ang=63.0)
ell(248, 299, 6.5, 3.6, "#FFFFFF", z=9.9, alpha=0.55, rot=-18)
ell(245, 306, 3.4, 2.2, "#B85F6C", z=9.9, alpha=0.55, rot=20)
ell(267, 306, 3.4, 2.2, "#B85F6C", z=9.9, alpha=0.55, rot=-20)

# mouth
shape(path("M 244 340 C 250 346 262 346 268 340 Z"), "#E48896", z=9.9,
      alpha=0.5)
strokes(["M 256 319 L 256 328",
         "M 256 328 C 251 341 234 344 226 334",
         "M 256 328 C 261 341 278 344 286 334"],
        "#9A6544", 4.6, z=9.95, alpha=0.9)

# whisker roots
for _x, _y in [(204, 313), (196, 325), (203, 337),
               (221, 309), (214, 321), (220, 334)]:
    dot(_x, _y, 2.3, "#CE9257", z=9.96, alpha=0.5)
    dot(SIZE - _x, _y, 2.3, "#CE9257", z=9.96, alpha=0.5)

# --------------------------------------------------------------------------
# 11. whiskers -- a soft dark under-stroke keeps them readable on the fur
# --------------------------------------------------------------------------
WHISKERS = ["M 196 312 C 156 300 116 292 78 292",
            "M 192 324 C 150 322 110 326 74 334",
            "M 194 338 C 158 346 124 358 96 376"]
BROWS = ["M 190 208 C 174 197 158 191 142 189"]
for _d in WHISKERS:
    for _mir in (False, True):
        outline(path(_d, mirror=_mir), "#8A6236", 5.0, z=10.0, alpha=0.20)
        outline(path(_d, mirror=_mir), "#FFFDF6", 3.1, z=10.1, alpha=0.95)
for _d in BROWS:
    for _mir in (False, True):
        outline(path(_d, mirror=_mir), "#8A6236", 5.0, z=10.0, alpha=0.20)
        outline(path(_d, mirror=_mir), "#FFFDF6", 2.6, z=10.1, alpha=0.78)

# --------------------------------------------------------------------------
# save
# --------------------------------------------------------------------------
ax.set_xlim(0, SIZE)
ax.set_ylim(0, SIZE)
ax.set_aspect("equal")
fig.savefig("kitten.png", dpi=150, facecolor="#F5FBF8")
print("saved kitten.png")
