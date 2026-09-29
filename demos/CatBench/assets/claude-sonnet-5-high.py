import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path

def draw_kitten():
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Background
    ax.set_facecolor('#FFF8E7')
    
    # ===== EARS =====
    # Left ear (outer)
    left_ear = patches.Polygon([(-2.8, 3.2), (-1.8, 5.5), (-0.5, 3.5)], 
                                 closed=True, fc='#F4A460', ec='black', lw=2, zorder=1)
    ax.add_patch(left_ear)
    # Left ear (inner)
    left_ear_inner = patches.Polygon([(-2.3, 3.5), (-1.8, 4.9), (-1.0, 3.7)], 
                                       closed=True, fc='#FFB6C1', ec='none', zorder=2)
    ax.add_patch(left_ear_inner)
    
    # Right ear (outer)
    right_ear = patches.Polygon([(2.8, 3.2), (1.8, 5.5), (0.5, 3.5)], 
                                  closed=True, fc='#F4A460', ec='black', lw=2, zorder=1)
    ax.add_patch(right_ear)
    # Right ear (inner)
    right_ear_inner = patches.Polygon([(2.3, 3.5), (1.8, 4.9), (1.0, 3.7)], 
                                        closed=True, fc='#FFB6C1', ec='none', zorder=2)
    ax.add_patch(right_ear_inner)
    
    # ===== HEAD =====
    head = patches.Ellipse((0, 1.5), 5.5, 5, fc='#F4A460', ec='black', lw=2, zorder=3)
    ax.add_patch(head)
    
    # ===== FACE MARKINGS (cheeks lighter patch) =====
    face_patch = patches.Ellipse((0, 1), 4.5, 3.5, fc='#FFDAB3', ec='none', alpha=0.5, zorder=4)
    ax.add_patch(face_patch)
    
    # ===== EYES =====
    # Eye whites
    left_eye_white = patches.Ellipse((-1.2, 1.8), 1.1, 1.3, fc='white', ec='black', lw=1.5, zorder=5)
    right_eye_white = patches.Ellipse((1.2, 1.8), 1.1, 1.3, fc='white', ec='black', lw=1.5, zorder=5)
    ax.add_patch(left_eye_white)
    ax.add_patch(right_eye_white)
    
    # Iris (big green eyes)
    left_iris = patches.Circle((-1.2, 1.75), 0.42, fc='#7CFC00', ec='black', lw=1, zorder=6)
    right_iris = patches.Circle((1.2, 1.75), 0.42, fc='#7CFC00', ec='black', lw=1, zorder=6)
    ax.add_patch(left_iris)
    ax.add_patch(right_iris)
    
    # Pupils
    left_pupil = patches.Ellipse((-1.2, 1.75), 0.15, 0.38, fc='black', zorder=7)
    right_pupil = patches.Ellipse((1.2, 1.75), 0.15, 0.38, fc='black', zorder=7)
    ax.add_patch(left_pupil)
    ax.add_patch(right_pupil)
    
    # Eye shine
    left_shine = patches.Circle((-1.35, 1.95), 0.1, fc='white', zorder=8)
    right_shine = patches.Circle((1.05, 1.95), 0.1, fc='white', zorder=8)
    ax.add_patch(left_shine)
    ax.add_patch(right_shine)
    
    # ===== NOSE =====
    nose = patches.Polygon([(-0.25, 0.9), (0.25, 0.9), (0, 0.55)], 
                             closed=True, fc='#FF69B4', ec='black', lw=1.5, zorder=6)
    ax.add_patch(nose)
    
    # ===== MOUTH =====
    # Vertical line from nose
    ax.plot([0, 0], [0.55, 0.3], color='black', lw=1.5, zorder=6)
    
    # Smile curves (like a "w" shape / cat mouth)
    t = [i/100 for i in range(101)]
    left_mouth_x = [-0.6 * (1 - (2*ti - 1)**2) for ti in t]
    left_mouth_y = [0.3 - 0.35*ti for ti in t]
    ax.plot([0 + x for x in left_mouth_x[:51]], 
             [0.3 - 0.3*x for x in [abs(i/50) for i in range(51)]], 
             color='black', lw=1.5, zorder=6)
    
    # Simpler mouth: two arcs
    from matplotlib.patches import Arc
    left_smile = Arc((-0.3, 0.35), 0.6, 0.5, angle=0, theta1=200, theta2=340, color='black', lw=1.5, zorder=6)
    right_smile = Arc((0.3, 0.35), 0.6, 0.5, angle=0, theta1=200, theta2=340, color='black', lw=1.5, zorder=6)
    ax.add_patch(left_smile)
    ax.add_patch(right_smile)
    
    # ===== WHISKERS =====
    whisker_specs = [
        # (start_x, start_y, end_x, end_y)
        (-1.5, 0.8, -3.3, 1.2),
        (-1.5, 0.6, -3.3, 0.6),
        (-1.5, 0.4, -3.3, 0.0),
        (1.5, 0.8, 3.3, 1.2),
        (1.5, 0.6, 3.3, 0.6),
        (1.5, 0.4, 3.3, 0.0),
    ]
    for x1, y1, x2, y2 in whisker_specs:
        ax.plot([x1, x2], [y1, y2], color='black', lw=1, zorder=6)
    
    # ===== BLUSH =====
    left_blush = patches.Ellipse((-2.0, 0.9), 0.6, 0.35, fc='#FFB6C1', ec='none', alpha=0.6, zorder=5)
    right_blush = patches.Ellipse((2.0, 0.9), 0.6, 0.35, fc='#FFB6C1', ec='none', alpha=0.6, zorder=5)
    ax.add_patch(left_blush)
    ax.add_patch(right_blush)
    
    # ===== BODY =====
    body = patches.Ellipse((0, -3), 4.5, 4, fc='#F4A460', ec='black', lw=2, zorder=0)
    ax.add_patch(body)
    
    # Belly patch
    belly = patches.Ellipse((0, -3.3), 2.5, 2.8, fc='#FFDAB3', ec='none', alpha=0.6, zorder=1)
    ax.add_patch(belly)
    
    # ===== PAWS =====
    left_paw = patches.Ellipse((-1.3, -4.8), 1.2, 0.8, fc='#F4A460', ec='black', lw=1.5, zorder=1)
    right_paw = patches.Ellipse((1.3, -4.8), 1.2, 0.8, fc='#F4A460', ec='black', lw=1.5, zorder=1)
    ax.add_patch(left_paw)
    ax.add_patch(right_paw)
    
    # Paw toe lines
    ax.plot([-1.6, -1.6], [-4.5, -4.9], color='black', lw=1, zorder=2)
    ax.plot([-1.3, -1.3], [-4.5, -4.9], color='black', lw=1, zorder=2)
    ax.plot([-1.0, -1.0], [-4.5, -4.9], color='black', lw=1, zorder=2)
    
    ax.plot([1.0, 1.0], [-4.5, -4.9], color='black', lw=1, zorder=2)
    ax.plot([1.3, 1.3], [-4.5, -4.9], color='black', lw=1, zorder=2)
    ax.plot([1.6, 1.6], [-4.5, -4.9], color='black', lw=1, zorder=2)
    
    # ===== TAIL =====
    tail_verts = [
        (2.2, -3.5),
        (3.5, -3.0),
        (4.3, -1.5),
        (4.0, 0.0),
        (3.3, 0.3),
        (3.6, -1.2),
        (3.0, -2.5),
        (2.0, -3.0),
    ]
    tail = patches.Polygon(tail_verts, closed=True, fc='#F4A460', ec='black', lw=2, zorder=-1)
    ax.add_patch(tail)
    
    # Tail tip
    tail_tip = patches.Ellipse((3.65, 0.0), 0.8, 0.5, fc='#FFDAB3', ec='none', alpha=0.7, zorder=0)
    ax.add_patch(tail_tip)
    
    # ===== STRIPES (tabby pattern) =====
    stripe_specs_head = [
        ((-1.8, 3.0), 0.15, 1.0, -20),
        ((0, 3.3), 0.15, 1.0, 0),
        ((1.8, 3.0), 0.15, 1.0, 20),
    ]
    for (cx, cy), w, h, angle in stripe_specs_head:
        stripe = patches.Ellipse((cx, cy), w, h, angle=angle, fc='#D2691E', ec='none', alpha=0.5, zorder=4)
        ax.add_patch(stripe)
    
    stripe_specs_body = [
        ((-1.5, -1.5), 0.3, 1.2, 10),
        ((0, -1.3), 0.3, 1.2, 0),
        ((1.5, -1.5), 0.3, 1.2, -10),
    ]
    for (cx, cy), w, h, angle in stripe_specs_body:
        stripe = patches.Ellipse((cx, cy), w, h, angle=angle, fc='#D2691E', ec='none', alpha=0.4, zorder=1)
        ax.add_patch(stripe)
    
    # Tail stripes
    tail_stripes = [
        ((2.7, -3.0), 0.3, 0.6, 60),
        ((3.5, -2.0), 0.3, 0.6, 70),
        ((3.8, -0.8), 0.3, 0.6, 80),
    ]
    for (cx, cy), w, h, angle in tail_stripes:
        stripe = patches.Ellipse((cx, cy), w, h, angle=angle, fc='#D2691E', ec='none', alpha=0.4, zorder=0)
        ax.add_patch(stripe)
    
    # ===== SET LIMITS AND STYLE =====
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.title('🐱 Cute Kitten 🐱', fontsize=18, fontweight='bold', color='#8B4513', pad=20)
    plt.tight_layout()
    plt.savefig('cute_kitten.png', dpi=150, bbox_inches='tight', facecolor='#FFF8E7')
    plt.show()

if __name__ == '__main__':
    draw_kitten()
