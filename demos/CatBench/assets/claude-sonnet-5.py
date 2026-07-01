import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle, Polygon

# ---------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------
def quad_bezier(p0, p1, p2, n=60):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2 = np.array(p0), np.array(p1), np.array(p2)
    return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2

def cubic_bezier(p0, p1, p2, p3, n=100):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2, p3 = np.array(p0), np.array(p1), np.array(p2), np.array(p3)
    return ((1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 +
             3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3)

def mirror_x(x, axis=5.0):
    return 2 * axis - x

def ellipse_point(center, a, b, r, theta_deg):
    theta = np.radians(theta_deg)
    return (center[0] + r * a * np.cos(theta), center[1] + r * b * np.sin(theta))

# ---------------------------------------------------------------
# Palette
# ---------------------------------------------------------------
fur      = '#F2A65A'
fur_dark = '#C97D3A'
outline  = '#5C3A21'
white    = '#FFFDF8'
pink     = '#F4A7B9'
ink      = '#3A2A20'
bg       = '#FBF3E7'

fig, ax = plt.subplots(figsize=(8, 8))
fig.patch.set_facecolor(bg)
ax.set_facecolor(bg)

# ---------------------------------------------------------------
# Tail (drawn first so the body overlaps its base)
# ---------------------------------------------------------------
tail = cubic_bezier((7.0, 3.0), (9.1, 3.2), (9.5, 5.4), (7.7, 6.1), n=100)
ax.plot(tail[:, 0], tail[:, 1], color=outline, linewidth=26,
        solid_capstyle='round', zorder=0.4)
ax.plot(tail[:, 0], tail[:, 1], color=fur, linewidth=20,
        solid_capstyle='round', zorder=0.5)

# ---------------------------------------------------------------
# Body
# ---------------------------------------------------------------
body_center, body_a, body_b = (5, 3.1), 2.2, 1.7
body = Ellipse(body_center, width=2 * body_a, height=2 * body_b,
               facecolor=fur, edgecolor=outline, linewidth=2.5, zorder=1.0)
ax.add_patch(body)

belly = Ellipse((5, 2.5), width=2.2, height=2.0, facecolor=white,
                 edgecolor='none', zorder=1.1)
ax.add_patch(belly)

for theta_deg in (150, 180, 210):
    p_in = ellipse_point(body_center, body_a, body_b, 0.45, theta_deg)
    p_out = ellipse_point(body_center, body_a, body_b, 0.8, theta_deg)
    ax.plot([p_in[0], p_out[0]], [p_in[1], p_out[1]], color=fur_dark,
            linewidth=5, solid_capstyle='round', zorder=1.05)
    ax.plot([mirror_x(p_in[0]), mirror_x(p_out[0])], [p_in[1], p_out[1]],
            color=fur_dark, linewidth=5, solid_capstyle='round', zorder=1.05)

# ---------------------------------------------------------------
# Front paws
# ---------------------------------------------------------------
for cx in (4.0, 6.0):
    paw = Ellipse((cx, 1.2), width=1.3, height=1.5, facecolor=white,
                   edgecolor=outline, linewidth=2, zorder=1.3)
    ax.add_patch(paw)
    pad = Ellipse((cx, 1.0), width=0.5, height=0.4, facecolor=pink,
                   edgecolor='none', zorder=1.4)
    ax.add_patch(pad)
    for dx in (-0.2, 0.0, 0.2):
        bean = Circle((cx + dx, 1.37), radius=0.09, facecolor=pink,
                       edgecolor='none', zorder=1.4)
        ax.add_patch(bean)

# ---------------------------------------------------------------
# Head
# ---------------------------------------------------------------
head = Ellipse((5, 6.4), width=4.0, height=3.8, facecolor=fur,
               edgecolor=outline, linewidth=2.5, zorder=3.0)
ax.add_patch(head)

# forehead tabby marks
for (x1, y1, x2, y2) in [(5, 8.0, 5, 7.2),
                          (4.35, 7.85, 3.75, 7.1),
                          (5.65, 7.85, 6.25, 7.1)]:
    ax.plot([x1, x2], [y1, y2], color=fur_dark, linewidth=6,
            solid_capstyle='round', zorder=3.05)

# ears (outer)
left_outer = Polygon([(3.3, 7.5), (2.6, 9.6), (4.5, 7.9)], facecolor=fur,
                      edgecolor=outline, linewidth=2.5, zorder=3.1)
right_outer = Polygon([(6.7, 7.5), (7.4, 9.6), (5.5, 7.9)], facecolor=fur,
                       edgecolor=outline, linewidth=2.5, zorder=3.1)
ax.add_patch(left_outer)
ax.add_patch(right_outer)

# ears (inner)
left_inner = Polygon([(3.55, 7.55), (3.05, 9.0), (4.2, 7.85)],
                      facecolor=pink, edgecolor='none', zorder=3.15)
right_inner = Polygon([(6.45, 7.55), (6.95, 9.0), (5.8, 7.85)],
                       facecolor=pink, edgecolor='none', zorder=3.15)
ax.add_patch(left_inner)
ax.add_patch(right_inner)

# muzzle
muzzle = Ellipse((5, 5.5), width=2.0, height=1.5, facecolor=white,
                  edgecolor='none', zorder=3.2)
ax.add_patch(muzzle)

# cheeks
for cx in (3.9, 6.1):
    cheek = Circle((cx, 5.9), radius=0.35, facecolor=pink, alpha=0.55,
                    edgecolor='none', zorder=3.3)
    ax.add_patch(cheek)

# eyes
def draw_eye(cx):
    ax.add_patch(Circle((cx, 6.5), radius=0.55, facecolor=white,
                         edgecolor=outline, linewidth=2, zorder=3.4))
    pupil_x = cx + 0.08 if cx < 5 else cx - 0.08
    ax.add_patch(Circle((pupil_x, 6.45), radius=0.28, facecolor=ink,
                         edgecolor='none', zorder=3.5))
    hl_x = cx + 0.2 if cx < 5 else cx - 0.2
    ax.add_patch(Circle((hl_x, 6.58), radius=0.09, facecolor='white',
                         edgecolor='none', zorder=3.6))

draw_eye(4.1)
draw_eye(5.9)

# nose
nose = Polygon([(4.85, 5.85), (5.15, 5.85), (5.0, 5.65)], facecolor=pink,
               edgecolor=outline, linewidth=1, zorder=3.5)
ax.add_patch(nose)

# mouth
ax.plot([5, 5], [5.65, 5.48], color=outline, linewidth=2.2, zorder=3.5)
left_mouth = quad_bezier((5, 5.48), (4.7, 5.62), (4.35, 5.46))
right_mouth = quad_bezier((5, 5.48), (5.3, 5.62), (5.65, 5.46))
ax.plot(left_mouth[:, 0], left_mouth[:, 1], color=outline, linewidth=2.2,
        solid_capstyle='round', zorder=3.5)
ax.plot(right_mouth[:, 0], right_mouth[:, 1], color=outline, linewidth=2.2,
        solid_capstyle='round', zorder=3.5)

# whiskers
whisker_lines = [
    ((3.7, 6.05), (1.7, 6.35)), ((3.7, 5.85), (1.6, 5.85)), ((3.7, 5.65), (1.7, 5.35)),
    ((6.3, 6.05), (8.3, 6.35)), ((6.3, 5.85), (8.4, 5.85)), ((6.3, 5.65), (8.3, 5.35)),
]
for (x1, y1), (x2, y2) in whisker_lines:
    ax.plot([x1, x2], [y1, y2], color='#6b4a35', linewidth=1.5, zorder=3.7)

# ---------------------------------------------------------------
# Final touches
# ---------------------------------------------------------------
ax.set_xlim(0, 10)
ax.set_ylim(0, 10.3)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('Meow~', fontsize=22, fontweight='bold', color=outline, pad=10)

plt.tight_layout()
plt.savefig('cute_kitten.png', dpi=200, facecolor=fig.get_facecolor())
plt.show()
