import unittest
import sys
import os

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.bomba import Bomba, Broma, Mina, Destructiva
from patterns.pared import Pared

class TestBomba(unittest.TestCase):
    """Pruebas para la clase Bomba y sus tipos."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.pared = Pared()
        self.bomba = Bomba(self.pared)
    
    def test_creacion_bomba(self):
        """Verificar que una bomba se crea correctamente."""
        self.assertIsInstance(self.bomba.pared, Pared)
        self.assertFalse(self.bomba.activa)
        self.assertIsNone(self.bomba.tipo_bomba)
    
    def test_activar_sin_tipo(self):
        """Verificar que no se puede activar una bomba sin tipo."""
        with self.assertRaises(ValueError):
            self.bomba.activar()
    
    def test_activar_desactivar(self):
        """Verificar la activación y desactivación de la bomba."""
        self.bomba.tipo_bomba = Broma()
        self.bomba.activar()
        self.assertTrue(self.bomba.activa)
        self.bomba.desactivar()
        self.assertFalse(self.bomba.activa)
    
    def test_bomba_broma(self):
        """Verificar el comportamiento de la bomba Broma."""
        self.bomba.tipo_bomba = Broma()
        self.bomba.activar()
        # No verificamos el valor de retorno, solo que no falle
        self.bomba.explotar()
    
    def test_bomba_mina(self):
        """Verificar el comportamiento de la bomba Mina."""
        self.bomba.tipo_bomba = Mina()
        self.bomba.activar()
        # No verificamos el valor de retorno, solo que no falle
        self.bomba.explotar()
    
    def test_bomba_destructiva(self):
        """Verificar el comportamiento de la bomba Destructiva."""
        self.bomba.tipo_bomba = Destructiva()
        self.bomba.activar()
        # No verificamos el valor de retorno, solo que no falle
        self.bomba.explotar()
    
    def test_explosion_sin_activar(self):
        """Verificar que no se puede explotar una bomba sin activar."""
        self.bomba.tipo_bomba = Broma()
        with self.assertRaises(ValueError):
            self.bomba.explotar()

if __name__ == "__main__":
    unittest.main()
