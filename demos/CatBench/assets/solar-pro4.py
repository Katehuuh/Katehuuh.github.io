import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create figure and axis
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_aspect('equal')
ax.axis('off')
ax.set_facecolor('#FFF8E7')  # Warm cream background

# === BODY ===
body = patches.Ellipse((0, -1), 3.5, 4, linewidth=2, 
                       edgecolor='#FFA500', facecolor='#FFD700', zorder=1)
ax.add_patch(body)

# === HEAD ===
head = patches.Circle((0, 2), 1.8, linewidth=2, 
                      edgecolor='#FFA500', facecolor='#FFD700', zorder=2)
ax.add_patch(head)

# === EARS ===
ear_left = patches.Polygon([[-1.5, 2.5], [-2.2, 4.5], [-0.5, 3]], 
                           linewidth=2, edgecolor='#FFA500', 
                           facecolor='#FFB6C1', zorder=3)
ear_right = patches.Polygon([[1.5, 2.5], [2.2, 4.5], [0.5, 3]], 
                            linewidth=2, edgecolor='#FFA500', 
                            facecolor='#FFB6C1', zorder=3)
ax.add_patch(ear_left)
ax.add_patch(ear_right)

# === INNER EARS ===
inner_ear_left = patches.Polygon([[-1.3, 2.8], [-1.9, 4.2], [-0.7, 3.1]], 
                                 linewidth=1, edgecolor='#FF69B4', 
                                 facecolor='#FF69B4', zorder=4)
inner_ear_right = patches.Polygon([[1.3, 2.8], [1.9, 4.2], [0.7, 3.1]], 
                                  linewidth=1, edgecolor='#FF69B4', 
                                  facecolor='#FF69B4', zorder=4)
ax.add_patch(inner_ear_left)
ax.add_patch(inner_ear_right)

# === EYES ===
eye_left = patches.Circle((-0.6, 2.5), 0.4, linewidth=1, 
                          edgecolor='black', facecolor='white', zorder=5)
eye_right = patches.Circle((0.6, 2.5), 0.4, linewidth=1, 
                           edgecolor='black', facecolor='white', zorder=5)
ax.add_patch(eye_left)
ax.add_patch(eye_right)

# Pupils
pupil_left = patches.Circle((-0.6, 2.5), 0.2, linewidth=1, 
                            edgecolor='black', facecolor='black', zorder=6)
pupil_right = patches.Circle((0.6, 2.5), 0.2, linewidth=1, 
                             edgecolor='black', facecolor='black', zorder=6)
ax.add_patch(pupil_left)
ax.add_patch(pupil_right)

# Eye shine (cute reflection)
shine_left = patches.Circle((-0.5, 2.6), 0.08, linewidth=0, 
                            facecolor='white', zorder=7)
shine_right = patches.Circle((0.7, 2.6), 0.08, linewidth=0, 
                             facecolor='white', zorder=7)
ax.add_patch(shine_left)
ax.add_patch(shine_right)

# === NOSE ===
nose = patches.Polygon([[0, 2.1], [-0.15, 1.9], [0.15, 1.9]], 
                       linewidth=1, edgecolor='pink', facecolor='pink', zorder=6)
ax.add_patch(nose)

# === MOUTH ===
mouth_left = plt.Line2D([-0.15, -0.35], [1.9, 1.7], 
                            color='pink', linewidth=2, zorder=6)
mouth_right = plt.Line2D([0.15, 0.35], [1.9, 1.7], 
                             color='pink', linewidth=2, zorder=6)
ax.add_line(mouth_left)
ax.add_line(mouth_right)

# === WHISKERS ===
import numpy as np
for i, y_offset in enumerate(np.linspace(-0.1, 0.1, 3)):
    # Left whiskers
    ax.plot([-0.3, -2.5], [1.85 + y_offset, 1.5 + y_offset], 
            color='gray', linewidth=1.5, alpha=0.7, zorder=5)
    # Right whiskers
    ax.plot([0.3, 2.5], [1.85 + y_offset, 1.5 + y_offset], 
            color='gray', linewidth=1.5, alpha=0.7, zorder=5)

# === PAWS ===
paw_left = patches.Ellipse((-1.2, -3.5), 0.6, 0.4, 
                           linewidth=1, edgecolor='#FFA500', 
                           facecolor='#FFE4B5', zorder=2)
paw_right = patches.Ellipse((1.2, -3.5), 0.6, 0.4, 
                            linewidth=1, edgecolor='#FFA500', 
                            facecolor='#FFE4B5', zorder=2)
ax.add_patch(paw_left)
ax.add_patch(paw_right)

# Paw pads
pad_left = patches.Circle((-1.2, -3.5), 0.15, linewidth=0, 
                          facecolor='#FF69B4', zorder=3)
pad_right = patches.Circle((1.2, -3.5), 0.15, linewidth=0, 
                           facecolor='#FF69B4', zorder=3)
ax.add_patch(pad_left)
ax.add_patch(pad_right)

# === TAIL ===
tail_x = np.linspace(2.5, 3.5, 50)
tail_y = -2.5 - 0.3 * np.sin(np.linspace(0, 3*np.pi, 50))
ax.plot(tail_x, tail_y, color='#FFA500', linewidth=8, solid_capstyle='round', zorder=1)
ax.plot(tail_x, tail_y, color='#FFD700', linewidth=6, solid_capstyle='round', zorder=1)

# === FUR TEXTURE (tiny circles on body) ===
for _ in range(20):
    x = np.random.uniform(-1.5, 1.5)
    y = np.random.uniform(-3, 1)
    fur = patches.Circle((x, y), 0.08, linewidth=0, 
                        facecolor='#FFE4B5', alpha=0.6, zorder=1)
    ax.add_patch(fur)

# === TITLE ===
ax.text(0, 4.8, '🐱 Cute Kitten 🐱', fontsize=18, ha='center', 
        fontweight='bold', color='#FF69B4')

# === HEART ===
heart_x = [0, 0.15, 0.3, 0.15, 0, -0.15, -0.3, -0.15, 0]
heart_y = [0.5, 0.65, 0.5, 0.35, 0.2, 0.35, 0.5, 0.65, 0.5]
heart = patches.Polygon(np.column_stack([heart_x, heart_y]), 
                        linewidth=2, edgecolor='#FF1493', 
                        facecolor='#FF1493', alpha=0.7, zorder=8)
ax.add_patch(heart)
ax.text(0, 0.25, '♥', fontsize=12, ha='center', va='center', 
        color='white', fontweight='bold', zorder=9)

plt.tight_layout()
plt.savefig('cute_kitten.png', dpi=300, bbox_inches='tight', 
            facecolor='#FFF8E7', edgecolor='none')
plt.show()
