import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, Arc

# ----- Colors (tweak these to recolor your kitten) -----
FUR    = "#9aa0a6"   # soft gray fur
FUR_LT = "#c5cace"   # lighter belly / muzzle
EAR_IN = "#f7b7c4"   # pink inner ear
NOSE   = "#f48fb1"   # pink nose
EYE    = "#3a3a3a"   # eye color
BG     = "#fdf6ee"   # cream background

fig, ax = plt.subplots(figsize=(6, 7))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

# ----- Tail (thick curved stroke, behind the body) -----
ax.add_patch(Arc((7.2, 1.8), 3.0, 3.0, theta1=-60, theta2=70,
                 lw=18, color=FUR, zorder=0))

# ----- Body + lighter belly -----
ax.add_patch(Ellipse((5, 2.6), 4.2, 4.4, facecolor=FUR, zorder=1))
ax.add_patch(Ellipse((5, 2.0), 2.4, 3.0, facecolor=FUR_LT, zorder=2))

# ----- Front paws -----
for px in (4.0, 6.0):
    ax.add_patch(Ellipse((px, 0.7), 1.1, 0.7, facecolor=FUR_LT, zorder=3))

# ----- Ears (outer triangles + pink inner triangles) -----
ax.add_patch(Polygon([(3.0, 7.1), (3.5, 9.3), (4.6, 7.6)], facecolor=FUR, zorder=2))
ax.add_patch(Polygon([(7.0, 7.1), (6.5, 9.3), (5.4, 7.6)], facecolor=FUR, zorder=2))
ax.add_patch(Polygon([(3.5, 7.3), (3.7, 8.6), (4.3, 7.6)], facecolor=EAR_IN, zorder=3))
ax.add_patch(Polygon([(6.5, 7.3), (6.3, 8.6), (5.7, 7.6)], facecolor=EAR_IN, zorder=3))

# ----- Head + muzzle -----
ax.add_patch(Circle((5, 6), 2.0, facecolor=FUR, zorder=4))
ax.add_patch(Ellipse((5, 5.2), 2.2, 1.6, facecolor=FUR_LT, zorder=5))

# ----- Eyes (white, pupil, highlight) -----
for ex in (4.2, 5.8):
    ax.add_patch(Ellipse((ex, 6.3), 0.7, 1.0, facecolor="white",
                         edgecolor=EYE, lw=1.2, zorder=6))
    ax.add_patch(Ellipse((ex, 6.2), 0.32, 0.7, facecolor=EYE, zorder=7))
    ax.add_patch(Circle((ex - 0.12, 6.5), 0.1, facecolor="white", zorder=8))

# ----- Nose + mouth -----
ax.add_patch(Polygon([(4.8, 5.5), (5.2, 5.5), (5.0, 5.2)], facecolor=NOSE, zorder=7))
ax.plot([5.0, 5.0], [5.2, 5.05], color=EYE, lw=1.4, zorder=7)
ax.add_patch(Arc((4.8, 5.0), 0.5, 0.4, theta1=200, theta2=340, lw=1.6, color=EYE, zorder=7))
ax.add_patch(Arc((5.2, 5.0), 0.5, 0.4, theta1=200, theta2=340, lw=1.6, color=EYE, zorder=7))

# ----- Whiskers (fan out from each cheek) -----
for side in (-1, 1):
    for dy in (0.25, 0.0, -0.25):
        length = 2.4 if dy == 0 else 2.2
        x0, y0 = 5 + side * 0.9, 5.1 + dy
        x1, y1 = 5 + side * (0.9 + length), y0 + dy * 0.6
        ax.plot([x0, x1], [y0, y1], color="#6b6f73", lw=1.0, zorder=6)

# ----- Finish -----
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_aspect("equal")
ax.axis("off")
plt.tight_layout()
plt.show()
