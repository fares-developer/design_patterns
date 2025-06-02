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

    def fabricar_puerta(self, hab1, hab2):
        puerta = Puerta(hab1, hab2)
        
        # Establecer la puerta en una dirección de cada habitación que esté libre
        if hab1.norte is None and hab2.sur is None:
            hab1.norte = puerta
            hab2.sur = puerta
        elif hab1.sur is None and hab2.norte is None:
            hab1.sur = puerta
            hab2.norte = puerta
        elif hab1.este is None and hab2.oeste is None:
            hab1.este = puerta
            hab2.oeste = puerta
        elif hab1.oeste is None and hab2.este is None:
            hab1.oeste = puerta
            hab2.este = puerta
        else:
            # Si no hay direcciones libres, lanzar una excepción
            raise ValueError("No hay direcciones libres para colocar la puerta")
            
        return puerta

class CreatorBomba(Creator):
    def fabricar_pared(self):
        return ParedBomba()
    

class CreatorBlindada(Creator):
    
    def fabricar_puerta(self, hab1, hab2):
        puerta = PuertaBlindada(hab1, hab2)
        
        # Establecer la puerta en una dirección de cada habitación que esté libre
        if hab1.norte is None and hab2.sur is None:
            hab1.norte = puerta
            hab2.sur = puerta
        elif hab1.sur is None and hab2.norte is None:
            hab1.sur = puerta
            hab2.norte = puerta
        elif hab1.este is None and hab2.oeste is None:
            hab1.este = puerta
            hab2.oeste = puerta
        elif hab1.oeste is None and hab2.este is None:
            hab1.oeste = puerta
            hab2.este = puerta
        else:
            # Si no hay direcciones libres, lanzar una excepción
            raise ValueError("No hay direcciones libres para colocar la puerta")
            
        return puerta