import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, PathPatch
from matplotlib.path import Path


def draw_kitten():
    ink = "#684A3B"
    fur = "#F4B56B"
    cream = "#FFF3DC"
    pink = "#F6A4B3"

    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor("#FFF8F2")
    ax.set(aspect="equal", xlim=(-3.1, 3.1), ylim=(-2.6, 3.3))
    ax.axis("off")

    def oval(center, width, height, color, edge="none", z=3):
        ax.add_patch(Ellipse(
            center, width, height,
            facecolor=color, edgecolor=edge,
            linewidth=2.5, zorder=z,
        ))

    # Soft shadow.
    oval((0, -2.23), 3.2, 0.25, "#EAD9CD", z=0)

    # Curled tail, drawn behind the body.
    tail = Path(
        [(0.95, -1.55), (2.6, -1.8), (2.95, -0.6), (2.4, -0.25),
         (2.0, 0.05), (1.9, -0.15), (2.1, -0.35)],
        [Path.MOVETO] + [Path.CURVE4] * 6,
    )
    for color, width in [(ink, 29), (fur, 23)]:
        ax.add_patch(PathPatch(
            tail, fill=False, edgecolor=color, linewidth=width,
            capstyle="round", zorder=1,
        ))

    # Round body and soft tummy.
    oval((0, -0.9), 2.5, 2.6, fur, edge=ink, z=2)
    oval((0, -1.02), 1.45, 1.85, cream, z=3)

    # Pointy ears with pink centers.
    for side in (-1, 1):
        ax.add_patch(Polygon(
            [(side * 0.65, 2.0), (side * 1.75, 3.05),
             (side * 1.62, 1.38)],
            facecolor=fur, edgecolor=ink, linewidth=2.5, zorder=4,
        ))
        ax.add_patch(Polygon(
            [(side * 0.98, 2.13), (side * 1.57, 2.74),
             (side * 1.47, 1.87)],
            facecolor=pink, edgecolor="none", zorder=4,
        ))

    # Front legs and tiny paws.
    for side in (-1, 1):
        ax.plot(
            [side * 0.53, side * 0.53], [-0.85, -1.8],
            color=ink, linewidth=1.8, zorder=3.5,
        )
        oval((side * 0.68, -2.0), 0.95, 0.55, fur, edge=ink, z=4)
        for offset in (-0.13, 0.13):
            x = side * 0.68 + offset
            ax.plot(
                [x, x], [-2.06, -2.2],
                color=ink, linewidth=1.3, zorder=5,
                solid_capstyle="round",
            )

    # Oversized head and little tabby stripes.
    oval((0, 1.0), 3.6, 2.7, fur, edge=ink, z=5)
    for x in (-0.48, 0, 0.48):
        ax.plot(
            [x * 1.1, x], [2.12, 1.82],
            color="#D98E48", linewidth=5, zorder=6,
            solid_capstyle="round",
        )

    # Cream muzzle, rosy cheeks, and shiny eyes.
    for side in (-1, 1):
        oval((side * 0.25, 0.5), 0.75, 0.6, cream, z=6)
        oval((side * 1.14, 0.59), 0.43, 0.23, pink, z=6)

        eye_x = side * 0.67
        oval((eye_x, 1.15), 0.63, 0.8, ink, z=7)
        oval((eye_x - 0.09, 1.32), 0.20, 0.23, "white", z=8)
        oval((eye_x + 0.12, 1.01), 0.075, 0.075, "white", z=8)

    # Tiny pink nose and smiling mouth.
    ax.add_patch(Polygon(
        [(-0.15, 0.66), (0.15, 0.66), (0, 0.51)],
        facecolor=pink, edgecolor=ink, linewidth=1.5, zorder=8,
    ))
    ax.plot([0, 0], [0.51, 0.44], color=ink, linewidth=2, zorder=8)

    smile = Path(
        [(-0.31, 0.43), (-0.16, 0.20), (0, 0.44),
         (0.16, 0.20), (0.31, 0.43)],
        [Path.MOVETO] + [Path.CURVE3] * 4,
    )
    ax.add_patch(PathPatch(
        smile, fill=False, edgecolor=ink, linewidth=2.2,
        capstyle="round", zorder=8,
    ))

    # Whiskers.
    for side in (-1, 1):
        for tilt in (-1, 0, 1):
            ax.plot(
                [side * 0.94, side * 2.18],
                [0.53 + tilt * 0.1, 0.53 + tilt * 0.28],
                color=ink, linewidth=1.7, zorder=8,
                solid_capstyle="round",
            )

    ax.text(2.3, 2.25, "\u2665", fontsize=34, color=pink,
            ha="center", va="center")

    fig.tight_layout(pad=0.5)
    # Uncomment to save the picture:
    # fig.savefig("kitten.png", dpi=200, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    draw_kitten()
