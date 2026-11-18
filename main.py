"""Graf wiedzy uczelni — networkx + matplotlib.

Program:
1. buduje skierowany graf wiedzy (węzły = obiekty, krawędzie = fakty),
2. odpowiada na 6 pytań, przechodząc po krawędziach grafu,
3. rysuje graf.
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

    # --- Węzły (obiekty). Atrybut "type" mówi, do jakiej klasy należy obiekt. ---
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

    # --- Krawędzie (fakty). Każdy fakt to trójka: (podmiot, RELACJA, obiekt). ---
    # Atrybut "relacja" mówi, jakiego typu jest powiązanie; razem 6 typów i 25 faktów.
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

    Przykład: dokad(g, "Jan Kowalski", "PROWADZI") -> przedmioty Jana.
    """
    return [cel for cel in g.successors(wezel) if g.edges[wezel, cel]["relacja"] == relacja]


def skad(g, wezel, relacja):
    """Węzły, z których strzałka `relacja` WCHODZI do `wezel`.

    Przykład: skad(g, "Jan Kowalski", "ZATRUDNIA") -> wydział Jana.
    """
    return [zrodlo for zrodlo in g.predecessors(wezel) if g.edges[zrodlo, wezel]["relacja"] == relacja]


# ---------------------------------------------------------------------------
# 3. ZAPYTANIA — każde zwraca posortowaną listę odpowiedzi
# ---------------------------------------------------------------------------

def kto_prowadzi(g, przedmiot):
    """Pytanie 1: kto prowadzi dany przedmiot? (strzałka PROWADZI wchodząca do przedmiotu)"""
    return sorted(skad(g, przedmiot, "PROWADZI"))


def przedmioty_wydzialu(g, wydzial):
    """Pytanie 2: jakie przedmioty prowadzą pracownicy wydziału?

    Dwa kroki: wydział --ZATRUDNIA--> pracownik --PROWADZI--> przedmiot.
    """
    wynik = set()  # zbiór, żeby ten sam przedmiot nie powtórzył się
    for pracownik in dokad(g, wydzial, "ZATRUDNIA"):
        wynik.update(dokad(g, pracownik, "PROWADZI"))
    return sorted(wynik)


def zapisy_studenta(g, student):
    """Pytanie 3: na jakie przedmioty zapisany jest student? (strzałki JEST_ZAPISANY_NA)"""
    return sorted(dokad(g, student, "JEST_ZAPISANY_NA"))


def wymagania(g, przedmiot):
    """Pytanie 4: jakie przedmioty trzeba zaliczyć przed danym przedmiotem?

    Idziemy po strzałkach WYMAGA także pośrednio: Machine Learning wymaga Statystyki,
    a Statystyka wymaga Analizy Matematycznej — więc obie są potrzebne przed ML.
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
    """
    wynik = set()
    for wydzial in skad(g, pracownik, "ZATRUDNIA"):
        wynik.update(dokad(g, wydzial, "ZATRUDNIA"))
    wynik.discard(pracownik)  # sam pracownik nie jest swoim współpracownikiem
    return sorted(wynik)


def przedmioty_kierunku(g, kierunek):
    """Pytanie 6: jakie przedmioty są dostępne dla studentów kierunku? (ZAWIERA_PRZEDMIOT)"""
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


def rysuj_graf(g):
    """Rysuje graf: kolor węzła = typ obiektu, napis na strzałce = relacja."""
    plt.figure(figsize=(16, 11))
    # spring_layout rozmieszcza węzły jak kulki na sprężynach; seed = zawsze ten sam układ,
    # k = większe odstępy między węzłami.
    pozycje = nx.spring_layout(g, seed=98, k=1.6)

    # Węzły rysujemy typ po typie, żeby każdy typ miał swój kolor i pozycję w legendzie.
    for typ, kolor in KOLORY.items():
        wezly = [n for n, t in g.nodes(data="type") if t == typ]
        nx.draw_networkx_nodes(g, pozycje, nodelist=wezly, node_color=kolor,
                               node_size=2200, label=typ)

    nx.draw_networkx_labels(g, pozycje, font_size=8)  # nazwy węzłów
    nx.draw_networkx_edges(g, pozycje, node_size=2200, arrowsize=15, edge_color="gray")
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
    print(f"Graf: {g.number_of_nodes()} obiektów ({len(typy_obiektow)} typów), "
          f"{g.number_of_edges()} faktów ({len(typy_relacji)} typów relacji)\n")

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
