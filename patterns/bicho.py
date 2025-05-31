from abc import ABC, abstractmethod

class Modo(ABC):
    """Interfaz base para los diferentes modos de comportamiento de los bichos."""
    
    def get_vidas_iniciales(self):
        """Devuelve el número de vidas iniciales para este modo."""
        pass
    
    def atacar(self):
        """Realiza un ataque según el modo."""
        pass
    
    def moverse(self):
        """Realiza un movimiento según el modo."""
        pass


class Agresivo(Modo):
    """Modo de ataque agresivo: alto poder, movimientos rápidos, pocas vidas."""
    
    def get_vidas_iniciales(self):
        return 5
    
    def atacar(self):
        return "¡Ataque agresivo! -10 de daño"
    
    def moverse(self):
        return "Avanzando rápidamente hacia el objetivo"


class Perezoso(Modo):
    """Modo perezoso: bajo poder, movimientos lentos, vidas estándar."""
    
    def get_vidas_iniciales(self):
        return 10
    
    def atacar(self):
        return "Ataque perezoso... -1 de daño"
    
    def moverse(self):
        return "Movimiento lento..."


class Sabio(Modo):
    """Modo sabio: equilibrio entre ataque y defensa, más vidas."""
    
    def get_vidas_iniciales(self):
        return 20
    
    def atacar(self):
        return "Ataque estratégico -5 de daño"
    
    def moverse(self):
        return "Analizando el terreno antes de moverse..."


class Bicho:
    """Clase que representa un bicho que puede cambiar de comportamiento."""
    
    def __init__(self, posicion, modo=None):
        self.posicion = posicion
        # Si no se especifica un modo, usamos Perezoso por defecto
        self.modo = modo if modo is not None else Perezoso()
        self.vidas = self.modo.get_vidas_iniciales()
    
    def recibir_danyo(self, cantidad):
        """Reduce las vidas del bicho."""
        self.vidas = max(0, self.vidas - cantidad)
    
    def esta_vivo(self):
        """Verifica si el bicho sigue con vida."""
        return self.vidas > 0
    
    def atacar(self):
        """El bicho ataca según su modo actual."""
        if not self.esta_vivo():
            return "¡El bicho está muerto y no puede atacar!"
        return self.modo.atacar()
    
    def moverse(self):
        """El bicho se mueve según su modo actual."""
        if not self.esta_vivo():
            return "¡El bicho está muerto y no puede moverse!"
        return self.modo.moverse()
    
    # Métodos para cambiar de modo
    def cambiar_modo(self, nuevo_modo):
        """Cambia el modo del bicho y ajusta sus vidas."""
        # Guardar el porcentaje de vida actual para mantenerlo proporcional
        if self.modo is not None:
            porcentaje_vida = self.vidas / self.modo.get_vidas_iniciales()
        else:
            porcentaje_vida = 1.0
            
        self.modo = nuevo_modo
        self.vidas = int(self.modo.get_vidas_iniciales() * porcentaje_vida)