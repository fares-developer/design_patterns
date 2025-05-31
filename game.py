from patterns.habitacion import Habitacion
from patterns.laberinto import Laberinto
from patterns.pared import Pared
from patterns.puerta import Puerta, PuertaBlindada
from patterns.decorator import (
    PuertaConLlave, 
    PuertaConSonido, 
    Bomba, 
    Pintura
)


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
            
            # Asignar el laberinto al juego
            self.laberinto = laberinto
            
            return laberinto
            
        except Exception as e:
            print(f"Error al crear el laberinto: {e}")
            return None

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
    
    def probar_decoradores(self):
        """
        Demuestra el uso de los decoradores de puertas y paredes.
        Muestra cómo se pueden combinar diferentes decoradores.
        """
        print("\n=== DEMOSTRACIÓN DE DECORADORES ===\n")
        
        try:
            # Crear habitaciones de ejemplo
            hab1 = Habitacion(1)
            hab2 = Habitacion(2)
            
            # ===== DEMO DECORADORES DE PUERTA =====
            print("\n--- DECORADORES DE PUERTA ---")
            
            # 1. Puerta normal
            print("\n1. Puerta normal:")
            puerta_normal = Puerta(hab1, hab2)
            print("- Abriendo puerta normal:")
            puerta_normal.abrir()
            print("- Intentando entrar:")
            puerta_normal.entrar()
            
            # 2. Puerta con llave
            print("\n2. Puerta con llave:")
            puerta_llave = PuertaConLlave(Puerta(hab1, hab2), llave_id=1234)
            print("- Intentar entrar sin llave (debe fallar):")
            puerta_llave.entrar()
            print("- Usar llave correcta:")
            puerta_llave.abrir_con_llave(1234)
            puerta_llave.entrar()
            
            # 3. Puerta con sonido
            print("\n3. Puerta con sonido:")
            puerta_sonido = PuertaConSonido(
                Puerta(hab1, hab2),
                sonido_apertura="¡Clic! La puerta se abre.",
                sonido_cierre="¡Clac! La puerta se cierra."
            )
            print("- Abriendo puerta con sonido:")
            puerta_sonido.abrir()
            print("- Cerrando puerta con sonido:")
            puerta_sonido.cerrar()
            
            # ===== DEMO DECORADORES DE PARED =====
            print("\n--- DECORADORES DE PARED ---")
            
            # 1. Pared normal
            print("\n1. Pared normal:")
            pared_normal = Pared()
            print("- Pared creada:", "Soy una pared")
            
            # 2. Pared con bomba
            print("\n2. Pared con bomba:")
            pared_bomba = Bomba(Pared())
            print("- Estado inicial:", "Activa" if hasattr(pared_bomba, 'activa') and pared_bomba.activa else "Inactiva")
            print("- Activando bomba:")
            pared_bomba.activar()
            print("- Desactivando bomba:")
            pared_bomba.desactivar()
            
            # 3. Pared con pintura
            print("\n3. Pared con pintura:")
            pared_pintura = Pintura(Pared(), color="azul")
            print("- Pintando la pared:")
            pared_pintura.pintar()
            print("- Cambiando el color a rojo:")
            pared_pintura.cambiar_color("rojo")
            print("- Quitando la pintura:")
            pared_pintura.quitar_pintura()
            
        except Exception as e:
            print(f"\nError en la demostración: {e}")
        
        print("\n=== FIN DE LA DEMOSTRACIÓN ===\n")