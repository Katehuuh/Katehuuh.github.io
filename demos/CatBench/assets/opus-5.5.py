"""
cute_kitten.py - draws a cute ginger kitten with matplotlib.

Everything is built from simple shapes (ellipses, circles, rounded polygons
and Bezier curves) layered back-to-front with zorder.
Requires: numpy, matplotlib
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Ellipse, PathPatch, Polygon
from matplotlib.path import Path
from matplotlib.transforms import Affine2D

# ---- Palette (swap FUR/STRIPE for greys to get a grey tabby) ----------------
BG        = "#E6F3FA"   # soft sky-blue background
FUR       = "#F9B36B"   # ginger fur
STRIPE    = "#EB8F3F"   # tabby stripes
CREAM     = "#FFF3E0"   # muzzle, chest and paws
INK       = "#5B3A29"   # soft brown outlines (gentler than black)
EAR_PINK  = "#F8B5C4"
NOSE_PINK = "#F28B9F"
BLUSH     = "#FF8FA8"
EYE       = "#2D2433"
EYE_GLOW  = "#6B5CA5"
COLLAR    = "#E75A7C"
GOLD      = "#FFD45C"
YARN      = "#B39DDB"
YARN_DARK = "#8E6FCB"
HEART     = "#FF8FAB"
LW = 2.6                # outline width in points


# ---- Geometry helpers -------------------------------------------------------
def ellipse(cx, cy, w, h):
    """Ellipse as a Path, so one shape can be filled, outlined and clipped to."""
    return Affine2D().scale(w / 2, h / 2).translate(cx, cy).transform_path(Path.unit_circle())


def rounded_polygon(points, soft=0.2):
    """Closed path through `points` with rounded corners
    (`soft` = fraction of each edge used by the rounding)."""
    pts = np.asarray(points, float)
    verts, codes = [], []
    for i, corner in enumerate(pts):
        prev, nxt = pts[i - 1], pts[(i + 1) % len(pts)]
        verts += [corner + (prev - corner) * soft, corner, corner + (nxt - corner) * soft]
        codes += [Path.LINETO, Path.CURVE3, Path.CURVE3]
    codes[0] = Path.MOVETO
    return Path(verts + [verts[0]], codes + [Path.CLOSEPOLY])


def both_sides(path):
    """A path plus its mirror image across x = 0 (ears, paws, haunches)."""
    return Path.make_compound_path(path, Affine2D().scale(-1, 1).transform_path(path))


def bezier(p0, p1, p2, p3, n=200):
    """n points along a cubic Bezier curve."""
    p0, p1, p2, p3 = map(np.asarray, (p0, p1, p2, p3))
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t)**3 * p0 + 3 * (1 - t)**2 * t * p1 + 3 * (1 - t) * t**2 * p2 + t**3 * p3


def stripe(base, tip, width):
    """Tapered tabby stripe: a thin triangle from a wide base to a pointed tip."""
    base, tip = np.asarray(base, float), np.asarray(tip, float)
    d = tip - base
    side = np.array([-d[1], d[0]]) / np.hypot(*d) * width / 2
    return [base + side, tip, base - side]


def mirrored(stripes):
    """The given stripes plus their mirror images across x = 0."""
    return list(stripes) + [[(-x, y) for x, y in s] for s in stripes]


# ---- Drawing helpers --------------------------------------------------------
def fur_shape(ax, path, z, stripes=()):
    """Fill a shape with fur, add stripes clipped inside it, then outline it.
    Returns the fill patch so other details can be clipped to the shape too."""
    fill = ax.add_patch(PathPatch(path, fc=FUR, ec="none", zorder=z))
    for s in stripes:
        ax.add_patch(Polygon(s, fc=STRIPE, ec="none", zorder=z + 0.1)).set_clip_path(fill)
    ax.add_patch(PathPatch(path, fc="none", ec=INK, lw=LW, zorder=z + 0.3))
    return fill


def stroke(ax, pts, z, lw=LW, color=INK):
    pts = np.asarray(pts, float)
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, solid_capstyle="round", zorder=z)


def heart(ax, cx, cy, size, tilt=0):
    t = np.linspace(0, 2 * np.pi, 120)
    x = 16 * np.sin(t)**3
    y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t) + 2.5
    a = np.radians(tilt)
    xr, yr = x * np.cos(a) - y * np.sin(a), x * np.sin(a) + y * np.cos(a)
    ax.fill(cx + xr * size / 16, cy + yr * size / 16, color=HEART, alpha=0.85, lw=0, zorder=9)


# ---- The kitten, drawn back to front ----------------------------------------
def draw_tail(ax):
    c = bezier((2.8, -5.8), (7.2, -7.6), (7.6, -2.0), (5.5, -1.0))   # centre line
    tangent = np.gradient(c, axis=0)
    tangent /= np.linalg.norm(tangent, axis=1, keepdims=True)
    inward = np.column_stack([-tangent[:, 1], tangent[:, 0]])      # toward inside of curl
    half_w = np.linspace(0.62, 0.48, len(c))[:, None]              # gently tapered
    a0 = np.arctan2(inward[-1, 1], inward[-1, 0])                  # round cap at the tip
    ang = np.linspace(a0, a0 - np.pi, 25)
    cap = c[-1] + half_w[-1] * np.column_stack([np.cos(ang), np.sin(ang)])
    outline = np.vstack([c + inward * half_w, cap, (c - inward * half_w)[::-1]])
    tail = Path(np.vstack([outline, outline[:1]]), closed=True)
    rings = [stripe(c[i] - inward[i] * 1.1, c[i] + inward[i] * 0.3, 0.75)
             for i in (72, 100, 128, 156)]
    fur_shape(ax, tail, z=2, stripes=rings)


def draw_body(ax):
    # haunches (back legs) bulging out at the bottom
    fur_shape(ax, both_sides(ellipse(2.8, -5.9, 3.4, 3.2)), z=3,
              stripes=mirrored([stripe((5.0, -5.35), (3.7, -5.7), 0.55),
                                stripe((4.9, -6.45), (3.8, -6.6), 0.5)]))
    body = fur_shape(ax, ellipse(0, -3.6, 8.0, 7.0), z=4,
                     stripes=mirrored([stripe((4.7, -1.75), (2.6, -2.05), 0.6),
                                       stripe((4.8, -3.0), (2.7, -3.25), 0.6),
                                       stripe((4.8, -4.25), (3.0, -4.35), 0.55)]))
    # cream chest and front legs, plus a collar peeking out under the chin
    ax.add_patch(Ellipse((0, -4.2), 4.4, 7.0, fc=CREAM, zorder=4.2)).set_clip_path(body)
    ax.add_patch(PathPatch(ellipse(0, 2.35, 9.2, 7.8), fc=COLLAR, ec=INK, lw=LW * 0.7,
                           zorder=4.25)).set_clip_path(body)
    stroke(ax, [(0, -6.95), (0, -5.25)], z=4.5)                    # gap between front legs
    # tiny golden bell
    ax.add_patch(Circle((0, -1.75), 0.42, fc=GOLD, ec=INK, lw=LW * 0.8, zorder=4.5))
    stroke(ax, [(-0.34, -1.68), (0.34, -1.68)], z=4.6, lw=LW * 0.6)
    stroke(ax, [(0, -1.93), (0, -2.1)], z=4.6, lw=LW * 0.6)
    ax.add_patch(Circle((0, -1.93), 0.07, fc=INK, zorder=4.6))
    ax.add_patch(Circle((-0.16, -1.54), 0.08, fc="white", zorder=4.6))


def draw_paws(ax):
    ax.add_patch(PathPatch(both_sides(ellipse(1.05, -7.05, 2.1, 1.3)),
                           fc=CREAM, ec=INK, lw=LW, zorder=5))
    for x in (-1.4, -0.7, 0.7, 1.4):                                # little toes
        stroke(ax, [(x, -6.45), (x, -6.8)], z=5.1, lw=LW * 0.8)


def draw_yarn(ax):
    # a loose strand that disappears under the kitten's paw
    stroke(ax, bezier((-5.3, -7.4), (-4.4, -8.3), (-3.0, -7.6), (-1.3, -7.5)),
           z=4.9, lw=2.5, color=YARN)
    center = np.array([-6.4, -6.9])
    ball = ax.add_patch(Circle(center, 1.2, fc=YARN, zorder=5))
    threads = [((-1.6, 1.4), (1.5, 1.95, 2.4, 2.85)),               # (centre offset, radii)
               ((1.9, 1.0), (1.6, 2.1, 2.6))]
    for offset, radii in threads:
        for r in radii:
            ax.add_patch(Circle(center + offset, r, fill=False, ec=YARN_DARK, lw=1.4,
                                zorder=5.1)).set_clip_path(ball)
    ax.add_patch(Circle(center, 1.2, fill=False, ec=INK, lw=LW * 0.85, zorder=5.2))


def draw_head(ax):
    # ears first, so the head overlaps their base
    ear = np.array([(-4.25, 3.3), (-3.95, 7.8), (-1.35, 5.4)])
    hub = np.array([-3.15, 5.25])
    inner = hub + 0.6 * (ear - hub)                                 # smaller copy for the pink
    fur_shape(ax, both_sides(rounded_polygon(ear, 0.15)), z=6)
    ax.add_patch(PathPatch(both_sides(rounded_polygon(inner, 0.25)),
                           fc=EAR_PINK, ec="none", zorder=6.2))
    # round head with tabby stripes on the forehead and cheeks
    fur_shape(ax, ellipse(0, 2.5, 9.0, 7.2), z=7,
              stripes=[stripe((0, 6.6), (0, 5.0), 0.7)]
              + mirrored([stripe((1.55, 6.35), (1.0, 5.25), 0.6),
                          stripe((4.9, 3.1), (3.75, 2.85), 0.5),
                          stripe((4.9, 2.2), (3.9, 2.05), 0.45)]))


def draw_face(ax):
    for s in (-1, 1):                                               # left side, right side
        ax.add_patch(Circle((0.5 * s, 0.55), 0.72, fc=CREAM, zorder=8))           # muzzle
        ax.add_patch(Ellipse((2.95 * s, 1.05), 1.2, 0.62, fc=BLUSH, alpha=0.5, zorder=8.1))
        ex, ey = 1.85 * s, 2.05                                     # big shiny eyes
        ax.add_patch(Ellipse((ex, ey), 1.6, 1.9, fc=EYE, zorder=8.5))
        ax.add_patch(Ellipse((ex, ey - 0.36), 1.15, 0.85, fc=EYE_GLOW, alpha=0.55, zorder=8.6))
        ax.add_patch(Circle((ex - 0.3, ey + 0.42), 0.33, fc="white", zorder=8.7))
        ax.add_patch(Circle((ex + 0.33, ey - 0.38), 0.14, fc="white", zorder=8.7))
        ax.add_patch(Arc((0.25 * s, 0.58), 0.5, 0.4, theta1=180, theta2=360, ec=INK,
                         lw=LW * 0.8, capstyle="round", zorder=8.3))  # half the w-mouth
    # whiskers: gently bowed curves, mirrored to both sides
    bow = np.array([0, 0.18])
    whiskers = [((1.15, 0.7), (4.7, 1.25)),
                ((1.2, 0.45), (4.9, 0.4)),
                ((1.1, 0.2), (4.5, -0.4))]
    for p0, p3 in whiskers:
        p0, p3 = np.array(p0), np.array(p3)
        w = bezier(p0, p0 + (p3 - p0) / 3 + bow, p0 + 2 * (p3 - p0) / 3 + bow, p3, n=50)
        for s in (-1, 1):
            stroke(ax, w * (s, 1), z=8.2, lw=LW * 0.65)
    # little pink nose
    stroke(ax, [(0, 0.9), (0, 0.58)], z=8.3, lw=LW * 0.8)
    ax.add_patch(PathPatch(rounded_polygon([(-0.42, 1.22), (0.42, 1.22), (0, 0.78)], 0.3),
                           fc=NOSE_PINK, ec="none", zorder=8.4))
    ax.add_patch(Ellipse((-0.1, 1.12), 0.22, 0.09, fc="white", alpha=0.8, zorder=8.45))


def main():
    fig = plt.figure(figsize=(7, 7.2), facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_aspect("equal")
    ax.axis("off")

    # soft shadows on the floor
    ax.add_patch(Ellipse((0.8, -7.65), 11.5, 1.3, fc="black", alpha=0.07, zorder=1))
    ax.add_patch(Ellipse((-6.4, -8.1), 2.8, 0.55, fc="black", alpha=0.07, zorder=1))

    draw_tail(ax)
    draw_body(ax)
    draw_paws(ax)
    draw_yarn(ax)
    draw_head(ax)
    draw_face(ax)
    hearts = [(-6.5, 5.4, 0.6, 15), (6.6, 6.4, 0.8, -12), (7.7, 4.4, 0.45, -25)]
    for x, y, size, tilt in hearts:
        heart(ax, x, y, size, tilt)

    ax.set_xlim(-8.5, 9)
    ax.set_ylim(-9.3, 8.7)
    fig.savefig("kitten.png", dpi=200, facecolor=BG)
    plt.show()


if __name__ == "__main__":
    main()
