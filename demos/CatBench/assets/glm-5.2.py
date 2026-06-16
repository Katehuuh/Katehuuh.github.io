import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Ellipse, Polygon, Circle
import numpy as np

def draw_kitten():
    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off') # Hide the axes
    
    # Colors
    body_color = '#F4A460' # Sandy brown
    dark_color = '#D2691E' # Darker brown for stripes
    inner_ear_color = '#FFB6C1' # Light pink
    eye_color = '#2F4F4F' # Dark slate gray
    nose_color = '#FF7F7F' # Pink
    
    # --- TAIL ---
    # Draw tail behind the body using a thick line
    tail_x = [6.8, 7.8, 8.8, 9.2]
    tail_y = [3.5, 4.5, 4.0, 5.2]
    ax.plot(tail_x, tail_y, color=body_color, linewidth=18, solid_capstyle='round', zorder=1)
    ax.plot(tail_x, tail_y, color=dark_color, linewidth=10, solid_capstyle='round', zorder=1)

    # --- BODY ---
    body = Ellipse((5, 3.5), 4.0, 3.5, color=body_color, zorder=2)
    ax.add_patch(body)

    # --- PAWS ---
    left_paw = Ellipse((4.0, 2.0), 1.2, 0.9, color=body_color, zorder=3)
    right_paw = Ellipse((6.0, 2.0), 1.2, 0.9, color=body_color, zorder=3)
    ax.add_patch(left_paw)
    ax.add_patch(right_paw)
    
    # Toe lines on paws
    for px in [3.7, 4.0, 4.3]:
        ax.plot([px, px], [1.7, 2.1], color=dark_color, lw=1.5, zorder=4)
    for px in [5.7, 6.0, 6.3]:
        ax.plot([px, px], [1.7, 2.1], color=dark_color, lw=1.5, zorder=4)

    # --- HEAD ---
    head = Ellipse((5, 6.5), 5.5, 4.8, color=body_color, zorder=5)
    ax.add_patch(head)

    # --- EARS ---
    # Outer ears
    left_ear = Polygon([(2.6, 8.8), (3.8, 7.8), (2.2, 10.0)], color=body_color, zorder=4)
    right_ear = Polygon([(7.4, 8.8), (6.2, 7.8), (7.8, 10.0)], color=body_color, zorder=4)
    ax.add_patch(left_ear)
    ax.add_patch(right_ear)

    # Inner ears
    left_inner_ear = Polygon([(2.7, 8.8), (3.6, 8.1), (2.5, 9.5)], color=inner_ear_color, zorder=5)
    right_inner_ear = Polygon([(7.3, 8.8), (6.4, 8.1), (7.5, 9.5)], color=inner_ear_color, zorder=5)
    ax.add_patch(left_inner_ear)
    ax.add_patch(right_inner_ear)

    # --- FOREHEAD STRIPES (Tabby marks) ---
    stripes_x = [[4.6, 4.4], [5.0, 5.0], [5.4, 5.6]]
    stripes_y = [[8.2, 7.6], [8.3, 7.7], [8.2, 7.6]]
    for x, y in zip(stripes_x, stripes_y):
        ax.plot(x, y, color=dark_color, lw=4, solid_capstyle='round', zorder=6)

    # --- CHEEKS (Fluff) ---
    left_cheek = Ellipse((3.2, 5.8), 1.5, 1.2, color=body_color, zorder=6)
    right_cheek = Ellipse((6.8, 5.8), 1.5, 1.2, color=body_color, zorder=6)
    ax.add_patch(left_cheek)
    ax.add_patch(right_cheek)

    # --- EYES ---
    # Eye base (big cute eyes)
    left_eye = Ellipse((3.8, 6.5), 1.2, 1.6, color=eye_color, zorder=7)
    right_eye = Ellipse((6.2, 6.5), 1.2, 1.6, color=eye_color, zorder=7)
    ax.add_patch(left_eye)
    ax.add_patch(right_eye)

    # Eye Highlights
    left_h1 = Circle((3.5, 7.0), 0.3, color='white', zorder=8)
    left_h2 = Circle((4.0, 6.3), 0.12, color='white', zorder=8)
    right_h1 = Circle((5.9, 7.0), 0.3, color='white', zorder=8)
    right_h2 = Circle((6.4, 6.3), 0.12, color='white', zorder=8)
    for patch in [left_h1, left_h2, right_h1, right_h2]:
        ax.add_patch(patch)

    # --- BLUSH ---
    left_blush = Ellipse((2.9, 5.4), 1.0, 0.5, color='#FFB6C1', alpha=0.6, zorder=7)
    right_blush = Ellipse((7.1, 5.4), 1.0, 0.5, color='#FFB6C1', alpha=0.6, zorder=7)
    ax.add_patch(left_blush)
    ax.add_patch(right_blush)

    # --- NOSE ---
    nose = Polygon([(4.8, 5.7), (5.2, 5.7), (5.0, 5.4)], color=nose_color, zorder=7)
    ax.add_patch(nose)

    # --- MOUTH ---
    # Using half circles for the classic "W" cat mouth
    theta = np.linspace(0, np.pi, 20)
    
    # Left mouth curve
    x_l = 4.85 - 0.2 * np.cos(theta)
    y_l = 5.4 + 0.2 * np.sin(theta) - 0.2
    ax.plot(x_l, y_l, color=eye_color, lw=2, zorder=7)

    # Right mouth curve
    x_r = 5.15 + 0.2 * np.cos(theta)
    y_r = 5.4 + 0.2 * np.sin(theta) - 0.2
    ax.plot(x_r, y_r, color=eye_color, lw=2, zorder=7)

    # --- WHISKERS ---
    # Left whiskers
    whisker_x_l = [[3.2, 1.2], [3.2, 1.0], [3.4, 1.4]]
    whisker_y_l = [[5.9, 6.4], [5.6, 5.5], [5.3, 4.8]]
    for x, y in zip(whisker_x_l, whisker_y_l):
        ax.plot(x, y, color='gray', lw=1.5, zorder=7)

    # Right whiskers
    whisker_x_r = [[6.8, 8.8], [6.8, 9.0], [6.6, 8.6]]
    whisker_y_r = [[5.9, 6.4], [5.6, 5.5], [5.3, 4.8]]
    for x, y in zip(whisker_x_r, whisker_y_r):
        ax.plot(x, y, color='gray', lw=1.5, zorder=7)

    # Add a title
    plt.title("Cute Kitten", fontsize=20, fontweight='bold', pad=20)
    
    plt.show()

if __name__ == "__main__":
    draw_kitten()
