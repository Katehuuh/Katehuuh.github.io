import matplotlib.pyplot as plt
from matplotlib.patches import (
    Circle,
    Ellipse,
    Polygon,
    Arc,
    FancyBboxPatch,
    PathPatch,
)
from matplotlib.path import Path


def draw_kitten():
    # Color palette
    background = "#FFF7F0"
    fur = "#D99A5B"
    cream = "#FFE8C5"
    outline = "#654236"
    stripe = "#A8653C"
    pink = "#F49AA3"
    inner_ear = "#F7B7B2"
    collar = "#E85D75"
    gold = "#F8C64E"
    eye_green = "#75C9A7"

    fig, ax = plt.subplots(figsize=(7, 7.5), facecolor=background)
    ax.set_facecolor(background)

    # Ground shadow
    ax.add_patch(
        Ellipse(
            (0, -4.35),
            7.2,
            0.8,
            facecolor="#D8C1B5",
            edgecolor="none",
            alpha=0.35,
            zorder=0,
        )
    )

    # Curved tail behind the body
    tail_path = Path(
        [
            (1.7, -2.6),
            (4.8, -2.2),
            (5.1, 0.6),
            (3.8, 1.15),
        ],
        [
            Path.MOVETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
        ],
    )

    ax.add_patch(
        PathPatch(
            tail_path,
            fill=False,
            edgecolor=outline,
            linewidth=28,
            capstyle="round",
            joinstyle="round",
            zorder=1,
        )
    )
    ax.add_patch(
        PathPatch(
            tail_path,
            fill=False,
            edgecolor=fur,
            linewidth=20,
            capstyle="round",
            joinstyle="round",
            zorder=1.1,
        )
    )

    # Body
    ax.add_patch(
        Ellipse(
            (0, -1.65),
            5.0,
            5.9,
            facecolor=fur,
            edgecolor=outline,
            linewidth=3,
            zorder=2,
        )
    )

    # Belly
    ax.add_patch(
        Ellipse(
            (0, -1.8),
            3.25,
            4.25,
            facecolor=cream,
            edgecolor="#C9844E",
            linewidth=2,
            zorder=2.2,
        )
    )

    # Back paws
    for x in (-1.85, 1.85):
        ax.add_patch(
            Ellipse(
                (x, -4.0),
                2.05,
                1.15,
                facecolor=fur,
                edgecolor=outline,
                linewidth=2.5,
                zorder=2.7,
            )
        )

    # Front legs
    for x in (-0.95, 0.95):
        ax.add_patch(
            Ellipse(
                (x, -2.55),
                1.35,
                3.55,
                facecolor=fur,
                edgecolor=outline,
                linewidth=2.5,
                zorder=3,
            )
        )

        # Toe lines
        for dx in (-0.2, 0.2):
            ax.plot(
                [x + dx, x + dx * 0.9],
                [-4.08, -3.72],
                color=outline,
                linewidth=1.6,
                solid_capstyle="round",
                zorder=3.2,
            )

    # Ears
    left_ear = Polygon(
        [(-2.65, 4.1), (-2.05, 6.45), (-0.55, 4.75)],
        closed=True,
        facecolor=fur,
        edgecolor=outline,
        linewidth=3,
        zorder=3,
    )
    right_ear = Polygon(
        [(2.65, 4.1), (2.05, 6.45), (0.55, 4.75)],
        closed=True,
        facecolor=fur,
        edgecolor=outline,
        linewidth=3,
        zorder=3,
    )
    ax.add_patch(left_ear)
    ax.add_patch(right_ear)

    # Inner ears
    ax.add_patch(
        Polygon(
            [(-2.25, 4.55), (-2.02, 5.85), (-1.05, 4.7)],
            closed=True,
            facecolor=inner_ear,
            edgecolor="#C97878",
            linewidth=1.7,
            zorder=3.2,
        )
    )
    ax.add_patch(
        Polygon(
            [(2.25, 4.55), (2.02, 5.85), (1.05, 4.7)],
            closed=True,
            facecolor=inner_ear,
            edgecolor="#C97878",
            linewidth=1.7,
            zorder=3.2,
        )
    )

    # Head
    ax.add_patch(
        Ellipse(
            (0, 2.45),
            6.15,
            5.2,
            facecolor=fur,
            edgecolor=outline,
            linewidth=3.2,
            zorder=4,
        )
    )

    # Forehead stripes
    stripe_data = [
        ([(0, 5.0), (0, 4.35)], [Path.MOVETO, Path.LINETO]),
        (
            [(-0.8, 4.85), (-0.72, 4.55), (-0.55, 4.22)],
            [Path.MOVETO, Path.CURVE3, Path.CURVE3],
        ),
        (
            [(0.8, 4.85), (0.72, 4.55), (0.55, 4.22)],
            [Path.MOVETO, Path.CURVE3, Path.CURVE3],
        ),
    ]

    for points, codes in stripe_data:
        ax.add_patch(
            PathPatch(
                Path(points, codes),
                fill=False,
                edgecolor=stripe,
                linewidth=5,
                capstyle="round",
                zorder=5,
            )
        )

    # Collar
    ax.add_patch(
        FancyBboxPatch(
            (-2.1, -0.2),
            4.2,
            0.55,
            boxstyle="round,pad=0.03,rounding_size=0.2",
            facecolor=collar,
            edgecolor=outline,
            linewidth=2.2,
            zorder=5,
        )
    )

    # Bell
    ax.add_patch(
        Circle(
            (0, -0.25),
            0.4,
            facecolor=gold,
            edgecolor=outline,
            linewidth=2.2,
            zorder=5.5,
        )
    )
    ax.add_patch(
        Circle(
            (0, -0.3),
            0.07,
            facecolor=outline,
            edgecolor="none",
            zorder=6,
        )
    )
    ax.plot(
        [0, 0],
        [-0.35, -0.5],
        color=outline,
        linewidth=1.7,
        solid_capstyle="round",
        zorder=6,
    )

    # Eyes
    for x in (-1.25, 1.25):
        ax.add_patch(
            Ellipse(
                (x, 3.05),
                1.08,
                1.38,
                facecolor=outline,
                edgecolor=outline,
                linewidth=1.5,
                zorder=6,
            )
        )
        ax.add_patch(
            Ellipse(
                (x, 2.96),
                0.72,
                0.88,
                facecolor=eye_green,
                edgecolor="none",
                zorder=6.1,
            )
        )
        ax.add_patch(
            Ellipse(
                (x, 2.94),
                0.32,
                0.68,
                facecolor="#201A18",
                edgecolor="none",
                zorder=6.2,
            )
        )
        ax.add_patch(
            Circle(
                (x - 0.18, 3.27),
                0.14,
                facecolor="white",
                edgecolor="none",
                zorder=6.4,
            )
        )
        ax.add_patch(
            Circle(
                (x + 0.13, 2.9),
                0.065,
                facecolor="white",
                edgecolor="none",
                zorder=6.4,
            )
        )

    # Blushing cheeks
    for x in (-2.15, 2.15):
        ax.add_patch(
            Ellipse(
                (x, 1.7),
                0.85,
                0.38,
                facecolor=pink,
                edgecolor="none",
                alpha=0.55,
                zorder=6,
            )
        )

    # Cream-colored muzzle
    for x in (-0.5, 0.5):
        ax.add_patch(
            Ellipse(
                (x, 1.65),
                1.35,
                0.95,
                facecolor=cream,
                edgecolor="none",
                zorder=6,
            )
        )

    # Nose
    ax.add_patch(
        Polygon(
            [(-0.29, 2.02), (0.29, 2.02), (0, 1.74)],
            closed=True,
            facecolor=pink,
            edgecolor=outline,
            linewidth=1.7,
            zorder=7,
        )
    )

    # Tiny tongue
    ax.add_patch(
        Ellipse(
            (0, 1.28),
            0.52,
            0.43,
            facecolor=pink,
            edgecolor=outline,
            linewidth=1.4,
            zorder=6.8,
        )
    )
    ax.plot(
        [0, 0],
        [1.14, 1.32],
        color="#C86E79",
        linewidth=1,
        zorder=7,
    )

    # Smiling mouth
    for control, end in [
        ((-0.18, 1.36), (-0.7, 1.43)),
        ((0.18, 1.36), (0.7, 1.43)),
    ]:
        mouth_path = Path(
            [(0, 1.76), control, end],
            [Path.MOVETO, Path.CURVE3, Path.CURVE3],
        )
        ax.add_patch(
            PathPatch(
                mouth_path,
                fill=False,
                edgecolor=outline,
                linewidth=2.2,
                capstyle="round",
                zorder=7.2,
            )
        )

    # Whisker dots
    for x, y in [
        (-0.75, 1.72),
        (-1.0, 1.58),
        (-0.78, 1.48),
        (0.75, 1.72),
        (1.0, 1.58),
        (0.78, 1.48),
    ]:
        ax.add_patch(
            Circle((x, y), 0.045, facecolor=outline, edgecolor="none", zorder=7)
        )

    # Whiskers
    left_whiskers = [
        ((-1.35, 1.75), (-4.35, 2.15)),
        ((-1.4, 1.55), (-4.5, 1.45)),
        ((-1.35, 1.35), (-4.2, 0.82)),
    ]

    for start, end in left_whiskers:
        ax.plot(
            [start[0], end[0]],
            [start[1], end[1]],
            color=outline,
            linewidth=1.8,
            solid_capstyle="round",
            zorder=7,
        )
        ax.plot(
            [-start[0], -end[0]],
            [start[1], end[1]],
            color=outline,
            linewidth=1.8,
            solid_capstyle="round",
            zorder=7,
        )

    # Small heart beside the kitten
    heart_path = Path(
        [
            (4.45, 4.85),
            (3.65, 5.35),
            (3.9, 6.05),
            (4.45, 5.55),
            (5.0, 6.05),
            (5.25, 5.35),
            (4.45, 4.85),
            (4.45, 4.85),
        ],
        [
            Path.MOVETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CLOSEPOLY,
        ],
    )
    ax.add_patch(
        PathPatch(
            heart_path,
            facecolor=pink,
            edgecolor="#D86778",
            linewidth=2,
            zorder=8,
        )
    )

    ax.set_xlim(-5.7, 5.7)
    ax.set_ylim(-4.9, 7.0)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout(pad=0)

    return fig, ax


if __name__ == "__main__":
    fig, ax = draw_kitten()

    # Uncomment to save the drawing:
    # fig.savefig("cute_kitten.png", dpi=300, bbox_inches="tight")

    plt.show()
