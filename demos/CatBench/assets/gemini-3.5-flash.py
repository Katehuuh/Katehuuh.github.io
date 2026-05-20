import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_kitten():
    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_aspect('equal')
    ax.axis('off')  # Hide grid and axes

    # Colors
    body_color = '#FBE3B5'       # Cream/Light Orange
    inner_ear_color = '#F9A7B0'  # Soft Pink
    eye_color = '#2C3E50'        # Dark Slate
    nose_color = '#E8818C'       # Rose Pink
    line_color = '#5C4033'       # Dark Brown

    # 1. Ears (Outer and Inner)
    # Left Ear
    left_ear = patches.Polygon([[-3.2, 1.5], [-1.2, 3.2], [-3.5, 4.8]], color=body_color, zorder=1)
    left_inner = patches.Polygon([[-2.9, 1.8], [-1.5, 3.0], [-3.1, 4.2]], color=inner_ear_color, zorder=2)
    # Right Ear
    right_ear = patches.Polygon([[3.2, 1.5], [1.2, 3.2], [3.5, 4.8]], color=body_color, zorder=1)
    right_inner = patches.Polygon([[2.9, 1.8], [1.5, 3.0], [3.1, 4.2]], color=inner_ear_color, zorder=2)
    
    ax.add_patch(left_ear)
    ax.add_patch(left_inner)
    ax.add_patch(right_ear)
    ax.add_patch(right_inner)

    # 2. Head (Main Face)
    head = patches.Circle((0, 0), radius=3.5, color=body_color, zorder=3)
    ax.add_patch(head)

    # 3. Eyes & Highlights
    # Left Eye
    left_eye = patches.Circle((-1.3, 0.5), radius=0.45, color=eye_color, zorder=4)
    left_sparkle1 = patches.Circle((-1.15, 0.65), radius=0.13, color='white', zorder=5)
    left_sparkle2 = patches.Circle((-1.45, 0.35), radius=0.06, color='white', zorder=5)
    # Right Eye
    right_eye = patches.Circle((1.3, 0.5), radius=0.45, color=eye_color, zorder=4)
    right_sparkle1 = patches.Circle((1.45, 0.65), radius=0.13, color='white', zorder=5)
    right_sparkle2 = patches.Circle((1.15, 0.35), radius=0.06, color='white', zorder=5)

    ax.add_patch(left_eye)
    ax.add_patch(left_sparkle1)
    ax.add_patch(left_sparkle2)
    ax.add_patch(right_eye)
    ax.add_patch(right_sparkle1)
    ax.add_patch(right_sparkle2)

    # 4. Blush
    left_blush = patches.Ellipse((-2.1, -0.3), 1.0, 0.5, color=inner_ear_color, alpha=0.6, zorder=4)
    right_blush = patches.Ellipse((2.1, -0.3), 1.0, 0.5, color=inner_ear_color, alpha=0.6, zorder=4)
    ax.add_patch(left_blush)
    ax.add_patch(right_blush)

    # 5. Nose
    nose = patches.Polygon([[-0.2, 0.0], [0.2, 0.0], [0, -0.18]], color=nose_color, zorder=4)
    ax.add_patch(nose)

    # 6. Mouth (Cute 'w' shape)
    # Left curve of mouth
    ax.plot([-0.4, -0.2, 0], [-0.4, -0.55, -0.3], color=line_color, lw=2.5, solid_capstyle='round', zorder=4)
    # Right curve of mouth
    ax.plot([0, 0.2, 0.4], [-0.3, -0.55, -0.4], color=line_color, lw=2.5, solid_capstyle='round', zorder=4)

    # 7. Whiskers
    # Left whiskers
    ax.plot([-2.8, -4.3], [-0.1, 0.1], color=line_color, lw=1.5, zorder=4)
    ax.plot([-2.9, -4.5], [-0.4, -0.4], color=line_color, lw=1.5, zorder=4)
    # Right whiskers
    ax.plot([2.8, 4.3], [-0.1, 0.1], color=line_color, lw=1.5, zorder=4)
    ax.plot([2.9, 4.5], [-0.4, -0.4], color=line_color, lw=1.5, zorder=4)

    # Display the final image
    plt.show()

if __name__ == "__main__":
    draw_kitten()
