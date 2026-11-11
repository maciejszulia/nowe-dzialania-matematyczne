"""Testy p-dodawania. Każdy przykład liczbowy z README ma tutaj test.

Uruchomienie: python3 -m pytest -q
"""

import math
import random

import pytest

from pdodawanie import dopasuj_p, padd, srednia_potegowa

BLISKO = dict(rel_tol=1e-9, abs_tol=1e-12)


def blisko(x, y, **kw):
    return math.isclose(x, y, **(BLISKO | kw))


# --- przykłady z README -----------------------------------------------------

@pytest.mark.parametrize(
    "a, b, p, wynik",
    [
        (6, 3, 1, 9),                # rezystory szeregowo [Ω]
        (3, 4, 2, 5),                # przeciwprostokątna; niepewności [mm]
        (6, 3, -1, 2),               # rezystory równolegle [Ω]
        (3, 4, -2, 2.4),             # Kv szeregowo [m³/h]; wysokość trójkąta 3-4-5
        (3, 4, 1, 7),                # suma przyprostokątnych
        (3, 4, -1, 12 / 7),          # bok kwadratu wpisanego w trójkąt 3-4-5
        (5, 7, -1, 35 / 12),         # czas wspólnej pracy [h]
        (8, 21, -1, 168 / 29),       # efektywny okres półtrwania [d]
        (300, 150, -1, 100),         # równanie soczewki cienkiej [mm]
        (2, 3, -1, 1.2),             # masa zredukowana [kg]
        (3, 4, 2, 5),                # moc pozorna [kVA] z mocy czynnej i biernej
        (1, 1, 3, 2 ** (1 / 3)),     # promień kropli po połączeniu [mm]
    ],
)
def test_przyklady(a, b, p, wynik):
    assert blisko(padd(a, b, p=p), wynik)


def test_przyklady_zaokraglone():
    assert round(padd(3, 4, p=10), 3) == 4.022
    assert round(padd(3, 4, p=-10), 3) == 2.984
    assert round(padd(3, 4, p=0.5), 3) == 13.928
    assert round(padd(3, 4, p=-0.5), 3) == 0.862
    assert round(padd(8, 21, p=-1), 2) == 5.79
    assert round(padd(5, 7, p=-1), 2) == 2.92


def test_rury_rownolegle_20_mm():
    assert round(padd(20, 20, p=2), 2) == 28.28      # równe pole przekroju
    assert round(padd(20, 20, p=2.5), 2) == 26.39    # przepływ burzliwy, równe λ i L
    assert round(padd(20, 20, p=4), 2) == 23.78      # przepływ laminarny, równe L


def test_opory_kwadratowe_rownolegle():
    # Δp = k·Q²; 2 równe gałęzie równoległe dają k/4.
    assert blisko(padd(8, 8, p=-0.5), 2)


def test_kv_w_l_na_min():
    # 3 m³/h = 50 l/min, 4 m³/h = 200/3 l/min, 2,4 m³/h = 40 l/min
    assert blisko(padd(50, 200 / 3, p=-2), 40)


def test_przyklady_z_tabel_readme():
    assert blisko(padd(0.03, 0.04, p=2), 0.05)                 # tolerancje [mm]
    assert round(padd(1, 1, p=2), 3) == 1.414                  # 2 niespójne sygnały [V]
    assert blisko(padd(3, 4, p=-2), 2.4)                       # 2 lampy: 3 m i 4 m
    assert round(dopasuj_p(20, 20, 26.39), 3) == 2.5           # rozpoznanie prawa z pomiaru


def test_powtorzenie():
    # n równych argumentów daje n^(1/p)·a
    assert blisko(padd(1, 1, 1, 1, p=2), 2)                    # 4 równe niepewności dają 2·u
    assert blisko(padd(10, 10, p=-1), 5)                       # 2 równe rezystory dają R/2
    for n in (2, 3, 7):
        for p in (-3, -1, 0.5, 2, 4):
            assert blisko(padd(*([2.5] * n), p=p), n ** (1 / p) * 2.5)


def test_zwiazek_ze_srednia_potegowa(probki):
    for a, b, _, p in probki:
        if 0.05 < abs(p) < 20:
            assert blisko(srednia_potegowa(a, b, p=p), 2 ** (-1 / p) * padd(a, b, p=p))


def test_trzy_argumenty():
    assert blisko(padd(3, 4, 12, p=2), 13)            # przekątna prostopadłościanu
    assert blisko(padd(6, 3, 2, p=-1), 1)             # 3 rezystory równolegle


# --- własności ---------------------------------------------------------------

@pytest.fixture(scope="module")
def probki():
    rng = random.Random(20261111)
    out = []
    for _ in range(400):
        a, b, c = (10 ** rng.uniform(-3, 3) for _ in range(3))
        p = rng.choice([-1, 1]) * 10 ** rng.uniform(-1, 1.3)
        out.append((a, b, c, p))
    return out


def test_przemiennosc(probki):
    for a, b, _, p in probki:
        assert blisko(padd(a, b, p=p), padd(b, a, p=p))


def test_lacznosc(probki):
    for a, b, c, p in probki:
        lewa = padd(padd(a, b, p=p), c, p=p)
        prawa = padd(a, padd(b, c, p=p), p=p)
        assert blisko(lewa, prawa) and blisko(lewa, padd(a, b, c, p=p))


def test_jednorodnosc(probki):
    for a, b, c, p in probki:
        assert blisko(c * padd(a, b, p=p), padd(c * a, c * b, p=p))


def test_dwoistosc(probki):
    for a, b, _, p in probki:
        assert blisko(padd(a, b, p=p) * padd(a, b, p=-p), a * b)


def test_ograniczenia(probki):
    # Matematycznie nierówności są ostre. Zaokrąglenie typu float dopuszcza równość.
    for a, b, _, p in probki:
        w = padd(a, b, p=p)
        assert w >= max(a, b) if p > 0 else w <= min(a, b)
    assert padd(3, 4, p=2) > 4 and padd(3, 4, p=-2) < 3


def test_wynik_maleje_gdy_p_rosnie():
    for ps in ([0.1, 0.5, 1, 2, 5, 50], [-50, -5, -2, -1, -0.5, -0.1]):
        wyniki = [padd(3, 4, p=p) for p in ps]
        assert wyniki == sorted(wyniki, reverse=True)


def test_granice():
    assert blisko(padd(3, 4, p=1e3), 4, rel_tol=1e-3)
    assert blisko(padd(3, 4, p=-1e3), 3, rel_tol=1e-3)
    assert padd(3, 4, p=math.inf) == 4 and padd(3, 4, p=-math.inf) == 3
    assert padd(3, 4, p=1e-3) > 1e300 and padd(3, 4, p=-1e-3) < 1e-300
    assert padd(3, 4, p=1e-6) == math.inf and padd(3, 4, p=-1e-6) == 0.0


def test_duze_wartosci_bez_przepelnienia():
    assert blisko(padd(1e200, 1e200, p=3), 1e200 * 2 ** (1 / 3))
    assert blisko(padd(1e-200, 1e-200, p=-3), 1e-200 * 2 ** (-1 / 3))


def test_skala_logarytmiczna(probki):
    # ln(a ⊕ₚ b) = h·ln(e^(x/h) + e^(y/h)) dla x = ln a, y = ln b, h = 1/p
    for a, b, _, p in probki:
        h, x, y = 1 / p, math.log(a), math.log(b)
        m = max(x / h, y / h)
        poziom = h * (m + math.log(math.exp(x / h - m) + math.exp(y / h - m)))
        assert blisko(math.log(padd(a, b, p=p)), poziom, abs_tol=1e-9)


def test_bledne_dane():
    for zle in [dict(x=(3, 4), p=0), dict(x=(3, -4), p=2), dict(x=(0, 4), p=2), dict(x=(3,), p=2),
                dict(x=(3, math.inf), p=2), dict(x=(3, 4), p=math.nan)]:
        with pytest.raises(ValueError):
            padd(*zle["x"], p=zle["p"])


# --- średnia potęgowa --------------------------------------------------------

def test_srednie_3_i_4():
    assert blisko(srednia_potegowa(3, 4, p=-1), 24 / 7)          # harmoniczna
    assert blisko(srednia_potegowa(3, 4, p=0), math.sqrt(12))    # geometryczna
    assert blisko(srednia_potegowa(3, 4, p=1), 3.5)              # arytmetyczna
    assert blisko(srednia_potegowa(3, 4, p=2), math.sqrt(12.5))  # kwadratowa
    assert srednia_potegowa(3, 4, p=-math.inf) == 3 and srednia_potegowa(3, 4, p=math.inf) == 4


def test_srednia_ciagla_w_zerze_i_rosnaca():
    assert blisko(srednia_potegowa(3, 4, p=1e-7), math.sqrt(12), rel_tol=1e-6)
    assert blisko(srednia_potegowa(3, 4, p=-1e-7), math.sqrt(12), rel_tol=1e-6)
    ps = [-50, -2, -1, -0.1, 0, 0.1, 1, 2, 50]
    wyniki = [srednia_potegowa(3, 4, p=p) for p in ps]
    assert wyniki == sorted(wyniki) and 3 < wyniki[0] and wyniki[-1] < 4


# --- dopasowanie p -----------------------------------------------------------

@pytest.mark.parametrize("a, b, c, p", [(3, 4, 5, 2), (3, 4, 2.4, -2), (6, 3, 2, -1), (3, 4, 7, 1),
                                         (20, 20, 20 * 2 ** 0.4, 2.5), (20, 20, 20 * 2 ** 0.25, 4)])
def test_dopasuj_p(a, b, c, p):
    assert blisko(dopasuj_p(a, b, c), p, rel_tol=1e-8)


def test_dopasuj_p_bez_rozwiazania():
    for c in (3, 3.5, 4):
        with pytest.raises(ValueError):
            dopasuj_p(3, 4, c)
