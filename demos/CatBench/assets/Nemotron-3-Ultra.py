import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
import numpy as np

def draw_kitten(ax, blink=False, look_direction='center'):
    """
    Draws a cute kitten on the provided axes.
    
    Parameters:
    - ax: matplotlib axes object
    - blink: bool, if True, eyes are closed (sleeping/blinking)
    - look_direction: 'left', 'right', 'center', 'up' - moves pupils
    """
    
    # --- Color Palette ---
    FUR_COLOR = '#F5E6D3'      # Cream/light tan
    FUR_DARK = '#D4B896'       # Slightly darker for shading/ears
    PINK = '#FFB6C1'           # Nose/inner ear
    WHITE = '#FFFFFF'
    BLACK = '#2D2D2D'
    EYE_COLOR = '#7FFFD4'      # Aquamarine/Cyan eyes
    PUPIL_COLOR = '#1A1A1A'
    WHISKER_COLOR = '#555555'

    # --- Helper to add patches easily ---
    def add_patch(patch):
        ax.add_patch(patch)

    # ==========================================
    # 1. HEAD SHAPE (Base)
    # ==========================================
    # Main face circle
    head = patches.Circle((0, 0), 1.0, facecolor=FUR_COLOR, edgecolor=BLACK, linewidth=2, zorder=1)
    add_patch(head)
    
    # Chin fluff (lower ellipse)
    chin = patches.Ellipse((0, -0.35), 1.1, 0.5, facecolor=WHITE, edgecolor=BLACK, linewidth=1.5, zorder=2)
    add_patch(chin)

    # ==========================================
    # 2. EARS
    # ==========================================
    ear_width = 0.55
    ear_height = 0.7
    
    # Left Ear
    left_ear_outer = patches.Ellipse((-0.55, 0.85), ear_width, ear_height, 
                                     angle=30, facecolor=FUR_DARK, edgecolor=BLACK, linewidth=2, zorder=0)
    left_ear_inner = patches.Ellipse((-0.55, 0.88), ear_width*0.5, ear_height*0.55, 
                                     angle=30, facecolor=PINK, edgecolor='none', zorder=1)
    
    # Right Ear
    right_ear_outer = patches.Ellipse((0.55, 0.85), ear_width, ear_height, 
                                      angle=-30, facecolor=FUR_DARK, edgecolor=BLACK, linewidth=2, zorder=0)
    right_ear_inner = patches.Ellipse((0.55, 0.88), ear_width*0.5, ear_height*0.55, 
                                      angle=-30, facecolor=PINK, edgecolor='none', zorder=1)

    add_patch(left_ear_outer)
    add_patch(left_ear_inner)
    add_patch(right_ear_outer)
    add_patch(right_ear_inner)

    # Ear tufts (little triangles on top)
    for x_base, angle in [(-0.55, 30), (0.55, -30)]:
        # Calculate tip of ear roughly
        tip_x = x_base + (ear_width/2) * np.sin(np.radians(angle))
        tip_y = 0.85 + (ear_height/2) * np.cos(np.radians(angle))
        tuft = patches.RegularPolygon((tip_x, tip_y + 0.05), 3, radius=0.08, 
                                      orientation=np.radians(angle), 
                                      facecolor=FUR_DARK, edgecolor=BLACK, linewidth=1, zorder=0)
        add_patch(tuft)

    # ==========================================
    # 3. EYES
    # ==========================================
    eye_y = 0.15
    eye_x_offset = 0.35
    eye_w = 0.22
    eye_h = 0.28 if not blink else 0.05 # Squash height if blinking

    # Eye Whites / Iris Base
    left_eye_bg = patches.Ellipse((-eye_x_offset, eye_y), eye_w, eye_h, 
                                  facecolor=WHITE, edgecolor=BLACK, linewidth=2, zorder=3)
    right_eye_bg = patches.Ellipse((eye_x_offset, eye_y), eye_w, eye_h, 
                                   facecolor=WHITE, edgecolor=BLACK, linewidth=2, zorder=3)
    add_patch(left_eye_bg)
    add_patch(right_eye_bg)

    if not blink:
        # Iris (Colored part)
        iris_r = 0.12
        # Pupil position logic
        pupil_offset_x = 0
        pupil_offset_y = 0
        if look_direction == 'left': pupil_offset_x = -0.04
        elif look_direction == 'right': pupil_offset_x = 0.04
        elif look_direction == 'up': pupil_offset_y = 0.04
        
        left_iris = patches.Circle((-eye_x_offset + pupil_offset_x, eye_y + pupil_offset_y), iris_r, 
                                   facecolor=EYE_COLOR, edgecolor='#3A8F7A', linewidth=1.5, zorder=4)
        right_iris = patches.Circle((eye_x_offset + pupil_offset_x, eye_y + pupil_offset_y), iris_r, 
                                    facecolor=EYE_COLOR, edgecolor='#3A8F7A', linewidth=1.5, zorder=4)
        add_patch(left_iris)
        add_patch(right_iris)

        # Pupils
        pupil_r = 0.06
        left_pupil = patches.Circle((-eye_x_offset + pupil_offset_x, eye_y + pupil_offset_y), pupil_r, 
                                    facecolor=PUPIL_COLOR, zorder=5)
        right_pupil = patches.Circle((eye_x_offset + pupil_offset_x, eye_y + pupil_offset_y), pupil_r, 
                                     facecolor=PUPIL_COLOR, zorder=5)
        add_patch(left_pupil)
        add_patch(right_pupil)

        # Highlights (Sparkle)
        hl_r = 0.025
        # Main highlight (top-right of pupil usually)
        hl_x_off = 0.04
        hl_y_off = 0.04
        for ex in [-eye_x_offset, eye_x_offset]:
            hl = patches.Circle((ex + hl_x_off + pupil_offset_x, eye_y + hl_y_off + pupil_offset_y), hl_r, 
                                facecolor=WHITE, edgecolor='none', zorder=6)
            add_patch(hl)
            # Secondary tiny highlight
            hl2 = patches.Circle((ex - 0.03 + pupil_offset_x, eye_y - 0.03 + pupil_offset_y), hl_r*0.6, 
                                 facecolor=WHITE, edgecolor='none', zorder=6)
            add_patch(hl2)

        # Eyebrows / Forehead markings (small lines above eyes)
        for ex in [-eye_x_offset, eye_x_offset]:
            brow = lines.Line2D([ex - 0.12, ex + 0.12], [eye_y + eye_h/2 + 0.02, eye_y + eye_h/2 + 0.02], 
                                color=FUR_DARK, linewidth=2, zorder=3)
            ax.add_line(brow)

    else:
        # Closed eyes (Happy arc)
        for ex in [-eye_x_offset, eye_x_offset]:
            closed_eye = patches.Arc((ex, eye_y), eye_w, 0.05, angle=0, theta1=0, theta2=180, 
                                     color=BLACK, linewidth=2.5, zorder=4)
            add_patch(closed_eye)
            # Eyelashes
            for i in range(3):
                ang = 30 + i * 30
                x_start = ex + (eye_w/2) * np.cos(np.radians(180-ang))
                y_start = eye_y + 0.02
                x_end = x_start + 0.05 * np.cos(np.radians(180-ang))
                y_end = y_start + 0.05 * np.sin(np.radians(180-ang))
                lash = lines.Line2D([x_start, x_end], [y_start, y_end], color=BLACK, linewidth=1.5, zorder=5)
                ax.add_line(lash)

    # ==========================================
    # 4. NOSE & MOUTH
    # ==========================================
    nose_y = -0.15
    # Nose triangle
    nose = patches.Polygon([(0, nose_y + 0.05), (-0.06, nose_y - 0.03), (0.06, nose_y - 0.03)], 
                           facecolor=PINK, edgecolor='#CC8899', linewidth=1.5, zorder=4)
    add_patch(nose)
    # Nose shine
    shine = patches.Ellipse((-0.015, nose_y + 0.02), 0.015, 0.01, facecolor='#FFDDEE', edgecolor='none', zorder=5)
    add_patch(shine)

    # Mouth (Anchor shape)
    mouth_y = nose_y - 0.08
    # Vertical line down from nose
    mouth_line = lines.Line2D([0, 0], [nose_y - 0.03, mouth_y], color=BLACK, linewidth=2, zorder=4)
    ax.add_line(mouth_line)
    # Left curve
    mouth_left = patches.Arc((-0.08, mouth_y), 0.16, 0.1, angle=0, theta1=270, theta2=360, 
                             color=BLACK, linewidth=2, zorder=4)
    # Right curve
    mouth_right = patches.Arc((0.08, mouth_y), 0.16, 0.1, angle=0, theta1=180, theta2=270, 
                              color=BLACK, linewidth=2, zorder=4)
    add_patch(mouth_left)
    add_patch(mouth_right)

    # ==========================================
    # 5. WHISKERS
    # ==========================================
    whisker_y_start = -0.10
    whisker_x_start_left = -0.45
    whisker_x_start_right = 0.45
    whisker_length = 0.7
    
    for side, x_start in [(-1, whisker_x_start_left), (1, whisker_x_start_right)]:
        for i, y_off in enumerate([-0.02, 0.02, 0.06]): # 3 rows
            y = whisker_y_start + y_off
            # Slight curve using a quadratic bezier approximation (polyline)
            # We'll just draw slightly curved lines using multiple segments or Arc
            # Simple straight lines with slight angle variation:
            angle = side * (5 + i * 3) # degrees outward
            x_end = x_start + side * whisker_length * np.cos(np.radians(angle))
            y_end = y + whisker_length * np.sin(np.radians(angle))
            
            whisker = lines.Line2D([x_start, x_end], [y, y_end], 
                                   color=WHISKER_COLOR, linewidth=1.2, alpha=0.8, zorder=3)
            ax.add_line(whisker)

    # ==========================================
    # 6. CHEEK FLUFF / FUR DETAIL
    # ==========================================
    # Small zig-zag or dots on cheeks for texture
    for side, cx in [(-1, -0.6), (1, 0.6)]:
        for i in range(3):
            angle = np.radians(side * (70 + i * 15))
            fx = cx + 0.15 * np.cos(angle)
            fy = -0.2 + 0.1 * np.sin(angle)
            dot = patches.Circle((fx, fy), 0.015, facecolor=FUR_DARK, edgecolor='none', zorder=2, alpha=0.5)
            add_patch(dot)

    # ==========================================
    # 7. BODY (Simple sitting pose)
    # ==========================================
    # Body oval behind head
    body = patches.Ellipse((0, -1.6), 1.6, 1.8, facecolor=FUR_COLOR, edgecolor=BLACK, linewidth=2, zorder=0)
    add_patch(body)
    
    # White belly
    belly = patches.Ellipse((0, -1.7), 0.9, 1.2, facecolor=WHITE, edgecolor='#E0E0E0', linewidth=1, zorder=1)
    add_patch(belly)

    # Front Paws (peeking over belly curve)
    paw_y = -1.1
    left_paw = patches.Ellipse((-0.4, paw_y), 0.3, 0.2, angle=20, facecolor=FUR_COLOR, edgecolor=BLACK, linewidth=1.5, zorder=2)
    right_paw = patches.Ellipse((0.4, paw_y), 0.3, 0.2, angle=-20, facecolor=FUR_COLOR, edgecolor=BLACK, linewidth=1.5, zorder=2)
    add_patch(left_paw)
    add_patch(right_paw)
    
    # Toe beans (pink dots on paws)
    for px in [-0.45, -0.3, 0.3, 0.45]:
        bean = patches.Ellipse((px, paw_y - 0.02), 0.04, 0.025, facecolor=PINK, edgecolor='none', zorder=3)
        add_patch(bean)

    # Tail (curved to the side)
    # Using a path patch for a curved tail
    from matplotlib.path import Path
    verts = [
        (0.7, -1.4),   # Base at hip
        (1.1, -1.2),   # Curve out
        (1.3, -0.7),   # Up
        (1.2, -0.2),   # Tip curl in
        (1.0, -0.1),   # Tip
    ]
    codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    path = Path(verts, codes)
    tail = patches.PathPatch(path, facecolor='none', edgecolor=BLACK, linewidth=3, zorder=0)
    add_patch(tail)
    # Tail fur color (draw a slightly thinner line on top)
    tail_fur = patches.PathPatch(path, facecolor='none', edgecolor=FUR_COLOR, linewidth=2.5, zorder=1)
    add_patch(tail_fur)
    
    # Tail tip fluff
    tip_fluff = patches.RegularPolygon((1.0, -0.1), 6, radius=0.08, facecolor=FUR_DARK, edgecolor=BLACK, linewidth=1, zorder=2)
    add_patch(tip_fluff)


# ==========================================
# MAIN EXECUTION BLOCK
# ==========================================
if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='#FFF8F0') # Warm background
    
    # Draw the kitten
    # Try changing blink=True or look_direction='left'
    draw_kitten(ax, blink=False, look_direction='center') 

    # Setup Axis
    ax.set_aspect('equal')
    ax.set_xlim(-1.8, 1.8)
    ax.set_ylim(-2.2, 1.8)
    ax.axis('off')
    
    # Title
    plt.title("Hello! 🐱", fontsize=20, fontweight='bold', color='#5D4E37', pad=20, fontfamily='sans-serif')
    
    plt.tight_layout()
    plt.show()
