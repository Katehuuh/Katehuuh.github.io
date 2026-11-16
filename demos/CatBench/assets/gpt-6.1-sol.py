import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import Arc, Circle, Ellipse, PathPatch, Polygon


def draw_kitten():
    background = "#FFF9F1"
    fur = "#F5C692"
    outline = "#65483D"
    pink = "#F4A6B8"
    cream = "#FFF0D8"

    fig, ax = plt.subplots(figsize=(6, 7), facecolor=background)
    ax.set_aspect("equal")
    ax.set_xlim(-3.2, 3.2)
    ax.set_ylim(-0.3, 6.4)
    ax.axis("off")

    # A soft shadow beneath the kitten.
    ax.add_patch(Ellipse(
        (0.15, 0.1), 4.4, 0.35,
        facecolor="#EADFD4", edgecolor="none"
    ))

    # Curled tail, drawn behind the body.
    tail = Path(
        [(0.9, 0.8), (3.4, 0.6), (3.2, 3.0), (2.1, 2.6)],
        [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4],
    )
    for color, width in [(outline, 30), (fur, 25)]:
        ax.add_patch(PathPatch(
            tail, fill=False, edgecolor=color,
            linewidth=width, capstyle="round"
        ))

    # Body and fluffy tummy.
    ax.add_patch(Ellipse(
        (0, 1.6), 2.45, 2.9,
        facecolor=fur, edgecolor=outline, linewidth=2.5
    ))
    ax.add_patch(Ellipse(
        (0, 1.45), 1.5, 1.9,
        facecolor=cream, edgecolor="none"
    ))

    # Front legs and paws.
    for x in (-0.45, 0.45):
        ax.plot(
            [x, x], [0.65, 1.35],
            color=outline, linewidth=1.8, solid_capstyle="round"
        )

    for x in (-0.64, 0.64):
        ax.add_patch(Ellipse(
            (x, 0.4), 1.1, 0.62,
            facecolor=fur, edgecolor=outline, linewidth=2.2
        ))
        for offset in (-0.16, 0.16):
            ax.plot(
                [x + offset, x + offset], [0.22, 0.38],
                color=outline, linewidth=1.3, solid_capstyle="round"
            )

    # Pointy ears and pink inner ears.
    for side in (-1, 1):
        ax.add_patch(Polygon(
            [(side * 1.65, 4.5),
             (side * 1.5, 6.0),
             (side * 0.35, 5.05)],
            closed=True, facecolor=fur,
            edgecolor=outline, linewidth=2.5, joinstyle="round"
        ))
        ax.add_patch(Polygon(
            [(side * 1.42, 4.95),
             (side * 1.37, 5.65),
             (side * 0.75, 5.1)],
            closed=True, facecolor=pink, edgecolor="none"
        ))

    # Oversized, round kitten face.
    ax.add_patch(Ellipse(
        (0, 3.95), 3.65, 2.9,
        facecolor=fur, edgecolor=outline, linewidth=2.5
    ))

    # Little forehead stripes.
    for x in (-0.4, 0, 0.4):
        ax.plot(
            [x, x * 0.85], [5.25, 4.96],
            color="#D99A61", linewidth=4, solid_capstyle="round"
        )

    # Cream muzzle and rosy cheeks.
    ax.add_patch(Ellipse(
        (0, 3.5), 1.25, 0.75,
        facecolor=cream, edgecolor="none"
    ))
    for x in (-1.15, 1.15):
        ax.add_patch(Ellipse(
            (x, 3.55), 0.55, 0.25,
            facecolor=pink, edgecolor="none", alpha=0.65
        ))

    # Big shiny eyes.
    for x in (-0.66, 0.66):
        ax.add_patch(Circle(
            (x, 4.08), 0.31, facecolor=outline, edgecolor="none"
        ))
        ax.add_patch(Circle(
            (x - 0.08, 4.18), 0.095,
            facecolor="white", edgecolor="none"
        ))
        ax.add_patch(Circle(
            (x + 0.09, 4.00), 0.04,
            facecolor="white", edgecolor="none"
        ))

    # Pink nose and a tiny smile.
    ax.add_patch(Polygon(
        [(-0.16, 3.73), (0.16, 3.73), (0, 3.55)],
        closed=True, facecolor=pink,
        edgecolor=outline, linewidth=1.5, joinstyle="round"
    ))
    ax.plot([0, 0], [3.55, 3.4], color=outline, linewidth=1.8)
    for x in (-0.18, 0.18):
        ax.add_patch(Arc(
            (x, 3.4), 0.36, 0.3,
            theta1=180, theta2=360,
            color=outline, linewidth=1.8
        ))

    # Whiskers.
    for side in (-1, 1):
        for offset in (-0.17, 0, 0.17):
            ax.plot(
                [side * 1.12, side * 2.35],
                [3.55 + offset, 3.55 + offset * 1.8],
                color=outline, linewidth=1.5, solid_capstyle="round"
            )

    # A few playful sparkles.
    ax.scatter(
        [-2.45, 2.45, -2.5], [5.2, 5.5, 2.1],
        s=[110, 85, 55], marker="*",
        color=pink, linewidths=0, zorder=0
    )

    plt.tight_layout()

    # Uncomment to save the picture:
    # fig.savefig("cute_kitten.png", dpi=200, bbox_inches="tight")

    plt.show()


if __name__ == "__main__":
    draw_kitten()
