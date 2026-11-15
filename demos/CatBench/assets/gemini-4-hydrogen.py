import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, PathPatch
from matplotlib.path import Path


def make_cubic_path(start, curves, closed=True):
    """Build a matplotlib Path from a start point and cubic Bezier segments."""
    verts = [start]
    codes = [Path.MOVETO]
    for c1, c2, end in curves:
        verts.extend([c1, c2, end])
        codes.extend([Path.CURVE4, Path.CURVE4, Path.CURVE4])
    if closed:
        verts.append(start)
        codes.append(Path.CLOSEPOLY)
    return Path(verts, codes)


def cubic_bezier(p0, p1, p2, p3, t):
    """Evaluate a cubic Bezier curve at parameter array t."""
    t = t[:, None]
    mt = 1.0 - t
    return (
        (mt**3) * p0
        + 3.0 * (mt**2) * t * p1
        + 3.0 * mt * (t**2) * p2
        + (t**3) * p3
    )


def cubic_bezier_deriv(p0, p1, p2, p3, t):
    """Evaluate the derivative of a cubic Bezier curve at parameter array t."""
    t = t[:, None]
    mt = 1.0 - t
    return (
        3.0 * (mt**2) * (p1 - p0)
        + 6.0 * mt * t * (p2 - p1)
        + 3.0 * (t**2) * (p3 - p2)
    )


def rotate_points(pts, angle_deg, origin=(0.0, 0.0)):
    """Rotate (N, 2) points around an origin by angle_deg counter-clockwise."""
    theta = np.radians(angle_deg)
    c, s = np.cos(theta), np.sin(theta)
    ox, oy = origin
    shifted = np.asarray(pts) - np.array([ox, oy])
    rot = np.column_stack([c * shifted[:, 0] - s * shifted[:, 1],
                           s * shifted[:, 0] + c * shifted[:, 1]])
    return rot + np.array([ox, oy])


def draw_heart(ax, x, y, size=0.35, color="#FF9AA2", angle=0, zorder=6.0):
    """Draw a cute smooth heart accent."""
    t = np.linspace(0, 2 * np.pi, 100)
    hx = 16 * np.sin(t) ** 3
    hy = (
        13 * np.cos(t)
        - 5 * np.cos(2 * t)
        - 2 * np.cos(3 * t)
        - np.cos(4 * t)
    )
    pts = np.column_stack([hx, hy]) / 16.0 * size
    pts = rotate_points(pts, angle) + np.array([x, y])
    ax.add_patch(Polygon(pts, closed=True, facecolor=color, edgecolor="none", zorder=zorder))


def draw_sparkle(ax, x, y, size=0.35, color="#F9E79F", zorder=6.0):
    """Draw a four-point sparkle accent."""
    s = size
    curves = [
        ((0.15 * s, 0.15 * s), (0.15 * s, 0.15 * s), (s, 0.0)),
        ((0.15 * s, -0.15 * s), (0.15 * s, -0.15 * s), (0.0, -s)),
        ((-0.15 * s, -0.15 * s), (-0.15 * s, -0.15 * s), (-s, 0.0)),
        ((-0.15 * s, 0.15 * s), (-0.15 * s, 0.15 * s), (0.0, s)),
    ]
    path = make_cubic_path((0.0, s), curves, closed=True)
    verts = path.vertices + np.array([x, y])
    ax.add_patch(
        PathPatch(Path(verts, path.codes), facecolor=color, edgecolor="none", zorder=zorder)
    )


def draw_kitten(save_path=None):
    # Color palette
    BG_CANVAS = "#FFF9F5"
    BACKDROP_COLOR = "#FEF0E6"
    CUSHION_FILL = "#FADBD8"
    CUSHION_EDGE = "#E6B0AA"
    SHADOW_COLOR = "#E6B0AA"

    FUR_BASE = "#F9CB9C"       # Soft peach-apricot
    FUR_STRIPE = "#E69138"     # Warm caramel tabby stripes
    CREAM = "#FFF7EC"          # Soft cream belly, paws, muzzle, tail tip
    PINK_EAR = "#F7A8B8"       # Pastel pink inner ear
    PINK_NOSE = "#F28B9C"      # Coral-pink nose
    BLUSH = "#FF9AA2"          # Cheek blush
    OUTLINE = "#4A2C2A"        # Warm dark brown outline

    COLLAR_FILL = "#5DADE2"    # Sky-blue collar
    BELL_GOLD = "#F4D03F"      # Golden bell
    BELL_DARK = "#7D6608"
    EYE_DARK = "#241914"
    EYE_AMBER = "#935116"

    fig, ax = plt.subplots(figsize=(8, 8), facecolor=BG_CANVAS)
    ax.set_facecolor(BG_CANVAS)
    ax.set_aspect("equal")
    ax.axis("off")

    # ---------------------------------------------------------
    # 1. Backdrop, cushion & ground shadow
    # ---------------------------------------------------------
    ax.add_patch(Circle((0.0, 0.2), 6.5, facecolor=BACKDROP_COLOR, edgecolor="none", zorder=0.5))
    ax.add_patch(
        Ellipse(
            (0.0, -4.45), 9.6, 2.3,
            facecolor=CUSHION_FILL, edgecolor=CUSHION_EDGE, linewidth=2.0, zorder=1.0
        )
    )
    ax.add_patch(
        Ellipse(
            (0.0, -4.25), 5.6, 1.15,
            facecolor=SHADOW_COLOR, alpha=0.55, edgecolor="none", zorder=1.2
        )
    )

    # ---------------------------------------------------------
    # 2. Fluffy curled tail (behind body)
    # ---------------------------------------------------------
    p0 = np.array([1.55, -3.55])
    p1 = np.array([3.60, -3.85])
    p2 = np.array([4.85, -2.55])
    p3 = np.array([3.85, -1.10])

    ts = np.linspace(0.0, 1.0, 90)
    pts = cubic_bezier(p0, p1, p2, p3, ts)
    tangents = cubic_bezier_deriv(p0, p1, p2, p3, ts)
    unit_t = tangents / np.linalg.norm(tangents, axis=1, keepdims=True)
    unit_n = np.column_stack([-unit_t[:, 1], unit_t[:, 0]])
    radii = 0.40 + 0.15 * np.sin(0.75 * np.pi * ts)

    left_side = pts + unit_n * radii[:, None]
    right_side = pts - unit_n * radii[:, None]

    end_pt = pts[-1]
    end_r = radii[-1]
    end_n_angle = np.arctan2(unit_n[-1, 1], unit_n[-1, 0])
    cap_angles = np.linspace(end_n_angle, end_n_angle - np.pi, 24)
    cap_pts = end_pt + end_r * np.column_stack([np.cos(cap_angles), np.sin(cap_angles)])

    tail_poly_pts = np.vstack([left_side, cap_pts[1:-1], right_side[::-1]])
    tail_fill = Polygon(tail_poly_pts, closed=True, facecolor=FUR_BASE, edgecolor="none", zorder=2.0)
    ax.add_patch(tail_fill)

    # Tail tabby stripes (clipped to tail)
    for t_val in [0.26, 0.46, 0.66]:
        t_arr = np.array([t_val])
        pt = cubic_bezier(p0, p1, p2, p3, t_arr)[0]
        tan = cubic_bezier_deriv(p0, p1, p2, p3, t_arr)[0]
        tan_angle = np.degrees(np.arctan2(tan[1], tan[0]))
        stripe = Ellipse(pt, width=0.25, height=1.6, angle=tan_angle, facecolor=FUR_STRIPE, edgecolor="none", zorder=2.1)
        ax.add_patch(stripe)
        stripe.set_clip_path(tail_fill)

    # Cream tail tip (clipped to tail)
    tail_tip = Circle((3.75, -0.85), 0.85, facecolor=CREAM, edgecolor="none", zorder=2.1)
    ax.add_patch(tail_tip)
    tail_tip.set_clip_path(tail_fill)

    # Tail outline
    ax.add_patch(
        Polygon(
            tail_poly_pts, closed=True, facecolor="none",
            edgecolor=OUTLINE, linewidth=2.4, joinstyle="round", zorder=2.2
        )
    )

    # ---------------------------------------------------------
    # 3. Ears (tucked just behind head)
    # ---------------------------------------------------------
    for side in [-1, 1]:
        ear_path = make_cubic_path(
            (side * 0.95, 3.75),
            [
                ((side * 1.55, 4.45), (side * 2.25, 5.05), (side * 2.55, 5.15)),
                ((side * 2.72, 5.20), (side * 2.88, 5.05), (side * 2.92, 4.65)),
                ((side * 3.02, 3.85), (side * 3.00, 2.85), (side * 2.75, 2.15)),
            ],
            closed=True,
        )
        ax.add_patch(
            PathPatch(
                ear_path, facecolor=FUR_BASE, edgecolor=OUTLINE,
                linewidth=2.4, joinstyle="round", zorder=2.5
            )
        )

        inner_ear_path = make_cubic_path(
            (side * 1.55, 3.88),
            [
                ((side * 1.92, 4.28), (side * 2.28, 4.62), (side * 2.48, 4.70)),
                ((side * 2.60, 4.74), (side * 2.68, 4.62), (side * 2.70, 4.35)),
                ((side * 2.76, 3.85), (side * 2.72, 3.38), (side * 2.64, 3.05)),
                ((side * 2.32, 3.42), (side * 1.95, 3.72), (side * 1.55, 3.88)),
            ],
            closed=True,
        )
        ax.add_patch(
            PathPatch(inner_ear_path, facecolor=PINK_EAR, edgecolor="none", zorder=2.6)
        )

    # ---------------------------------------------------------
    # 4. Sitting body, chest bib, stripes & paws
    # ---------------------------------------------------------
    theta = np.linspace(0, 2 * np.pi, 160)
    bx = 2.20 * np.cos(theta) * (1.0 - 0.22 * np.sin(theta))
    by = -2.30 + 1.85 * np.sin(theta) + 0.15 * (np.sin(theta) ** 2)
    body_pts = np.column_stack([bx, by])

    body_fill = Polygon(body_pts, closed=True, facecolor=FUR_BASE, edgecolor="none", zorder=3.0)
    ax.add_patch(body_fill)

    # Cream chest bib (clipped to body)
    chest_bib = Ellipse((0.0, -1.70), 1.95, 1.50, facecolor=CREAM, edgecolor="none", zorder=3.1)
    ax.add_patch(chest_bib)
    chest_bib.set_clip_path(body_fill)

    # Body side tabby stripes (clipped to body)
    for side in [-1, 1]:
        s1 = Ellipse((side * 2.05, -2.55), 1.15, 0.25, angle=side * 12, facecolor=FUR_STRIPE, edgecolor="none", zorder=3.1)
        s2 = Ellipse((side * 2.12, -3.02), 1.15, 0.25, angle=side * 8, facecolor=FUR_STRIPE, edgecolor="none", zorder=3.1)
        ax.add_patch(s1)
        ax.add_patch(s2)
        s1.set_clip_path(body_fill)
        s2.set_clip_path(body_fill)

    # Body outline
    ax.add_patch(
        Polygon(
            body_pts, closed=True, facecolor="none",
            edgecolor=OUTLINE, linewidth=2.4, joinstyle="round", zorder=3.2
        )
    )

    # Subtle sitting haunch curves
    for side in [-1, 1]:
        haunch_path = make_cubic_path(
            (side * 1.32, -3.78),
            [((side * 1.55, -3.50), (side * 1.72, -3.30), (side * 1.85, -3.10))],
            closed=False,
        )
        ax.add_patch(
            PathPatch(
                haunch_path, facecolor="none", edgecolor=OUTLINE,
                linewidth=2.0, capstyle="round", zorder=3.3
            )
        )

    # Hind paws (peeking out beside front paws)
    for side in [-1, 1]:
        hx, hy = side * 1.82, -4.10
        h_angle = -side * 10
        ax.add_patch(
            Ellipse(
                (hx, hy), 0.95, 0.62, angle=h_angle,
                facecolor=CREAM, edgecolor=OUTLINE, linewidth=2.2, zorder=3.5
            )
        )
        for dx in [-0.14, 0.14]:
            toe_pts = rotate_points([[dx, -0.29], [dx, -0.09]], h_angle) + np.array([hx, hy])
            ax.plot(
                toe_pts[:, 0], toe_pts[:, 1],
                color=OUTLINE, linewidth=1.8, solid_capstyle="round", zorder=3.6
            )

    # Front leg lines
    for side in [-1, 1]:
        ax.plot(
            [side * 0.28, side * 0.25], [-2.42, -3.82],
            color=OUTLINE, linewidth=2.1, solid_capstyle="round", zorder=3.6
        )
        ax.plot(
            [side * 1.12, side * 1.12], [-2.22, -3.82],
            color=OUTLINE, linewidth=2.1, solid_capstyle="round", zorder=3.6
        )

    # Front cream paws + toe lines
    for side in [-1, 1]:
        px, py = side * 0.68, -4.02
        ax.add_patch(
            Ellipse(
                (px, py), 0.96, 0.68,
                facecolor=CREAM, edgecolor=OUTLINE, linewidth=2.3, zorder=3.7
            )
        )
        for dx in [-0.14, 0.14]:
            ax.plot(
                [px + dx, px + dx], [py - 0.31, py - 0.09],
                color=OUTLINE, linewidth=1.8, solid_capstyle="round", zorder=3.8
            )

    # ---------------------------------------------------------
    # 5. Collar & Golden Bell
    # ---------------------------------------------------------
    collar_path = make_cubic_path(
        (-1.40, -0.78),
        [
            ((-0.65, -1.04), (0.65, -1.04), (1.40, -0.78)),
            ((1.48, -0.82), (1.48, -0.96), (1.40, -1.02)),
            ((0.65, -1.28), (-0.65, -1.28), (-1.40, -1.02)),
            ((-1.48, -0.96), (-1.48, -0.82), (-1.40, -0.78)),
        ],
        closed=True,
    )
    ax.add_patch(
        PathPatch(
            collar_path, facecolor=COLLAR_FILL, edgecolor=OUTLINE,
            linewidth=2.2, joinstyle="round", zorder=3.9
        )
    )

    # Bell ring & golden bell
    ax.add_patch(Circle((0.0, -1.23), 0.08, facecolor=BELL_GOLD, edgecolor=OUTLINE, linewidth=1.6, zorder=4.3))
    ax.add_patch(Circle((0.0, -1.48), 0.28, facecolor=BELL_GOLD, edgecolor=OUTLINE, linewidth=2.1, zorder=4.4))
    ax.plot([-0.15, 0.15], [-1.54, -1.54], color=BELL_DARK, linewidth=2.0, solid_capstyle="round", zorder=4.5)
    ax.add_patch(Circle((0.0, -1.54), 0.055, facecolor=BELL_DARK, edgecolor="none", zorder=4.5))
    ax.add_patch(Circle((-0.09, -1.39), 0.055, facecolor="#FEF9E7", edgecolor="none", zorder=4.5))

    # ---------------------------------------------------------
    # 6. Chubby Head & Tabby Markings
    # ---------------------------------------------------------
    hx = 3.10 * np.cos(theta) * (1.0 - 0.10 * np.sin(theta))
    hy = 1.60 + 2.55 * np.sin(theta)
    head_pts = np.column_stack([hx, hy])

    head_fill = Polygon(head_pts, closed=True, facecolor=FUR_BASE, edgecolor="none", zorder=4.0)
    ax.add_patch(head_fill)

    # Forehead stripes (clipped to head)
    center_stripe = Ellipse((0.0, 3.85), 0.24, 0.85, facecolor=FUR_STRIPE, edgecolor="none", zorder=4.1)
    ax.add_patch(center_stripe)
    center_stripe.set_clip_path(head_fill)

    for side in [-1, 1]:
        f_stripe = Ellipse(
            (side * 0.52, 3.82), 0.22, 0.72, angle=-side * 14,
            facecolor=FUR_STRIPE, edgecolor="none", zorder=4.1
        )
        ax.add_patch(f_stripe)
        f_stripe.set_clip_path(head_fill)

        # Cheek stripes
        c_s1 = Ellipse((side * 2.85, 1.55), 1.10, 0.22, angle=side * 8, facecolor=FUR_STRIPE, edgecolor="none", zorder=4.1)
        c_s2 = Ellipse((side * 2.82, 1.10), 1.05, 0.22, angle=side * 14, facecolor=FUR_STRIPE, edgecolor="none", zorder=4.1)
        ax.add_patch(c_s1)
        ax.add_patch(c_s2)
        c_s1.set_clip_path(head_fill)
        c_s2.set_clip_path(head_fill)

    # Head outline
    ax.add_patch(
        Polygon(
            head_pts, closed=True, facecolor="none",
            edgecolor=OUTLINE, linewidth=2.5, joinstyle="round", zorder=4.2
        )
    )

    # Soft cream muzzle patch
    ax.add_patch(Ellipse((0.0, 0.45), 1.72, 1.02, facecolor=CREAM, edgecolor="none", zorder=4.7))

    # ---------------------------------------------------------
    # 7. Expressive Eyes, Blush, Nose, Mouth & Whiskers
    # ---------------------------------------------------------
    # Rosy cheek blush
    for side in [-1, 1]:
        ax.add_patch(
            Ellipse(
                (side * 1.98, 0.76), 0.78, 0.44, angle=side * 6,
                facecolor=BLUSH, alpha=0.65, edgecolor="none", zorder=4.9
            )
        )

    # Big glossy kawaii eyes
    for side in [-1, 1]:
        ex, ey = side * 1.28, 1.35
        eye_patch = Ellipse((ex, ey), 1.16, 1.24, facecolor=EYE_DARK, edgecolor="none", zorder=5.0)
        ax.add_patch(eye_patch)

        # Warm amber lower iris glow (clipped to eye)
        iris_glow = Ellipse((ex, ey - 0.36), 0.88, 0.56, facecolor=EYE_AMBER, alpha=0.75, edgecolor="none", zorder=5.1)
        ax.add_patch(iris_glow)
        iris_glow.set_clip_path(eye_patch)

        # Crisp specular highlights (same direction for both eyes so gaze aligns)
        ax.add_patch(Circle((ex - 0.20, ey + 0.26), 0.20, facecolor="#FFFFFF", edgecolor="none", zorder=5.2))
        ax.add_patch(Circle((ex + 0.18, ey - 0.23), 0.095, facecolor="#FFFFFF", edgecolor="none", zorder=5.2))
        ax.add_patch(Circle((ex + 0.14, ey + 0.33), 0.055, facecolor="#FFFFFF", edgecolor="none", zorder=5.2))

        # Tiny cute eyebrows
        bt = np.linspace(-0.22, 0.22, 20)
        bx = ex + bt
        by = 2.25 - 0.55 * (bt**2) - side * 0.08 * bt
        ax.plot(bx, by, color=OUTLINE, linewidth=2.0, solid_capstyle="round", zorder=5.2)

    # Cute rounded pink nose
    nose_path = make_cubic_path(
        (0.0, 0.94),
        [
            ((0.14, 0.97), (0.25, 0.92), (0.18, 0.82)),
            ((0.12, 0.74), (0.04, 0.70), (0.0, 0.70)),
            ((-0.04, 0.70), (-0.12, 0.74), (-0.18, 0.82)),
            ((-0.25, 0.92), (-0.14, 0.97), (0.0, 0.94)),
        ],
        closed=True,
    )
    ax.add_patch(
        PathPatch(
            nose_path, facecolor=PINK_NOSE, edgecolor=OUTLINE,
            linewidth=1.8, joinstyle="round", zorder=5.2
        )
    )

    # Classic ":3" kitty smile
    ax.plot([0.0, 0.0], [0.70, 0.56], color=OUTLINE, linewidth=2.2, solid_capstyle="round", zorder=5.2)
    for side in [-1, 1]:
        smile_path = make_cubic_path(
            (0.0, 0.56),
            [((side * 0.06, 0.36), (side * 0.34, 0.32), (side * 0.46, 0.50))],
            closed=False,
        )
        ax.add_patch(
            PathPatch(
                smile_path, facecolor="none", edgecolor=OUTLINE,
                linewidth=2.2, capstyle="round", zorder=5.2
            )
        )

    # Delicate curved whiskers
    for side in [-1, 1]:
        whisker_specs = [
            ((side * 2.18, 0.95), (side * 3.00, 1.12), (side * 3.78, 1.05)),
            ((side * 2.25, 0.72), (side * 3.10, 0.78), (side * 3.90, 0.62)),
            ((side * 2.12, 0.48), (side * 2.95, 0.45), (side * 3.68, 0.18)),
        ]
        for w0, wc, w1 in whisker_specs:
            w_path = Path([w0, wc, w1], [Path.MOVETO, Path.CURVE3, Path.CURVE3])
            ax.add_patch(
                PathPatch(
                    w_path, facecolor="none", edgecolor=OUTLINE,
                    linewidth=1.8, capstyle="round", zorder=5.3
                )
            )

    # ---------------------------------------------------------
    # 8. Floating cute hearts & sparkles
    # ---------------------------------------------------------
    draw_heart(ax, -4.4, 3.6, size=0.36, color="#FF9AA2", angle=14)
    draw_heart(ax, -5.0, 2.6, size=0.22, color="#F5B7B1", angle=-10)
    draw_sparkle(ax, 4.4, 3.5, size=0.38, color="#F7DC6F")
    draw_sparkle(ax, 5.0, 2.5, size=0.20, color="#F9E79F")
    draw_sparkle(ax, 3.9, 4.3, size=0.18, color="#F5B7B1")

    ax.set_xlim(-6.8, 6.8)
    ax.set_ylim(-6.6, 7.0)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    if save_path:
        plt.savefig(save_path, dpi=300, facecolor=BG_CANVAS)

    plt.show()


if __name__ == "__main__":
    draw_kitten()
