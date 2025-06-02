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
        self.jugador_vivo = True
        self.juego_terminado = False
        self.motivo_fin_juego = ""
        self.inventario = []
        self.efectos_activos = {}
        self.estadisticas = {
            'ataque': 0,
            'defensa': 0,
            'velocidad': 0
        }
        self.jugador = {
            'vida_actual': 50,
            'vida_maxima': 50,
            'ataque_base': 8,
            'defensa': 3,
            'inventario': []
        }

    def verificar_estado_juego(self):
        """
        Verifica las condiciones de fin de juego, incluyendo combate con bichos.
        
        Returns:
            bool: True si el juego debe continuar, False si ha terminado.
        """
        # Verificar si el jugador ha muerto
        if not self.jugador_vivo or self.jugador['vida_actual'] <= 0:
            self.jugador_vivo = False
            self.juego_terminado = True
            self.motivo_fin_juego = "¡Has muerto!"
            return False
        
        # Verificar si el jugador ha ganado (si está en la habitación de salida)
        if hasattr(self, 'habitacion_actual') and hasattr(self.habitacion_actual, 'es_salida') and self.habitacion_actual.es_salida:
            # Verificar si hay bichos vivos en el laberinto
            bichos_vivos = [b for b in getattr(self, 'bichos', []) if b.get('vivo', False)]
            if not bichos_vivos or (hasattr(self, 'tiene_llave') and self.tiene_llave):
                self.juego_terminado = True
                if not bichos_vivos:
                    self.motivo_fin_juego = "¡Felicidades! Has vencido a todos los bichos y encontrado la salida. ¡Victoria total!"
                else:
                    self.motivo_fin_juego = "¡Felicidades! Has encontrado la salida. Los bichos restantes han quedado atrapados en el laberinto."
                return False
            else:
                print("\nLa puerta de salida está cerrada con llave. Busca la llave en el laberinto.")
                
        return True
        
    def aplicar_efecto_objeto(self, objeto):
        """Aplica el efecto de un objeto al jugador."""
        tipo = objeto.get('tipo')
        efecto = objeto.get('efecto')
        valor = objeto.get('valor', 0)
        
        if efecto == 'cura':
            self.jugador['vida_actual'] = min(self.jugador['vida_maxima'], self.jugador['vida_actual'] + valor)
            print(f"¡Recuperaste {valor} puntos de vida!")
            print(f"Vida actual: {self.jugador['vida_actual']}/{self.jugador['vida_maxima']}")
            
        elif efecto == 'aumenta_ataque':
            self.estadisticas['ataque'] += valor
            self.efectos_activos['aumenta_ataque'] = valor
            print(f"¡Tu ataque ha aumentado en {valor} puntos!")
            
        elif efecto == 'aumenta_defensa':
            self.estadisticas['defensa'] += valor
            self.efectos_activos['aumenta_defensa'] = valor
            print(f"¡Tu defensa ha aumentado en {valor} puntos!")
            
        elif efecto == 'reduce_daño':
            self.estadisticas['defensa'] += valor
            self.efectos_activos['reduce_daño'] = valor
            print(f"¡El daño que recibes se reduce en {valor} puntos!")
            
        elif efecto == 'aumenta_velocidad':
            self.estadisticas['velocidad'] += valor
            self.efectos_activos['aumenta_velocidad'] = valor
            print(f"¡Tu velocidad ha aumentado en {valor} puntos!")
            
        elif efecto == 'abre_puerta':
            self.tiene_llave = True
            print("¡Has encontrado una llave que abre la puerta de salida!")
            
        elif efecto == 'veneno':
            # Aplicar veneno a los bichos en la habitación actual
            bichos_en_habitacion = [b for b in self.bichos 
                                 if b.get('vivo', False) and b.get('habitacion', None) == self.habitacion_actual]
            for bicho in bichos_en_habitacion:
                bicho['vida'] = max(1, bicho['vida'] - valor)
                print(f"El bicho {bicho['modo']} ha sido envenenado y ha perdido {valor} puntos de vida.")
    
    def atacar_bicho(self, bicho):
        """Realiza un ataque del jugador a un bicho."""
        # Calcular daño base + bonificación de ataque - defensa del bicho
        dano_base = self.jugador.get('ataque_base', 5) + self.estadisticas.get('ataque', 0)
        defensa_bicho = bicho.get('defensa', 0)
        dano = max(1, dano_base - defensa_bicho)
        
        # Aplicar daño al bicho
        bicho['vida'] = max(0, bicho['vida'] - dano)
        print(f"¡Has infligido {dano} de daño al bicho {bicho['modo']}!")
        
        # Verificar si el bicho ha muerto
        if bicho['vida'] <= 0:
            bicho['vivo'] = False
            print(f"¡Has derrotado al bicho {bicho['modo']}!")
            # Verificar si todos los bichos están muertos
            bichos_vivos = [b for b in self.bichos if b.get('vivo', False)]
            if not bichos_vivos:
                print("¡Has derrotado a todos los bichos! Ahora busca la salida.")
            return True
        else:
            print(f"El bicho {bicho['modo']} tiene {bicho['vida']} puntos de vida restantes.")
            return False
    
    def recibir_ataque_bicho(self, bicho):
        """El jugador recibe un ataque de un bicho."""
        # Calcular daño del bicho - defensa del jugador
        dano_bicho = max(1, bicho.get('ataque', 2) - self.jugador.get('defensa', 0) - self.estadisticas.get('defensa', 0))
        self.jugador['vida_actual'] = max(0, self.jugador['vida_actual'] - dano_bicho)
        print(f"El bicho {bicho['modo']} te ha hecho {dano_bicho} puntos de daño.")
        
        # Verificar si el jugador ha muerto
        if self.jugador['vida_actual'] <= 0:
            self.jugador_vivo = False
            print("¡Has muerto!")
            return False
        else:
            print(f"Te quedan {self.jugador['vida_actual']}/{self.jugador['vida_maxima']} puntos de vida.")
            return True

    def iniciar_juego(self):
        """
        Inicia el bucle principal del juego con comandos de movimiento y combate.
        """
        print("¡Bienvenido al Laberinto!")
        print("Tu objetivo es encontrar la salida (habitación marcada como salida).")
        print("\nComandos disponibles:")
        print("- Movimiento: norte, sur, este, oeste")
        print("- Combate: atacar <bicho> (ej: atacar 1)")
        print("- Recolectar: recoger <objeto> (ej: recoger 1)")
        print("- Otros: ver, salir")
        
        # Inicializar habitación actual (tomamos la primera habitación del diccionario)
        if self.laberinto.habitaciones:
            primera_habitacion_num = next(iter(self.laberinto.habitaciones))
            self.habitacion_actual = self.laberinto.habitaciones[primera_habitacion_num]
            
            # Inicializar jugador con estadísticas base
            if not hasattr(self, 'jugador'):
                self.jugador = {
                    'vida_actual': 50,
                    'vida_maxima': 50,
                    'ataque_base': 8,
                    'defensa': 3,
                    'inventario': []
                }
        else:
            print("Error: No hay habitaciones en el laberinto.")
            return
        
        # Bucle principal del juego
        while not self.juego_terminado:
            # Mostrar estado actual
            print(f"\n--- Habitación {getattr(self.habitacion_actual, 'num', 'desconocida')} ---")
            
            # Mostrar salidas disponibles
            salidas = []
            for direccion in ["norte", "sur", "este", "oeste"]:
                if hasattr(self.habitacion_actual, direccion):
                    elemento = getattr(self.habitacion_actual, direccion)
                    if isinstance(elemento, Puerta):
                        hab_destino = elemento.lado2 if elemento.lado1 == self.habitacion_actual else elemento.lado1
                        salidas.append(f"{direccion.capitalize()} (Habitación {getattr(hab_destino, 'num', '?')})")
            
            if salidas:
                print("\nSalidas disponibles: " + ", ".join(salidas))
            else:
                print("\n¡No hay salidas visibles!")
            
            # Mostrar objetos en la habitación
            if hasattr(self.habitacion_actual, 'objetos') and self.habitacion_actual.objetos:
                print("\nObjetos en esta habitación:")
                for i, obj in enumerate(self.habitacion_actual.objetos, 1):
                    print(f"  {i}. {obj.get('descripcion')}")
                # Guardar los objetos en el juego para acceder a ellos fácilmente
                self.objetos = self.habitacion_actual.objetos.copy()
            else:
                # Limpiar la lista de objetos si no hay en la habitación
                if hasattr(self, 'objetos'):
                    del self.objetos
            
            # Mostrar bichos en la habitación
            bichos_en_habitacion = []
            if hasattr(self, 'bichos'):
                bichos_en_habitacion = [
                    b for b in self.bichos 
                    if b.get('vivo', False) and b.get('habitacion', None) == self.habitacion_actual
                ]
                
                if bichos_en_habitacion:
                    print("\n¡Bichos en esta habitación!")
                    for i, bicho in enumerate(bichos_en_habitacion, 1):
                        print(f"  {i}. {bicho['modo']} (Vida: {bicho['vida']}, Ataque: {bicho['ataque']})")
            
            # Obtener entrada del jugador
            try:
                partes = input("\n¿Qué quieres hacer? ").strip().lower().split()
                if not partes:
                    continue
                    
                comando = partes[0]
                
                # Comandos de movimiento
                if comando in ["norte", "sur", "este", "oeste"]:
                    if hasattr(self.habitacion_actual, comando):
                        elemento = getattr(self.habitacion_actual, comando)
                        if isinstance(elemento, Puerta):
                            # Verificar si hay bichos en la habitación actual
                            if bichos_en_habitacion:
                                print("¡No puedes huir! Hay bichos en la habitación.")
                                continue
                                
                            self.habitacion_actual = elemento.lado2 if elemento.lado1 == self.habitacion_actual else elemento.lado1
                            print(f"Has entrado en la habitación {getattr(self.habitacion_actual, 'num', 'desconocida')}")
                        else:
                            print("No puedes ir en esa dirección.")
                    else:
                        print("No hay salida en esa dirección.")
                
                # Comando de ataque
                elif comando == "atacar" and len(partes) > 1:
                    if not bichos_en_habitacion:
                        print("No hay bichos para atacar aquí.")
                        continue
                        
                    try:
                        indice = int(partes[1]) - 1
                        if 0 <= indice < len(bichos_en_habitacion):
                            bicho = bichos_en_habitacion[indice]
                            
                            # Turno del jugador
                            bicho_derrotado = self.atacar_bicho(bicho)
                            
                            # Si el bicho sigue vivo, contraataca
                            if not bicho_derrotado and bicho.get('vivo', False):
                                self.recibir_ataque_bicho(bicho)
                                
                            # Actualizar la lista de bichos en la habitación
                            bichos_en_habitacion = [b for b in self.bichos 
                                                 if b.get('vivo', False) and b.get('habitacion', None) == self.habitacion_actual]
                            
                            # Si no quedan bichos, puedes moverte
                            if not bichos_en_habitacion:
                                print("¡No hay más bichos en esta habitación! Puedes continuar tu camino.")
                                
                        else:
                            print("Número de bicho inválido.")
                    except (ValueError, IndexError):
                        print("Por favor, especifica un número de bicho válido.")
                
                # Comando para recoger objetos
                elif comando == "recoger" and len(partes) > 1:
                    if not hasattr(self, 'objetos') or not self.objetos:
                        print("No hay objetos en esta habitación.")
                        continue
                        
                    try:
                        indice = int(partes[1]) - 1
                        if 0 <= indice < len(self.objetos):
                            objeto = self.objetos[indice]
                            self.aplicar_efecto_objeto(objeto)
                            
                            # Si es un objeto que se puede guardar, lo añadimos al inventario
                            if objeto['tipo'] not in ['poción', 'veneno']:  # Las pociones se usan al recogerlas
                                self.inventario.append(objeto)
                                print(f"Has guardado en tu inventario: {objeto.get('descripcion')}")
                            
                            # Eliminar el objeto de la habitación
                            if hasattr(self.habitacion_actual, 'objetos'):
                                if objeto in self.habitacion_actual.objetos:
                                    self.habitacion_actual.objetos.remove(objeto)
                                    # Actualizar la lista de objetos mostrados
                                    if hasattr(self, 'objetos'):
                                        self.objetos = self.habitacion_actual.objetos.copy()
                        else:
                            print("Número de objeto inválido.")
                    except (ValueError, IndexError):
                        print("Por favor, especifica un número de objeto válido.")
                
                # Comando para ver información
                elif comando == "ver":
                    print("\n--- Estado del juego ---")
                    print(f"Estás en la habitación {getattr(self.habitacion_actual, 'num', 'desconocida')}")
                    print(f"Vida: {self.jugador['vida_actual']}/{self.jugador['vida_maxima']}")
                    
                    # Mostrar estadísticas
                    if any(self.estadisticas.values()):
                        print("\nEstadísticas mejoradas:")
                        for stat, valor in self.estadisticas.items():
                            if valor > 0:
                                print(f"- {stat.capitalize()}: +{valor}")
                    
                    # Mostrar inventario
                    if hasattr(self, 'inventario') and self.inventario:
                        print("\nInventario:")
                        for i, obj in enumerate(self.inventario, 1):
                            print(f"  {i}. {obj.get('descripcion')}")
                    
                    # Mostrar bichos restantes
                    bichos_vivos = [b for b in getattr(self, 'bichos', []) if b.get('vivo', False)]
                    print(f"\nBichos restantes en el laberinto: {len(bichos_vivos)}")
                    
                    # Mostrar si estás en la salida
                    if hasattr(self.habitacion_actual, 'es_salida') and self.habitacion_actual.es_salida:
                        print("\n¡Estás en la habitación de salida!")
                        if hasattr(self, 'tiene_llave') and self.tiene_llave:
                            print("Tienes la llave para salir. ¡Puedes ganar el juego!")
                        elif not bichos_vivos:
                            print("¡Ve a la salida para ganar!")
                        else:
                            print("Necesitas la llave o derrotar a todos los bichos para ganar.")
                
                # Comando para salir del juego
                elif comando == "salir":
                    confirmacion = input("¿Estás seguro de que quieres salir? (s/n): ").strip().lower()
                    if confirmacion == 's':
                        self.juego_terminado = True
                        self.motivo_fin_juego = "¡Has abandonado el juego!"
                
                else:
                    print("Comando no reconocido. Usa: norte, sur, este, oeste, atacar <n>, ver, salir")
            
            except Exception as e:
                print(f"Error: {e}")
            
            # Verificar condiciones de fin de juego
            self.verificar_estado_juego()
        
        # Mostrar mensaje de fin de juego
        print(f"\n--- {self.motivo_fin_juego} ---")
        print("¡Gracias por jugar!")

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