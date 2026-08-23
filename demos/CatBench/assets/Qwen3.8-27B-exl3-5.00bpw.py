import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_kitten():
    """Draw a cute kitten using matplotlib."""
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Colors
    fur_color = '#FFB6C1'  # Light pink
    ear_inner_color = '#FF69B4'  # Hot pink
    eye_color = '#333333'  # Dark gray
    nose_color = '#FF69B4'  # Hot pink
    mouth_color = '#333333'  # Dark gray
    whisker_color = '#333333'  # Dark gray
    cheek_color = '#FF99AA'  # Lighter pink for cheeks
    
    # Draw body (ellipse)
    body = patches.Ellipse((0, -1.5), width=4, height=3, facecolor=fur_color, edgecolor='#CC8899', linewidth=2)
    ax.add_patch(body)
    
    # Draw head (circle)
    head = patches.Circle((0, 1.5), radius=2, facecolor=fur_color, edgecolor='#CC8899', linewidth=2)
    ax.add_patch(head)
    
    # Draw left ear (triangle)
    left_ear_outer = patches.Polygon([(-1.5, 2.5), (-2.5, 4.5), (-0.5, 3.5)], closed=True, facecolor=fur_color, edgecolor='#CC8899', linewidth=2)
    ax.add_patch(left_ear_outer)
    
    # Draw left ear inner
    left_ear_inner = patches.Polygon([(-1.3, 2.8), (-2.1, 4.0), (-0.7, 3.3)], closed=True, facecolor=ear_inner_color, edgecolor='none')
    ax.add_patch(left_ear_inner)
    
    # Draw right ear (triangle)
    right_ear_outer = patches.Polygon([(1.5, 2.5), (2.5, 4.5), (0.5, 3.5)], closed=True, facecolor=fur_color, edgecolor='#CC8899', linewidth=2)
    ax.add_patch(right_ear_outer)
    
    # Draw right ear inner
    right_ear_inner = patches.Polygon([(1.3, 2.8), (2.1, 4.0), (0.7, 3.3)], closed=True, facecolor=ear_inner_color, edgecolor='none')
    ax.add_patch(right_ear_inner)
    
    # Draw left eye
    left_eye = patches.Circle((-0.7, 1.8), radius=0.3, facecolor=eye_color, edgecolor='none')
    ax.add_patch(left_eye)
    
    # Draw left eye highlight
    left_eye_highlight = patches.Circle((-0.6, 1.9), radius=0.1, facecolor='white', edgecolor='none')
    ax.add_patch(left_eye_highlight)
    
    # Draw right eye
    right_eye = patches.Circle((0.7, 1.8), radius=0.3, facecolor=eye_color, edgecolor='none')
    ax.add_patch(right_eye)
    
    # Draw right eye highlight
    right_eye_highlight = patches.Circle((0.8, 1.9), radius=0.1, facecolor='white', edgecolor='none')
    ax.add_patch(right_eye_highlight)
    
    # Draw nose (small triangle)
    nose = patches.Polygon([(-0.15, 1.2), (0.15, 1.2), (0, 1.0)], closed=True, facecolor=nose_color, edgecolor='none')
    ax.add_patch(nose)
    
    # Draw mouth (two small curves)
    # Left mouth curve
    t = np.linspace(0, np.pi, 50)
    x_left_mouth = -0.3 + 0.3 * np.cos(t)
    y_left_mouth = 0.9 - 0.15 * np.sin(t)
    ax.plot(x_left_mouth, y_left_mouth, color=mouth_color, linewidth=1.5)
    
    # Right mouth curve
    x_right_mouth = 0.3 - 0.3 * np.cos(t)
    y_right_mouth = 0.9 - 0.15 * np.sin(t)
    ax.plot(x_right_mouth, y_right_mouth, color=mouth_color, linewidth=1.5)
    
    # Draw whiskers
    # Left whiskers
    ax.plot([-1.5, -3.0], [1.3, 1.5], color=whisker_color, linewidth=1)
    ax.plot([-1.5, -3.0], [1.1, 1.1], color=whisker_color, linewidth=1)
    ax.plot([-1.5, -3.0], [0.9, 0.7], color=whisker_color, linewidth=1)
    
    # Right whiskers
    ax.plot([1.5, 3.0], [1.3, 1.5], color=whisker_color, linewidth=1)
    ax.plot([1.5, 3.0], [1.1, 1.1], color=whisker_color, linewidth=1)
    ax.plot([1.5, 3.0], [0.9, 0.7], color=whisker_color, linewidth=1)
    
    # Draw cheeks (blush)
    left_cheek = patches.Circle((-1.2, 1.0), radius=0.25, facecolor=cheek_color, edgecolor='none', alpha=0.5)
    ax.add_patch(left_cheek)
    
    right_cheek = patches.Circle((1.2, 1.0), radius=0.25, facecolor=cheek_color, edgecolor='none', alpha=0.5)
    ax.add_patch(right_cheek)
    
    # Draw front paws
    left_paw = patches.Ellipse((-1.0, -2.5), width=0.8, height=0.6, facecolor=fur_color, edgecolor='#CC8899', linewidth=1.5)
    ax.add_patch(left_paw)
    
    right_paw = patches.Ellipse((1.0, -2.5), width=0.8, height=0.6, facecolor=fur_color, edgecolor='#CC8899', linewidth=1.5)
    ax.add_patch(right_paw)
    
    # Draw tail
    t_tail = np.linspace(0, np.pi, 50)
    x_tail = 2.0 + 0.5 * np.cos(t_tail)
    y_tail = -1.5 + 1.5 * np.sin(t_tail)
    ax.plot(x_tail, y_tail, color=fur_color, linewidth=8, solid_capstyle='round')
    ax.plot(x_tail, y_tail, color='#CC8899', linewidth=1, solid_capstyle='round')
    
    plt.title('Cute Kitten', fontsize=16, pad=10)
    plt.tight_layout()
    plt.savefig('kitten.png', dpi=150, bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    draw_kitten()