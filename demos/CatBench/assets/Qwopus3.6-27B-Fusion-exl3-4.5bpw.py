import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_cute_kitten():
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.set_aspect('equal')
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.axis('off')

    # --- Body ---
    body = patches.Ellipse((0, -0.5), width=2.4, height=2.0, 
                           facecolor='#FFB6C1', edgecolor='#FF69B4', linewidth=2)
    ax.add_patch(body)

    # --- Head ---
    head = patches.Circle((0, 1.2), radius=1.2, 
                          facecolor='#FFB6C1', edgecolor='#FF69B4', linewidth=2)
    ax.add_patch(head)

    # --- Ears ---
    # Left ear
    left_ear = patches.Polygon([(-0.8, 1.8), (-1.3, 2.8), (-0.3, 2.2)], 
                               facecolor='#FFB6C1', edgecolor='#FF69B4', linewidth=2)
    ax.add_patch(left_ear)
    # Inner left ear
    inner_left_ear = patches.Polygon([(-0.7, 2.0), (-1.1, 2.6), (-0.4, 2.2)], 
                                     facecolor='#FFC0CB', edgecolor='#FF69B4', linewidth=1)
    ax.add_patch(inner_left_ear)

    # Right ear
    right_ear = patches.Polygon([(0.8, 1.8), (1.3, 2.8), (0.3, 2.2)], 
                                facecolor='#FFB6C1', edgecolor='#FF69B4', linewidth=2)
    ax.add_patch(right_ear)
    # Inner right ear
    inner_right_ear = patches.Polygon([(0.7, 2.0), (1.1, 2.6), (0.4, 2.2)], 
                                      facecolor='#FFC0CB', edgecolor='#FF69B4', linewidth=1)
    ax.add_patch(inner_right_ear)

    # --- Eyes ---
    # Left eye
    left_eye_outer = patches.Circle((-0.4, 1.3), radius=0.25, 
                                    facecolor='white', edgecolor='#333333', linewidth=1.5)
    ax.add_patch(left_eye_outer)
    left_eye_inner = patches.Circle((-0.4, 1.3), radius=0.15, 
                                    facecolor='#333333', edgecolor='#333333', linewidth=1)
    ax.add_patch(left_eye_inner)
    # Left eye shine
    left_eye_shine = patches.Circle((-0.35, 1.35), radius=0.05, 
                                    facecolor='white', edgecolor='none')
    ax.add_patch(left_eye_shine)

    # Right eye
    right_eye_outer = patches.Circle((0.4, 1.3), radius=0.25, 
                                     facecolor='white', edgecolor='#333333', linewidth=1.5)
    ax.add_patch(right_eye_outer)
    right_eye_inner = patches.Circle((0.4, 1.3), radius=0.15, 
                                     facecolor='#333333', edgecolor='#333333', linewidth=1)
    ax.add_patch(right_eye_inner)
    # Right eye shine
    right_eye_shine = patches.Circle((0.45, 1.35), radius=0.05, 
                                     facecolor='white', edgecolor='none')
    ax.add_patch(right_eye_shine)

    # --- Nose ---
    nose = patches.Polygon([(-0.08, 0.95), (0.08, 0.95), (0, 0.85)], 
                           facecolor='#FF69B4', edgecolor='#FF69B4', linewidth=1)
    ax.add_patch(nose)

    # --- Mouth ---
    # Left mouth curve
    left_mouth = patches.Arc((0, 0.9), width=0.3, height=0.2, 
                             angle=0, theta1=180, theta2=360, 
                             color='#333333', linewidth=1.5)
    ax.add_patch(left_mouth)
    # Right mouth curve
    right_mouth = patches.Arc((0, 0.9), width=0.3, height=0.2, 
                              angle=0, theta1=0, theta2=180, 
                              color='#333333', linewidth=1.5)
    ax.add_patch(right_mouth)

    # --- Whiskers ---
    # Left whiskers
    ax.plot([-0.5, -1.5], [0.9, 0.8], color='#333333', linewidth=1)
    ax.plot([-0.5, -1.6], [0.95, 0.95], color='#333333', linewidth=1)
    ax.plot([-0.5, -1.5], [1.0, 1.1], color='#333333', linewidth=1)

    # Right whiskers
    ax.plot([0.5, 1.5], [0.9, 0.8], color='#333333', linewidth=1)
    ax.plot([0.5, 1.6], [0.95, 0.95], color='#333333', linewidth=1)
    ax.plot([0.5, 1.5], [1.0, 1.1], color='#333333', linewidth=1)

    # --- Paws ---
    # Left front paw
    left_paw = patches.Ellipse((-0.8, -1.5), width=0.5, height=0.4, 
                               facecolor='#FFB6C1', edgecolor='#FF69B4', linewidth=2)
    ax.add_patch(left_paw)
    # Right front paw
    right_paw = patches.Ellipse((0.8, -1.5), width=0.5, height=0.4, 
                                facecolor='#FFB6C1', edgecolor='#FF69B4', linewidth=2)
    ax.add_patch(right_paw)

    # --- Tail ---
    tail_x = np.linspace(1.0, 2.5, 50)
    tail_y = -0.5 + 0.8 * np.sin(np.linspace(0, np.pi, 50))
    ax.plot(tail_x, tail_y, color='#FFB6C1', linewidth=8, solid_capstyle='round')
    ax.plot(tail_x, tail_y, color='#FF69B4', linewidth=2, solid_capstyle='round')

    # --- Cheeks (blush) ---
    left_cheek = patches.Circle((-0.7, 1.0), radius=0.15, 
                                facecolor='#FF9999', alpha=0.5, edgecolor='none')
    ax.add_patch(left_cheek)
    right_cheek = patches.Circle((0.7, 1.0), radius=0.15, 
                                 facecolor='#FF9999', alpha=0.5, edgecolor='none')
    ax.add_patch(right_cheek)

    plt.title('Cute Kitten', fontsize=16, fontweight='bold', color='#FF69B4')
    plt.tight_layout()
    plt.savefig('cute_kitten.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.show()

if __name__ == '__main__':
    draw_cute_kitten()