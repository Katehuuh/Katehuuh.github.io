import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, PathPatch
from matplotlib.path import Path

fig, ax = plt.subplots(figsize=(7, 7))
fig.patch.set_facecolor("#fff9f2")
ax.set_facecolor("#fff9f2")

fur = "#f3c69b"
outline = "#765b53"
pink = "#f4a7ac"

# Curly tail, drawn behind the kitten
tail_points = [(1.7, -2.3), (3.7, -2.8), (4.5, -0.8), (3.4, -0.5)]
tail_codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
tail = Path(tail_points, tail_codes)
ax.add_patch(PathPatch(tail, fill=False, edgecolor=outline, lw=24, capstyle="round"))
ax.add_patch(PathPatch(tail, fill=False, edgecolor=fur, lw=19, capstyle="round"))

# Body and belly
ax.add_patch(Ellipse((0, -1.5), 3.8, 4.0, facecolor=fur, edgecolor=outline, lw=3))
ax.add_patch(Ellipse((0, -1.8), 2.2, 2.8, facecolor="#ffe9d5", edgecolor="none"))

# Ears, behind the head
for side in (-1, 1):
    ax.add_patch(Polygon(
        [(side * 1.15, 2.8), (side * 2.25, 4.7), (side * 2.6, 2.25)],
        closed=True, facecolor=fur, edgecolor=outline, lw=3, joinstyle="round"
    ))
    ax.add_patch(Polygon(
        [(side * 1.55, 2.9), (side * 2.2, 4.15), (side * 2.35, 2.65)],
        closed=True, facecolor=pink, edgecolor="none"
    ))

# Head
ax.add_patch(Ellipse((0, 1.35), 5.2, 4.25, facecolor=fur, edgecolor=outline, lw=3))

# Forehead stripes
for x in (-0.65, 0, 0.65):
    ax.plot([x * 1.2, x], [3.3, 2.8], color="#d99d78", lw=4, solid_capstyle="round")

# Eyes and highlights
for x in (-1.05, 1.05):
    ax.add_patch(Ellipse((x, 1.75), 0.55, 0.8, facecolor=outline))
    ax.add_patch(Circle((x - 0.12, 1.95), 0.11, facecolor="white"))
    ax.add_patch(Ellipse((x * 1.75, 1.05), 0.55, 0.25,
                         facecolor=pink, alpha=0.65, edgecolor="none"))

# Nose and smiling mouth
ax.add_patch(Polygon([(-0.2, 1.05), (0.2, 1.05), (0, 0.83)],
                     closed=True, facecolor=pink, edgecolor=outline, lw=1.5))
ax.plot([0, 0], [0.83, 0.65], color=outline, lw=2)

for side in (-1, 1):
    smile = Path(
        [(0, 0.65), (side * 0.23, 0.35), (side * 0.55, 0.48)],
        [Path.MOVETO, Path.CURVE3, Path.CURVE3]
    )
    ax.add_patch(PathPatch(smile, fill=False, edgecolor=outline, lw=2.2,
                           capstyle="round"))
    for y, slope in [(0.95, 0.25), (0.7, 0), (0.45, -0.25)]:
        ax.plot([side * 1.45, side * 2.65],
                [y, y + slope], color=outline, lw=1.8, solid_capstyle="round")

# Paws
for x in (-1.05, 1.05):
    ax.add_patch(Ellipse((x, -3.05), 1.35, 0.9,
                         facecolor=fur, edgecolor=outline, lw=2.5))
    for offset in (-0.2, 0.2):
        ax.plot([x + offset, x + offset], [-3.35, -3.17],
                color=outline, lw=1.5)

ax.set_xlim(-4.5, 5)
ax.set_ylim(-3.8, 5.2)
ax.set_aspect("equal")
ax.axis("off")
plt.tight_layout()
plt.show()
