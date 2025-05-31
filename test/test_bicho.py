import unittest
import sys
import os

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.bicho import Bicho, Agresivo, Perezoso, Sabio

class TestBicho(unittest.TestCase):
    """Pruebas para la clase Bicho y sus modos de comportamiento."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.posicion = (0, 0)
        self.modo_perezoso = Perezoso()
        self.modo_agresivo = Agresivo()
        self.modo_sabio = Sabio()
    
    def test_creacion_bicho_modo_por_defecto(self):
        """Verificar que un bicho se crea con el modo Perezoso por defecto."""
        bicho = Bicho(self.posicion)
        self.assertIsInstance(bicho.modo, Perezoso)
        self.assertEqual(bicho.vidas, 10)  # Perezoso tiene 10 vidas
    
    def test_cambio_modo_agresivo(self):
        """Verificar el cambio a modo Agresivo."""
        bicho = Bicho(self.posicion, self.modo_perezoso)
        bicho.cambiar_modo(self.modo_agresivo)
        self.assertIsInstance(bicho.modo, Agresivo)
        self.assertEqual(bicho.vidas, 5)  # Agresivo tiene 5 vidas
    
    def test_cambio_modo_con_vida_proporcional(self):
        """Verificar que las vidas se ajustan proporcionalmente al cambiar de modo."""
        bicho = Bicho(self.posicion, self.modo_perezoso)  # 10 vidas
        bicho.recibir_danyo(5)  # Quedan 5/10 vidas (50%)
        bicho.cambiar_modo(self.modo_agresivo)  # 50% de 5 vidas = 2.5 -> 2 vidas
        self.assertEqual(bicho.vidas, 2)
    
    def test_recibir_danyo(self):
        """Verificar que el bicho recibe daño correctamente."""
        bicho = Bicho(self.posicion, self.modo_perezoso)  # 10 vidas
        bicho.recibir_danyo(3)
        self.assertEqual(bicho.vidas, 7)
    
    def test_no_vidas_negativas(self):
        """Verificar que las vidas no pueden ser negativas."""
        bicho = Bicho(self.posicion, self.modo_perezoso)  # 10 vidas
        bicho.recibir_danyo(15)  # Más daño que vidas
        self.assertEqual(bicho.vidas, 0)
    
    def test_esta_vivo(self):
        """Verificar el método esta_vivo()."""
        bicho = Bicho(self.posicion, self.modo_perezoso)
        self.assertTrue(bicho.esta_vivo())
        bicho.recibir_danyo(10)
        self.assertFalse(bicho.esta_vivo())
    
    def test_atacar_modo_agresivo(self):
        """Verificar el ataque en modo Agresivo."""
        bicho = Bicho(self.posicion, self.modo_agresivo)
        self.assertIn("-10 de daño", bicho.atacar())  # El ataque agresivo hace -10 de daño
    
    def test_movimiento_modo_sabio(self):
        """Verificar el movimiento en modo Sabio."""
        bicho = Bicho(self.posicion, self.modo_sabio)
        self.assertIn("analizando", bicho.moverse().lower())
    
    def test_no_acciones_sin_vida(self):
        """Verificar que no se puede atacar ni mover sin vidas."""
        bicho = Bicho(self.posicion, self.modo_perezoso)
        bicho.recibir_danyo(10)  # Matar al bicho
        self.assertEqual(bicho.atacar(), "¡El bicho está muerto y no puede atacar!")
        self.assertEqual(bicho.moverse(), "¡El bicho está muerto y no puede moverse!")

if __name__ == "__main__":
    unittest.main()
