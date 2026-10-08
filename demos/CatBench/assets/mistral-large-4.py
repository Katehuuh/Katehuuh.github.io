import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_cute_kitten():
    # Create figure with warm background
    fig, ax = plt.subplots(figsize=(8, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FFF5EE')  # Seashell cream background

    # Color palette
    fur = '#FFD8A8'           # Peach/cream fur
    fur_dark = '#E6B87A'      # Tabby stripes
    inner_ear = '#FFB6C1'     # Light pink inner ears
    eye_white = '#FFFFFF'
    iris = '#87CEEB'          # Sky blue eyes
    pupil = '#2C3E50'         # Dark pupil
    nose = '#FF9999'          # Pink nose
    blush = '#FFB6C1'         # Rosy cheeks
    outline = '#8B4513'       # Warm brown outlines
    whisker = '#D3D3D3'       # Light grey whiskers

    # Draw tail (behind body) - using sine wave for curve
    tail_x = np.linspace(7.2, 9.5, 100)
    tail_y = 2.5 + 1.2 * np.sin((tail_x - 7.2) * 2)
    ax.plot(tail_x, tail_y, color=outline, linewidth=10, solid_capstyle='round', zorder=0)
    ax.plot(tail_x, tail_y, color=fur, linewidth=7, solid_capstyle='round', zorder=0)

    # Draw body
    body = patches.Ellipse((5, 3), 4.5, 5, facecolor=fur,
                          edgecolor=outline, linewidth=2.5, zorder=1)
    ax.add_patch(body)

    # Draw front paws
    left_paw = patches.Ellipse((3.5, 1), 1.3, 1.1, facecolor=fur,
                              edgecolor=outline, linewidth=2, zorder=2)
    right_paw = patches.Ellipse((6.5, 1), 1.3, 1.1, facecolor=fur,
                               edgecolor=outline, linewidth=2, zorder=2)
    ax.add_patch(left_paw)
    ax.add_patch(right_paw)

    # Paw toe details
    for x in [3.2, 3.8, 6.2, 6.8]:
        ax.plot([x, x], [0.4, 1.2], color=outline, linewidth=1, zorder=3)

    # Draw ears (triangles behind head)
    left_ear = patches.Polygon([[2.8, 8.5], [1.5, 11], [4.5, 9.5]], closed=True,
                              facecolor=fur, edgecolor=outline, linewidth=2.5, zorder=3)
    right_ear = patches.Polygon([[7.2, 8.5], [8.5, 11], [5.5, 9.5]], closed=True,
                               facecolor=fur, edgecolor=outline, linewidth=2.5, zorder=3)
    ax.add_patch(left_ear)
    ax.add_patch(right_ear)

    # Inner ears (pink)
    left_inner = patches.Polygon([[3.0, 8.8], [2.2, 10.3], [4.2, 9.5]], closed=True,
                                facecolor=inner_ear, edgecolor='none', zorder=3)
    right_inner = patches.Polygon([[7.0, 8.8], [7.8, 10.3], [5.8, 9.5]], closed=True,
                                 facecolor=inner_ear, edgecolor='none', zorder=3)
    ax.add_patch(left_inner)
    ax.add_patch(right_inner)

    # Draw head (main circle)
    head = patches.Circle((5, 7), 2.8, facecolor=fur,
                         edgecolor=outline, linewidth=2.5, zorder=4)
    ax.add_patch(head)

    # Forehead stripes (tabby markings)
    for x_offset in [-0.6, 0, 0.6]:
        ax.plot([5 + x_offset, 5 + x_offset], [9.0, 9.6],
               color=fur_dark, linewidth=4, zorder=4)

    # Draw eyes (big and sparkly!)
    eye_y = 7.2
    eye_spacing = 1.3

    # Left eye components
    left_white = patches.Circle((5 - eye_spacing, eye_y), 0.65,
                               facecolor=eye_white, edgecolor=outline,
                               linewidth=1.5, zorder=5)
    left_iris = patches.Circle((5 - eye_spacing, eye_y), 0.4,
                              facecolor=iris, zorder=6)
    left_pupil = patches.Circle((5 - eye_spacing, eye_y), 0.2,
                               facecolor=pupil, zorder=7)
    left_shine = patches.Circle((5 - eye_spacing - 0.15, eye_y + 0.15), 0.12,
                               facecolor='white', zorder=8)
    left_shine_small = patches.Circle((5 - eye_spacing + 0.15, eye_y - 0.1), 0.06,
                                     facecolor='white', zorder=8)

    # Right eye components
    right_white = patches.Circle((5 + eye_spacing, eye_y), 0.65,
                                facecolor=eye_white, edgecolor=outline,
                                linewidth=1.5, zorder=5)
    right_iris = patches.Circle((5 + eye_spacing, eye_y), 0.4,
                               facecolor=iris, zorder=6)
    right_pupil = patches.Circle((5 + eye_spacing, eye_y), 0.2,
                                facecolor=pupil, zorder=7)
    right_shine = patches.Circle((5 + eye_spacing - 0.15, eye_y + 0.15), 0.12,
                                facecolor='white', zorder=8)
    right_shine_small = patches.Circle((5 + eye_spacing + 0.15, eye_y - 0.1), 0.06,
                                      facecolor='white', zorder=8)

    # Add all eye parts
    for eye_part in [left_white, left_iris, left_pupil, left_shine, left_shine_small,
                     right_white, right_iris, right_pupil, right_shine, right_shine_small]:
        ax.add_patch(eye_part)

    # Draw nose (little triangle)
    nose = patches.Polygon([[4.7, 6.2], [5.3, 6.2], [5, 5.7]], closed=True,
                          facecolor=nose, edgecolor=outline, linewidth=1.5, zorder=5)
    ax.add_patch(nose)

    # Draw mouth (w-shaped curve)
    # Left side of mouth
    mouth_x_left = np.linspace(5, 4.4, 20)
    mouth_y_left = 5.7 - 0.4 * (5 - mouth_x_left)**2
    ax.plot(mouth_x_left, mouth_y_left, color=outline, linewidth=1.5, zorder=5)

    # Right side of mouth
    mouth_x_right = np.linspace(5, 5.6, 20)
    mouth_y_right = 5.7 - 0.4 * (mouth_x_right - 5)**2
    ax.plot(mouth_x_right, mouth_y_right, color=outline, linewidth=1.5, zorder=5)

    # Draw whiskers
    whisker_positions = [(0.4, 2.0), (0.2, 2.2), (0, 2.2), (-0.2, 2.0), (-0.4, 1.8)]

    for y_off, length in whisker_positions:
        y = 6.5 + y_off
        # Left whiskers
        ax.plot([2.2, 2.2 - length], [y, y + 0.3],
               color=whisker, linewidth=1.2, zorder=5)
        # Right whiskers
        ax.plot([7.8, 7.8 + length], [y, y + 0.3],
               color=whisker, linewidth=1.2, zorder=5)

    # Draw blush cheeks
    left_blush = patches.Ellipse((3.4, 5.8), 1.0, 0.6,
                                facecolor=blush, alpha=0.6, zorder=4)
    right_blush = patches.Ellipse((6.6, 5.8), 1.0, 0.6,
                                 facecolor=blush, alpha=0.6, zorder=4)
    ax.add_patch(left_blush)
    ax.add_patch(right_blush)

    # Add title
    plt.title('🐱 My Cute Kitten 🐱', fontsize=24, fontweight='bold',
              pad=20, color='#8B4513')

    plt.tight_layout()

    # Save and show
    plt.savefig('cute_kitten.png', dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    print("Kitten saved as 'cute_kitten.png'!")
    plt.show()

if __name__ == "__main__":
    draw_cute_kitten()
