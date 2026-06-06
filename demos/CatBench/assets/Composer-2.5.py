#!/usr/bin/env python3
"""Draw a cute sleeping curled-up kitten in a cozy pillow/blanket scene."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Arc, Circle, Ellipse, FancyBboxPatch, Polygon, Wedge
import numpy as np


def draw_pillow(ax):
    """Draw a soft pillow beneath the kitten."""
    pillow = FancyBboxPatch(
        (1.8, 1.5), 5.4, 2.2,
        boxstyle="round,pad=0.08,rounding_size=0.6",
        facecolor="#E8D4C4",
        edgecolor="#C9A88E",
        linewidth=2,
        zorder=1,
    )
    ax.add_patch(pillow)

    # Pillow highlight
    highlight = Ellipse(
        (4.0, 2.9), 3.0, 0.5,
        angle=0,
        facecolor="#F5E6D8",
        edgecolor="none",
        alpha=0.6,
        zorder=2,
    )
    ax.add_patch(highlight)

    # Pillow shadow/crease
    crease = Arc(
        (4.5, 2.0), 4.0, 1.2,
        angle=0, theta1=200, theta2=340,
        color="#C9A88E", linewidth=1.5, zorder=2,
    )
    ax.add_patch(crease)


def draw_blanket(ax):
    """Draw a cozy blanket draped over part of the scene."""
    blanket_points = np.array([
        [0.5, 3.2], [1.0, 4.5], [3.0, 5.0], [6.5, 4.8],
        [8.0, 3.8], [7.5, 2.8], [5.5, 2.5], [2.0, 2.6],
    ])
    blanket = Polygon(
        blanket_points,
        closed=True,
        facecolor="#B8D4E8",
        edgecolor="#7BA3C4",
        linewidth=2,
        zorder=3,
        alpha=0.85,
    )
    ax.add_patch(blanket)

    # Blanket fold lines
    for pts in [
        [(2.5, 4.2), (4.0, 4.6), (5.5, 4.3)],
        [(3.5, 3.5), (5.0, 3.8), (6.5, 3.4)],
    ]:
        fold = Polygon(
            pts,
            closed=False,
            fill=False,
            edgecolor="#8BB8D4",
            linewidth=1.2,
            linestyle="--",
            zorder=4,
        )
        ax.add_patch(fold)

    # Blanket fringe
    for x in np.linspace(1.2, 7.8, 8):
        fringe = Ellipse(
            (x, 4.85 + 0.05 * np.sin(x)), 0.15, 0.25,
            facecolor="#A8C8E0",
            edgecolor="#7BA3C4",
            linewidth=0.5,
            zorder=4,
        )
        ax.add_patch(fringe)


def draw_kitten_body(ax):
    """Draw the curled-up sleeping kitten body."""
    # Main body - curled ball shape
    body = Ellipse(
        (4.5, 2.6), 3.2, 2.4,
        angle=-15,
        facecolor="#F4A460",
        edgecolor="#C87830",
        linewidth=2,
        zorder=5,
    )
    ax.add_patch(body)

    # Belly patch (lighter)
    belly = Ellipse(
        (4.2, 2.4), 2.0, 1.5,
        angle=-10,
        facecolor="#FFE4C4",
        edgecolor="none",
        zorder=6,
    )
    ax.add_patch(belly)

    # Head tucked in
    head = Circle(
        (3.0, 2.8), 1.1,
        facecolor="#F4A460",
        edgecolor="#C87830",
        linewidth=2,
        zorder=7,
    )
    ax.add_patch(head)

    # Cheek fluff
    cheek = Circle(
        (2.5, 2.5), 0.35,
        facecolor="#FFE4C4",
        edgecolor="none",
        zorder=8,
    )
    ax.add_patch(cheek)


def draw_kitten_ears(ax):
    """Draw triangular kitten ears."""
    # Left ear
    left_ear = Polygon(
        [(2.2, 3.5), (2.0, 4.3), (2.8, 3.7)],
        closed=True,
        facecolor="#F4A460",
        edgecolor="#C87830",
        linewidth=1.5,
        zorder=8,
    )
    ax.add_patch(left_ear)

    left_inner = Polygon(
        [(2.25, 3.65), (2.15, 4.05), (2.55, 3.75)],
        closed=True,
        facecolor="#FFB6C1",
        edgecolor="none",
        zorder=9,
    )
    ax.add_patch(left_inner)

    # Right ear (partially visible)
    right_ear = Polygon(
        [(3.5, 3.6), (3.3, 4.2), (4.0, 3.65)],
        closed=True,
        facecolor="#F4A460",
        edgecolor="#C87830",
        linewidth=1.5,
        zorder=8,
    )
    ax.add_patch(right_ear)

    right_inner = Polygon(
        [(3.55, 3.72), (3.45, 4.0), (3.8, 3.7)],
        closed=True,
        facecolor="#FFB6C1",
        edgecolor="none",
        zorder=9,
    )
    ax.add_patch(right_inner)


def draw_kitten_face(ax):
    """Draw sleeping face with closed eyes, nose, and whiskers."""
    # Closed eyes (curved arcs - sleeping)
    left_eye = Arc(
        (2.55, 3.0), 0.5, 0.3,
        angle=0, theta1=0, theta2=180,
        color="#5C3D2E", linewidth=2.5, zorder=10,
    )
    ax.add_patch(left_eye)

    right_eye = Arc(
        (3.15, 3.0), 0.5, 0.3,
        angle=0, theta1=0, theta2=180,
        color="#5C3D2E", linewidth=2.5, zorder=10,
    )
    ax.add_patch(right_eye)

    # Little pink nose
    nose = Polygon(
        [(2.85, 2.65), (2.75, 2.55), (2.95, 2.55)],
        closed=True,
        facecolor="#FFB6C1",
        edgecolor="#E8909C",
        linewidth=1,
        zorder=10,
    )
    ax.add_patch(nose)

    # Tiny mouth (content smile while sleeping)
    mouth = Arc(
        (2.85, 2.45), 0.3, 0.2,
        angle=0, theta1=200, theta2=340,
        color="#5C3D2E", linewidth=1.5, zorder=10,
    )
    ax.add_patch(mouth)

    # Whiskers
    whisker_color = "#5C3D2E"
    whiskers = [
        [(2.2, 2.7), (1.3, 2.85)],
        [(2.2, 2.5), (1.2, 2.45)],
        [(2.2, 2.3), (1.3, 2.1)],
        [(3.5, 2.7), (4.2, 2.85)],
        [(3.5, 2.5), (4.3, 2.45)],
    ]
    for start, end in whiskers:
        ax.plot(
            [start[0], end[0]], [start[1], end[1]],
            color=whisker_color, linewidth=1.2, zorder=10,
        )


def draw_kitten_paws_and_tail(ax):
    """Draw tucked paws and curled tail."""
    # Front paw tucked under chin
    front_paw = Ellipse(
        (2.8, 2.2), 0.7, 0.5,
        angle=30,
        facecolor="#F4A460",
        edgecolor="#C87830",
        linewidth=1.5,
        zorder=9,
    )
    ax.add_patch(front_paw)

    # Paw pad
    paw_pad = Circle(
        (2.75, 2.15), 0.12,
        facecolor="#FFB6C1",
        edgecolor="none",
        zorder=10,
    )
    ax.add_patch(paw_pad)

    # Back paw peeking out
    back_paw = Ellipse(
        (5.8, 2.3), 0.8, 0.55,
        angle=-20,
        facecolor="#F4A460",
        edgecolor="#C87830",
        linewidth=1.5,
        zorder=9,
    )
    ax.add_patch(back_paw)

    for dx in [-0.15, 0, 0.15]:
        toe = Circle(
            (5.85 + dx, 2.15), 0.08,
            facecolor="#FFB6C1",
            edgecolor="none",
            zorder=10,
        )
        ax.add_patch(toe)

    # Curled tail wrapping around body
    tail_segments = [
        ((5.5, 2.8), 0.6, 0.35, -60),
        ((6.0, 3.1), 0.55, 0.3, -30),
        ((6.3, 3.5), 0.5, 0.28, 10),
        ((6.1, 3.9), 0.45, 0.25, 50),
    ]
    for center, w, h, angle in tail_segments:
        segment = Ellipse(
            center, w, h,
            angle=angle,
            facecolor="#F4A460",
            edgecolor="#C87830",
            linewidth=1.5,
            zorder=6,
        )
        ax.add_patch(segment)

    # Tail tip (darker stripe)
    tail_tip = Ellipse(
        (5.9, 4.0), 0.35, 0.2,
        angle=60,
        facecolor="#C87830",
        edgecolor="#A06020",
        linewidth=1,
        zorder=7,
    )
    ax.add_patch(tail_tip)

    # Stripes on body
    for center, w, h, angle in [
        ((4.8, 3.0), 0.6, 0.15, -20),
        ((5.3, 2.7), 0.5, 0.12, -30),
        ((4.0, 2.9), 0.4, 0.1, 10),
    ]:
        stripe = Ellipse(
            center, w, h,
            angle=angle,
            facecolor="#E09040",
            edgecolor="none",
            alpha=0.5,
            zorder=7,
        )
        ax.add_patch(stripe)


def draw_cozy_details(ax):
    """Add cozy scene details: zzz, stars, warm glow."""
    # Sleep "Zzz" bubbles
    zzz_positions = [(5.5, 4.5, 18), (6.2, 5.0, 14), (6.7, 5.3, 11)]
    for x, y, size in zzz_positions:
        ax.text(
            x, y, "z",
            fontsize=size,
            fontstyle="italic",
            fontweight="bold",
            color="#7BA3C4",
            alpha=0.7,
            zorder=12,
            ha="center",
            va="center",
        )

    # Soft moon through window (implied cozy night)
    moon = Circle(
        (7.5, 6.5), 0.6,
        facecolor="#FFFACD",
        edgecolor="#F0E68C",
        linewidth=1.5,
        zorder=0,
        alpha=0.8,
    )
    ax.add_patch(moon)

    # Tiny stars
    star_positions = [(1.0, 6.8), (2.5, 7.2), (6.8, 7.0), (0.8, 5.5)]
    for sx, sy in star_positions:
        ax.plot(sx, sy, marker="*", markersize=10, color="#FFFACD", alpha=0.6, zorder=0)

    # Warm floor/rug
    rug = FancyBboxPatch(
        (0.3, 0.3), 8.4, 1.5,
        boxstyle="round,pad=0.05,rounding_size=0.3",
        facecolor="#D4A574",
        edgecolor="#B8895A",
        linewidth=1.5,
        zorder=0,
    )
    ax.add_patch(rug)

    # Rug pattern dots
    for rx in np.linspace(1.0, 8.0, 6):
        for ry in np.linspace(0.6, 1.5, 3):
            ax.plot(rx, ry, "o", markersize=4, color="#C49A6C", alpha=0.5, zorder=1)


def draw_kitten():
    """Main function to compose and display the cozy kitten scene."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    fig.patch.set_facecolor("#2C3E50")
    ax.set_facecolor("#34495E")

    draw_cozy_details(ax)
    draw_pillow(ax)
    draw_blanket(ax)
    draw_kitten_body(ax)
    draw_kitten_ears(ax)
    draw_kitten_face(ax)
    draw_kitten_paws_and_tail(ax)

    ax.set_xlim(0, 9)
    ax.set_ylim(0, 8)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.set_title(
        "Sleepy Kitten ~ Zzz...",
        fontsize=18,
        fontweight="bold",
        color="#F5E6D8",
        pad=15,
        fontfamily="serif",
    )

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    draw_kitten()
