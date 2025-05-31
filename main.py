
import sys
import os

# Añadir el directorio raíz al path para que los imports funcionen
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from patterns.director import Director

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <ruta_al_archivo_json>")
        print("Ejemplo: python main.py utils/lab4Hab.json")
        sys.exit(1)
    
    ruta_json = sys.argv[1]
    
    # Asegurarse de que la ruta sea absoluta
    if not os.path.isabs(ruta_json):
        ruta_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), ruta_json)
    
    try:
        director = Director()
        director.construir_juego(ruta_json)
    except Exception as e:
        print(f"Error al ejecutar el juego: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()