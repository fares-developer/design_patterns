from abc import ABC

from patterns.elementomapa import ElementoMapa


# TODO: DECORADORES DE PARED
class DecoratorPared(ElementoMapa):

    def __init__(self, pared):
        super().__init__()
        self.pared = pared


class Pintura(DecoratorPared):
    """Decorador que añade una capa de pintura a una pared."""
    
    def __init__(self, pared, color="blanco"):
        super().__init__(pared)
        self.color = color
        self.pintada = False
        print(f"Preparando pintura de color {self.color}...")
        # No establecemos pintada aquí, solo cuando se llame a pintar()

    def pintar(self):
        """Aplica la capa de pintura a la pared."""
        self.pintada = True
        print(f"Pared pintada de color {self.color}")
        return self.pared

    def quitar_pintura(self):
        """Elimina la capa de pintura de la pared."""
        if hasattr(self.pared, 'pintada'):
            self.pintada = False
        print(f"Se ha quitado la pintura {self.color} de la pared")
        return self.pared
        
    def cambiar_color(self, nuevo_color):
        """Cambia el color de la pintura."""
        color_anterior = self.color
        self.color = nuevo_color
        print(f"Color de pintura cambiado de {color_anterior} a {nuevo_color}")
        return self


class DecoradorPuerta(ElementoMapa):
    """Decorador base para puertas. Delega todas las llamadas a la puerta envuelta."""
    
    def __init__(self, puerta):
        super().__init__()
        self.puerta = puerta
    
    def entrar(self):
        return self.puerta.entrar()
    
    def abrir(self):
        return self.puerta.abrir()
    
    def cerrar(self):
        return self.puerta.cerrar()

    def __str__(self):
        return str(self.puerta)


class PuertaConLlave(DecoradorPuerta):
    """Decorador que añade una cerradura con llave a la puerta."""
    
    def __init__(self, puerta, llave_id):
        super().__init__(puerta)
        self.llave_id = llave_id
        self.cerrada = True
    
    def abrir_con_llave(self, llave):
        """Intenta abrir la puerta con una llave."""
        if llave == self.llave_id:
            self.cerrada = False
            print("¡La cerradura ha hecho click! La puerta se abre.")
            # Devolvemos True para indicar que la llave funciona
            return True
        print("La llave no coincide. La puerta sigue cerrada.")
        return False
    
    def abrir(self):
        """Sobrescribe abrir para verificar la llave."""
        if self.cerrada:
            print("La puerta está cerrada con llave. Usa abrir_con_llave(llave).")
            return False
        return self.puerta.abrir()
    
    def entrar(self):
        if self.cerrada:
            print("La puerta está cerrada con llave. Necesitas la llave correcta.")
            return False
        return self.puerta.entrar()
    
    def __str__(self):
        return f"{self.puerta} (con llave)"


class PuertaConSonido(DecoradorPuerta):
    """Decorador que añade efectos de sonido a la puerta."""
    
    def __init__(self, puerta, sonido_apertura="¡Clic! La puerta se abre.",
                 sonido_cierre="¡Clac! La puerta se cierra."):
        super().__init__(puerta)
        self.sonido_apertura = sonido_apertura
        self.sonido_cierre = sonido_cierre
    
    def abrir(self):
        """Abre la puerta y reproduce el sonido de apertura."""
        resultado = self.puerta.abrir()
        print(self.sonido_apertura)
        return resultado
    
    def cerrar(self):
        """Cierra la puerta y reproduce el sonido de cierre."""
        resultado = self.puerta.cerrar()
        print(self.sonido_cierre)
        return resultado
    
    def __str__(self):
        return f"{self.puerta} (con sonido)"

