from patterns.elementomapa import ElementoMapa

class Habitacion(ElementoMapa):
    def __init__(self, num):
        super().__init__()
        self.num = num

    def entrar(self):
        print(f"Entrando en la habitación {self.num}")
