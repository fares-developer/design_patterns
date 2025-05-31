
from game import Juego

def main():
    try:
        juego = Juego()
        juego.probar_decoradores()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()