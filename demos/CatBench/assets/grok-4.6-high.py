import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-5.5, 5.5)
ax.set_ylim(-3.5, 7)
ax.set_aspect("equal")
ax.axis("off")
fig.patch.set_facecolor("#FFF8F0")

fur = "#FFDAB9"
outline = "#CD853F"
lw = 1.8

# Tail (behind body)
tail = patches.Ellipse(
    (2.15, -0.7), 2.9, 0.75, angle=28,
    facecolor=fur, edgecolor=outline, linewidth=lw, zorder=1
)
ax.add_patch(tail)

# Body
body = patches.Ellipse(
    (0, 0.1), 3.6, 4.6,
    facecolor=fur, edgecolor=outline, linewidth=lw, zorder=2
)
ax.add_patch(body)

# Paws
for x in (-1.15, 1.15):
    paw = patches.Ellipse(
        (x, -2.05), 1.25, 0.85,
        facecolor=fur, edgecolor=outline, linewidth=lw, zorder=3
    )
    ax.add_patch(paw)

# Head
head = patches.Circle(
    (0, 2.85), 2.05,
    facecolor=fur, edgecolor=outline, linewidth=lw, zorder=4
)
ax.add_patch(head)

# Outer ears
left_ear = patches.Polygon(
    [(-1.55, 4.35), (-2.35, 6.25), (-0.45, 4.7)],
    closed=True, facecolor=fur, edgecolor=outline, linewidth=lw, zorder=5
)
right_ear = patches.Polygon(
    [(1.55, 4.35), (2.35, 6.25), (0.45, 4.7)],
    closed=True, facecolor=fur, edgecolor=outline, linewidth=lw, zorder=5
)
ax.add_patch(left_ear)
ax.add_patch(right_ear)

# Inner ears
left_inner = patches.Polygon(
    [(-1.45, 4.5), (-2.05, 5.85), (-0.7, 4.75)],
    closed=True, facecolor="#FFB6C1", edgecolor="none", zorder=6
)
right_inner = patches.Polygon(
    [(1.45, 4.5), (2.05, 5.85), (0.7, 4.75)],
    closed=True, facecolor="#FFB6C1", edgecolor="none", zorder=6
)
ax.add_patch(left_inner)
ax.add_patch(right_inner)

# Blush
for x in (-1.35, 1.35):
    blush = patches.Ellipse(
        (x, 2.55), 0.75, 0.28,
        facecolor="#FFB6C1", alpha=0.55, edgecolor="none", zorder=7
    )
    ax.add_patch(blush)

# Eyes (big sparkly black for extra cuteness)
for x in (-0.78, 0.78):
    eye = patches.Circle((x, 3.12), 0.58, facecolor="black", zorder=8)
    ax.add_patch(eye)
    # Highlights
    ax.add_patch(patches.Circle((x - 0.18, 3.28), 0.2, facecolor="white", zorder=9))
    ax.add_patch(patches.Circle((x + 0.16, 3.02), 0.09, facecolor="white", zorder=9))

# Nose
nose = patches.Polygon(
    [(-0.22, 2.42), (0.22, 2.42), (0, 2.18)],
    closed=True, facecolor="#FF69B4", edgecolor="#C71585", linewidth=1, zorder=10
)
ax.add_patch(nose)

# Mouth
ax.plot([0, 0], [2.18, 2.02], color="black", lw=1.4, zorder=10)
ax.plot([-0.38, 0, 0.38], [2.12, 1.92, 2.12], color="black", lw=1.6, solid_capstyle="round", zorder=10)

# Whiskers
whisker_style = dict(color="#5C4033", lw=1.1, solid_capstyle="round", zorder=11)
ax.plot([-2.55, -1.15], [2.72, 2.68], **whisker_style)
ax.plot([-2.65, -1.15], [2.48, 2.50], **whisker_style)
ax.plot([-2.50, -1.15], [2.24, 2.32], **whisker_style)
ax.plot([2.55, 1.15], [2.72, 2.68], **whisker_style)
ax.plot([2.65, 1.15], [2.48, 2.50], **whisker_style)
ax.plot([2.50, 1.15], [2.24, 2.32], **whisker_style)

plt.tight_layout()
plt.show()
