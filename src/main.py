# src/main.py
from app.inventario import Inventario
from storage.storage import JsonStorage
from storage.categoria_storage import cargar_categorias, guardar_categorias
from ui.gui import iniciar_interfaz

if __name__ == "__main__":
    storage = JsonStorage("data/datos.json")
    inventario = Inventario(storage)
    inventario.cargar()
    categorias = cargar_categorias("data/categorias.json")
    # If you need to set categories in inventario, do it here:
    # inventario.set_categorias(categorias)
    iniciar_interfaz(inventario)
    guardar_categorias("data/categorias.json", categorias)

