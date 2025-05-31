import unittest
from game import Juego
from patterns.creator import Creator, CreatorBomba, CreatorBlindada
from patterns.habitacion import Habitacion
from patterns.puerta import Puerta, PuertaBlindada
from patterns.pared import ParedBomba

class TestJuego(unittest.TestCase):
    def setUp(self):
        self.juego = Juego()
        self.creator = Creator()

    def test_crear_laberinto2_hab_fm(self):
        laberinto = self.juego.crear_laberinto2_hab_fm(self.creator)
        self.assertIsNotNone(laberinto)
        self.assertEqual(len(laberinto.habitaciones), 2)
        self.assertIsInstance(laberinto.obtenerHabitacion(1), Habitacion)
        self.assertIsInstance(laberinto.obtenerHabitacion(2), Habitacion)

    def test_obtener_habitacion(self):
        self.juego.crear_laberinto2_hab_fm(self.creator)
        habitacion = self.juego.obtener_habitacion(1)
        self.assertIsNotNone(habitacion)
        self.assertEqual(habitacion.num, 1)

    def test_obtener_puerta(self):
        # Necesitamos crear el laberinto primero
        self.juego.crear_laberinto2_hab_fm(self.creator)
        # Obtener una habitación del laberinto en lugar de crear una nueva
        hab1 = self.juego.obtener_habitacion(1)
        # Verificar que la habitación tiene una puerta en el sur
        self.assertIsNotNone(hab1.sur)
        self.assertIsInstance(hab1.sur, Puerta)

    def test_activar_pared_bomba(self):
        # Necesitamos un creador que cree paredes con bomba
        from patterns.creator import CreatorBomba
        juego_bomba = Juego()
        creator_bomba = CreatorBomba()
        juego_bomba.crear_laberinto2_hab_fm(creator_bomba)
        hab1 = juego_bomba.obtener_habitacion(1)
        
        # Verificar que la pared norte es una ParedBomba
        self.assertIsInstance(hab1.norte, ParedBomba)
        
        # Activar la bomba
        juego_bomba.activar_pared_bomba(hab1, "norte")
        self.assertTrue(hab1.norte.activa)

    def test_activar_puerta_blindada(self):
        from patterns.creator import CreatorBlindada
        juego_blindado = Juego()
        creator_blindado = CreatorBlindada()
        juego_blindado.crear_laberinto2_hab_fm(creator_blindado)
        hab1 = juego_blindado.obtener_habitacion(1)
        
        # Verificar que la puerta es blindada
        puerta = juego_blindado.obtener_puerta(hab1)
        self.assertIsInstance(puerta, PuertaBlindada)
        
        # Activar la puerta blindada
        juego_blindado.activar_puerta_blindada(hab1)
        self.assertTrue(puerta.activa)

if __name__ == '__main__':
    unittest.main()
