from gui import start_interface
from storage import load_data

if __name__ == "__main__":
    # cargar información de la base de datos
    load_data("data/datos.txt")
    
    # iniciar la interfaz gráfica
    start_interface()