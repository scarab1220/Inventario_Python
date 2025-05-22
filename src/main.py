# src/main.py
from src.inventario import Inventario
from storage import cargar_datos, guardar_datos
from gui import iniciar_interfaz

if __name__ == "__main__":
    inventario = Inventario()
    inventario.productos = cargar_datos("data/datos.json")
    iniciar_interfaz(inventario)
    guardar_datos("data/datos.json", inventario.productos)
