import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_cute_kitten():
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    ax.axis('off')

    # Colors
    fur = '#FFBB70'
    fur_dark = '#E69E4D'
    white = '#FFFDF7'
    pink = '#FF90A9'
    pink_light = '#FFC2D1'
    black = '#2B2B2B'

    # --- Body ---
    ax.add_patch(patches.Ellipse((0, -1.3), 1.8, 1.4, color=fur, zorder=1))
    # Belly white
    ax.add_patch(patches.Ellipse((0, -1.5), 1.0, 0.8, color=white, zorder=2))
    # Tail
    ax.add_patch(patches.Ellipse((1.1, -1.2), 0.9, 0.45, angle=35, color=fur, zorder=0))
    ax.add_patch(patches.Ellipse((1.3, -1.1), 0.5, 0.3, angle=35, color=fur_dark, zorder=0, alpha=0.4))
    
    # Little paws
    ax.add_patch(patches.Ellipse((-0.4, -1.95), 0.4, 0.25, color=white, zorder=3))
    ax.add_patch(patches.Ellipse((0.4, -1.95), 0.4, 0.25, color=white, zorder=3))

    # --- Ears ---
    # Left outer ear
    left_ear_outer = patches.Polygon([[-0.95, 0.4], [-0.7, 1.5], [0.0, 0.7]], closed=True, color=fur, ec=fur_dark, lw=2, zorder=3)
    # Right outer ear
    right_ear_outer = patches.Polygon([[0.95, 0.4], [0.7, 1.5], [0.0, 0.7]], closed=True, color=fur, ec=fur_dark, lw=2, zorder=3)
    ax.add_patch(left_ear_outer)
    ax.add_patch(right_ear_outer)

    # Inner ears
    ax.add_patch(patches.Polygon([[-0.75, 0.6], [-0.6, 1.15], [-0.15, 0.65]], closed=True, color=pink_light, zorder=4))
    ax.add_patch(patches.Polygon([[0.75, 0.6], [0.6, 1.15], [0.15, 0.65]], closed=True, color=pink_light, zorder=4))

    # --- Head ---
    ax.add_patch(patches.Circle((0, 0.1), 1.05, color=fur, ec=fur_dark, lw=2, zorder=5))
    
    # Muzzle
    ax.add_patch(patches.Ellipse((0, -0.35), 1.1, 0.7, color=white, zorder=6))

    # --- Eyes ---
    # Big cute eyes
    ax.add_patch(patches.Circle((-0.35, 0.15), 0.22, color=black, zorder=7))
    ax.add_patch(patches.Circle((0.35, 0.15), 0.22, color=black, zorder=7))

    # Eye highlights - makes it super cute
    ax.add_patch(patches.Circle((-0.28, 0.25), 0.08, color='white', zorder=8))
    ax.add_patch(patches.Circle((0.42, 0.25), 0.08, color='white', zorder=8))
    ax.add_patch(patches.Circle((-0.32, 0.18), 0.03, color='white', zorder=8))
    ax.add_patch(patches.Circle((0.38, 0.18), 0.03, color='white', zorder=8))

    # Blush
    ax.add_patch(patches.Ellipse((-0.65, -0.2), 0.25, 0.12, color=pink, alpha=0.5, zorder=7))
    ax.add_patch(patches.Ellipse((0.65, -0.2), 0.25, 0.12, color=pink, alpha=0.5, zorder=7))

    # --- Nose ---
    nose = patches.Polygon([[0, -0.15], [-0.07, -0.28], [0.07, -0.28]], closed=True, color=pink, ec=black, lw=1, zorder=8)
    ax.add_patch(nose)

    # Mouth - little 'w'
    ax.plot([-0.07, 0, 0.07], [-0.28, -0.38, -0.28], color=black, lw=1.5, zorder=8)

    # Whiskers
    for y in [-0.25, -0.35, -0.45]:
        ax.plot([-0.55, -0.95], [y, y-0.05], color=black, lw=1, alpha=0.6, zorder=6)
        ax.plot([0.55, 0.95], [y, y-0.05], color=black, lw=1, alpha=0.6, zorder=6)

    # Forehead stripes
    ax.add_patch(patches.Ellipse((0, 0.6), 0.15, 0.35, color=fur_dark, alpha=0.6, zorder=6))
    ax.add_patch(patches.Ellipse((-0.2, 0.55), 0.08, 0.22, color=fur_dark, alpha=0.5, zorder=6))
    ax.add_patch(patches.Ellipse((0.2, 0.55), 0.08, 0.22, color=fur_dark, alpha=0.5, zorder=6))

    ax.set_xlim(-2, 2)
    ax.set_ylim(-2.5, 2)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    draw_cute_kitten()