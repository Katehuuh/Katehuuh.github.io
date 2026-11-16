import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

fig, ax = plt.subplots(figsize=(6, 7))
ax.set_xlim(-2, 2)
ax.set_ylim(-2.2, 2.4)
ax.set_aspect("equal")
ax.axis("off")
fig.patch.set_facecolor("#f7f3ee")
ax.set_facecolor("#f7f3ee")

# Body
body = patches.Ellipse((0, -0.85), 2.2, 1.9, facecolor="#f4c07a", edgecolor="#c48a4a", lw=2, zorder=1)
ax.add_patch(body)

# Head
head = patches.Circle((0, 0.55), 1.05, facecolor="#f6c98a", edgecolor="#c48a4a", lw=2, zorder=2)
ax.add_patch(head)

# Ears
left_ear = patches.Polygon([(-0.85, 1.15), (-0.45, 2.15), (-0.05, 1.25)], closed=True,
                           facecolor="#f6c98a", edgecolor="#c48a4a", lw=2, zorder=1)
right_ear = patches.Polygon([(0.85, 1.15), (0.45, 2.15), (0.05, 1.25)], closed=True,
                            facecolor="#f6c98a", edgecolor="#c48a4a", lw=2, zorder=1)
left_inner = patches.Polygon([(-0.72, 1.25), (-0.45, 1.95), (-0.18, 1.32)], closed=True,
                             facecolor="#f3a6b5", edgecolor="none", zorder=2)
right_inner = patches.Polygon([(0.72, 1.25), (0.45, 1.95), (0.18, 1.32)], closed=True,
                              facecolor="#f3a6b5", edgecolor="none", zorder=2)
ax.add_patch(left_ear)
ax.add_patch(right_ear)
ax.add_patch(left_inner)
ax.add_patch(right_inner)

# Cheeks
ax.add_patch(patches.Circle((-0.48, 0.35), 0.22, facecolor="#f7b3c0", edgecolor="none", alpha=0.7, zorder=3))
ax.add_patch(patches.Circle((0.48, 0.35), 0.22, facecolor="#f7b3c0", edgecolor="none", alpha=0.7, zorder=3))

# Eyes
ax.add_patch(patches.Ellipse((-0.38, 0.72), 0.38, 0.46, facecolor="white", edgecolor="#5a3a22", lw=1.5, zorder=3))
ax.add_patch(patches.Ellipse((0.38, 0.72), 0.38, 0.46, facecolor="white", edgecolor="#5a3a22", lw=1.5, zorder=3))
ax.add_patch(patches.Circle((-0.32, 0.68), 0.14, facecolor="#3d2a1a", zorder=4))
ax.add_patch(patches.Circle((0.44, 0.68), 0.14, facecolor="#3d2a1a", zorder=4))
ax.add_patch(patches.Circle((-0.28, 0.74), 0.05, facecolor="white", zorder=5))
ax.add_patch(patches.Circle((0.48, 0.74), 0.05, facecolor="white", zorder=5))

# Nose
nose = patches.Polygon([(0, 0.48), (-0.12, 0.36), (0.12, 0.36)], closed=True,
                       facecolor="#e07a8a", edgecolor="#c45a6a", lw=1, zorder=4)
ax.add_patch(nose)

# Mouth
mouth_x = np.linspace(-0.28, 0.28, 80)
mouth_y = -0.18 * np.cos(mouth_x / 0.28 * np.pi) + 0.28
ax.plot(mouth_x, mouth_y, color="#c45a6a", lw=1.8, zorder=4)
ax.plot([0, 0], [0.36, 0.28], color="#c45a6a", lw=1.5, zorder=4)

# Whiskers
for y, dy in [(0.42, 0.08), (0.34, 0.0), (0.26, -0.08)]:
    ax.plot([-0.18, -0.95], [y, y + dy], color="#8a6a4a", lw=1.2, zorder=4)
    ax.plot([0.18, 0.95], [y, y + dy], color="#8a6a4a", lw=1.2, zorder=4)

# Front paws
ax.add_patch(patches.Ellipse((-0.45, -1.55), 0.55, 0.38, facecolor="#f6c98a", edgecolor="#c48a4a", lw=1.5, zorder=3))
ax.add_patch(patches.Ellipse((0.45, -1.55), 0.55, 0.38, facecolor="#f6c98a", edgecolor="#c48a4a", lw=1.5, zorder=3))

# Tail
theta = np.linspace(0.2, 2.4, 60)
tail_x = 0.85 + 0.55 * np.cos(theta)
tail_y = -0.55 + 0.7 * np.sin(theta)
ax.plot(tail_x, tail_y, color="#e8b06a", lw=10, solid_capstyle="round", zorder=0)
ax.plot(tail_x, tail_y, color="#c48a4a", lw=1.5, solid_capstyle="round", zorder=0)

ax.set_title("meow", fontsize=16, color="#8a5a3a", pad=8)
plt.tight_layout()
plt.show()
