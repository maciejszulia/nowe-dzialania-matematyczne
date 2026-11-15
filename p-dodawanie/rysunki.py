"""Generuje rysunki SVG do README.

Uruchomienie: python3 rysunki.py
Wymaga bibliotek matplotlib i numpy.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np

from pdodawanie import padd, srednia_potegowa

KATALOG = Path(__file__).parent / "img"
PODGLAD = Path(sys.argv[1]) if len(sys.argv) > 1 else None  # opcjonalny katalog na podgląd PNG

TLO = "#fcfcfb"
TUSZ = "#0b0b0b"
TUSZ2 = "#52514e"
TUSZ3 = "#898781"
SIATKA = "#e1e0d9"
OS = "#c3c2b7"
NIEBIESKI = "#2a78d6"
NIEBIESKI_JASNY = "#cde2fb"
POMARANCZOWY = "#eb6834"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "mathtext.fontset": "dejavusans",
    "axes.edgecolor": OS,
    "axes.labelcolor": TUSZ2,
    "axes.titlecolor": TUSZ,
    "axes.titlesize": 11,
    "axes.titleweight": "regular",
    "axes.titlelocation": "left",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.color": TUSZ3,
    "ytick.color": TUSZ3,
    "xtick.labelcolor": TUSZ3,
    "ytick.labelcolor": TUSZ3,
    "grid.color": SIATKA,
    "grid.linewidth": 0.8,
    "figure.facecolor": TLO,
    "axes.facecolor": TLO,
    "savefig.facecolor": TLO,
    "svg.hashsalt": "p-dodawanie",
})

OBWODKA = [pe.withStroke(linewidth=3, foreground=TLO)]


def pl(x: float, miejsca: int = 3) -> str:
    """Liczba z przecinkiem dziesiętnym, bez zbędnych zer."""
    s = f"{x:.{miejsca}f}".rstrip("0").rstrip(".")
    return s.replace(".", ",").replace("-", "−")


def zapisz(fig, nazwa: str) -> None:
    KATALOG.mkdir(exist_ok=True)
    fig.savefig(KATALOG / f"{nazwa}.svg", metadata={"Date": None})
    if PODGLAD:
        PODGLAD.mkdir(parents=True, exist_ok=True)
        fig.savefig(PODGLAD / f"{nazwa}.png", dpi=110)
    plt.close(fig)


def punkt(ax, x, y, r=6):
    ax.plot([x], [y], "o", ms=r, mfc=NIEBIESKI, mec=TLO, mew=1.6, zorder=5)


def rys_wynik_vs_p(a=3.0, b=4.0):
    fig, ax = plt.subplots(figsize=(7.4, 4.0), layout="constrained")
    ujemne = np.linspace(-10, -0.02, 600)
    dodatnie = np.linspace(0.02, 10, 2000)
    ax.plot(ujemne, [padd(a, b, p=p) for p in ujemne], color=NIEBIESKI, lw=2, solid_capstyle="round")
    ax.plot(dodatnie, [min(padd(a, b, p=p), 50) for p in dodatnie], color=NIEBIESKI, lw=2)
    ax.axvline(0, color=OS, lw=1, ls=(0, (4, 4)))
    ax.plot([-10, 0], [min(a, b)] * 2, color=TUSZ3, lw=1, ls=(0, (6, 4)))
    ax.plot([0, 10], [max(a, b)] * 2, color=TUSZ3, lw=1, ls=(0, (6, 4)))
    ax.text(-9.8, min(a, b) + 0.22, f"min(a, b) = {pl(min(a, b))}", color=TUSZ2, fontsize=9)
    ax.text(9.9, max(a, b) - 0.55, f"max(a, b) = {pl(max(a, b))}", color=TUSZ2, fontsize=9, ha="right")
    ax.text(-0.25, 9.45, "p = 0: brak wyniku", color=TUSZ2, fontsize=9, ha="right")
    etykiety = {-2: (-0.35, -0.75, "right"), -1: (-0.35, -0.75, "right"), 1: (0.35, 0.15, "left"), 2: (0.35, 0.25, "left")}
    for p, (dx, dy, ha) in etykiety.items():
        w = padd(a, b, p=p)
        ax.plot([p, p], [0, w], color=OS, lw=0.8, ls=(0, (2, 3)), zorder=1)
        punkt(ax, p, w)
        ax.text(p + dx, w + dy, f"p = {pl(p)}:  {pl(w)}", color=TUSZ, fontsize=9, ha=ha, path_effects=OBWODKA, zorder=6)
    ax.set_xlim(-10, 10)
    ax.set_ylim(0, 10)
    ax.set_xticks([-10, -5, -2, -1, 0, 1, 2, 5, 10], ["−10", "−5", "−2", "−1", "0", "1", "2", "5", "10"])
    ax.set_yticks(range(0, 11, 2))
    ax.grid(axis="y")
    ax.set_axisbelow(True)
    ax.tick_params(length=3)
    ax.set_xlabel("parametr p")
    ax.set_title(rf"Wynik ${pl(a)} \oplus_{{p}}\, {pl(b)}$ w funkcji parametru p")
    zapisz(fig, "wynik-vs-p")


def rys_trojkat():
    fig, osie = plt.subplots(1, 2, figsize=(7.4, 3.5), layout="constrained")
    A, B, C = (4, 0), (0, 3), (0, 0)
    for ax in osie:
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-0.9, 4.6)
        ax.set_ylim(-0.75, 3.55)
        ax.plot([C[0], A[0], B[0], C[0]], [C[1], A[1], B[1], C[1]], color=TUSZ2, lw=1.2, solid_joinstyle="round")
        ax.text(2, -0.32, "4", color=TUSZ2, ha="center", va="center")
        ax.text(-0.28, 1.5, "3", color=TUSZ2, ha="center", va="center")

    ax = osie[0]
    ax.set_title("p = 2 i p = −2")
    D = (36 / 25, 48 / 25)
    ax.plot([A[0], B[0]], [A[1], B[1]], color=NIEBIESKI, lw=2.4, solid_capstyle="round")
    ax.plot([C[0], D[0]], [C[1], D[1]], color=NIEBIESKI, lw=2.4, solid_capstyle="round")
    k = 0.2  # znacznik kąta prostego przy D
    u = np.array([4, -3]) / 5
    n = np.array([-3, -4]) / 5
    q = np.array(D)
    ax.plot(*zip(q + k * u, q + k * u + k * n, q + k * n), color=TUSZ3, lw=0.9)
    ax.plot([0, 0.2, 0.2], [0.2, 0.2, 0], color=TUSZ3, lw=0.9)
    ax.text(2.25, 1.72, r"przeciwprostokątna" "\n" r"$3 \oplus_{2}\, 4 = 5$", color=TUSZ, fontsize=9.5, ha="left", va="bottom")
    ax.text(0.95, 0.72, r"wysokość" "\n" r"$3 \oplus_{-2}\, 4 = 2{,}4$", color=TUSZ, fontsize=9.5, ha="left", va="top",
            path_effects=OBWODKA)

    ax = osie[1]
    ax.set_title("p = 1 i p = −1")
    s = 12 / 7
    ax.fill([0, s, s, 0], [0, 0, s, s], color=NIEBIESKI_JASNY, lw=0)
    ax.plot([0, s, s, 0, 0], [0, 0, s, s, 0], color=NIEBIESKI, lw=1.6, solid_joinstyle="round")
    ax.plot([C[0], A[0]], [C[1], A[1]], color=NIEBIESKI, lw=2.4, solid_capstyle="round")
    ax.plot([C[0], B[0]], [C[1], B[1]], color=NIEBIESKI, lw=2.4, solid_capstyle="round")
    ax.text(s / 2, s / 2, r"bok kwadratu" "\n" r"$3 \oplus_{-1}\, 4 = 1{,}714$", color=TUSZ, fontsize=9.5, ha="center", va="center")
    ax.text(2.3, 1.72, r"suma przyprostokątnych" "\n" r"$3 \oplus_{1}\, 4 = 3 + 4 = 7$", color=TUSZ, fontsize=9.5, ha="left", va="bottom")
    zapisz(fig, "trojkat-3-4-5")


def rys_izolinie():
    fig, ax = plt.subplots(figsize=(5.4, 5.2), layout="constrained")
    kres = 3.0
    ax.set_aspect("equal")
    for p in (0.5, 1, 2):
        a = np.linspace(0, 1, 800)
        ax.plot(a, (1 - a ** p) ** (1 / p), color=NIEBIESKI, lw=2)
    ax.plot([1, 1, 0], [0, 1, 1], color=NIEBIESKI, lw=2, solid_joinstyle="round")
    for p in (-1, -2):
        a = np.linspace(1.0005, kres * 4, 6000)
        b = (1 - a ** p) ** (1 / p)
        ax.plot(a, b, color=POMARANCZOWY, lw=2)
    ax.plot([1, 1, kres * 4], [kres * 4, 1, 1], color=POMARANCZOWY, lw=2, solid_joinstyle="round")
    ax.plot([0, kres], [0, kres], color=OS, lw=0.8, ls=(0, (2, 3)), zorder=1)
    for p, t in ((1, "p = 1"), (2, "p = 2"), (np.inf, "p → +∞")):
        d = 1.0 if np.isinf(p) else 2 ** (-1 / p)
        ax.text(d - 0.05, d - 0.05, t, color=TUSZ, fontsize=9, ha="right", va="top", path_effects=OBWODKA, zorder=6)
    ax.text(0.30, 0.25, "p = 0,5", color=TUSZ, fontsize=9, ha="left", va="bottom", path_effects=OBWODKA, zorder=6)
    for p, t in ((-1, "p = −1"), (-2, "p = −2"), (-np.inf, "p → −∞")):
        d = 1.0 if np.isinf(p) else 2 ** (-1 / p)
        ax.text(d + 0.06, d + 0.06, t, color=TUSZ, fontsize=9, ha="left", va="bottom", path_effects=OBWODKA, zorder=6)
    ax.set_xlim(0, kres)
    ax.set_ylim(0, kres)
    ax.set_xticks([0, 1, 2, 3])
    ax.set_yticks([0, 1, 2, 3])
    ax.grid(True)
    ax.set_axisbelow(True)
    ax.tick_params(length=3)
    ax.set_xlabel("a")
    ax.set_ylabel("b", rotation=0, labelpad=10)
    ax.set_title(r"Izolinie: punkty (a, b), dla których $a \oplus_{p}\, b = 1$")
    uchwyty = [plt.Line2D([], [], color=NIEBIESKI, lw=2), plt.Line2D([], [], color=POMARANCZOWY, lw=2)]
    leg = ax.legend(uchwyty, ["p > 0", "p < 0"], loc="upper right", frameon=True, facecolor=TLO, edgecolor=SIATKA,
                    fontsize=9, labelcolor=TUSZ2, handlelength=1.6)
    leg.get_frame().set_linewidth(0.8)
    zapisz(fig, "izolinie")


def rys_srednia(a=3.0, b=4.0):
    fig, ax = plt.subplots(figsize=(7.4, 4.0), layout="constrained")
    ps = np.linspace(-10, 10, 1201)
    ax.plot(ps, [srednia_potegowa(a, b, p=float(p)) for p in ps], color=NIEBIESKI, lw=2)
    ax.axhline(min(a, b), color=TUSZ3, lw=1, ls=(0, (6, 4)))
    ax.axhline(max(a, b), color=TUSZ3, lw=1, ls=(0, (6, 4)))
    ax.text(9.9, min(a, b) + 0.035, f"min(a, b) = {pl(min(a, b))}", color=TUSZ2, fontsize=9, ha="right")
    ax.text(-9.9, max(a, b) - 0.075, f"max(a, b) = {pl(max(a, b))}", color=TUSZ2, fontsize=9)
    opisy = {
        -1: ("harmoniczna", -0.5, 0.04, "right", "bottom"),
        0: ("geometryczna", -0.5, 0.055, "right", "bottom"),
        1: ("arytmetyczna", 0.5, -0.045, "left", "top"),
        2: ("kwadratowa", 0.5, -0.035, "left", "top"),
    }
    for p, (nazwa, dx, dy, ha, va) in opisy.items():
        w = srednia_potegowa(a, b, p=p)
        punkt(ax, p, w)
        ax.text(p + dx, w + dy, f"p = {pl(p)}: {nazwa} {pl(w)}", color=TUSZ, fontsize=9, ha=ha, va=va,
                path_effects=OBWODKA, zorder=6)
    ax.set_xlim(-10, 10)
    ax.set_ylim(2.9, 4.1)
    ax.set_xticks([-10, -5, -2, -1, 0, 1, 2, 5, 10], ["−10", "−5", "−2", "−1", "0", "1", "2", "5", "10"])
    ax.set_yticks([3, 3.25, 3.5, 3.75, 4], ["3", "3,25", "3,5", "3,75", "4"])
    ax.grid(axis="y")
    ax.set_axisbelow(True)
    ax.tick_params(length=3)
    ax.set_xlabel("parametr p")
    ax.set_title(rf"Średnia potęgowa liczb {pl(a)} i {pl(b)} w funkcji parametru p")
    zapisz(fig, "srednia-potegowa")


TEKSTY_3D = {
    "pl": (r"Dla każdej pary $a, b > 0$: powierzchnia $p = 1$ leży nad powierzchnią $p = 2$," "\n"
           r"a powierzchnia $p = -1$ leży pod obiema", "powierzchnie-3d"),
    "en": (r"For every pair $a, b > 0$: the surface $p = 1$ lies above the surface $p = 2$," "\n"
           r"and the surface $p = -1$ lies below both", "powierzchnie-3d.en"),
}


def rys_powierzchnie_3d(jezyk: str = "pl"):
    """Powierzchnie a ⊕p b nad płaszczyzną (a, b) dla p = −1, 1, 2 (W4 i W5 w przestrzeni)."""
    tytul, plik = TEKSTY_3D[jezyk]
    os_ab = np.linspace(0.25, 5, 30)
    A, B = np.meshgrid(os_ab, os_ab)
    fig = plt.figure(figsize=(7.4, 6.0), layout="constrained")
    ax = fig.add_subplot(projection="3d")
    # matplotlib maluje powierzchnie w kolejności wywołań: od dolnej do górnej, bo kamera patrzy z góry
    warstwy = ((-1, POMARANCZOWY, 0.9), (2, "#8cbcf2", 0.9), (1, "#1b4f91", 0.42))
    for p, kolor, alfa in warstwy:
        Z = np.vectorize(lambda x, y: padd(x, y, p=p))(A, B)
        ax.plot_surface(A, B, Z, color=kolor, alpha=alfa, linewidth=0, antialiased=True, rasterized=True)
    ax.set_xlabel("a")
    ax.set_ylabel("b")
    ax.zaxis.set_rotate_label(False)
    ax.set_zlabel(r"$a \oplus_{p}\, b$", rotation=0, labelpad=10)
    ax.view_init(elev=20, azim=-125)
    uchwyty = [plt.Rectangle((0, 0), 1, 1, color=kolor, alpha=alfa) for _, kolor, alfa in reversed(warstwy)]
    leg = ax.legend(uchwyty, [f"p = {pl(p)}" for p, _, _ in reversed(warstwy)], loc="upper left", frameon=True,
                    facecolor=TLO, edgecolor=SIATKA, fontsize=9, labelcolor=TUSZ2)
    leg.get_frame().set_linewidth(0.8)
    ax.set_title(tytul, loc="left")
    zapisz(fig, plik)  # powierzchnie są rastrowane wewnątrz SVG, tekst zostaje wektorowy


if __name__ == "__main__":
    rys_wynik_vs_p()
    rys_trojkat()
    rys_izolinie()
    rys_srednia()
    rys_powierzchnie_3d("pl")
    rys_powierzchnie_3d("en")
    print("Zapisano rysunki w katalogu", KATALOG)
