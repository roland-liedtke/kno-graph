# NOW — stan projektu
*Ostatnia aktualizacja: 2026-11-18 20:40*

## Stan
- `main.py` na `main` (PR #1): graf 16 obiektów (5 typów) / 25 faktów (6 typów relacji), 6 zapytań z odpowiedziami w konsoli, wizualizacja `spring_layout` z legendą i etykietami krawędzi, kopia rysunku w `graf_wiedzy.png`.
- Opisy w `main.py` mają model `G = (V, E)` i wzory zapytań na zbiorach; nagłówek w konsoli podaje |V|, |E|, |T|, |R| (PR #2).
- `test_main.py`: 14 testów `unittest` — wymagania grafu, odpowiedzi na 6 pytań, nieznany obiekt, deduplikacja, brak krawędzi pod obcym węzłem (`TestRysunek`), zgodność |V| i |E| w opisie z grafem. Wszystkie przechodzą.
- Sprawdzone tylko backendem Agg i w pliku PNG; okna `plt.show()` na ekranie nikt nie oglądał (maszyny bez ekranu).

## W toku
- PR #3 (`test/wzory-w-opisie`): test zgodności wzorów z grafem obejmuje też |T|, |R| i nazwy typów oraz relacji (sugestie z recenzji PR #2) — czeka na recenzję.

## Dalej
- Właściciel: uruchomić `main.py` u siebie i obejrzeć okno z rysunkiem przed zaliczeniem.

## Decyzje
- 2026-11-18: układ rysunku `seed=241, k=2.2`, `node_size=1600` — jedyny z przeszukanych (seed 0–399, k 1.0–3.0) bez krawędzi pod obcym węzłem i bez nachodzących etykiet; kosztem większej liczby przecięć linii (48). Pilnuje tego test `TestRysunek`.
- 2026-11-18: nazwy węzłów łamane na dwie linie zamiast białego tła pod napisem — tło zasłaniało groty strzałek.
- 2026-11-18: nieznany obiekt w zapytaniu daje pustą listę (`dokad`/`skad`), a nie błąd.
- 2026-11-18: cały program w jednym `main.py` — wymóg zadania; testy w `unittest`, żeby nie dodawać zależności.

## Otwarte problemy
- Opis scalonego PR #1 jest nieaktualny (`seed=98`, „dwie strzałki pod węzłami”, 9 testów) — do poprawienia przez właściciela w WWW, jeśli ma zostać w historii.
- Lokalny klon testera ma `main` ze starą historią bez wspólnych commitów z `origin/main` — właściciel wyrówna go ręcznie.
