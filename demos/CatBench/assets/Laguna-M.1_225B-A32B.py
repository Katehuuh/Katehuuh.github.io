import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_kitten():
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.set_aspect('equal')
    ax.set_xlim(-3, 3)
    ax.set_ylim(-4, 4)
    ax.axis('off')

    # Kitten body (main oval)
    body = patches.Ellipse((0, -1), width=2.5, height=3.5, 
                           facecolor='#FFB6C1', edgecolor='black', linewidth=2)
    ax.add_patch(body)

    # Head (smaller oval on top)
    head = patches.Ellipse((0, 1.5), width=2, height=1.8,
                           facecolor='#FFB6C1', edgecolor='black', linewidth=2)
    ax.add_patch(head)

    # Ears (two triangles)
    ear_left = patches.Polygon([[-0.9, 2.8], [0, 3.8], [-0.6, 2.8]],
                                facecolor='#FFB6C1', edgecolor='black', linewidth=2)
    ear_right = patches.Polygon([[0.9, 2.8], [0, 3.8], [0.6, 2.8]],
                                facecolor='#FFB6C1', edgecolor='black', linewidth=2)
    ax.add_patch(ear_left)
    ax.add_patch(ear_right)

    # Inner ears
    inner_ear_left = patches.Polygon([[-0.8, 2.9], [-0.1, 3.5], [-0.5, 2.9]],
                                     facecolor='#FFC0CB', alpha=0.7)
    inner_ear_right = patches.Polygon([[0.8, 2.9], [0.1, 3.5], [0.5, 2.9]],
                                     facecolor='#FFC0CB', alpha=0.7)
    ax.add_patch(inner_ear_left)
    ax.add_patch(inner_ear_right)

    # Eyes (big circles for cuteness)
    eye_left = patches.Circle((-0.5, 1.7), radius=0.3, 
                              facecolor='white', edgecolor='black', linewidth=2)
    eye_right = patches.Circle((0.5, 1.7), radius=0.3,
                               facecolor='white', edgecolor='black', linewidth=2)
    ax.add_patch(eye_left)
    ax.add_patch(eye_right)

    # Pupils
    pupil_left = patches.Circle((-0.45, 1.75), radius=0.15, facecolor='black')
    pupil_right = patches.Circle((0.45, 1.75), radius=0.15, facecolor='black')
    ax.add_patch(pupil_left)
    ax.add_patch(pupil_right)

    # Nose (small triangle)
    nose = patches.Polygon([[0, 1.2], [-0.2, 0.9], [0.2, 0.9]],
                          facecolor='#FFB6C1', edgecolor='black', linewidth=1.5)
    ax.add_patch(nose)

    # Mouth
    mouth = patches.Arc((0, 0.8), width=0.8, height=0.4, theta1=200, theta2=320,
                        color='black', linewidth=1.5)
    ax.add_patch(mouth)

    # Whiskers
    whisker_left1 = patches.FancyArrow(-1.2, 1.1, -0.8, 0.2, width=0.02, 
                                        head_length=0.1, head_width=0.1, color='black')
    whisker_left2 = patches.FancyArrow(-1.2, 0.95, -0.8, 0, width=0.02,
                                        head_length=0.1, head_width=0.1, color='black')
    whisker_left3 = patches.FancyArrow(-1.2, 0.8, -0.8, -0.2, width=0.02,
                                        head_length=0.1, head_width=0.1, color='black')
    whisker_right1 = patches.FancyArrow(1.2, 1.1, 0.8, 0.2, width=0.02,
                                         head_length=0.1, head_width=0.1, color='black')
    whisker_right2 = patches.FancyArrow(1.2, 0.95, 0.8, 0, width=0.02,
                                         head_length=0.1, head_width=0.1, color='black')
    whisker_right3 = patches.FancyArrow(1.2, 0.8, 0.8, -0.2, width=0.02,
                                         head_length=0.1, head_width=0.1, color='black')
    for w in [whisker_left1, whisker_left2, whisker_left3, 
              whisker_right1, whisker_right2, whisker_right3]:
        ax.add_patch(w)

    # Front legs
    leg_left = patches.Rectangle((-1, -2.5), width=0.4, height=1.2,
                                facecolor='#FFB6C1', edgecolor='black', linewidth=2)
    leg_right = patches.Rectangle((0.6, -2.5), width=0.4, height=1.2,
                                 facecolor='#FFB6C1', edgecolor='black', linewidth=2)
    ax.add_patch(leg_left)
    ax.add_patch(leg_right)

    # Paws
    paw_left = patches.Ellipse((-0.8, -3.2), width=0.5, height=0.3,
                              facecolor='#FFC0CB', edgecolor='black', linewidth=1.5)
    paw_right = patches.Ellipse((0.8, -3.2), width=0.5, height=0.3,
                               facecolor='#FFC0CB', edgecolor='black', linewidth=1.5)
    ax.add_patch(paw_left)
    ax.add_patch(paw_right)

    # Tail (curved shape)
    tail = patches.Arc((0, -1), width=4, height=2, theta1=-60, theta2=200,
                       color='#FFB6C1', linewidth=10, alpha=0.9)
    ax.add_patch(tail)

    # Blush marks on cheeks
    blush_left = patches.Circle((-0.85, 0.8), radius=0.25, facecolor='#FF69B4', alpha=0.5)
    blush_right = patches.Circle((0.85, 0.8), radius=0.25, facecolor='#FF69B4', alpha=0.5)
    ax.add_patch(blush_left)
    ax.add_patch(blush_right)

    plt.title("A Cute Kitten", fontsize=20, pad=20, fontfamily='cursive')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    draw_kitten()
