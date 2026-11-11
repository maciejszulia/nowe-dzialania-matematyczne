"""p-dodawanie: a ⊕ₚ b = (a^p + b^p)^(1/p).

Moduł nie wymaga żadnej biblioteki poza biblioteką standardową Pythona.

Użycie w kodzie:
    from pdodawanie import padd
    padd(3, 4, p=2)     # 5.0
    padd(6, 3, p=-1)    # 2.0

Użycie w terminalu:
    python3 pdodawanie.py P A B [C ...]
    python3 pdodawanie.py -2 3 4    # 2.4
"""

from __future__ import annotations

import argparse
import math

__all__ = ["padd", "srednia_potegowa", "dopasuj_p"]


def _sprawdz_argumenty(x: tuple[float, ...]) -> None:
    if len(x) < 2:
        raise ValueError("Działanie wymaga co najmniej 2 argumentów.")
    for v in x:
        if not (v > 0) or math.isinf(v):
            raise ValueError("Każdy argument MUSI być liczbą dodatnią i skończoną.")


def _exp(t: float) -> float:
    # math.exp zgłasza OverflowError dla t > 709,78; granicą jest +∞.
    try:
        return math.exp(t)
    except OverflowError:
        return math.inf


def padd(*x: float, p: float) -> float:
    """Zwraca (x1^p + x2^p + ... + xn^p)^(1/p).

    x: co najmniej 2 liczby dodatnie w tej samej jednostce.
    p: liczba rzeczywista różna od 0; float('inf') zwraca max, float('-inf') zwraca min.
    Wynik ma jednostkę argumentów.
    Jeżeli wynik przekracza zakres typu float (około 1,8e308), to funkcja zwraca float('inf').
    """
    _sprawdz_argumenty(x)
    if p == 0 or math.isnan(p):
        raise ValueError("Parametr p MUSI być różny od 0.")
    if math.isinf(p):
        return max(x) if p > 0 else min(x)
    # Dzielenie przez m utrzymuje każdy składnik w przedziale (0, 1].
    # Dzięki temu potęga nie przekracza zakresu liczb zmiennoprzecinkowych.
    m = max(x) if p > 0 else min(x)
    s = math.fsum((v / m) ** p for v in x)
    return m * _exp(math.log(s) / p)


def srednia_potegowa(*x: float, p: float) -> float:
    """Zwraca średnią potęgową ((x1^p + ... + xn^p) / n)^(1/p).

    Dla p = 0 zwraca średnią geometryczną, czyli granicę średniej potęgowej dla p → 0.
    """
    _sprawdz_argumenty(x)
    if math.isnan(p):
        raise ValueError("Parametr p MUSI być liczbą.")
    if p == 0:
        return math.exp(math.fsum(math.log(v) for v in x) / len(x))
    if math.isinf(p):
        return max(x) if p > 0 else min(x)
    # Wzór w logarytmach jest stabilny także dla p bliskiego 0.
    m = max(x) if p > 0 else min(x)
    s = math.fsum((v / m) ** p for v in x)
    return m * _exp(math.log(s / len(x)) / p)


def dopasuj_p(a: float, b: float, c: float, *, tolerancja: float = 1e-12) -> float:
    """Zwraca parametr p, dla którego padd(a, b, p=p) = c.

    Rozwiązanie istnieje tylko dla c > max(a, b) (wtedy p > 0)
    albo dla 0 < c < min(a, b) (wtedy p < 0).
    Funkcja szuka p metodą bisekcji w przedziale 1e-6 <= |p| <= 1e3.
    """
    _sprawdz_argumenty((a, b, c))
    lo, hi = min(a, b), max(a, b)
    if lo <= c <= hi:
        raise ValueError("Brak rozwiązania: c MUSI być mniejsze niż min(a, b) albo większe niż max(a, b).")
    znak = 1.0 if c > hi else -1.0
    # Na każdej gałęzi wynik maleje, gdy p rośnie.
    p_lewe, p_prawe = (1e-6, 1e3) if znak > 0 else (-1e3, -1e-6)
    if not (padd(a, b, p=p_lewe) >= c >= padd(a, b, p=p_prawe)):
        raise ValueError("Brak rozwiązania w przedziale 1e-6 <= |p| <= 1e3.")
    for _ in range(200):
        p_srodek = 0.5 * (p_lewe + p_prawe)
        if padd(a, b, p=p_srodek) > c:
            p_lewe = p_srodek
        else:
            p_prawe = p_srodek
        if p_prawe - p_lewe < tolerancja:
            break
    return 0.5 * (p_lewe + p_prawe)


def _main() -> None:
    parser = argparse.ArgumentParser(
        description="p-dodawanie: (A^P + B^P + ...)^(1/P). Przykład: pdodawanie.py -2 3 4",
    )
    parser.add_argument("p", type=float, help="parametr p, różny od 0 (inf i -inf są dozwolone)")
    parser.add_argument("x", type=float, nargs="+", help="co najmniej 2 liczby dodatnie w tej samej jednostce")
    args = parser.parse_args()
    print(f"{padd(*args.x, p=args.p):.12g}")


if __name__ == "__main__":
    _main()
