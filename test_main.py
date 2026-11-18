"""Testy grafu wiedzy: wymagania zadania i odpowiedzi na 6 pytań."""

import unittest

import main


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


if __name__ == "__main__":
    unittest.main()
