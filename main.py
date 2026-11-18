"""Graf wiedzy uczelni — networkx + matplotlib.

Program:
1. buduje skierowany graf wiedzy (węzły = obiekty, krawędzie = fakty),
2. odpowiada na 6 pytań, przechodząc po krawędziach grafu,
3. rysuje graf.

Model matematyczny — graf skierowany G = (V, E):
    V            zbiór węzłów (obiektów), |V| = 16
    E ⊆ V × V    zbiór krawędzi (faktów): para (u, v) to strzałka u -> v, |E| = 25
    typ: V -> T  typ węzła,     T = {Wydział, Pracownik, Student, Przedmiot, Kierunek}, |T| = 5
    r:   E -> R  relacja krawędzi, R = {ZATRUDNIA, PROWADZI, JEST_ZAPISANY_NA, WYMAGA,
                                        ZAWIERA_PRZEDMIOT, JEST_NA_KIERUNKU}, |R| = 6
Fakt to trójka (u, r(u, v), v), np. (Jan Kowalski, PROWADZI, Knowledge Representation).
W opisach funkcji ρ ∈ R oznacza nazwę relacji, np. ρ = PROWADZI.
"""

import matplotlib.pyplot as plt
import networkx as nx


# ---------------------------------------------------------------------------
# 1. BUDOWA GRAFU WIEDZY
# ---------------------------------------------------------------------------

def zbuduj_graf():
    """Tworzy graf wiedzy uczelni i zwraca go."""
    # DiGraph = graf skierowany: każda krawędź ma kierunek (od -> do),
    # np. "Wydział Informatyki" --ZATRUDNIA--> "Jan Kowalski".
    g = nx.DiGraph()

    # --- Węzły (obiekty) = zbiór V. Atrybut "type" to typ(v): klasa obiektu. ---
    # 5 typów: Wydział, Pracownik, Student, Przedmiot, Kierunek; razem 16 obiektów.
    obiekty = {
        "Wydział": ["Wydział Informatyki", "Wydział Matematyki"],
        "Pracownik": ["Jan Kowalski", "Anna Nowak", "Tomasz Zieliński", "Maria Lewandowska"],
        "Student": ["Piotr Wiśniewski", "Katarzyna Wójcik"],
        "Przedmiot": ["Knowledge Representation", "Machine Learning", "Programowanie w Pythonie",
                      "Statystyka", "Analiza Matematyczna", "Algebra Liniowa"],
        "Kierunek": ["Informatyka", "Matematyka"],
    }
    for typ, nazwy in obiekty.items():
        for nazwa in nazwy:
            g.add_node(nazwa, type=typ)

    # --- Krawędzie (fakty) = zbiór E. Każdy fakt to trójka: (podmiot, RELACJA, obiekt). ---
    # Atrybut "relacja" to r(u, v): typ powiązania; razem |R| = 6 typów i |E| = 25 faktów.
    fakty = [
        # Wydział ZATRUDNIA pracownika
        ("Wydział Informatyki", "ZATRUDNIA", "Jan Kowalski"),
        ("Wydział Informatyki", "ZATRUDNIA", "Anna Nowak"),
        ("Wydział Informatyki", "ZATRUDNIA", "Tomasz Zieliński"),
        ("Wydział Matematyki", "ZATRUDNIA", "Maria Lewandowska"),
        # Pracownik PROWADZI przedmiot
        ("Jan Kowalski", "PROWADZI", "Knowledge Representation"),
        ("Anna Nowak", "PROWADZI", "Machine Learning"),
        ("Tomasz Zieliński", "PROWADZI", "Programowanie w Pythonie"),
        ("Maria Lewandowska", "PROWADZI", "Statystyka"),
        ("Maria Lewandowska", "PROWADZI", "Analiza Matematyczna"),
        ("Maria Lewandowska", "PROWADZI", "Algebra Liniowa"),
        # Student JEST_ZAPISANY_NA przedmiot
        ("Piotr Wiśniewski", "JEST_ZAPISANY_NA", "Knowledge Representation"),
        ("Piotr Wiśniewski", "JEST_ZAPISANY_NA", "Machine Learning"),
        ("Katarzyna Wójcik", "JEST_ZAPISANY_NA", "Statystyka"),
        # Przedmiot WYMAGA wcześniejszego zaliczenia innego przedmiotu
        ("Machine Learning", "WYMAGA", "Statystyka"),
        ("Machine Learning", "WYMAGA", "Programowanie w Pythonie"),
        ("Statystyka", "WYMAGA", "Analiza Matematyczna"),
        # Kierunek ZAWIERA_PRZEDMIOT w programie studiów
        ("Informatyka", "ZAWIERA_PRZEDMIOT", "Knowledge Representation"),
        ("Informatyka", "ZAWIERA_PRZEDMIOT", "Machine Learning"),
        ("Informatyka", "ZAWIERA_PRZEDMIOT", "Programowanie w Pythonie"),
        ("Informatyka", "ZAWIERA_PRZEDMIOT", "Statystyka"),
        ("Matematyka", "ZAWIERA_PRZEDMIOT", "Statystyka"),
        ("Matematyka", "ZAWIERA_PRZEDMIOT", "Analiza Matematyczna"),
        ("Matematyka", "ZAWIERA_PRZEDMIOT", "Algebra Liniowa"),
        # Student JEST_NA_KIERUNKU
        ("Piotr Wiśniewski", "JEST_NA_KIERUNKU", "Informatyka"),
        ("Katarzyna Wójcik", "JEST_NA_KIERUNKU", "Matematyka"),
    ]
    for podmiot, relacja, obiekt in fakty:
        g.add_edge(podmiot, obiekt, relacja=relacja)

    return g


# ---------------------------------------------------------------------------
# 2. FUNKCJE POMOCNICZE — chodzenie po grafie
# ---------------------------------------------------------------------------

def dokad(g, wezel, relacja):
    """Węzły, do których prowadzi strzałka `relacja` WYCHODZĄCA z `wezel`.

    dokad(v, ρ) = { u ∈ V : (v, u) ∈ E  i  r(v, u) = ρ }

    Przykład: dokad(g, "Jan Kowalski", "PROWADZI") -> przedmioty Jana.
    """
    if wezel not in g:
        return []  # nieznany obiekt — brak odpowiedzi zamiast błędu
    return [cel for cel in g.successors(wezel) if g.edges[wezel, cel]["relacja"] == relacja]


def skad(g, wezel, relacja):
    """Węzły, z których strzałka `relacja` WCHODZI do `wezel`.

    skad(v, ρ) = { u ∈ V : (u, v) ∈ E  i  r(u, v) = ρ }

    Przykład: skad(g, "Jan Kowalski", "ZATRUDNIA") -> wydział Jana.
    """
    if wezel not in g:
        return []  # nieznany obiekt — brak odpowiedzi zamiast błędu
    return [zrodlo for zrodlo in g.predecessors(wezel) if g.edges[zrodlo, wezel]["relacja"] == relacja]


# ---------------------------------------------------------------------------
# 3. ZAPYTANIA — każde zwraca posortowaną listę odpowiedzi
# ---------------------------------------------------------------------------

def kto_prowadzi(g, przedmiot):
    """Pytanie 1: kto prowadzi dany przedmiot? (strzałka PROWADZI wchodząca do przedmiotu)

    wynik(p) = skad(p, PROWADZI) = { u ∈ V : (u, p) ∈ E  i  r(u, p) = PROWADZI }
    """
    return sorted(skad(g, przedmiot, "PROWADZI"))


def przedmioty_wydzialu(g, wydzial):
    """Pytanie 2: jakie przedmioty prowadzą pracownicy wydziału?

    Dwa kroki: wydział --ZATRUDNIA--> pracownik --PROWADZI--> przedmiot.

    wynik(w) = ⋃ dokad(x, PROWADZI)  po wszystkich  x ∈ dokad(w, ZATRUDNIA)
    """
    wynik = set()  # zbiór, żeby ten sam przedmiot nie powtórzył się
    for pracownik in dokad(g, wydzial, "ZATRUDNIA"):
        wynik.update(dokad(g, pracownik, "PROWADZI"))
    return sorted(wynik)


def zapisy_studenta(g, student):
    """Pytanie 3: na jakie przedmioty zapisany jest student? (strzałki JEST_ZAPISANY_NA)

    wynik(s) = dokad(s, JEST_ZAPISANY_NA)
    """
    return sorted(dokad(g, student, "JEST_ZAPISANY_NA"))


def wymagania(g, przedmiot):
    """Pytanie 4: jakie przedmioty trzeba zaliczyć przed danym przedmiotem?

    Idziemy po strzałkach WYMAGA także pośrednio: Machine Learning wymaga Statystyki,
    a Statystyka wymaga Analizy Matematycznej — więc obie są potrzebne przed ML.

    E_W = { e ∈ E : r(e) = WYMAGA }             (tylko krawędzie WYMAGA)
    wynik(p) = { u ∈ V : w grafie (V, E_W) istnieje ścieżka p -> ... -> u }
    """
    # Bierzemy tylko krawędzie WYMAGA i szukamy wszystkich węzłów osiągalnych z przedmiotu.
    krawedzie_wymaga = [(a, b) for a, b, r in g.edges(data="relacja") if r == "WYMAGA"]
    graf_wymagan = g.edge_subgraph(krawedzie_wymaga)
    if przedmiot not in graf_wymagan:
        return []  # przedmiot nie ma żadnych wymagań
    return sorted(nx.descendants(graf_wymagan, przedmiot))


def wspolpracownicy(g, pracownik):
    """Pytanie 5: kto pracuje na tym samym wydziale co dany pracownik?

    Krok wstecz do wydziału (ZATRUDNIA), potem do wszystkich zatrudnionych tam osób.

    wynik(p) = ( ⋃ dokad(w, ZATRUDNIA)  po wszystkich  w ∈ skad(p, ZATRUDNIA) ) ∖ {p}
    """
    wynik = set()
    for wydzial in skad(g, pracownik, "ZATRUDNIA"):
        wynik.update(dokad(g, wydzial, "ZATRUDNIA"))
    wynik.discard(pracownik)  # sam pracownik nie jest swoim współpracownikiem
    return sorted(wynik)


def przedmioty_kierunku(g, kierunek):
    """Pytanie 6: jakie przedmioty są dostępne dla studentów kierunku? (ZAWIERA_PRZEDMIOT)

    wynik(k) = dokad(k, ZAWIERA_PRZEDMIOT)
    """
    return sorted(dokad(g, kierunek, "ZAWIERA_PRZEDMIOT"))


# ---------------------------------------------------------------------------
# 4. WIZUALIZACJA
# ---------------------------------------------------------------------------

KOLORY = {  # każdy typ obiektu ma własny kolor węzła
    "Wydział": "tomato",
    "Pracownik": "gold",
    "Student": "lightgreen",
    "Przedmiot": "skyblue",
    "Kierunek": "plum",
}
ROZMIAR_WEZLA = 1600


def rozmiesc_wezly(g):
    """Zwraca pozycje węzłów na rysunku (słownik: węzeł -> (x, y)).

    spring_layout rozmieszcza węzły jak kulki połączone sprężynami.
    seed = zawsze ten sam układ; k = odstępy między węzłami. Wartości dobrane tak,
    żeby żadna strzałka nie przechodziła pod obcym węzłem (sprawdza to test).
    """
    return nx.spring_layout(g, seed=241, k=2.2)


def rysuj_graf(g):
    """Rysuje graf: kolor węzła = typ obiektu, napis na strzałce = relacja."""
    plt.figure(figsize=(16, 11))
    pozycje = rozmiesc_wezly(g)

    # Węzły rysujemy typ po typie, żeby każdy typ miał swój kolor i pozycję w legendzie.
    for typ, kolor in KOLORY.items():
        wezly = [n for n, t in g.nodes(data="type") if t == typ]
        nx.draw_networkx_nodes(g, pozycje, nodelist=wezly, node_color=kolor,
                               node_size=ROZMIAR_WEZLA, label=typ)

    # Nazwy węzłów w dwóch liniach ("Tomasz\nZieliński"), żeby mieściły się w kółkach
    # i strzałki nie wchodziły w napisy.
    napisy = {n: n.replace(" ", "\n", 1) for n in g}
    nx.draw_networkx_labels(g, pozycje, labels=napisy, font_size=8)
    nx.draw_networkx_edges(g, pozycje, node_size=ROZMIAR_WEZLA, arrowsize=15, edge_color="gray")
    nx.draw_networkx_edge_labels(g, pozycje, edge_labels=nx.get_edge_attributes(g, "relacja"),
                                 font_size=7, font_color="darkred")  # nazwy relacji

    plt.title("Graf wiedzy uczelni")
    plt.legend(scatterpoints=1, markerscale=0.4, loc="upper left")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("graf_wiedzy.png", dpi=120)  # kopia rysunku w pliku
    plt.show()


# ---------------------------------------------------------------------------
# 5. PROGRAM GŁÓWNY
# ---------------------------------------------------------------------------

def main():
    g = zbuduj_graf()

    typy_relacji = {r for _, _, r in g.edges(data="relacja")}
    typy_obiektow = {t for _, t in g.nodes(data="type")}
    # |V| = liczba węzłów, |E| = liczba krawędzi, |T| = liczba typów, |R| = liczba relacji.
    print(f"Graf G = (V, E): |V| = {g.number_of_nodes()} obiektów "
          f"(|T| = {len(typy_obiektow)} typów), |E| = {g.number_of_edges()} faktów "
          f"(|R| = {len(typy_relacji)} typów relacji)\n")

    # Każda para: (pytanie, odpowiedź z funkcji-zapytania).
    pytania = [
        ("Kto prowadzi przedmiot Knowledge Representation?",
         kto_prowadzi(g, "Knowledge Representation")),
        ("Jakie przedmioty prowadzą pracownicy Wydziału Informatyki?",
         przedmioty_wydzialu(g, "Wydział Informatyki")),
        ("Na jakie przedmioty zapisany jest Piotr Wiśniewski?",
         zapisy_studenta(g, "Piotr Wiśniewski")),
        ("Jakie przedmioty są wymagane przed rozpoczęciem kursu Machine Learning?",
         wymagania(g, "Machine Learning")),
        ("Kto pracuje na tym samym wydziale co Jan Kowalski?",
         wspolpracownicy(g, "Jan Kowalski")),
        ("Jakie przedmioty są dostępne dla studentów kierunku Informatyka?",
         przedmioty_kierunku(g, "Informatyka")),
    ]
    for numer, (pytanie, odpowiedz) in enumerate(pytania, start=1):
        print(f"{numer}. {pytanie}")
        print("   -> " + (", ".join(odpowiedz) if odpowiedz else "brak"))

    rysuj_graf(g)


# Uruchamiamy main() tylko przy starcie pliku (python main.py), a nie przy imporcie w testach.
if __name__ == "__main__":
    main()
