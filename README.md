# Nowe działania matematyczne

Repozytorium zbiera działania matematyczne, które mają zastosowanie w fizyce i w technice. Każde działanie ma osobny katalog.

| Nr | Działanie | Wzór | Katalog |
|---|---|---|---|
| 1 | p-dodawanie | `a ⊕ₚ b = (a^p + b^p)^(1/p)` | [p-dodawanie](p-dodawanie/README.md) |

![Wynik 3 ⊕ₚ 4 w funkcji parametru p](p-dodawanie/img/wynik-vs-p.svg)

## Punkt wyjścia

Każde działanie w ciągu „dodawanie, mnożenie, potęgowanie” jest powtórzeniem działania poprzedniego:

- Powtórzone dodawanie daje mnożenie: `a·n = a + a + … + a` (n składników).
- Powtórzone mnożenie daje potęgowanie: `a^n = a·a·…·a` (n czynników).

Potęgowanie nie jest przemienne: `2^3 = 8`, a `3^2 = 9`. Potęgowanie nie jest łączne: `(2^3)^2 = 64`, a `2^(3^2) = 512`. Repozytorium opisuje działania, które zachowują przemienność i łączność.

## Zawartość katalogu działania

Każdy katalog działania zawiera 5 części:

1. Definicję ze słownikiem terminów.
2. Własności z testami.
3. Zastosowania ze źródłami.
4. Wizualizacje: rysunki i stronę interaktywną.
5. Kod w Pythonie.

## Styl tekstu

Każdy plik README stosuje reguły polszczyzny kontrolowanej: 1 termin ma 1 znaczenie, 1 wzór zajmuje 1 wiersz, każda liczba ma jednostkę.
