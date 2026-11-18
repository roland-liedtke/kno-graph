# NOW — stan projektu
*Ostatnia aktualizacja: 2026-11-18 18:25*

## Stan
- Szkielet repo: `CLAUDE.md`, `NOW.md`, `CONTRIBUTING.md`, `.gitignore`, `requirements.txt`.

## W toku
- `main.py` (graf 16 obiektów / 25 faktów, 6 zapytań, wizualizacja) + `test_main.py` gotowe lokalnie na `feat/graf-wiedzy-uczelni`; czeka na wypchnięcie (patrz Otwarte problemy).

## Dalej
- (brak)

## Decyzje
- 2026-11-18: cały program w jednym `main.py` — wymóg zadania; testy w `unittest`, żeby nie dodawać zależności.

## Otwarte problemy
- Repo `kno-graph` na serwerze jest puste, a `main` już chroniony — push szkieletu na `main` odrzucony (pre-receive hook), więc PR przez AGit nie ma bazy. Potrzebny pierwszy commit na `main` od właściciela.
