import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
import numpy as np

def draw_kitten():
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FFF6EC')

    FUR    = '#F7C873'   # warm ginger
    FUR_D  = '#EDA94F'   # darker ginger (stripes, ears back)
    CREAM  = '#FFF1DC'   # muzzle / belly
    PINK   = '#F49CBB'   # nose, inner ears
    BLUSH  = '#F8A5B8'   # cheeks
    DARK   = '#4A3225'   # eyes, outlines

    # ---------- tail (behind body) ----------
    tail = Path([(7.6, 2.6), (9.6, 2.4), (9.9, 5.2), (8.2, 5.6)],
                [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4])
    ax.add_patch(mpatches.PathPatch(tail, fill=False, lw=14,
                                    color=FUR, capstyle='round'))
    # tail tip stripe
    tip = Path([(9.35, 4.6), (9.1, 5.2), (8.5, 5.5)],
               [Path.MOVETO, Path.CURVE3, Path.CURVE3])
    ax.add_patch(mpatches.PathPatch(tip, fill=False, lw=14,
                                    color=FUR_D, capstyle='round'))

    # ---------- body ----------
    ax.add_patch(mpatches.Ellipse((5, 3.2), 4.6, 3.8, facecolor=FUR,
                                  edgecolor='none'))
    ax.add_patch(mpatches.Ellipse((5, 2.9), 2.6, 2.4, facecolor=CREAM,
                                  edgecolor='none'))  # belly

    # ---------- paws ----------
    for x in (3.8, 6.2):
        ax.add_patch(mpatches.Ellipse((x, 1.55), 1.5, 0.8, facecolor=FUR,
                                      edgecolor='none'))
        ax.add_patch(mpatches.Ellipse((x, 1.5), 1.3, 0.6, facecolor=CREAM,
                                      edgecolor='none'))

    # ---------- ears ----------
    left_ear  = plt.Polygon([(3.1, 7.9), (2.5, 10.2), (4.6, 8.9)], color=FUR)
    right_ear = plt.Polygon([(6.9, 7.9), (7.5, 10.2), (5.4, 8.9)], color=FUR)
    ax.add_patch(left_ear); ax.add_patch(right_ear)
    ax.add_patch(plt.Polygon([(3.3, 8.2), (2.95, 9.6), (4.25, 8.75)], color=PINK))
    ax.add_patch(plt.Polygon([(6.7, 8.2), (7.05, 9.6), (5.75, 8.75)], color=PINK))

    # ---------- head ----------
    ax.add_patch(mpatches.Circle((5, 6.6), 2.35, facecolor=FUR, edgecolor='none'))

    # forehead stripes
    for dx in (-0.55, 0, 0.55):
        ax.plot([5+dx*0.9, 5+dx], [8.55, 8.0], color=FUR_D, lw=5,
                solid_capstyle='round')

    # ---------- eyes (big & sparkly) ----------
    for x in (4.0, 6.0):
        ax.add_patch(mpatches.Circle((x, 6.7), 0.5, facecolor=DARK))
        ax.add_patch(mpatches.Circle((x+0.16, 6.86), 0.18, facecolor='white'))
        ax.add_patch(mpatches.Circle((x-0.15, 6.5), 0.08, facecolor='white'))

    # ---------- muzzle ----------
    ax.add_patch(mpatches.Ellipse((4.55, 5.55), 1.15, 0.85, facecolor=CREAM))
    ax.add_patch(mpatches.Ellipse((5.45, 5.55), 1.15, 0.85, facecolor=CREAM))

    # nose
    ax.add_patch(plt.Polygon([(4.82, 5.85), (5.18, 5.85), (5, 5.55)],
                             color=PINK, joinstyle='round'))
    # mouth ("w")
    mouth_l = Path([(5, 5.55), (4.85, 5.3), (4.55, 5.35)],
                   [Path.MOVETO, Path.CURVE3, Path.CURVE3])
    mouth_r = Path([(5, 5.55), (5.15, 5.3), (5.45, 5.35)],
                   [Path.MOVETO, Path.CURVE3, Path.CURVE3])
    for m in (mouth_l, mouth_r):
        ax.add_patch(mpatches.PathPatch(m, fill=False, lw=3, color=DARK,
                                        capstyle='round'))

    # ---------- blush ----------
    for x in (3.15, 6.85):
        ax.add_patch(mpatches.Ellipse((x, 5.6), 0.85, 0.5, facecolor=BLUSH,
                                      alpha=0.6))

    # ---------- whiskers ----------
    for side in (-1, 1):
        cx = 5 + side*2.3
        for i, dy in enumerate((0.25, 0.0, -0.25)):
            slope = 0.12*(1-i) if side > 0 else -0.12*(1-i)
            ax.plot([cx, cx + side*1.5], [5.7+dy, 5.7+dy+slope+ (0.15*(1-i))],
                    color='#B8A48F', lw=2, solid_capstyle='round')

    ax.set_title('Meow!', fontsize=22, color='#8B5E3C', pad=12,
                 fontweight='bold')
    return fig

fig = draw_kitten()
plt.savefig('/tmp/kitten.png', dpi=120, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.show()