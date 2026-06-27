import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_cute_kitten():
    # Create figure and axis
    fig, ax = plt.subplots(1, figsize=(10, 10))
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Background
    ax.add_patch(patches.Rectangle((-5, -5), 10, 10, facecolor='#87CEEB', edgecolor='none'))
    
    # Body (main circle)
    body = patches.Circle((0, 0), 2.5, facecolor='#FFB6C1', edgecolor='black', linewidth=2)
    ax.add_patch(body)
    
    # Belly
    belly = patches.Ellipse((0, -0.5), 3, 1.5, angle=0, facecolor='#FFD1DC', edgecolor='black', linewidth=2)
    ax.add_patch(belly)
    
    # Ears (left)
    ear_left = patches.Polygon([[ -1.8, 4.5], [-1.2, 2.5], [-0.6, 4.5]], 
                                facecolor='#FFB6C1', edgecolor='black', linewidth=2)
    ax.add_patch(ear_left)
    
    # Ears (right)
    ear_right = patches.Polygon([[ 0.6, 4.5], [ 1.2, 2.5], [ 1.8, 4.5]], 
                                 facecolor='#FFB6C1', edgecolor='black', linewidth=2)
    ax.add_patch(ear_right)
    
    # Inner ears (left)
    inner_ear_left = patches.Polygon([[ -1.5, 4.2], [-1.2, 2.8], [-0.9, 4.2]], 
                                        facecolor='#FFB6C1', edgecolor='black', linewidth=2)
    ax.add_patch(inner_ear_left)
    
    # Inner ears (right)
    inner_ear_right = patches.Polygon([[ 0.9, 4.2], [ 1.2, 2.8], [ 1.5, 4.2]], 
                                       facecolor='#FFB6C1', edgecolor='black', linewidth=2)
    ax.add_patch(inner_ear_right)
    
    # Head
    head = patches.Circle((0, 3), 2, facecolor='#FFB6C1', edgecolor='black', linewidth=2)
    ax.add_patch(head)
    
    # Eyes (left)
    eye_left = patches.Ellipse((-0.7, 3.5), 0.8, 0.6, angle=0, 
                                facecolor='white', edgecolor='black', linewidth=2)
    ax.add_patch(eye_left)
    pupil_left = patches.Circle((-0.7, 3.5), 0.2, facecolor='black')
    ax.add_patch(pupil_left)
    
    # Eyes (right)
    eye_right = patches.Ellipse((0.7, 3.5), 0.8, 0.6, angle=0, 
                                 facecolor='white', edgecolor='black', linewidth=2)
    ax.add_patch(eye_right)
    pupil_right = patches.Circle((0.7, 3.5), 0.2, facecolor='black')
    ax.add_patch(pupil_right)
    
    # Nose
    nose = patches.Ellipse((0, 3.2), 0.4, 0.25, angle=0, facecolor='#FF69B4', edgecolor='black', linewidth=1.5)
    ax.add_patch(nose)
    
    # Mouth
    mouth = patches.Arc((0, 3.0), 0.8, 0.4, angle=0, theta1=0, theta2=180, color='black', linewidth=2)
    ax.add_patch(mouth)
    
    # Whiskers (left)
    ax.plot([-1.3, -0.5], [2.9, 2.95], color='black', linewidth=1)
    ax.plot([-1.3, -0.5], [2.7, 2.75], color='black', linewidth=1)
    
    # Whiskers (right)
    ax.plot([1.3, 0.5], [2.9, 2.95], color='black', linewidth=1)
    ax.plot([1.3, 0.5], [2.7, 2.75], color='black', linewidth=1)
    
    # Front paws
    paw_left = patches.Ellipse((-0.8, -1.5), 0.6, 0.3, angle=0, facecolor='#FFB6C1', edgecolor='black', linewidth=2)
    ax.add_patch(paw_left)
    paw_right = patches.Ellipse((0.8, -1.5), 0.6, 0.3, angle=0, facecolor='#FFB6C1', edgecolor='black', linewidth=2)
    ax.add_patch(paw_right)
    
    # Back paws
    back_paw_left = patches.Ellipse((-1.5, -2.2), 0.7, 0.35, angle=30, facecolor='#FFB6C1', edgecolor='black', linewidth=2)
    ax.add_patch(back_paw_left)
    back_paw_right = patches.Ellipse((1.5, -2.2), 0.7, 0.35, angle=-30, facecolor='#FFB6C1', edgecolor='black', linewidth=2)
    ax.add_patch(back_paw_right)
    
    # Tail
    tail = patches.Ellipse((0, -2.5), 0.5, 2.2, angle=-45, facecolor='#FFB6C1', edgecolor='black', linewidth=2)
    ax.add_patch(tail)
    
    # Tail tip
    tail_tip = patches.Circle((0.3, -3.8), 0.3, facecolor='#FFB6C1', edgecolor='black', linewidth=2)
    ax.add_patch(tail_tip)
    
    # Title
    plt.title('🐱 Cute Kitten 🐱', fontsize=20, fontfamily='serif', fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.show()

# Run the function
draw_cute_kitten()
