# NOW — stan projektu
*Ostatnia aktualizacja: 2026-11-18 19:31*

## Stan
- Szkielet repo: `CLAUDE.md`, `NOW.md`, `CONTRIBUTING.md`, `.gitignore`, `requirements.txt`.

## W toku
- `main.py` (graf 16 obiektów / 25 faktów, 6 zapytań, wizualizacja) + `test_main.py` — PR #1 (`feat/graf-wiedzy-uczelni`), zatwierdzony (recenzja #22); dopisany commit z sugestiami nieblokującymi czeka na ponowną recenzję.

## Dalej
- (brak)

## Decyzje
- 2026-11-18: układ rysunku `seed=241, k=2.2`, `node_size=1600` — jedyny z przeszukanych (seed 0–399, k 1.0–3.0) bez krawędzi pod obcym węzłem i bez nachodzących etykiet; kosztem większej liczby przecięć linii (48). Pilnuje tego test `TestRysunek`.
- 2026-11-18: cały program w jednym `main.py` — wymóg zadania; testy w `unittest`, żeby nie dodawać zależności.

## Otwarte problemy
- (brak)
