import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, Arc

# ---------- canvas ----------
fig, ax = plt.subplots(figsize=(7, 8))
fig.patch.set_facecolor('#FFF6EA')
ax.set_facecolor('#FFF6EA')
ax.set_xlim(-6, 6)
ax.set_ylim(-7, 7)
ax.set_aspect('equal')
ax.axis('off')

# ---------- palette ----------
FUR      = '#F6A94A'   # orange fur
FUR_DARK = '#D97E1F'   # outlines & stripes
CREAM    = '#FFE9C7'   # chest, muzzle, tail tip
PINK     = '#F87E9F'   # nose, ears, tongue
BLUSH    = '#FFB6C6'
EYE      = '#33231A'
LINE     = '#8C5A22'

def mirror(pts):
    return [(-x, y) for x, y in pts]

# ---------- ground shadow ----------
ax.add_patch(Ellipse((0, -5.55), 5.8, 0.7, fc='#F0DCC0', ec='none', zorder=-1))

# ---------- tail (quadratic Bezier curve) ----------
t = np.linspace(0, 1, 100)
P0, P1, P2 = np.array([2.2, -4.0]), np.array([5.2, -4.8]), np.array([4.4, -0.9])
tail = np.outer((1 - t)**2, P0) + np.outer(2 * (1 - t) * t, P1) + np.outer(t**2, P2)
ax.plot(tail[:, 0], tail[:, 1], color=FUR, lw=22, solid_capstyle='round', zorder=0)
ax.plot(tail[72:, 0], tail[72:, 1], color=CREAM, lw=22, solid_capstyle='round', zorder=0.1)

# ---------- body ----------
ax.add_patch(Ellipse((0, -3.0), 5.6, 4.8, fc=FUR, ec=FUR_DARK, lw=2, zorder=1))
for s in (-1, 1):  # side stripes
    ax.add_patch(Polygon([(s*2.35, -2.3), (s*2.35, -1.8), (s*1.55, -2.05)],
                         fc=FUR_DARK, ec='none', zorder=1.2))
    ax.add_patch(Polygon([(s*2.55, -3.3), (s*2.55, -2.85), (s*1.7, -3.08)],
                         fc=FUR_DARK, ec='none', zorder=1.2))
ax.add_patch(Ellipse((0, -2.7), 2.7, 3.2, fc=CREAM, ec='none', zorder=1.5))  # chest

# ---------- front paws ----------
for s in (-1, 1):
    ax.add_patch(Ellipse((s*1.05, -5.0), 1.45, 1.0, fc=FUR, ec=FUR_DARK, lw=2, zorder=2))
    for dx in (-0.24, 0.24):  # toe lines
        ax.plot([s*1.05 + dx]*2, [-5.42, -5.05], color=FUR_DARK, lw=1.5, zorder=2.1)

# ---------- head ----------
ax.add_patch(Circle((0, 1.5), 3.0, fc=FUR, ec=FUR_DARK, lw=2, zorder=3))

# ---------- ears ----------
left_outer = [(-2.82, 2.53), (-2.30, 5.90), (-0.78, 4.40)]
left_inner = [(-2.45, 3.35), (-2.25, 5.30), (-1.25, 4.60)]
for pts in (left_outer, mirror(left_outer)):
    ax.add_patch(Polygon(pts, fc=FUR, ec=FUR_DARK, lw=2, zorder=3.2))
for pts in (left_inner, mirror(left_inner)):
    ax.add_patch(Polygon(pts, fc=PINK, ec='none', zorder=3.3))

# ---------- forehead stripes ----------
ax.add_patch(Polygon([(-0.25, 4.47), (0.25, 4.47), (0, 3.55)], fc=FUR_DARK, ec='none', zorder=3.4))
for s in (-1, 1):
    ax.add_patch(Polygon([(s*1.05, 4.26), (s*0.6, 4.44), (s*0.8, 3.5)],
                         fc=FUR_DARK, ec='none', zorder=3.4))

# ---------- muzzle ----------
ax.add_patch(Ellipse((0, 0.72), 2.0, 1.35, fc=CREAM, ec='none', zorder=4))

# ---------- big sparkly eyes ----------
for s in (-1, 1):
    ex = 1.15 * s
    ax.add_patch(Circle((ex, 1.95), 0.52, fc=EYE, ec='none', zorder=5))
    ax.add_patch(Circle((ex - 0.15, 2.12), 0.15, fc='white', ec='none', zorder=6))
    ax.add_patch(Circle((ex + 0.12, 1.76), 0.07, fc='white', ec='none', alpha=0.85, zorder=6))

# ---------- blush ----------
for s in (-1, 1):
    ax.add_patch(Ellipse((s*2.1, 1.05), 0.85, 0.5, fc=BLUSH, ec='none', alpha=0.8, zorder=5))

# ---------- nose, mouth, tongue ----------
ax.add_patch(Polygon([(-0.26, 1.02), (0.26, 1.02), (0, 0.64)], fc=PINK, ec='none', zorder=6))
ax.plot([0, 0], [0.64, 0.5], color=LINE, lw=1.8, zorder=6)
ax.add_patch(Ellipse((0, 0.34), 0.34, 0.3, fc=PINK, ec='#E2607E', lw=1, zorder=5.5))
for s in (-1, 1):  # the "w" smile
    ax.add_patch(Arc((s*0.3, 0.5), 0.6, 0.45, theta1=180, theta2=360, color=LINE, lw=1.8, zorder=6))

# ---------- whiskers ----------
whiskers = [((1.05, 0.95), (3.6, 1.35)),
            ((1.05, 0.72), (3.7, 0.70)),
            ((1.05, 0.50), (3.6, 0.10))]
for (x1, y1), (x2, y2) in whiskers:
    for s in (-1, 1):
        ax.plot([s*x1, s*x2], [y1, y2], color='#9B9B9B', lw=1.6, zorder=6)

# ---------- decorations ----------
ax.text(3.8, 4.7, '♥', fontsize=24, color=PINK, ha='center', va='center', zorder=7)
ax.text(-4.1, 2.3, '♥', fontsize=15, color=BLUSH, ha='center', va='center', zorder=7)
ax.text(0, -6.35, 'meow ♥', fontsize=14, color=FUR_DARK, ha='center', style='italic', zorder=7)
ax.text(0, 6.4, '=^.^=', fontsize=20, color=FUR_DARK, ha='center', weight='bold', zorder=7)

plt.tight_layout()
# plt.savefig('kitten.png', dpi=200, bbox_inches='tight')
plt.show()
