import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, Arc, PathPatch
from matplotlib.path import Path


def add(ax, patch):
    ax.add_patch(patch)
    return patch


def draw_curve(ax, points, color, lw=3, zorder=10):
    codes = [Path.MOVETO] + [Path.CURVE3] * (len(points) - 1)
    path = Path(points, codes)
    patch = PathPatch(
        path,
        facecolor="none",
        edgecolor=color,
        lw=lw,
        capstyle="round",
        joinstyle="round",
        zorder=zorder,
    )
    ax.add_patch(patch)
    return patch


# Figure setup
fig, ax = plt.subplots(figsize=(7, 7))
ax.set_aspect("equal")
ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.axis("off")

bg = "#fff7fb"
fur = "#f6c7a6"
fur_dark = "#d8956f"
belly = "#ffe2cf"
outline = "#6b4b3e"
pink = "#ff9fb3"
eye = "#2b1d1a"
white = "#ffffff"

fig.patch.set_facecolor(bg)
ax.set_facecolor(bg)

# Soft shadow
add(
    ax,
    Ellipse(
        (0, -2.75),
        4.5,
        0.45,
        facecolor="#d8b5a5",
        edgecolor="none",
        alpha=0.35,
        zorder=0,
    ),
)

# Tail behind body
tail_points = [
    (1.25, -1.3),
    (2.7, -0.7),
    (2.25, 0.9),
    (1.15, 0.45),
]
draw_curve(ax, tail_points, fur, lw=34, zorder=1)
draw_curve(ax, tail_points, outline, lw=3, zorder=2)

# Tail stripes
for x, y, angle in [(2.25, -0.4, 55), (2.35, 0.25, 20), (1.75, 0.65, -30)]:
    add(
        ax,
        Ellipse(
            (x, y),
            0.55,
            0.12,
            angle=angle,
            facecolor=fur_dark,
            edgecolor="none",
            alpha=0.65,
            zorder=3,
        ),
    )

# Body
add(
    ax,
    Ellipse(
        (0, -1.15),
        3.0,
        2.8,
        facecolor=fur,
        edgecolor=outline,
        linewidth=3,
        zorder=4,
    ),
)

# Belly
add(
    ax,
    Ellipse(
        (0, -1.25),
        1.65,
        2.0,
        facecolor=belly,
        edgecolor="none",
        zorder=5,
    ),
)

# Back feet
for x in [-0.9, 0.9]:
    add(
        ax,
        Ellipse(
            (x, -2.35),
            1.05,
            0.55,
            facecolor=fur,
            edgecolor=outline,
            linewidth=2.5,
            zorder=6,
        ),
    )

# Front paws
for x in [-0.45, 0.45]:
    add(
        ax,
        Ellipse(
            (x, -1.95),
            0.65,
            0.9,
            facecolor=belly,
            edgecolor=outline,
            linewidth=2.2,
            zorder=7,
        ),
    )
    for dx in [-0.12, 0, 0.12]:
        ax.plot(
            [x + dx, x + dx * 1.15],
            [-2.18, -2.35],
            color=outline,
            lw=1.5,
            zorder=8,
        )

# Ears
left_ear = Polygon(
    [(-1.25, 1.85), (-0.65, 3.0), (-0.25, 1.75)],
    closed=True,
    facecolor=fur,
    edgecolor=outline,
    linewidth=3,
    zorder=8,
)
right_ear = Polygon(
    [(1.25, 1.85), (0.65, 3.0), (0.25, 1.75)],
    closed=True,
    facecolor=fur,
    edgecolor=outline,
    linewidth=3,
    zorder=8,
)
add(ax, left_ear)
add(ax, right_ear)

# Inner ears
add(
    ax,
    Polygon(
        [(-1.05, 1.95), (-0.68, 2.65), (-0.45, 1.9)],
        closed=True,
        facecolor=pink,
        edgecolor="none",
        zorder=9,
    ),
)
add(
    ax,
    Polygon(
        [(1.05, 1.95), (0.68, 2.65), (0.45, 1.9)],
        closed=True,
        facecolor=pink,
        edgecolor="none",
        zorder=9,
    ),
)

# Head
add(
    ax,
    Circle(
        (0, 1.15),
        1.45,
        facecolor=fur,
        edgecolor=outline,
        linewidth=3,
        zorder=10,
    ),
)

# Face fluff
for x in [-1.2, 1.2]:
    add(
        ax,
        Circle(
            (x, 0.85),
            0.28,
            facecolor=fur,
            edgecolor=outline,
            linewidth=2,
            zorder=11,
        ),
    )

# Forehead stripes
for x in [-0.45, 0, 0.45]:
    ax.plot(
        [x, x * 0.55],
        [2.35, 1.9],
        color=fur_dark,
        lw=4,
        solid_capstyle="round",
        zorder=12,
    )

# Eyes
for x in [-0.52, 0.52]:
    add(
        ax,
        Circle(
            (x, 1.35),
            0.27,
            facecolor=eye,
            edgecolor=outline,
            linewidth=1.2,
            zorder=13,
        ),
    )
    add(
        ax,
        Circle(
            (x - 0.08, 1.45),
            0.08,
            facecolor=white,
            edgecolor="none",
            zorder=14,
        ),
    )
    add(
        ax,
        Circle(
            (x + 0.08, 1.27),
            0.035,
            facecolor=white,
            edgecolor="none",
            alpha=0.8,
            zorder=14,
        ),
    )

# Blush
for x in [-0.82, 0.82]:
    add(
        ax,
        Ellipse(
            (x, 0.88),
            0.42,
            0.22,
            facecolor=pink,
            edgecolor="none",
            alpha=0.45,
            zorder=12,
        ),
    )

# Nose
add(
    ax,
    Polygon(
        [(-0.14, 1.05), (0.14, 1.05), (0, 0.9)],
        closed=True,
        facecolor="#e86f86",
        edgecolor=outline,
        linewidth=1.5,
        zorder=15,
    ),
)

# Mouth
ax.plot([0, 0], [0.9, 0.78], color=outline, lw=2, zorder=15)
add(
    ax,
    Arc(
        (-0.14, 0.78),
        0.28,
        0.22,
        angle=0,
        theta1=200,
        theta2=360,
        color=outline,
        lw=2,
        zorder=15,
    ),
)
add(
    ax,
    Arc(
        (0.14, 0.78),
        0.28,
        0.22,
        angle=0,
        theta1=180,
        theta2=340,
        color=outline,
        lw=2,
        zorder=15,
    ),
)

# Whiskers
for side in [-1, 1]:
    for y, slope in [(1.05, 0.18), (0.9, 0.03), (0.75, -0.13)]:
        ax.plot(
            [side * 0.22, side * 1.25],
            [y, y + slope],
            color=outline,
            lw=2,
            solid_capstyle="round",
            zorder=14,
        )

# Tiny bow
bow_color = "#ff6fa3"
add(
    ax,
    Polygon(
        [(-0.15, -0.05), (-0.85, 0.25), (-0.85, -0.35)],
        closed=True,
        facecolor=bow_color,
        edgecolor=outline,
        linewidth=2,
        zorder=16,
    ),
)
add(
    ax,
    Polygon(
        [(0.15, -0.05), (0.85, 0.25), (0.85, -0.35)],
        closed=True,
        facecolor=bow_color,
        edgecolor=outline,
        linewidth=2,
        zorder=16,
    ),
)
add(
    ax,
    Circle(
        (0, -0.05),
        0.18,
        facecolor="#ff4f91",
        edgecolor=outline,
        linewidth=2,
        zorder=17,
    ),
)

# Little hearts
for x, y, s in [(-2.7, 2.2, 0.18), (2.8, 1.7, 0.15), (-2.3, -0.3, 0.12)]:
    add(ax, Circle((x - s / 2, y + s / 2), s, facecolor=pink, edgecolor="none", zorder=1))
    add(ax, Circle((x + s / 2, y + s / 2), s, facecolor=pink, edgecolor="none", zorder=1))
    add(
        ax,
        Polygon(
            [(x - s * 1.5, y + s / 2), (x + s * 1.5, y + s / 2), (x, y - s * 1.7)],
            closed=True,
            facecolor=pink,
            edgecolor="none",
            zorder=1,
        ),
    )

plt.tight_layout()
plt.show()