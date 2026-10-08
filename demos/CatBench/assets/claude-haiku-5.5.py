"""
Draw a cute kitten with matplotlib.

Run it with:
    python kitten.py

A window opens with the drawing (when a display is available), and the
picture is also saved to kitten.png in the current folder.

Requirements:
    pip install matplotlib numpy
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, Ellipse, Polygon

# Colours
BACKGROUND = "#FFF6EA"  # warm cream
FUR = "#F5A65B"         # orange fur
STRIPE = "#DE7F38"      # darker tabby stripes
CREAM = "#FFF1DE"       # muzzle and belly
PINK = "#F7A1B4"        # inside of the ears
NOSE = "#EF7790"
BLUSH = "#FF8FA3"
INK = "#4A3428"         # eyes, mouth and whiskers
COLLAR = "#4C9BE8"
GOLD = "#FFD166"


def mirror(points):
    """Reflect (x, y) points across the kitten's centre line x = 5."""
    return [(10 - x, y) for x, y in points]


def bezier(control_points, t):
    """Points on a cubic Bezier curve for parameter values t in [0, 1]."""
    p0, p1, p2, p3 = (np.asarray(p, dtype=float) for p in control_points)
    t = np.asarray(t, dtype=float)[:, None]
    return ((1 - t) ** 3 * p0
            + 3 * (1 - t) ** 2 * t * p1
            + 3 * (1 - t) * t ** 2 * p2
            + t ** 3 * p3)


def draw_kitten(ax):
    # Soft shadow on the ground (zorder 0 keeps it behind everything)
    ax.add_patch(Ellipse((5.0, 0.95), 4.9, 0.55, color="#EBDCC6", zorder=0))

    # Tail: a low curl on the right (kept below the whiskers), with tabby rings
    tail = [(6.0, 1.7), (8.9, 0.9), (9.7, 2.6), (8.5, 3.9)]
    x, y = bezier(tail, np.linspace(0, 1, 200)).T
    ax.plot(x, y, color=FUR, linewidth=20, solid_capstyle="round", zorder=1)
    for start, end in [(0.40, 0.48), (0.62, 0.70), (0.84, 0.92)]:
        x, y = bezier(tail, np.linspace(start, end, 30)).T
        ax.plot(x, y, color=STRIPE, linewidth=20, solid_capstyle="butt", zorder=1.1)

    # Ears: orange outer shell with a pink inner ear
    outer_left = [(2.9, 7.2), (2.55, 9.4), (4.5, 8.2)]
    inner_left = [(3.07, 7.6), (2.9, 8.95), (4.05, 8.25)]
    for shape in (outer_left, mirror(outer_left)):
        ax.add_patch(Polygon(shape, closed=True, color=FUR, linewidth=8,
                             joinstyle="round", zorder=2))
    for shape in (inner_left, mirror(inner_left)):
        ax.add_patch(Polygon(shape, closed=True, color=PINK, linewidth=6,
                             joinstyle="round", zorder=2.1))

    # Body, belly and front paws
    ax.add_patch(Ellipse((5.0, 2.85), 3.4, 3.1, color=FUR, zorder=3))
    ax.add_patch(Ellipse((5.0, 2.65), 1.9, 2.0, color=CREAM, zorder=4))
    for paw_x in (4.25, 5.75):
        ax.add_patch(Ellipse((paw_x, 1.35), 1.0, 0.58, color=FUR, zorder=5))
        for toe_dx, toe_y in [(-0.27, 1.3), (0.0, 1.22), (0.27, 1.3)]:
            ax.add_patch(Ellipse((paw_x + toe_dx, toe_y), 0.16, 0.12,
                                 color=STRIPE, zorder=5.1))

    # Head, muzzle and forehead stripes
    ax.add_patch(Ellipse((5.0, 6.2), 4.4, 3.8, color=FUR, zorder=6))
    ax.add_patch(Ellipse((5.0, 5.2), 1.9, 1.2, color=CREAM, zorder=6.5))
    for (x0, y0), (x1, y1) in [((5.0, 7.9), (5.0, 7.35)),
                               ((3.85, 7.55), (3.5, 7.15)),
                               ((6.15, 7.55), (6.5, 7.15))]:
        ax.plot([x0, x1], [y0, y1], color=STRIPE, linewidth=7,
                solid_capstyle="round", zorder=6.6)

    # Big sparkly eyes
    for ex in (3.9, 6.1):
        ax.add_patch(Ellipse((ex, 6.05), 0.62, 0.84, color=INK, zorder=7))
    for hx, hy, r in [(3.98, 6.3, 0.12), (3.8, 5.85, 0.06),
                      (6.02, 6.3, 0.12), (6.2, 5.85, 0.06)]:
        ax.add_patch(Circle((hx, hy), r, color="white", zorder=7.1))

    # Rosy cheeks
    for bx in (3.2, 6.8):
        ax.add_patch(Ellipse((bx, 5.4), 0.7, 0.4, color=BLUSH, alpha=0.6,
                             zorder=6.8))

    # Pink nose and a little "w" mouth
    ax.add_patch(Polygon([(4.8, 5.6), (5.2, 5.6), (5.0, 5.38)], closed=True,
                         color=NOSE, linewidth=4, joinstyle="round", zorder=7))
    ax.plot([5.0, 5.0], [5.38, 5.15], color=INK, linewidth=2, zorder=7)
    for cx in (4.75, 5.25):
        ax.add_patch(Arc((cx, 5.15), 0.5, 0.34, theta1=180, theta2=360,
                         color=INK, linewidth=2, zorder=7))

    # Whiskers, three on each side
    for (x0, y0), (x1, y1) in [((2.9, 5.45), (0.6, 5.85)),
                               ((2.95, 5.2), (0.55, 5.15)),
                               ((2.9, 4.95), (0.7, 4.5))]:
        for xa, xb in [(x0, x1), (10 - x0, 10 - x1)]:
            ax.plot([xa, xb], [y0, y1], color=INK, linewidth=1.6,
                    solid_capstyle="round", zorder=7.2)

    # Collar with a little bell
    ax.add_patch(Arc((5.0, 4.6), 2.6, 0.9, theta1=200, theta2=340,
                     color=COLLAR, linewidth=9, zorder=8))
    ax.add_patch(Circle((5.0, 3.92), 0.2, facecolor=GOLD, edgecolor="#B8860B",
                        linewidth=1.2, zorder=9))
    ax.add_patch(Circle((4.93, 3.99), 0.05, color="white", alpha=0.8, zorder=9.1))

    # Sparkles and a speech bubble
    ax.scatter([1.0, 1.9, 8.9], [3.4, 8.7, 7.6], marker="*", s=[160, 100, 130],
               color=GOLD, edgecolors="#E9A800", linewidths=0.8, zorder=10)
    ax.text(8.6, 9.1, "meow!", fontsize=16, fontweight="bold", color=INK,
            ha="center", va="center", zorder=10,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                      edgecolor=STRIPE, linewidth=1.5))


def main():
    fig = plt.figure(figsize=(6, 6.6))
    fig.patch.set_facecolor(BACKGROUND)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BACKGROUND)
    ax.set_xlim(0, 10)
    ax.set_ylim(0.3, 10)
    ax.set_aspect("equal")
    ax.axis("off")

    draw_kitten(ax)

    fig.savefig("kitten.png", dpi=200, facecolor=BACKGROUND, bbox_inches="tight")
    print("Saved kitten.png")
    plt.show()


if __name__ == "__main__":
    main()
