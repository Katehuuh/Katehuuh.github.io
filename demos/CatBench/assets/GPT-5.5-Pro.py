#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import Circle, Ellipse, Polygon, Arc, PathPatch
from matplotlib.path import Path


def _bezier_curve(p0, p1, p2, p3, n=140):
    """Return points along a cubic Bézier curve."""
    p0, p1, p2, p3 = map(lambda p: np.array(p, dtype=float), (p0, p1, p2, p3))
    t = np.linspace(0, 1, n)[:, None]
    pts = (
        (1 - t) ** 3 * p0
        + 3 * (1 - t) ** 2 * t * p1
        + 3 * (1 - t) * t**2 * p2
        + t**3 * p3
    )
    return pts[:, 0], pts[:, 1]


def _bezier_point_normal(t, p0, p1, p2, p3):
    """Return a point and normal vector on a cubic Bézier curve."""
    p0, p1, p2, p3 = map(lambda p: np.array(p, dtype=float), (p0, p1, p2, p3))

    point = (
        (1 - t) ** 3 * p0
        + 3 * (1 - t) ** 2 * t * p1
        + 3 * (1 - t) * t**2 * p2
        + t**3 * p3
    )

    tangent = (
        3 * (1 - t) ** 2 * (p1 - p0)
        + 6 * (1 - t) * t * (p2 - p1)
        + 3 * t**2 * (p3 - p2)
    )

    length = np.linalg.norm(tangent)
    if length == 0:
        normal = np.array([0.0, 1.0])
    else:
        normal = np.array([-tangent[1], tangent[0]]) / length

    return point, normal


def _quad_stroke(ax, p0, p1, p2, color, linewidth, zorder):
    """Draw a smooth quadratic curve."""
    path = Path([p0, p1, p2], [Path.MOVETO, Path.CURVE3, Path.CURVE3])
    ax.add_patch(
        PathPatch(
            path,
            fill=False,
            edgecolor=color,
            linewidth=linewidth,
            capstyle="round",
            joinstyle="round",
            zorder=zorder,
        )
    )


def draw_cute_kitten(save_path=None):
    # Palette
    bg = "#fff4f8"
    fur = "#f7c99a"
    fur_light = "#ffe6ca"
    outline = "#6b4630"
    inner_ear = "#ffb3c7"
    blush = "#ff8fb1"
    stripe = "#c8875f"
    collar = "#e85d75"
    tag = "#ffd166"
    eye = "#241716"

    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)

    # Cute background doodles
    for x, y, char, size in [
        (-2.35, 2.25, "♡", 30),
        (2.25, 2.15, "♡", 26),
        (-2.55, -0.25, "✦", 20),
        (2.35, -0.05, "✦", 18),
        (0.0, 2.75, "✧", 22),
    ]:
        ax.text(
            x,
            y,
            char,
            ha="center",
            va="center",
            fontsize=size,
            color="#f3a4bb",
            alpha=0.75,
            zorder=0,
        )

    # Soft shadow
    ax.add_patch(
        Ellipse(
            (0, -2.02),
            2.7,
            0.35,
            facecolor="#d9b8a6",
            edgecolor="none",
            alpha=0.25,
            zorder=0.1,
        )
    )

    # Tail behind the body
    tail_p0 = (1.05, -1.13)
    tail_p1 = (2.65, -0.85)
    tail_p2 = (2.35, 1.35)
    tail_p3 = (1.05, 0.75)

    tx, ty = _bezier_curve(tail_p0, tail_p1, tail_p2, tail_p3)
    ax.plot(tx, ty, color=outline, linewidth=44, solid_capstyle="round", zorder=1)
    ax.plot(tx, ty, color=fur, linewidth=34, solid_capstyle="round", zorder=1.1)

    # Tail stripes
    for t in [0.22, 0.38, 0.55, 0.72]:
        p, n = _bezier_point_normal(t, tail_p0, tail_p1, tail_p2, tail_p3)
        a = p - n * 0.20
        b = p + n * 0.20
        ax.plot(
            [a[0], b[0]],
            [a[1], b[1]],
            color=stripe,
            linewidth=5,
            solid_capstyle="round",
            alpha=0.85,
            zorder=1.2,
        )

    # Body
    ax.add_patch(
        Ellipse(
            (0, -0.78),
            2.35,
            2.45,
            facecolor=fur,
            edgecolor=outline,
            linewidth=3,
            zorder=2,
        )
    )

    # Belly
    ax.add_patch(
        Ellipse(
            (0, -0.92),
            1.15,
            1.35,
            facecolor=fur_light,
            edgecolor="none",
            alpha=0.85,
            zorder=3,
        )
    )

    # Ears
    left_ear = [(-1.03, 1.55), (-0.42, 1.84), (-0.91, 2.58)]
    right_ear = [(1.03, 1.55), (0.42, 1.84), (0.91, 2.58)]

    ax.add_patch(
        Polygon(
            left_ear,
            closed=True,
            facecolor=fur,
            edgecolor=outline,
            linewidth=3,
            joinstyle="round",
            zorder=4,
        )
    )
    ax.add_patch(
        Polygon(
            right_ear,
            closed=True,
            facecolor=fur,
            edgecolor=outline,
            linewidth=3,
            joinstyle="round",
            zorder=4,
        )
    )

    ax.add_patch(
        Polygon(
            [(-0.87, 1.75), (-0.55, 1.91), (-0.83, 2.34)],
            closed=True,
            facecolor=inner_ear,
            edgecolor="none",
            alpha=0.9,
            zorder=4.5,
        )
    )
    ax.add_patch(
        Polygon(
            [(0.87, 1.75), (0.55, 1.91), (0.83, 2.34)],
            closed=True,
            facecolor=inner_ear,
            edgecolor="none",
            alpha=0.9,
            zorder=4.5,
        )
    )

    # Head
    ax.add_patch(
        Circle(
            (0, 0.72),
            1.25,
            facecolor=fur,
            edgecolor=outline,
            linewidth=3,
            zorder=5,
        )
    )

    # Forehead stripes
    _quad_stroke(ax, (-0.33, 1.78), (-0.28, 1.57), (-0.16, 1.42), stripe, 4, 6)
    _quad_stroke(ax, (0.00, 1.84), (0.00, 1.58), (0.00, 1.43), stripe, 4, 6)
    _quad_stroke(ax, (0.33, 1.78), (0.28, 1.57), (0.16, 1.42), stripe, 4, 6)

    # Cheek stripes
    _quad_stroke(ax, (-0.95, 0.95), (-0.75, 0.90), (-0.58, 0.80), stripe, 3, 6)
    _quad_stroke(ax, (-1.02, 0.66), (-0.80, 0.62), (-0.62, 0.52), stripe, 3, 6)
    _quad_stroke(ax, (0.95, 0.95), (0.75, 0.90), (0.58, 0.80), stripe, 3, 6)
    _quad_stroke(ax, (1.02, 0.66), (0.80, 0.62), (0.62, 0.52), stripe, 3, 6)

    # Paws
    for x in [-0.45, 0.45]:
        ax.add_patch(
            Ellipse(
                (x, -1.65),
                0.56,
                0.46,
                facecolor=fur,
                edgecolor=outline,
                linewidth=2.5,
                zorder=6,
            )
        )
        for dx in [-0.10, 0.10]:
            ax.plot(
                [x + dx, x + dx * 0.8],
                [-1.54, -1.72],
                color=outline,
                linewidth=1.8,
                solid_capstyle="round",
                alpha=0.85,
                zorder=7,
            )

    # Collar as a curved band
    theta = np.linspace(np.deg2rad(200), np.deg2rad(340), 120)
    cx, cy = 0.0, -0.26
    rx, ry = 0.72, 0.32
    collar_x = cx + rx * np.cos(theta)
    collar_y = cy + ry * np.sin(theta)

    ax.plot(
        collar_x,
        collar_y,
        color=outline,
        linewidth=10,
        solid_capstyle="round",
        zorder=6.8,
    )
    ax.plot(
        collar_x,
        collar_y,
        color=collar,
        linewidth=7,
        solid_capstyle="round",
        zorder=6.9,
    )

    # Bell tag
    ax.add_patch(
        Circle(
            (0, -0.56),
            0.14,
            facecolor=tag,
            edgecolor=outline,
            linewidth=1.5,
            zorder=7.2,
        )
    )
    ax.text(
        0,
        -0.565,
        "✦",
        ha="center",
        va="center",
        fontsize=9,
        color=outline,
        zorder=7.3,
    )

    # Blush
    ax.add_patch(
        Ellipse(
            (-0.72, 0.43),
            0.42,
            0.20,
            facecolor=blush,
            edgecolor="none",
            alpha=0.35,
            zorder=7,
        )
    )
    ax.add_patch(
        Ellipse(
            (0.72, 0.43),
            0.42,
            0.20,
            facecolor=blush,
            edgecolor="none",
            alpha=0.35,
            zorder=7,
        )
    )

    # Muzzle
    ax.add_patch(
        Ellipse(
            (-0.18, 0.46),
            0.45,
            0.34,
            facecolor=fur_light,
            edgecolor="none",
            alpha=0.95,
            zorder=7.1,
        )
    )
    ax.add_patch(
        Ellipse(
            (0.18, 0.46),
            0.45,
            0.34,
            facecolor=fur_light,
            edgecolor="none",
            alpha=0.95,
            zorder=7.1,
        )
    )

    # Eyes
    for x in [-0.43, 0.43]:
        ax.add_patch(
            Ellipse(
                (x, 0.95),
                0.38,
                0.52,
                facecolor=eye,
                edgecolor=outline,
                linewidth=1.2,
                zorder=8,
            )
        )
        ax.add_patch(
            Circle(
                (x - 0.07, 1.08),
                0.075,
                facecolor="white",
                edgecolor="none",
                zorder=9,
            )
        )
        ax.add_patch(
            Circle(
                (x + 0.06, 0.84),
                0.035,
                facecolor="white",
                edgecolor="none",
                alpha=0.9,
                zorder=9,
            )
        )

    # Nose
    ax.text(
        0,
        0.53,
        "♥",
        ha="center",
        va="center",
        fontsize=24,
        color="#e85d75",
        fontweight="bold",
        zorder=9,
    )

    # Mouth
    ax.plot(
        [0, 0],
        [0.45, 0.36],
        color=outline,
        linewidth=2,
        solid_capstyle="round",
        zorder=8.8,
    )
    ax.add_patch(
        Arc(
            (-0.11, 0.36),
            0.25,
            0.18,
            theta1=200,
            theta2=340,
            color=outline,
            linewidth=2,
            zorder=8.8,
        )
    )
    ax.add_patch(
        Arc(
            (0.11, 0.36),
            0.25,
            0.18,
            theta1=200,
            theta2=340,
            color=outline,
            linewidth=2,
            zorder=8.8,
        )
    )

    # Whiskers
    whiskers = [
        ((-0.30, 0.56), (-1.45, 0.80)),
        ((-0.32, 0.45), (-1.55, 0.45)),
        ((-0.30, 0.35), (-1.40, 0.18)),
        ((0.30, 0.56), (1.45, 0.80)),
        ((0.32, 0.45), (1.55, 0.45)),
        ((0.30, 0.35), (1.40, 0.18)),
    ]

    for start, end in whiskers:
        ax.plot(
            [start[0], end[0]],
            [start[1], end[1]],
            color=outline,
            linewidth=2,
            alpha=0.8,
            solid_capstyle="round",
            zorder=8.5,
        )

    # Tiny head fluff
    ax.plot(
        [-0.18, -0.06, 0.03, 0.15],
        [1.88, 2.05, 1.91, 2.03],
        color=outline,
        linewidth=2.2,
        solid_capstyle="round",
        zorder=7,
    )

    ax.set_xlim(-3, 3)
    ax.set_ylim(-2.45, 3.0)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=220, bbox_inches="tight", facecolor=fig.get_facecolor())

    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Draw a cute kitten with matplotlib.")
    parser.add_argument(
        "--save",
        metavar="PATH",
        default=None,
        help="Optionally save the drawing, for example: kitten.png",
    )
    args = parser.parse_args()
    draw_cute_kitten(args.save)


if __name__ == "__main__":
    main()