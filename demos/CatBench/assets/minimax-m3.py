import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Ellipse, Polygon, FancyBboxPatch
import numpy as np

def draw_cute_kitten():
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FFF5E1')  # Warm cream background

    # ===== Color Palette =====
    fur_color   = '#F4C2A1'   # Soft peach fur
    inner_ear   = '#FFB6C1'   # Pink inner ear
    nose_color  = '#FF6F91'   # Pink nose
    eye_color   = '#2C3E50'   # Dark eyes
    cheek_color = '#FFB6C1'   # Blush cheeks
    mouth_color = '#E57373'   # Mouth outline

    # ===== Head =====
    head = Circle((0, 0), 1.2, color=fur_color, ec='#8B4513', lw=2, zorder=1)
    ax.add_patch(head)

    # ===== Ears (triangular) =====
    # Left ear
    left_ear = Polygon([(-1.0, 0.9), (-0.4, 1.5), (-0.5, 0.6)],
                       color=fur_color, ec='#8B4513', lw=2, zorder=1)
    ax.add_patch(left_ear)
    left_inner_ear = Polygon([(-0.85, 0.95), (-0.5, 1.35), (-0.55, 0.8)],
                             color=inner_ear, zorder=2)
    ax.add_patch(left_inner_ear)

    # Right ear
    right_ear = Polygon([(1.0, 0.9), (0.4, 1.5), (0.5, 0.6)],
                        color=fur_color, ec='#8B4513', lw=2, zorder=1)
    ax.add_patch(right_ear)
    right_inner_ear = Polygon([(0.85, 0.95), (0.5, 1.35), (0.55, 0.8)],
                              color=inner_ear, zorder=2)
    ax.add_patch(right_inner_ear)

    # ===== Eyes =====
    for x in [-0.4, 0.4]:
        # White of the eye
        eye_white = Ellipse((x, 0.25), 0.35, 0.45,
                            color='white', ec=eye_color, lw=2, zorder=3)
        ax.add_patch(eye_white)
        # Pupil
        pupil = Ellipse((x, 0.2), 0.18, 0.28, color=eye_color, zorder=4)
        ax.add_patch(pupil)
        # Eye shine (big sparkle)
        sparkle1 = Circle((x - 0.05, 0.32), 0.06, color='white', zorder=5)
        ax.add_patch(sparkle1)
        # Small sparkle
        sparkle2 = Circle((x + 0.05, 0.15), 0.025, color='white', zorder=5)
        ax.add_patch(sparkle2)

    # ===== Cheeks (blush) =====
    for x in [-0.7, 0.7]:
        cheek = Ellipse((x, -0.15), 0.35, 0.22,
                        color=cheek_color, alpha=0.6, zorder=3)
        ax.add_patch(cheek)

    # ===== Nose =====
    nose = Polygon([(-0.1, -0.05), (0.1, -0.05), (0, -0.18)],
                   color=nose_color, zorder=5)
    ax.add_patch(nose)

    # ===== Mouth =====
    # Vertical line from nose
    ax.plot([0, 0], [-0.18, -0.32], color=mouth_color, lw=2, zorder=5)
    # Smile curves
    smile_x = np.linspace(-0.2, 0.2, 30)
    left_smile  = np.array([[-0.2, -0.32], [0, -0.42], [0.2, -0.32]])
    ax.plot(left_smile[:, 0], left_smile[:, 1],
            color=mouth_color, lw=2, zorder=5)

    # ===== Whiskers =====
    for y_shift in [-0.1, -0.2]:
        # Left whiskers
        ax.plot([-0.15, -0.9], [y_shift - 0.15, y_shift],
                color='#5D4037', lw=1.2, zorder=4)
        ax.plot([-0.15, -0.85], [y_shift - 0.05, y_shift + 0.1],
                color='#5D4037', lw=1.2, zorder=4)
        # Right whiskers
        ax.plot([0.15, 0.9], [y_shift - 0.15, y_shift],
                color='#5D4037', lw=1.2, zorder=4)
        ax.plot([0.15, 0.85], [y_shift - 0.05, y_shift + 0.1],
                color='#5D4037', lw=1.2, zorder=4)

    # ===== Forehead stripe (tabby pattern) =====
    forehead_stripes = [
        Polygon([(-0.3, 0.7), (-0.2, 0.95), (-0.1, 0.7)], color='#D4A574'),
        Polygon([(0.0, 0.75), (0.1, 1.0), (0.2, 0.75)], color='#D4A574'),
        Polygon([(0.2, 0.7), (0.3, 0.95), (0.4, 0.7)], color='#D4A574'),
    ]
    for stripe in forehead_stripes:
        stripe.set_zorder(2)
        ax.add_patch(stripe)

    # ===== Title =====
    ax.text(0, -1.7, "Hello, I'm a Kitten! 🐾",
            ha='center', va='center', fontsize=16,
            color='#5D4037', fontweight='bold', style='italic')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    draw_cute_kitten()
