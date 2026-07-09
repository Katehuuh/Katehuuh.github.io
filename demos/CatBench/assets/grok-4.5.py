#!/usr/bin/env python3
"""
Cute Kitten Drawer using Matplotlib
Draws an adorable cartoon kitten face with geometric shapes.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, Arc, FancyBboxPatch
import numpy as np

def draw_cute_kitten():
    # Create figure with a soft background
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='#FFF8F0')
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor('#FFF8F0')

    # ========== HEAD ==========
    head = Circle((0, 0), 1.35, 
                  facecolor='#F4A460',  # Sandy brown / orange tabby
                  edgecolor='#8B4513', 
                  linewidth=3,
                  zorder=1)
    ax.add_patch(head)

    # Soft cheek shading
    left_cheek = Ellipse((-0.55, -0.15), 0.7, 0.55,
                         facecolor='#E8956A', alpha=0.35, zorder=2)
    right_cheek = Ellipse((0.55, -0.15), 0.7, 0.55,
                          facecolor='#E8956A', alpha=0.35, zorder=2)
    ax.add_patch(left_cheek)
    ax.add_patch(right_cheek)

    # ========== EARS ==========
    # Outer ears
    left_ear = Polygon(
        [[-0.75, 0.85], [-1.25, 1.85], [-0.25, 1.25]],
        closed=True,
        facecolor='#F4A460',
        edgecolor='#8B4513',
        linewidth=3,
        zorder=0
    )
    right_ear = Polygon(
        [[0.75, 0.85], [1.25, 1.85], [0.25, 1.25]],
        closed=True,
        facecolor='#F4A460',
        edgecolor='#8B4513',
        linewidth=3,
        zorder=0
    )
    ax.add_patch(left_ear)
    ax.add_patch(right_ear)

    # Inner ears (pink)
    left_inner_ear = Polygon(
        [[-0.70, 0.95], [-1.05, 1.65], [-0.40, 1.20]],
        closed=True,
        facecolor='#FFB6C1',
        edgecolor='none',
        zorder=1
    )
    right_inner_ear = Polygon(
        [[0.70, 0.95], [1.05, 1.65], [0.40, 1.20]],
        closed=True,
        facecolor='#FFB6C1',
        edgecolor='none',
        zorder=1
    )
    ax.add_patch(left_inner_ear)
    ax.add_patch(right_inner_ear)

    # ========== EYES (big and sparkly for maximum cuteness) ==========
    # Eye whites
    left_eye = Circle((-0.45, 0.25), 0.32,
                      facecolor='white',
                      edgecolor='#333333',
                      linewidth=2.5,
                      zorder=3)
    right_eye = Circle((0.45, 0.25), 0.32,
                       facecolor='white',
                       edgecolor='#333333',
                       linewidth=2.5,
                       zorder=3)
    ax.add_patch(left_eye)
    ax.add_patch(right_eye)

    # Irises (soft green-gold)
    left_iris = Circle((-0.42, 0.27), 0.20,
                       facecolor='#90EE90',
                       edgecolor='#228B22',
                       linewidth=1,
                       zorder=4)
    right_iris = Circle((0.48, 0.27), 0.20,
                        facecolor='#90EE90',
                        edgecolor='#228B22',
                        linewidth=1,
                        zorder=4)
    ax.add_patch(left_iris)
    ax.add_patch(right_iris)

    # Pupils
    left_pupil = Circle((-0.40, 0.28), 0.11,
                        facecolor='#1a1a1a',
                        zorder=5)
    right_pupil = Circle((0.50, 0.28), 0.11,
                         facecolor='#1a1a1a',
                         zorder=5)
    ax.add_patch(left_pupil)
    ax.add_patch(right_pupil)

    # Eye sparkles (highlights)
    left_sparkle1 = Circle((-0.50, 0.35), 0.06, facecolor='white', zorder=6)
    left_sparkle2 = Circle((-0.35, 0.20), 0.03, facecolor='white', zorder=6)
    right_sparkle1 = Circle((0.40, 0.35), 0.06, facecolor='white', zorder=6)
    right_sparkle2 = Circle((0.55, 0.20), 0.03, facecolor='white', zorder=6)
    ax.add_patch(left_sparkle1)
    ax.add_patch(left_sparkle2)
    ax.add_patch(right_sparkle1)
    ax.add_patch(right_sparkle2)

    # Soft eyelashes / upper lids for cuteness
    ax.plot([-0.75, -0.45, -0.15], [0.50, 0.58, 0.48], 
            color='#333333', linewidth=2.5, solid_capstyle='round', zorder=7)
    ax.plot([0.15, 0.45, 0.75], [0.48, 0.58, 0.50], 
            color='#333333', linewidth=2.5, solid_capstyle='round', zorder=7)

    # ========== NOSE ==========
    nose = Polygon(
        [[0, -0.05], [-0.13, -0.28], [0.13, -0.28]],
        closed=True,
        facecolor='#FF69B4',
        edgecolor='#C71585',
        linewidth=1.5,
        zorder=4
    )
    ax.add_patch(nose)

    # Nose highlight
    nose_highlight = Ellipse((0.03, -0.12), 0.06, 0.04,
                             facecolor='white', alpha=0.7, zorder=5)
    ax.add_patch(nose_highlight)

    # ========== MOUTH ==========
    # Cute little cat mouth (like a soft W / inverted Y)
    mouth_left = Arc((-0.12, -0.35), 0.28, 0.22,
                     angle=0, theta1=200, theta2=340,
                     edgecolor='#333333', linewidth=2.5,
                     fill=False, zorder=4)
    mouth_right = Arc((0.12, -0.35), 0.28, 0.22,
                      angle=0, theta1=200, theta2=340,
                      edgecolor='#333333', linewidth=2.5,
                      fill=False, zorder=4)
    ax.add_patch(mouth_left)
    ax.add_patch(mouth_right)

    # Tiny smile curve under nose
    smile = Arc((0, -0.32), 0.18, 0.12,
                angle=0, theta1=200, theta2=340,
                edgecolor='#333333', linewidth=2,
                fill=False, zorder=4)
    ax.add_patch(smile)

    # ========== WHISKERS ==========
    whisker_style = dict(color='#555555', linewidth=1.8, 
                         solid_capstyle='round', alpha=0.85, zorder=3)

    # Left whiskers
    ax.plot([-0.35, -1.55], [-0.15, 0.05], **whisker_style)
    ax.plot([-0.35, -1.65], [-0.28, -0.28], **whisker_style)
    ax.plot([-0.35, -1.50], [-0.42, -0.60], **whisker_style)

    # Right whiskers
    ax.plot([0.35, 1.55], [-0.15, 0.05], **whisker_style)
    ax.plot([0.35, 1.65], [-0.28, -0.28], **whisker_style)
    ax.plot([0.35, 1.50], [-0.42, -0.60], **whisker_style)

    # ========== BLUSH ==========
    left_blush = Ellipse((-0.75, -0.05), 0.38, 0.20,
                         facecolor='#FFB6C1', alpha=0.55, zorder=2)
    right_blush = Ellipse((0.75, -0.05), 0.38, 0.20,
                          facecolor='#FFB6C1', alpha=0.55, zorder=2)
    ax.add_patch(left_blush)
    ax.add_patch(right_blush)

    # ========== OPTIONAL: little body hint ==========
    body = Ellipse((0, -1.6), 1.6, 1.0,
                   facecolor='#F4A460',
                   edgecolor='#8B4513',
                   linewidth=3,
                   zorder=0)
    ax.add_patch(body)

    # Tiny front paws
    left_paw = Ellipse((-0.45, -1.95), 0.45, 0.28,
                       facecolor='#F4A460',
                       edgecolor='#8B4513',
                       linewidth=2,
                       zorder=1)
    right_paw = Ellipse((0.45, -1.95), 0.45, 0.28,
                        facecolor='#F4A460',
                        edgecolor='#8B4513',
                        linewidth=2,
                        zorder=1)
    ax.add_patch(left_paw)
    ax.add_patch(right_paw)

    # Paw pads (cute pink beans)
    for x_offset in [-0.45, 0.45]:
        # Main pad
        pad = Ellipse((x_offset, -2.0), 0.18, 0.12,
                      facecolor='#FFB6C1', alpha=0.8, zorder=2)
        ax.add_patch(pad)
        # Toe beans
        for dx in [-0.12, 0, 0.12]:
            toe = Circle((x_offset + dx, -1.88), 0.05,
                         facecolor='#FFB6C1', alpha=0.8, zorder=2)
            ax.add_patch(toe)

    # ========== TITLE & DECOR ==========
    ax.text(0, 2.45, "Cute Kitten 🐱",
            fontsize=26, fontweight='bold',
            ha='center', va='center',
            color='#8B4513',
            fontfamily='sans-serif')

    ax.text(0, 2.15, "meow~",
            fontsize=14, style='italic',
            ha='center', va='center',
            color='#CD853F')

    # Soft decorative hearts
    def draw_heart(ax, x, y, size=0.15, color='#FF69B4', alpha=0.6):
        t = np.linspace(0, 2 * np.pi, 100)
        heart_x = size * 16 * np.sin(t)**3
        heart_y = size * (13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t))
        ax.fill(heart_x + x, heart_y / 16 + y, color=color, alpha=alpha, zorder=10)

    draw_heart(ax, -1.9, 1.8, size=0.08)
    draw_heart(ax, 1.9, 1.6, size=0.07)
    draw_heart(ax, -2.0, -0.8, size=0.06, color='#FFB6C1')
    draw_heart(ax, 2.0, -1.0, size=0.065, color='#FFB6C1')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    draw_cute_kitten()
