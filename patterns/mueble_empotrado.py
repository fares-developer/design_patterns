from abc import ABC, abstractmethod
from patterns.elementomapa import ElementoMapa, Contenedor
from patterns.orientacion import Norte, Sur, Este, Oeste

class Mueble(ElementoMapa, ABC):
    """Clase base abstracta para todos los muebles"""
    def __init__(self, nombre, ancho=0, alto=0, largo=0, orientacion=None):
        super().__init__(ancho, alto, largo)
        self.nombre = nombre
        # Por defecto, orientación Norte si no se especifica
        self.orientacion = orientacion if orientacion is not None else Norte()
    
    @abstractmethod
    def mostrar_estructura(self, nivel=0):
        pass
        
    def cambiar_orientacion(self, nueva_orientacion):
        """Cambia la orientación del mueble"""
        self.orientacion = nueva_orientacion
        print(f"{self.nombre}: Orientación cambiada a {self.obtener_nombre_orientacion()}")
    
    def obtener_nombre_orientacion(self):
        """Devuelve el nombre de la orientación actual"""
        return self.orientacion.__class__.__name__

class MuebleSimple(Mueble):
    """Hoja del patrón Composite - representa muebles que no pueden contener otros muebles"""
    def __init__(self, nombre, ancho=0, alto=0, largo=0, orientacion=None):
        super().__init__(nombre, ancho, alto, largo, orientacion)
    
    def entrar(self):
        print(f"Entrando en {self.nombre} (orientado al {self.obtener_nombre_orientacion()})")
    
    def mostrar_estructura(self, nivel=0):
        print("  " * nivel + f"- {self.nombre} ({self.ancho}x{self.alto}x{self.largo}cm, {self.obtener_nombre_orientacion()})")

class MuebleCompuesto(Mueble, Contenedor):
    """Composite del patrón Composite - puede contener otros muebles"""
    def __init__(self, nombre, ancho=0, alto=0, largo=0, orientacion=None):
        Mueble.__init__(self, nombre, ancho, alto, largo, orientacion)
        Contenedor.__init__(self, ancho, alto, largo)
        self.hijos = []
    
    def entrar(self):
        print(f"Abriendo {self.nombre} (orientado al {self.obtener_nombre_orientacion()})...")
        for hijo in self.hijos:
            hijo.entrar()
    
    def agregar_mueble(self, mueble):
        if not self.cabe_dentro(mueble):
            print(f"¡No cabe {mueble.nombre} en {self.nombre}!")
            return False
        self.hijos.append(mueble)
        self.espacio_ocupado += mueble.volumen
        return True
    
    def mostrar_estructura(self, nivel=0):
        print("  " * nivel + f"+ {self.nombre} ({self.ancho}x{self.alto}x{self.largo}cm, {len(self.hijos)} elementos)")
        for hijo in self.hijos:
            hijo.mostrar_estructura(nivel + 1)

# Decoradores para funcionalidad adicional
class MuebleDecorador(Mueble, ABC):
    """Clase base para decoradores de muebles"""
    def __init__(self, mueble: Mueble):
        super().__init__(mueble.nombre, mueble.ancho, mueble.alto, mueble.largo)
        self._mueble = mueble
    
    def entrar(self):
        return self._mueble.entrar()
    
    def mostrar_estructura(self, nivel=0):
        return self._mueble.mostrar_estructura(nivel)

class MuebleEmpotrado(MuebleDecorador):
    """Decorador para muebles empotrados"""
    def __init__(self, mueble: Mueble):
        super().__init__(mueble)
        self.nombre = f"{mueble.nombre} (Empotrado)"
    
    def entrar(self):
        print(f"Abriendo {self.nombre} empotrado...")
        return super().entrar()
    
    def get_espacio_util(self):
        # Los muebles empotrados tienen un 5% más de espacio útil
        return self.volumen * 1.05