"""
cute_kitten.py — Draw a cute cartoon kitten with matplotlib.

Run:  python cute_kitten.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, Arc, PathPatch
from matplotlib.path import Path


def shrunk(vertices, factor=0.5):
    """Scale a polygon toward its centroid (used for inner ears)."""
    v = np.asarray(vertices, dtype=float)
    centroid = v.mean(axis=0)
    return centroid + factor * (v - centroid)


def draw_kitten():
    fig, ax = plt.subplots(figsize=(8, 9))
    fig.patch.set_facecolor("#FFF9EF")
    ax.set_facecolor("#FFF9EF")
    ax.set_xlim(-11, 11)
    ax.set_ylim(-11, 11)
    ax.set_aspect("equal")
    ax.axis("off")

    # ---- palette ----
    FUR, FUR_DARK = "#F6A85C", "#DE8A34"      # orange tabby coat
    EAR_PINK, NOSE_PINK, BLUSH = "#F9BFC8", "#EF7FA3", "#FFAB91"
    INK, EYE = "#4E342E", "#33241C"

    # ---- ground shadow ----
    ax.add_patch(Ellipse((0, -9.5), 13, 1.5, facecolor="black",
                         alpha=0.08, edgecolor="none"))

    # ---- tail (drawn first so it sits behind the body) ----
    tail = Path([(4.5, -5.5), (9.0, -6.2), (10.2, -1.0), (7.6, 0.6)],
                [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4])
    ax.add_patch(PathPatch(tail, fill=False, edgecolor=FUR,
                           linewidth=30, capstyle="round"))
    ax.add_patch(Circle((7.6, 0.6), 0.63, facecolor=FUR_DARK,
                        edgecolor="none"))                 # dark tail tip

    # ---- body & chest ----
    ax.add_patch(Ellipse((0, -4.8), 10, 8, facecolor=FUR, edgecolor="none"))
    ax.add_patch(Ellipse((0, -4.0), 5.4, 5.6, facecolor="#FFE3BF",
                         edgecolor="none"))                # cream chest

    # ---- front paws with toe lines ----
    for x in (-2.3, 2.3):
        ax.add_patch(Ellipse((x, -8.0), 2.6, 1.6, facecolor=FUR,
                             edgecolor="none"))
        for dx in (-0.5, 0.5):
            ax.plot([x + dx, x + dx], [-8.75, -8.25],
                    color=FUR_DARK, lw=2, solid_capstyle="round")

    # ---- ears (behind the head) ----
    left_ear  = [(-4.8, 4.0), (-4.0, 8.4), (-0.6, 5.4)]
    right_ear = [( 4.8, 4.0), ( 4.0, 8.4), ( 0.6, 5.4)]
    for ear in (left_ear, right_ear):
        ax.add_patch(Polygon(ear, closed=True, facecolor=FUR,
                             edgecolor="none"))
        ax.add_patch(Polygon(shrunk(ear, 0.5), closed=True,
                             facecolor=EAR_PINK, edgecolor="none"))

    # ---- head ----
    ax.add_patch(Circle((0, 2.2), 4.6, facecolor=FUR, edgecolor="none"))

    # ---- forehead stripes ----
    for x, y1, y2 in [(-1.0, 5.1, 6.1), (0.0, 5.0, 6.4), (1.0, 5.1, 6.1)]:
        ax.plot([x, x], [y1, y2], color=FUR_DARK, lw=5,
                solid_capstyle="round")

    # ---- big sparkly eyes ----
    for sx in (-1, 1):
        ex = 1.7 * sx
        ax.add_patch(Circle((ex, 2.4), 0.95, facecolor=EYE, edgecolor="none"))
        ax.add_patch(Circle((ex - 0.32 * sx, 2.75), 0.30,
                            facecolor="white", edgecolor="none"))
        ax.add_patch(Circle((ex + 0.28 * sx, 2.05), 0.13, alpha=0.9,
                            facecolor="white", edgecolor="none"))

    # ---- blush ----
    for sx in (-1, 1):
        ax.add_patch(Circle((3.1 * sx, 0.9), 0.75, facecolor=BLUSH,
                            alpha=0.55, edgecolor="none"))

    # ---- nose and "w" mouth ----
    ax.add_patch(Polygon([(-0.42, 1.52), (0.42, 1.52), (0.0, 1.02)],
                         closed=True, facecolor=NOSE_PINK, edgecolor="none"))
    ax.plot([0, 0], [1.02, 0.76], color=INK, lw=2.5,
            solid_capstyle="round")
    for sx in (-1, 1):
        ax.add_patch(Arc((0.55 * sx, 0.74), 1.1, 0.9,
                         theta1=180, theta2=360, edgecolor=INK, lw=2.5))

    # ---- whiskers ----
    whiskers = [((2.4, 1.4), (6.8, 2.3)),
                ((2.5, 0.9), (7.1, 0.9)),
                ((2.4, 0.4), (6.8, -0.5))]
    for (x0, y0), (x1, y1) in whiskers:
        for sx in (-1, 1):
            ax.plot([sx * x0, sx * x1], [y0, y1], color=INK, lw=1.8,
                    solid_capstyle="round")

    # ---- finishing touches ----
    ax.text(-6.6, 7.6, "\u2665", color="#F48FB1", fontsize=22, ha="center")
    ax.text( 6.9, 6.2, "\u2665", color="#F8BBD0", fontsize=15, ha="center")
    ax.text(0, 9.7, "~ Meow! ~", ha="center", fontsize=15,
            color=INK, style="italic")

    plt.tight_layout()
    plt.savefig("kitten.png", dpi=150, bbox_inches="tight")  # optional
    plt.show()


if __name__ == "__main__":
    draw_kitten()
