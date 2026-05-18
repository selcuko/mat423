"""Generate free_body.png for the README.

Run from the repo root:
    python figs/generate_free_body.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon


def main() -> None:
    fig, ax = plt.subplots(figsize=(5.5, 6.0))
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3.5, 3.5)
    ax.set_aspect("equal")
    ax.axis("off")

    body = Polygon(
        [(-0.45, -1.8), (0.45, -1.8), (0.45, 1.2), (0.0, 1.8), (-0.45, 1.2)],
        closed=True,
        facecolor="#dfe6ee",
        edgecolor="#1d232c",
        linewidth=1.5,
    )
    ax.add_patch(body)
    fin_left = Polygon(
        [(-0.45, -1.8), (-0.45, -1.2), (-0.95, -1.8)],
        closed=True,
        facecolor="#8b97a7",
        edgecolor="#1d232c",
        linewidth=1.2,
    )
    fin_right = Polygon(
        [(0.45, -1.8), (0.45, -1.2), (0.95, -1.8)],
        closed=True,
        facecolor="#8b97a7",
        edgecolor="#1d232c",
        linewidth=1.2,
    )
    ax.add_patch(fin_left)
    ax.add_patch(fin_right)

    flame = Polygon(
        [(-0.30, -1.8), (0.30, -1.8), (0.0, -2.7)],
        closed=True,
        facecolor="#f0883e",
        edgecolor="#f85149",
        linewidth=1.2,
        alpha=0.9,
    )
    ax.add_patch(flame)

    def arrow(x0, y0, x1, y1, color, label, label_xy):
        ax.add_patch(
            FancyArrowPatch(
                (x0, y0),
                (x1, y1),
                arrowstyle="-|>",
                mutation_scale=22,
                color=color,
                linewidth=2.2,
            )
        )
        ax.annotate(
            label,
            xy=label_xy,
            color=color,
            fontsize=14,
            fontweight="bold",
            ha="center",
            va="center",
        )

    # Thrust: from engine bell upward into the rocket body.
    arrow(0.0, -2.6, 0.0, -1.6, "#2ea043", r"Thrust $T(t)$", (1.05, -2.2))
    # Weight: from centre of mass straight down.
    arrow(0.0, 0.0, 0.0, -1.5, "#4f8ef7", r"Weight $m(t)\,g(y)$", (1.30, -0.75))
    # Drag: opposes velocity. Ascending → points downward.
    arrow(0.0, 1.8, 0.0, 0.6, "#f85149", r"Drag $D(y,v)$", (1.20, 1.3))
    # Velocity reference vector (up, ascending).
    ax.add_patch(
        FancyArrowPatch(
            (-1.8, -0.6),
            (-1.8, 0.6),
            arrowstyle="-|>",
            mutation_scale=18,
            color="#1d232c",
            linewidth=1.6,
        )
    )
    ax.annotate(
        r"$v$",
        xy=(-1.55, 0.55),
        color="#1d232c",
        fontsize=13,
        ha="left",
        va="center",
    )

    ax.set_title("Forces on the rocket (ascending)", fontsize=13, pad=8)

    out = Path(__file__).parent / "free_body.png"
    fig.savefig(out, dpi=160, bbox_inches="tight", facecolor="white")
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
