
from game import Juego

def main():
    try:
        juego = Juego()
        # juego.probar_decoradores()
        # juego.probar_estrategias_bomba()
        juego.probar_bichos()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()