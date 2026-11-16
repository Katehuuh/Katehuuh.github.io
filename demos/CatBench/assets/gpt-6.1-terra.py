import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Ellipse, PathPatch, Polygon
from matplotlib.path import Path

# Colors
background = "#fff8ef"
fur = "#f2b675"
cream = "#ffe2b5"
pink = "#ed9a9f"
ink = "#594540"
stripe = "#d58e55"

fig, ax = plt.subplots(figsize=(7, 8), facecolor=background)
ax.set_xlim(-3.8, 3.8)
ax.set_ylim(-4.25, 4.35)
ax.set_aspect("equal")
ax.axis("off")
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

# Shadow
ax.add_patch(Ellipse(
    (0, -3.9), 4.8, 0.35,
    facecolor="#d9c8b4", edgecolor="none", alpha=0.5, zorder=0
))

# Curled tail, drawn with two strokes for an outline
tail = Path(
    [(1.4, -2.55), (2.8, -3.1), (3.6, -2.1), (3.0, -0.95)],
    [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4],
)
for color, width, layer in [(ink, 38, 1), (fur, 30, 2)]:
    ax.add_patch(PathPatch(
        tail, facecolor="none", edgecolor=color, linewidth=width,
        capstyle="round", zorder=layer
    ))

# Body and chest
ax.add_patch(Ellipse(
    (0, -1.6), 3.9, 4.1,
    facecolor=fur, edgecolor=ink, linewidth=3, zorder=3
))
ax.add_patch(Ellipse(
    (0, -1.75), 1.8, 2.45,
    facecolor=cream, edgecolor="none", zorder=4
))

# Ears
for side in (-1, 1):
    outer = [(side * 2.12, 1.8), (side * 2.05, 3.95),
             (side * 0.45, 2.75)]
    inner = [(side * 1.83, 2.55), (side * 1.84, 3.48),
             (side * 0.95, 2.72)]
    ax.add_patch(Polygon(
        outer, closed=True, facecolor=fur, edgecolor=ink,
        linewidth=3, joinstyle="round", zorder=4
    ))
    ax.add_patch(Polygon(
        inner, closed=True, facecolor=pink, edgecolor="none", zorder=5
    ))

# Head and muzzle
ax.add_patch(Ellipse(
    (0, 1.0), 4.65, 3.8,
    facecolor=fur, edgecolor=ink, linewidth=3, zorder=6
))
ax.add_patch(Ellipse(
    (0, 0.65), 1.35, 0.72,
    facecolor=cream, edgecolor="none", zorder=7
))

# Forehead stripes
ax.plot([0, 0], [2.65, 2.28], color=stripe, linewidth=5,
        solid_capstyle="round", zorder=7)
for side in (-1, 1):
    ax.plot([side * 0.42, side * 0.32], [2.57, 2.28],
            color=stripe, linewidth=4.5, solid_capstyle="round", zorder=7)

# Eyes, highlights, cheeks, and whiskers
for side in (-1, 1):
    x = side * 0.85
    ax.add_patch(Ellipse(
        (x, 1.3), 0.56, 0.82,
        facecolor=ink, edgecolor="none", zorder=8
    ))
    ax.add_patch(Circle((x - 0.09, 1.47), 0.10, color="white", zorder=9))
    ax.add_patch(Circle((x + 0.08, 1.16), 0.04, color="white", zorder=9))
    ax.add_patch(Ellipse(
        (side * 1.48, 0.72), 0.6, 0.33,
        facecolor=pink, edgecolor="none", alpha=0.65, zorder=7
    ))
    for start_y, end_y in [(1.0, 1.12), (0.78, 0.75), (0.56, 0.35)]:
        ax.plot([side * 1.58, side * 2.68], [start_y, end_y],
                color=ink, linewidth=1.8, solid_capstyle="round", zorder=8)

# Nose and smiling mouth
ax.add_patch(Polygon(
    [(-0.17, 0.94), (0.17, 0.94), (0, 0.76)],
    closed=True, facecolor="#d97980", edgecolor=ink,
    linewidth=1.5, joinstyle="round", zorder=9
))
ax.plot([0, 0], [0.76, 0.58], color=ink, linewidth=2, zorder=9)
for side in (-1, 1):
    ax.add_patch(Arc(
        (side * 0.23, 0.58), 0.46, 0.34,
        theta1=180, theta2=360, edgecolor=ink, linewidth=2, zorder=9
    ))

# Paws and toes
for x in (-0.95, 0.95):
    ax.add_patch(Ellipse(
        (x, -3.4), 1.5, 0.85,
        facecolor=cream, edgecolor=ink, linewidth=2.5, zorder=8
    ))
    for offset in (-0.2, 0.2):
        ax.plot([x + offset, x + offset], [-3.56, -3.42],
                color=ink, linewidth=1.5, solid_capstyle="round", zorder=9)

# A little heart
heart = Path(
    [(2.9, 2.55), (2.62, 2.9), (2.3, 2.49), (2.9, 2.14),
     (3.5, 2.49), (3.18, 2.9), (2.9, 2.55), (2.9, 2.55)],
    [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4,
     Path.CURVE4, Path.CURVE4, Path.CURVE4, Path.CLOSEPOLY],
)
ax.add_patch(PathPatch(heart, facecolor=pink, edgecolor="none", zorder=1))

# Uncomment to save the picture:
# fig.savefig("kitten.png", dpi=200, facecolor=fig.get_facecolor())
plt.show()
