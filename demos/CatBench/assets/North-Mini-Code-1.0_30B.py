#!/usr/bin/env python
"""
Cute Kitten Drawing Script using Matplotlib

This script creates a simple, cartoonish kitten using matplotlib's
patches and lines. The drawing consists of:
- A cream-colored body and head
- Two pointed ears
- Two eyes with pupils
- A small pink nose
- A smiling mouth
- Whiskers
- A fluffy tail

Run this script with:   python kitten.py
(Requires matplotlib and optionally numpy for helper calculations.)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

def draw_kitten():
    # Create a figure and axis with equal aspect ratio for correct proportions
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.axis('off')          # Hide axes for a clean illustration
    fig.patch.set_facecolor('lightgray')   # Light background

    # ---------- Body ----------
    # Cream torso (large ellipse)
    body = mpatches.Ellipse((0, -1), width=4, height=2, angle=0,
                            facecolor='#f7cdac', edgecolor='none', zorder=1)
    ax.add_patch(body)

    # ---------- Head ----------
    # Main head ellipse
    head = mpatches.Ellipse((-1, 1.5), width=2, height=2.2, angle=0,
                            facecolor='#f7cdac', edgecolor='none', zorder=2)
    ax.add_patch(head)

    # ---------- Ears ----------
    # Left ear (triangle)
    left_ear = mpatches.Polygon(xy=[(-2.2, 3.2), (-1.2, 2.5), (-2, 3)],
                                facecolor='#f7cdac', edgecolor='none', zorder=3)
    # Right ear (triangle, mirrored)
    right_ear = mpatches.Polygon(xy=[(0.8, 3.2), (1.8, 2.5), (1, 3)],
                                 facecolor='#f7cdac', edgecolor='none', zorder=3)
    ax.add_patch(left_ear)
    ax.add_patch(right_ear)

    # ---------- Eyes ----------
    # White part of each eye
    left_eye_white = mpatches.Circle((-0.7, 2.2), 0.3, facecolor='white',
                                     edgecolor='black', linewidth=1, zorder=4)
    right_eye_white = mpatches.Circle((0.3, 2.2), 0.3, facecolor='white',
                                      edgecolor='black', linewidth=1, zorder=4)
    # Pupils (black circles)
    left_eye_pupil = mpatches.Circle((-0.7, 2.2), 0.12, facecolor='black',
                                     zorder=5)
    right_eye_pupil = mpatches.Circle((0.3, 2.2), 0.12, facecolor='black',
                                      zorder=5)

    ax.add_patch(left_eye_white)
    ax.add_patch(right_eye_white)
    ax.add_patch(left_eye_pupil)
    ax.add_patch(right_eye_pupil)

    # ---------- Nose ----------
    # Small pinkish ellipse
    nose = mpatches.Ellipse((-0.1, 1.5), width=0.3, height=0.15,
                            angle=0, facecolor='#f9b3b3', edgecolor='none',
                            zorder=3)
    ax.add_patch(nose)

    # ---------- Mouth / Smile ----------
    # Use an Arc to draw a cute smile
    smile = mpatches.Arc((-0.1, 1.35), width=0.4, height=0.2, angle=0,
                         theta1=210, theta2=330, color='pink',
                         linewidth=2, zorder=3)
    ax.add_patch(smile)

    # ---------- Whiskers ----------
    # Helper function to draw a whisker line
    def whisker(start, end):
        line = FancyArrowPatch(start, end,
                               arrowstyle='-|>',
                               color='black',
                               linewidth=1,
                               zorder=2,
                               shrinkA=4, shrinkB=4)
        ax.add_patch(line)

    # Left whiskers (three lines)
    whisker((-2.2, 2.1), (-3.5, 1.6))
    whisker((-2.2, 2),   (-3.3, 1.3))
    whisker((-2.2, 1.9), (-3.1, 1))

    # Right whiskers (mirrored)
    whisker((0.8, 2.1), (2.2, 1.6))
    whisker((0.8, 2),   (2.0, 1.3))
    whisker((0.8, 1.9), (1.9, 1))

    # ---------- Tail ----------
    # A fluffy tail using a series of arcs
    tail_path = mpatches.Path([(1.8, -1.2), (2.8, -1.5), (3.2, -2),
                               (3.5, -2.5), (3.3, -3), (2.8, -3.5),
                               (2.2, -3.2), (1.8, -2.8)],
                              closed=False)
    tail = mpatches.PathPatch(tail_path, facecolor='#f7cdac',
                              edgecolor='none', zorder=1, alpha=0.8)
    ax.add_patch(tail)

    # ---------- Optional fur details ----------
    # Add a few small circles for a textured kitten feel
    import random
    for _ in range(15):
        x = random.uniform(-2, 3)
        y = random.uniform(-2, 3)
        r = random.uniform(0.05, 0.15)
        circle = mpatches.Circle((x, y), r, color='#eecfda',
                                 edgecolor=None, zorder=0)
        ax.add_patch(circle)

    # Adjust plot limits to include the whole kitten
    ax.set_xlim(-5, 5)
    ax.set_ylim(-4, 5)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    draw_kitten()
