import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, PathPatch, Polygon
from matplotlib.path import Path


def draw_kitten():
    ink = "#633C38"
    fur = "#FFB778"
    cream = "#FFF0D7"
    pink = "#F394A5"
    stripe = "#E58B54"
    cx = 4.8

    fig, ax = plt.subplots(figsize=(6, 6), facecolor="#FFF3E9")
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set(xlim=(0, 10), ylim=(0, 10), aspect="equal")
    ax.axis("off")

    def oval(x, y, width, height, fill, edge="none"):
        ax.add_patch(Ellipse(
            (x, y), width, height,
            facecolor=fill, edgecolor=edge, linewidth=2.5,
        ))

    def curve(points, color=ink, width=2.5, fill="none"):
        # One starting point, then three points per cubic Bézier segment.
        codes = [Path.MOVETO] + [Path.CURVE4] * (len(points) - 1)
        ax.add_patch(PathPatch(
            Path(points, codes), facecolor=fill, edgecolor=color,
            linewidth=width, capstyle="round", joinstyle="round",
        ))

    # Ground shadow and tail. Two strokes give the tail a soft outline.
    oval(5.1, 1.23, 6.2, 0.55, "#F2D7C9")
    tail = [
        (6.05, 2.65),
        (7.25, 1.92), (8.55, 2.73), (8.43, 3.83),
        (8.35, 4.58), (7.62, 4.62), (7.58, 4.07),
    ]
    curve(tail, width=25)
    curve(tail, color=fur, width=20)

    # Body, cream bib, and front paws.
    oval(cx, 3.12, 3.3, 3.5, fur, ink)
    oval(cx, 3.22, 2.02, 2.55, cream)
    for x in (cx - 0.74, cx + 0.74):
        oval(x, 1.65, 1.32, 0.82, fur, ink)
        for dx in (-0.16, 0.16):
            ax.plot([x + dx, x + dx], [1.29, 1.46],
                    color=stripe, lw=1.6, solid_capstyle="round")

    # Mirror the ears, then draw the head over their bases.
    for side in (-1, 1):
        for points, fill, edge in (
            ([(2.02, 6.55), (2.22, 8.72), (0.30, 7.22)], fur, ink),
            ([(1.86, 7.03), (1.93, 8.15), (0.83, 7.38)], pink, "none"),
        ):
            ax.add_patch(Polygon(
                [(cx + side * x, y) for x, y in points],
                facecolor=fill, edgecolor=edge, linewidth=2.5,
                joinstyle="round",
            ))
    oval(cx, 5.85, 4.9, 3.66, fur, ink)

    # Forehead stripes.
    for dx in (-0.52, 0, 0.52):
        curve([
            (cx + 1.2 * dx, 7.42), (cx + 1.13 * dx, 7.24),
            (cx + dx, 7.10), (cx + 0.92 * dx, 6.98 if dx else 6.88),
        ], color=stripe, width=5)

    # Eyes, catchlights, rosy cheeks, and whiskers.
    for side in (-1, 1):
        x = cx + side
        oval(x, 5.84, 0.77, 1.02, ink)
        oval(x - 0.13, 6.03, 0.25, 0.25, "white")
        oval(x + 0.14, 5.68, 0.10, 0.10, "white")
        oval(cx + side * 1.56, 5.18, 0.59, 0.30, pink)

        for y0, y1 in ((5.28, 5.52), (5.06, 4.98)):
            ax.plot([cx + side * 1.98, cx + side * 3.13], [y0, y1],
                    color=ink, lw=1.5, solid_capstyle="round")

    # Muzzle, little smile, and pink nose.
    oval(cx - 0.24, 5.01, 0.84, 0.62, cream)
    oval(cx + 0.24, 5.01, 0.84, 0.62, cream)
    for side in (-1, 1):
        curve([
            (cx, 5.09), (cx, 4.77),
            (cx + side * 0.28, 4.72), (cx + side * 0.40, 4.89),
        ], width=1.8)

    curve([
        (cx - 0.27, 5.31),
        (cx - 0.24, 5.44), (cx + 0.24, 5.44), (cx + 0.27, 5.31),
        (cx + 0.25, 5.19), (cx + 0.08, 5.06), (cx, 5.06),
        (cx - 0.08, 5.06), (cx - 0.25, 5.19), (cx - 0.27, 5.31),
    ], width=1.6, fill=pink)

    ax.scatter([1.55, 8.17], [7.1, 7.5],
               marker="*", s=[140, 200], color="#F0BA72")

    # Uncomment to save a copy:
    # fig.savefig("kitten.png", dpi=200, facecolor=fig.get_facecolor())
    plt.show()


if __name__ == "__main__":
    draw_kitten()
