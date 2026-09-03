"""Draw a cute cartoon kitten with matplotlib.  Run: python kitten.py"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Ellipse, Polygon

# Palette
ORANGE = "#F7A94B"   # fur
DARK   = "#C9772A"   # outlines & stripes
CREAM  = "#FFF3DD"   # belly, muzzle, tail tip
PINK   = "#F7A1B8"   # ears, nose, cheeks, hearts
GREEN  = "#6FBF73"   # eyes
BROWN  = "#4A3223"   # pupils, mouth, whiskers
BG     = "#E7F3F8"

fig, ax = plt.subplots(figsize=(6, 6), facecolor=BG)
fig.subplots_adjust(0, 0, 1, 1)
ax.set(xlim=(0, 10), ylim=(0, 10), aspect="equal")
ax.axis("off")


def add(patch, z):
    patch.set_zorder(z)
    ax.add_patch(patch)


def line(p, q, color, lw, z):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw,
            solid_capstyle="round", zorder=z)


def on_head(deg):
    """Point on the head circle (centre (5, 6), radius 2.4) at a given angle."""
    a = np.deg2rad(deg)
    return 5 + 2.4 * np.cos(a), 6 + 2.4 * np.sin(a)


def bezier(p0, p1, p2, p3, n=120):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2, p3 = map(np.array, (p0, p1, p2, p3))
    pts = ((1 - t)**3 * p0 + 3 * (1 - t)**2 * t * p1
           + 3 * (1 - t) * t**2 * p2 + t**3 * p3)
    return pts[:, 0], pts[:, 1]


def heart(cx, cy, size):
    t = np.linspace(0, 2 * np.pi, 200)
    x = np.sin(t)**3
    y = (13*np.cos(t) - 5*np.cos(2*t) - 2*np.cos(3*t) - np.cos(4*t)) / 16
    ax.fill(cx + size * x, cy + size * y, color=PINK, zorder=0.5)


# Tail -- drawn first so the body hides its root
tx, ty = bezier((6.2, 2.2), (8.8, 1.2), (9.4, 4.6), (8.0, 5.4))
ax.plot(tx, ty, color=DARK, lw=24, solid_capstyle="round", zorder=1.0)
ax.plot(tx, ty, color=ORANGE, lw=20, solid_capstyle="round", zorder=1.1)
ax.plot(tx[-20:], ty[-20:], color=CREAM, lw=20, solid_capstyle="round", zorder=1.2)

# Body, belly, flank stripes
add(Ellipse((5, 3.2), 4.2, 3.6, fc=ORANGE, ec=DARK, lw=2), 2.0)
add(Ellipse((5, 2.85), 2.4, 2.3, fc=CREAM, ec="none"), 2.1)
for s in (-1, 1):
    line((5 + s*1.95, 3.5), (5 + s*1.45, 3.65), DARK, 5, 2.2)
    line((5 + s*1.95, 2.9), (5 + s*1.45, 3.05), DARK, 5, 2.2)

# Paws with little toes
for x in (4.0, 6.0):
    add(Ellipse((x, 1.7), 1.25, 0.8, fc=ORANGE, ec=DARK, lw=2), 3.0)
    for dx in (-0.2, 0.2):
        line((x + dx, 1.36), (x + dx, 1.6), DARK, 2, 3.1)

# Collar and bell
add(Arc((5, 3.95), 2.4, 1.4, theta1=175, theta2=365, color="#E0474C", lw=9), 3.5)
add(Circle((5, 3.2), 0.3, fc="#FFD23F", ec=DARK, lw=1.5), 3.6)
line((5, 3.22), (5, 3.02), DARK, 2, 3.7)
add(Circle((5, 3.02), 0.05, fc=DARK, ec="none"), 3.7)

# Head
add(Circle((5, 6.0), 2.4, fc=ORANGE, ec=DARK, lw=2), 5.0)

# Ears -- filled on top of the head so their outline flows into the head's
for s in (-1, 1):
    base_out, base_in = on_head(90 - s*62), on_head(90 - s*18)
    tip = (5 + s*1.95, 9.45)
    add(Polygon([base_out, tip, base_in], fc=ORANGE, ec="none"), 5.1)
    line(base_out, tip, DARK, 2, 5.2)
    line(tip, base_in, DARK, 2, 5.2)
    add(Polygon([(5 + s*1.95, 7.5), (5 + s*1.88, 8.95), (5 + s*1.0, 8.25)],
                fc=PINK, ec="none"), 5.3)

# Tabby "M", muzzle, blush
line((4.45, 7.5), (4.6, 8.05), DARK, 5, 5.4)
line((5.0, 7.6), (5.0, 8.25), DARK, 5, 5.4)
line((5.55, 7.5), (5.4, 8.05), DARK, 5, 5.4)
add(Ellipse((5, 5.15), 1.8, 0.95, fc=CREAM, ec="none"), 5.5)
for s in (-1, 1):
    add(Circle((5 + s*1.35, 5.45), 0.32, fc=PINK, ec="none", alpha=0.7), 5.6)

# Eyes
for ex in (4.15, 5.85):
    add(Ellipse((ex, 6.3), 0.95, 1.2, fc="white", ec=DARK, lw=1.5), 6.0)
    add(Circle((ex, 6.2), 0.36, fc=GREEN, ec="none"), 6.1)
    add(Ellipse((ex, 6.2), 0.34, 0.54, fc=BROWN, ec="none"), 6.2)
    add(Circle((ex - 0.13, 6.45), 0.11, fc="white", ec="none"), 6.3)
    add(Circle((ex + 0.10, 6.02), 0.05, fc="white", ec="none"), 6.3)

# Nose, mouth, whiskers
add(Polygon([(4.78, 5.5), (5.22, 5.5), (5.0, 5.22)], fc=PINK, ec="#E48AA2",
            lw=1.5, joinstyle="round"), 6.5)
line((5.0, 5.22), (5.0, 5.12), BROWN, 2, 6.5)
for cx in (4.8, 5.2):
    add(Arc((cx, 5.15), 0.4, 0.34, theta1=190, theta2=350, color=BROWN, lw=2), 6.5)
for s in (-1, 1):
    line((5 + s*0.75, 5.35), (5 + s*2.7, 5.7), BROWN, 1.5, 7.0)
    line((5 + s*0.8, 5.15), (5 + s*2.8, 5.15), BROWN, 1.5, 7.0)
    line((5 + s*0.75, 4.95), (5 + s*2.65, 4.6), BROWN, 1.5, 7.0)

# Floating hearts and a caption
heart(8.3, 7.9, 0.4)
heart(9.1, 8.9, 0.25)
heart(1.6, 8.6, 0.3)
ax.text(5, 0.5, "meow!", ha="center", va="center", fontsize=18,
        color=DARK, fontweight="bold")

# fig.savefig("kitten.png", dpi=200, facecolor=BG)
plt.show()
