#!/usr/bin/env python3
"""
Candidate 10: Elegant minimalist line-focused cute kitten (clean lines, soft pastels, large almond eyes, few whiskers, negative space charm).
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, Arc, Rectangle


def draw_kitten(ax):
    ax.set_xlim(-4.6, 4.6)
    ax.set_ylim(-3.3, 4.5)
    ax.set_aspect('equal')
    ax.axis('off')

    outline = '#4A4A4A'
    head_fill = '#FFF8F0'
    ear_fill = '#EDE4F7'
    inner = '#FFE8F0'
    eye_white = '#FFFEFA'
    pupil = '#6B6B8A'
    blush = '#F8C8D8'
    nose = '#F8A0A8'
    w_color = '#5A5A5A'
    bg = '#F7F3FA'

    # Very light background wash
    ax.add_patch(Rectangle((-5.5, -4), 11, 9.5, facecolor=bg, alpha=0.55, edgecolor='none', zorder=0))

    # Head
    ax.add_patch(Circle((0, 0), 2.25, facecolor=head_fill, edgecolor=outline, linewidth=1.55, zorder=1))

    # Ears (tall elegant)
    ax.add_patch(Polygon([(-1.28, 1.58), (-2.18, 3.62), (-0.18, 1.82)], closed=True, facecolor=ear_fill, edgecolor=outline, linewidth=1.45, zorder=1))
    ax.add_patch(Polygon([(-1.12, 1.82), (-1.92, 3.15), (-0.32, 1.95)], closed=True, facecolor=inner, edgecolor='none', zorder=2))
    ax.add_patch(Polygon([(1.28, 1.58), (2.18, 3.62), (0.18, 1.82)], closed=True, facecolor=ear_fill, edgecolor=outline, linewidth=1.45, zorder=1))
    ax.add_patch(Polygon([(1.12, 1.82), (1.92, 3.15), (0.32, 1.95)], closed=True, facecolor=inner, edgecolor='none', zorder=2))

    # Soft blush
    ax.add_patch(Circle((-1.12, 0.02), 0.42, facecolor=blush, alpha=0.22, zorder=2))
    ax.add_patch(Circle((1.12, 0.02), 0.42, facecolor=blush, alpha=0.22, zorder=2))

    # Large softly tilted almond eyes
    ax.add_patch(Ellipse((-0.82, 0.38), 1.02, 0.58, angle=11, facecolor=eye_white, edgecolor=outline, linewidth=1.15, zorder=3))
    ax.add_patch(Ellipse((0.82, 0.38), 1.02, 0.58, angle=-11, facecolor=eye_white, edgecolor=outline, linewidth=1.15, zorder=3))
    ax.add_patch(Circle((-0.82, 0.365), 0.165, facecolor=pupil, zorder=4))
    ax.add_patch(Circle((0.82, 0.365), 0.165, facecolor=pupil, zorder=4))
    ax.add_patch(Circle((-0.75, 0.47), 0.055, facecolor='white', alpha=0.95, zorder=5))
    ax.add_patch(Circle((0.89, 0.47), 0.055, facecolor='white', alpha=0.95, zorder=5))

    # Delicate long lashes
    ax.plot([-0.98, -1.18], [0.66, 0.92], color=outline, linewidth=0.75, zorder=6)
    ax.plot([-0.82, -0.90], [0.68, 0.95], color=outline, linewidth=0.75, zorder=6)
    ax.plot([-0.66, -0.58], [0.66, 0.88], color=outline, linewidth=0.75, zorder=6)
    ax.plot([0.98, 1.18], [0.66, 0.92], color=outline, linewidth=0.75, zorder=6)
    ax.plot([0.82, 0.90], [0.68, 0.95], color=outline, linewidth=0.75, zorder=6)
    ax.plot([0.66, 0.58], [0.66, 0.88], color=outline, linewidth=0.75, zorder=6)

    # Minimal nose
    ax.add_patch(Ellipse((0, -0.25), 0.30, 0.17, facecolor=nose, edgecolor='#5F5F5F', linewidth=0.65, zorder=4))

    # Subtle single-line mouth
    ax.add_patch(Arc((0, -0.48), 0.32, 0.22, theta1=205, theta2=335, color=w_color, linewidth=0.85, zorder=5))

    # Few long elegant whiskers (negative space)
    ax.plot([-1.42, -3.65], [0.32, 0.52], color=w_color, linewidth=0.65, zorder=6)
    ax.plot([-1.48, -3.82], [0.08, 0.08], color=w_color, linewidth=0.65, zorder=6)
    ax.plot([-1.42, -3.55], [-0.15, -0.32], color=w_color, linewidth=0.65, zorder=6)
    ax.plot([1.42, 3.65], [0.32, 0.52], color=w_color, linewidth=0.65, zorder=6)
    ax.plot([1.48, 3.82], [0.08, 0.08], color=w_color, linewidth=0.65, zorder=6)
    ax.plot([1.42, 3.55], [-0.15, -0.32], color=w_color, linewidth=0.65, zorder=6)


if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(7.2, 7.8), facecolor='#F4F0F8')
    draw_kitten(ax)
    # Display the plot interactively on screen (normal behavior).
    # Close the window to exit the script.
    plt.show()
