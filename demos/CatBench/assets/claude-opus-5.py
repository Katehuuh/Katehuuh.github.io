# -*- coding: utf-8 -*-
"""
A cute kitten, drawn from nothing but matplotlib primitives.

Everything is authored as Python numbers: Bezier control points evaluated with
numpy, parametric arcs, offset ribbons, and radial/linear gradients painted as
clipped images.  Run it and it writes ``kitten.png``.
"""

import matplotlib

matplotlib.use("Agg")

from math import comb

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import Circle, Ellipse, Polygon, Wedge, PathPatch
from matplotlib.collections import LineCollection


# --------------------------------------------------------------------------
# palette
# --------------------------------------------------------------------------
BG_TOP = "#e6eef9"
BG_BOT = "#fdf1e1"
GROUND = "#f0e1c9"
MAT = "#f4ddc0"
MAT_RIM = "#e4c69f"

FUR_HI = "#fde3c0"       # lit top of the fur
FUR = "#f8c489"          # body colour
FUR_LO = "#e8a260"       # shaded underside
STRIPE = "#e0954b"       # tabby markings

CREAM = "#fff6ea"        # muzzle, chest, paws
CREAM_HI = "#fffdf8"
INK = "#6d4b34"          # warm brown outline

PINK = "#f4a3a8"
PINK_DK = "#e07f89"
NOSE = "#ef8f97"

EYE_HI = "#b8f1d1"       # top of iris gradient
EYE_LO = "#2c8a63"       # bottom of iris gradient
EYE_DK = "#31221a"       # eye socket / lash colour

GOLD = "#f9d268"
GOLD_DK = "#c8931f"
COLLAR = "#4fb3a6"
COLLAR_D = "#37897f"

SPARK = "#f7d68a"
HEART = "#f6b3c1"


# --------------------------------------------------------------------------
# small geometry helpers
# --------------------------------------------------------------------------
def bez(ctrl, n=80):
    """Sample a Bezier curve of any degree from its control points."""
    P = np.asarray(ctrl, dtype=float)
    deg = len(P) - 1
    t = np.linspace(0.0, 1.0, n).reshape(-1, 1)
    out = np.zeros((n, 2))
    for i, p in enumerate(P):
        out += comb(deg, i) * (t ** i) * ((1.0 - t) ** (deg - i)) * p
    return out


def mirror(pts):
    """Left-hand copy of a right-hand outline (negate x, reverse order)."""
    q = np.asarray(pts, dtype=float).copy()
    q[:, 0] *= -1.0
    return q[::-1]


def lens(p0, p1, half_w, bow=0.0, n=60, power=0.72):
    """A tapered sliver between two points -- used for every fur stripe."""
    p0 = np.asarray(p0, float)
    p1 = np.asarray(p1, float)
    d = p1 - p0
    length = float(np.hypot(*d))
    tan = d / length
    nrm = np.array([-tan[1], tan[0]])
    s = np.linspace(0.0, 1.0, n)
    mid = p0 + s[:, None] * d + (bow * np.sin(np.pi * s))[:, None] * nrm
    w = half_w * np.sin(np.pi * s) ** power
    return np.vstack([mid + w[:, None] * nrm, (mid - w[:, None] * nrm)[::-1]])


def ribbon(centre, half_w, round_tip=True, cap_n=26):
    """Offset a centreline by a varying half-width into a closed outline."""
    c = np.asarray(centre, float)
    d = np.gradient(c, axis=0)
    L = np.hypot(d[:, 0], d[:, 1])
    L[L == 0.0] = 1e-9
    tan = d / L[:, None]
    nrm = np.stack([-tan[:, 1], tan[:, 0]], axis=1)
    left = c + half_w[:, None] * nrm
    right = c - half_w[:, None] * nrm
    if round_tip:
        r = half_w[-1]
        a0 = np.arctan2(nrm[-1, 1], nrm[-1, 0])
        a = a0 - np.linspace(0.0, np.pi, cap_n)
        cap = c[-1] + r * np.stack([np.cos(a), np.sin(a)], axis=1)
        outline = np.vstack([left, cap, right[::-1]])
    else:
        outline = np.vstack([left, right[::-1]])
    return outline, left, right


def blob(ax, pts, zorder, fc=None, ec=None, lw=0.0, alpha=1.0, clip=None,
         joinstyle="round"):
    """Add a closed polygon and hand it back."""
    p = Polygon(np.asarray(pts, float), closed=True,
                facecolor="none" if fc is None else fc,
                edgecolor="none" if ec is None else ec,
                linewidth=lw, alpha=alpha, zorder=zorder,
                joinstyle=joinstyle, capstyle="round")
    ax.add_patch(p)
    if clip is not None:
        p.set_clip_path(clip)
    return p


def stroke(ax, pts, color, lw, zorder, alpha=1.0, clip=None):
    """A round-capped open stroke."""
    pts = np.asarray(pts, float)
    pp = PathPatch(Path(pts), facecolor="none", edgecolor=color, lw=lw,
                   alpha=alpha, zorder=zorder, capstyle="round",
                   joinstyle="round")
    ax.add_patch(pp)
    if clip is not None:
        pp.set_clip_path(clip)
    return pp


def lin_grad(ax, extent, c_bot, c_top, zorder, clip=None, n=256):
    """Vertical linear gradient painted as an image, optionally clipped."""
    t = np.linspace(0.0, 1.0, n).reshape(-1, 1, 1)
    a = np.array(matplotlib.colors.to_rgba(c_bot))
    b = np.array(matplotlib.colors.to_rgba(c_top))
    img = a * (1.0 - t) + b * t
    img = np.repeat(img, 2, axis=1)
    im = ax.imshow(img, extent=extent, origin="lower", zorder=zorder,
                   interpolation="bilinear")
    if clip is not None:
        im.set_clip_path(clip)
    return im


def rad_grad(ax, centre, radius, c_in, c_out, zorder, clip=None, n=200,
             gamma=1.0):
    """Radial gradient painted as an image, optionally clipped."""
    cx, cy = centre
    g = np.linspace(-1.0, 1.0, n)
    X, Y = np.meshgrid(g, g)
    r = np.clip(np.hypot(X, Y), 0.0, 1.0) ** gamma
    a = np.array(matplotlib.colors.to_rgba(c_in))
    b = np.array(matplotlib.colors.to_rgba(c_out))
    img = a * (1.0 - r[..., None]) + b * r[..., None]
    im = ax.imshow(img, extent=(cx - radius, cx + radius,
                                cy - radius, cy + radius),
                   origin="lower", zorder=zorder, interpolation="bilinear")
    if clip is not None:
        im.set_clip_path(clip)
    return im


# --------------------------------------------------------------------------
# canvas
# --------------------------------------------------------------------------
XMIN, XMAX = -4.30, 4.90
YMIN, YMAX = -3.90, 6.20

fig = plt.figure(figsize=(7.2, 7.9))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_axis_off()

# sky --------------------------------------------------------------------
lin_grad(ax, (XMIN, XMAX, YMIN, YMAX), BG_BOT, BG_TOP, zorder=0.0)

# a soft far-ground band
gx = np.linspace(XMIN, XMAX, 500)
gy = -2.05 + 0.30 * np.cos((gx - 0.4) * 0.42) + 0.10 * np.sin(gx * 0.9)
ax.fill_between(gx, YMIN, gy, color=GROUND, alpha=0.75, lw=0, zorder=0.2)
ax.fill_between(gx, YMIN, gy - 0.55, color=GROUND, alpha=0.55, lw=0, zorder=0.22)

# halo behind the kitten
rad_grad(ax, (0.15, 1.70), 4.70, (1, 1, 1, 0.66), (1, 1, 1, 0.0),
         zorder=0.35, gamma=0.85)


# --------------------------------------------------------------------------
# background decorations
# --------------------------------------------------------------------------
def heart(cx, cy, s, tilt=0.0):
    t = np.linspace(0.0, 2.0 * np.pi, 220)
    x = 16.0 * np.sin(t) ** 3
    y = (13.0 * np.cos(t) - 5.0 * np.cos(2 * t)
         - 2.0 * np.cos(3 * t) - np.cos(4 * t))
    x, y = x / 17.0 * s, y / 17.0 * s
    a = np.radians(tilt)
    return np.stack([cx + x * np.cos(a) - y * np.sin(a),
                     cy + x * np.sin(a) + y * np.cos(a)], axis=1)


def sparkle(cx, cy, R, pinch=0.20):
    tips = [(0.0, R), (R * 0.78, 0.0), (0.0, -R), (-R * 0.78, 0.0)]
    verts = [(cx + tips[0][0], cy + tips[0][1])]
    codes = [Path.MOVETO]
    for i in range(4):
        p, q = tips[i], tips[(i + 1) % 4]
        verts.append((cx + (p[0] + q[0]) * pinch, cy + (p[1] + q[1]) * pinch))
        codes.append(Path.CURVE3)
        verts.append((cx + q[0], cy + q[1]))
        codes.append(Path.CURVE3)
    return Path(verts, codes)


def paw_print(cx, cy, s, tilt, color, alpha, zorder):
    a = np.radians(tilt)
    rot = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])

    def place(dx, dy):
        v = rot @ np.array([dx * s, dy * s])
        return (cx + v[0], cy + v[1])

    ax.add_patch(Ellipse(place(0.0, -0.26), 1.04 * s, 0.86 * s, angle=tilt,
                         fc=color, ec="none", alpha=alpha, zorder=zorder))
    for dx, dy, w, h in ((-0.50, 0.38, 0.36, 0.44), (-0.17, 0.62, 0.34, 0.44),
                         (0.17, 0.62, 0.34, 0.44), (0.50, 0.38, 0.36, 0.44)):
        ax.add_patch(Ellipse(place(dx, dy), w * s, h * s, angle=tilt,
                             fc=color, ec="none", alpha=alpha, zorder=zorder))


for hx, hy, hs, ht, ha in ((-2.95, 4.05, 0.62, -14, 0.55),
                           (3.85, 4.75, 0.46, 12, 0.48),
                           (-3.45, 1.05, 0.40, -20, 0.42),
                           (4.15, -0.35, 0.34, 16, 0.36)):
    blob(ax, heart(hx, hy, hs, ht), zorder=0.6, fc=HEART, alpha=ha)

for sx, sy, sr, sa in ((-2.45, 5.30, 0.40, 0.85), (2.75, 5.70, 0.30, 0.75),
                       (-3.75, 2.60, 0.26, 0.70), (4.35, 2.35, 0.32, 0.70),
                       (-3.10, -1.55, 0.24, 0.60), (1.05, 5.85, 0.22, 0.60)):
    ax.add_patch(PathPatch(sparkle(sx, sy, sr), fc=SPARK, ec="none",
                           alpha=sa, zorder=0.62))

paw_print(-3.55, -0.30, 0.52, 18, FUR_LO, 0.22, 0.58)
paw_print(3.55, 3.35, 0.44, -22, FUR_LO, 0.20, 0.58)


# --------------------------------------------------------------------------
# the mat the kitten sits on, plus contact shadows
# --------------------------------------------------------------------------
ax.add_patch(Ellipse((0.20, -2.80), 7.10, 1.20, fc=MAT, ec=MAT_RIM, lw=2.2,
                     zorder=1.20))
ax.add_patch(Ellipse((0.20, -2.80), 6.10, 0.80, fc="none", ec=MAT_RIM, lw=1.4,
                     alpha=0.65, zorder=1.22))
ax.add_patch(Ellipse((0.10, -2.66), 5.10, 0.62, fc="#a97f52", alpha=0.15,
                     ec="none", zorder=1.30))
ax.add_patch(Ellipse((0.00, -2.60), 3.30, 0.34, fc="#8f6539", alpha=0.16,
                     ec="none", zorder=1.32))


# --------------------------------------------------------------------------
# tail -- an offset ribbon along a two-piece Bezier centreline
# --------------------------------------------------------------------------
tail_centre = np.vstack([
    bez([(1.10, -2.35), (3.05, -2.85), (4.20, -1.30), (3.78, 0.35)], 70),
    bez([(3.78, 0.35), (3.62, 1.55), (3.22, 2.38), (2.68, 2.86)], 55)[1:],
])
s_tail = np.linspace(0.0, 1.0, len(tail_centre))
tail_w = 0.22 + 0.25 * (1.0 - s_tail) ** 1.10 + 0.05 * np.sin(np.pi * s_tail)
tail_out, tail_L, tail_R = ribbon(tail_centre, tail_w)

tail_patch = blob(ax, tail_out, zorder=2.00, fc=FUR)
lin_grad(ax, (0.55, 4.75, -2.95, 3.20), FUR_LO, FUR_HI, zorder=2.02,
         clip=tail_patch)

N = len(tail_centre)


def tail_band(s0, s1, color, z=2.06, alpha=1.0):
    i0, i1 = int(s0 * (N - 1)), int(s1 * (N - 1))
    band = np.vstack([tail_L[i0:i1 + 1], tail_R[i0:i1 + 1][::-1]])
    blob(ax, band, zorder=z, fc=color, alpha=alpha, clip=tail_patch)


for a, b in ((0.20, 0.29), (0.42, 0.51), (0.63, 0.71), (0.81, 0.87)):
    tail_band(a, b, STRIPE)
tail_band(0.925, 1.0, CREAM)
blob(ax, tail_out, zorder=2.10, ec=INK, lw=2.6)


# --------------------------------------------------------------------------
# body -- a bell shaped sitting silhouette
# --------------------------------------------------------------------------
body_right = np.vstack([
    bez([(0.00, 1.55), (0.85, 1.55), (1.35, 1.35), (1.55, 0.95)], 40),
    bez([(1.55, 0.95), (1.80, 0.50), (2.15, -0.45), (2.15, -1.30)], 50)[1:],
    bez([(2.15, -1.30), (2.15, -1.95), (2.10, -2.45), (1.80, -2.45)], 40)[1:],
    bez([(1.80, -2.45), (1.25, -2.62), (0.62, -2.66), (0.00, -2.66)], 40)[1:],
])
body_pts = np.vstack([body_right, mirror(body_right)])

body = blob(ax, body_pts, zorder=3.00, fc=FUR)
lin_grad(ax, (-2.30, 2.30, -2.80, 1.70), FUR_LO, FUR_HI, zorder=3.02,
         clip=body)

# haunch suggestion
for sgn in (1, -1):
    stroke(ax, bez([(sgn * 1.00, -0.75), (sgn * 1.95, -1.10),
                    (sgn * 1.78, -2.30)], 50),
           FUR_LO, 2.4, zorder=3.06, alpha=0.75, clip=body)

# flank stripes
for sgn in (1, -1):
    for p0, p1 in (((1.05, 0.36), (2.45, 0.06)),
                   ((1.12, -0.50), (2.52, -0.80)),
                   ((1.26, -1.34), (2.50, -1.66))):
        blob(ax, lens((sgn * p0[0], p0[1]), (sgn * p1[0], p1[1]), 0.125,
                      bow=0.05 * sgn),
             zorder=3.08, fc=STRIPE, alpha=0.85, clip=body)

# cream chest
chest_right = np.vstack([
    bez([(0.00, 0.76), (0.56, 0.72), (0.93, 0.12), (1.02, -0.55)], 40),
    bez([(1.02, -0.55), (1.10, -1.22), (1.08, -1.78), (0.88, -2.06)], 40)[1:],
    bez([(0.88, -2.06), (0.64, -2.30), (0.32, -2.36), (0.00, -2.36)], 40)[1:],
])
chest = blob(ax, np.vstack([chest_right, mirror(chest_right)]),
             zorder=3.12, fc=CREAM, clip=body)
blob(ax, body_pts, zorder=3.20, ec=INK, lw=2.8)


# --------------------------------------------------------------------------
# collar + bell
# --------------------------------------------------------------------------
collar_c = bez([(-1.80, 1.40), (0.00, -0.58), (1.80, 1.40)], 120)
collar_w = np.full(len(collar_c), 0.135)
collar_out, _, _ = ribbon(collar_c, collar_w, round_tip=False)
cpatch = blob(ax, collar_out, zorder=3.40, fc=COLLAR, ec=COLLAR_D, lw=1.8,
              clip=body)

ax.add_patch(Circle((0.0, 0.52), 0.075, fc=GOLD_DK, ec="none", zorder=3.44))
ax.add_patch(Circle((0.0, 0.30), 0.225, fc=GOLD, ec=GOLD_DK, lw=1.8,
                    zorder=3.46))
rad_grad(ax, (-0.05, 0.36), 0.225, "#fff0b8", GOLD_DK,
         zorder=3.47, gamma=1.5,
         clip=ax.add_patch(Circle((0.0, 0.30), 0.215, fc="none", ec="none",
                                  zorder=3.47)))
stroke(ax, bez([(-0.15, 0.24), (0.0, 0.16), (0.15, 0.24)], 30), GOLD_DK, 1.7,
       zorder=3.50)
ax.add_patch(Circle((0.0, 0.235), 0.045, fc=GOLD_DK, ec="none", zorder=3.51))
ax.add_patch(Circle((-0.08, 0.38), 0.055, fc="#fffbe6", ec="none", alpha=0.9,
                    zorder=3.52))


# --------------------------------------------------------------------------
# front paws
# --------------------------------------------------------------------------
for px in (-0.78, 0.78):
    ax.add_patch(Ellipse((px, -2.30), 1.16, 0.74, fc=CREAM, ec=INK, lw=2.3,
                         zorder=3.60))
    for dx in (-0.21, 0.21):
        stroke(ax, bez([(px + dx, -2.06), (px + dx * 1.25, -2.30),
                        (px + dx * 1.15, -2.52)], 30),
               INK, 1.7, zorder=3.62, alpha=0.5)


# --------------------------------------------------------------------------
# head + ears as one merged silhouette
# --------------------------------------------------------------------------
HC = np.array([0.0, 2.45])
RX, RY = 1.95, 1.78


def head_pt(deg):
    a = np.radians(deg)
    return np.array([RX * np.cos(a), RY * np.sin(a)]) + HC


def head_arc(d0, d1, n=170, fluff=0.0, lobes=4):
    a = np.radians(np.linspace(d0, d1, n))
    pts = np.stack([RX * np.cos(a), RY * np.sin(a)], axis=1)
    if fluff:
        nx, ny = np.cos(a) / RX, np.sin(a) / RY
        m = np.hypot(nx, ny)
        s = np.linspace(0.0, 1.0, n)
        bump = fluff * np.sin(lobes * np.pi * s) ** 2 * np.sin(np.pi * s)
        pts = pts + np.stack([nx / m * bump, ny / m * bump], axis=1)
    return pts + HC


head_right = np.vstack([
    head_arc(-90.0, 28.0, 210, fluff=0.16, lobes=3),          # fluffy cheek
    bez([head_pt(28.0), (1.99, 3.95), (1.80, 4.75), (1.40, 5.12)], 55)[1:],
    bez([(1.40, 5.12), (1.55, 5.58), (1.16, 5.06)], 24)[1:],  # rounded tip
    bez([(1.16, 5.06), (1.06, 4.60), (0.98, 4.32), head_pt(70.0)], 55)[1:],
    head_arc(70.0, 90.0, 26)[1:],
])
head_pts = np.vstack([head_right, mirror(head_right)])

head = blob(ax, head_pts, zorder=4.00, fc=FUR)
lin_grad(ax, (-2.20, 2.20, 0.50, 5.70), FUR_LO, FUR_HI, zorder=4.02, clip=head)

# inner ears -------------------------------------------------------------
inner_right = np.vstack([
    bez([(1.48, 3.62), (1.72, 4.10), (1.58, 4.62), (1.30, 4.86)], 45),
    bez([(1.30, 4.86), (1.17, 4.58), (1.12, 4.34), (0.92, 4.12)], 40)[1:],
    bez([(0.92, 4.12), (1.06, 3.86), (1.24, 3.68), (1.48, 3.62)], 40)[1:],
])
for sgn in (1, -1):
    pts = inner_right if sgn > 0 else mirror(inner_right)
    ip = blob(ax, pts, zorder=4.10, fc=PINK, clip=head)
    lin_grad(ax, (0.7 if sgn > 0 else -1.9, 1.9 if sgn > 0 else -0.7,
                  3.5, 5.0), PINK_DK, "#fdd3d6", zorder=4.11, clip=ip)
    for a, b, w in (((1.10, 3.84), (1.26, 4.44), 0.055),
                    ((1.33, 3.76), (1.52, 4.22), 0.048),
                    ((0.97, 3.94), (1.05, 4.30), 0.042)):
        blob(ax, lens((sgn * a[0], a[1]), (sgn * b[0], b[1]), w),
             zorder=4.14, fc=CREAM, alpha=0.85, clip=ip)

blob(ax, head_pts, zorder=4.20, ec=INK, lw=2.9)

# forehead + cheek stripes ------------------------------------------------
blob(ax, lens((0.0, 3.30), (0.0, 4.18), 0.135), zorder=4.24, fc=STRIPE,
     clip=head)
for sgn in (1, -1):
    for a, b, w in (((sgn * 0.55, 3.24), (sgn * 0.76, 4.06), 0.115),
                    ((sgn * 1.02, 3.10), (sgn * 1.34, 3.74), 0.100),
                    ((sgn * 1.12, 2.62), (sgn * 2.35, 2.88), 0.100),
                    ((sgn * 1.18, 2.12), (sgn * 2.38, 2.20), 0.094)):
        blob(ax, lens(a, b, w, bow=0.03 * sgn), zorder=4.24, fc=STRIPE,
             clip=head)

# blush -------------------------------------------------------------------
for sgn in (1, -1):
    ax.add_patch(Ellipse((sgn * 1.30, 1.78), 0.88, 0.50, fc=PINK, ec="none",
                         alpha=0.40, zorder=4.30))
    ax.add_patch(Ellipse((sgn * 1.30, 1.78), 0.62, 0.34, fc=PINK, ec="none",
                         alpha=0.32, zorder=4.31))


# --------------------------------------------------------------------------
# muzzle
# --------------------------------------------------------------------------
ax.add_patch(Ellipse((0.0, 1.45), 2.30, 1.26, fc=CREAM, ec="none",
                     zorder=4.40))
for sgn in (1, -1):
    ax.add_patch(Ellipse((sgn * 0.44, 1.34), 1.04, 0.68, fc=CREAM_HI,
                         ec="none", alpha=0.85, zorder=4.42))


# --------------------------------------------------------------------------
# eyes
# --------------------------------------------------------------------------
def eye(cx, cy):
    socket = ax.add_patch(Ellipse((cx, cy), 1.08, 1.24, fc=EYE_DK, ec=INK,
                                  lw=2.0, zorder=5.00))
    iris = ax.add_patch(Ellipse((cx, cy - 0.02), 0.92, 1.06, fc=EYE_LO,
                                ec="none", zorder=5.04))
    lin_grad(ax, (cx - 0.55, cx + 0.55, cy - 0.60, cy + 0.55),
             EYE_HI, EYE_LO, zorder=5.06, clip=iris)
    ax.add_patch(Ellipse((cx, cy - 0.02), 0.44, 0.70, fc="#20160f", ec="none",
                         zorder=5.10))
    ax.add_patch(Circle((cx - 0.21, cy + 0.28), 0.205, fc="white", ec="none",
                        zorder=5.14))
    ax.add_patch(Circle((cx + 0.19, cy - 0.26), 0.105, fc="white", ec="none",
                        alpha=0.9, zorder=5.14))
    ax.add_patch(Circle((cx + 0.27, cy + 0.31), 0.062, fc="white", ec="none",
                        alpha=0.85, zorder=5.14))
    # eyelid shading along the top
    blob(ax, lens((cx - 0.50, cy + 0.30), (cx + 0.50, cy + 0.30), 0.085,
                  bow=0.30), zorder=5.18, fc=EYE_DK, alpha=0.55,
         clip=socket)
    return socket


eye(-0.82, 2.50)
eye(0.82, 2.50)


# --------------------------------------------------------------------------
# nose, mouth, tongue
# --------------------------------------------------------------------------
nose_pts = np.vstack([
    bez([(-0.21, 1.92), (-0.06, 1.99), (0.06, 1.99), (0.21, 1.92)], 30),
    bez([(0.21, 1.92), (0.18, 1.78), (0.08, 1.68), (0.00, 1.63)], 30)[1:],
    bez([(0.00, 1.63), (-0.08, 1.68), (-0.18, 1.78), (-0.21, 1.92)], 30)[1:],
])
nose = blob(ax, nose_pts, zorder=5.40, fc=NOSE, ec=PINK_DK, lw=1.6)
rad_grad(ax, (-0.05, 1.90), 0.24, "#ffc8cc", NOSE, zorder=5.42, gamma=1.4,
         clip=nose)

# tongue peeking out
ax.add_patch(Wedge((0.0, 1.48), 0.190, 180, 360, fc=PINK, ec=PINK_DK, lw=1.2,
                   zorder=5.44))
stroke(ax, [(0.0, 1.44), (0.0, 1.32)], PINK_DK, 1.1, zorder=5.46, alpha=0.8)

stroke(ax, [(0.0, 1.63), (0.0, 1.50)], INK, 2.1, zorder=5.50)
stroke(ax, bez([(0.0, 1.50), (-0.06, 1.31), (-0.30, 1.30), (-0.40, 1.52)], 40),
       INK, 2.1, zorder=5.50)
stroke(ax, bez([(0.0, 1.50), (0.06, 1.31), (0.30, 1.30), (0.40, 1.52)], 40),
       INK, 2.1, zorder=5.50)

# whisker dots
for sgn in (1, -1):
    for dx, dy in ((0.32, 1.54), (0.58, 1.58), (0.84, 1.50),
                   (0.40, 1.26), (0.68, 1.28)):
        ax.add_patch(Circle((sgn * dx, dy), 0.036, fc=INK, ec="none",
                            alpha=0.42, zorder=5.60))


# --------------------------------------------------------------------------
# whiskers -- tapered with a LineCollection
# --------------------------------------------------------------------------
def whisker(ctrl, w0=2.6, w1=0.45, n=44, color=INK, alpha=0.72):
    p = bez(ctrl, n)
    segs = np.stack([p[:-1], p[1:]], axis=1)
    ax.add_collection(LineCollection(segs, linewidths=np.linspace(w0, w1, n - 1),
                                     colors=color, alpha=alpha,
                                     capstyle="round", zorder=6.0))


for sgn in (1, -1):
    whisker([(sgn * 1.02, 1.60), (sgn * 1.80, 1.92), (sgn * 2.48, 2.06)])
    whisker([(sgn * 1.06, 1.40), (sgn * 1.90, 1.44), (sgn * 2.62, 1.36)])
    whisker([(sgn * 1.00, 1.20), (sgn * 1.78, 1.02), (sgn * 2.42, 0.82)])


# --------------------------------------------------------------------------
# finish
# --------------------------------------------------------------------------
ax.set_xlim(XMIN, XMAX)
ax.set_ylim(YMIN, YMAX)
ax.set_aspect("equal")

fig.savefig("kitten.png", dpi=150, facecolor=BG_BOT)
print("saved kitten.png")
