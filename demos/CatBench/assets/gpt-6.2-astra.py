import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, PathPatch
from matplotlib.path import Path

fig, ax = plt.subplots(figsize=(6, 6), facecolor="#eaf7f3")
ax.set(xlim=(-2.65, 2.65), ylim=(-2.25, 2.95), aspect="equal")
ax.axis("off")

fur = "#f6bb79"
cream = "#fff0d5"
ink = "#503b38"
pink = "#f3a6ad"
stripe = "#cf8550"


def oval(x, y, width, height, fill, edge="none"):
    ax.add_patch(Ellipse((x, y), width, height,
                         facecolor=fill, edgecolor=edge, linewidth=2))


def curve(points, color=ink, width=2, fill="none"):
    """Draw a smooth path: a start point followed by (control, end) pairs."""
    codes = [Path.MOVETO] + [Path.CURVE3] * (len(points) - 1)
    ax.add_patch(PathPatch(Path(points, codes), facecolor=fill,
                           edgecolor=color, linewidth=width,
                           capstyle="round", joinstyle="round"))


# Shadow and curled tail, tucked behind the body
oval(0, -1.87, 2.8, 0.24, "#cddfd8")
tail = [(0.7, -1.42), (2.15, -1.82), (2.10, -0.51),
        (2.07, 0.06), (1.76, -0.08)]
curve(tail, ink, 25)
curve(tail, fur, 20)

# Belly and little paws
oval(0, -0.85, 2.05, 1.98, fur, ink)
oval(0, -0.95, 1.34, 1.48, cream)
for x in (-0.57, 0.57):
    oval(x, -1.67, 0.80, 0.44, fur, ink)
    for dx in (-0.12, 0.10):
        curve([(x + dx, -1.72), (x + dx - 0.03, -1.78),
               (x + dx - 0.02, -1.83)], stripe, 1.5)

# One continuous outline for the round cheeks and pointy ears
head = [(0, -0.49),
        (-1.57, -0.49), (-1.48, 0.96),
        (-1.45, 1.25), (-1.42, 1.46),
        (-1.53, 2.63), (-1.34, 2.54),
        (-0.98, 2.33), (-0.60, 1.84),
        (0, 2.02), (0.60, 1.84),
        (0.98, 2.33), (1.34, 2.54),
        (1.53, 2.63), (1.42, 1.46),
        (1.45, 1.25), (1.48, 0.96),
        (1.57, -0.49), (0, -0.49)]
curve(head, fill=fur)

# Tabby stripes
for x in (-0.32, 0, 0.32):
    curve([(x, 1.80), (x, 1.62), (0.8 * x, 1.43 + abs(x) / 3)], stripe, 4)

oval(0, 0.30, 0.94, 0.44, cream)  # muzzle
for s in (-1, 1):
    ear = [(s * 1.29, 2.29), (s * 0.84, 1.81), (s * 1.27, 1.57)]
    ax.add_patch(Polygon(ear, facecolor=pink, edgecolor="none"))

    x = s * 0.56
    oval(x, 0.85, 0.43, 0.52, ink)
    oval(x - 0.065, 0.95, 0.13, 0.13, "white")  # eye sparkle
    oval(x + 0.065, 0.79, 0.055, 0.055, "white")
    oval(s * 0.99, 0.38, 0.46, 0.23, pink)

    curve([(0, 0.30), (s * 0.09, 0.08), (s * 0.27, 0.22)], width=1.8)
    for dy in (-0.14, 0.14):
        curve([(s * 0.88, 0.35 + dy / 3), (s * 1.35, 0.35 + dy),
               (s * 1.87, 0.35 + 1.6 * dy)], width=1.5)

# Button nose
ax.add_patch(Polygon([(-0.14, 0.45), (0.14, 0.45), (0, 0.29)],
                     facecolor=pink, edgecolor=ink, linewidth=1.5,
                     joinstyle="round"))

fig.tight_layout(pad=0.3)
# fig.savefig("kitten.png", dpi=200)  # Uncomment to save the drawing.
plt.show()
