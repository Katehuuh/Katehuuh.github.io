import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, PathPatch
from matplotlib.path import Path

# Colors
BG = "#FFF7EF"
FUR = "#D9915B"
FUR_DARK = "#754A38"
FUR_MARK = "#BD744B"
BELLY = "#F7DFC1"
MUZZLE = "#FFF2E2"
PINK = "#E9959B"
EYE = "#49352F"
COLLAR = "#78B9C5"
GOLD = "#F4C965"


def add_curve(ax, points, color, width=2, zorder=1):
    """Add a smooth cubic Bezier curve."""
    codes = [Path.MOVETO] + [Path.CURVE4] * (len(points) - 1)
    path = Path(points, codes)
    ax.add_patch(
        PathPatch(
            path,
            facecolor="none",
            edgecolor=color,
            linewidth=width,
            capstyle="round",
            joinstyle="round",
            zorder=zorder,
        )
    )


def add_sparkle(ax, x, y, size):
    points = [
        (x, y + size),
        (x + size * 0.18, y + size * 0.18),
        (x + size, y),
        (x + size * 0.18, y - size * 0.18),
        (x, y - size),
        (x - size * 0.18, y - size * 0.18),
        (x - size, y),
        (x - size * 0.18, y + size * 0.18),
    ]
    ax.add_patch(
        Polygon(points, closed=True, facecolor=GOLD, edgecolor="none", zorder=0.3)
    )


fig, ax = plt.subplots(figsize=(7, 7))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_aspect("equal")
ax.axis("off")
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

# A couple of little background sparkles
add_sparkle(ax, 1.45, 7.6, 0.20)
add_sparkle(ax, 8.55, 7.85, 0.17)

# Ground shadow
ax.add_patch(
    Ellipse((5, 1.0), 4.4, 0.55, facecolor="#EADAC8", edgecolor="none", zorder=0.5)
)

# Curled tail, drawn behind the kitten
tail = [
    (5.95, 2.0),
    (7.0, 1.05), (8.65, 1.05), (8.55, 2.25),
    (8.48, 3.02), (7.30, 3.26), (7.38, 2.56),
]
add_curve(ax, tail, FUR_DARK, width=28, zorder=1)
add_curve(ax, tail, FUR, width=19, zorder=1.1)

# Body
ax.add_patch(
    Ellipse(
        (5, 3.05), 3.5, 4.0,
        facecolor=FUR, edgecolor=FUR_DARK, linewidth=2.4, zorder=2
    )
)
ax.add_patch(
    Ellipse(
        (5, 3.0), 1.85, 2.55,
        facecolor=BELLY, edgecolor="none", zorder=3
    )
)

# A few subtle tabby marks on the sides
for points in [
    [(3.58, 4.10), (3.85, 3.93), (3.96, 3.77), (3.96, 3.63)],
    [(3.52, 3.68), (3.80, 3.53), (3.91, 3.37), (3.92, 3.23)],
    [(6.42, 4.10), (6.15, 3.93), (6.04, 3.77), (6.04, 3.63)],
    [(6.48, 3.68), (6.20, 3.53), (6.09, 3.37), (6.08, 3.23)],
]:
    add_curve(ax, points, FUR_MARK, width=2.2, zorder=3.2)

# Front paws
for x in (4.42, 5.58):
    ax.add_patch(
        Ellipse(
            (x, 1.55), 1.22, 0.72,
            facecolor=FUR, edgecolor=FUR_DARK, linewidth=2, zorder=4
        )
    )

# Little toe marks
for x in (4.30, 4.58, 5.42, 5.70):
    add_curve(
        ax,
        [(x, 1.46), (x, 1.52), (x, 1.62), (x, 1.68)],
        FUR_DARK,
        width=1.5,
        zorder=4.2,
    )

# Collar and bell
collar = [(3.82, 5.0), (4.12, 4.25), (5.88, 4.25), (6.18, 5.0)]
add_curve(ax, collar, FUR_DARK, width=11, zorder=4.5)
add_curve(ax, collar, COLLAR, width=7, zorder=4.6)
ax.add_patch(
    Circle((5, 4.47), 0.21, facecolor=GOLD, edgecolor=FUR_DARK, linewidth=1.5, zorder=4.8)
)
ax.add_patch(Circle((4.94, 4.54), 0.045, facecolor="white", edgecolor="none", zorder=4.9))

# Ears, behind the head
left_ear = [(3.05, 7.05), (3.22, 9.05), (4.82, 7.95), (4.55, 7.12)]
right_ear = [(5.18, 7.95), (6.78, 9.05), (6.95, 7.05), (5.45, 7.12)]
for points in (left_ear, right_ear):
    ax.add_patch(
        Polygon(points, closed=True, facecolor=FUR, edgecolor=FUR_DARK, linewidth=2.3, zorder=5)
    )

# Pink inner ears
ax.add_patch(
    Polygon(
        [(3.43, 7.60), (3.50, 8.68), (4.34, 8.00)],
        closed=True, facecolor=PINK, edgecolor="none", zorder=5.2
    )
)
ax.add_patch(
    Polygon(
        [(6.57, 7.60), (6.50, 8.68), (5.66, 8.00)],
        closed=True, facecolor=PINK, edgecolor="none", zorder=5.2
    )
)

# Head
ax.add_patch(
    Ellipse(
        (5, 6.45), 4.5, 3.35,
        facecolor=FUR, edgecolor=FUR_DARK, linewidth=2.5, zorder=6
    )
)

# Forehead stripes
for points in [
    [(4.72, 7.78), (4.80, 7.68), (4.88, 7.57), (4.92, 7.48)],
    [(5.00, 7.82), (5.00, 7.70), (5.00, 7.58), (5.00, 7.48)],
    [(5.28, 7.78), (5.20, 7.68), (5.12, 7.57), (5.08, 7.48)],
]:
    add_curve(ax, points, FUR_MARK, width=2.5, zorder=7)

# Blushy cheeks
for x in (3.95, 6.05):
    ax.add_patch(
        Ellipse((x, 5.82), 0.55, 0.28, facecolor=PINK, edgecolor="none", alpha=0.55, zorder=7)
    )

# Whiskers
whiskers = [
    [(4.33, 5.92), (4.02, 6.02), (3.55, 6.10), (3.12, 6.16)],
    [(4.33, 5.78), (3.95, 5.80), (3.53, 5.79), (3.06, 5.78)],
    [(4.34, 5.64), (3.98, 5.55), (3.55, 5.42), (3.16, 5.34)],
]
for points in whiskers:
    add_curve(ax, points, FUR_DARK, width=1.5, zorder=7.2)
    add_curve(ax, [(10 - x, y) for x, y in points], FUR_DARK, width=1.5, zorder=7.2)

# Big shiny eyes
for x in (4.15, 5.85):
    ax.add_patch(
        Ellipse((x, 6.63), 0.29, 0.45, facecolor=EYE, edgecolor="none", zorder=7.5)
    )
    ax.add_patch(Circle((x - 0.045, 6.76), 0.055, facecolor="white", edgecolor="none", zorder=7.6))
    ax.add_patch(Circle((x + 0.055, 6.57), 0.022, facecolor="white", edgecolor="none", zorder=7.6))

# Soft muzzle puffs
for x in (4.72, 5.28):
    ax.add_patch(
        Ellipse((x, 5.78), 0.84, 0.62, facecolor=MUZZLE, edgecolor="none", zorder=7.7)
    )

# Nose and little smile
ax.add_patch(
    Polygon(
        [(4.82, 6.07), (5.18, 6.07), (5.0, 5.85)],
        closed=True, facecolor=PINK, edgecolor="#B95B64", linewidth=1, zorder=8
    )
)
add_curve(ax, [(5.0, 5.86), (5.0, 5.78), (5.0, 5.72), (5.0, 5.68)], FUR_DARK, 2, 8.1)
add_curve(ax, [(5.0, 5.69), (4.91, 5.56), (4.77, 5.56), (4.67, 5.69)], FUR_DARK, 2, 8.1)
add_curve(ax, [(5.0, 5.69), (5.09, 5.56), (5.23, 5.56), (5.33, 5.69)], FUR_DARK, 2, 8.1)

# Tiny freckles
for x, y in [(4.48, 5.82), (4.56, 5.70), (4.64, 5.82),
             (5.52, 5.82), (5.44, 5.70), (5.36, 5.82)]:
    ax.add_patch(Circle((x, y), 0.025, facecolor=FUR_DARK, edgecolor="none", zorder=8.2))

# Uncomment to save a copy:
# fig.savefig("cute_kitten.png", dpi=200, bbox_inches="tight", facecolor=BG)

plt.show()
