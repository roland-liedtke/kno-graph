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

def build_graph():
    """Tworzy graf wiedzy uczelni i zwraca go."""
    # DiGraph = graf skierowany: każda krawędź ma kierunek (od -> do),
    # np. "Wydział Informatyki" --ZATRUDNIA--> "Jan Kowalski".
    g = nx.DiGraph()

    # --- Węzły (obiekty) = zbiór V. Atrybut "type" to typ(v): klasa obiektu. ---
    # 5 typów: Wydział, Pracownik, Student, Przedmiot, Kierunek; razem 16 obiektów.
    objects = {
        "Wydział": ["Wydział Informatyki", "Wydział Matematyki"],
        "Pracownik": ["Jan Kowalski", "Anna Nowak", "Tomasz Zieliński", "Maria Lewandowska"],
        "Student": ["Piotr Wiśniewski", "Katarzyna Wójcik"],
        "Przedmiot": ["Knowledge Representation", "Machine Learning", "Programowanie w Pythonie",
                      "Statystyka", "Analiza Matematyczna", "Algebra Liniowa"],
        "Kierunek": ["Informatyka", "Matematyka"],
    }
    for node_type, names in objects.items():
        for name in names:
            g.add_node(name, type=node_type)

    # --- Krawędzie (fakty) = zbiór E. Każdy fakt to trójka: (podmiot, RELACJA, obiekt). ---
    # Atrybut "relacja" to r(u, v): typ powiązania; razem |R| = 6 typów i |E| = 25 faktów.
    facts = [
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
    for subject, relation, obj in facts:
        g.add_edge(subject, obj, relacja=relation)

    return g


# ---------------------------------------------------------------------------
# 2. FUNKCJE POMOCNICZE — chodzenie po grafie
# ---------------------------------------------------------------------------

def targets(g, node, relation):
    """Węzły, do których prowadzi strzałka `relation` WYCHODZĄCA z `node`.

    targets(v, ρ) = { u ∈ V : (v, u) ∈ E  i  r(v, u) = ρ }

    Przykład: targets(g, "Jan Kowalski", "PROWADZI") -> przedmioty Jana.
    """
    if node not in g:
        return []  # nieznany obiekt — brak odpowiedzi zamiast błędu
    return [target for target in g.successors(node) if g.edges[node, target]["relacja"] == relation]


def sources(g, node, relation):
    """Węzły, z których strzałka `relation` WCHODZI do `node`.

    sources(v, ρ) = { u ∈ V : (u, v) ∈ E  i  r(u, v) = ρ }

    Przykład: sources(g, "Jan Kowalski", "ZATRUDNIA") -> wydział Jana.
    """
    if node not in g:
        return []  # nieznany obiekt — brak odpowiedzi zamiast błędu
    return [source for source in g.predecessors(node) if g.edges[source, node]["relacja"] == relation]


# ---------------------------------------------------------------------------
# 3. ZAPYTANIA — każde zwraca posortowaną listę odpowiedzi
# ---------------------------------------------------------------------------

def who_teaches(g, course):
    """Pytanie 1: kto prowadzi dany przedmiot? (strzałka PROWADZI wchodząca do przedmiotu)

    wynik(p) = sources(p, PROWADZI) = { u ∈ V : (u, p) ∈ E  i  r(u, p) = PROWADZI }
    """
    return sorted(sources(g, course, "PROWADZI"))


def faculty_courses(g, faculty):
    """Pytanie 2: jakie przedmioty prowadzą pracownicy wydziału?

    Dwa kroki: wydział --ZATRUDNIA--> pracownik --PROWADZI--> przedmiot.

    wynik(w) = ⋃ targets(x, PROWADZI)  po wszystkich  x ∈ targets(w, ZATRUDNIA)
    """
    result = set()  # zbiór, żeby ten sam przedmiot nie powtórzył się
    for employee in targets(g, faculty, "ZATRUDNIA"):
        result.update(targets(g, employee, "PROWADZI"))
    return sorted(result)


def student_courses(g, student):
    """Pytanie 3: na jakie przedmioty zapisany jest student? (strzałki JEST_ZAPISANY_NA)

    wynik(s) = targets(s, JEST_ZAPISANY_NA)
    """
    return sorted(targets(g, student, "JEST_ZAPISANY_NA"))


def prerequisites(g, course):
    """Pytanie 4: jakie przedmioty trzeba zaliczyć przed danym przedmiotem?

    Idziemy po strzałkach WYMAGA także pośrednio: Machine Learning wymaga Statystyki,
    a Statystyka wymaga Analizy Matematycznej — więc obie są potrzebne przed ML.

    E_W = { e ∈ E : r(e) = WYMAGA }             (tylko krawędzie WYMAGA)
    wynik(p) = { u ∈ V : w grafie (V, E_W) istnieje ścieżka p -> ... -> u }
    """
    # Bierzemy tylko krawędzie WYMAGA i szukamy wszystkich węzłów osiągalnych z przedmiotu.
    requires_edges = [(a, b) for a, b, r in g.edges(data="relacja") if r == "WYMAGA"]
    requires_graph = g.edge_subgraph(requires_edges)
    if course not in requires_graph:
        return []  # przedmiot nie ma żadnych wymagań
    return sorted(nx.descendants(requires_graph, course))


def coworkers(g, employee):
    """Pytanie 5: kto pracuje na tym samym wydziale co dany pracownik?

    Krok wstecz do wydziału (ZATRUDNIA), potem do wszystkich zatrudnionych tam osób.

    wynik(p) = ( ⋃ targets(w, ZATRUDNIA)  po wszystkich  w ∈ sources(p, ZATRUDNIA) ) ∖ {p}
    """
    result = set()
    for faculty in sources(g, employee, "ZATRUDNIA"):
        result.update(targets(g, faculty, "ZATRUDNIA"))
    result.discard(employee)  # sam pracownik nie jest swoim współpracownikiem
    return sorted(result)


def program_courses(g, program):
    """Pytanie 6: jakie przedmioty są dostępne dla studentów kierunku? (ZAWIERA_PRZEDMIOT)

    wynik(k) = targets(k, ZAWIERA_PRZEDMIOT)
    """
    return sorted(targets(g, program, "ZAWIERA_PRZEDMIOT"))


# ---------------------------------------------------------------------------
# 4. WIZUALIZACJA
# ---------------------------------------------------------------------------

COLORS = {  # każdy typ obiektu ma własny kolor węzła
    "Wydział": "tomato",
    "Pracownik": "gold",
    "Student": "lightgreen",
    "Przedmiot": "skyblue",
    "Kierunek": "plum",
}
NODE_SIZE = 1600


def layout_nodes(g):
    """Zwraca pozycje węzłów na rysunku (słownik: węzeł -> (x, y)).

    spring_layout rozmieszcza węzły jak kulki połączone sprężynami.
    seed = zawsze ten sam układ; k = odstępy między węzłami. Wartości dobrane tak,
    żeby żadna strzałka nie przechodziła pod obcym węzłem (sprawdza to test).
    """
    return nx.spring_layout(g, seed=241, k=2.2)


def draw_graph(g):
    """Rysuje graf: kolor węzła = typ obiektu, napis na strzałce = relacja."""
    plt.figure(figsize=(16, 11))
    positions = layout_nodes(g)

    # Węzły rysujemy typ po typie, żeby każdy typ miał swój kolor i pozycję w legendzie.
    for node_type, color in COLORS.items():
        nodes = [n for n, t in g.nodes(data="type") if t == node_type]
        nx.draw_networkx_nodes(g, positions, nodelist=nodes, node_color=color,
                               node_size=NODE_SIZE, label=node_type)

    # Nazwy węzłów w dwóch liniach ("Tomasz\nZieliński"), żeby mieściły się w kółkach
    # i strzałki nie wchodziły w napisy.
    labels = {n: n.replace(" ", "\n", 1) for n in g}
    nx.draw_networkx_labels(g, positions, labels=labels, font_size=8)
    nx.draw_networkx_edges(g, positions, node_size=NODE_SIZE, arrowsize=15, edge_color="gray")
    nx.draw_networkx_edge_labels(g, positions, edge_labels=nx.get_edge_attributes(g, "relacja"),
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
    g = build_graph()

    relation_types = {r for _, _, r in g.edges(data="relacja")}
    node_types = {t for _, t in g.nodes(data="type")}
    # |V| = liczba węzłów, |E| = liczba krawędzi, |T| = liczba typów, |R| = liczba relacji.
    print(f"Graf G = (V, E): |V| = {g.number_of_nodes()} obiektów "
          f"(|T| = {len(node_types)} typów), |E| = {g.number_of_edges()} faktów "
          f"(|R| = {len(relation_types)} typów relacji)\n")

    # Każda para: (pytanie, odpowiedź z funkcji-zapytania).
    questions = [
        ("Kto prowadzi przedmiot Knowledge Representation?",
         who_teaches(g, "Knowledge Representation")),
        ("Jakie przedmioty prowadzą pracownicy Wydziału Informatyki?",
         faculty_courses(g, "Wydział Informatyki")),
        ("Na jakie przedmioty zapisany jest Piotr Wiśniewski?",
         student_courses(g, "Piotr Wiśniewski")),
        ("Jakie przedmioty są wymagane przed rozpoczęciem kursu Machine Learning?",
         prerequisites(g, "Machine Learning")),
        ("Kto pracuje na tym samym wydziale co Jan Kowalski?",
         coworkers(g, "Jan Kowalski")),
        ("Jakie przedmioty są dostępne dla studentów kierunku Informatyka?",
         program_courses(g, "Informatyka")),
    ]
    for number, (question, answer) in enumerate(questions, start=1):
        print(f"{number}. {question}")
        print("   -> " + (", ".join(answer) if answer else "brak"))

    draw_graph(g)


# Uruchamiamy main() tylko przy starcie pliku (python main.py), a nie przy imporcie w testach.
if __name__ == "__main__":
    main()
