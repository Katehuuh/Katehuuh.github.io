import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Arc

def draw_kitten():
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#fdf6e3')  # soft cream background
    ax.set_facecolor('#fdf6e3')

    # --- Body (simple oval) ---
    body = patches.Ellipse((0, -1.2), width=2.4, height=1.6,
                           facecolor='#ffe4c4', edgecolor='#d2a679', linewidth=3)
    ax.add_patch(body)

    # --- Head ---
    head = patches.Circle((0, 0.6), radius=1.1,
                          facecolor='#fff0e6', edgecolor='#dcbfa6', linewidth=3, zorder=3)
    ax.add_patch(head)

    # --- Ears ---
    # Left ear
    ear_l = patches.Polygon([(-0.95, 1.35), (-1.3, 2.2), (-0.55, 1.5)],
                            facecolor='#fff0e6', edgecolor='#dcbfa6', linewidth=3)
    ax.add_patch(ear_l)
    # Inner left ear
    ear_l_in = patches.Polygon([(-0.92, 1.45), (-1.1, 1.9), (-0.65, 1.55)],
                               facecolor='#ffb6b6', edgecolor='#e08e8e', linewidth=2)
    ax.add_patch(ear_l_in)

    # Right ear
    ear_r = patches.Polygon([(0.95, 1.35), (1.3, 2.2), (0.55, 1.5)],
                            facecolor='#fff0e6', edgecolor='#dcbfa6', linewidth=3)
    ax.add_patch(ear_r)
    # Inner right ear
    ear_r_in = patches.Polygon([(0.92, 1.45), (1.1, 1.9), (0.65, 1.55)],
                               facecolor='#ffb6b6', edgecolor='#e08e8e', linewidth=2)
    ax.add_patch(ear_r_in)

    # --- Eyes ---
    # Left eye
    eye_l = patches.Circle((-0.45, 0.9), radius=0.22,
                          facecolor='#ffffff', edgecolor='#dcbfa6', linewidth=2, zorder=4)
    ax.add_patch(eye_l)
    # Left pupil
    pupil_l = patches.Circle((-0.45, 0.9), radius=0.08,
                            facecolor='#5a3a2a', edgecolor='none', zorder=5)
    ax.add_patch(pupil_l)
    # Highlight
    highlight_l = patches.Circle((-0.48, 0.93), radius=0.03,
                                 facecolor='#ffffff', edgecolor='none', zorder=6)
    ax.add_patch(highlight_l)

    # Right eye
    eye_r = patches.Circle((0.45, 0.9), radius=0.22,
                          facecolor='#ffffff', edgecolor='#dcbfa6', linewidth=2, zorder=4)
    ax.add_patch(eye_r)
    # Right pupil
    pupil_r = patches.Circle((0.45, 0.9), radius=0.08,
                            facecolor='#5a3a2a', edgecolor='none', zorder=5)
    ax.add_patch(pupil_r)
    # Highlight
    highlight_r = patches.Circle((0.42, 0.93), radius=0.03,
                                 facecolor='#ffffff', edgecolor='none', zorder=6)
    ax.add_patch(highlight_r)

    # --- Nose ---
    nose = patches.Polygon([(-0.08, 0.55), (0.08, 0.55), (0, 0.45)],
                           facecolor='#ffb6b6', edgecolor='#e08e8e', linewidth=2)
    ax.add_patch(nose)

    # --- Mouth ---
    # Simple "w" shape using arcs or curves
    mouth_left = Arc((-0.15, 0.35), width=0.3, height=0.25,
                     angle=0, theta1=180, theta2=360,
                     color='#e08e8e', linewidth=2)
    mouth_right = Arc((0.15, 0.35), width=0.3, height=0.25,
                      angle=0, theta1=0, theta2=180,
                      color='#e08e8e', linewidth=2)
    ax.add_patch(mouth_left)
    ax.add_patch(mouth_right)

    # --- Whiskers ---
    for y in [0.5, 0.55, 0.6]:
        # Left whiskers
        ax.plot([-0.3, -1.4], [y, y+0.05], color='#dcbfa6', linewidth=1.5)
        ax.plot([-0.35, -1.3], [y-0.03, y-0.1], color='#dcbfa6', linewidth=1.5)
        # Right whiskers
        ax.plot([0.3, 1.4], [y, y+0.05], color='#dcbfa6', linewidth=1.5)
        ax.plot([0.35, 1.3], [y-0.03, y-0.1], color='#dcbfa6', linewidth=1.5)

    # --- Paws (little circles at bottom of body) ---
    paw_l = patches.Circle((-0.6, -2.1), radius=0.18,
                          facecolor='#fff0e6', edgecolor='#dcbfa6', linewidth=2)
    paw_r = patches.Circle((0.6, -2.1), radius=0.18,
                          facecolor='#fff0e6', edgecolor='#dcbfa6', linewidth=2)
    ax.add_patch(paw_l)
    ax.add_patch(paw_r)

    # --- Tail (curved) ---
    tail = Arc((-1.3, -0.8), width=1.2, height=1.6,
               angle=-30, theta1=-60, theta2=20,
               color='#ffe4c4', linewidth=12, capstyle='round')
    ax.add_patch(tail)

    # Title
    plt.title("🐱 Cute Kitten 🐱", fontsize=16, color='#5a3a2a', pad=10)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    draw_kitten()