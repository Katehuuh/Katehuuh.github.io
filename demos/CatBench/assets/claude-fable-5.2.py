"""Draw a cute kitten with matplotlib."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Ellipse, PathPatch, Polygon
from matplotlib.path import Path

# ── Colour palette (tweak these to change the kitten!) ──────────────
BG       = "#E4F3F7"   # background
SHADOW   = "#C9E2EA"   # ground shadow
FUR      = "#F7B267"   # main fur
FUR_DARK = "#E58A3C"   # tabby stripes
CREAM    = "#FFF4E3"   # belly, muzzle, front paws
PINK     = "#FF9EAA"   # ears, nose, cheeks, hearts
BOW      = "#5AA9E6"   # bow tie
EYE      = "#2D1B14"
OUTLINE  = "#4A2F25"
LW       = 2.5         # outline width


# ── Small helpers ───────────────────────────────────────────────────
def bezier(p0, p1, p2, p3, n=100):
    """Return n points along a cubic Bézier curve."""
    p0, p1, p2, p3 = (np.asarray(p, dtype=float) for p in (p0, p1, p2, p3))
    t = np.linspace(0, 1, n)[:, None]
    return ((1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1
            + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3)


def rounded_triangle(base1, tip, base2, r=0.3):
    """Triangle path whose tip is softened with a quadratic curve."""
    base1, tip, base2 = (np.asarray(p, dtype=float) for p in (base1, tip, base2))
    a = tip + r * (base1 - tip)
    b = tip + r * (base2 - tip)
    verts = [base1, a, tip, b, base2, base1]
    codes = [Path.MOVETO, Path.LINETO, Path.CURVE3, Path.CURVE3,
             Path.LINETO, Path.CLOSEPOLY]
    return Path(verts, codes)


def heart(cx, cy, size, **kwargs):
    """A little heart-shaped polygon."""
    t = np.linspace(0, 2 * np.pi, 200)
    x = 16 * np.sin(t) ** 3
    y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
    return Polygon(np.column_stack([cx + size * x / 16, cy + size * y / 16]), **kwargs)


# ── Kitten parts ────────────────────────────────────────────────────
def draw_tail(ax):
    spine = bezier((1.0, -3.0), (2.9, -3.6), (3.95, -2.3), (3.05, -1.45))
    d = np.gradient(spine, axis=0)
    normal = np.column_stack([-d[:, 1], d[:, 0]])
    normal /= np.linalg.norm(normal, axis=1, keepdims=True)
    half_w = 0.33
    left, right = spine + half_w * normal, spine - half_w * normal

    # round cap at the tip of the tail
    a0 = np.arctan2(normal[-1, 1], normal[-1, 0])
    ang = np.linspace(a0, a0 - np.pi, 30)
    cap = spine[-1] + half_w * np.column_stack([np.cos(ang), np.sin(ang)])
    shape = np.vstack([left, cap, right[::-1]])

    ax.add_patch(Polygon(shape, fc=FUR, ec="none", zorder=1))
    for i in (28, 44, 60, 76):  # tabby stripes
        stripe = np.vstack([left[i:i + 9], right[i:i + 9][::-1]])
        ax.add_patch(Polygon(stripe, fc=FUR_DARK, ec="none", zorder=1.1))
    ax.add_patch(Polygon(shape, fc="none", ec=OUTLINE, lw=LW,
                         joinstyle="round", zorder=1.2))


def draw_body(ax):
    # hind feet peeking out from behind the body
    for s in (-1, 1):
        ax.add_patch(Ellipse((s * 1.35, -4.0), 1.1, 0.6,
                             fc=FUR, ec=OUTLINE, lw=LW, zorder=1.5))

    # body and belly
    ax.add_patch(Ellipse((0, -2.5), 3.3, 3.5, fc=FUR, ec=OUTLINE, lw=LW, zorder=2))
    ax.add_patch(Ellipse((0, -2.75), 1.9, 2.3, fc=CREAM, ec="none", zorder=2.1))

    # front paws with tiny toe lines
    for s in (-1, 1):
        cx = s * 0.55
        ax.add_patch(Ellipse((cx, -4.05), 0.95, 0.6,
                             fc=CREAM, ec=OUTLINE, lw=LW, zorder=3))
        for dx in (-0.15, 0.15):
            ax.plot([cx + dx, cx + dx], [-4.31, -4.16], color=OUTLINE,
                    lw=1.6, solid_capstyle="round", zorder=3.1)


def draw_head(ax):
    # ears (drawn first so the head overlaps their bases)
    for s in (-1, 1):
        outer = np.array([(2.4, 1.5), (2.3, 3.9), (0.7, 2.7)]) * (s, 1)
        inner = np.array([(2.1, 1.85), (2.05, 3.35), (1.05, 2.6)]) * (s, 1)
        ax.add_patch(PathPatch(rounded_triangle(*outer), fc=FUR, ec=OUTLINE,
                               lw=LW, joinstyle="round", zorder=4))
        ax.add_patch(PathPatch(rounded_triangle(*inner), fc=PINK, ec="none",
                               zorder=4.1))

    # head
    head = Ellipse((0, 0.8), 5.2, 4.2, fc=FUR, ec="none", zorder=5)
    ax.add_patch(head)

    # forehead stripes, clipped to the head shape
    for x, length in ((-0.48, 0.55), (0.0, 0.8), (0.48, 0.55)):
        stripe = Polygon([(x - 0.13, 3.0), (x + 0.13, 3.0), (x, 2.9 - length)],
                         fc=FUR_DARK, ec="none", zorder=5.1)
        ax.add_patch(stripe)
        stripe.set_clip_path(head)

    # head outline on top of the stripes
    ax.add_patch(Ellipse((0, 0.8), 5.2, 4.2, fc="none", ec=OUTLINE,
                         lw=LW, zorder=5.2))


def draw_face(ax):
    # muzzle and rosy cheeks
    ax.add_patch(Ellipse((0, -0.05), 1.7, 1.1, fc=CREAM, ec="none", zorder=6))
    for s in (-1, 1):
        ax.add_patch(Ellipse((s * 1.6, -0.05), 0.7, 0.38, fc=PINK, ec="none",
                             alpha=0.6, zorder=6))

    # big sparkly eyes
    for s in (-1, 1):
        ex, ey = s * 1.1, 0.65
        ax.add_patch(Ellipse((ex, ey), 0.85, 1.05, fc=EYE, ec="none", zorder=7))
        ax.add_patch(Circle((ex - 0.12, ey + 0.20), 0.17, fc="white", ec="none", zorder=7.1))
        ax.add_patch(Circle((ex + 0.14, ey - 0.20), 0.08, fc="white", ec="none", zorder=7.1))

    # mouth: a short line and two little arcs forming a "w"
    ax.plot([0, 0], [0.16, 0.0], color=OUTLINE, lw=1.8,
            solid_capstyle="round", zorder=6.9)
    ax.add_patch(Arc((-0.2, 0.0), 0.4, 0.4, theta1=190, theta2=360,
                     ec=OUTLINE, lw=1.8, capstyle="round", zorder=6.9))
    ax.add_patch(Arc((0.2, 0.0), 0.4, 0.4, theta1=180, theta2=350,
                     ec=OUTLINE, lw=1.8, capstyle="round", zorder=6.9))

    # nose
    ax.add_patch(Polygon([(-0.17, 0.36), (0.17, 0.36), (0, 0.16)], fc=PINK,
                         ec=OUTLINE, lw=1.8, joinstyle="round", zorder=7))

    # whiskers
    for s in (-1, 1):
        for y0, x1, y1 in ((0.15, 3.25, 0.5), (-0.05, 3.4, -0.05), (-0.25, 3.25, -0.6)):
            ax.plot([s * 1.95, s * x1], [y0, y1], color=OUTLINE, lw=1.4,
                    solid_capstyle="round", zorder=8)


def draw_bow(ax):
    for s in (-1, 1):
        ax.add_patch(Polygon([(0, -1.4), (s * 0.62, -1.06), (s * 0.62, -1.74)],
                             fc=BOW, ec=OUTLINE, lw=LW, joinstyle="round", zorder=8))
    ax.add_patch(Circle((0, -1.4), 0.16, fc=BOW, ec=OUTLINE, lw=LW, zorder=8.1))


# ── Put it all together ─────────────────────────────────────────────
def main():
    fig = plt.figure(figsize=(7, 7), facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-4.8, 5.2)
    ax.set_ylim(-5.3, 4.7)
    ax.set_aspect("equal")
    ax.axis("off")

    # ground shadow and a few floating hearts
    ax.add_patch(Ellipse((0.15, -4.3), 4.8, 0.55, fc=SHADOW, ec="none", zorder=0))
    for cx, cy, size, alpha in ((3.5, 3.1, 0.38, 0.9),
                                (4.25, 2.2, 0.24, 0.7),
                                (-3.7, 2.7, 0.28, 0.8)):
        ax.add_patch(heart(cx, cy, size, fc=PINK, ec="none", alpha=alpha, zorder=0.5))

    draw_tail(ax)
    draw_body(ax)
    draw_head(ax)
    draw_face(ax)
    draw_bow(ax)

    # Uncomment to save the picture to a file:
    # fig.savefig("kitten.png", dpi=200, facecolor=fig.get_facecolor())
    plt.show()


if __name__ == "__main__":
    main()
