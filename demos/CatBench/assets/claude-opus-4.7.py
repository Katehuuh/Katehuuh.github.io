"""Cute kitten in matplotlib — Claude Opus 4.7's take."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(6, 6), facecolor="#fdf6e3")
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_aspect("equal")
ax.set_facecolor("#fdf6e3")
ax.axis("off")

ax.add_patch(mpatches.Ellipse((5, 2.5), 4, 2.2, color="#ff9a4a", zorder=1))

t = np.linspace(0, 1, 50)
tail_x = 7 + 1.5 * np.sin(t * np.pi * 0.5)
tail_y = 2.5 + 2 * t
ax.plot(tail_x, tail_y, color="#ff9a4a", linewidth=10, solid_capstyle="round", zorder=2)

ax.add_patch(mpatches.Circle((5, 6), 2.0, color="#ffb060", zorder=3))

ax.add_patch(mpatches.Polygon([(3.4, 6.6), (3.2, 8.4), (4.4, 7.0)], color="#ffb060", zorder=3))
ax.add_patch(mpatches.Polygon([(6.6, 6.6), (6.8, 8.4), (5.6, 7.0)], color="#ffb060", zorder=3))
ax.add_patch(mpatches.Polygon([(3.6, 6.7), (3.5, 7.8), (4.2, 6.95)], color="#ff7a8a", zorder=4))
ax.add_patch(mpatches.Polygon([(6.4, 6.7), (6.5, 7.8), (5.8, 6.95)], color="#ff7a8a", zorder=4))

for x in (4.25, 5.75):
    ax.add_patch(mpatches.Ellipse((x, 6.0), 0.4, 0.55, color="#2c3e50", zorder=5))
    ax.add_patch(mpatches.Circle((x + 0.08, 6.15), 0.12, color="white", zorder=6))

ax.add_patch(mpatches.Polygon([(5, 5.4), (4.85, 5.55), (5.15, 5.55)], color="#ff7a8a", zorder=5))

ax.plot([5, 4.85, 4.7], [5.4, 5.2, 5.25], color="#3a2a1a", linewidth=1.5, solid_capstyle="round", zorder=5)
ax.plot([5, 5.15, 5.3], [5.4, 5.2, 5.25], color="#3a2a1a", linewidth=1.5, solid_capstyle="round", zorder=5)

for y in (5.55, 5.75):
    ax.plot([3.0, 4.2], [y, y - 0.05], color="#3a2a1a", linewidth=1, zorder=5)
    ax.plot([5.8, 7.0], [y - 0.05, y], color="#3a2a1a", linewidth=1, zorder=5)

ax.plot([4.5, 5, 5.5], [3.5, 3.7, 3.5], color="white", linewidth=2, zorder=2)

plt.tight_layout()
plt.show()
