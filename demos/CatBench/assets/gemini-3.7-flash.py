import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np


def draw_cute_kitten():
    # Setup canvas
    fig, ax = plt.subplots(figsize=(8, 8), facecolor="#FFFDF9")
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect("equal")
    ax.axis("off")

    # --- Color Palette ---
    FUR_MAIN = "#FFAE5D"  # Warm ginger fur
    FUR_DARK = "#E68936"  # Tabby stripes / shadows
    FUR_LIGHT = "#FFF2E2"  # Cream fur (tummy, snout, paw tips)
    PINK_NOSE = "#FF8DA1"  # Soft nose pink
    PINK_BLUSH = "#FFAAA6"  # Cheek blush
    PINK_EAR = "#FFB6C1"  # Inner ear pink
    EYE_COLOR = "#231F20"  # Deep dark eye
    COLLAR_RED = "#FF4B4B"  # Collar band
    BELL_GOLD = "#FFD13B"  # Collar bell
    WHISKER_CLR = "#543825"  # Whisker brown

    # ==========================================
    # 1. TAIL (Curved Bezier behind the body)
    # ==========================================
    t = np.linspace(0, 1, 100)
    p0 = np.array([1.2, -2.5])
    p1 = np.array([3.4, -2.6])
    p2 = np.array([3.8, -0.4])
    p3 = np.array([2.9, 0.7])
    tail = (
        (1 - t) ** 3 * p0[:, None]
        + 3 * (1 - t) ** 2 * t * p1[:, None]
        + 3 * (1 - t) * t**2 * p2[:, None]
        + t**3 * p3[:, None]
    )

    # Shadow/Outline & Tail Body
    ax.plot(
        tail[0],
        tail[1],
        color=FUR_MAIN,
        lw=24,
        solid_capstyle="round",
        zorder=1,
    )
    ax.plot(
        tail[0][-25:],
        tail[1][-25:],
        color=FUR_LIGHT,
        lw=20,
        solid_capstyle="round",
        zorder=1.1,
    )  # Tail tip

    # ==========================================
    # 2. BODY & TUMMY
    # ==========================================
    # Main Body
    body = patches.Ellipse(
        (0, -1.8),
        3.5,
        3.2,
        angle=0,
        facecolor=FUR_MAIN,
        edgecolor=FUR_DARK,
        lw=2,
        zorder=2,
    )
    ax.add_patch(body)

    # Cream Tummy
    tummy = patches.Ellipse(
        (0, -1.9), 2.3, 2.3, angle=0, facecolor=FUR_LIGHT, zorder=2.1
    )
    ax.add_patch(tummy)

    # ==========================================
    # 3. EARS & HEAD BASE
    # ==========================================
    # Outer Ears (Polygons)
    left_ear_pts = np.array([[-2.2, 0.8], [-2.6, 2.9], [-0.5, 1.8]])
    right_ear_pts = np.array([[2.2, 0.8], [2.6, 2.9], [0.5, 1.8]])

    ax.add_patch(
        patches.Polygon(
            left_ear_pts,
            closed=True,
            facecolor=FUR_MAIN,
            edgecolor=FUR_DARK,
            lw=2,
            zorder=3,
        )
    )
    ax.add_patch(
        patches.Polygon(
            right_ear_pts,
            closed=True,
            facecolor=FUR_MAIN,
            edgecolor=FUR_DARK,
            lw=2,
            zorder=3,
        )
    )

    # Inner Pink Ears
    left_inner_ear = np.array([[-2.0, 1.0], [-2.3, 2.5], [-0.8, 1.7]])
    right_inner_ear = np.array([[2.0, 1.0], [2.3, 2.5], [0.8, 1.7]])

    ax.add_patch(
        patches.Polygon(
            left_inner_ear, closed=True, facecolor=PINK_EAR, zorder=3.1
        )
    )
    ax.add_patch(
        patches.Polygon(
            right_inner_ear, closed=True, facecolor=PINK_EAR, zorder=3.1
        )
    )

    # Head (Chubby wide ellipse)
    head = patches.Ellipse(
        (0, 0.5),
        4.6,
        3.6,
        angle=0,
        facecolor=FUR_MAIN,
        edgecolor=FUR_DARK,
        lw=2,
        zorder=4,
    )
    ax.add_patch(head)

    # Cheek Fluff Tufts
    left_tuft = np.array([[-2.2, 0.3], [-2.7, 0.2], [-2.0, -0.2]])
    right_tuft = np.array([[2.2, 0.3], [2.7, 0.2], [2.0, -0.2]])
    ax.add_patch(
        patches.Polygon(left_tuft, closed=True, facecolor=FUR_MAIN, zorder=4.1)
    )
    ax.add_patch(
        patches.Polygon(right_tuft, closed=True, facecolor=FUR_MAIN, zorder=4.1)
    )

    # ==========================================
    # 4. TABBY STRIPES (Forehead)
    # ==========================================
    ax.add_patch(
        patches.Polygon(
            [[-0.15, 2.0], [0, 1.3], [0.15, 2.0]],
            closed=True,
            facecolor=FUR_DARK,
            zorder=4.2,
        )
    )
    ax.add_patch(
        patches.Polygon(
            [[-0.6, 1.9], [-0.4, 1.35], [-0.35, 1.9]],
            closed=True,
            facecolor=FUR_DARK,
            zorder=4.2,
        )
    )
    ax.add_patch(
        patches.Polygon(
            [[0.6, 1.9], [0.4, 1.35], [0.35, 1.9]],
            closed=True,
            facecolor=FUR_DARK,
            zorder=4.2,
        )
    )

    # ==========================================
    # 5. FACE (Snout, Eyes, Blush, Whiskers)
    # ==========================================
    # Cream Snout / Muzzle Area
    snout = patches.Ellipse(
        (0, 0.05), 1.9, 1.2, angle=0, facecolor=FUR_LIGHT, zorder=4.3
    )
    ax.add_patch(snout)

    # Big Kawaii Eyes
    eye_y = 0.6
    eye_x_dist = 1.15
    eye_rad = 0.52

    for side in [-1, 1]:
        ex = side * eye_x_dist
        # Dark Eyeball
        ax.add_patch(
            patches.Circle((ex, eye_y), eye_rad, facecolor=EYE_COLOR, zorder=5)
        )
        # Iris subtle teal highlight at bottom
        ax.add_patch(
            patches.Arc(
                (ex, eye_y - 0.1),
                0.7,
                0.5,
                angle=0,
                theta1=200,
                theta2=340,
                color="#50C8B4",
                lw=3,
                zorder=5.1,
            )
        )
        # Big Main Glint (top-left on both eyes)
        ax.add_patch(
            patches.Circle(
                (ex - 0.14, eye_y + 0.16), 0.18, facecolor="white", zorder=5.2
            )
        )
        # Small Sparkle (bottom-right)
        ax.add_patch(
            patches.Circle(
                (ex + 0.16, eye_y - 0.16), 0.08, facecolor="white", zorder=5.2
            )
        )

    # Soft Cheek Blush
    ax.add_patch(
        patches.Ellipse(
            (-1.6, 0.0),
            0.75,
            0.4,
            facecolor=PINK_BLUSH,
            alpha=0.55,
            zorder=4.4,
        )
    )
    ax.add_patch(
        patches.Ellipse(
            (1.6, 0.0), 0.75, 0.4, facecolor=PINK_BLUSH, alpha=0.55, zorder=4.4
        )
    )

    # Tiny Nose
    nose_pts = np.array([[-0.16, 0.22], [0.16, 0.22], [0, 0.07]])
    ax.add_patch(
        patches.Polygon(
            nose_pts,
            closed=True,
            facecolor=PINK_NOSE,
            edgecolor=FUR_DARK,
            lw=0.5,
            zorder=5.3,
        )
    )

    # Cat Mouth (W shaped arcs)
    m_left = patches.Arc(
        (-0.2, -0.02),
        0.4,
        0.32,
        angle=0,
        theta1=190,
        theta2=360,
        color=WHISKER_CLR,
        lw=2.2,
        capstyle="round",
        zorder=5.3,
    )
    m_right = patches.Arc(
        (0.2, -0.02),
        0.4,
        0.32,
        angle=0,
        theta1=180,
        theta2=350,
        color=WHISKER_CLR,
        lw=2.2,
        capstyle="round",
        zorder=5.3,
    )
    ax.add_patch(m_left)
    ax.add_patch(m_right)

    # Whiskers
    whisker_opts = dict(
        color=WHISKER_CLR, lw=1.8, alpha=0.75, solid_capstyle="round", zorder=5.4
    )
    # Left Whiskers
    ax.plot([-1.4, -2.8, -3.8], [0.1, 0.25, 0.2], **whisker_opts)
    ax.plot([-1.4, -2.9, -3.9], [-0.05, -0.1, -0.2], **whisker_opts)
    ax.plot([-1.4, -2.7, -3.6], [-0.2, -0.4, -0.55], **whisker_opts)
    # Right Whiskers
    ax.plot([1.4, 2.8, 3.8], [0.1, 0.25, 0.2], **whisker_opts)
    ax.plot([1.4, 2.9, 3.9], [-0.05, -0.1, -0.2], **whisker_opts)
    ax.plot([1.4, 2.7, 3.6], [-0.2, -0.4, -0.55], **whisker_opts)

    # ==========================================
    # 6. COLLAR & GOLDEN BELL
    # ==========================================
    collar = patches.Arc(
        (0, -0.9),
        2.2,
        1.1,
        angle=0,
        theta1=205,
        theta2=335,
        color=COLLAR_RED,
        lw=7,
        capstyle="round",
        zorder=6,
    )
    ax.add_patch(collar)

    # Bell
    ax.add_patch(
        patches.Circle(
            (0, -1.45),
            0.28,
            facecolor=BELL_GOLD,
            edgecolor="#C69214",
            lw=1.5,
            zorder=6.1,
        )
    )
    ax.add_patch(
        patches.Circle((0, -1.48), 0.05, facecolor="#5A3E00", zorder=6.2)
    )

    # ==========================================
    # 7. FRONT PAWS
    # ==========================================
    for side in [-1, 1]:
        px = side * 0.75
        # Main Paw
        paw = patches.Ellipse(
            (px, -3.05),
            0.95,
            0.7,
            angle=-side * 8,
            facecolor=FUR_MAIN,
            edgecolor=FUR_DARK,
            lw=1.5,
            zorder=5.5,
        )
        ax.add_patch(paw)
        # White "sock" tip
        paw_sock = patches.Ellipse(
            (px, -3.15),
            0.75,
            0.5,
            angle=-side * 8,
            facecolor=FUR_LIGHT,
            zorder=5.6,
        )
        ax.add_patch(paw_sock)
        # Toe dividing lines
        ax.plot(
            [px - 0.12, px - 0.12],
            [-3.0, -3.35],
            color=FUR_DARK,
            lw=1.2,
            zorder=5.7,
        )
        ax.plot(
            [px + 0.12, px + 0.12],
            [-3.0, -3.35],
            color=FUR_DARK,
            lw=1.2,
            zorder=5.7,
        )

    # ==========================================
    # 8. CUTE DECORATIONS (Floating Hearts & Stars)
    # ==========================================
    def draw_heart(x, y, size=0.2, color="#FF6B8B"):
        t_h = np.linspace(0, 2 * np.pi, 100)
        hx = size * 16 * np.sin(t_h) ** 3 / 14 + x
        hy = (
            size
            * (
                13 * np.cos(t_h)
                - 5 * np.cos(2 * t_h)
                - 2 * np.cos(3 * t_h)
                - np.cos(4 * t_h)
            )
            / 14
            + y
        )
        ax.fill(hx, hy, color=color, zorder=7)

    # Floating hearts
    draw_heart(3.0, 2.5, size=0.28, color="#FF7597")
    draw_heart(-3.0, 2.2, size=0.20, color="#FFADC1")
    draw_heart(3.3, 1.6, size=0.15, color="#FFADC1")

    # Sparkle Stars (Cross-stars)
    def draw_sparkle(x, y, s=0.2, color="#FFD13B"):
        ax.plot([x - s, x + s], [y, y], color=color, lw=2.5, zorder=7)
        ax.plot([x, x], [y - s, y + s], color=color, lw=2.5, zorder=7)
        ax.plot(
            [x - s * 0.4, x + s * 0.4],
            [y - s * 0.4, y + s * 0.4],
            color=color,
            lw=1.5,
            zorder=7,
        )
        ax.plot(
            [x - s * 0.4, x + s * 0.4],
            [y + s * 0.4, y - s * 0.4],
            color=color,
            lw=1.5,
            zorder=7,
        )

    draw_sparkle(-3.2, 3.2, s=0.22, color="#FFD13B")
    draw_sparkle(2.5, 3.4, s=0.18, color="#FFD13B")
    draw_sparkle(-3.5, 0.8, s=0.15, color="#FFB6C1")

    plt.title("Meow! 🐾", fontsize=18, color="#543825", pad=20, weight="bold")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    draw_cute_kitten()
