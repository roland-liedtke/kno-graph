"""Testy grafu wiedzy: wymagania zadania i odpowiedzi na 6 pytań."""

import re
import unittest

import matplotlib

matplotlib.use("Agg")  # rysowanie bez okna (testy działają też bez ekranu)
import matplotlib.pyplot as plt  # noqa: E402
import networkx as nx  # noqa: E402
import numpy as np  # noqa: E402

import main  # noqa: E402


class TestKnowledgeGraph(unittest.TestCase):
    def setUp(self):
        self.g = main.build_graph()
        self.node_types = {t for _, t in self.g.nodes(data="type")}
        self.relations = {r for _, _, r in self.g.edges(data="relacja")}

    def test_graph_meets_minimum_requirements(self):
        self.assertTrue(self.g.is_directed())
        self.assertGreaterEqual(len({t for _, t in self.g.nodes(data="type")}), 5)
        self.assertGreaterEqual(self.g.number_of_nodes(), 15)
        self.assertGreaterEqual(len({r for _, _, r in self.g.edges(data="relacja")}), 6)
        self.assertGreaterEqual(self.g.number_of_edges(), 20)

    def test_counts_in_docstring_formulas_match_graph(self):
        counts = {"V": self.g.number_of_nodes(), "E": self.g.number_of_edges(),
                  "T": len(self.node_types), "R": len(self.relations)}
        for symbol, count in counts.items():
            with self.subTest(symbol=symbol):
                # \b = koniec liczby, żeby "|V| = 16" nie pasowało do "|V| = 160"
                self.assertRegex(main.__doc__, rf"\|{symbol}\| = {count}\b")

    def test_sets_T_and_R_in_docstring_match_graph(self):
        for symbol, in_graph in (("T", self.node_types), ("R", self.relations)):
            with self.subTest(symbol=symbol):
                # zawartość wyliczenia "T = {...}" z opisu (może zajmować kilka linii)
                listing = re.search(rf"{symbol} = \{{(.*?)\}}", main.__doc__, re.S)
                self.assertIsNotNone(listing)
                in_docstring = {name.strip() for name in listing.group(1).split(",")}
                self.assertEqual(in_docstring, in_graph)

    def test_every_node_has_type_and_every_edge_has_relation(self):
        self.assertTrue(all(t for _, t in self.g.nodes(data="type")))
        self.assertTrue(all(r for _, _, r in self.g.edges(data="relacja")))

    def test_who_teaches_knowledge_representation(self):
        self.assertEqual(main.who_teaches(self.g, "Knowledge Representation"), ["Jan Kowalski"])

    def test_faculty_courses_computer_science(self):
        self.assertEqual(main.faculty_courses(self.g, "Wydział Informatyki"),
                         ["Knowledge Representation", "Machine Learning", "Programowanie w Pythonie"])

    def test_faculty_courses_when_employee_teaches_several(self):
        # Maria Lewandowska (jedyna na Wydziale Matematyki) prowadzi 3 przedmioty.
        self.assertEqual(main.faculty_courses(self.g, "Wydział Matematyki"),
                         ["Algebra Liniowa", "Analiza Matematyczna", "Statystyka"])

    def test_faculty_courses_without_duplicates(self):
        # Dwie osoby z Wydziału Informatyki prowadzą ten sam przedmiot -> przedmiot raz.
        self.g.add_edge("Anna Nowak", "Knowledge Representation", relacja="PROWADZI")
        self.assertEqual(main.faculty_courses(self.g, "Wydział Informatyki"),
                         ["Knowledge Representation", "Machine Learning", "Programowanie w Pythonie"])

    def test_student_courses_piotr_wisniewski(self):
        self.assertEqual(main.student_courses(self.g, "Piotr Wiśniewski"),
                         ["Knowledge Representation", "Machine Learning"])

    def test_prerequisites_machine_learning_including_indirect(self):
        self.assertEqual(main.prerequisites(self.g, "Machine Learning"),
                         ["Analiza Matematyczna", "Programowanie w Pythonie", "Statystyka"])

    def test_prerequisites_course_without_prerequisites(self):
        self.assertEqual(main.prerequisites(self.g, "Knowledge Representation"), [])

    def test_coworkers_jan_kowalski(self):
        self.assertEqual(main.coworkers(self.g, "Jan Kowalski"),
                         ["Anna Nowak", "Tomasz Zieliński"])

    def test_program_courses_computer_science(self):
        self.assertEqual(main.program_courses(self.g, "Informatyka"),
                         ["Knowledge Representation", "Machine Learning",
                          "Programowanie w Pythonie", "Statystyka"])

    def test_unknown_object_gives_empty_answer(self):
        for query in (main.who_teaches, main.faculty_courses, main.student_courses,
                      main.prerequisites, main.coworkers, main.program_courses):
            with self.subTest(query=query.__name__):
                self.assertEqual(query(self.g, "Fizyka"), [])


class TestDrawing(unittest.TestCase):
    def test_no_edge_passes_under_foreign_node(self):
        g = main.build_graph()
        positions = main.layout_nodes(g)
        # Geometria przybliżona: ten sam rozmiar figury, dpi i węzły co w draw_graph, ale bez
        # tight_layout, legendy i axis("off"), które lekko przesuwają piksele. Na prawdziwym
        # rysunku najbliższa krawędź jest ok. 1,7 promienia od obcego węzła, więc zapas wystarcza.
        fig, ax = plt.subplots(figsize=(16, 11), dpi=120)
        nx.draw_networkx_nodes(g, positions, ax=ax, node_size=main.NODE_SIZE)
        fig.canvas.draw()
        pixels = {n: ax.transData.transform(positions[n]) for n in g}
        plt.close(fig)
        radius = main.NODE_SIZE ** 0.5 / 2 * fig.dpi / 72  # node_size to pole w pt²

        for a, b in g.edges:
            A, B = pixels[a], pixels[b]
            for n in g:
                if n in (a, b):
                    continue
                # najbliższy punkt odcinka A-B do środka węzła n
                t = np.clip(np.dot(pixels[n] - A, B - A) / np.dot(B - A, B - A), 0, 1)
                distance = np.linalg.norm(A + t * (B - A) - pixels[n])
                with self.subTest(edge=(a, b), node=n):
                    self.assertGreater(distance, radius)


if __name__ == "__main__":
    unittest.main()
