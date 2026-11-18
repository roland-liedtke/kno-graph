"""Testy grafu wiedzy: wymagania zadania i odpowiedzi na 6 pytań."""

import unittest

import matplotlib

matplotlib.use("Agg")  # rysowanie bez okna (testy działają też bez ekranu)
import matplotlib.pyplot as plt  # noqa: E402
import networkx as nx  # noqa: E402
import numpy as np  # noqa: E402

import main  # noqa: E402


class TestGrafWiedzy(unittest.TestCase):
    def setUp(self):
        self.g = main.zbuduj_graf()

    def test_graf_spelnia_minimalne_wymagania(self):
        self.assertTrue(self.g.is_directed())
        self.assertGreaterEqual(len({t for _, t in self.g.nodes(data="type")}), 5)
        self.assertGreaterEqual(self.g.number_of_nodes(), 15)
        self.assertGreaterEqual(len({r for _, _, r in self.g.edges(data="relacja")}), 6)
        self.assertGreaterEqual(self.g.number_of_edges(), 20)

    def test_kazdy_wezel_ma_typ_i_kazda_krawedz_relacje(self):
        self.assertTrue(all(t for _, t in self.g.nodes(data="type")))
        self.assertTrue(all(r for _, _, r in self.g.edges(data="relacja")))

    def test_kto_prowadzi_knowledge_representation(self):
        self.assertEqual(main.kto_prowadzi(self.g, "Knowledge Representation"), ["Jan Kowalski"])

    def test_przedmioty_wydzialu_informatyki(self):
        self.assertEqual(main.przedmioty_wydzialu(self.g, "Wydział Informatyki"),
                         ["Knowledge Representation", "Machine Learning", "Programowanie w Pythonie"])

    def test_przedmioty_wydzialu_gdy_pracownik_prowadzi_kilka(self):
        # Maria Lewandowska (jedyna na Wydziale Matematyki) prowadzi 3 przedmioty.
        self.assertEqual(main.przedmioty_wydzialu(self.g, "Wydział Matematyki"),
                         ["Algebra Liniowa", "Analiza Matematyczna", "Statystyka"])

    def test_przedmioty_wydzialu_bez_powtorzen(self):
        # Dwie osoby z Wydziału Informatyki prowadzą ten sam przedmiot -> przedmiot raz.
        self.g.add_edge("Anna Nowak", "Knowledge Representation", relacja="PROWADZI")
        self.assertEqual(main.przedmioty_wydzialu(self.g, "Wydział Informatyki"),
                         ["Knowledge Representation", "Machine Learning", "Programowanie w Pythonie"])

    def test_zapisy_piotra_wisniewskiego(self):
        self.assertEqual(main.zapisy_studenta(self.g, "Piotr Wiśniewski"),
                         ["Knowledge Representation", "Machine Learning"])

    def test_wymagania_machine_learning_takze_posrednie(self):
        self.assertEqual(main.wymagania(self.g, "Machine Learning"),
                         ["Analiza Matematyczna", "Programowanie w Pythonie", "Statystyka"])

    def test_wymagania_przedmiotu_bez_wymagan(self):
        self.assertEqual(main.wymagania(self.g, "Knowledge Representation"), [])

    def test_wspolpracownicy_jana_kowalskiego(self):
        self.assertEqual(main.wspolpracownicy(self.g, "Jan Kowalski"),
                         ["Anna Nowak", "Tomasz Zieliński"])

    def test_przedmioty_kierunku_informatyka(self):
        self.assertEqual(main.przedmioty_kierunku(self.g, "Informatyka"),
                         ["Knowledge Representation", "Machine Learning",
                          "Programowanie w Pythonie", "Statystyka"])

    def test_nieznany_obiekt_daje_pusta_odpowiedz(self):
        for zapytanie in (main.kto_prowadzi, main.przedmioty_wydzialu, main.zapisy_studenta,
                          main.wymagania, main.wspolpracownicy, main.przedmioty_kierunku):
            with self.subTest(zapytanie=zapytanie.__name__):
                self.assertEqual(zapytanie(self.g, "Fizyka"), [])


class TestRysunek(unittest.TestCase):
    def test_zadna_krawedz_nie_przechodzi_pod_obcym_wezlem(self):
        g = main.zbuduj_graf()
        pozycje = main.rozmiesc_wezly(g)
        fig, ax = plt.subplots(figsize=(16, 11), dpi=120)  # jak w rysuj_graf
        nx.draw_networkx_nodes(g, pozycje, ax=ax, node_size=main.ROZMIAR_WEZLA)
        fig.canvas.draw()
        piksele = {n: ax.transData.transform(pozycje[n]) for n in g}
        plt.close(fig)
        promien = main.ROZMIAR_WEZLA ** 0.5 / 2 * fig.dpi / 72  # node_size to pole w pt²

        for a, b in g.edges:
            A, B = piksele[a], piksele[b]
            for n in g:
                if n in (a, b):
                    continue
                # najbliższy punkt odcinka A-B do środka węzła n
                t = np.clip(np.dot(piksele[n] - A, B - A) / np.dot(B - A, B - A), 0, 1)
                odleglosc = np.linalg.norm(A + t * (B - A) - piksele[n])
                with self.subTest(krawedz=(a, b), wezel=n):
                    self.assertGreater(odleglosc, promien)


if __name__ == "__main__":
    unittest.main()
