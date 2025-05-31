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


class TipoBomba(ABC):

    def explotar(self):
        pass


class Broma(TipoBomba):

    def __init__(self):
        super().__init__()

    def explotar(self):
        print("Explosión inminente en 3 segundos")
        self.mostrar_confeti()

    def mostrar_confeti(self):
        print("Confeti, confeti, confeti")
        print("Era una broma")


class Mina(TipoBomba):

    def __init__(self):
        super().__init__()

    def explotar(self):
        print("Explosión inminente en 3 segundos")
        self.minar()

    def minar(self):
        print("Lo siento, esta mina va volar a todo el mundo por los aires")
        print("El mundo va a morir")

class Destructiva(TipoBomba):

    def __init__(self):
        super().__init__()

    def explotar(self):
        print("Explosión inminente en 3 segundos")
        self.aplicar_radiacion()

    def aplicar_radiacion(self):
        print("Radiación, radiación, radiación")
        print("Esto va a ser otro Chernobyl")
