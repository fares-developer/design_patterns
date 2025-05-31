import unittest
from patterns.creator import Creator, CreatorBomba, CreatorBlindada
from patterns.habitacion import Habitacion
from patterns.pared import Pared, ParedBomba
from patterns.puerta import Puerta, PuertaBlindada

class TestCreator(unittest.TestCase):
    def setUp(self):
        self.creator = Creator()

    def test_crear_habitacion(self):
        hab = self.creator.crear_habitacion(1)
        self.assertIsInstance(hab, Habitacion)
        self.assertEqual(hab.num, 1)
        self.assertIsInstance(hab.norte, Pared)
        self.assertIsInstance(hab.sur, Pared)
        self.assertIsInstance(hab.este, Pared)
        self.assertIsInstance(hab.oeste, Pared)

    def test_fabricar_laberinto(self):
        laberinto = self.creator.fabricar_laberinto()
        self.assertEqual(len(laberinto.habitaciones), 0)

    def test_fabricar_pared(self):
        pared = self.creator.fabricar_pared()
        self.assertIsInstance(pared, Pared)

    def test_fabricar_puerta(self):
        puerta = self.creator.fabricar_puerta(1, 2)
        self.assertIsInstance(puerta, Puerta)
        self.assertEqual(puerta.lado1, 1)
        self.assertEqual(puerta.lado2, 2)

class TestCreatorBomba(unittest.TestCase):
    def setUp(self):
        self.creator = CreatorBomba()

    def test_fabricar_pared(self):
        pared = self.creator.fabricar_pared()
        self.assertIsInstance(pared, ParedBomba)

class TestCreatorBlindada(unittest.TestCase):
    def setUp(self):
        self.creator = CreatorBlindada()

    def test_fabricar_puerta(self):
        puerta = self.creator.fabricar_puerta(1, 2)
        self.assertIsInstance(puerta, PuertaBlindada)
        self.assertEqual(puerta.lado1, 1)
        self.assertEqual(puerta.lado2, 2)

if __name__ == '__main__':
    unittest.main()
