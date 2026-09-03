import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, Arc

def draw_kitten():
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FFF8F0')
    ax.set_facecolor('#FFF8F0')

    # Colors
    fur = '#FFCC99'       # light orange fur
    fur_dark = '#EAA266'  # stripes
    belly = '#FFF5E6'     # cream belly
    pink = '#FF9999'      # inner ear / nose / blush
    outline = '#6B4A35'   # warm brown outline
    bow_color = '#FF6B81'

    # --- Tail (draw first so it's behind body) ---
    # thick outline + thinner fur color for cartoon look
    ax.add_patch(Arc((7.2, 3.8), 3.2, 3.5, theta1=300, theta2=90,
                     color=outline, linewidth=16, capstyle='round', zorder=1))
    ax.add_patch(Arc((7.2, 3.8), 3.2, 3.5, theta1=300, theta2=90,
                     color=fur, linewidth=11, capstyle='round', zorder=1))
    # tail tip
    ax.add_patch(Circle((7.25, 5.5), 0.35, color=fur, ec=outline, lw=2, zorder=1))

    # --- Body ---
    ax.add_patch(Ellipse((5, 2.7), 4.6, 3.2, color=fur, ec=outline, lw=2.5, zorder=2))
    ax.add_patch(Ellipse((5, 2.5), 2.5, 1.9, color=belly, ec=outline, lw=2, zorder=3))

    # body stripes
    for x in [3.8, 6.2]:
        ax.add_patch(Ellipse((x, 3.5), 0.3, 0.7, color=fur_dark, zorder=3))

    # --- Front paws ---
    ax.add_patch(Ellipse((4.1, 1.6), 1.2, 0.8, color=fur, ec=outline, lw=2, zorder=4))
    ax.add_patch(Ellipse((5.9, 1.6), 1.2, 0.8, color=fur, ec=outline, lw=2, zorder=4))
    # toe lines
    ax.plot([4.1, 4.1], [1.2, 1.7], color=outline, lw=1.5, zorder=5)
    ax.plot([5.9, 5.9], [1.2, 1.7], color=outline, lw=1.5, zorder=5)

    # --- Ears ---
    left_ear = [[3.4, 7.0], [2.7, 9.4], [5.0, 8.0]]
    right_ear = [[6.6, 7.0], [7.3, 9.4], [5.0, 8.0]]
    ax.add_patch(Polygon(left_ear, closed=True, color=fur, ec=outline, lw=2.5, zorder=3))
    ax.add_patch(Polygon(right_ear, closed=True, color=fur, ec=outline, lw=2.5, zorder=3))

    # inner ears
    left_inner = [[3.6, 7.5], [3.2, 8.8], [4.6, 8.0]]
    right_inner = [[6.4, 7.5], [6.8, 8.8], [5.4, 8.0]]
    ax.add_patch(Polygon(left_inner, closed=True, color=pink, ec=outline, lw=1.5, zorder=4))
    ax.add_patch(Polygon(right_inner, closed=True, color=pink, ec=outline, lw=1.5, zorder=4))

    # --- Head ---
    ax.add_patch(Circle((5, 6), 2.0, color=fur, ec=outline, lw=2.5, zorder=4))

    # forehead stripes
    ax.add_patch(Ellipse((4.5, 7.6), 0.25, 0.6, color=fur_dark, zorder=5))
    ax.add_patch(Ellipse((5.0, 7.8), 0.25, 0.7, color=fur_dark, zorder=5))
    ax.add_patch(Ellipse((5.5, 7.6), 0.25, 0.6, color=fur_dark, zorder=5))

    # --- Eyes (big and kawaii) ---
    for cx in [4.1, 5.9]:
        ax.add_patch(Circle((cx, 6.1), 0.55, color='white', ec=outline, lw=2, zorder=5))
        ax.add_patch(Circle((cx, 6.1), 0.32, color='#3A3A3A', zorder=6))
        ax.add_patch(Circle((cx-0.1, 6.2), 0.12, color='white', zorder=7))
        ax.add_patch(Circle((cx+0.1, 6.0), 0.06, color='white', zorder=7))

    # --- Blush ---
    ax.add_patch(Ellipse((3.6, 5.4), 0.6, 0.4, color=pink, alpha=0.6, zorder=5))
    ax.add_patch(Ellipse((6.4, 5.4), 0.6, 0.4, color=pink, alpha=0.6, zorder=5))

    # --- Nose + Mouth ---
    ax.add_patch(Polygon([[4.8, 5.6], [5.2, 5.6], [5.0, 5.3]],
                         closed=True, color=pink, ec=outline, lw=1.2, zorder=6))
    ax.add_patch(Arc((4.75, 5.25), 0.5, 0.4, theta1=180, theta2=360,
                     color=outline, lw=2, zorder=6))
    ax.add_patch(Arc((5.25, 5.25), 0.5, 0.4, theta1=180, theta2=360,
                     color=outline, lw=2, zorder=6))

    # --- Whiskers ---
    for y1, y2 in [(5.6, 5.8), (5.3, 5.3), (5.0, 4.8)]:
        ax.plot([3.5, 2.0], [y1, y2], color=outline, lw=1.5, zorder=5)
        ax.plot([6.5, 8.0], [y1, y2], color=outline, lw=1.5, zorder=5)

    # --- Little bow on right ear ---
    bow_left = [[6.6, 8.3], [6.0, 8.0], [6.0, 8.7]]
    bow_right = [[6.6, 8.3], [7.2, 8.0], [7.2, 8.7]]
    ax.add_patch(Polygon(bow_left, closed=True, color=bow_color, ec=outline, lw=1.5, zorder=6))
    ax.add_patch(Polygon(bow_right, closed=True, color=bow_color, ec=outline, lw=1.5, zorder=6))
    ax.add_patch(Circle((6.6, 8.3), 0.18, color=bow_color, ec=outline, lw=1.5, zorder=7))

    ax.text(5, 0.4, 'Meow!', ha='center', va='center', fontsize=16,
            color=outline, fontfamily='sans-serif', fontweight='bold')

    plt.tight_layout()
    plt.savefig('cute_kitten.png', dpi=150)
    plt.show()

if __name__ == '__main__':
    draw_kitten()
