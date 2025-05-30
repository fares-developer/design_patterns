from patterns.elementomapa import ElementoMapa
from patterns.puerta import PuertaBlindada

class Laberinto(ElementoMapa):
    def __init__(self):
        super().__init__()
        self.habitaciones = dict()

    def entrar(self):
        print("Entrando en el laberinto")

    def agregar_habitacion(self, habitacion):
        self.habitaciones[habitacion.num] = habitacion

    def obtenerHabitacion(self, num):
        return self.habitaciones.get(num, None)
    
    def obtenerPuerta(self, habitacion):
        if isinstance(habitacion.norte, PuertaBlindada):
            return habitacion.norte
        elif isinstance(habitacion.sur, PuertaBlindada):
            return habitacion.sur
        elif isinstance(habitacion.este, PuertaBlindada):
            return habitacion.este
        elif isinstance(habitacion.oeste, PuertaBlindada):
            return habitacion.oeste
        else:
            print("No hay puerta blindada en la habitación especificada.")
            return None