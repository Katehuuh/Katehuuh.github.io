#!/usr/bin/env python3
"""Draw a cute kitten with matplotlib patches."""

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, FancyBboxPatch, Arc
from matplotlib.collections import PatchCollection
import numpy as np


def draw_cute_kitten():
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("#FFF8F0")
    ax.set_facecolor("#FFF8F0")

    # Body
    body = Ellipse((5, 3.2), 4.2, 3.6,
                   facecolor="#F4A460", edgecolor="#D2691E", linewidth=2)
    ax.add_patch(body)

    # Belly
    belly = Ellipse((5, 3.0), 2.4, 2.2,
                    facecolor="#FFE4C4", edgecolor="none")
    ax.add_patch(belly)

    # Head
    head = Circle((5, 6.2), 2.1,
                  facecolor="#F4A460", edgecolor="#D2691E", linewidth=2)
    ax.add_patch(head)

    # Ears (outer)
    left_ear = Polygon([[3.3, 7.4], [3.5, 9.1], [4.5, 7.8]],
                       closed=True, facecolor="#F4A460",
                       edgecolor="#D2691E", linewidth=2)
    right_ear = Polygon([[6.7, 7.4], [6.5, 9.1], [5.5, 7.8]],
                        closed=True, facecolor="#F4A460",
                        edgecolor="#D2691E", linewidth=2)
    ax.add_patch(left_ear)
    ax.add_patch(right_ear)

    # Ears (inner pink)
    left_inner = Polygon([[3.55, 7.55], [3.7, 8.6], [4.25, 7.8]],
                         closed=True, facecolor="#FFB6C1", edgecolor="none")
    right_inner = Polygon([[6.45, 7.55], [6.3, 8.6], [5.75, 7.8]],
                          closed=True, facecolor="#FFB6C1", edgecolor="none")
    ax.add_patch(left_inner)
    ax.add_patch(right_inner)

    # Eyes (whites)
    ax.add_patch(Ellipse((4.2, 6.4), 0.9, 1.05,
                        facecolor="white", edgecolor="#D2691E", linewidth=1.5))
    ax.add_patch(Ellipse((5.8, 6.4), 0.9, 1.05,
                        facecolor="white", edgecolor="#D2691E", linewidth=1.5))

    # Pupils
    ax.add_patch(Ellipse((4.3, 6.3), 0.38, 0.55, facecolor="#2F1B14"))
    ax.add_patch(Ellipse((5.9, 6.3), 0.38, 0.55, facecolor="#2F1B14"))

    # Eye shine
    ax.add_patch(Circle((4.15, 6.55), 0.12, facecolor="white"))
    ax.add_patch(Circle((5.75, 6.55), 0.12, facecolor="white"))
    ax.add_patch(Circle((4.4, 6.15), 0.06, facecolor="white", alpha=0.7))
    ax.add_patch(Circle((6.0, 6.15), 0.06, facecolor="white", alpha=0.7))

    # Nose
    nose = Polygon([[5.0, 5.85], [4.7, 5.55], [5.3, 5.55]],
                   closed=True, facecolor="#FF69B4", edgecolor="#E75480", linewidth=1)
    ax.add_patch(nose)

    # Mouth
    ax.plot([5.0, 5.0], [5.55, 5.3], color="#8B4513", linewidth=1.5)
    mouth_l = Arc((4.75, 5.3), 0.5, 0.4, angle=0, theta1=200, theta2=340,
                  color="#8B4513", linewidth=1.5)
    mouth_r = Arc((5.25, 5.3), 0.5, 0.4, angle=0, theta1=200, theta2=340,
                  color="#8B4513", linewidth=1.5)
    ax.add_patch(mouth_l)
    ax.add_patch(mouth_r)

    # Whiskers
    for y in (5.7, 5.5, 5.3):
        ax.plot([2.6, 4.3], [y + 0.15, y], color="#8B4513",
                linewidth=1.2, alpha=0.7)
        ax.plot([5.7, 7.4], [y, y + 0.15], color="#8B4513",
                linewidth=1.2, alpha=0.7)

    # Cheeks
    ax.add_patch(Circle((3.7, 5.7), 0.35, facecolor="#FFB6C1", alpha=0.55))
    ax.add_patch(Circle((6.3, 5.7), 0.35, facecolor="#FFB6C1", alpha=0.55))

    # Paws
    for x in (3.6, 4.6, 5.4, 6.4):
        ax.add_patch(Ellipse((x, 1.55), 0.85, 0.7,
                            facecolor="#F4A460", edgecolor="#D2691E", linewidth=1.5))
        ax.add_patch(Ellipse((x, 1.35), 0.55, 0.35,
                            facecolor="#FFE4C4", edgecolor="none"))

    # Tail
    t = np.linspace(0, np.pi * 0.9, 80)
    tail_x = 7.0 + 1.4 * np.cos(t - 0.4)
    tail_y = 3.2 + 1.8 * np.sin(t - 0.4)
    ax.plot(tail_x, tail_y, color="#D2691E", linewidth=10, solid_capstyle="round")
    ax.plot(tail_x, tail_y, color="#F4A460", linewidth=7, solid_capstyle="round")

    # Stripes on forehead & body
    for dx, dy in [(-0.35, 0), (0, 0.1), (0.35, 0)]:
        ax.plot([5 + dx, 5 + dx * 0.4],
                [7.5 + dy, 7.0], color="#D2691E",
                linewidth=2.2, solid_capstyle="round", alpha=0.7)

    ax.set_title("A Very Cute Kitten 🐱", fontsize=16,
                fontweight="bold", color="#8B4513", pad=12)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    draw_cute_kitten()
