from abc import ABC, abstractmethod

class Orientacion(ABC):
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Orientacion, cls).__new__(cls, *args, **kwargs)
        return cls._instances[cls]
    
    @abstractmethod
    def caminar(self, contenedor):
        pass

class Norte(Orientacion):
    def caminar(self, contenedor):
        print("Caminando hacia el Norte")
        # Lógica para moverse al norte

class Sur(Orientacion):
    def caminar(self, contenedor):
        print("Caminando hacia el Sur")
        # Lógica para moverse al sur

class Este(Orientacion):
    def caminar(self, contenedor):
        print("Caminando hacia el Este")
        # Lógica para moverse al este

class Oeste(Orientacion):
    def caminar(self, contenedor):
        print("Caminando hacia el Oeste")
        # Lógica para moverse al oeste