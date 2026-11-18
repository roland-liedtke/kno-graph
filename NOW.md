# NOW — stan projektu
*Ostatnia aktualizacja: 2026-11-18 22:23*

## Stan
- `main.py` na `main` (PR #1): graf 16 obiektów (5 typów) / 25 faktów (6 typów relacji), 6 zapytań z odpowiedziami w konsoli, wizualizacja `spring_layout` z legendą i etykietami krawędzi, kopia rysunku w `graf_wiedzy.png`.
- Opisy w `main.py` mają model `G = (V, E)` i wzory zapytań na zbiorach; nagłówek w konsoli podaje |V|, |E|, |T|, |R| (PR #2).
- `test_main.py`: 15 testów `unittest` — wymagania grafu, odpowiedzi na 6 pytań, nieznany obiekt, deduplikacja, brak krawędzi pod obcym węzłem (`TestDrawing`), zgodność |V|, |E|, |T|, |R| i wyliczeń `T`, `R` w opisie z grafem (PR #3, #5). Wszystkie przechodzą.
- Sprawdzone tylko backendem Agg i w pliku PNG; okna `plt.show()` na ekranie nikt nie oglądał (maszyny bez ekranu).

## W toku
- PR `refactor/angielskie-nazwy`: identyfikatory w `main.py` i `test_main.py` po angielsku (np. `build_graph`, `who_teaches`, `targets`/`sources`, `TestDrawing`); opisy, komentarze i komunikaty zostają po polsku — czeka na recenzję.

## Dalej
- Właściciel: uruchomić `main.py` u siebie i obejrzeć okno z rysunkiem przed zaliczeniem.

## Decyzje
- 2026-11-18: identyfikatory (zmienne, stałe, funkcje, klasy i metody testów) po angielsku, opisy, komentarze i komunikaty po polsku — prośba właściciela. Wartości w grafie (nazwy obiektów, typy, relacje) i klucz atrybutu `relacja` zostają po polsku: to dane pokazywane na rysunku, a `relacja` to nazwa z treści zadania.
- 2026-11-18: układ rysunku `seed=241, k=2.2`, `node_size=1600` — jedyny z przeszukanych (seed 0–399, k 1.0–3.0) bez krawędzi pod obcym węzłem i bez nachodzących etykiet; kosztem większej liczby przecięć linii (48). Pilnuje tego test `TestDrawing`.
- 2026-11-18: nazwy węzłów łamane na dwie linie zamiast białego tła pod napisem — tło zasłaniało groty strzałek.
- 2026-11-18: nieznany obiekt w zapytaniu daje pustą listę (`targets`/`sources`), a nie błąd.
- 2026-11-18: cały program w jednym `main.py` — wymóg zadania; testy w `unittest`, żeby nie dodawać zależności.

## Otwarte problemy
- Opis scalonego PR #1 jest nieaktualny (`seed=98`, „dwie strzałki pod węzłami”, 9 testów) — do poprawienia przez właściciela w WWW, jeśli ma zostać w historii.
