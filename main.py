
import os
from pathlib import Path

# Añadir el directorio raíz al path para que los imports funcionen
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from patterns.director import Director

def main():
    
    # Ruta al archivo JSON del laberinto
    ruta_json = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'utils',
        'laberinto_facil.json'  # Cambia este nombre por el archivo JSON que desees cargar
    )
    
    # Verificar que el archivo exista
    if not os.path.exists(ruta_json):
        print(f"Error: No se encontró el archivo {ruta_json}")
        print("Asegúrate de que el archivo existe en la ruta especificada.")
        sys.exit(1)
    
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