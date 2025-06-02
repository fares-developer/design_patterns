import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.bicho import Bicho, Agresivo, Perezoso, Sabio
from patterns.habitacion import Habitacion

class TestBicho(unittest.TestCase):
    """Pruebas para la clase Bicho y sus modos de comportamiento."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.habitacion = Habitacion(1)
        self.modo_perezoso = Perezoso()
        self.modo_agresivo = Agresivo()
        self.modo_sabio = Sabio()
        self.bicho = Bicho(self.habitacion, self.modo_perezoso)
        self.bicho.vidas = self.bicho.modo.get_vidas_iniciales()  # Asegurar vidas iniciales
    
    def test_creacion_bicho_modo_por_defecto(self):
        """Verificar que un bicho se crea con el modo Perezoso por defecto."""
        bicho = Bicho(self.habitacion)
        self.assertIsInstance(bicho.modo, Perezoso)
        self.assertEqual(bicho.vidas, 10)  # Perezoso tiene 10 vidas
        self.assertEqual(bicho.posicion, self.habitacion)
    
    def test_cambio_modo_agresivo(self):
        """Verificar el cambio a modo Agresivo."""
        self.bicho.cambiar_modo(self.modo_agresivo)
        self.assertIsInstance(self.bicho.modo, Agresivo)
        self.assertEqual(self.bicho.vidas, 5)  # Agresivo tiene 5 vidas
    
    def test_cambio_modo_con_vida_proporcional(self):
        """Verificar que las vidas se ajustan proporcionalmente al cambiar de modo."""
        self.bicho.recibir_danyo(5)  # Quedan 5/10 vidas (50%)
        self.bicho.cambiar_modo(self.modo_agresivo)  # 50% de 5 vidas = 2.5 -> 2 vidas
        self.assertEqual(self.bicho.vidas, 2)
    
    def test_recibir_danyo(self):
        """Verificar que el bicho recibe daño correctamente."""
        self.bicho.recibir_danyo(3)
        self.assertEqual(self.bicho.vidas, 7)
    
    def test_no_vida_negativa(self):
        """Verificar que las vidas no pueden ser negativas."""
        self.bicho.recibir_danyo(15)  # Más daño que vidas
        self.assertEqual(self.bicho.vidas, 0)
    
    def test_esta_vivo(self):
        """Verificar el método esta_vivo()."""
        self.assertTrue(self.bicho.esta_vivo())
        self.bicho.recibir_danyo(10)
        self.assertFalse(self.bicho.esta_vivo())
    
    def test_atacar_modo_agresivo(self):
        """Verificar el ataque en modo Agresivo."""
        bicho = Bicho(self.habitacion, self.modo_agresivo)
        # Verificamos que el método atacar() devuelve el mensaje correcto
        resultado = bicho.atacar()
        self.assertEqual(resultado, "¡Ataque agresivo! -10 de daño")
    
    def test_moverse_modo_sabio(self):
        """Verificar el movimiento en modo Sabio."""
        bicho = Bicho(self.habitacion, self.modo_sabio)
        # Verificamos que el método moverse() devuelve el mensaje correcto
        resultado = bicho.moverse()
        self.assertEqual(resultado, "Analizando el terreno antes de moverse...")
    
    def test_no_acciones_sin_vida(self):
        """Verificar que no se puede atacar sin vida."""
        # Matar al bicho
        self.bicho.recibir_danyo(10)
        # Verificamos que el método atacar() devuelve el mensaje correcto
        resultado = self.bicho.atacar()
        self.assertEqual(resultado, "¡El bicho está muerto y no puede atacar!")


if __name__ == "__main__":
    unittest.main(verbosity=2)
