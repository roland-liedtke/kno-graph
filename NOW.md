# NOW — stan projektu
*Ostatnia aktualizacja: 2026-11-18 18:40*

## Stan
- Szkielet repo: `CLAUDE.md`, `NOW.md`, `CONTRIBUTING.md`, `.gitignore`, `requirements.txt`.

## W toku
- `main.py` (graf 16 obiektów / 25 faktów, 6 zapytań, wizualizacja) + `test_main.py` — PR #1 (`feat/graf-wiedzy-uczelni`), czeka na recenzję testera.

## Dalej
- (brak)

## Decyzje
- 2026-11-18: cały program w jednym `main.py` — wymóg zadania; testy w `unittest`, żeby nie dodawać zależności.

## Otwarte problemy
- Ochrona `main`: na czas pushu szkieletu `ai-agent` dostał prawo pushu do `main` — do przywrócenia przez właściciela (push i scalanie tylko właściciel).
