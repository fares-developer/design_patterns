import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.bomba import Bomba, Broma, Mina, Destructiva
from patterns.pared import Pared
from patterns.habitacion import Habitacion

class TestBomba(unittest.TestCase):
    """Pruebas para la clase Bomba y sus tipos."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.pared = Pared()
        self.bomba = Bomba(self.pared)
    
    def test_creacion_bomba(self):
        """Verificar que una bomba se crea correctamente."""
        self.assertEqual(self.bomba.pared, self.pared)
        self.assertFalse(self.bomba.activa)
        self.assertIsNone(self.bomba.tipo_bomba)
        self.assertIsNone(self.bomba.nivel_destruccion)
        self.assertIsNone(self.bomba.nivel_radiacion)
    
    def test_iniciar_broma(self):
        """Verificar la configuración de una bomba tipo broma."""
        self.bomba.iniciar_broma()
        self.assertIsInstance(self.bomba.tipo_bomba, Broma)
        self.assertEqual(self.bomba.nivel_destruccion, 0)
        self.assertEqual(self.bomba.nivel_radiacion, 0)
        self.assertFalse(self.bomba.activa)
    
    def test_iniciar_mina(self):
        """Verificar la configuración de una bomba tipo mina."""
        self.bomba.iniciar_mina()
        self.assertIsInstance(self.bomba.tipo_bomba, Mina)
        self.assertEqual(self.bomba.nivel_destruccion, 20)
        self.assertEqual(self.bomba.nivel_radiacion, 5)
        self.assertFalse(self.bomba.activa)
    
    def test_iniciar_destructiva(self):
        """Verificar la configuración de una bomba tipo destructiva."""
        self.bomba.iniciar_destructiva()
        self.assertIsInstance(self.bomba.tipo_bomba, Destructiva)
        self.assertEqual(self.bomba.nivel_destruccion, 50)
        self.assertEqual(self.bomba.nivel_radiacion, 100)
        self.assertFalse(self.bomba.activa)
    
    def test_activar_desactivar(self):
        """Verificar que se puede activar y desactivar la bomba."""
        # Configurar un tipo de bomba primero
        self.bomba.iniciar_broma()
        
        # Probar activación
        with patch('builtins.print') as mock_print:
            result = self.bomba.activar()
            mock_print.assert_any_call("Bomba activada")
            mock_print.assert_any_call("Explotará en 5 segundos")
            self.assertTrue(self.bomba.activa)
            self.assertEqual(result, self.pared)  # Debería devolver la pared decorada
        
        # Probar desactivación
        with patch('builtins.print') as mock_print:
            result = self.bomba.desactivar()
            mock_print.assert_called_once_with("Bomba desactivada")
            self.assertFalse(self.bomba.activa)
            self.assertEqual(result, self.pared)  # Debería devolver la pared decorada
    
    def test_activar_sin_tipo(self):
        """Verificar que no se puede activar sin un tipo de bomba definido."""
        with self.assertRaises(ValueError) as context:
            self.bomba.activar()
        self.assertEqual(str(context.exception), 
                        "No se puede activar la bomba: no se ha definido un tipo de bomba")
    
    @patch('builtins.print')
    def test_explotar_broma(self, mock_print):
        """Verificar la explosión de una bomba tipo broma."""
        self.bomba.iniciar_broma()
        self.bomba.activar()
        
        resultado = self.bomba.explotar()
        self.assertEqual(resultado, "¡Sorpresa! Era una bomba fumaça.")
        mock_print.assert_called_with("¡Sorpresa! Era una bomba fumaça.")
    
    @patch('builtins.print')
    def test_explotar_mina(self, mock_print):
        """Verificar la explosión de una bomba tipo mina."""
        self.bomba.iniciar_mina()
        self.bomba.activar()
        
        resultado = self.bomba.explotar()
        self.assertEqual(resultado, "¡Boom! La mina ha explotado.")
        mock_print.assert_any_call("¡Boom! La mina ha explotado.")
        mock_print.assert_any_call("Aplicando radiación...")
    
    @patch('builtins.print')
    def test_explotar_destructiva(self, mock_print):
        """Verificar la explosión de una bomba tipo destructiva."""
        self.bomba.iniciar_destructiva()
        self.bomba.activar()
        
        resultado = self.bomba.explotar()
        self.assertEqual(resultado, "¡EXPLOSIÓN MASIVA!")
        mock_print.assert_any_call("¡EXPLOSIÓN MASIVA!")
        mock_print.assert_any_call("Radiación extrema liberada.")
    
    def test_explotar_sin_activar(self):
        """Verificar que no se puede explotar una bomba no activa."""
        self.bomba.iniciar_broma()
        with self.assertRaises(ValueError) as context:
            self.bomba.explotar()
        self.assertEqual(str(context.exception), "La bomba no está activa")

if __name__ == "__main__":
    unittest.main(verbosity=2)
