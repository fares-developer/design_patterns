
from patterns.creator import *
from game import Juego


def main():
    
    try:
        print(f"####### Bienvenido al juego del Laberinto #######")
        #ejemplo de uso
        fm = Creator()
        juego = Juego()
        juego.laberinto = juego.crear_laberinto2_hab_fm(fm)
        hab1=juego.obtener_habitacion(1)
        hab2=juego.obtener_habitacion(2)
        print(hab1.num)
        print(hab2.num)

        #laberinto con paredes bomba
        print(f"\nPrueba del laberinto con paredes bomba")
        fmb = CreatorBomba()
        juego.laberinto = juego.crear_laberinto2_hab_fm(fmb)
        hab1=juego.obtener_habitacion(1)
        hab2=juego.obtener_habitacion(2)
        juego.activar_pared_bomba(hab1,"norte")
        print(hab1.norte.activa)
        print(hab2.sur.activa)

        
        #laberinto con puertas blindadas
        print(f"\nPrueba del laberinto con puertas blindadas")
        fmblind = CreatorBlindada()
        juego.laberinto = juego.crear_laberinto2_hab_fm(fmblind)
        hab1 = juego.obtener_habitacion(1)
        hab2 = juego.obtener_habitacion(2)
        juego.activar_puerta_blindada(hab1)
        print(hab1.sur.activa)
    
    except Exception as e:
        print(f"Error en el juego: {e}")
        return None
    finally:
        print("Fin del juego. Gracias por jugar.")


if __name__ == "__main__":
    main()