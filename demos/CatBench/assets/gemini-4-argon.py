import matplotlib.patches as patches
from matplotlib.path import Path
import matplotlib.pyplot as plt
import numpy as np


def draw_kitten():
    # Setup the figure and axis
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_aspect("equal")
    ax.axis("off")  # Hide the axes

    # Background color
    fig.patch.set_facecolor("#FDF6F0")  # Soft cream background

    # Colors
    fur_color = "#D3D3D3"  # Light gray
    dark_fur = "#A9A9A9"  # Darker gray for stripes
    outline_color = "#4A4A4A"  # Dark charcoal for outlines
    pink_color = "#FFB6C1"  # Light pink for ears/nose/blush
    collar_color = "#FF6B6B"  # Red/Coral for collar
    bell_color = "#FFD700"  # Gold for the bell

    # --- 1. TAIL (zorder=1, furthest back) ---
    # Using a Bezier curve for a smooth, curvy tail
    tail_verts = [(1.0, -2.8), (3.0, -3.0), (3.5, -0.5), (2.2, -0.8)]
    tail_codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    tail_path = Path(tail_verts, tail_codes)
    tail = patches.PathPatch(
        tail_path,
        facecolor="none",
        edgecolor=fur_color,
        lw=18,
        capstyle="round",
        zorder=1,
    )
    tail_outline = patches.PathPatch(
        tail_path,
        facecolor="none",
        edgecolor=outline_color,
        lw=22,
        capstyle="round",
        zorder=0.9,
    )
    ax.add_patch(tail)
    ax.add_patch(tail_outline)

    # --- 2. BODY (zorder=2) ---
    body = patches.Ellipse(
        (0, -1.8),
        width=2.6,
        height=2.8,
        facecolor=fur_color,
        edgecolor=outline_color,
        lw=3,
        zorder=2,
    )
    ax.add_patch(body)

    # --- 3. EARS (zorder=3, behind the head) ---
    # Left Ear
    left_ear = patches.Polygon(
        [[-1.8, 0.8], [-1.9, 2.7], [-0.4, 1.8]],
        closed=True,
        facecolor=fur_color,
        edgecolor=outline_color,
        lw=3,
        zorder=3,
        joinstyle="round",
    )
    left_inner_ear = patches.Polygon(
        [[-1.6, 1.0], [-1.7, 2.3], [-0.7, 1.6]],
        closed=True,
        facecolor=pink_color,
        edgecolor="none",
        zorder=3.1,
    )
    # Right Ear
    right_ear = patches.Polygon(
        [[1.8, 0.8], [1.9, 2.7], [0.4, 1.8]],
        closed=True,
        facecolor=fur_color,
        edgecolor=outline_color,
        lw=3,
        zorder=3,
        joinstyle="round",
    )
    right_inner_ear = patches.Polygon(
        [[1.6, 1.0], [1.7, 2.3], [0.7, 1.6]],
        closed=True,
        facecolor=pink_color,
        edgecolor="none",
        zorder=3.1,
    )
    ax.add_patch(left_ear)
    ax.add_patch(left_inner_ear)
    ax.add_patch(right_ear)
    ax.add_patch(right_inner_ear)

    # --- 4. HEAD (zorder=4) ---
    head = patches.Ellipse(
        (0, 0.6),
        width=3.8,
        height=3.0,
        facecolor=fur_color,
        edgecolor=outline_color,
        lw=3,
        zorder=4,
    )
    ax.add_patch(head)

    # Forehead Stripes
    stripe1 = patches.Ellipse(
        (0, 1.7), width=0.2, height=0.6, facecolor=dark_fur, zorder=4.1
    )
    stripe2 = patches.Ellipse(
        (-0.4, 1.6),
        width=0.15,
        height=0.4,
        angle=15,
        facecolor=dark_fur,
        zorder=4.1,
    )
    stripe3 = patches.Ellipse(
        (0.4, 1.6),
        width=0.15,
        height=0.4,
        angle=-15,
        facecolor=dark_fur,
        zorder=4.1,
    )
    ax.add_patch(stripe1)
    ax.add_patch(stripe2)
    ax.add_patch(stripe3)

    # --- 5. PAWS (zorder=5) ---
    left_paw = patches.Ellipse(
        (-0.7, -3.1),
        width=0.9,
        height=0.6,
        facecolor=fur_color,
        edgecolor=outline_color,
        lw=3,
        zorder=5,
    )
    right_paw = patches.Ellipse(
        (0.7, -3.1),
        width=0.9,
        height=0.6,
        facecolor=fur_color,
        edgecolor=outline_color,
        lw=3,
        zorder=5,
    )
    ax.add_patch(left_paw)
    ax.add_patch(right_paw)

    # --- 6. COLLAR & BELL (zorder=5) ---
    collar = patches.Arc(
        (0, -0.5),
        width=2.2,
        height=0.8,
        theta1=190,
        theta2=350,
        edgecolor=collar_color,
        lw=8,
        capstyle="round",
        zorder=4.5,
    )
    bell = patches.Circle(
        (0, -1.0),
        radius=0.25,
        facecolor=bell_color,
        edgecolor=outline_color,
        lw=2,
        zorder=5,
    )
    bell_detail = patches.Circle(
        (0, -1.05), radius=0.05, facecolor=outline_color, zorder=5.1
    )
    ax.add_patch(collar)
    ax.add_patch(bell)
    ax.add_patch(bell_detail)

    # --- 7. FACE DETAILS (zorder=6) ---
    # Eyes
    left_eye = patches.Circle(
        (-0.9, 0.6), radius=0.35, facecolor=outline_color, zorder=6
    )
    right_eye = patches.Circle(
        (0.9, 0.6), radius=0.35, facecolor=outline_color, zorder=6
    )
    # Eye Shines (makes it cute!)
    left_shine1 = patches.Circle(
        (-1.0, 0.72), radius=0.12, facecolor="white", zorder=6.1
    )
    left_shine2 = patches.Circle(
        (-0.8, 0.5), radius=0.05, facecolor="white", zorder=6.1
    )
    right_shine1 = patches.Circle(
        (0.8, 0.72), radius=0.12, facecolor="white", zorder=6.1
    )
    right_shine2 = patches.Circle(
        (1.0, 0.5), radius=0.05, facecolor="white", zorder=6.1
    )
    ax.add_patch(left_eye)
    ax.add_patch(right_eye)
    ax.add_patch(left_shine1)
    ax.add_patch(left_shine2)
    ax.add_patch(right_shine1)
    ax.add_patch(right_shine2)

    # Blush
    left_blush = patches.Ellipse(
        (-1.2, 0.15),
        width=0.5,
        height=0.25,
        facecolor=pink_color,
        alpha=0.6,
        zorder=6,
    )
    right_blush = patches.Ellipse(
        (1.2, 0.15),
        width=0.5,
        height=0.25,
        facecolor=pink_color,
        alpha=0.6,
        zorder=6,
    )
    ax.add_patch(left_blush)
    ax.add_patch(right_blush)

    # Nose
    nose = patches.Polygon(
        [[-0.15, 0.3], [0.15, 0.3], [0, 0.1]],
        closed=True,
        facecolor=pink_color,
        edgecolor=outline_color,
        lw=2,
        joinstyle="round",
        zorder=6,
    )
    ax.add_patch(nose)

    # Mouth (Two arcs forming a 'w')
    mouth_left = patches.Arc(
        (-0.15, 0.0),
        width=0.3,
        height=0.3,
        theta1=180,
        theta2=360,
        edgecolor=outline_color,
        lw=2.5,
        capstyle="round",
        zorder=6,
    )
    mouth_right = patches.Arc(
        (0.15, 0.0),
        width=0.3,
        height=0.3,
        theta1=180,
        theta2=360,
        edgecolor=outline_color,
        lw=2.5,
        capstyle="round",
        zorder=6,
    )
    ax.add_patch(mouth_left)
    ax.add_patch(mouth_right)

    # Whiskers
    # Left whiskers
    ax.plot(
        [-1.6, -2.3],
        [0.4, 0.5],
        color=outline_color,
        lw=2.5,
        solid_capstyle="round",
        zorder=6,
    )
    ax.plot(
        [-1.6, -2.4],
        [0.2, 0.2],
        color=outline_color,
        lw=2.5,
        solid_capstyle="round",
        zorder=6,
    )
    ax.plot(
        [-1.6, -2.3],
        [0.0, -0.1],
        color=outline_color,
        lw=2.5,
        solid_capstyle="round",
        zorder=6,
    )
    # Right whiskers
    ax.plot(
        [1.6, 2.3],
        [0.4, 0.5],
        color=outline_color,
        lw=2.5,
        solid_capstyle="round",
        zorder=6,
    )
    ax.plot(
        [1.6, 2.4],
        [0.2, 0.2],
        color=outline_color,
        lw=2.5,
        solid_capstyle="round",
        zorder=6,
    )
    ax.plot(
        [1.6, 2.3],
        [0.0, -0.1],
        color=outline_color,
        lw=2.5,
        solid_capstyle="round",
        zorder=6,
    )

    # Title
    plt.title(
        "Meow!",
        fontsize=24,
        fontweight="bold",
        color=outline_color,
        fontname="Comic Sans MS",
        y=0.92,
    )

    # Display the plot
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    draw_kitten()
