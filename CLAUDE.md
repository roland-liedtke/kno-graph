# kno-graph — graf wiedzy uczelni

## Cel
Projekt zaliczeniowy: prosty graf wiedzy uczelni w Pythonie (`networkx` + `matplotlib`).
Kod ma być minimalistyczny i czytelny — właściciel broni go krok po kroku na zaliczeniu
(wideoczat), więc prostota i polskie komentarze są ważniejsze niż „sprytne” rozwiązania.

Wymagania zadania:
- skierowany graf `nx.DiGraph()`;
- co najmniej 5 typów węzłów (atrybut `type`), 15 węzłów, 6 typów relacji (atrybut `relacja`
  na krawędzi) i 20 krawędzi (faktów);
- 6 osobnych funkcji-zapytań wypisujących odpowiedzi w konsoli;
- wizualizacja `matplotlib` z `nx.spring_layout`, nazwami węzłów i etykietami krawędzi.

## Stack i struktura
- Python 3.13, `networkx`, `matplotlib` (`requirements.txt`).
- `main.py` — cały program (graf, zapytania, wizualizacja) w jednym pliku — wymóg zadania.
- `test_main.py` — testy `unittest` (biblioteka standardowa, bez dodatkowych zależności).

## Komendy
```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt   # instalacja
.venv/bin/python main.py                                             # uruchomienie
.venv/bin/python -m unittest -v                                      # checki przed PR
```
Na maszynie bez ekranu `plt.show()` nic nie pokaże — rysunek zapisuje się też do
`graf_wiedzy.png` (plik w `.gitignore`).

## Konwencje
- Nazewnictwo (identyfikatory po angielsku, opisy po polsku): `.claude/rules/style.md`.
- Zapytania przyjmują graf jako argument i zwracają posortowaną listę — wypisywanie jest
  w `main()`, dzięki czemu funkcje da się testować.

## Git
- Remote: `origin` → `gitea@192.168.11.52:konfiguracje.online/kno-graph.git`
- Gałąź główna: `main`. Zasady gałęzi i PR-ów: `CONTRIBUTING.md`.
- Tworzenie PR (AGit):
  ```bash
  T=$(printf '%s' "Tytuł PR" | base64 -w0)
  D=$(printf '%s\n' "Opis PR (markdown)" | base64 -w0)
  git push origin HEAD:refs/for/main -o topic=<nazwa-gałęzi> \
    -o "title={base64}$T" -o "description={base64}$D"
  ```

@NOW.md
