from patterns.habitacion import Habitacion
from patterns.laberinto import Laberinto
from patterns.pared import Pared
from patterns.puerta import Puerta


class LaberintoBuilder:

    def __init__(self):
        self.laberinto = None
    
    def fabricar_laberinto(self):
        self.laberinto = Laberinto()
        return self.laberinto
    
    def fabricar_habitacion(self, num_habitacion):
        if not self.laberinto:
            raise ValueError("Primero debe fabricar el laberinto")
            
        habitacion = Habitacion(num_habitacion)
        
        # Crear las paredes por defecto
        habitacion.norte = self.fabricar_pared()
        habitacion.sur = self.fabricar_pared()
        habitacion.este = self.fabricar_pared()
        habitacion.oeste = self.fabricar_pared()
        
        # Añadir la habitación al laberinto
        self.laberinto.agregar_habitacion(habitacion)
        return habitacion
    
    def fabricar_pared(self):
        return Pared()
    
    def fabricar_puerta(self, habitacion1, habitacion2):
        puerta = Puerta(habitacion1, habitacion2)
        return puerta
