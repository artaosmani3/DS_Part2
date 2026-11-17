"""Gemeinsame Gestaltung: dieselben Farben für dieselben Gruppen in allen Notebooks und auf allen Folien."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

from src.daten import GRAFIKEN

# Farbe je Zimmerart (farbenblind-taugliche Palette, überall gleich)
FARBEN_ZIMMERART = {
    "Entire home/apt": "#1f5f8b",   # dunkelblau
    "Private room": "#d9822b",      # orange
    "Hotel room": "#5a9e6f",        # grün
    "Shared room": "#8c6bb1",       # violett
}
GRAU = "#6b7280"
AKZENT = "#b2182b"

PREIS_TICKS = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 50000, 100000]
PREIS_TICKS_WEIT = [10, 30, 100, 300, 1000, 3000, 10000, 30000, 100000]


def zahl(wert, nachkomma: int = 0) -> str:
    """Schweizer Tausendertrennzeichen: 37584 -> 37'584."""
    return f"{wert:,.{nachkomma}f}".replace(",", "'")


def stil():
    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams.update(
        {
            "figure.figsize": (8, 4.5),
            "figure.dpi": 110,
            "savefig.dpi": 200,
            "axes.titlesize": 13,
            "axes.labelsize": 11,
            "axes.titleweight": "bold",
        }
    )


def log_preisachse(ax, achse: str = "x", beschriftung: str = "Preis pro Nacht in EUR (log-Achse)"):
    """Logarithmische ACHSE: Die Werte bleiben unverändert, nur der Abstand auf dem Papier ändert sich."""
    formatierer = mticker.FuncFormatter(lambda v, _: zahl(v))
    if achse == "x":
        ax.set_xscale("log")
        unten, oben = ax.get_xlim()
        ticks = PREIS_TICKS_WEIT if oben / max(unten, 1e-9) > 300 else PREIS_TICKS
        ax.xaxis.set_major_locator(mticker.FixedLocator(ticks))
        ax.xaxis.set_major_formatter(formatierer)
        ax.xaxis.set_minor_formatter(mticker.NullFormatter())
        ax.set_xlabel(beschriftung)
    else:
        ax.set_yscale("log")
        unten, oben = ax.get_ylim()
        ticks = PREIS_TICKS_WEIT if oben / max(unten, 1e-9) > 300 else PREIS_TICKS
        ax.yaxis.set_major_locator(mticker.FixedLocator(ticks))
        ax.yaxis.set_major_formatter(formatierer)
        ax.yaxis.set_minor_formatter(mticker.NullFormatter())
        ax.set_ylabel(beschriftung)
    return ax


def speichere(fig, name: str) -> Path:
    GRAFIKEN.mkdir(parents=True, exist_ok=True)
    pfad = GRAFIKEN / f"{name}.png"
    fig.savefig(pfad, bbox_inches="tight")
    return pfad
