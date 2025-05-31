import json
from pathlib import Path
from patterns.laberinto_builder import LaberintoBuilder
from game import Juego


class Director:
    """
    El Director se encarga de orquestar la construcción del juego completo
    a partir de un archivo de configuración JSON.
    """
    
    def __init__(self):
        """Inicializa el Director con un constructor de laberinto."""
        self._builder = LaberintoBuilder()
        self._habitaciones = {}  # Diccionario para almacenar las habitaciones por número
        self._bichos = []  # Lista para almacenar los bichos
        self.juego = None
    
    def cargar_desde_json(self, ruta_archivo):
        """
        Carga la configuración del laberinto desde un archivo JSON.
        
        Args:
            ruta_archivo: Ruta al archivo JSON de configuración.
            
        Returns:
            dict: Diccionario con la configuración cargada.
            
        Raises:
            FileNotFoundError: Si el archivo no existe.
            json.JSONDecodeError: Si el archivo no es un JSON válido.
        """
        ruta = Path(ruta_archivo)
        if not ruta.exists():
            raise FileNotFoundError(f"El archivo {ruta_archivo} no existe.")
        
        with open(ruta, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    
    def construir_juego(self, ruta_archivo):
        """
        Construye un juego completo a partir de un archivo JSON de configuración.
        
        Args:
            ruta_archivo: Ruta al archivo JSON de configuración.
            
        Returns:
            Juego: El juego construido y listo para iniciar.
        """
        try:
            print(f"Cargando configuración desde {ruta_archivo}...")
            
            # Cargar configuración
            config = self.cargar_desde_json(ruta_archivo)
            
            # Crear el juego
            self.juego = Juego()
            
            # Construir el laberinto
            self.construir_laberinto(config)
            self.conectar_habitaciones(config.get('puertas', []))
            self.agregar_bichos(config.get('bichos', []))
            
            # Asignar el laberinto al juego (el laberinto ya está en self._builder.laberinto)
            self.juego.laberinto = self._builder.laberinto
            
            print("¡Juego construido exitosamente!")
            print(f"- Habitaciones: {len(self._habitaciones)}")
            print(f"- Bichos: {len(self._bichos)}")
            
            # Iniciar el juego
            self.juego.iniciar_juego()
            
            return self.juego
            
        except Exception as e:
            print(f"Error al construir el juego: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def construir_laberinto(self, config):
        """
        Crea las habitaciones del laberinto a partir de la configuración.
        
        Args:
            config: Configuración del laberinto (diccionario).
        """
        self._builder.fabricar_laberinto()
        
        # Crear todas las habitaciones primero
        for hab_config in config.get('laberinto', []):
            if hab_config['tipo'] == 'habitacion':
                num_habitacion = hab_config['num']
                habitacion = self._builder.fabricar_habitacion(num_habitacion)
                # Marcar la última habitación como salida
                if num_habitacion == max([h['num'] for h in config.get('laberinto', []) if h['tipo'] == 'habitacion']):
                    habitacion.es_salida = True
                self._habitaciones[num_habitacion] = habitacion
    
    def conectar_habitaciones(self, conexiones):
        """
        Conecta las habitaciones según la configuración de puertas.
        
        Args:
            conexiones: Lista de conexiones entre habitaciones.
                Cada conexión es una lista [num_hab1, direccion1, num_hab2, direccion2]
        """
        for conexion in conexiones:
            if len(conexion) != 4:
                print(f"Advertencia: Formato de conexión inválido: {conexion}")
                continue
                
            num_hab1, dir1, num_hab2, dir2 = conexion
            
            if num_hab1 not in self._habitaciones or num_hab2 not in self._habitaciones:
                print(f"Advertencia: Una de las habitaciones {num_hab1} o {num_hab2} no existe.")
                continue
                
            hab1 = self._habitaciones[num_hab1]
            hab2 = self._habitaciones[num_hab2]
            
            # Crear la puerta que conecta las habitaciones
            puerta = self._builder.fabricar_puerta(hab1, hab2)
            
            # Conectar las habitaciones en las direcciones especificadas
            if hasattr(hab1, dir1.lower()) and hasattr(hab2, dir2.lower()):
                setattr(hab1, dir1.lower(), puerta)
                setattr(hab2, dir2.lower(), puerta)
            else:
                print(f"Advertencia: Dirección inválida en la conexión {conexion}")
    
    def agregar_bichos(self, bichos_config):
        """
        Agrega bichos a las habitaciones según la configuración.
        
        Args:
            bichos_config: Lista de configuraciones de bichos.
        """
        for bicho_config in bichos_config:
            modo = bicho_config.get('modo', '').lower()
            posicion = bicho_config.get('posicion')
            vida = bicho_config.get('vida', 10)
            ataque = bicho_config.get('ataque', 2)
            
            if posicion not in self._habitaciones:
                print(f"Advertencia: La habitación {posicion} para el bicho no existe.")
                continue
                
            # Crear el bicho con sus atributos
            bicho = {
                'modo': modo,
                'posicion': posicion,
                'habitacion': self._habitaciones[posicion],
                'vida': vida,
                'ataque': ataque,
                'vivo': True
            }
            
            self._bichos.append(bicho)
            
            # Si el juego está configurado, añadir el bicho al juego
            if hasattr(self.juego, 'agregar_bicho'):
                self.juego.agregar_bicho(bicho)
        
        # Configurar los bichos en el juego
        if hasattr(self.juego, 'bichos'):
            self.juego.bichos = self._bichos
