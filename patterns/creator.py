from patterns.habitacion import Habitacion
from patterns.laberinto import Laberinto
from patterns.pared import Pared, ParedBomba
from patterns.puerta import Puerta, PuertaBlindada


class Creator:
    
    def crear_habitacion(self, num):
        habitacion = Habitacion(num)
        habitacion.norte = self.fabricar_pared()
        habitacion.sur = self.fabricar_pared()
        habitacion.este = self.fabricar_pared()
        habitacion.oeste = self.fabricar_pared()
        return habitacion

    def fabricar_laberinto(self):
        return Laberinto()

    def fabricar_pared(self):
        return Pared()

    def fabricar_puerta(self, lado1, lado2):
        return Puerta(lado1, lado2)

class CreatorBomba(Creator):
    def fabricar_pared(self):
        return ParedBomba()
    

class CreatorBlindada(Creator):
    
    def fabricar_puerta(self, lado1, lado2):
        return PuertaBlindada(lado1, lado2)