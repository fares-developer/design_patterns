from patterns.bicho import Bicho, Agresivo, Perezoso, Sabio
from patterns.bomba import Bomba
from patterns.decorator import (
    PuertaConLlave,
    PuertaConSonido,
    Pintura
)
from patterns.habitacion import Habitacion
from patterns.laberinto import Laberinto
from patterns.mueble_empotrado import MuebleSimple, MuebleCompuesto
from patterns.orientacion import *
from patterns.pared import Pared
from patterns.puerta import Puerta, PuertaBlindada


class Juego:
    def __init__(self):
        self.laberinto = Laberinto()
        self.bichos = list()

    def iniciar_juego(self):
        # Lógica para iniciar el juego
        pass

    def crear_laberinto2_hab_fm(self, creator):
        """
        Crea un laberinto con 2 habitaciones y una puerta entre ellas.
        Utiliza el patrón Factory Method para crear las habitaciones y la puerta.

        Args:
            creator: Instancia de Creator o sus subclases.
        
        Returns:
            Laberinto con 2 habitaciones y una puerta."""
        
        try:
            laberinto = creator.fabricar_laberinto()
            habitacion1 = creator.crear_habitacion(1)
            habitacion2 = creator.crear_habitacion(2)
            puerta = creator.fabricar_puerta(habitacion1.num, habitacion2.num)
            habitacion1.sur = puerta
            habitacion2.norte = puerta
            laberinto.agregar_habitacion(habitacion1)
            laberinto.agregar_habitacion(habitacion2)
            
            # Asignar el laberinto al juego
            self.laberinto = laberinto
            
            return laberinto
            
        except Exception as e:
            print(f"Error al crear el laberinto: {e}")
            return None

    def obtener_habitacion(self, num):
        return self.laberinto.obtenerHabitacion(num)
    
    def obtener_puerta(self, habitacion):
        return self.laberinto.obtenerPuerta(habitacion)
    
    def activar_pared_bomba(self, habitacion, pared):
        """
        Activa una pared bomba en la habitación especificada.
        
        Args:
            habitacion: Instancia de Habitacion.
            pared: String que indica la pared a activar ('norte', 'sur', 'este', 'oeste').
        Raises:
            ParedNovalida: Si la pared no es válida.
        
        """

        hab = self.obtener_habitacion(habitacion.num)
        if pared == "norte":
            hab.norte.activar()
        elif pared == "sur":
            hab.sur.activar()
        elif pared == "este":
            hab.este.activar()
        elif pared == "oeste":
            hab.oeste.activar()    
        else:
            print("Pared no válida. Debe ser 'norte', 'sur', 'este' u 'oeste'.")

    def activar_puerta_blindada(self, habitacion):
        """
        Activa una puerta blindada en la habitación especificada.
        
        Args:
            habitacion: Instancia de Habitacion.
        Raises:
            PuertaNovalida: Si la puerta no es válida.
        """
        puerta = self.obtener_puerta(habitacion)
        if isinstance(puerta, PuertaBlindada):
            puerta.activar()
        else:
            print("No hay una puerta blindada en la habitación especificada.")
    
    def probar_decoradores(self):
        """
        Demuestra el uso de los decoradores de puertas y paredes.
        Muestra cómo se pueden combinar diferentes decoradores.
        """
        print("\n=== DEMOSTRACIÓN DE DECORADORES ===\n")
        
        try:
            # Crear habitaciones de ejemplo
            hab1 = Habitacion(1)
            hab2 = Habitacion(2)
            
            # ===== DEMO DECORADORES DE PUERTA =====
            print("\n--- DECORADORES DE PUERTA ---")
            
            # 1. Puerta normal
            print("\n1. Puerta normal:")
            puerta_normal = Puerta(hab1, hab2)
            print("- Abriendo puerta normal:")
            puerta_normal.abrir()
            print("- Intentando entrar:")
            puerta_normal.entrar()
            
            # 2. Puerta con llave
            print("\n2. Puerta con llave:")
            puerta_llave = PuertaConLlave(Puerta(hab1, hab2), llave_id=1234)
            print("- Intentar entrar sin llave (debe fallar):")
            puerta_llave.entrar()
            print("- Usar llave correcta:")
            puerta_llave.abrir_con_llave(1234)
            puerta_llave.entrar()
            
            # 3. Puerta con sonido
            print("\n3. Puerta con sonido:")
            puerta_sonido = PuertaConSonido(
                Puerta(hab1, hab2),
                sonido_apertura="¡Clic! La puerta se abre.",
                sonido_cierre="¡Clac! La puerta se cierra."
            )
            print("- Abriendo puerta con sonido:")
            puerta_sonido.abrir()
            print("- Cerrando puerta con sonido:")
            puerta_sonido.cerrar()
            
            # ===== DEMO DECORADORES DE PARED =====
            print("\n--- DECORADORES DE PARED ---")
            
            # 1. Pared normal
            print("\n1. Pared normal:")
            pared_normal = Pared()
            print("- Pared creada:", "Soy una pared")
            
            # 2. Pared con bomba
            print("\n2. Pared con bomba:")
            pared_bomba = Bomba(Pared())
            print("- Estado inicial:", "Activa" if hasattr(pared_bomba, 'activa') and pared_bomba.activa else "Inactiva")
            print("- Activando bomba:")
            pared_bomba.activar()
            print("- Desactivando bomba:")
            pared_bomba.desactivar()
            
            # 3. Pared con pintura
            print("\n3. Pared con pintura:")
            pared_pintura = Pintura(Pared(), color="azul")
            print("- Pintando la pared:")
            pared_pintura.pintar()
            print("- Cambiando el color a rojo:")
            pared_pintura.cambiar_color("rojo")
            print("- Quitando la pintura:")
            pared_pintura.quitar_pintura()
            
        except Exception as e:
            print(f"\nError en la demostración: {e}")
        
        print("\n=== FIN DE LA DEMOSTRACIÓN ===\n")

    def agregar_bicho(self, bicho):
        self.bichos.append(bicho)
        
    def probar_estrategias_bomba(self):
        """
        Prueba las diferentes estrategias de bombas implementadas.
        Muestra cómo se comporta cada tipo de bomba al activarse.
        """
        print("\n=== PRUEBA DE ESTRATEGIAS DE BOMBA ===\n")
        
        # Crear una bomba de cada tipo
        bomba_broma = Bomba(Pared())
        bomba_mina = Bomba(Pared())
        bomba_destructiva = Bomba(Pared())
        
        # Inicializar cada bomba con su estrategia correspondiente
        bomba_broma.iniciar_broma()
        bomba_mina.iniciar_mina()
        bomba_destructiva.iniciar_destructiva()
        
        # Función auxiliar para probar una bomba
        def probar_bomba(nombre, bomba):
            print(f"\n--- Probando {nombre} ---")
            print(f"Tipo: {bomba.tipo_bomba.__class__.__name__}")
            print(f"Nivel de radiación: {bomba.nivel_radiacion}")
            print(f"Nivel de destrucción: {bomba.nivel_destruccion}")
            print("Activando bomba...")
            bomba.activar()
            bomba.tipo_bomba.explotar()
            print("--- Fin de la prueba ---")
        
        # Probar cada tipo de bomba
        probar_bomba("Bomba Broma", bomba_broma)
        probar_bomba("Bomba Mina", bomba_mina)
        probar_bomba("Bomba Destructiva", bomba_destructiva)
        
        print("\n=== FIN DE LA PRUEBA ===\n")
    
    def probar_bichos(self):
        """Prueba la funcionalidad de los bichos con diferentes modos."""
        print("\n=== PRUEBA DE BICHOS ===")
        
        # Crear instancias de los modos
        modo_perezoso = Perezoso()
        modo_agresivo = Agresivo()
        modo_sabio = Sabio()
        
        # Crear un bicho en modo por defecto (Perezoso)
        bicho = Bicho(posicion=(5, 5), modo=modo_perezoso)
        print("\nBicho creado en modo Perezoso (por defecto):")
        print(f"Vidas iniciales: {bicho.vidas}")
        print(f"Ataque: {bicho.atacar()}")
        
        # Cambiar a modo agresivo
        bicho.cambiar_modo(modo_agresivo)
        print("\nCambiado a modo Agresivo:")
        print(f"Vidas: {bicho.vidas}")
        print(f"Ataque: {bicho.atacar()}")
        
        # Recibir daño
        bicho.recibir_danyo(3)
        print(f"\nDespués de recibir 3 de daño: {bicho.vidas} vidas")
        
        # Cambiar a modo sabio (más vidas)
        bicho.cambiar_modo(modo_sabio)
        print("\nCambiado a modo Sabio (más vidas):")
        print(f"Vidas: {bicho.vidas}")
        
        # Recibir daño letal
        print("\nRecibiendo daño letal...")
        bicho.recibir_danyo(100)
        print(f"Vidas: {bicho.vidas}")
        print(f"¿Está vivo? {bicho.esta_vivo()}")
        print(f"Intento de ataque: {bicho.atacar()}")
        print(f"Intento de movimiento: {bicho.moverse()}")
        
        # Volver al modo perezoso para probar otro cambio
        bicho.cambiar_modo(modo_perezoso)
        print("\nCambiado a modo Perezoso después de morir:")
        print(f"Vidas: {bicho.vidas}")
        print(f"¿Está vivo? {bicho.esta_vivo()}")
        
        # Agregar el bicho a la lista de bichos del juego
        self.bichos.append(bicho)
        print(f"\nTotal de bichos en el juego: {len(self.bichos)}")
        print("\n=== FIN DE LA PRUEBA DE BICHOS ===\n")

    def probar_composite_muebles(self):
        """
        Prueba el patrón Composite con la jerarquía de muebles.
        """
        print("\n=== Probando patrón Composite con muebles ===")

        # Crear un armario principal (compuesto)
        armario = MuebleCompuesto("Armario Principal", 200, 220, 60, orientacion=Norte())

        # Crear muebles simples
        estante_superior = MuebleSimple("Estante Superior", 180, 40, 50, orientacion=Norte())
        cajonera = MuebleSimple("Cajonera", 80, 60, 40, orientacion=Sur())
        perchero = MuebleSimple("Perchero", 100, 180, 30, orientacion=Este())

        # Añadir muebles al armario
        print("\nAñadiendo muebles al armario...")
        armario.agregar_mueble(estante_superior)
        armario.agregar_mueble(cajonera)
        armario.agregar_mueble(perchero)

        # Crear un cajón pequeño (no cabe en el armario por sus dimensiones)
        cajon_pequeno = MuebleSimple("Cajón Pequeño", 35, 15, 30, orientacion=Norte())

        # Intentar añadir un mueble que no cabe
        print("\nIntentando añadir un mueble que no cabe...")
        try:
            armario.agregar_mueble(cajon_pequeno)
        except ValueError as e:
            print(f"Error: {e}")

        # Mostrar la estructura del armario
        print("\nEstructura del armario:")
        armario.mostrar_estructura()

        # Probar el método entrar()
        print("\nProbando el método entrar() en los muebles:")
        for mueble in [armario, estante_superior, cajonera, perchero]:
            mueble.entrar()

        # Probar cambio de orientación
        print("\nCambiando orientación del estante superior:")
        estante_superior.cambiar_orientacion(Oeste())

        # Mostrar estructura final
        print("\nEstructura final del armario:")
        armario.mostrar_estructura()

        print("\n=== Fin de la prueba de Composite con muebles ===\n")