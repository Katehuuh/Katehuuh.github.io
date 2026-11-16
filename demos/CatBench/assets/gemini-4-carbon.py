import matplotlib.patches as patches
import matplotlib.path as mpath
import matplotlib.pyplot as plt
import numpy as np


def draw_heart(ax, center_x, center_y, scale=0.04, angle=0, color="#FF758F"):
    """Helper function to draw a cute tilted heart using parametric equations."""
    t = np.linspace(0, 2 * np.pi, 100)
    x = 16 * np.sin(t) ** 3
    y = (
        13 * np.cos(t)
        - 5 * np.cos(2 * t)
        - 2 * np.cos(3 * t)
        - np.cos(4 * t)
    )

    # Scale
    x = x * scale
    y = y * scale

    # Rotate
    rad = np.radians(angle)
    x_rot = x * np.cos(rad) - y * np.sin(rad)
    y_rot = x * np.sin(rad) + y * np.cos(rad)

    # Translate
    ax.fill(x_rot + center_x, y_rot + center_y, color=color, zorder=10)


def draw_kitten():
    # Setup canvas
    fig, ax = plt.subplots(figsize=(7, 8), facecolor="#FFF5F7")
    ax.set_facecolor("#FFF5F7")
    ax.set_aspect("equal")
    ax.set_xlim(-4.2, 4.2)
    ax.set_ylim(-5.2, 4.0)
    ax.axis("off")

    # Color Palette
    FUR_MAIN = "#D0D5DD"  # Soft pastel grey
    FUR_STRIPE = "#98A2B3"  # Darker grey for tabby stripes
    WHITE = "#FFFFFF"  # Belly, paws, eye sparkles
    PINK_EAR = "#FFB3C6"  # Inner ears
    PINK_BLUSH = "#FF8FA3"  # Cheek blush & nose
    OUTLINE = "#475467"  # Soft dark charcoal outline
    EYE_COLOR = "#1D2939"  # Deep dark eyes
    COLLAR_RED = "#FF4D6D"  # Cute pink-red collar
    BELL_GOLD = "#FFD166"  # Golden bell

    Path = mpath.Path
    lw_main = 2.5

    # ---------------------------------------------------------
    # 1. Ground Shadow & Tail
    # ---------------------------------------------------------
    shadow = patches.Ellipse(
        (0, -4.55), width=4.2, height=0.65, facecolor="#F2E2E6", zorder=0
    )
    ax.add_patch(shadow)

    # Wavy tail using a double-stroked Bezier curve (outer stroke = outline, inner = fur)
    tail_verts = [(0.8, -4.1), (3.2, -4.4), (2.4, -2.0), (3.5, -1.5)]
    tail_codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    tail_path = Path(tail_verts, tail_codes)

    tail_outline = patches.PathPatch(
        tail_path,
        facecolor="none",
        edgecolor=OUTLINE,
        lw=22,
        capstyle="round",
        zorder=1,
    )
    tail_fill = patches.PathPatch(
        tail_path,
        facecolor="none",
        edgecolor=FUR_MAIN,
        lw=16.5,
        capstyle="round",
        zorder=1.1,
    )
    ax.add_patch(tail_outline)
    ax.add_patch(tail_fill)

    # ---------------------------------------------------------
    # 2. Body, Belly & Paws
    # ---------------------------------------------------------
    # Main chubby body
    body = patches.Ellipse(
        (0, -2.9),
        width=3.3,
        height=3.4,
        facecolor=FUR_MAIN,
        edgecolor=OUTLINE,
        lw=lw_main,
        zorder=2,
    )
    ax.add_patch(body)

    # White fluffy belly patch
    belly = patches.Ellipse(
        (0, -3.1),
        width=2.0,
        height=2.3,
        facecolor=WHITE,
        edgecolor="none",
        zorder=2.5,
    )
    ax.add_patch(belly)

    # Back paws (sticking out slightly on the sides)
    for sign in [-1, 1]:
        back_paw = patches.Ellipse(
            (sign * 1.35, -4.3),
            width=1.0,
            height=0.65,
            angle=sign * -15,
            facecolor=WHITE,
            edgecolor=OUTLINE,
            lw=lw_main,
            zorder=3,
        )
        ax.add_patch(back_paw)

    # Front paws (resting neatly together in front)
    for sign in [-1, 1]:
        front_paw = patches.Ellipse(
            (sign * 0.52, -4.35),
            width=0.85,
            height=0.75,
            facecolor=WHITE,
            edgecolor=OUTLINE,
            lw=lw_main,
            zorder=4,
        )
        ax.add_patch(front_paw)
        # Tiny paw toe lines
        for offset in [-0.12, 0.12]:
            ax.plot(
                [sign * 0.52 + offset, sign * 0.52 + offset],
                [-4.68, -4.5],
                color=OUTLINE,
                lw=1.5,
                solid_capstyle="round",
                zorder=4.1,
            )

    # ---------------------------------------------------------
    # 3. Collar & Bell
    # ---------------------------------------------------------
    collar = patches.Ellipse(
        (0, -1.65),
        width=2.4,
        height=0.7,
        facecolor=COLLAR_RED,
        edgecolor=OUTLINE,
        lw=lw_main,
        zorder=4.5,
    )
    ax.add_patch(collar)

    bell = patches.Circle(
        (0, -2.02),
        radius=0.26,
        facecolor=BELL_GOLD,
        edgecolor=OUTLINE,
        lw=2,
        zorder=6.5,
    )
    ax.add_patch(bell)
    # Bell detail (little slot)
    ax.plot([0, 0], [-2.27, -2.08], color=OUTLINE, lw=1.8, zorder=6.6)
    ax.add_patch(patches.Circle((0, -2.05), radius=0.05, color=OUTLINE, zorder=6.6))

    # ---------------------------------------------------------
    # 4. Rounded Ears (Left & Right)
    # ---------------------------------------------------------
    for sign in [-1, 1]:
        # Outer fur ear
        ear_verts = [
            (sign * 2.0, 0.4),
            (sign * 2.55, 2.85),
            (sign * 1.8, 3.05),
            (sign * 0.4, 1.5),
            (0, 0),
        ]
        ear_codes = [
            Path.MOVETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CLOSEPOLY,
        ]
        ear_patch = patches.PathPatch(
            Path(ear_verts, ear_codes),
            facecolor=FUR_MAIN,
            edgecolor=OUTLINE,
            lw=lw_main,
            zorder=3,
        )
        ax.add_patch(ear_patch)

        # Inner pink ear
        inner_verts = [
            (sign * 1.75, 0.7),
            (sign * 2.15, 2.45),
            (sign * 1.65, 2.6),
            (sign * 0.7, 1.4),
            (0, 0),
        ]
        inner_patch = patches.PathPatch(
            Path(inner_verts, ear_codes),
            facecolor=PINK_EAR,
            edgecolor="none",
            zorder=3.1,
        )
        ax.add_patch(inner_patch)

    # ---------------------------------------------------------
    # 5. Head & Clipped Tabby Stripes
    # ---------------------------------------------------------
    # Base head fill (used to clip stripes cleanly inside the head)
    head_fill = patches.Ellipse(
        (0, 0),
        width=4.6,
        height=3.8,
        facecolor=FUR_MAIN,
        edgecolor="none",
        zorder=5,
    )
    ax.add_patch(head_fill)

    # Forehead stripes (clipped to head_fill)
    stripe_specs = [
        (0, 1.65, 0.32, 1.1, 0),  # Center forehead stripe
        (-0.55, 1.55, 0.28, 0.95, 12),  # Left forehead stripe
        (0.55, 1.55, 0.28, 0.95, -12),  # Right forehead stripe
        (-2.25, -0.1, 0.8, 0.25, 10),  # Left cheek stripe 1
        (-2.20, -0.45, 0.7, 0.22, -5),  # Left cheek stripe 2
        (2.25, -0.1, 0.8, 0.25, -10),  # Right cheek stripe 1
        (2.20, -0.45, 0.7, 0.22, 5),  # Right cheek stripe 2
    ]
    for sx, sy, sw, sh, s_ang in stripe_specs:
        stripe = patches.Ellipse(
            (sx, sy), width=sw, height=sh, angle=s_ang, facecolor=FUR_STRIPE, zorder=5.2
        )
        stripe.set_clip_path(head_fill)
        ax.add_patch(stripe)

    # Crisp head outline on top of stripes
    head_outline = patches.Ellipse(
        (0, 0),
        width=4.6,
        height=3.8,
        facecolor="none",
        edgecolor=OUTLINE,
        lw=lw_main,
        zorder=5.5,
    )
    ax.add_patch(head_outline)

    # ---------------------------------------------------------
    # 6. Cute Kawaii Face Details
    # ---------------------------------------------------------
    # Rosy Blush
    for sign in [-1, 1]:
        blush = patches.Ellipse(
            (sign * 1.48, -0.62),
            width=0.68,
            height=0.34,
            facecolor=PINK_BLUSH,
            alpha=0.65,
            zorder=6,
        )
        ax.add_patch(blush)

    # Big Sparkling Eyes
    for sign in [-1, 1]:
        eye_x, eye_y = sign * 1.02, -0.22
        eye = patches.Circle((eye_x, eye_y), radius=0.42, facecolor=EYE_COLOR, zorder=6)
        ax.add_patch(eye)

        # Big upper-left catchlight & tiny lower-right catchlight
        sparkle_big = patches.Circle(
            (eye_x - 0.13, eye_y + 0.13), radius=0.14, facecolor=WHITE, zorder=7
        )
        sparkle_small = patches.Circle(
            (eye_x + 0.14, eye_y - 0.14), radius=0.06, facecolor=WHITE, zorder=7
        )
        ax.add_patch(sparkle_big)
        ax.add_patch(sparkle_small)

    # Tiny Pink Nose
    nose = patches.Polygon(
        [(-0.18, -0.38), (0.18, -0.38), (0, -0.54)],
        closed=True,
        facecolor=PINK_BLUSH,
        edgecolor=OUTLINE,
        lw=1.8,
        joinstyle="round",
        zorder=7,
    )
    ax.add_patch(nose)

    # ':3' Cat Mouth (Two meeting arcs)
    mouth_left = patches.Arc(
        (-0.22, -0.60),
        width=0.44,
        height=0.34,
        theta1=200,
        theta2=360,
        edgecolor=OUTLINE,
        lw=2.2,
        capstyle="round",
        zorder=6.5,
    )
    mouth_right = patches.Arc(
        (0.22, -0.60),
        width=0.44,
        height=0.34,
        theta1=180,
        theta2=340,
        edgecolor=OUTLINE,
        lw=2.2,
        capstyle="round",
        zorder=6.5,
    )
    ax.add_patch(mouth_left)
    ax.add_patch(mouth_right)

    # Whiskers
    for sign in [-1, 1]:
        ax.plot(
            [sign * 1.9, sign * 2.85],
            [-0.25, -0.10],
            color=OUTLINE,
            lw=1.8,
            solid_capstyle="round",
            zorder=7,
        )
        ax.plot(
            [sign * 1.95, sign * 2.95],
            [-0.45, -0.45],
            color=OUTLINE,
            lw=1.8,
            solid_capstyle="round",
            zorder=7,
        )
        ax.plot(
            [sign * 1.9, sign * 2.80],
            [-0.65, -0.82],
            color=OUTLINE,
            lw=1.8,
            solid_capstyle="round",
            zorder=7,
        )

    # ---------------------------------------------------------
    # 7. Floating Hearts Decoration
    # ---------------------------------------------------------
    draw_heart(ax, center_x=0.0, center_y=2.9, scale=0.032, angle=5, color="#FF758F")
    draw_heart(ax, center_x=2.6, center_y=2.2, scale=0.022, angle=-18, color="#FFA3B5")
    draw_heart(ax, center_x=-2.7, center_y=1.9, scale=0.018, angle=15, color="#FFA3B5")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    draw_kitten()
