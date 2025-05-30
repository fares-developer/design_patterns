from patterns.elementomapa import ElementoMapa

class Pared(ElementoMapa):
    def __init__(self):
        super().__init__()

    def entrar(self):
        print("Entrando en una pared")

class ParedBomba(Pared):
    def __init__(self):
        super().__init__()
        self.activa = False

    def entrar(self):
        print("Entrando en una pared bomba")

    def activar(self):
        self.activa = True
        print("Pared bomba activada")

    def desactivar(self):
        self.activa = False
        print("Pared bomba desactivada")