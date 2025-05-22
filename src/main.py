from gui import iniciar_interfaz
from storage import cargar_datos

if __name__ == "__main__":
    inventario = cargar_datos("data/datos.txt")
    iniciar_interfaz(inventario)
