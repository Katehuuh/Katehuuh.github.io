"""Draw a cute kitten with matplotlib.

Run ``python cute_kitten.py`` to save ``cute_kitten.png``.
Add ``--show`` to open the drawing window as well.
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, PathPatch
from matplotlib.path import Path as MplPath


BACKGROUND = "#FFF9F3"
FUR = "#F3C39A"
FUR_DARK = "#D99A70"
CREAM = "#FFF1DE"
OUTLINE = "#66504A"
PINK = "#EFA3A6"
EYE = "#4B4042"


def path_patch(ax, vertices, codes, **kwargs):
    """Add a path to the axes and return it."""
    patch = PathPatch(MplPath(vertices, codes), **kwargs)
    ax.add_patch(patch)
    return patch


def stroke(ax, vertices, codes, color=OUTLINE, width=2, zorder=5):
    """Draw a rounded, unfilled Bezier stroke."""
    return path_patch(
        ax,
        vertices,
        codes,
        fill=False,
        edgecolor=color,
        linewidth=width,
        capstyle="round",
        joinstyle="round",
        zorder=zorder,
    )


def draw_kitten(ax):
    # Soft backdrop and ground shadow.
    ax.add_patch(Circle((5, 5.05), 4.35, facecolor="#FDEDE3", edgecolor="none", zorder=0))
    ax.add_patch(Ellipse((5, 0.72), 5.4, 0.55, facecolor="#DCCFC7", alpha=0.45, zorder=0))

    # Curled tail, drawn behind the body. Two strokes create a clean outline.
    tail_vertices = [
        (6.25, 2.65),
        (7.55, 1.95), (8.55, 2.85), (8.12, 4.05),
        (7.91, 4.73), (7.13, 4.73), (7.28, 4.16),
    ]
    tail_codes = [MplPath.MOVETO] + [MplPath.CURVE4] * 6
    stroke(ax, tail_vertices, tail_codes, width=25, zorder=1)
    stroke(ax, tail_vertices, tail_codes, color=FUR, width=18, zorder=1.1)
    stroke(
        ax,
        [(7.96, 3.48), (8.13, 3.50), (8.31, 3.57)],
        [MplPath.MOVETO, MplPath.CURVE3, MplPath.CURVE3],
        color=FUR_DARK,
        width=4,
        zorder=1.2,
    )
    stroke(
        ax,
        [(7.88, 3.88), (8.05, 3.91), (8.21, 4.00)],
        [MplPath.MOVETO, MplPath.CURVE3, MplPath.CURVE3],
        color=FUR_DARK,
        width=4,
        zorder=1.2,
    )

    # Body, creamy chest, and round little paws.
    ax.add_patch(Ellipse((5, 3.0), 4.0, 4.3, facecolor=FUR, edgecolor=OUTLINE, linewidth=2.2, zorder=2))
    ax.add_patch(Ellipse((5, 2.95), 2.5, 3.15, facecolor=CREAM, edgecolor="none", zorder=2.1))
    for x in (4.2, 5.8):
        ax.add_patch(Ellipse((x, 1.25), 1.75, 1.35, facecolor=FUR, edgecolor=OUTLINE, linewidth=2.0, zorder=3))
        for toe_x in (x - 0.23, x + 0.23):
            stroke(
                ax,
                [(toe_x, 1.38), (toe_x, 1.19), (toe_x, 1.05)],
                [MplPath.MOVETO, MplPath.CURVE3, MplPath.CURVE3],
                color=FUR_DARK,
                width=1.5,
                zorder=3.1,
            )

    # Ears with pink centers.
    left_ear = [
        (2.86, 7.55),
        (2.84, 8.30), (2.88, 9.03), (3.22, 9.25),
        (3.39, 9.36), (3.55, 9.18), (3.75, 9.00),
        (4.65, 8.05), (2.86, 7.55),
    ]
    left_codes = [
        MplPath.MOVETO,
        MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4,
        MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4,
        MplPath.LINETO, MplPath.CLOSEPOLY,
    ]
    right_ear = [(10 - x, y) for x, y in left_ear]
    for vertices in (left_ear, right_ear):
        path_patch(
            ax,
            vertices,
            left_codes,
            facecolor=FUR,
            edgecolor=OUTLINE,
            linewidth=2.2,
            joinstyle="round",
            zorder=3,
        )

    left_inner = [
        (3.15, 7.93),
        (3.12, 8.40), (3.16, 8.75), (3.32, 8.88),
        (3.51, 8.72), (3.78, 8.43), (4.10, 8.16),
        (3.15, 7.93),
    ]
    inner_codes = [
        MplPath.MOVETO,
        MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4,
        MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4,
        MplPath.CLOSEPOLY,
    ]
    for vertices in (left_inner, [(10 - x, y) for x, y in left_inner]):
        path_patch(ax, vertices, inner_codes, facecolor=PINK, edgecolor="none", zorder=3.1)

    # Round head with slightly chubby cheeks.
    head_vertices = [
        (5.0, 8.35),
        (3.55, 8.35), (2.55, 7.55), (2.50, 6.25),
        (2.45, 5.25), (2.95, 4.45), (3.80, 4.20),
        (4.25, 4.05), (4.60, 4.05), (5.00, 4.05),
        (5.40, 4.05), (5.75, 4.05), (6.20, 4.20),
        (7.05, 4.45), (7.55, 5.25), (7.50, 6.25),
        (7.45, 7.55), (6.45, 8.35), (5.00, 8.35),
        (5.00, 8.35),
    ]
    head_codes = [MplPath.MOVETO] + [MplPath.CURVE4] * 18 + [MplPath.CLOSEPOLY]
    path_patch(
        ax,
        head_vertices,
        head_codes,
        facecolor=FUR,
        edgecolor=OUTLINE,
        linewidth=2.3,
        joinstyle="round",
        zorder=4,
    )

    # Three soft tabby stripes on the forehead.
    forehead_strokes = [
        ([(4.30, 8.20), (4.33, 7.92), (4.52, 7.66)], [MplPath.MOVETO, MplPath.CURVE3, MplPath.CURVE3]),
        ([(5.00, 8.28), (5.00, 7.98), (5.00, 7.67)], [MplPath.MOVETO, MplPath.CURVE3, MplPath.CURVE3]),
        ([(5.70, 8.20), (5.67, 7.92), (5.48, 7.66)], [MplPath.MOVETO, MplPath.CURVE3, MplPath.CURVE3]),
    ]
    for vertices, codes in forehead_strokes:
        stroke(ax, vertices, codes, color=FUR_DARK, width=4.5, zorder=4.2)

    # Big shiny eyes.
    for x in (4.05, 5.95):
        ax.add_patch(Ellipse((x, 6.35), 1.05, 1.30, facecolor=EYE, edgecolor="none", zorder=5))
        ax.add_patch(Circle((x - 0.20, 6.66), 0.15, facecolor="white", edgecolor="none", zorder=5.1))
        ax.add_patch(Circle((x + 0.18, 6.08), 0.065, facecolor="white", edgecolor="none", zorder=5.1))

    # Blush and a pale, two-lobed muzzle.
    ax.add_patch(Ellipse((3.30, 5.47), 0.78, 0.34, angle=8, facecolor=PINK, alpha=0.55, edgecolor="none", zorder=4.8))
    ax.add_patch(Ellipse((6.70, 5.47), 0.78, 0.34, angle=-8, facecolor=PINK, alpha=0.55, edgecolor="none", zorder=4.8))
    for x in (4.57, 5.43):
        ax.add_patch(Ellipse((x, 5.18), 1.55, 1.15, facecolor=CREAM, edgecolor="none", zorder=4.7))

    # Tiny pink nose and a smiling mouth.
    nose_vertices = [
        (4.78, 5.58),
        (4.78, 5.73), (5.22, 5.73), (5.22, 5.58),
        (5.18, 5.43), (5.06, 5.32), (5.00, 5.28),
        (4.94, 5.32), (4.82, 5.43), (4.78, 5.58),
        (4.78, 5.58),
    ]
    nose_codes = [MplPath.MOVETO] + [MplPath.CURVE4] * 9 + [MplPath.CLOSEPOLY]
    path_patch(ax, nose_vertices, nose_codes, facecolor=PINK, edgecolor=OUTLINE, linewidth=1.4, zorder=5.2)
    stroke(ax, [(5, 5.29), (5, 5.19), (5, 5.10)], [MplPath.MOVETO, MplPath.CURVE3, MplPath.CURVE3], width=1.7, zorder=5.3)
    stroke(ax, [(5, 5.10), (4.86, 4.91), (4.60, 4.94), (4.51, 5.10)], [MplPath.MOVETO] + [MplPath.CURVE4] * 3, width=1.7, zorder=5.3)
    stroke(ax, [(5, 5.10), (5.14, 4.91), (5.40, 4.94), (5.49, 5.10)], [MplPath.MOVETO] + [MplPath.CURVE4] * 3, width=1.7, zorder=5.3)

    # Three gently curved whiskers on each cheek.
    left_whiskers = [
        [(3.65, 5.38), (3.10, 5.48), (2.52, 5.56), (1.95, 5.45)],
        [(3.62, 5.10), (3.04, 5.10), (2.47, 5.03), (1.90, 4.90)],
        [(3.70, 4.84), (3.15, 4.72), (2.65, 4.55), (2.15, 4.35)],
    ]
    for vertices in left_whiskers:
        codes = [MplPath.MOVETO] + [MplPath.CURVE4] * 3
        stroke(ax, vertices, codes, width=1.6, zorder=5.4)
        stroke(ax, [(10 - x, y) for x, y in vertices], codes, width=1.6, zorder=5.4)

    # A small floating heart finishes the illustration.
    heart_vertices = [
        (8.35, 7.15),
        (7.88, 7.40), (8.05, 7.82), (8.35, 7.55),
        (8.65, 7.82), (8.82, 7.40), (8.35, 7.15),
        (8.35, 7.15),
    ]
    heart_codes = [MplPath.MOVETO] + [MplPath.CURVE4] * 6 + [MplPath.CLOSEPOLY]
    path_patch(ax, heart_vertices, heart_codes, facecolor=PINK, edgecolor="none", zorder=1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="cute_kitten.png", help="image file to write")
    parser.add_argument("--show", action="store_true", help="also display the drawing window")
    args = parser.parse_args()

    fig = plt.figure(figsize=(8, 8), facecolor=BACKGROUND)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, 10), ylim=(0, 10))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_facecolor(BACKGROUND)

    draw_kitten(ax)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=200, facecolor=BACKGROUND)
    print(f"Saved kitten to {output.resolve()}")

    if args.show:
        plt.show()
    plt.close(fig)


if __name__ == "__main__":
    main()
