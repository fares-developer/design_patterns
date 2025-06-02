from abc import ABC

from patterns.decorator import DecoratorPared


class Bomba(DecoratorPared):
    """
    Decorador que convierte una pared en una bomba que se puede activar/desactivar.
    
    Utiliza el patrón Strategy para definir diferentes comportamientos de explosión.
    """

    def __init__(self, pared):
        super().__init__(pared)
        self.activa = False  # Atributo propio del decorador
        self.tipo_bomba = None
        self.nivel_destruccion = None
        self.nivel_radiacion = None

    def activar(self):
        """
        Activa la bomba.
        
        Returns:
            La pared decorada.
            
        Raises:
            ValueError: Si no se ha definido un tipo de bomba.
        """
        if self.tipo_bomba is None:
            raise ValueError("No se puede activar la bomba: no se ha definido un tipo de bomba")
            
        self.activa = True
        print("Bomba activada")
        print("Explotará en 5 segundos")
        return self.pared

    def desactivar(self):
        """
        Desactiva la bomba.
        
        Returns:
            La pared decorada.
        """
        self.activa = False
        print("Bomba desactivada")
        return self.pared
        
    def explotar(self):
        """
        Ejecuta la explosión de la bomba según su tipo.
        
        Returns:
            str: Mensaje con el resultado de la explosión.
            
        Raises:
            ValueError: Si la bomba no está activa o no tiene tipo definido.
        """
        if not self.activa:
            raise ValueError("La bomba no está activa")
            
        if self.tipo_bomba is None:
            raise ValueError("No se puede explotar: tipo de bomba no definido")
            
        return self.tipo_bomba.explotar()

    def iniciar_broma(self):
        """Configura la bomba con la estrategia de tipo broma."""
        self.tipo_bomba = Broma()
        self.nivel_radiacion = 0
        self.nivel_destruccion = 0
        self.activa = False
        print("Bomba configurada como tipo: Broma")

    def iniciar_mina(self):
        """Configura la bomba con la estrategia de tipo mina."""
        self.tipo_bomba = Mina()
        self.nivel_radiacion = 5
        self.nivel_destruccion = 20
        self.activa = False
        print("Bomba configurada como tipo: Mina")

    def iniciar_destructiva(self):
        """Configura la bomba con la estrategia de tipo destructiva."""
        self.tipo_bomba = Destructiva()
        self.nivel_radiacion = 100
        self.nivel_destruccion = 50
        self.activa = False
        print("Bomba configurada como tipo: Destructiva")
        
    def entrar(self):
        """
        Implementación del método abstracto de ElementoMapa.
        Se llama cuando el jugador intenta entrar en la pared decorada con la bomba.
        
        Returns:
            bool: True si el jugador puede pasar, False en caso contrario.
        """
        if self.activa:
            try:
                self.explotar()
                return True  # Después de explotar, la pared podría ser destruida
            except ValueError as e:
                print(f"Error: {e}")
                return False
        # Si la bomba no está activa, se comporta como una pared normal
        return self.pared.entrar()


class TipoBomba(ABC):

    def explotar(self):
        pass


class Broma(TipoBomba):

    def __init__(self):
        super().__init__()

    def explotar(self):
        print("¡Sorpresa! Era una bomba fumaça.")
        return "¡Sorpresa! Era una bomba fumaça."


class Mina(TipoBomba):

    def __init__(self):
        super().__init__()

    def explotar(self):
        print("¡Boom! La mina ha explotado.")
        print("Aplicando radiación...")
        return "¡Boom! La mina ha explotado."

class Destructiva(TipoBomba):

    def __init__(self):
        super().__init__()

    def explotar(self):
        print("¡EXPLOSIÓN MASIVA!")
        print("Radiación extrema liberada.")
        return "¡EXPLOSIÓN MASIVA!"
