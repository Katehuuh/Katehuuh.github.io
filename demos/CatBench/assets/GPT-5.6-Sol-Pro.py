import matplotlib.pyplot as plt
from matplotlib.patches import (
    Circle,
    Ellipse,
    Polygon,
    FancyBboxPatch,
    PathPatch,
)
from matplotlib.path import Path


# Color palette
BACKGROUND = "#FFF4ED"
FUR = "#F3A35C"
LIGHT_FUR = "#FFD6A0"
DARK_FUR = "#C86B3C"
OUTLINE = "#5A3B32"
PINK = "#F58FA3"
TEAL = "#65C3BA"
GOLD = "#F6C453"


def add_curve(ax, points, color, width, zorder=1):
    """Add a smooth cubic Bézier curve."""
    codes = [Path.MOVETO] + [Path.CURVE4] * (len(points) - 1)
    path = Path(points, codes)

    patch = PathPatch(
        path,
        facecolor="none",
        edgecolor=color,
        linewidth=width,
        capstyle="round",
        joinstyle="round",
        zorder=zorder,
    )
    ax.add_patch(patch)
    return patch


def draw_kitten(save_path=None):
    fig, ax = plt.subplots(figsize=(7, 7), facecolor=BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    ax.axis("off")

    # Background decorations
    ax.text(
        1.15,
        7.9,
        "♥",
        fontsize=30,
        color="#F6A5B4",
        rotation=-15,
        ha="center",
        va="center",
        zorder=0,
    )
    ax.text(
        8.75,
        8.2,
        "♥",
        fontsize=25,
        color="#F6A5B4",
        rotation=15,
        ha="center",
        va="center",
        zorder=0,
    )

    for x, y in [(1.6, 5.0), (8.6, 6.6), (2.0, 8.9), (8.0, 9.1)]:
        ax.plot(
            [x - 0.13, x + 0.13],
            [y, y],
            color=GOLD,
            linewidth=2,
            solid_capstyle="round",
            zorder=0,
        )
        ax.plot(
            [x, x],
            [y - 0.13, y + 0.13],
            color=GOLD,
            linewidth=2,
            solid_capstyle="round",
            zorder=0,
        )

    for x, y, radius in [
        (1.1, 6.5, 0.06),
        (1.8, 7.0, 0.05),
        (8.2, 7.5, 0.06),
        (9.0, 6.0, 0.05),
    ]:
        ax.add_patch(
            Circle(
                (x, y),
                radius,
                facecolor="#E8A8A4",
                edgecolor="none",
                zorder=0,
            )
        )

    # Ground shadow
    ax.add_patch(
        Ellipse(
            (5, 0.9),
            5.8,
            0.75,
            facecolor="#E8CFC4",
            edgecolor="none",
            alpha=0.65,
            zorder=0,
        )
    )

    # Curled tail behind the body
    tail_points = [
        (6.55, 3.25),
        (7.95, 2.75),
        (9.10, 3.45),
        (8.78, 4.75),
        (8.63, 5.42),
        (8.02, 5.72),
        (7.72, 5.34),
    ]
    add_curve(ax, tail_points, OUTLINE, 33, zorder=1)
    add_curve(ax, tail_points, FUR, 25, zorder=2)

    # Dark tail tip
    tail_tip = [
        (8.63, 4.98),
        (8.50, 5.43),
        (8.00, 5.68),
        (7.72, 5.34),
    ]
    add_curve(ax, tail_tip, OUTLINE, 27, zorder=3)
    add_curve(ax, tail_tip, DARK_FUR, 21, zorder=4)

    # Body
    ax.add_patch(
        Ellipse(
            (5, 3.35),
            4.35,
            4.7,
            facecolor=FUR,
            edgecolor=OUTLINE,
            linewidth=3,
            zorder=3,
        )
    )

    # Belly
    ax.add_patch(
        Ellipse(
            (5, 3.05),
            2.65,
            3.45,
            facecolor=LIGHT_FUR,
            edgecolor="none",
            zorder=4,
        )
    )

    # Body stripes
    body_stripes = [
        [
            (2.92, 4.45),
            (3.22, 4.30),
            (3.42, 4.05),
            (3.58, 3.75),
        ],
        [
            (2.75, 3.82),
            (3.05, 3.70),
            (3.28, 3.47),
            (3.42, 3.18),
        ],
    ]

    for stripe in body_stripes:
        add_curve(ax, stripe, DARK_FUR, 7, zorder=5)
        add_curve(
            ax,
            [(10 - x, y) for x, y in stripe],
            DARK_FUR,
            7,
            zorder=5,
        )

    # Front legs
    for x in (3.55, 5.20):
        ax.add_patch(
            FancyBboxPatch(
                (x, 1.05),
                1.30,
                3.05,
                boxstyle="round,pad=0.02,rounding_size=0.58",
                facecolor=FUR,
                edgecolor=OUTLINE,
                linewidth=3,
                zorder=6,
            )
        )

    # Cream-colored paws
    for center_x in (4.20, 5.85):
        ax.add_patch(
            Ellipse(
                (center_x, 1.35),
                1.15,
                0.72,
                facecolor=LIGHT_FUR,
                edgecolor="none",
                zorder=7,
            )
        )

        for offset in (-0.20, 0.20):
            add_curve(
                ax,
                [
                    (center_x + offset, 1.08),
                    (center_x + offset - 0.02, 1.18),
                    (center_x + offset - 0.02, 1.28),
                    (center_x + offset, 1.36),
                ],
                OUTLINE,
                1.4,
                zorder=8,
            )

    # Collar behind the head
    ax.add_patch(
        FancyBboxPatch(
            (3.40, 4.24),
            3.20,
            0.50,
            boxstyle="round,pad=0.02,rounding_size=0.22",
            facecolor=TEAL,
            edgecolor=OUTLINE,
            linewidth=2.5,
            zorder=7,
        )
    )

    # Ears
    left_ear = Polygon(
        [(2.65, 7.65), (2.90, 9.48), (4.30, 8.38)],
        closed=True,
        facecolor=FUR,
        edgecolor=OUTLINE,
        linewidth=3,
        joinstyle="round",
        zorder=7,
    )
    right_ear = Polygon(
        [(5.70, 8.38), (7.10, 9.48), (7.35, 7.65)],
        closed=True,
        facecolor=FUR,
        edgecolor=OUTLINE,
        linewidth=3,
        joinstyle="round",
        zorder=7,
    )
    ax.add_patch(left_ear)
    ax.add_patch(right_ear)

    # Inner ears
    ax.add_patch(
        Polygon(
            [(2.98, 8.00), (3.10, 9.02), (3.92, 8.35)],
            closed=True,
            facecolor="#F6B1B0",
            edgecolor=DARK_FUR,
            linewidth=1.8,
            zorder=8,
        )
    )
    ax.add_patch(
        Polygon(
            [(6.08, 8.35), (6.90, 9.02), (7.02, 8.00)],
            closed=True,
            facecolor="#F6B1B0",
            edgecolor=DARK_FUR,
            linewidth=1.8,
            zorder=8,
        )
    )

    # Head
    ax.add_patch(
        Ellipse(
            (5, 6.60),
            5.55,
            4.25,
            facecolor=FUR,
            edgecolor=OUTLINE,
            linewidth=3,
            zorder=8,
        )
    )

    # Forehead stripes
    forehead_stripes = [
        [
            (4.40, 8.64),
            (4.40, 8.42),
            (4.52, 8.20),
            (4.62, 8.02),
        ],
        [
            (5.00, 8.70),
            (5.00, 8.46),
            (5.00, 8.22),
            (5.00, 8.00),
        ],
        [
            (5.60, 8.64),
            (5.60, 8.42),
            (5.48, 8.20),
            (5.38, 8.02),
        ],
    ]

    for stripe in forehead_stripes:
        add_curve(ax, stripe, DARK_FUR, 7, zorder=9)

    # Cheek stripes
    cheek_stripes = [
        [
            (2.48, 6.73),
            (2.78, 6.66),
            (3.06, 6.50),
            (3.35, 6.30),
        ],
        [
            (2.40, 6.12),
            (2.74, 6.12),
            (3.02, 6.02),
            (3.32, 5.88),
        ],
    ]

    for stripe in cheek_stripes:
        add_curve(ax, stripe, DARK_FUR, 6.5, zorder=9)
        add_curve(
            ax,
            [(10 - x, y) for x, y in stripe],
            DARK_FUR,
            6.5,
            zorder=9,
        )

    # Blushing cheeks
    for x in (3.15, 6.85):
        ax.add_patch(
            Ellipse(
                (x, 5.85),
                0.75,
                0.34,
                facecolor=PINK,
                edgecolor="none",
                alpha=0.55,
                zorder=10,
            )
        )

    # Eyes
    for eye_x in (3.95, 6.05):
        ax.add_patch(
            Ellipse(
                (eye_x, 6.72),
                1.17,
                1.28,
                facecolor="#4A332F",
                edgecolor=OUTLINE,
                linewidth=2,
                zorder=10,
            )
        )
        ax.add_patch(
            Ellipse(
                (eye_x, 6.64),
                0.82,
                0.95,
                facecolor="#93623F",
                edgecolor="none",
                zorder=11,
            )
        )
        ax.add_patch(
            Ellipse(
                (eye_x, 6.62),
                0.23,
                0.72,
                facecolor="#241A19",
                edgecolor="none",
                zorder=12,
            )
        )

        # Eye highlights
        ax.add_patch(
            Circle(
                (eye_x - 0.20, 6.96),
                0.16,
                facecolor="white",
                edgecolor="none",
                zorder=13,
            )
        )
        ax.add_patch(
            Circle(
                (eye_x + 0.18, 6.46),
                0.07,
                facecolor="white",
                edgecolor="none",
                alpha=0.9,
                zorder=13,
            )
        )

    # Whiskers
    left_whiskers = [
        [
            (4.25, 5.78),
            (3.65, 5.78),
            (2.75, 5.98),
            (1.92, 6.18),
        ],
        [
            (4.22, 5.58),
            (3.55, 5.50),
            (2.66, 5.46),
            (1.82, 5.55),
        ],
        [
            (4.28, 5.40),
            (3.65, 5.25),
            (2.80, 5.00),
            (2.08, 4.88),
        ],
    ]

    for whisker in left_whiskers:
        add_curve(ax, whisker, OUTLINE, 1.7, zorder=11)
        add_curve(
            ax,
            [(10 - x, y) for x, y in whisker],
            OUTLINE,
            1.7,
            zorder=11,
        )

    # Muzzle
    ax.add_patch(
        Ellipse(
            (4.48, 5.68),
            1.45,
            1.05,
            facecolor=LIGHT_FUR,
            edgecolor="none",
            zorder=12,
        )
    )
    ax.add_patch(
        Ellipse(
            (5.52, 5.68),
            1.45,
            1.05,
            facecolor=LIGHT_FUR,
            edgecolor="none",
            zorder=12,
        )
    )

    # Tongue
    ax.add_patch(
        Ellipse(
            (5, 5.25),
            0.50,
            0.42,
            facecolor=PINK,
            edgecolor=OUTLINE,
            linewidth=1.5,
            zorder=13,
        )
    )

    # Nose
    ax.add_patch(
        Polygon(
            [(4.70, 6.02), (5.30, 6.02), (5.00, 5.70)],
            closed=True,
            facecolor=PINK,
            edgecolor=OUTLINE,
            linewidth=1.8,
            zorder=14,
        )
    )

    # Smiling mouth
    ax.plot(
        [5.00, 5.00],
        [5.71, 5.50],
        color=OUTLINE,
        linewidth=1.8,
        solid_capstyle="round",
        zorder=14,
    )
    add_curve(
        ax,
        [(5.00, 5.50), (4.90, 5.28), (4.70, 5.28), (4.52, 5.43)],
        OUTLINE,
        1.8,
        zorder=14,
    )
    add_curve(
        ax,
        [(5.00, 5.50), (5.10, 5.28), (5.30, 5.28), (5.48, 5.43)],
        OUTLINE,
        1.8,
        zorder=14,
    )

    # Collar bell
    ax.add_patch(
        Circle(
            (5, 4.28),
            0.30,
            facecolor=GOLD,
            edgecolor=OUTLINE,
            linewidth=2,
            zorder=15,
        )
    )
    ax.add_patch(
        Circle(
            (5, 4.20),
            0.055,
            facecolor=OUTLINE,
            edgecolor="none",
            zorder=16,
        )
    )

    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

    if save_path:
        fig.savefig(
            save_path,
            dpi=220,
            bbox_inches="tight",
            facecolor=fig.get_facecolor(),
        )

    plt.show()


if __name__ == "__main__":
    draw_kitten()
    # To save the drawing, use:
    # draw_kitten("cute_kitten.png")
