"""Generate a guitar fretboard diagram in standard EADGBE tuning."""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from pathlib import Path

CHROMATIC = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Top to bottom: high E (string 1) → low E (string 6)
OPEN_STRINGS = ["E", "B", "G", "D", "A", "E"]
STRING_LABELS = ["e", "B", "G", "D", "A", "E"]  # lowercase e = high E convention
NUM_STRINGS = 6
NUM_FRETS = 12
FRET_MARKERS = {3, 5, 7, 9, 12}


def note_at_fret(open_note: str, fret: int) -> str:
    idx = (CHROMATIC.index(open_note) + fret) % 12
    return CHROMATIC[idx]


def build_fretboard() -> list[list[str]]:
    """Return notes grid [string][fret], including fret 0 (open) at index 0."""
    board: list[list[str]] = []
    for open_note in OPEN_STRINGS:
        row = [note_at_fret(open_note, fret) for fret in range(NUM_FRETS + 1)]
        board.append(row)
    return board


def draw_fretboard(output_path: Path) -> None:
    board = build_fretboard()
    total_frets = NUM_FRETS  # display columns 1..12 plus nut

    fig_w = 14
    fig_h = 4.5
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), facecolor="white")
    ax.set_facecolor("white")
    ax.set_xlim(-0.6, total_frets + 0.8)
    ax.set_ylim(-0.8, NUM_STRINGS - 0.2)
    ax.invert_yaxis()
    ax.axis("off")

    # Fret positions: 0 = nut, 1..12 = frets
    fret_x = list(range(total_frets + 1))

    # Strings (horizontal lines)
    for s in range(NUM_STRINGS):
        ax.plot(
            [0, total_frets],
            [s, s],
            color="#888888",
            linewidth=0.8,
            solid_capstyle="round",
            zorder=1,
        )

    # Nut (thick black line)
    ax.plot(
        [0, 0],
        [-0.35, NUM_STRINGS - 0.65],
        color="black",
        linewidth=6,
        solid_capstyle="butt",
        zorder=2,
    )

    # Fret wires
    for f in range(1, total_frets + 1):
        ax.plot(
            [f, f],
            [-0.35, NUM_STRINGS - 0.65],
            color="#BBBBBB",
            linewidth=1.2,
            zorder=2,
        )

    # Fret marker dots (inlays)
    for f in FRET_MARKERS:
        if f == 12:
            for s in (1.5, 3.5):
                ax.add_patch(
                    Circle(
                        (f, s),
                        radius=0.12,
                        facecolor="#D8D8D8",
                        edgecolor="none",
                        zorder=0,
                    )
                )
        else:
            ax.add_patch(
                Circle(
                    (f, 2.5),
                    radius=0.12,
                    facecolor="#D8D8D8",
                    edgecolor="none",
                    zorder=0,
                )
            )

    # Note circles
    circle_r = 0.28
    for s, row in enumerate(board):
        for f, note in enumerate(row):
            x = f if f > 0 else -0.02  # open strings slightly left of nut
            ax.add_patch(
                Circle(
                    (x, s),
                    radius=circle_r,
                    facecolor="black",
                    edgecolor="black",
                    zorder=3,
                )
            )
            ax.text(
                x,
                s,
                note,
                ha="center",
                va="center",
                color="white",
                fontsize=9 if len(note) <= 1 else 8,
                fontweight="bold",
                zorder=4,
            )

    # Fret numbers below
    for f in FRET_MARKERS:
        ax.text(
            f,
            NUM_STRINGS - 0.15,
            str(f),
            ha="center",
            va="top",
            fontsize=9,
            color="#333333",
        )

    # Open string / tuning labels on the left
    for s, label in enumerate(STRING_LABELS):
        ax.text(
            -0.48,
            s,
            label,
            ha="center",
            va="center",
            fontsize=10,
            color="#444444",
            fontstyle="italic",
        )

    ax.text(
        -0.48,
        -0.55,
        "EADGBE",
        ha="center",
        va="center",
        fontsize=8,
        color="#666666",
        rotation=0,
    )

    fig.tight_layout(pad=0.3)
    fig.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight",
        facecolor="white",
        edgecolor="none",
    )
    plt.close(fig)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "image.png"
    draw_fretboard(out)
