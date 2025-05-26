# src/main.py
from inventario import Inventario
from storage import JsonStorage
from gui import iniciar_interfaz

if __name__ == "__main__":
    storage = JsonStorage("data/datos.json")
    inventario = Inventario(storage)
    inventario.cargar()
    iniciar_interfaz(inventario)
