import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.path import Path
import numpy as np

# Set up the canvas
fig, ax = plt.subplots(figsize=(9, 9), facecolor="#FFF9F5")
ax.set_facecolor("#FFF9F5")
ax.set_xlim(-4.6, 4.6)
ax.set_ylim(-4.6, 4.6)
ax.set_aspect("equal")
ax.axis("off")

# -------------------------------------------------------------
# 0. Background Decorative Elements
# -------------------------------------------------------------
# Soft pastel halo backdrop
halo_bg = patches.Circle(
    (0, -0.1), 4.2, facecolor="#FFF2E6", edgecolor="none", zorder=0
)
halo_border = patches.Circle(
    (0, -0.1),
    4.2,
    facecolor="none",
    edgecolor="#F7D6C8",
    lw=3,
    linestyle="--",
    zorder=0,
)
ax.add_patch(halo_bg)
ax.add_patch(halo_border)


# Helper: Draw smooth cartoon hearts
def draw_heart(ax, cx, cy, size, color, alpha=0.85):
    t = np.linspace(0, 2 * np.pi, 100)
    hx = 16 * np.sin(t) ** 3
    hy = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
    hx = hx / 17.0 * size + cx
    hy = hy / 17.0 * size + cy
    ax.fill(hx, hy, color=color, alpha=alpha, zorder=1)


# Helper: Draw sparkling stars
def draw_sparkle(ax, cx, cy, size, color="#FFD166", alpha=0.9):
    s = size
    w = size * 0.22
    star_x = [cx, cx + w, cx + s, cx + w, cx, cx - w, cx - s, cx - w]
    star_y = [cy + s, cy + w, cy, cy - w, cy - s, cy - w, cy, cy + w]
    ax.fill(star_x, star_y, color=color, alpha=alpha, zorder=1)


# Floating hearts & sparkles
draw_heart(ax, -3.1, 2.6, 0.42, "#FF758F", 0.8)
draw_heart(ax, -3.6, 1.8, 0.26, "#FFAAC1", 0.75)
draw_heart(ax, 3.1, 2.7, 0.40, "#FF758F", 0.8)

draw_sparkle(ax, 3.2, 1.5, 0.35, "#FFD166")
draw_sparkle(ax, -3.2, -0.8, 0.30, "#FFD166")
draw_sparkle(ax, 3.3, -1.2, 0.28, "#FFD166")
draw_sparkle(ax, 0.0, 3.8, 0.32, "#FFD166")
draw_sparkle(ax, -2.6, 3.5, 0.22, "#FFE3A8")
draw_sparkle(ax, 2.6, 3.5, 0.22, "#FFE3A8")

# Floating soft pastel bubbles
bubbles = [
    (-2.4, 3.0, 0.14),
    (2.4, 3.0, 0.14),
    (-3.4, 0.3, 0.16),
    (3.4, 0.3, 0.16),
    (-3.2, -2.2, 0.14),
    (3.2, -2.3, 0.14),
    (-1.8, -3.9, 0.12),
    (1.8, -3.9, 0.12),
]
for bx, by, br in bubbles:
    ax.add_patch(
        patches.Circle((bx, by), br, facecolor="#FFDAC1", alpha=0.55, zorder=1)
    )
    ax.add_patch(
        patches.Circle(
            (bx - br * 0.35, by + br * 0.35),
            br * 0.28,
            facecolor="white",
            alpha=0.85,
            zorder=2,
        )
    )

# -------------------------------------------------------------
# 1. Tail (Curled up fluffily on the right)
# -------------------------------------------------------------
tail_path = Path(
    [
        (0.8, -2.6),
        (2.4, -2.8),
        (3.6, -1.8),
        (3.6, -0.4),
        (3.6, 0.5),
        (2.9, 0.7),
        (2.3, 0.3),
    ],
    [
        Path.MOVETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
    ],
)
tail_patch = patches.PathPatch(
    tail_path,
    facecolor="none",
    edgecolor="#EAA058",
    lw=36,
    capstyle="round",
    joinstyle="round",
    zorder=2,
)
ax.add_patch(tail_patch)

# White tip of the tail
tail_tip_path = Path(
    [(3.3, 0.45), (3.0, 0.65), (2.7, 0.62), (2.3, 0.3)],
    [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4],
)
tail_tip_patch = patches.PathPatch(
    tail_tip_path,
    facecolor="none",
    edgecolor="#FFFDF8",
    lw=36,
    capstyle="round",
    joinstyle="round",
    zorder=3,
)
ax.add_patch(tail_tip_patch)

# -------------------------------------------------------------
# 2. Body & Paws
# -------------------------------------------------------------
# Plump flanks & main torso
left_flank = patches.Ellipse(
    (-1.6, -2.2), 2.2, 2.4, angle=20, facecolor="#EAA058", zorder=4
)
right_flank = patches.Ellipse(
    (1.6, -2.2), 2.2, 2.4, angle=-20, facecolor="#EAA058", zorder=4
)
torso = patches.Ellipse(
    (0.0, -1.8), 3.2, 3.4, facecolor="#EAA058", edgecolor="none", zorder=4
)
ax.add_patch(left_flank)
ax.add_patch(right_flank)
ax.add_patch(torso)

# Fluffy white belly/chest bib
belly = patches.Ellipse(
    (0.0, -1.75), 2.2, 2.6, facecolor="#FFFDF8", zorder=5
)
ax.add_patch(belly)

# Back paws peeking from behind
ax.add_patch(
    patches.Ellipse(
        (-2.0, -3.1),
        1.0,
        0.7,
        angle=-10,
        facecolor="#FFFDF8",
        edgecolor="#D48446",
        lw=2,
        zorder=4,
    )
)
ax.add_patch(
    patches.Ellipse(
        (2.0, -3.1),
        1.0,
        0.7,
        angle=10,
        facecolor="#FFFDF8",
        edgecolor="#D48446",
        lw=2,
        zorder=4,
    )
)

# Cute front paws resting side by side
ax.add_patch(
    patches.Ellipse(
        (-0.75, -3.15),
        1.05,
        0.8,
        facecolor="#FFFDF8",
        edgecolor="#D48446",
        lw=2,
        zorder=6,
    )
)
ax.add_patch(
    patches.Ellipse(
        (0.75, -3.15),
        1.05,
        0.8,
        facecolor="#FFFDF8",
        edgecolor="#D48446",
        lw=2,
        zorder=6,
    )
)

# Toe divider lines
for px in [-0.75, 0.75]:
    ax.plot(
        [px - 0.16, px - 0.16],
        [-3.3, -3.0],
        color="#D48446",
        lw=2,
        solid_capstyle="round",
        zorder=7,
    )
    ax.plot(
        [px + 0.16, px + 0.16],
        [-3.3, -3.0],
        color="#D48446",
        lw=2,
        solid_capstyle="round",
        zorder=7,
    )

# -------------------------------------------------------------
# 3. Ears (Outer, Inner Pink, and Fluffy Tufts)
# -------------------------------------------------------------
# Left outer ear
left_ear = Path(
    [
        (-0.5, 1.8),
        (-1.3, 3.4),
        (-2.2, 3.2),
        (-2.4, 2.2),
        (-2.0, 1.0),
        (-0.5, 1.8),
    ],
    [
        Path.MOVETO,
        Path.CURVE3,
        Path.CURVE3,
        Path.CURVE3,
        Path.CURVE3,
        Path.CLOSEPOLY,
    ],
)
ax.add_patch(
    patches.PathPatch(
        left_ear, facecolor="#EAA058", edgecolor="#D48446", lw=1.5, zorder=8
    )
)

# Right outer ear
right_ear = Path(
    [(0.5, 1.8), (1.3, 3.4), (2.2, 3.2), (2.4, 2.2), (2.0, 1.0), (0.5, 1.8)],
    [
        Path.MOVETO,
        Path.CURVE3,
        Path.CURVE3,
        Path.CURVE3,
        Path.CURVE3,
        Path.CLOSEPOLY,
    ],
)
ax.add_patch(
    patches.PathPatch(
        right_ear, facecolor="#EAA058", edgecolor="#D48446", lw=1.5, zorder=8
    )
)

# Inner pink ears
left_inner = Path(
    [
        (-0.7, 1.8),
        (-1.3, 3.0),
        (-2.0, 2.9),
        (-2.1, 2.0),
        (-1.8, 1.2),
        (-0.7, 1.8),
    ],
    [
        Path.MOVETO,
        Path.CURVE3,
        Path.CURVE3,
        Path.CURVE3,
        Path.CURVE3,
        Path.CLOSEPOLY,
    ],
)
ax.add_patch(
    patches.PathPatch(left_inner, facecolor="#FFB8B8", edgecolor="none", zorder=9)
)

right_inner = Path(
    [(0.7, 1.8), (1.3, 3.0), (2.0, 2.9), (2.1, 2.0), (1.8, 1.2), (0.7, 1.8)],
    [
        Path.MOVETO,
        Path.CURVE3,
        Path.CURVE3,
        Path.CURVE3,
        Path.CURVE3,
        Path.CLOSEPOLY,
    ],
)
ax.add_patch(
    patches.PathPatch(right_inner, facecolor="#FFB8B8", edgecolor="none", zorder=9)
)

# Soft ear fluff tufts
ax.add_patch(
    patches.Polygon(
        [(-0.9, 1.7), (-1.4, 2.3), (-1.2, 1.6)], facecolor="#FFFDF8", zorder=9
    )
)
ax.add_patch(
    patches.Polygon(
        [(-1.3, 1.6), (-1.8, 2.1), (-1.6, 1.4)], facecolor="#FFFDF8", zorder=9
    )
)
ax.add_patch(
    patches.Polygon(
        [(0.9, 1.7), (1.4, 2.3), (1.2, 1.6)], facecolor="#FFFDF8", zorder=9
    )
)
ax.add_patch(
    patches.Polygon(
        [(1.3, 1.6), (1.8, 2.1), (1.6, 1.4)], facecolor="#FFFDF8", zorder=9
    )
)

# -------------------------------------------------------------
# 4. Head & Chubby Cheeks
# -------------------------------------------------------------
# Main head base
head_base = patches.Ellipse(
    (0.0, 0.75), 4.6, 3.8, facecolor="#EAA058", zorder=10
)
ax.add_patch(head_base)

# Chubby cheek expansions
left_cheek = patches.Ellipse(
    (-1.9, 0.35), 1.6, 1.5, angle=25, facecolor="#EAA058", zorder=10
)
right_cheek = patches.Ellipse(
    (1.9, 0.35), 1.6, 1.5, angle=-25, facecolor="#EAA058", zorder=10
)
ax.add_patch(left_cheek)
ax.add_patch(right_cheek)

# Fur spikes on cheeks for extra cuteness
ax.add_patch(
    patches.Polygon(
        [(-2.3, 0.7), (-2.85, 0.45), (-2.1, 0.15)],
        facecolor="#EAA058",
        zorder=10,
    )
)
ax.add_patch(
    patches.Polygon(
        [(-2.1, 0.25), (-2.7, -0.05), (-1.8, -0.15)],
        facecolor="#EAA058",
        zorder=10,
    )
)
ax.add_patch(
    patches.Polygon(
        [(2.3, 0.7), (2.85, 0.45), (2.1, 0.15)], facecolor="#EAA058", zorder=10
    )
)
ax.add_patch(
    patches.Polygon(
        [(2.1, 0.25), (2.7, -0.05), (1.8, -0.15)], facecolor="#EAA058", zorder=10
    )
)

# White muzzle & forehead blaze
muzzle = patches.Ellipse((0.0, 0.15), 2.7, 1.9, facecolor="#FFFDF8", zorder=11)
blaze = patches.Ellipse((0.0, 0.55), 1.3, 1.8, facecolor="#FFFDF8", zorder=11)
ax.add_patch(muzzle)
ax.add_patch(blaze)

# Tabby stripes on forehead
ax.add_patch(
    patches.Polygon(
        [(-0.14, 2.35), (0.14, 2.35), (0.07, 1.55), (-0.07, 1.55)],
        facecolor="#C46B23",
        zorder=12,
    )
)
ax.add_patch(
    patches.Polygon(
        [(-0.6, 2.2), (-0.35, 2.25), (-0.38, 1.6), (-0.55, 1.6)],
        facecolor="#C46B23",
        zorder=12,
    )
)
ax.add_patch(
    patches.Polygon(
        [(0.6, 2.2), (0.35, 2.25), (0.38, 1.6), (0.55, 1.6)],
        facecolor="#C46B23",
        zorder=12,
    )
)

# Side cheek stripes
ax.add_patch(
    patches.Polygon(
        [(-2.2, 0.65), (-1.65, 0.55), (-1.7, 0.45), (-2.25, 0.52)],
        facecolor="#C46B23",
        zorder=12,
    )
)
ax.add_patch(
    patches.Polygon(
        [(-2.1, 0.35), (-1.6, 0.28), (-1.63, 0.18), (-2.15, 0.22)],
        facecolor="#C46B23",
        zorder=12,
    )
)
ax.add_patch(
    patches.Polygon(
        [(2.2, 0.65), (1.65, 0.55), (1.7, 0.45), (2.25, 0.52)],
        facecolor="#C46B23",
        zorder=12,
    )
)
ax.add_patch(
    patches.Polygon(
        [(2.1, 0.35), (1.6, 0.28), (1.63, 0.18), (2.15, 0.22)],
        facecolor="#C46B23",
        zorder=12,
    )
)

# Soft pink blushing cheeks
ax.add_patch(
    patches.Ellipse(
        (-1.55, 0.25), 0.7, 0.42, facecolor="#FF85A1", alpha=0.45, zorder=12
    )
)
ax.add_patch(
    patches.Ellipse(
        (1.55, 0.25), 0.7, 0.42, facecolor="#FF85A1", alpha=0.45, zorder=12
    )
)
# Kawaii blush sparkle dots
ax.plot(
    [-1.6, -1.4],
    [0.28, 0.22],
    "o",
    color="white",
    ms=3.5,
    alpha=0.85,
    zorder=13,
)
ax.plot(
    [1.4, 1.6], [0.22, 0.28], "o", color="white", ms=3.5, alpha=0.85, zorder=13
)

# -------------------------------------------------------------
# 5. Expressive Glossy Anime Eyes
# -------------------------------------------------------------
eye_xs = [-1.15, 1.15]
for x in eye_xs:
    # 1. Dark eyeliner socket
    ax.add_patch(
        patches.Ellipse((x, 0.85), 1.08, 1.28, facecolor="#1A120B", zorder=14)
    )

    # 2. Outer deep ocean teal
    ax.add_patch(
        patches.Ellipse((x, 0.83), 0.98, 1.16, facecolor="#004E64", zorder=15)
    )

    # 3. Mid vibrant turquoise
    ax.add_patch(
        patches.Ellipse((x, 0.78), 0.90, 0.98, facecolor="#00A5CF", zorder=16)
    )

    # 4. Lower radiant mint crescent
    ax.add_patch(
        patches.Ellipse((x, 0.66), 0.76, 0.65, facecolor="#25A18E", zorder=17)
    )

    # 5. Light green reflection glow
    ax.add_patch(
        patches.Ellipse(
            (x, 0.58), 0.55, 0.38, facecolor="#7AE582", alpha=0.75, zorder=18
        )
    )

    # 6. Large black pupil
    ax.add_patch(
        patches.Ellipse((x, 0.85), 0.52, 0.74, facecolor="#0D1B2A", zorder=19)
    )

    # 7. Catchlights (Big & secondary shine for lifelike gloss)
    ax.add_patch(
        patches.Circle((x + 0.16, 1.05), 0.18, facecolor="#FFFFFF", zorder=20)
    )
    ax.add_patch(
        patches.Circle(
            (x - 0.20, 0.65), 0.10, facecolor="#FFFFFF", alpha=0.9, zorder=20
        )
    )
    ax.add_patch(
        patches.Circle(
            (x + 0.22, 0.78), 0.05, facecolor="#FFFFFF", alpha=0.85, zorder=20
        )
    )

# Sweet little eyelashes on the outer corners
ax.add_patch(
    patches.Polygon(
        [(-1.6, 1.25), (-1.8, 1.45), (-1.4, 1.35)],
        facecolor="#1A120B",
        zorder=15,
    )
)
ax.add_patch(
    patches.Polygon(
        [(1.6, 1.25), (1.8, 1.45), (1.4, 1.35)], facecolor="#1A120B", zorder=15
    )
)

# -------------------------------------------------------------
# 6. Nose, Tiny Tongue (Blep), and ":3" Mouth
# -------------------------------------------------------------
# Soft pink nose
nose = patches.Polygon(
    [(-0.16, 0.40), (0.16, 0.40), (0.0, 0.22)],
    facecolor="#FF758F",
    edgecolor="#E05770",
    lw=1,
    zorder=22,
)
ax.add_patch(nose)
ax.add_patch(
    patches.Circle(
        (0.04, 0.36), 0.035, facecolor="#FFFFFF", alpha=0.85, zorder=23
    )
)

# Tiny playful pink tongue (blep)
tongue = patches.Polygon(
    [(-0.10, 0.08), (0.10, 0.08), (0.09, -0.04), (0.0, -0.10), (-0.09, -0.04)],
    facecolor="#FF8DA1",
    edgecolor="#E05770",
    lw=1.5,
    zorder=21,
)
ax.add_patch(tongue)
ax.plot([0.0, 0.0], [0.06, -0.04], color="#E05770", lw=1.2, zorder=21)

# Cat ":3" mouth lines
philtrum = ax.plot(
    [0.0, 0.0],
    [0.22, 0.12],
    color="#3A2312",
    lw=2.2,
    solid_capstyle="round",
    zorder=22,
)
left_mouth = Path(
    [(0.0, 0.12), (-0.22, -0.06), (-0.46, 0.08)],
    [Path.MOVETO, Path.CURVE3, Path.CURVE3],
)
right_mouth = Path(
    [(0.0, 0.12), (0.22, -0.06), (0.46, 0.08)],
    [Path.MOVETO, Path.CURVE3, Path.CURVE3],
)
ax.add_patch(
    patches.PathPatch(
        left_mouth,
        facecolor="none",
        edgecolor="#3A2312",
        lw=2.2,
        capstyle="round",
        zorder=22,
    )
)
ax.add_patch(
    patches.PathPatch(
        right_mouth,
        facecolor="none",
        edgecolor="#3A2312",
        lw=2.2,
        capstyle="round",
        zorder=22,
    )
)

# -------------------------------------------------------------
# 7. Graceful Whiskers
# -------------------------------------------------------------
whisker_data = [
    # Left whiskers
    [(-1.0, 0.22), (-2.0, 0.42), (-3.2, 0.52)],
    [(-1.05, 0.12), (-2.1, 0.15), (-3.4, 0.16)],
    [(-1.0, 0.02), (-2.0, -0.12), (-3.1, -0.22)],
    # Right whiskers
    [(1.0, 0.22), (2.0, 0.42), (3.2, 0.52)],
    [(1.05, 0.12), (2.1, 0.15), (3.4, 0.16)],
    [(1.0, 0.02), (2.0, -0.12), (3.1, -0.22)],
]
for pts in whisker_data:
    w_path = Path(pts, [Path.MOVETO, Path.CURVE3, Path.CURVE3])
    ax.add_patch(
        patches.PathPatch(
            w_path,
            facecolor="none",
            edgecolor="#5C4033",
            lw=1.8,
            capstyle="round",
            alpha=0.65,
            zorder=23,
        )
    )

# -------------------------------------------------------------
# 8. Collar with Red Bow Tie & Golden Bell
# -------------------------------------------------------------
# Red collar strap
collar_path = Path(
    [(-1.2, -0.65), (0.0, -1.0), (1.2, -0.65)],
    [Path.MOVETO, Path.CURVE3, Path.CURVE3],
)
ax.add_patch(
    patches.PathPatch(
        collar_path,
        facecolor="none",
        edgecolor="#E63946",
        lw=8,
        capstyle="round",
        zorder=8,
    )
)

# Cute red bow tie loops behind the bell
ax.add_patch(
    patches.Ellipse(
        (-0.32, -0.92),
        0.45,
        0.28,
        angle=25,
        facecolor="#E63946",
        edgecolor="#BA181B",
        lw=1.5,
        zorder=8,
    )
)
ax.add_patch(
    patches.Ellipse(
        (0.32, -0.92),
        0.45,
        0.28,
        angle=-25,
        facecolor="#E63946",
        edgecolor="#BA181B",
        lw=1.5,
        zorder=8,
    )
)
ax.add_patch(
    patches.Polygon(
        [(-0.15, -0.95), (-0.38, -1.45), (-0.05, -1.2)],
        facecolor="#E63946",
        edgecolor="#BA181B",
        lw=1,
        zorder=8,
    )
)
ax.add_patch(
    patches.Polygon(
        [(0.15, -0.95), (0.38, -1.45), (0.05, -1.2)],
        facecolor="#E63946",
        edgecolor="#BA181B",
        lw=1,
        zorder=8,
    )
)

# Golden bell
ax.add_patch(patches.Circle((0, -0.95), 0.07, facecolor="#B58300", zorder=8))
ax.add_patch(
    patches.Circle(
        (0, -1.08),
        0.22,
        facecolor="#FFD166",
        edgecolor="#B58300",
        lw=1.6,
        zorder=9,
    )
)
ax.plot([-0.14, 0.14], [-1.14, -1.14], color="#7F5539", lw=1.8, zorder=10)
ax.add_patch(patches.Circle((0, -1.14), 0.04, facecolor="#7F5539", zorder=10))
ax.add_patch(
    patches.Circle(
        (-0.06, -1.02), 0.05, facecolor="#FFFFFF", alpha=0.85, zorder=10
    )
)

# Display the masterpiece!
plt.tight_layout()
plt.show()
