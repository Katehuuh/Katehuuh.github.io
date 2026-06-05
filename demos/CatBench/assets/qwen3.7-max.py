import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.path import Path

def draw_kitten():
    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.axis('off') # Hide the axes
    fig.patch.set_facecolor('#E8F4F8') # Soft pastel blue background

    # --- Color Palette ---
    fur_color = '#FFCBA4'      # Soft peach/orange
    dark_fur = '#E59866'       # Darker orange for stripes
    pink = '#FFB6C1'           # Light pink for nose, ears, blush
    eye_color = '#4DB8FF'      # Bright cute blue
    collar_color = '#FF6B6B'   # Pastel red collar
    bell_color = '#FFD700'     # Gold bell
    dark_gray = '#333333'      # For outlines, whiskers, pupils

    # Helper function to add patches easily
    def add_patch(patch, zorder=2):
        ax.add_patch(patch)

    # ================= TAIL =================
    # Drawn first so it sits behind the body
    tail_verts = [(0.35, -0.3), (0.8, -0.5), (0.9, 0.1), (0.6, 0.3)]
    tail_codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    tail_path = Path(tail_verts, tail_codes)
    tail = patches.PathPatch(tail_path, facecolor='none', edgecolor=fur_color, lw=25, capstyle='round', zorder=1)
    add_patch(tail)

    # ================= BODY & PAWS =================
    # Main Body
    body = patches.Ellipse((0, -0.3), 0.7, 0.65, color=fur_color, zorder=2)
    add_patch(body)

    # Paws
    left_paw = patches.Ellipse((-0.22, -0.6), 0.2, 0.15, color=fur_color, zorder=3)
    right_paw = patches.Ellipse((0.22, -0.6), 0.2, 0.15, color=fur_color, zorder=3)
    add_patch(left_paw)
    add_patch(right_paw)

    # Toe beans (Left Paw)
    add_patch(patches.Ellipse((-0.22, -0.6), 0.06, 0.04, color=pink, zorder=4))
    add_patch(patches.Circle((-0.27, -0.56), 0.025, color=pink, zorder=4))
    add_patch(patches.Circle((-0.22, -0.54), 0.025, color=pink, zorder=4))
    add_patch(patches.Circle((-0.17, -0.56), 0.025, color=pink, zorder=4))
    
    # Toe beans (Right Paw)
    add_patch(patches.Ellipse((0.22, -0.6), 0.06, 0.04, color=pink, zorder=4))
    add_patch(patches.Circle((0.17, -0.56), 0.025, color=pink, zorder=4))
    add_patch(patches.Circle((0.22, -0.54), 0.025, color=pink, zorder=4))
    add_patch(patches.Circle((0.27, -0.56), 0.025, color=pink, zorder=4))

    # ================= EARS =================
    # Left Ear & Inner Ear
    left_ear = patches.Polygon([[-0.25, 0.4], [-0.35, 0.8], [-0.05, 0.5]], color=fur_color, zorder=4)
    left_inner = patches.Polygon([[-0.24, 0.45], [-0.31, 0.72], [-0.1, 0.5]], color=pink, zorder=5)
    add_patch(left_ear)
    add_patch(left_inner)

    # Right Ear & Inner Ear
    right_ear = patches.Polygon([[0.25, 0.4], [0.35, 0.8], [0.05, 0.5]], color=fur_color, zorder=4)
    right_inner = patches.Polygon([[0.24, 0.45], [0.31, 0.72], [0.1, 0.5]], color=pink, zorder=5)
    add_patch(right_ear)
    add_patch(right_inner)

    # ================= HEAD =================
    head = patches.Ellipse((0, 0.2), 0.65, 0.55, color=fur_color, zorder=6)
    add_patch(head)

    # Forehead Stripes
    stripes = [
        ([-0.05, 0], [0.45, 0.35]), ([0.05, 0], [0.45, 0.35]), ([0, 0], [0.47, 0.32])
    ]
    for sx, sy in stripes:
        ax.plot(sx, sy, color=dark_fur, lw=4, solid_capstyle='round', zorder=7)

    # ================= COLLAR & BELL =================
    collar = patches.Arc((0, -0.05), 0.5, 0.2, angle=0, theta1=180, theta2=360, color=collar_color, lw=8, zorder=8)
    add_patch(collar)
    bell = patches.Circle((0, -0.15), 0.06, color=bell_color, zorder=9)
    add_patch(bell)
    ax.plot([0, 0], [-0.15, -0.21], color=dark_gray, lw=1.5, zorder=10)
    add_patch(patches.Circle((0, -0.21), 0.015, color=dark_gray, zorder=10))

    # ================= FACE =================
    # Blush
    add_patch(patches.Ellipse((-0.22, 0.1), 0.08, 0.04, color=pink, alpha=0.6, zorder=8))
    add_patch(patches.Ellipse((0.22, 0.1), 0.08, 0.04, color=pink, alpha=0.6, zorder=8))

    # Left Eye
    add_patch(patches.Ellipse((-0.15, 0.22), 0.14, 0.16, color='white', zorder=8))
    add_patch(patches.Circle((-0.15, 0.22), 0.06, color=eye_color, zorder=9))
    add_patch(patches.Circle((-0.15, 0.22), 0.035, color=dark_gray, zorder=10))
    # Eye Highlights
    add_patch(patches.Circle((-0.17, 0.24), 0.015, color='white', zorder=11))
    add_patch(patches.Circle((-0.13, 0.20), 0.008, color='white', zorder=11))

    # Right Eye
    add_patch(patches.Ellipse((0.15, 0.22), 0.14, 0.16, color='white', zorder=8))
    add_patch(patches.Circle((0.15, 0.22), 0.06, color=eye_color, zorder=9))
    add_patch(patches.Circle((0.15, 0.22), 0.035, color=dark_gray, zorder=10))
    # Eye Highlights
    add_patch(patches.Circle((0.13, 0.24), 0.015, color='white', zorder=11))
    add_patch(patches.Circle((0.17, 0.20), 0.008, color='white', zorder=11))

    # Nose
    nose = patches.Polygon([[-0.03, 0.08], [0.03, 0.08], [0, 0.04]], color=pink, zorder=8)
    add_patch(nose)

    # Mouth (A cute 'w' shape using two arcs)
    left_mouth = patches.Arc((-0.03, 0.05), 0.06, 0.04, angle=0, theta1=0, theta2=180, color=dark_gray, lw=2, zorder=8)
    right_mouth = patches.Arc((0.03, 0.05), 0.06, 0.04, angle=0, theta1=0, theta2=180, color=dark_gray, lw=2, zorder=8)
    add_patch(left_mouth)
    add_patch(right_mouth)
    # Line connecting nose to mouth
    ax.plot([0, 0], [0.04, 0.05], color=dark_gray, lw=2, zorder=8)

    # Whiskers (Left)
    ax.plot([-0.2, -0.45], [0.1, 0.15], color=dark_gray, lw=1.5, zorder=8)
    ax.plot([-0.2, -0.45], [0.05, 0.05], color=dark_gray, lw=1.5, zorder=8)
    ax.plot([-0.2, -0.45], [0.0, -0.05], color=dark_gray, lw=1.5, zorder=8)

    # Whiskers (Right)
    ax.plot([0.2, 0.45], [0.1, 0.15], color=dark_gray, lw=1.5, zorder=8)
    ax.plot([0.2, 0.45], [0.05, 0.05], color=dark_gray, lw=1.5, zorder=8)
    ax.plot([0.2, 0.45], [0.0, -0.05], color=dark_gray, lw=1.5, zorder=8)

    # Title and Display
    plt.title("A Cute Matplotlib Kitten", fontsize=20, color='#555555', pad=20, fontfamily='sans-serif')
    plt.show()

if __name__ == "__main__":
    draw_kitten()
