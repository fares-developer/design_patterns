from patterns.laberinto import Laberinto
from patterns.puerta import PuertaBlindada

class Juego:
    def __init__(self):
        self.laberinto = Laberinto()

    def iniciar_juego(self):
        # Lógica para iniciar el juego
        pass

    def crear_laberinto2_hab_fm(self, creator):
        """
        
        Crea un laberinto con 2 habitaciones y una puerta entre ellas.
        Utiliza el patrón Factory Method para crear las habitaciones y la puerta.

        Args:
            creator: Instancia de Creator o sus subclases.
        
        Returns:
            Laberinto con 2 habitaciones y una puerta."""
        
        try:
            laberinto = creator.fabricar_laberinto()
            habitacion1 = creator.crear_habitacion(1)
            habitacion2 = creator.crear_habitacion(2)
            puerta = creator.fabricar_puerta(habitacion1.num, habitacion2.num)
            habitacion1.sur = puerta
            habitacion2.norte = puerta
            laberinto.agregar_habitacion(habitacion1)
            laberinto.agregar_habitacion(habitacion2)

        except Exception as e:
            print(f"Error al crear el laberinto: {e}")
            return None
        
        return laberinto

    def obtener_habitacion(self, num):
        return self.laberinto.obtenerHabitacion(num)
    
    def obtener_puerta(self, habitacion):
        return self.laberinto.obtenerPuerta(habitacion)
    
    def activar_pared_bomba(self, habitacion, pared):
        """
        Activa una pared bomba en la habitación especificada.
        
        Args:
            habitacion: Instancia de Habitacion.
            pared: String que indica la pared a activar ('norte', 'sur', 'este', 'oeste').
        Raises:
            ParedNovalida: Si la pared no es válida.
        
        """

        hab = self.obtener_habitacion(habitacion.num)
        if pared == "norte":
            hab.norte.activar()
        elif pared == "sur":
            hab.sur.activar()
        elif pared == "este":
            hab.este.activar()
        elif pared == "oeste":
            hab.oeste.activar()    
        else:
            print("Pared no válida. Debe ser 'norte', 'sur', 'este' u 'oeste'.")

    def activar_puerta_blindada(self, habitacion):
        """
        Activa una puerta blindada en la habitación especificada.
        
        Args:
            habitacion: Instancia de Habitacion.
        Raises:
            PuertaNovalida: Si la puerta no es válida.
        
        """

        puerta = self.obtener_puerta(habitacion)
        if isinstance(puerta, PuertaBlindada):
            puerta.activar()
        else:
            print("No hay una puerta blindada en la habitación especificada.")