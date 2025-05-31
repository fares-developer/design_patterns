from abc import ABC, abstractmethod


class ElementoMapa(ABC):
    def __init__(self, ancho=0, alto=0, largo=0):
        self.ancho = ancho  # anchura (x)
        self.alto = alto    # altura (y)
        self.largo = largo  # profundidad (z)
        self.volumen = ancho * alto * largo

    @abstractmethod
    def entrar(self):
        pass


class Contenedor(ElementoMapa):
    def __init__(self, ancho=0, alto=0, largo=0):
        super().__init__(ancho, alto, largo)
        self.hijos = []
        self.espacio_ocupado = 0

    def entrar(self):
        print("Entrando a un contenedor")

    def agregar_hijo(self, elemento):
        self.hijos.append(elemento)

    def eliminar_hijo(self, elemento):
        self.hijos.remove(elemento)

    def obtener_hijo(self, indice):
        return self.hijos[indice]
        
    def cabe_dentro(self, elemento):
        # Verificar si hay espacio suficiente en volumen
        espacio_libre = self.volumen - self.espacio_ocupado
        if elemento.volumen > espacio_libre:
            return False
            
        # Verificar dimensiones físicas
        return (elemento.ancho <= self.ancho and 
                elemento.alto <= self.alto and 
                elemento.largo <= self.largo)


class Hoja(ElementoMapa):
    def __init__(self):
        super().__init__()

    def entrar(self):
        print("Estoy en hoja")