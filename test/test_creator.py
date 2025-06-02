import unittest
import sys
import os

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
        # Verificar que las paredes están inicializadas correctamente
        self.assertIsNotNone(hab.norte)
        self.assertIsNotNone(hab.sur)
        self.assertIsNotNone(hab.este)
        self.assertIsNotNone(hab.oeste)

    def test_fabricar_laberinto(self):
        laberinto = self.creator.fabricar_laberinto()
        self.assertEqual(len(laberinto.habitaciones), 0)

    def test_fabricar_pared(self):
        pared = self.creator.fabricar_pared()
        self.assertIsInstance(pared, Pared)

    def test_fabricar_puerta(self):
        hab1 = Habitacion(1)
        hab2 = Habitacion(2)
        puerta = self.creator.fabricar_puerta(hab1, hab2)
        self.assertIsInstance(puerta, Puerta)
        self.assertIn(puerta, [hab1.norte, hab1.sur, hab1.este, hab1.oeste])
        self.assertIn(puerta, [hab2.norte, hab2.sur, hab2.este, hab2.oeste])

class TestCreatorBomba(unittest.TestCase):
    def setUp(self):
        self.creator = CreatorBomba()

    def test_fabricar_pared(self):
        pared = self.creator.fabricar_pared()
        self.assertIsInstance(pared, ParedBomba)
        
    def test_crear_habitacion_con_paredes_bomba(self):
        hab = self.creator.crear_habitacion(1)
        self.assertIsInstance(hab.norte, ParedBomba)
        self.assertIsInstance(hab.sur, ParedBomba)
        self.assertIsInstance(hab.este, ParedBomba)
        self.assertIsInstance(hab.oeste, ParedBomba)

class TestCreatorBlindada(unittest.TestCase):
    def setUp(self):
        self.creator = CreatorBlindada()

    def test_fabricar_puerta_blindada(self):
        hab1 = Habitacion(1)
        hab2 = Habitacion(2)
        puerta = self.creator.fabricar_puerta(hab1, hab2)
        self.assertIsInstance(puerta, PuertaBlindada)
        self.assertIn(puerta, [hab1.norte, hab1.sur, hab1.este, hab1.oeste])
        self.assertIn(puerta, [hab2.norte, hab2.sur, hab2.este, hab2.oeste])
        
    def test_puerta_blindada_inactiva_por_defecto(self):
        hab1 = Habitacion(1)
        hab2 = Habitacion(2)
        puerta = self.creator.fabricar_puerta(hab1, hab2)
        self.assertFalse(puerta.activa)

if __name__ == '__main__':
    unittest.main()
